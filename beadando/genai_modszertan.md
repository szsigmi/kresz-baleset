# GenAI-támogatás és ellenőrzések

## Mit végzett a genAI

- A megadott kutatási kérdést változatlanul kezelte, és a KSH 4.1.1.50 (okozó járműtípus szerinti összes baleset) és 4.1.1.52 (ittas okozás járműtípus szerint) táblákhoz feldolgozó szkriptet készített.
- A szkript a két nyers XLSX-ből gépileg kiolvassa a 2001–2023-as kerékpár- és személygépkocsi-sorokat, kiszámítja az ittas arányt, a jelzőoszlopokat, az egyszerű DiD-t, az ábrát, a dokumentációt és a beadandó csomagot.
- Megírta a forrásleírást, kódkönyvet, ezt a módszertani jegyzetet és az egyoldalas HTML-alapú PDF-összefoglalót.

## Mit és hogyan ellenőriztünk

- A 4.1.1.50 és 4.1.1.52 fejlécéből a kerékpár és személygépkocsi oszlopot név szerint választottuk ki; a CSV minden összes és ittas darabszámát közvetlenül összevetettük a forrás-munkafüzet megfelelő év/oszlop cellájával (46 év–típus sor, összesen 92 forrásérték).
- Ellenőriztük, hogy minden ittas balesetszám nemnegatív és nem nagyobb az adott okozótípus összes balesetszámánál; a 2024–2025-ös sorokat kizártuk.
- Az arányt a két ellenőrzött számláló és nevező hányadosaként számoltuk. A DiD-ben 2001–2013 és 2015–2023 éves arányainak egyszerű számtani átlagát használtuk; 2014 átmeneti év, nem része egyik átlagnak sem.
- A jogi váltás dátumát és szövegét a projekt 26. és 27. NJT-időállapotának szövegdiffjével ellenőriztük. A KSH-tábla 2024-es módszertani megjegyzése szerint ettől az évtől nem minden kerékpárosnál vizsgálják az ittasságot.

## Korlátok

- A 2014-es módosítás csak a főútvonali kivételt szüntette meg; a KSH-adat nem bontja az eseteket úttípus szerint, ezért a ténylegesen érintett esetek nem különíthetők el.
- Évente egy megfigyelés van, a vizsgált idősor rövid (23 év × két okozótípus), és a szabály hatálybalépésének éve átmeneti.
- A COVID-időszak 2020–2021-es értékei kilógnak a szokásos trendből; az alap DiD ezeket tartalmazza, ezért az átlagok érzékenyek rájuk.
- Az ittas kerékpáros esetek mérésében 2024-től törés van, ezért 2024–2025 kimaradt.
- A személygépkocsi-vezető összehasonlító csoport, nem garantáltan érintetlen kontroll. Az egyszerű különbségek különbsége nem kontrollálja az egyidejű változásokat, és nem okozati bizonyíték.
- A százalékos arányok nevezője az okozótípushoz tartozó balesetek száma; az elemzés nem használ kitettségi adatot (például megtett kilométert vagy közlekedők számát).
