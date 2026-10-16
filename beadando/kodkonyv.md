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
