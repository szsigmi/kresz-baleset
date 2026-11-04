# Változásnapló

## 2026-10-16 — Beadandó összefoglaló és adatcsomag bővítése

- A `scripts/05_kerekpar_ittas_elemzes.py` frissítve: az összefoglalóba bekerült az adatbázis létrehozásának hét számozott lépése, a jogszabályi megfogalmazás pontosítása és a 2023 nélküli (2015–2022) DiD-érzékenységi számítás.
- A PDF és a ZIP dokumentumai külön jelölik a COVID-éveket, a 2022–2023-as kerékpáros aránycsökkenést pedig lehetséges adatfelvételi törésként nevezik meg. A PDF-hez A4-es oldaltördelést állítottam be.
- A v2 ZIP-be bekerül a `kresz_valtozasok.csv` és a `balesetek_havi.csv`; a kódkönyv mindkét fájl oszlopait dokumentálja.
- A 46 soros éves elemzési CSV 92 forráscellájának ellenőrzése sikeres. A DiD 2015–2023-ra −2,808, 2023 nélkül (2015–2022) −1,808 százalékpont; a PDF `mdls` ellenőrzése 1 A4-es oldalt jelzett.
- A v2 ZIP sértetlen; 7 fájlt tartalmaz, mérete 219 137 bájt.
- Bizonytalanság: a 2022–2023-as csökkenés adatfelvételi okát a dokumentált források nem igazolják.

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

## 2026-10-12 — KRESZ-teljeségi ellenőrzés

- A `scripts/03_kresz_valtozasok.py` most a NJT szeletként tárolt rendelkezéseit, a bekezdésen belüli alpontokat, valamint az 1. és 2. számú függelék szöveges elemeit is feldolgozza; a 41. § (9) puszta jelölésre redukálódását hatályvesztésként jelöli.
- Újrafuttatás után a `data/processed/kresz_valtozasok.csv` 95 sort tartalmaz (51 új, 40 módosított, 4 hatályon kívül helyezett), amelyekből 9 függeléki tétel. Az ellenőrző szkript 23/23 teljes dokumentum-összevetést és 62/62 releváns lábjegyzet-célrendelkezést fedettnek talált; a négy nagyobb HTML-diff szegmens több külön CSV-sort fogott össze, ezek megfeleltetését az összesítő rögzíti.
- Változott: `scripts/03_kresz_valtozasok.py`, `scripts/04_kresz_teljessegellenorzes.py`, `data/processed/kresz_valtozasok.csv`, `data/processed/kresz_valtozasok_proba.csv`, `data/processed/kresz_idoallapotok.csv`, `docs/kresz_valtozasok_osszegzes.md`, `docs/valtozasnaplo.md`. Bizonytalan maradékot nem találtam.
## 2026-10-16 — Projektállapot dokumentálása

- Elkészült az `ALLAPOT.md`, amely összefoglalja az elkészült adatbázist és KRESZ-változásfeldolgozást, a fontos fájlok helyét, a dokumentált korlátokat és a következő elemzési lépést.
- Változott: `ALLAPOT.md`, `docs/valtozasnaplo.md`. Bizonytalan maradékot az eddigi teljességi ellenőrzés nem talált; az elemzési terv és a hatásvizsgálat még hátravan.
## 2026-10-16 — Kerékpáros ittas okozás adatforrásai

- A 2014-07-19-i KRESZ 4. § (4) módosítás régi/új szövegét és a 172/2014. (VII. 18.) Korm. rendeletet ellenőriztem a helyi változás-CSV-ben.
- A KSH STADATból letöltöttem a 4.1.1.50, 4.1.1.52, 4.2.1.4 és 4.2.1.6 táblák változatlan XLSX-exportját a `data/raw/` alá; az éves járműtípus és ittas járműtípus sorok 2001–2025-ig, a havi táblák 2022-től adnak bontást. Letöltöttem a rendőrség 2025. I–II. havi jelentését is.
- A `docs/forrasok.md` kiegészült az URL-ekkel, időszakokkal, gyakorisággal és a 2024-es ittas kerékpáros adatfelvételi törésre vonatkozó megjegyzéssel. Bizonytalan maradék: a rendőrségi jelentésekben a járműtípus szerinti okozói bontás mellett nem találtam ittas okozó × járműtípus kereszttáblát; a KSH éves STADAT-táblája viszont tartalmazza.
## 2026-10-16 — Kerékpáros ittas baleseti elemzés és leadandók

- Elkészült a `scripts/05_kerekpar_ittas_elemzes.py`; a KSH STADAT 4.1.1.50 és 4.1.1.52 változatlan forrásfájljaiból előállítja a `data/processed/kerekpar_ittas_eves.csv` fájlt és a `output/kerekpar_ittas_arany.png` ábrát.
- 46 év–okozótípus sor készült 2001–2023-ra. A CSV 92 balesetszám-celláját visszaellenőriztem a forrás-munkafüzetekkel; nem volt eltérés. Az egyszerű átlagarányos különbségek különbsége: −2,808 százalékpont.
- Elkészült az `beadando/kresz-baleset_adatcsomag_20261016_v1.zip` CSV-vel, ábrával, README-vel, kódkönyvvel és GenAI-módszertani leírással; továbbá az egyoldalas `beadando/osszefoglalo.pdf` és a Chrome által használt HTML-forrás.
- A PDF Chrome headless-szel készült; a `mdls` eredménye `kMDItemNumberOfPages = 1`, a PDF-et megnyitottam. Korlátok: csak a főútvonali kivétel szűnt meg, az adatok nem bontanak úttípus szerint, az éves pontok száma kevés, a COVID-évek kilógnak, és az eredmény nem okozati bizonyíték.
- Változott: `scripts/05_kerekpar_ittas_elemzes.py`, `data/processed/kerekpar_ittas_eves.csv`, `output/kerekpar_ittas_arany.png`, `beadando/`, `docs/valtozasnaplo.md`.

## 2026-11-03 — végleges adatbázis és validálás

- Létrehoztam a `data/final/` három CSV-jét: 95 KRESZ-változás, 180 havi összes balesetszám, 46 éves okozó × év rekord. A KRESZ-tábla őrzi a régi és az új normaszöveget; mindhárom tábla kapott egyedi első oszlopú azonosítót és forrás URL-t.
- Hozzáadtam a `scripts/06_validalas.py` szkriptet és a `docs/validacio_jelentes.md` riportot. A havi köztes táblát nyers Statinfo-exportokból, az éves mutatót a két nyers KSH XLSX-ből építi újra.
- Elkészült a `docs/kodkonyv.md`; a 172/2014. (VII. 18.) Korm. rendelet leírását egységesítettem a README-ben, a módszertani leírásban, a HTML-összefoglalóban és az elemző szkript szövegében.
- Validálás: 19 ellenőrzés, 0 eltérés; a havi–éves KSH összegellenőrzés nem végezhető el, mert nincs helyi éves összesítő export. A kerékpáros ittas okozás idősorában a 2024-től jelzett adatfelvételi törés és a 2024–2025-ös táblabeli lefedettség hiánya korlát marad.
- Változott fájlok: `data/final/*.csv`, `docs/kodkonyv.md`, `docs/validacio_jelentes.md`, `scripts/06_validalas.py`, `scripts/05_kerekpar_ittas_elemzes.py`, `beadando/README.md`, `beadando/genai_modszertan.md`, `beadando/osszefoglalo.html`, `docs/valtozasnaplo.md`. Az `AI_NAPLO.md`-hoz nem nyúltam.

## 2026-11-03 — havi végleges tábla bővítése és független egyeztetése

- A `data/final/balesetek_havi.csv` immár 180 soros, 11 oszlopos széles tábla: hét egész havi mutató és forrásmezők. A hét értéket közvetlenül a három nyers JA2A01 XLSX-ből olvassa a `scripts/06_validalas.py`.
- Kiegészítettem az ellenőrzést a két havi kategóriaazonossággal, a hét mutató havi→éves összegének Statinfo év-soraival való egyeztetésével, valamint a teljes balesetszám KSH 4.1.1.50 `Összesen` oszlopával végzett 2011–2025-ös ellenőrzéssel.
- Javítottam a kódkönyv havi oszloplistáját, a KRESZ-változások dátumtartományát és a `K2014-07-19_4-4` azonosítópéldát. A jelentésben 23 ellenőrzés futott, eltérés nem volt.
- Módosult: `data/final/balesetek_havi.csv`, `docs/kodkonyv.md`, `docs/validacio_jelentes.md`, `scripts/06_validalas.py`, `docs/valtozasnaplo.md`. Kétséges pont nem maradt; a PDF még nem készült el.

## 2026-11-04 — munkakörnyezet-ellenőrzés

- A wscheck jelzései alapján hozzáadtam a `.gitignore` szabályait a `.env` és a kulcsfájl-minták kizárására.
- Létrehoztam az `.agent/workflows/adatbazis-veglegesites.md` projektmunkafolyamatot.
- A GitHub CLI bejelentkezése a sandboxban a macOS Kulcskarikához nem fér hozzá, ezért az ottani ellenőrzés érvénytelennek mutatja a tokent. A felhasználó jelezte, hogy a `gh` a Terminálban működik, és a GitHub-műveleteket ott végzi; további `gh`-műveletet nem futtattam. A logoutkérés megszakadt, kijelentkeztetés nem történt.
- A `.gitignore` megjegyzése rögzíti, hogy a `data/` nyilvános KSH- és NJT-forrásadatot, illetve a leadandó adatbázist tartalmaz, ezért a privát tárolóban verziókezelt; a `data/raw/cache/` továbbra is kizárt.
