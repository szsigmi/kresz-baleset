# KRESZ-változások és közúti balesetek

Egyetemi projekt az „AI a társadalomtudományokban” kurzusra. Az adatbázis a KRESZ (1/1975. (II. 5.) KPM–BM rendelet) 2011–2025 között hatályba lépett változásait kapcsolja össze a magyarországi személysérüléses közúti balesetek KSH-adataival. Minden változás irány-kódot kapott (szigorítás / enyhítés / semleges / vegyes), az alkoholszabályra pedig csoportonkénti szabályozási szint-skála készült. Az elemzés azt vizsgálja, hogyan változott az ittas okozás aránya a kerékpárosok által okozott balesetekben a kerékpárosok alkoholszabályának két enyhítése (2012, 2014) után, a személygépkocsi-vezetőkhöz képest (2001–2023).

**Fő eredmény:** a teljes zéró tolerancia (2001–2011) és a teljes lazítás (2015–2023) évei között a különbségek különbsége −2,6 százalékpont, 95%-os konfidencia-intervallum [−6,1; +0,9]. Az ittas arány a kerékpárosoknál nem nőtt; a csökkenés nem különíthető el az idősor szokásos ingadozásától. Részletek: `beadando/` (elemzés PDF), `output/elemzes_eredmenyek.md`.

## Mi hol van

| Mappa / fájl | Tartalom |
|---|---|
| `data/raw/` | A letöltött nyers fájlok változatlanul: NJT KRESZ-időállapotok (HTML), KSH Statinfo-exportok és STADAT-táblák (XLSX). |
| `data/processed/` | Szkriptekkel előállított köztes táblák. |
| `data/final/` | **A végleges adatbázis:** `kresz_valtozasok.csv` (95 sor), `balesetek_havi.csv` (180 sor), `kerekpar_ittas_eves.csv` (46 sor), `kresz_valtozasok_irany.csv` (95 sor, irány-kód), `szabalyozasi_szint_alkohol.csv` (szintskála). |
| `data/raw/kezi_kodolas/` | Kézzel kódolt adatok: az alkoholszabály szint-skálája a jogszabályszöveg alapján. |
| `data/processed/iranykod/` | Az irány-kódolás anyagai: szövegek, `prompt.md`, `models.md`, gépi címkék (`labels.csv`), kézi minta (`hand.csv`). |
| `scripts/` | Számozott feldolgozó, ellenőrző és elemző szkriptek (01–07). |
| `output/` | Ábrák, elemzési táblák, ellenőrzési eredmények. |
| `docs/` | Kódkönyv (`kodkonyv.md`), az irány-kód kódkönyve (`iranykod_kodkonyv.md`), forráslista, validálási jelentés, változásnapló. |
| `beadando/` | A leadott dokumentumok (kódkönyv és elemzés PDF-ben, adatcsomag). |
| `AGENTS.md` | Az MI-ügynök munkaszabályai ebben a projektben. |

## Reprodukálás

Szükséges: Python 3.11 vagy újabb (tesztelve: Python 3.14, macOS) és git.

```bash
git clone https://github.com/szsigmi/kresz-baleset.git
cd kresz-baleset
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt          # Windows: .venv\Scripts\pip install -r requirements.txt

# 1. Végleges táblák előállítása a nyers fájlokból + 23 ellenőrzés
.venv/bin/python scripts/06_validalas.py
# 2. Elemzés: táblázatok, robusztussági és placebo-becslések, ábrák
.venv/bin/python scripts/07_elemzes.py
# 3. Irány-kódolás: címke-ellenőrzés, egyezés a kézi kódolással, végleges irány-tábla
.venv/bin/python scripts/09_iranykod_osszesites.py
```

**Elvárt eredmény:**
- A `06_validalas.py` futás végén ezt írja ki: `Validálási ellenőrzések: 23; hibás/eltérő ellenőrzések: 0`. A részletek a `docs/validacio_jelentes.md` fájlban vannak.
- A `07_elemzes.py` kiírja az eredménytáblákat; a fő becslés `-2,60` pp. Ugyanez kerül az `output/elemzes_eredmenyek.md` fájlba, az ábrák pedig az `output/abra1_ittas_arany.png` és az `output/abra2_kulonbseg.png` fájlba.
- A `09_iranykod_osszesites.py` a címke-ellenőrzést (0 hiba), a kódgyakoriságokat és az egyezést (pontos egyezés, Cohen-féle kappa) írja ki, és az `output/iranykod_egyezes.md` fájlba menti.

Mindhárom lépés internet nélkül fut, csak a tárolóban lévő fájlokat használja. A gépi címkék (`labels.csv`) egy nyelvi modell kimenetei: ezeket nem a szkript állítja elő, hanem rögzített eredményként szerepelnek a tárolóban; a modellt és a promptot a `models.md` és a `prompt.md` írja le.

**A korábbi lépések (nem szükségesek a reprodukáláshoz):**
- `01_statinfo_beolvasas.py`, `02_validacio.py`: a Statinfo-exportok beolvasása és első ellenőrzése. A Statinfo-adatokat kézzel exportáltam (lásd `docs/statinfo_lekerdezesek.md`); a fájlok a `data/raw/` mappában vannak.
- `03_kresz_valtozasok.py`, `04_kresz_teljessegellenorzes.py`: a KRESZ 16–39. időállapotának összevetése és teljességi ellenőrzése. A letöltött HTML-fájlok a `data/raw/` mappában vannak; ami hiányzik, azt a szkript a Nemzeti Jogszabálytárból tölti le (kérések között 2 mp szünettel).
- `05_kerekpar_ittas_elemzes.py`: az első, előzetes elemzés (október 16.).
- `08_iranykod_elokeszites.py`: a 95 változás szövegfájlja és a 25 elemű kézi minta (mag = 1) az irány-kódoláshoz. A gépi kódolás a `$vclassify` skill szerint készült: az első futás (Codex) félbemaradt, a címkéket a második futás (Claude) készítette ugyanazzal a `prompt.md` v1 utasítással; a kézi kódolást én végeztem, vakon.

## Források

- Nemzeti Jogszabálytár: a KRESZ időállapotai, `https://njt.jog.gov.hu/jogszabaly/1975-1-20-24.<verzió>` (letöltve 2026-10-12)
- KSH Statinfo, JA2A01 (Közúti balesetek), `https://statinfo.ksh.hu/Statinfo/QueryServlet?ha=JA2A01` (kézi export, 2026-10-12)
- KSH STADAT 4.1.1.50 és 4.1.1.52, `https://www.ksh.hu/stadat_files/ege/hu/ege0064.xlsx`, `ege0066.xlsx` (letöltve 2026-10-16)

Minden adatsor tartalmazza a saját forráscímét és letöltési dátumát (`forras_url`, `letoltes_datuma`).

## MI-nyilatkozat

- **Eszközök:** Codex CLI (OpenAI), GPT-6-Luna modellel (közepes gondolkodási szint), a saját gépemen, az `AGENTS.md` szabályaival és az oktatói skillekkel. Claude (Anthropic) csevegő-asszisztens: akkor használtam, amikor elakadtam, a visszaellenőrzésre, a 95 KRESZ-változás irány-címkézésére, valamint a kódkönyvek, az elemző szkriptek (07–09) és az elemzés megszövegezéséhez.
- **Mit végzett az MI:** a Codex gyűjtötte és dolgozta fel az adatokat (01–06. szkript), és megírta az irány-kódolás promptját; a címkézés első futása nála félbemaradt. A Claude javasolta az elemzés módszerét, megírta az irány-kódkönyv és a 07–09. szkript első változatát, a Codex promptja alapján besorolta a 95 változást, és megírta a kódkönyv és az elemzés szövegét. Én választottam ki a kutatási kérdést, 25 változást vakon kézzel kódoltam, döntöttem minden lépésnél, és átnéztem az eredményeket.
- **Hogyan ellenőriztem:** minden lépés újrafuttatható szkriptből fut, verziókezelve. A végleges adatbázist 23 automatikus ellenőrzés és egy független KSH-forrás igazolja; a gépi irány-címkéket a darabszám- és idézet-ellenőrzés és a saját vak kódolásommal való egyezés. A munka közben az ellenőrzés több valódi hibát kiszűrt (hibás Statinfo-export, a 2014-es szabály fordított leírása, egy tévesen elvégezhetetlennek ítélt ellenőrzés, és a szintskála kitöltésekor derült ki, hogy az első lazítás már 2012-ben megtörtént).
- **Fennmaradó kockázat:** a KRESZ-változások gépi szövegösszevetésből, irányuk gépi kódolásból származik; a kézi minta 25 elemén kívül nem ellenőriztem őket egyenként. A két MI-eszköz azonos hibát is véthet. Az elemzés kevés éves adatpontra épül, ezért az eredmény leíró jellegű, nem okozati.

## Licenc

A saját feldolgozás (táblák, kód, dokumentáció) CC BY 4.0 licenccel használható. A forrásadatokra a KSH és a Nemzeti Jogszabálytár felhasználási feltételei vonatkoznak.
