#!/usr/bin/env python3
"""A kutatási kérdés elemzése: a kerékpárosok és a személygépkocsi-vezetők ittas
okozási aránya a kerékpárosok alkoholszabályának két enyhítése (2012, 2014) előtt és után.

Bemenet:
  data/final/kerekpar_ittas_eves.csv                     (a 06_validalas.py állítja elő)
  data/raw/kezi_kodolas/szabalyozasi_szint_alkohol.csv   (kézzel kódolt szintskála, NJT alapján)
Kimenet:
  output/elemzes_leiro.csv, output/elemzes_osszefoglalo_statisztika.csv,
  output/elemzes_robusztussag.csv, output/elemzes_placebo.csv, output/elemzes_eredmenyek.md,
  output/abra1_ittas_arany.png, output/abra2_kulonbseg.png

A szkript csak olvassa az adatokat. Függőség: numpy, matplotlib (a requirements.txt része).
Futtatás a projekt gyökeréből:  .venv/bin/python scripts/07_elemzes.py
"""
from __future__ import annotations

import csv
from datetime import date
from pathlib import Path
from statistics import NormalDist

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "final" / "kerekpar_ittas_eves.csv"
SZINT = ROOT / "data" / "raw" / "kezi_kodolas" / "szabalyozasi_szint_alkohol.csv"
OUT = ROOT / "output"

COVID_EVEK = {2020, 2021}
NW_LAG = 2                  # Newey–West késleltetés az autokorrelált éves különbségekhez
Z = NormalDist().inv_cdf(0.975)
SZINC = {3: "#e9eef0", 2: "#d6e6e6", 1: "#c3dede"}


def beolvas() -> dict[int, dict[str, dict[str, float]]]:
    """Évenként és okozónként: összes baleset, ittas baleset, ittas arány."""
    adat: dict[int, dict[str, dict[str, float]]] = {}
    with DATA.open(encoding="utf-8") as f:
        for sor in csv.DictReader(f):
            adat.setdefault(int(sor["ev"]), {})[sor["okozo"]] = {
                "osszes": int(sor["osszes_baleset"]),
                "ittas": int(sor["ittas_baleset"]),
                "arany": float(sor["ittas_arany"]),
            }
    hianyos = [ev for ev, d in adat.items() if set(d) != {"kerekpar", "szemelygepkocsi"}]
    if hianyos:
        raise SystemExit(f"Hiányos évek a bemenetben: {hianyos}")
    return adat


def kerekparos_szint(evek: list[int]) -> tuple[dict[int, int | None], list[date]]:
    """Az alkohol-szintskála évenként a kerékpárosokra. Ha egy évben szintváltás volt,
    az év átmeneti (None). Visszaadja a váltások dátumait is."""
    with SZINT.open(encoding="utf-8") as f:
        sorok = [s for s in csv.DictReader(f) if s["csoport"] == "kerekparos"]
    szakaszok = []
    for s in sorok:
        tol = date.fromisoformat(s["ervenyes_tol"]) if s["ervenyes_tol"] else date(1900, 1, 1)
        ig = date.fromisoformat(s["ervenyes_ig"]) if s["ervenyes_ig"] else date(2100, 12, 31)
        szakaszok.append((tol, ig, int(s["szint"])))
    valtasok = sorted(t for t, _, _ in szakaszok if t.year > 1900)
    szint: dict[int, int | None] = {}
    for ev in evek:
        ervenyes = {sz for tol, ig, sz in szakaszok if tol <= date(ev, 12, 31) and ig >= date(ev, 1, 1)}
        szint[ev] = ervenyes.pop() if len(ervenyes) == 1 else None
    return szint, valtasok


def ols_nw(y: np.ndarray, X: np.ndarray, lag: int = NW_LAG) -> tuple[np.ndarray, np.ndarray]:
    """OLS-becslés Newey–West (HAC) standard hibákkal. Visszaad: együtthatók, SE-k."""
    XtX_inv = np.linalg.inv(X.T @ X)
    b = XtX_inv @ X.T @ y
    e = y - X @ b
    n = len(y)
    S = (X * e[:, None]).T @ (X * e[:, None])
    for l in range(1, lag + 1):
        w = 1 - l / (lag + 1)
        G = (X[l:] * e[l:, None]).T @ (X[:-l] * e[:-l, None])
        S += w * (G + G.T)
    V = XtX_inv @ S @ XtX_inv * n / (n - X.shape[1])
    return b, np.sqrt(np.diag(V))


def kulonbseg(adat, t: int) -> float:
    """Az éves arány-különbség: kerékpáros − személygépkocsis ittas arány."""
    return adat[t]["kerekpar"]["arany"] - adat[t]["szemelygepkocsi"]["arany"]


def becsles(adat, x: dict[int, float], trend: bool = False) -> dict[str, float]:
    """d_t = a + beta * x_t (+ c * (t − 2014)) + e_t, Newey–West SE-vel.
    Ha x 0/1 (előtte/utána), beta a különbségek különbsége; ha x a lazítás foka, beta lépésenkénti hatás."""
    evek = sorted(x)
    d = np.array([kulonbseg(adat, t) for t in evek])
    oszlopok = [np.ones(len(evek)), np.array([x[t] for t in evek], dtype=float)]
    if trend:
        oszlopok.append(np.array([t - 2014 for t in evek], dtype=float))
    b, se = ols_nw(d, np.column_stack(oszlopok))
    return {"becsles": b[1], "se": se[1], "ci_also": b[1] - Z * se[1], "ci_felso": b[1] + Z * se[1],
            "n_ev": len(evek)}


def main() -> None:
    adat = beolvas()
    OUT.mkdir(exist_ok=True)
    evek = sorted(adat)
    szint, valtasok = kerekparos_szint(evek)
    zero = [t for t in evek if szint[t] == 3]          # teljes zéró tolerancia (2001–2011)
    reszleges = [t for t in evek if szint[t] == 2]     # főútvonalon tilos (2013)
    laza = [t for t in evek if szint[t] == 1]          # csak a vezetésre képtelen állapot tilos (2015–)
    atmeneti = [t for t in evek if szint[t] is None]   # szintváltás éve (2012, 2014)

    # 1. Mintaszűkítés és összefoglaló statisztika (vdescriptives)
    elemzett = zero + reszleges + laza
    valtozok = {
        "Ittas arány, kerékpáros okozó (%)": [adat[t]["kerekpar"]["arany"] * 100 for t in elemzett],
        "Ittas arány, személygépkocsi-vezető okozó (%)": [adat[t]["szemelygepkocsi"]["arany"] * 100 for t in elemzett],
        "Különbség (százalékpont)": [kulonbseg(adat, t) * 100 for t in elemzett],
        "Balesetek, kerékpáros okozó (db/év)": [adat[t]["kerekpar"]["osszes"] for t in elemzett],
        "Balesetek, személygépkocsi-vezető okozó (db/év)": [adat[t]["szemelygepkocsi"]["osszes"] for t in elemzett],
        "Lazítás foka (0–2)": [3 - szint[t] for t in elemzett],
    }
    osszefoglalo = [{"valtozo": k, "n": len(v), "atlag": float(np.mean(v)), "szoras": float(np.std(v, ddof=1)),
                     "min": float(np.min(v)), "max": float(np.max(v))} for k, v in valtozok.items()]
    with (OUT / "elemzes_osszefoglalo_statisztika.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(osszefoglalo[0]))
        w.writeheader()
        w.writerows(osszefoglalo)

    # 2. Leíró táblázat: átlagos arány a szintskála szakaszaiban
    leiro = []
    for okozo, nev in (("kerekpar", "Kerékpáros okozó"), ("szemelygepkocsi", "Személygépkocsi-vezető okozó")):
        sor = {"csoport": nev}
        for kulcs, evlista in (("zero_2001_2011", zero), ("reszleges_2013", reszleges), ("laza_2015_2023", laza)):
            sor[kulcs] = float(np.mean([adat[t][okozo]["arany"] for t in evlista]))
        sor["valtozas_zero_laza"] = sor["laza_2015_2023"] - sor["zero_2001_2011"]
        leiro.append(sor)
    did_atlag = leiro[0]["valtozas_zero_laza"] - leiro[1]["valtozas_zero_laza"]
    with (OUT / "elemzes_leiro.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(leiro[0]))
        w.writeheader()
        w.writerows(leiro)

    # 3. Fő becslés és robusztussági változatok
    def elo_uto(elott, utana):
        return {**{t: 0.0 for t in elott}, **{t: 1.0 for t in utana}}

    valtozatok = [
        ("Fő becslés: zéró tolerancia (2001–2011) vs. teljes lazítás (2015–2023)", elo_uto(zero, laza), False),
        ("Lépésenként: a lazítás foka (0–2), 2013-mal együtt", {t: float(3 - szint[t]) for t in elemzett}, False),
        ("2023 nélkül", elo_uto(zero, [t for t in laza if t != 2023]), False),
        ("2022–2023 nélkül", elo_uto(zero, [t for t in laza if t < 2022]), False),
        ("COVID-évek (2020–2021) nélkül", elo_uto(zero, [t for t in laza if t not in COVID_EVEK]), False),
        ("Szűk ablak: 2007–2011 vs. 2015–2019", elo_uto([t for t in zero if t >= 2007], [t for t in laza if t <= 2019]), False),
        ("Lineáris trenddel (megszakított idősor)", elo_uto(zero, laza), True),
        ("Régi felosztás: 2001–2013 vs. 2015–2023", elo_uto([t for t in evek if t <= 2013], laza), False),
    ]
    robusztus = [{"valtozat": nev, **becsles(adat, x, trend)} for nev, x, trend in valtozatok]
    with (OUT / "elemzes_robusztussag.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(robusztus[0]))
        w.writeheader()
        w.writerows(robusztus)

    # 4. Placebo-időpontok: ál-módosítás a zéró toleranciás és a laza szakaszon belül
    placebo = []
    for ev in range(2004, 2010):
        placebo.append({"placebo_ev": ev, "idoszak": "2001–2011",
                        **becsles(adat, elo_uto([t for t in zero if t < ev], [t for t in zero if t >= ev]))})
    for ev in range(2018, 2021):
        placebo.append({"placebo_ev": ev, "idoszak": "2015–2023",
                        **becsles(adat, elo_uto([t for t in laza if t < ev], [t for t in laza if t >= ev]))})
    with (OUT / "elemzes_placebo.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(placebo[0]))
        w.writeheader()
        w.writerows(placebo)

    # 5. Ábrák
    k = [adat[t]["kerekpar"]["arany"] * 100 for t in evek]
    s = [adat[t]["szemelygepkocsi"]["arany"] * 100 for t in evek]
    d = [a - b for a, b in zip(k, s)]
    vonalak = [v.year + (v.timetuple().tm_yday - 1) / 365 - 0.5 for v in valtasok]  # év-középpontos tengely

    def hatter(ax):
        ax.axvspan(evek[0] - 0.6, vonalak[0], color=SZINC[3], lw=0, zorder=0)
        ax.axvspan(vonalak[0], vonalak[1], color=SZINC[2], lw=0, zorder=0)
        ax.axvspan(vonalak[1], evek[-1] + 0.6, color=SZINC[1], lw=0, zorder=0)
        for v in vonalak:
            ax.axvline(v, color="#444", ls="--", lw=0.9)
        ax.set_xlim(evek[0] - 0.6, evek[-1] + 0.6)
        ax.set_xticks(range(2001, 2024, 2))
        ax.spines[["top", "right"]].set_visible(False)

    fig, ax = plt.subplots(figsize=(7.2, 2.9))
    hatter(ax)
    ax.plot(evek, k, marker="o", ms=3.5, lw=1.8, color="#0f6f73", label="Kerékpáros okozó")
    ax.plot(evek, s, marker="o", ms=3.5, lw=1.8, color="#b5651d", label="Személygépkocsi-vezető okozó")
    ax.text(2006, 28.3, "kerékpáros szint: 3", fontsize=7.5, color="#333", ha="center")
    ax.text((vonalak[0] + vonalak[1]) / 2, 28.3, "2", fontsize=7.5, color="#333", ha="center")
    ax.text(2019, 28.3, "kerékpáros szint: 1", fontsize=7.5, color="#333", ha="center")
    ax.set_ylabel("Ittas okozás aránya (%)")
    ax.set_ylim(0, 30)
    ax.grid(axis="y", alpha=0.3)
    ax.legend(frameon=False, fontsize=8, loc="lower left")
    fig.tight_layout()
    fig.savefig(OUT / "abra1_ittas_arany.png", dpi=220, facecolor="white")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.2, 2.5))
    hatter(ax)
    ax.bar(evek, d, color=["#9aa5ab" if szint[t] is None else "#0f6f73" for t in evek], width=0.7, zorder=2)
    for evlista, szin, felirat in ((zero, "#b5651d", "Átlag 2001–2011"), (laza, "#7a1f1f", "Átlag 2015–2023")):
        m = float(np.mean([kulonbseg(adat, t) * 100 for t in evlista]))
        ax.hlines(m, evlista[0] - 0.4, evlista[-1] + 0.4, color=szin, lw=2, zorder=3,
                  label=f"{felirat}: {m:.1f} pp".replace(".", ","))
    ax.set_ylabel("Különbség (százalékpont)")
    ax.grid(axis="y", alpha=0.3, zorder=1)
    ax.legend(frameon=False, fontsize=8, loc="lower center", ncol=2, bbox_to_anchor=(0.5, 1.0))
    fig.tight_layout()
    fig.savefig(OUT / "abra2_kulonbseg.png", dpi=220, facecolor="white")
    plt.close(fig)

    # 6. Összefoglaló a kimenetek ellenőrzéséhez
    sz = lambda v: f"{v:.2f}".replace(".", ",")
    sorok = ["# Elemzési eredmények (scripts/07_elemzes.py)", "",
             f"Bemenet: {len(evek)} év × 2 okozó = {2 * len(evek)} sor. Átmeneti (szintváltási) évek, kihagyva: "
             f"{', '.join(map(str, atmeneti))}. Elemzett: {len(elemzett)} év × 2 = {2 * len(elemzett)} sor.", "",
             "## Összefoglaló statisztika (elemzett évek)", "",
             "| Változó | N | Átlag | Szórás | Min. | Max. |", "|---|---:|---:|---:|---:|---:|"]
    for r in osszefoglalo:
        sorok.append(f"| {r['valtozo']} | {r['n']} | {sz(r['atlag'])} | {sz(r['szoras'])} | {sz(r['min'])} | {sz(r['max'])} |")
    sorok += ["", "## Átlagos ittas arány a szintskála szakaszaiban", "",
              "| Csoport | 2001–2011 (3) | 2013 (2) | 2015–2023 (1) | Változás 3→1 (pp) |", "|---|---:|---:|---:|---:|"]
    for r in leiro:
        sorok.append(f"| {r['csoport']} | {sz(r['zero_2001_2011']*100)}% | {sz(r['reszleges_2013']*100)}% | "
                     f"{sz(r['laza_2015_2023']*100)}% | {sz(r['valtozas_zero_laza']*100)} |")
    sorok += ["", f"Különbségek különbsége (átlagokból, 2001–2011 vs. 2015–2023): {sz(did_atlag*100)} pp", "",
              "## Becslések (pp, Newey–West SE, késleltetés: 2)", "",
              "| Változat | Becslés | SE | 95% CI | Évek |", "|---|---:|---:|---|---:|"]
    for r in robusztus:
        sorok.append(f"| {r['valtozat']} | {sz(r['becsles']*100)} | {sz(r['se']*100)} | "
                     f"[{sz(r['ci_also']*100)}; {sz(r['ci_felso']*100)}] | {r['n_ev']} |")
    sorok += ["", "## Placebo-időpontok", "", "| Placebo-év | Szakasz | Becslés (pp) | 95% CI |", "|---:|---|---:|---|"]
    for r in placebo:
        sorok.append(f"| {r['placebo_ev']} | {r['idoszak']} | {sz(r['becsles']*100)} | "
                     f"[{sz(r['ci_also']*100)}; {sz(r['ci_felso']*100)}] |")
    (OUT / "elemzes_eredmenyek.md").write_text("\n".join(sorok) + "\n", encoding="utf-8")
    print("\n".join(sorok))


if __name__ == "__main__":
    main()
