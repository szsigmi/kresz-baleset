# Irány-kódolás: ellenőrzés és egyezés (scripts/09_iranykod_osszesites.py)

Címke-ellenőrzés: 95 fájl · 95 címkesor · 62 kódolt · 33 félretett · hibák: 0

## Gépi kódok gyakorisága (95 változás)

| Kód | Db |
|---|---:|
| SZIGORITAS | 18 |
| ENYHITES | 23 |
| SEMLEGES | 19 |
| VEGYES | 2 |
| NEM_BESOROLHATO | 33 |

## Egyezés a kézi kódolással (n = 25)

Pontos egyezés: 60% · Cohen-féle kappa: 0.47

| Kód | n (kézi) | Arány | Pontosság (gép) | Felidézés (gép) |
|---|---:|---:|---:|---:|
| SZIGORITAS | 11 | 44% | 80% | 36% |
| ENYHITES (n < 10: nincs ítélet) | 2 | 8% | 40% | 100% |
| SEMLEGES (n < 10: nincs ítélet) | 4 | 16% | 29% | 50% |
| VEGYES (n < 10: nincs ítélet) | 0 | 0% | – | – |
| NEM_BESOROLHATO (n < 10: nincs ítélet) | 8 | 32% | 88% | 88% |

Eltérések: 10 → output/iranykod_elteresek.csv

- K2011-07-22_1-sz-m-f-ggel-k-zs.txt: kézi SZIGORITAS, gépi SEMLEGES
- K2012-08-24_5-1-c.txt: kézi SEMLEGES, gépi SZIGORITAS
- K2012-08-24_54-6.txt: kézi NEM_BESOROLHATO, gépi ENYHITES
- K2013-05-01_1-sz-m-f-ggel-k-y-1.txt: kézi SZIGORITAS, gépi SEMLEGES
- K2013-07-01_48-15-15.txt: kézi SZIGORITAS, gépi ENYHITES
- K2014-07-19_65-a.txt: kézi SZIGORITAS, gépi SEMLEGES
- K2014-09-05_1-sz-m-f-ggel-k-j-f.txt: kézi SZIGORITAS, gépi SEMLEGES
- K2014-09-05_67-d.txt: kézi SZIGORITAS, gépi SEMLEGES
- K2021-02-01_4-1-a.txt: kézi SEMLEGES, gépi ENYHITES
- K2024-12-17_36-8-b-bb-bbc.txt: kézi SZIGORITAS, gépi NEM_BESOROLHATO
