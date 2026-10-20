# Kódkönyv

| Oszlop | Jelentés |
|---|---|
| `ev` | Naptári év, 2001–2023. |
| `okozo` | Okozó járműtípus: `kerekpar` vagy `szemelygepkocsi`. |
| `osszes_baleset` | Az adott típushoz tartozó, személysérüléses balesetek száma a KSH 4.1.1.50 táblájában. |
| `ittas_baleset` | Az adott típushoz tartozó, ittas okozással jelölt személysérüléses balesetek száma a KSH 4.1.1.52 táblájában. |
| `ittas_arany` | `ittas_baleset / osszes_baleset`, 0 és 1 közötti arány; a megjelenítés százalékra szorozza. |
| `utana` | 1, ha `ev >= 2015`; egyébként 0. |
| `atmeneti` | 1 a 2014-es évre, amelyben a szabály július 19-én lépett hatályba; egyébként 0. |
| `covid` | 1 a 2020-as és 2021-es évekre; egyébként 0. |

Egy sor = egy év × okozótípus. A 2024–2025-ös éveket az adat nem tartalmazza.

## `kresz_valtozasok.csv`

| Oszlop | Jelentés |
|---|---|
| `verzio_elotte`, `verzio_utana` | NJT-időállapotok sorszáma a változás előtt és után. |
| `hatalybalepes` | A változás hatálybalépésének dátuma. |
| `rendelkezes` | Megváltozott KRESZ-rendelkezés azonosítója; a függelékek sorai is szerepelnek. |
| `valtozas_tipusa` | Új, módosított vagy hatályon kívül helyezett rendelkezés. |
| `regi_szoveg`, `uj_szoveg` | A két időállapot érintett rendelkezésének szövege. |
| `modosito_jogszabaly` | A lábjegyzetből azonosított módosító jogszabály, ha rendelkezésre áll. |
| `modosito_rendelkezes` | A módosító jogszabályra utaló NJT-lábjegyzet szó szerinti szövege. |
| `forras_url` | Az összehasonlított NJT-időállapotok URL-je. |

## `balesetek_havi.csv`

| Oszlop | Jelentés |
|---|---|
| `honap` | Hónap ÉÉÉÉ-HH formában. |
| `adatkor` | Statinfo-adatkör azonosítója. |
| `dimenzio`, `kategoria`, `szulo_kategoria` | Dimenzió, kategória és igazolt hierarchikus szülő (hiányzó kapcsolatnál üres). |
| `ertek` | A forrás szerinti havi érték. |
| `ures_cella_kezelese` | Az eredeti üres cella kezelésének jelölése. |
| `forras_fajl`, `forras_oszlop` | Helyi nyers export és munkalaposzlop. |
| `forras_url` | Statinfo-lekérdezés URL-je. |
| `letoltes_datuma` | A nyers export letöltési dátuma. |
