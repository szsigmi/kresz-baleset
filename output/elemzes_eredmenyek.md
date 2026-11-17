# Elemzési eredmények (scripts/07_elemzes.py)

Bemenet: 23 év × 2 okozó = 46 sor. Átmeneti (szintváltási) évek, kihagyva: 2012, 2014. Elemzett: 21 év × 2 = 42 sor.

## Összefoglaló statisztika (elemzett évek)

| Változó | N | Átlag | Szórás | Min. | Max. |
|---|---:|---:|---:|---:|---:|
| Ittas arány, kerékpáros okozó (%) | 21 | 20,79 | 4,12 | 8,76 | 26,20 |
| Ittas arány, személygépkocsi-vezető okozó (%) | 21 | 9,60 | 1,99 | 7,16 | 12,95 |
| Különbség (százalékpont) | 21 | 11,18 | 3,20 | 1,60 | 17,28 |
| Balesetek, kerékpáros okozó (db/év) | 21 | 1737,19 | 190,83 | 1289,00 | 2004,00 |
| Balesetek, személygépkocsi-vezető okozó (db/év) | 21 | 11004,95 | 1453,31 | 8837,00 | 13365,00 |
| Lazítás foka (0–2) | 21 | 0,90 | 1,00 | 0,00 | 2,00 |

## Átlagos ittas arány a szintskála szakaszaiban

| Csoport | 2001–2011 (3) | 2013 (2) | 2015–2023 (1) | Változás 3→1 (pp) |
|---|---:|---:|---:|---:|
| Kerékpáros okozó | 23,34% | 22,90% | 17,43% | -5,91 |
| Személygépkocsi-vezető okozó | 11,14% | 8,64% | 7,83% | -3,31 |

Különbségek különbsége (átlagokból, 2001–2011 vs. 2015–2023): -2,60 pp

## Becslések (pp, Newey–West SE, késleltetés: 2)

| Változat | Becslés | SE | 95% CI | Évek |
|---|---:|---:|---|---:|
| Fő becslés: zéró tolerancia (2001–2011) vs. teljes lazítás (2015–2023) | -2,60 | 1,79 | [-6,11; 0,91] | 20 |
| Lépésenként: a lazítás foka (0–2), 2013-mal együtt | -1,28 | 0,91 | [-3,06; 0,49] | 21 |
| 2023 nélkül | -1,60 | 1,31 | [-4,18; 0,98] | 19 |
| 2022–2023 nélkül | -1,00 | 1,10 | [-3,16; 1,17] | 18 |
| COVID-évek (2020–2021) nélkül | -2,51 | 2,05 | [-6,52; 1,50] | 18 |
| Szűk ablak: 2007–2011 vs. 2015–2019 | -2,05 | 0,81 | [-3,65; -0,46] | 10 |
| Lineáris trenddel (megszakított idősor) | -1,42 | 4,56 | [-10,36; 7,51] | 20 |
| Régi felosztás: 2001–2013 vs. 2015–2023 | -2,81 | 1,72 | [-6,17; 0,56] | 22 |

## Placebo-időpontok

| Placebo-év | Szakasz | Becslés (pp) | 95% CI |
|---:|---|---:|---|
| 2004 | 2001–2011 | 2,94 | [1,00; 4,87] |
| 2005 | 2001–2011 | 2,68 | [0,48; 4,89] |
| 2006 | 2001–2011 | 2,41 | [-0,30; 5,13] |
| 2007 | 2001–2011 | 3,34 | [1,87; 4,81] |
| 2008 | 2001–2011 | 3,40 | [1,93; 4,86] |
| 2009 | 2001–2011 | 3,38 | [1,65; 5,11] |
| 2018 | 2015–2023 | -3,88 | [-7,96; 0,21] |
| 2019 | 2015–2023 | -4,31 | [-8,48; -0,14] |
| 2020 | 2015–2023 | -5,33 | [-8,95; -1,71] |
