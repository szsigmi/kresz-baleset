# Projektállapot

Frissítve: 2026-10-16

## Mi készült el

- Összeállt a 2011–2025-ös, 180 hónapot lefedő közúti baleseti adatbázis és a hozzá tartozó forrásleírás. A nyers Statinfo-exportok változatlanul megvannak; a tisztított adatok szkriptekből állíthatók elő.
- Elkészült a KRESZ 2010–2025 közötti időállapotainak rendelkezésszintű összevetése. A 23 összevethető átmenetből 95 változássor került a táblába: 51 új, 40 módosított és 4 hatályon kívül helyezett rendelkezés; 9 sor az 1. vagy 2. számú függelékből származik.
- A teljességi ellenőrzés mind a 23 teljes szöveg-összevetést és a 2025. végi állapot mind a 62 releváns lábjegyzetét lefedettnek találta. A részletek és a kontrollok az összesítőben szerepelnek.
- A források, módszertani korlátok és munkamenetek dokumentálva vannak. A projekt validációja az `output/validacio.md` fájlban található.

## Fájlok és helyük

- **Nyers forrásadatok:** `data/raw/` – Statinfo- és STADAT-fájlok, NJT-időállapotok és jogszabályoldalak. A letöltött oldalak gyorsítótára: `data/raw/cache/`.
- **Feldolgozott táblák:** `data/processed/balesetek_havi.csv`, `data/processed/kresz_idoallapotok.csv`, `data/processed/kresz_valtozasok.csv`. A kísérleti KRESZ-kimenet is itt van `kresz_valtozasok_proba.csv` néven.
- **Feldolgozó szkriptek:** `scripts/01_statinfo_beolvasas.py`, `scripts/02_validacio.py`, `scripts/03_kresz_valtozasok.py`, `scripts/04_kresz_teljessegellenorzes.py`, valamint a baleseti hierarchiához a `scripts/hierarchia.py`.
- **Dokumentáció:** `docs/forrasok.md`, `docs/forrasok_kresz.md`, `docs/statinfo_lekerdezesek.md`, `docs/kresz_valtozasok_osszegzes.md`, `docs/valtozasnaplo.md`.
- **Függőségek és környezet:** `requirements.txt`; a helyi virtuális környezet mappája `.venv/`.
- **GitHub:** a projekt az `origin/main` ágra van feltöltve.

## Ismert korlátok

- A KRESZ 2010-01-01-i állapotváltásnak nincs elérhető előző időállapota, ezért az összevetések a 2011-ben kezdődő baleseti idősorhoz tartozó első elérhető állapottól indulnak.
- A Statinfo felületén okozó szerinti ittas baleseti bontás nem volt elérhető; rendelkezésre csak az ittas okozás havi összesített értéke áll.
- A régi STADAT 2.4.2 táblával néhány havi eltérés van; ezek év és mutató szerint az `output/validacio.md` fájlban vannak felsorolva. Az ege0072 táblával mind a 48 közös hónap és mindhárom kimeneteli mutató egyezett.
- A `docs/kresz_valtozasok_osszegzes.md` teljességi fejezete a korábbi, 61 soros eredményt kifejezetten elavultként jelöli; a jelenlegi végső eredmény 95 sor.

## Következő lépés

Az adat-előkészítés után meg kell határozni és dokumentálni az elemzési tervet: a KRESZ-változások időzítését össze kell kapcsolni a havi baleseti idősorral, rögzítve a vizsgált kimeneteket, az összehasonlítási időablakokat és az értelmezési korlátokat. Ezután az elemzést újrafuttatható szkriptben kell megvalósítani, az eredményeket pedig ábrákkal és módszertani leírással közölni. A hatásvizsgálat még nem készült el; az idősoros együttmozgás önmagában nem bizonyít okozati hatást.
