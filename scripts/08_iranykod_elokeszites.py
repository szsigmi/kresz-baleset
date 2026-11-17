#!/usr/bin/env python3
"""Az irány-kódolás előkészítése (vcodebook → vclassify → vcoder-agreement).

1. Minden KRESZ-változásból egy szövegfájlt készít a gépi kódoláshoz:
   data/processed/iranykod/szovegek/<valtozas_id>.txt
2. Kihúzza a kézi (vak) kódolás 25 elemű véletlen mintáját (mag = 1), a
   kódkönyv példáiként használt változások nélkül:
   data/processed/iranykod/kezi_minta.csv  (file, code – a code oszlopot kézzel kell kitölteni)

Bemenet: data/final/kresz_valtozasok.csv. A szkript nem módosít adatot.
Futtatás: .venv/bin/python scripts/08_iranykod_elokeszites.py
"""
from __future__ import annotations

import csv
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BE = ROOT / "data" / "final" / "kresz_valtozasok.csv"
KI = ROOT / "data" / "processed" / "iranykod"
SZOVEGEK = KI / "szovegek"
MINTA = KI / "kezi_minta.csv"
MINTA_MERET = 25
MAG = 1
# A kódkönyvben (docs/iranykod_kodkonyv.md) példaként használt egységek nem kerülhetnek a próbamintába.
KODKONYV_PELDAK = {
    "K2013-07-01_48-14-14", "K2013-05-01_48-12-12", "K2012-08-24_4-4", "K2013-07-01_48-16-16",
    "K2012-01-01_1", "K2013-07-01_1-sz-m-f-ggel-k-i-1", "K2014-07-19_4-4",
}


def main() -> None:
    with BE.open(encoding="utf-8") as f:
        sorok = list(csv.DictReader(f))
    SZOVEGEK.mkdir(parents=True, exist_ok=True)
    for regi in SZOVEGEK.glob("*.txt"):
        regi.unlink()
    for s in sorok:
        szoveg = (
            f"Azonosító: {s['valtozas_id']}\n"
            f"Rendelkezés: {s['rendelkezes']}\n"
            f"Változás típusa: {s['valtozas_tipusa']}\n"
            f"Hatálybalépés: {s['hatalybalepes']}\n\n"
            f"RÉGI SZÖVEG:\n{s['regi_szoveg'] or '(nincs – új rendelkezés)'}\n\n"
            f"ÚJ SZÖVEG:\n{s['uj_szoveg'] or '(nincs – hatályon kívül helyezve)'}\n"
        )
        (SZOVEGEK / f"{s['valtozas_id']}.txt").write_text(szoveg, encoding="utf-8")

    jeloltek = sorted(s["valtozas_id"] for s in sorok if s["valtozas_id"] not in KODKONYV_PELDAK)
    minta = sorted(random.Random(MAG).sample(jeloltek, MINTA_MERET))
    if not MINTA.exists():
        with MINTA.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["file", "code"])
            for v in minta:
                w.writerow([f"{v}.txt", ""])
        print(f"Kézi minta létrehozva: {MINTA} ({len(minta)} egység)")
    else:
        print(f"A kézi minta már létezik, nem írom felül: {MINTA}")
    print(f"Szövegfájlok: {len(sorok)} db → {SZOVEGEK}")
    print("Minta:", ", ".join(minta))


if __name__ == "__main__":
    main()
