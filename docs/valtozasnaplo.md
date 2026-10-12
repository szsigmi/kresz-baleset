# Változásnapló

## 2026-10-12 — Validáció javítása

- Új szabály került az AGENTS.md-be az összevetett elemszámok és a nem elvégezhető ellenőrzések jelentéséről.
- A `statinfo_JA2A01_ok.xlsx.xlsx` fájlt tartalomváltoztatás nélkül `statinfo_JA2A01_ok.xlsx` névre neveztem át; a két forrásdokumentumot frissítettem.
- A validáció most fájlonként kilistázza a CSV dimenzióit és kategóriáit, megvizsgálja a JA2A02-export fejlécét és havi arányait, külön összeveti a mindösszesent a két STADAT-időszakkal, valamint megszámolja a 2022–2026-os numerikus cellák betűszínkódjait.
- Bizonytalanság: a kimenetel nevű export kategóriái okozókat sorolnak, nem halálos/súlyos/könnyű baleseteket; a súlyosság szerinti összevetéshez megfelelő Statinfo-export szükséges.

## 2026-10-12 — Projektindítás

- Létrejött a projekt mappastruktúrája, a `.venv` virtuális környezet és a `requirements.txt` függőségi lista.
- Telepítettem és importtal ellenőriztem a pandas, requests, beautifulsoup4, lxml, openpyxl, pdfplumber, matplotlib és statsmodels csomagokat.
- A `cryptography<47` kiegészítő korlát biztosítja, hogy a `pdfplumber` függősége Python 3.14-en előre fordított kerékből települjön.
- Git-repót inicializáltam; a `.gitignore` kizárja a `.venv/` és a `data/raw/cache/` tartalmát.
- Létrehozott fájlok: `.gitignore`, `requirements.txt`, `docs/valtozasnaplo.md`, valamint a mappákat jelölő `.gitkeep` fájlok.
- Bizonytalanság: nincs; adatforrás-letöltés és adatelemzés még nem történt.

## 2026-10-12 — 1. lépés, A rész: forrásfeltárás

- Elkészült a `docs/forrasok.md` forrásjegyzék: KSH havi és éves STADAT-táblák, a Tájékoztatási adatbázis, KSH kiadványok, 2021-es negyedéves közlemények és rendőrségi tartalékforrások.
- A forrásjegyzék megadja a ténylegesen megnyitott URL-eket, formátumokat, mutatókat, időbontást, lefedettséget és az előzetes/végleges adat megjegyzéseit; letöltési tervet is tartalmaz.
- Adatfájlt nem töltöttem le. Változott fájlok: `docs/forrasok.md`, `docs/valtozasnaplo.md`.
- Bizonytalanság: a havi KSH táblákban 2021 rés látszik; a teljes 2005–2015-ös PDF-sorozat URL-jeinek teljességét nem ellenőriztem; a Tájékoztatási adatbázis egyedi baleseti adatkörei hibával nyíltak meg. A forráslista és terv jóváhagyásra vár.
# 2026-10-12

- Az AGENTS.md robots.txt-szabályát a pontosított szövegre cseréltem.
- A kézi Statinfo-exportokkal elkészült a `scripts/01_statinfo_beolvasas.py` és a `data/processed/balesetek_havi.csv` (2011–2025; a `data/raw/proba/` fájl kimaradt).
- Létrehoztam a `docs/statinfo_lekerdezesek.md` fejlécleltárt, és kiegészítettem a `docs/forrasok.md`-t a JA2A01/JA2A02 exportokkal és a hallgató által megadott robots.txt-állapottal.
- Elkészült a `scripts/02_validacio.py` és az `output/validacio.md`. A két helyi STADAT-export időszakai nem fedik egymást; a megadott Statinfo-exportokban nincs halálos/súlyos/könnyű bontás, ezért az ilyen összevetés nem állítható elő. A 2024-es okozói kategóriaváltás és a JA2A02 fájl/munkalap-kód eltérés bizonytalan maradt.
- A `.venv` újralétrejött a `requirements.txt` alapján; minden felsorolt csomag importálható. A Git-tároló `main` ágon volt, meglévő módosításokkal és nem követett fájlokkal.
- A vizsgálati időszakot AGENTS.md-ben és `docs/forrasok.md`-ben 2011–2025-re állítottam. A beolvasó most ezt az időszakot írja ki, `szulo_kategoria`, forrás-URL és letöltési dátum mezőkkel.
- A `statinfo_JA2A02_okozo.xlsx` fájlt változatlan tartalommal `statinfo_JA2A01_ittas_osszes.xlsx` névre neveztem át; a forrásleltárakat és a validációs szkriptet ehhez igazítottam. Rögzítettem, hogy okozó szerinti ittas bontás nem volt elérhető.
- Újrafuttattam az 01/02 szkriptet. A kimenetel-export 180 havi sorában a halálos + súlyos + könnyű érték minden hónapban kiadja a Mindösszesent. A 4.c ellenőrzés mindkét STADAT-táblánál tartalmazza mindhárom súlyosságot: ege0072-nél 48/48 hónap eltérés nélkül; a régi 2.4.2-nél 60 hónapból halálos 2, súlyos 5, könnyű 6 eltérés.
- Nyitott kérdés: a Baleset oka és a Baleset természete exportjának lapos fejléce nem jelöli egyértelműen a főcsoport–alkategória kapcsolatot. Emiatt a CSV szülőmezője üres, a hierarchikus összegvizsgálat nem végezhető el; a feloldás a hallgató kategóriatérképét igényli.
- Kiegészítő összegpróba: a `Baleset oka` főcsoportjai összege mind a 180 hónapban kiadja a Mindösszesent. A sebesség, járművezetői egyéb hiba és gyalogos csoport alábontása 180/180 hónapban egyezik. A pályahiba alábontásának két szintje csak a 130 olyan hónapban egyezik, ahol a szülő numerikus; 50 hónapban a szülő hiányzik, ezért ezek a `szulo_kategoria` mezők üresek maradtak. A `Baleset természete` kategóriáinak összege 180/180 hónapban kiadja a Mindösszesent, tehát lapos.
- A CSV-be bekerült a forrás munkalaposzlopa (`forras_oszlop`), hogy az azonos nevű, azonos értéksorú exportoszlopok visszakövethetők legyenek. Az 01/02 szkriptet ismét lefuttattam.
- A 4.c régi STADAT-táblás eltérései közül a Mindösszesen 5 eltérése mind 2020-as; halálos eltérései 2/2 2020-asak, súlyosnál 5-ből 1 (2017-12), könnyűnél 6-ból 1 (2017-12) nem 2020-as.
- A `.DS_Store` rendszerfájlokat a `.gitignore` kizárja a verziókövetésből.

## 2026-10-12 — 2. lépés, A rész: KRESZ-forrásfeltárás

- Sikeres robots.txt-próba a projekt `.venv` requests csomagjával; a `/search/*` tiltást tiszteletben tartottam.
- Létrejött a `docs/forrasok_kresz.md`: NJT KRESZ-oldal, időállapotlista, három minta-időállapot és egy módosító rendelet oldalának forrásvizsgálata, módszerek lefedettsége, letöltési/feldolgozási terv.
- A megnyitott oldalválaszok a `data/raw/cache/` mappába kerültek; tömeges letöltés nem történt.
- Bizonytalanság: a jogszabályoldal export kezelőfelületének önálló fájlformátumát nem igazoltam; a végleges módosításjegyzék a későbbi feldolgozás feladata.

## 2026-10-12 — KRESZ-kísérleti kör előkészítése

- A robots.txt `/ajax/` útvonalra vonatkozó megjegyzése bekerült a `docs/forrasok_kresz.md` fájlba; javítottam a verziólista elemszámát is: 26 állapot, a legkorábbi felsorolt verzió 16.
- A változatlan JSON-válasz `data/raw/kresz_idoallapotok.json` néven, a 16. verzió HTML-je `data/raw/kresz_1975-1-20-24_16.html` néven került a nyers adatok közé; a `data/processed/kresz_idoallapotok.csv` 24, 2010–2025 közötti állapotkezdést tartalmaz.
- A 15. verzió URL-je a főoldalra irányított át (HTTP 200, végső URL: `https://njt.jog.gov.hu/`, 133403 bájt). A verziólista nem tartalmaz 15. verziót, ezért a kért 15→16 szövegösszevetés és pozitív kontroll nem végezhető el; itt megálltam, összehasonlító CSV és feldolgozószkript még nem készült.

## 2026-10-12 — KRESZ-kísérleti kör, 16→17

- A `docs/forrasok_kresz.md` rögzíti, hogy a 2010-01-01-i váltásnak nincs letölthető előző állapota; a 16. verzió az összevetések kiindulópontja, a korlát a 2011-ben induló baleseti idősorra nincs hatással.
- A változatlan 16. és 17. verzió HTML-je, valamint a 280/2010. (XII. 15.) Korm. rendelet oldala a `data/raw/` alatt van. A 03-as szkript elkészült; a 16→17 összevetés két új rendelkezést talált, mindkettő lábjegyzete a rendelet 6. §-ára mutat.
- A rendelet saját szövegében a 6. § a KRESZ 37. §-át (6) és (7) bekezdéssel egészíti ki; a rendelet és a 17. állapot kezdőnapja egyaránt 2011-01-01. A kétforrásos kontroll egyezett.
- Futtatással a verzió-CSV is újragenerálódott; 23 összevethető állapotkezdés van 2010-01-02 és 2025-12-31 között. A kísérleti változás-CSV két sort tartalmaz. Tömeges lekérés nem történt.

## 2026-10-12 — KRESZ-változások teljes időállapot-összevetése

- Letöltöttem és gyorsítótáraztam a 18–39. KRESZ-időállapotokat (kérések között legalább 2 másodperccel), majd kiterjesztettem és lefuttattam a `scripts/03_kresz_valtozasok.py` szkriptet mind a 23 összevethető váltásra.
- Elkészült a `data/processed/kresz_valtozasok.csv` (61 sor: 32 új, 29 módosított; 0 hatályon kívül helyezett; 0 ábraváltozás; nincs lábjegyzet alapján azonosíthatatlan jogszabály). A 2026-os állapotkezdések a verziólistában vizsgálati időszakon kívüliként vannak jelölve.
- Négy kontrollmintát ellenőriztem a módosító jogszabályok időállapot szerinti saját szövegével; mindegyikben egyeztek az azonosított KRESZ-rendelkezések. A kért hatályon kívül helyezési mintához nem volt valódi átmenet, ezért a korábban törlésnek látszott 2017-es §-cserét kontrolláltam, és módosítottként osztályoztam.
- Elkészült a `docs/kresz_valtozasok_osszegzes.md`; frissült a `docs/forrasok_kresz.md`. A verziólisták, minta-jogszabályoldalak és módosítórendelet-időállapotok gyorsítótárazva vannak. Tömeges módosítórendelet-letöltés nem történt.
