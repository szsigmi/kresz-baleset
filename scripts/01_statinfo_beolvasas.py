"""Statinfo Excel-exportok beolvasása hosszú havi táblába."""
from pathlib import Path
import re
import csv
import openpyxl
from hierarchia import elfogadott_szulok, fejlec_sor as hier_fejlec_sor, havi_adatok

GYOKER = Path(__file__).resolve().parents[1]
NYERS = GYOKER / "data/raw"
KIMENET = GYOKER / "data/processed/balesetek_havi.csv"
HONAPOK = {"január": 1, "február": 2, "március": 3, "április": 4,
           "május": 5, "június": 6, "július": 7, "augusztus": 8,
           "szeptember": 9, "október": 10, "november": 11, "december": 12}
FORRAS_URL = "https://statinfo.ksh.hu/Statinfo/QueryServlet?ha=JA2A01"
LETOLTES_DATUMA = "2026-10-12"

def szoveg(x):
    return " ".join(str(x).split()) if x is not None else ""

def honap_sor(x):
    m = re.fullmatch(r"(20\d{2})\.\s+([\wáéíóöőúüű]+)", szoveg(x), re.I)
    if not m or m.group(2).lower() not in HONAPOK:
        return None
    ev = int(m.group(1))
    return f"{ev:04d}-{HONAPOK[m.group(2).lower()]:02d}" if 2011 <= ev <= 2025 else None

def main():
    fajlok = sorted(NYERS.glob("statinfo_JA2A0*_*.xlsx"))
    fajlok = [p for p in fajlok if p.name != "statinfo_JA2A01_elso_proba.xlsx"]
    rekordok = []
    for fajl in fajlok:
        wb = openpyxl.load_workbook(fajl, data_only=True)
        ws = wb.active
        adatkor = ws.title
        fejlec_sor = next(i for i in range(6, min(ws.max_row, 12) + 1)
                          if szoveg(ws.cell(i, 1).value).lower() == "időszak")
        # Az összevont fejlécet kitöltjük; az utolsó oszlopcímek adják a kategóriákat.
        # A dimenziócímeket az összevont, többsoros fejlécből töltjük ki oszloponként.
        dim_oszlop = {}
        for c in range(2, ws.max_column + 1):
            talalat = ""
            for r in range(6, fejlec_sor):
                v = szoveg(ws.cell(r, c).value)
                if not v:
                    for tartomany in ws.merged_cells.ranges:
                        if tartomany.min_row == r and tartomany.min_col <= c <= tartomany.max_col:
                            v = szoveg(ws.cell(r, tartomany.min_col).value)
                            break
                if v and not v.lower().startswith("mindösszesen"):
                    talalat = v
            if not talalat and szoveg(ws.cell(fejlec_sor, c).value) and c == 2:
                talalat = szoveg(ws.cell(fejlec_sor, c).value)
            dim_oszlop[c] = talalat or "Mutató"
        szulok = elfogadott_szulok(ws, dim_oszlop.get(3, ""))
        # Az ismétlődő, azonos kategórianév és havi sorozat ugyanazt az igazolt ágat jelöli.
        if szulok:
            rows = havi_adatok(ws)
            for child, parent_name in list(szulok.items()):
                child_name = szoveg(ws.cell(fejlec_sor, child).value)
                child_values = tuple(ws.cell(rows[k], child).value for k in sorted(rows))
                for other in range(2, ws.max_column + 1):
                    if (szoveg(ws.cell(fejlec_sor, other).value) == child_name
                            and tuple(ws.cell(rows[k], other).value for k in sorted(rows)) == child_values):
                        szulok[other] = parent_name
        # A fix dimenziók szövege a kért negyedik fejlécsorban van.
        fix = szoveg(ws.cell(4, 1).value)
        idx_osszes = next((c for c in range(2, ws.max_column + 1)
                           if szoveg(ws.cell(fejlec_sor, c).value).lower().startswith("mindösszesen")), None)
        elso_ertek = {}
        for c in range(2, ws.max_column + 1):
            elso_ertek[c] = next((honap_sor(ws.cell(r, 1).value) for r in range(fejlec_sor + 1, ws.max_row + 1)
                                  if honap_sor(ws.cell(r, 1).value) and ws.cell(r, c).value is not None), None)
        idx_havi = []
        for r in range(fejlec_sor + 1, ws.max_row + 1):
            h = honap_sor(ws.cell(r, 1).value)
            if not h:
                continue
            # A sor kategóriaértékei csak akkor kapnak 0-t, ha a teljes összeg ezt igazolja.
            osszes = ws.cell(r, idx_osszes).value if idx_osszes else None
            oszlopok = [c for c in range(2, ws.max_column + 1) if c != idx_osszes]
            ertekek = [ws.cell(r, c).value for c in oszlopok]
            osszeg = sum(float(x) for x in ertekek if isinstance(x, (int, float)))
            uresek_potolhetok = (osszes is not None and all(x is not None or osszeg == float(osszes)
                                                            for x in ertekek)
                                 and osszeg == float(osszes))
            for c in range(2, ws.max_column + 1):
                kategoria = szoveg(ws.cell(fejlec_sor, c).value)
                value = ws.cell(r, c).value
                kezeles = "eredeti érték"
                if value is None:
                    if c == idx_osszes:
                        kezeles = "üres összesen: hiányzó"
                    elif elso_ertek[c] is None or h < elso_ertek[c]:
                        kezeles = "hiányzó: a kategória még nem szerepelt; módszertani törés"
                    elif uresek_potolhetok:
                        value, kezeles = 0, "0-ra állítva: kategóriaösszeg=Mindösszesen"
                    else:
                        kezeles = "üres, nem igazolható nullaként"
                if value is not None and not isinstance(value, (int, float)):
                    continue
                rekordok.append({"honap": h, "adatkor": adatkor, "dimenzio": dim_oszlop[c],
                    "kategoria": kategoria, "szulo_kategoria": szulok.get(c, ""),
                    "ertek": value, "ures_cella_kezelese": kezeles,
                    "forras_fajl": fajl.name, "forras_oszlop": c, "forras_url": FORRAS_URL,
                    "letoltes_datuma": LETOLTES_DATUMA})
        wb.close()
    KIMENET.parent.mkdir(parents=True, exist_ok=True)
    with KIMENET.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["honap", "adatkor", "dimenzio", "kategoria", "szulo_kategoria", "ertek",
            "ures_cella_kezelese", "forras_fajl", "forras_oszlop", "forras_url", "letoltes_datuma"],
            lineterminator="\n")
        w.writeheader(); w.writerows(rekordok)
    print(f"{len(rekordok)} havi rekord: {KIMENET}")

if __name__ == "__main__":
    main()
