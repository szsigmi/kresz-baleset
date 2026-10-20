#!/usr/bin/env python3
"""Kerékpáros és személygépkocsi-vezető ittas baleseti arányának vizsgálata."""

from __future__ import annotations

import csv
import html
import statistics
import subprocess
import zipfile
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from openpyxl import load_workbook


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
OUTPUT = ROOT / "output"
PACKAGE = ROOT / "beadando"
ZIP_PATH = PACKAGE / "kresz-baleset_adatcsomag_20261016_v2.zip"
PDF_PATH = PACKAGE / "osszefoglalo.pdf"
HTML_PATH = PACKAGE / "osszefoglalo.html"
CSV_PATH = PROCESSED / "kerekpar_ittas_eves.csv"
FIG_PATH = OUTPUT / "kerekpar_ittas_arany.png"

SOURCES = {
    "total": RAW / "KSH_STADAT_ege0064_okozo_eves.xlsx",
    "drunk": RAW / "KSH_STADAT_ege0066_ittas_okozo_eves.xlsx",
}
DOWNLOAD_DATE = "2026-10-16"
YEARS = range(2001, 2024)
VEHICLES = {
    "kerekpar": "Ebből: kerékpár",
    "szemelygepkocsi": "Ebből: személygépkocsi",
}


def source_values(path: Path, required_columns: tuple[str, ...]) -> dict[int, dict[str, int]]:
    """Kiolvassa az éves táblát, és megőrzi az eredeti cellaértékeket."""
    sheet = load_workbook(path, read_only=True, data_only=True).active
    rows = sheet.iter_rows(values_only=True)
    title = next(rows)
    header = next(rows)
    indexes = {name: header.index(name) for name in required_columns}
    result: dict[int, dict[str, int]] = {}
    for row in rows:
        year = row[0]
        if not isinstance(year, int):
            continue
        result[year] = {}
        for name, column in indexes.items():
            value = row[column]
            if not isinstance(value, (int, float)):
                continue
            result[year][name] = int(value)
    return result


def prepare_rows() -> list[dict[str, object]]:
    total = source_values(SOURCES["total"], ("Ebből: kerékpár", "Ebből: személygépkocsi"))
    drunk = source_values(SOURCES["drunk"], ("Ebből: kerékpár", "Ebből: személygépkocsi"))
    result = []
    matched_source_values = 0
    for year in YEARS:
        for vehicle, source_column in VEHICLES.items():
            all_count = total[year][source_column]
            drunk_count = drunk[year][source_column]
            if all_count <= 0 or drunk_count < 0 or drunk_count > all_count:
                raise ValueError(f"Érvénytelen érték: {year}, {vehicle}: {all_count}, {drunk_count}")
            matched_source_values += 2
            result.append(
                {
                    "ev": year,
                    "okozo": vehicle,
                    "osszes_baleset": all_count,
                    "ittas_baleset": drunk_count,
                    "ittas_arany": drunk_count / all_count,
                    "utana": int(year >= 2015),
                    "atmeneti": int(year == 2014),
                    "covid": int(year in (2020, 2021)),
                }
            )
    assert len(result) == 46
    assert matched_source_values == 92
    return result


def write_csv(rows: list[dict[str, object]]) -> None:
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    fields = ["ev", "okozo", "osszes_baleset", "ittas_baleset", "ittas_arany", "utana", "atmeneti", "covid"]
    with CSV_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            out = dict(row)
            out["ittas_arany"] = f"{row['ittas_arany']:.10f}"
            writer.writerow(out)


def validate_csv_against_sources() -> int:
    """Újraolvassa a CSV-t, és mindkét darabszámot a forráscella ellenőrzi."""
    total = source_values(SOURCES["total"], ("Ebből: kerékpár", "Ebből: személygépkocsi"))
    drunk = source_values(SOURCES["drunk"], ("Ebből: kerékpár", "Ebből: személygépkocsi"))
    checked = 0
    with CSV_PATH.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 46:
        raise AssertionError(f"A CSV 46 sora helyett {len(rows)} sort találtam.")
    for row in rows:
        year = int(row["ev"])
        vehicle = row["okozo"]
        source_column = VEHICLES[vehicle]
        observed_total = int(row["osszes_baleset"])
        observed_drunk = int(row["ittas_baleset"])
        if observed_total != total[year][source_column]:
            raise AssertionError(f"Összes baleset eltér a forrástól: {year}, {vehicle}")
        if observed_drunk != drunk[year][source_column]:
            raise AssertionError(f"Ittas baleset eltér a forrástól: {year}, {vehicle}")
        if abs(float(row["ittas_arany"]) - observed_drunk / observed_total) > 1e-9:
            raise AssertionError(f"Az arány hibás: {year}, {vehicle}")
        checked += 2
    if checked != 92:
        raise AssertionError(f"92 darabszám helyett {checked} cellát ellenőriztem.")
    return checked


def did_estimate(rows: list[dict[str, object]], post_end: int = 2023) -> tuple[float, dict[str, dict[str, float]]]:
    rates = {
        vehicle: {
            "pre": statistics.mean(float(r["ittas_arany"]) for r in rows if r["okozo"] == vehicle and 2001 <= r["ev"] <= 2013),
            "post": statistics.mean(float(r["ittas_arany"]) for r in rows if r["okozo"] == vehicle and 2015 <= r["ev"] <= post_end),
        }
        for vehicle in VEHICLES
    }
    delta_bike = rates["kerekpar"]["post"] - rates["kerekpar"]["pre"]
    delta_car = rates["szemelygepkocsi"]["post"] - rates["szemelygepkocsi"]["pre"]
    return delta_bike - delta_car, rates


def write_plot(rows: list[dict[str, object]]) -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
    fig, ax = plt.subplots(figsize=(9.5, 3.15), constrained_layout=True)
    colors = {"kerekpar": "#007F86", "szemelygepkocsi": "#D36B32"}
    labels = {"kerekpar": "Kerékpár", "szemelygepkocsi": "Személygépkocsi"}
    for vehicle in VEHICLES:
        subset = [r for r in rows if r["okozo"] == vehicle]
        ax.plot(
            [r["ev"] for r in subset],
            [100 * float(r["ittas_arany"]) for r in subset],
            marker="o",
            markersize=3.2,
            linewidth=1.8,
            color=colors[vehicle],
            label=labels[vehicle],
        )
    ax.axvline(2014, color="#424242", linestyle="--", linewidth=1.2, label="Hatály: 2014. július 19.")
    ax.axvspan(2014, 2015, color="#9E9E9E", alpha=.13, linewidth=0)
    ax.set_title("Ittas okozók aránya a járműtípus szerint okozott balesetekben", loc="left", weight="bold", pad=9)
    ax.set_ylabel("Ittas balesetek aránya (%)")
    ax.set_xlabel("Év")
    ax.set_xlim(2000.5, 2023.5)
    ax.set_xticks(range(2001, 2024, 2))
    ax.grid(axis="y", color="#DDE3E6", linewidth=.7)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(.5, -.18))
    fig.savefig(FIG_PATH, dpi=200, facecolor="white", bbox_inches="tight")
    plt.close(fig)


def write_package_docs(rows: list[dict[str, object]], did: float, rates: dict[str, dict[str, float]], did22: float, rates22: dict[str, dict[str, float]]) -> None:
    PACKAGE.mkdir(parents=True, exist_ok=True)
    (PACKAGE / "README.md").write_text(
        f"""# Előzetes adatcsomag — KRESZ és ittas kerékpáros okozás

Készült: {DOWNLOAD_DATE}. Az adat a KSH 2001–2023 közötti éves STADAT-tábláiból készült. A CSV 46 sora járműtípusonként 23 évet tartalmaz.

## Források

- KSH STADAT 4.1.1.50, okozó járműtípus szerinti balesetszám, XLSX: https://www.ksh.hu/stadat_files/ege/hu/ege0064.xlsx — letöltve {DOWNLOAD_DATE}. Táblalap: https://www.ksh.hu/stadat_files/ege/hu/ege0064.html
- KSH STADAT 4.1.1.52, ittas okozás és okozótípus, XLSX: https://www.ksh.hu/stadat_files/ege/hu/ege0066.xlsx — letöltve {DOWNLOAD_DATE}. Táblalap: https://www.ksh.hu/stadat_files/ege/hu/ege0066.html
- KRESZ időállapotok (26. verzió, előtte): https://njt.jog.gov.hu/jogszabaly/1975-1-20-24.26 — a projekt nyers állományának letöltése: 2026-10-12.
- KRESZ időállapotok (27. verzió, utána): https://njt.jog.gov.hu/jogszabaly/1975-1-20-24.27 — a projekt nyers állományának letöltése: 2026-10-12.
- KRESZ-változások CSV: a fenti NJT-időállapotokból előállítva; forrás-URL-enkénti leltár szerepel az `forras_url` oszlopban, nyers időállapotok letöltve 2026-10-12.
- Havi baleseti CSV: KSH Statinfo JA2A01 kézi exportok; https://statinfo.ksh.hu/Statinfo/QueryServlet?ha=JA2A01 — exportok letöltve 2026-10-12.

## Képzett mutató és előzetes eredmény

Az `ittas_arany` = `ittas_baleset / osszes_baleset`. Az egyszerű DiD a 2015–2023-as éves átlagarány és a 2001–2013-as éves átlagarány különbsége kerékpárosoknál, mínusz ugyanez személygépkocsi-vezetőknél. A számított különbség **{did*100:.3f} százalékpont**. Kerékpár: előtte {rates['kerekpar']['pre']*100:.3f}%, utána {rates['kerekpar']['post']*100:.3f}%; személygépkocsi: előtte {rates['szemelygepkocsi']['pre']*100:.3f}%, utána {rates['szemelygepkocsi']['post']*100:.3f}%.

Az érzékenységi számítás 2015–2022-re (2023 nélkül) a következő: kerékpár {rates22['kerekpar']['pre']*100:.3f}% → {rates22['kerekpar']['post']*100:.3f}%, személygépkocsi {rates22['szemelygepkocsi']['pre']*100:.3f}% → {rates22['szemelygepkocsi']['post']*100:.3f}%; DiD **{did22*100:.3f} százalékpont**.

Ez leíró, előzetes összehasonlítás, nem okozati hatásbecslés. A 2014-es átmeneti évet kizártuk az előtte/utána átlagokból; a COVID-éveket külön jelöltük. A 2022–2023-as kerékpáros arány hirtelen csökkenése lehetséges adatfelvételi törésre utalhat, de önmagában nem igazolja azt.

A 172/2014. (VII. 18.) Korm. rendelet 2014. július 19-től a főútvonalakra is kiterjesztette a kerékpárosok felmentését az alkohol jelenlétére vonatkozó tilalom alól (a befolyásoltság továbbra is tilos maradt).

## A ZIP tartalma

- `kerekpar_ittas_eves.csv` és `kerekpar_ittas_arany.png`: elemzési tábla és ábra.
- `kresz_valtozasok.csv`: KRESZ-rendelkezésenkénti változások 2010–2025 között.
- `balesetek_havi.csv`: Statinfo JA2A01 havi idősor 2011–2025 között.
- `kodkonyv.md` és `genai_modszertan.md`: változók, források, ellenőrzések és korlátok.
""",
        encoding="utf-8",
    )
    (PACKAGE / "kodkonyv.md").write_text(
        """# Kódkönyv

| Oszlop | Jelentés |
|---|---|
| `ev` | Naptári év, 2001–2023. |
| `okozo` | Okozó járműtípus: `kerekpar` vagy `szemelygepkocsi`. |
| `osszes_baleset` | Az adott típushoz tartozó, személysérüléses balesetek száma a KSH 4.1.1.50 táblájában. |
| `ittas_baleset` | Az adott típushoz tartozó, ittas okozással jelölt személysérüléses balesetek száma a KSH 4.1.1.52 táblájában. |
| `ittas_arany` | `ittas_baleset / osszes_baleset`, 0 és 1 közötti arány; a megjelenítés százalékra szorozza. |
| `utana` | 1, ha `ev >= 2015`; egyébként 0. |
| `atmeneti` | 1 a 2014-es évre, amelyben a szabály július 19-én lépett hatályba; egyébként 0. |
| `covid` | 1 a 2020-as és 2021-es évekre; egyébként 0. |

Egy sor = egy év × okozótípus. A 2024–2025-ös éveket az adat nem tartalmazza.

## `kresz_valtozasok.csv`

| Oszlop | Jelentés |
|---|---|
| `verzio_elotte`, `verzio_utana` | NJT-időállapotok sorszáma a változás előtt és után. |
| `hatalybalepes` | A változás hatálybalépésének dátuma. |
| `rendelkezes` | Megváltozott KRESZ-rendelkezés azonosítója; a függelékek sorai is szerepelnek. |
| `valtozas_tipusa` | Új, módosított vagy hatályon kívül helyezett rendelkezés. |
| `regi_szoveg`, `uj_szoveg` | A két időállapot érintett rendelkezésének szövege. |
| `modosito_jogszabaly` | A lábjegyzetből azonosított módosító jogszabály, ha rendelkezésre áll. |
| `modosito_rendelkezes` | A módosító jogszabályra utaló NJT-lábjegyzet szó szerinti szövege. |
| `forras_url` | Az összehasonlított NJT-időállapotok URL-je. |

## `balesetek_havi.csv`

| Oszlop | Jelentés |
|---|---|
| `honap` | Hónap ÉÉÉÉ-HH formában. |
| `adatkor` | Statinfo-adatkör azonosítója. |
| `dimenzio`, `kategoria`, `szulo_kategoria` | Dimenzió, kategória és igazolt hierarchikus szülő (hiányzó kapcsolatnál üres). |
| `ertek` | A forrás szerinti havi érték. |
| `ures_cella_kezelese` | Az eredeti üres cella kezelésének jelölése. |
| `forras_fajl`, `forras_oszlop` | Helyi nyers export és munkalaposzlop. |
| `forras_url` | Statinfo-lekérdezés URL-je. |
| `letoltes_datuma` | A nyers export letöltési dátuma. |
""",
        encoding="utf-8",
    )
    (PACKAGE / "genai_modszertan.md").write_text(
        """# GenAI-támogatás és ellenőrzések

## Mit végzett a genAI

- A megadott kutatási kérdést változatlanul kezelte, és a KSH 4.1.1.50 (okozó járműtípus szerinti összes baleset) és 4.1.1.52 (ittas okozás járműtípus szerint) táblákhoz feldolgozó szkriptet készített.
- A szkript a két nyers XLSX-ből gépileg kiolvassa a 2001–2023-as kerékpár- és személygépkocsi-sorokat, kiszámítja az ittas arányt, a jelzőoszlopokat, a 2015–2023-as és a 2015–2022-es egyszerű DiD-t, az ábrát, a dokumentációt és a beadandó csomagot.
- Megírta a forrásleírást, kódkönyvet, ezt a módszertani jegyzetet és az egyoldalas HTML-alapú PDF-összefoglalót.

## Mit és hogyan ellenőriztünk

- A 4.1.1.50 és 4.1.1.52 fejlécéből a kerékpár és személygépkocsi oszlopot név szerint választottuk ki; a CSV minden összes és ittas darabszámát közvetlenül összevetettük a forrás-munkafüzet megfelelő év/oszlop cellájával (46 év–típus sor, összesen 92 forrásérték).
- Ellenőriztük, hogy minden ittas balesetszám nemnegatív és nem nagyobb az adott okozótípus összes balesetszámánál; a 2024–2025-ös sorokat kizártuk.
- Az arányt a két ellenőrzött számláló és nevező hányadosaként számoltuk. A DiD-ben 2001–2013 és 2015–2023, illetve érzékenységként 2015–2022 éves arányainak egyszerű számtani átlagát használtuk; 2014 átmeneti év, nem része egyik átlagnak sem.
- A jogi váltás dátumát és szövegét a projekt 26. és 27. NJT-időállapotának szövegdiffjével ellenőriztük. A KSH-tábla 2024-es módszertani megjegyzése szerint ettől az évtől nem minden kerékpárosnál vizsgálják az ittasságot.

## Korlátok

- A 172/2014. (VII. 18.) Korm. rendelet 2014. július 19-től a főútvonalakra is kiterjesztette a kerékpárosok felmentését az alkohol jelenlétére vonatkozó tilalom alól (a befolyásoltság továbbra is tilos maradt). A KSH-adat nem bontja az eseteket úttípus szerint, ezért a ténylegesen érintett esetek nem különíthetők el.
- Évente egy megfigyelés van, a vizsgált idősor rövid (23 év × két okozótípus), és a szabály hatálybalépésének éve átmeneti.
- A COVID-időszak 2020–2021-es éveit külön jelöltük; az alap DiD ezeket tartalmazza, ezért az átlagok érzékenyek rájuk.
- A kerékpáros ittas arány 2022 és 2023 között hirtelen csökkent; ez lehetséges adatfelvételi törés, amelyet a rendelkezésre álló forrásokból nem tudtunk igazolni.
- Az ittas kerékpáros esetek mérésében 2024-től törés van, ezért 2024–2025 kimaradt.
- A személygépkocsi-vezető összehasonlító csoport, nem garantáltan érintetlen kontroll. Az egyszerű különbségek különbsége nem kontrollálja az egyidejű változásokat, és nem okozati bizonyíték.
- A százalékos arányok nevezője az okozótípushoz tartozó balesetek száma; az elemzés nem használ kitettségi adatot (például megtett kilométert vagy közlekedők számát).
""",
        encoding="utf-8",
    )


def write_html(rows: list[dict[str, object]], did: float, rates: dict[str, dict[str, float]], did22: float, rates22: dict[str, dict[str, float]]) -> None:
    vehicle_labels = {"kerekpar": "kerékpár", "szemelygepkocsi": "személygépkocsi"}
    covid = ", ".join(
        f"{vehicle_labels[v]}: {next(float(r['ittas_arany']) for r in rows if r['ev'] == 2020 and r['okozo'] == v)*100:.1f}% (2020), "
        f"{next(float(r['ittas_arany']) for r in rows if r['ev'] == 2021 and r['okozo'] == v)*100:.1f}% (2021)"
        for v in VEHICLES
    )
    HTML_PATH.write_text(
        f"""<!doctype html><html lang="hu"><head><meta charset="utf-8"><title>Kutatási összefoglaló</title>
<style>
@page {{ size: A4; margin: 9mm 11mm; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; color: #202B33; font: 9pt/1.18 Arial, sans-serif; }}
h1 {{ margin: 0 0 1.5mm; color: #102E3A; font-size: 15pt; line-height: 1.08; }}
.deck {{ color: #52636B; margin: 0 0 2mm; font-size: 9pt; }}
section {{ margin: 0 0 1.5mm; break-inside: avoid; }}
h2 {{ margin: 0 0 .6mm; font-size: 10pt; color: #007F86; border-bottom: 0.5pt solid #C7D7D8; padding-bottom: .4mm; }}
p {{ margin: 0 0 .7mm; }}
.steps {{ margin: 0; padding-left: 5mm; }} .steps li {{ margin: 0 0 .35mm; }}
.cols {{ display: grid; grid-template-columns: 1fr 1fr; gap: 4mm; }}
.figure {{ margin: .3mm 0 1.3mm; break-inside: avoid; }}
.figure img {{ display: block; width: 100%; height: 34mm; object-fit: contain; }}
.small {{ color: #506068; font-size: 9pt; }}
.stat {{ background: #EAF3F2; border-left: 2mm solid #007F86; padding: 1mm 2mm; margin: .8mm 0; }}
.foot {{ margin-top: .8mm; padding-top: .6mm; border-top: .5pt solid #C7D1D5; font-size: 9pt; color: #58666C; }}
</style></head><body>
<h1>Kerékpáros ittas okozás és a KRESZ 2014-es módosítása</h1>
<p class="deck">Előzetes, éves összehasonlítás — Magyarország, 2001–2023</p>
<section><h2>Kutatási kérdés</h2><p>Hogyan változott az ittasan okozott balesetek aránya a kerékpárosok által okozott személysérüléses balesetekben a 2014-es KRESZ-módosítás után, a személygépkocsi-vezetőkhöz képest?</p><p class="small">A 172/2014. (VII. 18.) Korm. rendelet 2014. július 19-től a főútvonalakra is kiterjesztette a kerékpárosok felmentését az alkohol jelenlétére vonatkozó tilalom alól (a befolyásoltság továbbra is tilos maradt).</p></section>
<section><h2>Empirikus anyag</h2><p>A KSH STADAT 4.1.1.50 és 4.1.1.52 éves táblái alapján 2001–2023-ra, kerékpárra és személygépkocsira számoltunk ittas baleseti arányt: ittas okozású balesetek / az adott járműtípus által okozott összes személysérüléses baleset. Ez 23 év és 46 év–járműtípus megfigyelés. 2014 átmeneti év; a COVID-éveket külön jelöltük.</p></section>
<div class="figure"><img src="{FIG_PATH.as_uri()}" alt="Ittas balesetek aránya kerékpár és személygépkocsi szerint, 2001–2023"></div>
<section><h2>Az adatbázis létrehozása</h2><ol class="steps"><li>NJT: KRESZ-időállapotok 2010–2025; 23 összevethető váltás szövegdiffje.</li><li>kresz_valtozasok.csv: 95 változás (4 hatályvesztés, 9 függeléksor); teljességi audit 62 releváns lábjegyzettel.</li><li>Statinfo havi baleseti idősor 2011–2025 (180 hónap); havi és STADAT-validálás.</li><li>A 95 módosítás szűrése mérhetőség és elkülönülés szerint; kiválasztva a 2014-es 4. § (4).</li><li>KSH STADAT 4.1.1.50 és 4.1.1.52 letöltése; 2024–2025 kizárása a módszertani törés miatt.</li><li>kerekpar_ittas_eves.csv: 46 sor, 92 forráscella-összevetés, automatikus ellenőrzés; scripts/05_kerekpar_ittas_elemzes.py.</li><li>Codex CLI genAI-ügynök, Python virtuális környezet, Git-verziókezelés privát GitHub-tárolóval és változásnapló.</li></ol><p>A genAI a források feldolgozását és dokumentálását segítette; a jogi változásokat forrásszöveggel, az adatokat programozott összevetéssel ellenőriztük.</p></section>
<section><h2>Módszertan</h2><div class="cols"><div><p>Leíró DiD: a 2015–2023 és a 2001–2013 közötti éves átlagarány-változás különbsége; 2014 egyik átlagban sincs. Érzékenység: 2023 nélkül, 2015–2022.</p><div class="stat"><b>DiD 2015–2023: {did*100:+.3f} százalékpont; 2015–2022: {did22*100:+.3f} százalékpont</b><br><span class="small">2001–2013 → 2015–2022: kerékpár {rates22['kerekpar']['pre']*100:.2f}% → {rates22['kerekpar']['post']*100:.2f}%; személygépkocsi {rates22['szemelygepkocsi']['pre']*100:.2f}% → {rates22['szemelygepkocsi']['post']*100:.2f}%.</span></div></div><div><p><b>Korlátok.</b> Csak a főútvonali kivétel szűnt meg; az adat nem bont úttípus szerint. Évente egy adatpont van. A COVID-éveket külön jelöltük ({html.escape(covid)}). A 2022–2023-as kerékpáros csökkenés lehetséges adatfelvételi törés. 2024–2025 a módszertani törés miatt kimaradt.</p><p>Az egyszerű DiD nem kontrollálja az egyidejű változásokat; nem okozati bizonyíték.</p></div></div></section>
<p class="foot">Forrás: KSH STADAT 4.1.1.50 és 4.1.1.52, letöltve 2026-10-16. Feldolgozás: scripts/05_kerekpar_ittas_elemzes.py. Súlyozatlan éves átlagarányok.</p>
</body></html>""",
        encoding="utf-8",
    )


def write_pdf() -> None:
    chrome = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    if not chrome.exists():
        raise FileNotFoundError("A kért Chrome headless PDF-készítéshez nem található a Google Chrome.")
    PDF_PATH.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            str(chrome), "--headless", "--disable-gpu", "--no-sandbox", "--no-pdf-header-footer",
            f"--print-to-pdf={PDF_PATH}", HTML_PATH.as_uri(),
        ],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )


def write_zip() -> None:
    PACKAGE.mkdir(parents=True, exist_ok=True)
    members = {
        CSV_PATH: "kerekpar_ittas_eves.csv",
        PROCESSED / "kresz_valtozasok.csv": "kresz_valtozasok.csv",
        PROCESSED / "balesetek_havi.csv": "balesetek_havi.csv",
        FIG_PATH: "kerekpar_ittas_arany.png",
        PACKAGE / "README.md": "README.md",
        PACKAGE / "kodkonyv.md": "kodkonyv.md",
        PACKAGE / "genai_modszertan.md": "genai_modszertan.md",
    }
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for source, name in members.items():
            zf.write(source, arcname=name)


def main() -> None:
    rows = prepare_rows()
    did, rates = did_estimate(rows)
    did22, rates22 = did_estimate(rows, post_end=2022)
    write_csv(rows)
    checked = validate_csv_against_sources()
    write_plot(rows)
    write_package_docs(rows, did, rates, did22, rates22)
    write_html(rows, did, rates, did22, rates22)
    write_pdf()
    write_zip()
    print(f"Forrásegyezés: {len(rows)} sor, {checked} darabszámcella ellenőrizve.")
    print(f"DiD = {did * 100:+.6f} százalékpont")
    print(f"DiD 2015–2022 (2023 nélkül) = {did22 * 100:+.6f} százalékpont")
    print(f"CSV: {CSV_PATH}")
    print(f"Ábra: {FIG_PATH}")
    print(f"PDF: {PDF_PATH}")
    print(f"ZIP: {ZIP_PATH}")


if __name__ == "__main__":
    main()
