# Validációs jelentés

Készült: 2026-10-12. A nyers fájlokat nem módosítottam.

## CSV-kategórialeltár

### `statinfo_JA2A01_helye.xlsx`
- **Baleset helye** (3 kategória): Lakott területen; Lakott területen kívül; Mindösszesen Baleset helye
### `statinfo_JA2A01_ittas_osszes.xlsx`
- **Mutatók** (1 kategória): Ittasan okozott balesetek (db)
### `statinfo_JA2A01_kimenetel.xlsx`
- **Kimenetel** (5 kategória): Halálos; Könnyű sérüléses; Mindösszesen Kimenetel; Nem sérült; Súlyos sérüléses
### `statinfo_JA2A01_ok.xlsx`
- **Baleset oka** (26 kategória): A járművezető egyéb hibája; A sebesség nem megfelelő alkalmazása; Egyéb; Egyéb hiba; Egyéb nem megfelelő jelzőtáblák; Egyéb okok; Elsőbbség nem adása; Gyalogos hibája; Gyalogosok egyéb hibája; Helytelen alkalmazkodás az útviszonyokhoz; Jármű műszaki hibája; Járművezetők hibája; Megállási kötelezettség elmulasztása; Mindösszesen Baleset oka; Nem megfelelő közlekedési jelzések; Pálya hibája; Sebességtúllépés; Szabálytalan előzés; Szabálytalan irányváltoztatás, haladás, bekanyarodás; Tilos jelzésen áthaladás; Tiltott helyen áthaladás; Utasok hibája; Veszélyes helyek nem megfelelő jelzése; Vigyázatlan lelépés az úttestre; Világítási szabályok megszegése; Álló jármű vagy oszlop előtti áthaladás
### `statinfo_JA2A01_okozo.xlsx`
- **Okozó** (19 kategória): Autóbusz; Egyéb; Egyéb jármű; Egyéb személy; Elektromos rásegítésű kerékpár; Gyalogos; Gyalogos egyéb motoros közlekedési eszközzel; Kerékpár, emberi erővel hajtott; Mindösszesen Okozó; Motorkerékpár; Motoros roller (kis és nagy teljesítményű); Segédmotoros kerékpár; Személygépkocsi; Tehergépkocsi; Tömegközlekedési jármű; Utas; Vasúti szerelvény; Állat; Állati erővel vont jármű
### `statinfo_JA2A01_termeszet.xlsx`
- **Baleset természete (2011-)** (14 kategória): Egyéb baleset; Gyalogosok elütése; Körforgalomban történt ütközéses balesetek; Megcsúszás, farolás felborulás, pálya elhagyása; Mindösszesen Baleset természete (2011-); Szilárd tárgynak ütközés; Várakozó, parkoló járműnek ütközés; azonos irányba egyenesen haladó járművek; azonos irányba haladó és kanyarodó járművek; keresztirányba egyenesen haladó járművek; keresztirányból érkező, és kanyarodó járművek; szembe egyenesen haladó járművek; szembe haladó és kanyarodó járművek; Ütközés állattal
### `statinfo_JA2A01_utkategoria.xlsx`
- **Az út kategóriája (2011-)** (7 kategória): Autópálya; Autóút; Egyéb; Főút; Ismeretlen, vagy nem út; Mellékút; Mindösszesen Az út kategóriája (2011-)

## 4. Baleseti kategóriák hierarchiája – havi összegpróba

Az ellenőrzés a 2011–2025-ös 180 havi sort használja. A fejlécek szerinti ismétlődő kategórianév és teljesen azonos havi sorozat a főcsoportösszegben csak egyszer szerepel; a CSV-ben az eredeti oszlopok megmaradnak. Üres cellát nem töltök ki: az összegek csak a numerikus forráscellákat tartalmazzák.

### Baleset oka

- `Mindösszesen Baleset oka` = `Járművezetők hibája` + `Jármű műszaki hibája` + `Pálya hibája` + `Gyalogos hibája` + `Utasok hibája` + `Egyéb okok`: 180/180 összevethető szülőérték; hiányzó gyerekcellák: 71; maradékos hónapok: 0; elfogadva.
- `Járművezetők hibája` = `A sebesség nem megfelelő alkalmazása` + `Szabálytalan előzés` + `Elsőbbség nem adása` + `Szabálytalan irányváltoztatás, haladás, bekanyarodás` + `A járművezető egyéb hibája`: 180/180 összevethető szülőérték; hiányzó gyerekcellák: 0; maradékos hónapok: 0; elfogadva.
- `A sebesség nem megfelelő alkalmazása` = `Helytelen alkalmazkodás az útviszonyokhoz` + `Sebességtúllépés` + `Egyéb`: 180/180 összevethető szülőérték; hiányzó gyerekcellák: 0; maradékos hónapok: 0; elfogadva.
- `A járművezető egyéb hibája` = `Megállási kötelezettség elmulasztása` + `Világítási szabályok megszegése` + `Egyéb hiba`: 180/180 összevethető szülőérték; hiányzó gyerekcellák: 47; maradékos hónapok: 0; elfogadva.
- `Pálya hibája` = `Nem megfelelő közlekedési jelzések`: 130/180 összevethető szülőérték; hiányzó gyerekcellák: 0; maradékos hónapok: 0; nem igazolható 180/180 hónapra.
  - Szülőérték hiányzik: 2011-01, 2011-05, 2011-07, 2011-11, 2012-02, 2012-07, 2012-11, 2013-02, 2013-12, 2014-01, 2014-03, 2014-06, 2014-11, 2014-12, 2015-01, 2015-02, 2015-03, 2015-05, 2015-11, 2016-01, 2016-04, 2016-11, 2016-12, 2017-02, 2017-11, 2017-12, 2018-06, 2018-12, 2019-01, 2019-02, 2019-12, 2020-02, 2020-03, 2020-11, 2020-12, 2021-11, 2021-12, 2022-01, 2022-02, 2022-03, 2022-06, 2022-07, 2022-12, 2023-01, 2023-11, 2024-11, 2025-02, 2025-08, 2025-10, 2025-11.
- `Nem megfelelő közlekedési jelzések` = `Veszélyes helyek nem megfelelő jelzése` + `Egyéb  nem megfelelő jelzőtáblák` + `Egyéb`: 130/180 összevethető szülőérték; hiányzó gyerekcellák: 237; maradékos hónapok: 0; nem igazolható 180/180 hónapra.
  - Szülőérték hiányzik: 2011-01, 2011-05, 2011-07, 2011-11, 2012-02, 2012-07, 2012-11, 2013-02, 2013-12, 2014-01, 2014-03, 2014-06, 2014-11, 2014-12, 2015-01, 2015-02, 2015-03, 2015-05, 2015-11, 2016-01, 2016-04, 2016-11, 2016-12, 2017-02, 2017-11, 2017-12, 2018-06, 2018-12, 2019-01, 2019-02, 2019-12, 2020-02, 2020-03, 2020-11, 2020-12, 2021-11, 2021-12, 2022-01, 2022-02, 2022-03, 2022-06, 2022-07, 2022-12, 2023-01, 2023-11, 2024-11, 2025-02, 2025-08, 2025-10, 2025-11.
- `Gyalogos hibája` = `Vigyázatlan lelépés az úttestre` + `Tilos jelzésen áthaladás` + `Tiltott helyen áthaladás` + `Álló jármű vagy oszlop előtti áthaladás` + `Gyalogosok egyéb hibája`: 180/180 összevethető szülőérték; hiányzó gyerekcellák: 25; maradékos hónapok: 0; elfogadva.
- Teljesen azonos, ismétlődő név és 180 havi értéksor oszlopa(i): `Szabálytalan előzés`: 8, 9; `Elsőbbség nem adása`: 10, 11; `Szabálytalan irányváltoztatás, haladás, bekanyarodás`: 12, 13; `Jármű műszaki hibája`: 18, 19, 20; `Gyalogos hibája`: 26, 27; `Utasok hibája`: 33, 34, 35; `Egyéb okok`: 36, 37, 38. A főcsoport-összegben ezek egy kategóriaként szerepelnek.

### Baleset természete

- A Mindösszesen kivételével az összes kategória összege kiadja a Mindösszesent mind a 180 hónapban: a lista lapos, további csoportosítást nem alkalmaztam.
- Összegpróba: 180/180 hónap; hiányzó kategóriacellák: 1; maradékos hónapok: 0.

## 4.a Havi összeg és éves sor

- `statinfo_JA2A01_helye.xlsx`: az összes teljes (12 hónapos), numerikus éves sor egyezik; vizsgált évek: 15.
- `statinfo_JA2A01_ittas_osszes.xlsx`: az összes teljes (12 hónapos), numerikus éves sor egyezik; vizsgált évek: 15.
- `statinfo_JA2A01_kimenetel.xlsx`: az összes teljes (12 hónapos), numerikus éves sor egyezik; vizsgált évek: 15.
- `statinfo_JA2A01_ok.xlsx`: az összes teljes (12 hónapos), numerikus éves sor egyezik; vizsgált évek: 15.
- `statinfo_JA2A01_okozo.xlsx`: az összes teljes (12 hónapos), numerikus éves sor egyezik; vizsgált évek: 15.
- `statinfo_JA2A01_termeszet.xlsx`: az összes teljes (12 hónapos), numerikus éves sor egyezik; vizsgált évek: 15.
- `statinfo_JA2A01_utkategoria.xlsx`: az összes teljes (12 hónapos), numerikus éves sor egyezik; vizsgált évek: 15.

## 4.b Mindösszesen havi egyezés fájlok között

A JA2A01 baleseti adatköri fájlok Mindösszesen értékei egyeznek minden közös, ellenőrzött hónapban (180 hónap). Az ittas balesetek külön havi összes mutatója nem került ebbe az egyezőségvizsgálatba.

## 4. JA2A01 ittas összes export vizsgálata

- 1. sor: Közúti balesetek
- 2. sor: Közúti balesetek
- 4. sor: (Mindösszesen Baleset helye; Mindösszesen Kimenetel; Mindösszesen Baleset oka; Mindösszesen Okozó; Mindösszesen Az út kategóriája (2011-); Mindösszesen Baleset természete (2011-); Mindösszesen Terület)
- Az ittas okozás / összes baleset aránya: 180 közös hónap; minimum 0.0435 (2024-12), maximum 0.1350 (2020-05).
A nevezőként használt JA2A01 Mindösszesen az adatköri exportokban azonos a 180 vizsgált hónapban.
- Havi arányok (%), soronként év, oszloponként január–december:
  - 2011: 11.65; 9.87; 10.10; 9.85; 9.52; 11.35; 9.72; 10.08; 9.78; 11.25; 10.67; 11.03
  - 2012: 10.48; 8.98; 10.51; 12.32; 11.95; 12.14; 10.93; 11.61; 10.71; 11.36; 10.93; 11.11
  - 2013: 8.07; 9.60; 12.01; 8.84; 11.65; 10.48; 9.88; 12.14; 11.88; 9.59; 11.00; 10.67
  - 2014: 10.85; 10.14; 11.20; 11.44; 9.28; 10.00; 9.86; 10.39; 9.74; 9.12; 10.18; 9.62
  - 2015: 8.47; 10.87; 9.15; 9.33; 9.22; 9.13; 9.60; 9.73; 8.49; 11.07; 9.46; 11.79
  - 2016: 9.38; 9.39; 11.51; 9.61; 9.73; 9.49; 9.66; 9.18; 8.15; 10.19; 9.93; 9.29
  - 2017: 7.74; 7.40; 8.14; 8.66; 8.63; 7.89; 8.99; 8.57; 8.25; 7.94; 9.17; 9.95
  - 2018: 8.03; 7.02; 8.45; 8.09; 9.83; 8.83; 8.60; 9.02; 8.14; 8.21; 8.89; 8.16
  - 2019: 5.97; 7.99; 8.65; 8.16; 8.13; 9.28; 9.07; 10.18; 7.99; 7.24; 7.98; 8.98
  - 2020: 8.31; 8.15; 11.35; 11.69; 13.50; 9.97; 8.93; 10.51; 8.95; 9.66; 8.85; 9.60
  - 2021: 6.84; 7.36; 10.04; 10.69; 8.36; 8.34; 9.16; 7.98; 7.87; 8.12; 9.47; 9.48
  - 2022: 8.75; 7.41; 10.27; 7.86; 8.18; 8.02; 8.01; 7.47; 8.83; 7.58; 7.68; 7.53
  - 2023: 6.57; 6.23; 7.67; 8.86; 8.26; 7.58; 7.30; 6.97; 7.82; 6.32; 6.33; 6.24
  - 2024: 5.78; 6.31; 6.19; 5.19; 6.26; 6.77; 5.97; 5.77; 5.07; 4.96; 6.39; 4.35
  - 2025: 5.66; 6.82; 6.55; 5.84; 6.70; 6.25; 5.56; 5.77; 5.67; 4.99; 4.43; 6.04
- A munkalap JA2A01 adatkörből származik, és csak az ittas okozás havi összesét tartalmazza. Okozó szerinti ittas bontás a Statinfo felületén nem volt elérhető.

## 5. 4.c Összevetés a kézi STADAT-exportokkal

A `2_4_2h.xls` régi tábla 2016–2020-as hónapjai, az `ege0072.xlsx` tábla 2022–2025-ös hónapjai külön ellenőrizve.
- Mindösszesen – régi 2.4.2: 60 hónap összevetve; eltérések: 5.
- 2020-01: Statinfo=1095; STADAT=1101
- 2020-04: Statinfo=838; STADAT=837
- 2020-05: Statinfo=1030; STADAT=1029
- 2020-06: Statinfo=1274; STADAT=1271
- 2020-10: Statinfo=1325; STADAT=1324
  - Minden Mindösszesen-eltérés 2020-as: igen.
- Mindösszesen – ege0072: 48 hónap összevetve; eltérések: 0.
  - Eltérés nincs az összevetett hónapokban.
- A kimenetel-fájl tartalmazza a Halálos, Súlyos sérüléses és Könnyű sérüléses kategóriát.
- A kimenetel-fájl fejlécének oszlopkategóriái: Mindösszesen Kimenetel; Halálos; Súlyos sérüléses; Könnyű sérüléses; Nem sérült
- Sor-dimenzió a B oszlopban: Mindösszesen Kimenetel; jelenlegi rögzített értéke a havi sorokban: 15827.0.
- Halálos + súlyos + könnyű = Mindösszesen: 180 hónap összevetve; eltérések: 0.
- Halálos – régi 2.4.2: 60 hónap összevetve; eltérések: 2; 2020-01, 2020-03; mind 2020-as: igen.
- Súlyos – régi 2.4.2: 60 hónap összevetve; eltérések: 5; 2017-12, 2020-01, 2020-05, 2020-07, 2020-10; mind 2020-as: nem.
- Könnyű – régi 2.4.2: 60 hónap összevetve; eltérések: 6; 2017-12, 2020-01, 2020-03, 2020-04, 2020-06, 2020-07; mind 2020-as: nem.
- Halálos – ege0072: 48 hónap összevetve; eltérések: 0.
- Súlyos – ege0072: 48 hónap összevetve; eltérések: 0.
- Könnyű – ege0072: 48 hónap összevetve; eltérések: 0.

## 6. 4.d Kék betűszín ellenőrzése

A 2022–2026-os sorok numerikus baleseti mutatócelláinak színkódjai:
Vizsgált cellák száma: 660.
- `nincs`: 576 cella
- `rgb:FF0000FF`: 84 cella
Kék (előzetes) színnel jelölt hónapok 2022–2025-ben: nincs (48 hónap ellenőrizve).
Kék (előzetes) színnel jelölt hónapok 2026-ban: 2026-01, 2026-02, 2026-03, 2026-04, 2026-05, 2026-06, 2026-07
