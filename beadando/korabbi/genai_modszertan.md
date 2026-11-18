# GenAI-támogatás és ellenőrzések

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

- A 172/2014. (VII. 18.) Korm. rendelet 2014. július 19-től a főútvonalakra is kiterjesztette a kerékpárosok felmentését az alkohol jelenlétére vonatkozó tilalom alól; a befolyásoltság továbbra is tilos maradt. A KSH-adat nem bontja az eseteket úttípus szerint, ezért a ténylegesen érintett esetek nem különíthetők el.
- Évente egy megfigyelés van, a vizsgált idősor rövid (23 év × két okozótípus), és a szabály hatálybalépésének éve átmeneti.
- A COVID-időszak 2020–2021-es éveit külön jelöltük; az alap DiD ezeket tartalmazza, ezért az átlagok érzékenyek rájuk.
- A kerékpáros ittas arány 2022 és 2023 között hirtelen csökkent; ez lehetséges adatfelvételi törés, amelyet a rendelkezésre álló forrásokból nem tudtunk igazolni.
- Az ittas kerékpáros esetek mérésében 2024-től törés van, ezért 2024–2025 kimaradt.
- A személygépkocsi-vezető összehasonlító csoport, nem garantáltan érintetlen kontroll. Az egyszerű különbségek különbsége nem kontrollálja az egyidejű változásokat, és nem okozati bizonyíték.
- A százalékos arányok nevezője az okozótípushoz tartozó balesetek száma; az elemzés nem használ kitettségi adatot (például megtett kilométert vagy közlekedők számát).
