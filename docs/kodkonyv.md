# Kódkönyv – KRESZ-változások és közúti balesetek

**Adatbázis-verzió:** 2026-11-03 · **Terjedelem:** három CSV-tábla · **Kódolás:** UTF-8, vesszővel tagolt, fejlécsorral. Az üres érték hiányzó adatot jelent; nincs imputálás. A forrásfájlok változatlanul a `data/raw/` mappában vannak. A végleges fájlokat a `scripts/06_validalas.py` állítja elő.

## Cél, egységek és lefedettség

Az adatbázis a KRESZ időállapotai között azonosított rendelkezésváltozásokat, a havi személysérüléses balesetszámokat és az éves, járműtípus szerinti ittas okozás mutatóit teszi ellenőrizhetővé. A KRESZ-tábla 95 változássort tartalmaz a 2010–2025 közötti vizsgált hatálybalépésekről. A havi tábla 180 megfigyelése 2011 januárjától 2025 decemberéig tart, havonta egy teljes balesetszámmal. Az éves tábla 46 sort tartalmaz: 2001–2023, két járműtípus (kerékpár és személygépkocsi). Az éves tábla 2024–2025-öt nem fedi le.

## `kresz_valtozasok.csv`

Egy sor = egy megváltozott rendelkezés egy hatálybalépési eseményben. A régi és új normaszöveg megmarad, a változástípus új/módosított/hatályon kívül helyezett érték.

| Változó | Jelentés |
|---|---|
| `valtozas_id` | Egyedi kulcs: `KÉÉÉÉ-HH-NN_rendelkezés` formátum, pl. `K2014-07-19_4-§-4`. |
| `verzio_elotte`, `verzio_utana` | A NJT összevetett időállapotainak sorszáma. |
| `hatalybalepes` | Hatálybalépés dátuma, ISO `ÉÉÉÉ-HH-NN`. |
| `rendelkezes`, `valtozas_tipusa` | Érintett KRESZ-egység és változás jellege. |
| `regi_szoveg`, `uj_szoveg` | A rendelkezés szövege a két időállapotban; üres szöveg új vagy hatályon kívül helyezett rendelkezésnél értelmezett. |
| `modosito_jogszabaly`, `modosito_rendelkezes` | Az NJT-időállapot lábjegyzetéből kinyert jogszabály és közlés. |
| `forras_url` | Mindkét összevetett NJT-időállapot pontos címe. |
| `letoltes_datuma` | A nyers NJT-állomány projektbeli letöltési dátuma: 2026-10-12. |

## `balesetek_havi.csv`

Egy sor = egy hónap teljes személysérüléses balesetszáma. Forrás: kézi KSH Statinfo JA2A01-export `statinfo_JA2A01_helye.xlsx`, feldolgozási időszak 2011–2025; letöltve 2026-10-12.

| Változó | Jelentés |
|---|---|
| `honap_id` | Egyedi hónapkulcs, `ÉÉÉÉ-HH`. |
| `adatkor`, `dimenzio`, `kategoria` | Statinfo-adatkör, dimenzió és kategória. A végleges tábla a `Baleset helye` dimenzió `Mindösszesen Baleset helye` sorát tartalmazza. |
| `szulo_kategoria` | Hierarchikus szülőkategória; ennél az összesítő sornál üres. |
| `ertek` | Balesetek száma darabban, az eredeti export numerikus értéke. |
| `ures_cella_kezelese` | Forráscella-kezelési megjegyzés. |
| `forras_fajl`, `forras_oszlop` | Nyers export neve és eredeti oszlopszáma. |
| `forras_url`, `letoltes_datuma` | Statinfo JA2A01 lekérdezési cím és exportdátum. |

## `kerekpar_ittas_eves.csv`

Egy sor = egy naptári év × okozótípus. A két KSH éves XLSX-ből 2001–2023 időszakra épül; letöltésük dátuma 2026-10-16.

| Változó | Jelentés |
|---|---|
| `sor_id` | Egyedi kulcs, például `2014_kerekpar`. |
| `ev`, `okozo` | Naptári év; `kerekpar` vagy `szemelygepkocsi`. |
| `osszes_baleset` | Az adott okozótípushoz tartozó balesetek száma (KSH 4.1.1.50). |
| `ittas_baleset` | Ittas okozóhoz tartozó balesetek száma (KSH 4.1.1.52). |
| `ittas_arany` | `ittas_baleset / osszes_baleset`, 0–1 arány, tíz tizedesre kiírva. |
| `utana`, `atmeneti`, `covid` | Jelzőváltozók: 2015-től; 2014 átmeneti év; 2020 vagy 2021. |
| `valtozas_id` | Kapcsolókulcs a 2014-07-19-i KRESZ 4. § (4) változáshoz. |
| `forras_url`, `letoltes_datuma` | Két KSH-forrás XLSX URL-je és a letöltés napja. |

## Kapcsolatok, validálás és korlátok

Az éves tábla `valtozas_id` mezője a KRESZ-tábla kulcsára **many:1** kapcsolatú: 46 forrássor mind a 2014-es rendelkezéshez kapcsolódik, 46/46 illesztéssel. A KRESZ-változás hatálybalépési hónapja és a havi `honap_id` kapcsolata szintén **many:1**. A 2010-es KRESZ-változásokhoz nem tartozik havi pár; ez várt. A részletes sor- és illesztési számokat a `docs/validacio_jelentes.md` közli.

A Statinfo kategóriarendszer 2011-től egységes. A KSH éves kerékpáros ittassági táblája jelzi, hogy 2024-től a rendőrség nem minden esetben vizsgálja a kerékpárosok ittasságát; a sor időbeli összevethetősége korlátozott. Havi–éves független összegellenőrzés nem végezhető el a helyi nyers állományokkal: a meglévő `ege0072.xlsx` havi tábla 2022-től indul, éves megfelelő tábla nincs letöltve.

A korpuszokra írt sentiment-, Wordfish-, topikmodell-, TF-IDF- és mondattokenizálási vizsgálat nem értelmezhető jogszabályi összehasonlításra vagy aggregált havi/éves táblákra, ezért kimaradt. A normatív szövegeknél ellenőriztük a kötelező szövegmezők, UTF-8 olvashatóság és gyakori mojibake-jelölők jelenlétét.
