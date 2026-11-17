#!/usr/bin/env python3
"""Az irány-kódolás ellenőrzése és összesítése (vclassify → vcoder-agreement).

Bemenet:
  data/processed/iranykod/labels.csv        gépi címkék (Codex, $vclassify)
  data/processed/iranykod/hand.csv          kézi, vak kódolás a 25 elemű mintán (file, code)
  data/processed/iranykod/szovegek/*.txt    a kódolt szövegek (08_iranykod_elokeszites.py)
  data/final/kresz_valtozasok.csv
  data/raw/kezi_kodolas/szabalyozasi_szint_alkohol.csv
Kimenet:
  data/final/kresz_valtozasok_irany.csv     95 sor: valtozas_id + irány, csoport, terület, indoklás, idézet
  data/final/szabalyozasi_szint_alkohol.csv a kézi szintskála, ellenőrzött hivatkozásokkal
  output/iranykod_egyezes.md                címke-ellenőrzés, egyezés, kappa, kategóriánként, eltérések
  output/iranykod_elteresek.csv, output/iranykod_evente.csv
Futtatás: .venv/bin/python scripts/09_iranykod_osszesites.py
"""
from __future__ import annotations

import csv
import re
import shutil
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IK = ROOT / "data" / "processed" / "iranykod"
FINAL = ROOT / "data" / "final"
OUT = ROOT / "output"
KODOK = ["SZIGORITAS", "ENYHITES", "SEMLEGES", "VEGYES", "NEM_BESOROLHATO"]
FELRETETT = {"NEM_BESOROLHATO"}


def olvas(p: Path) -> list[dict[str, str]]:
    with p.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def norm(s: str) -> str:
    s = s.replace("’", "'").replace("„", '"').replace("”", '"').replace("“", '"')
    return re.sub(r"\s+", " ", s).strip().lower()


def main() -> None:
    valtozasok = {s["valtozas_id"]: s for s in olvas(FINAL / "kresz_valtozasok.csv")}
    cimkek = olvas(IK / "labels.csv")
    kezi = {s["file"].strip(): s["code"].strip() for s in olvas(IK / "hand.csv") if s["code"].strip()}
    hibak: list[str] = []

    # 1. Címke-ellenőrzés (a vclassify label_check.py logikája szerint)
    fajlok = sorted(p.name for p in (IK / "szovegek").glob("*.txt"))
    db = Counter(s["file"].strip() for s in cimkek)
    for f in fajlok:
        if db[f] != 1:
            hibak.append(f"{f}: {db[f]} címkesor")
    for s in cimkek:
        f, c, mondat = s["file"].strip(), s["code"].strip(), (s.get("sentence") or "").strip()
        if f not in fajlok:
            hibak.append(f"ismeretlen fájl: {f}")
            continue
        if c not in KODOK:
            hibak.append(f"{f}: nem megengedett kód: {c!r}")
        if c not in FELRETETT and norm(mondat) not in norm((IK / "szovegek" / f).read_text(encoding="utf-8")):
            hibak.append(f"{f}: az idézett mondat nem szerepel szó szerint a szövegben")
    kodolt = sum(1 for s in cimkek if s["code"].strip() not in FELRETETT)
    felretett = sum(1 for s in cimkek if s["code"].strip() in FELRETETT)
    if kodolt + felretett != len(fajlok):
        hibak.append(f"a darabszám nem zárul: {len(fajlok)} fájl ≠ {kodolt} kódolt + {felretett} félretett")

    # 2. Egyezés a kézi kódolással (vcoder-agreement)
    gep = {s["file"].strip(): s["code"].strip() for s in cimkek}
    parok = [(kezi[f], gep[f]) for f in sorted(kezi) if f in gep]
    n = len(parok)
    po = sum(a == b for a, b in parok) / n
    ca, cb = Counter(a for a, _ in parok), Counter(b for _, b in parok)
    pe = sum(ca[c] / n * cb[c] / n for c in set(ca) | set(cb))
    kappa = (po - pe) / (1 - pe) if pe < 1 else 1.0
    kategoriak = []
    for c in KODOK:
        tp = sum(1 for a, b in parok if a == c and b == c)
        pred, val = sum(1 for _, b in parok if b == c), ca[c]
        kategoriak.append((c, val, val / n, tp / pred if pred else None, tp / val if val else None))
    elteresek = [(f, kezi[f], gep[f]) for f in sorted(kezi) if f in gep and kezi[f] != gep[f]]
    with (OUT / "iranykod_elteresek.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["file", "kezi", "gepi", "gepi_indoklas", "idezet"])
        cim = {s["file"].strip(): s for s in cimkek}
        for f, a, b in elteresek:
            w.writerow([f, a, b, cim[f].get("reason", ""), cim[f].get("sentence", "")])

    # 3. Végleges tábla és éves összesítés
    with (FINAL / "kresz_valtozasok_irany.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["valtozas_id", "hatalybalepes", "rendelkezes", "irany", "csoport", "terulet", "indoklas",
                    "idezet", "kodolo_modell", "prompt_verzio", "kezi_irany"])
        for s in sorted(cimkek, key=lambda x: x["file"]):
            vid = s["file"].strip()[:-4]
            v = valtozasok[vid]
            w.writerow([vid, v["hatalybalepes"], v["rendelkezes"], s["code"].strip(), s.get("csoport", ""),
                        s.get("terulet", ""), s.get("reason", ""), s.get("sentence", ""), s.get("model", ""),
                        s.get("prompt_version", ""), kezi.get(s["file"].strip(), "")])
    evente = Counter((valtozasok[s["file"].strip()[:-4]]["hatalybalepes"][:4], s["code"].strip()) for s in cimkek)
    evek = sorted({e for e, _ in evente})
    with (OUT / "iranykod_evente.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["ev", *KODOK, "osszes"])
        for e in evek:
            w.writerow([e, *[evente[(e, c)] for c in KODOK], sum(evente[(e, c)] for c in KODOK)])

    # 4. A kézi szintskála ellenőrzése és átvétele
    szint = olvas(ROOT / "data" / "raw" / "kezi_kodolas" / "szabalyozasi_szint_alkohol.csv")
    for s in szint:
        if s["valtozas_id"] and s["valtozas_id"] not in valtozasok:
            hibak.append(f"szintskála: ismeretlen valtozas_id {s['valtozas_id']}")
        if s["szint"] not in {"0", "1", "2", "3"}:
            hibak.append(f"szintskála: érvénytelen szint {s['szint']}")
    shutil.copyfile(ROOT / "data" / "raw" / "kezi_kodolas" / "szabalyozasi_szint_alkohol.csv",
                    FINAL / "szabalyozasi_szint_alkohol.csv")

    # 5. Jelentés
    pct = lambda x: "–" if x is None else f"{x*100:.0f}%"
    gy = Counter(s["code"].strip() for s in cimkek)
    sorok = ["# Irány-kódolás: ellenőrzés és egyezés (scripts/09_iranykod_osszesites.py)", "",
             f"Címke-ellenőrzés: {len(fajlok)} fájl · {len(cimkek)} címkesor · {kodolt} kódolt · {felretett} félretett · "
             f"hibák: {len(hibak)}", ""]
    sorok += [f"- HIBA: {h}" for h in hibak] + ([""] if hibak else [])
    sorok += ["## Gépi kódok gyakorisága (95 változás)", "", "| Kód | Db |", "|---|---:|"]
    sorok += [f"| {c} | {gy[c]} |" for c in KODOK]
    sorok += ["", f"## Egyezés a kézi kódolással (n = {n})", "",
              f"Pontos egyezés: {po*100:.0f}% · Cohen-féle kappa: {kappa:.2f}", "",
              "| Kód | n (kézi) | Arány | Pontosság (gép) | Felidézés (gép) |", "|---|---:|---:|---:|---:|"]
    for c, val, arany, prec, rec in kategoriak:
        megj = " (n < 10: nincs ítélet)" if val < 10 else ""
        sorok.append(f"| {c}{megj} | {val} | {arany*100:.0f}% | {pct(prec)} | {pct(rec)} |")
    sorok += ["", f"Eltérések: {len(elteresek)} → output/iranykod_elteresek.csv", ""]
    sorok += [f"- {f}: kézi {a}, gépi {b}" for f, a, b in elteresek]
    (OUT / "iranykod_egyezes.md").write_text("\n".join(sorok) + "\n", encoding="utf-8")
    print("\n".join(sorok))
    if hibak:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
