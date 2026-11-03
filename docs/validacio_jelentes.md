# Végleges adatbázis validációs jelentése

Futtatás: `python scripts/06_validalas.py`. A CSV-k UTF-8, vesszővel tagolt fájlok. A validálás nem javít adatot automatikusan.

## Ellenőrzések

| Ellenőrzés | Eredmény | Hibák száma |
|---|---|---:|
| sorszám: KRESZ (várt 95) (95 összevetett elem) | MEGFELELT | 0 |
| sorszám: havi (várt 180) (180 összevetett elem) | MEGFELELT | 0 |
| sorszám: éves (várt 46) (46 összevetett elem) | MEGFELELT | 0 |
| KRESZ-hatálybalépési dátumtartomány (2011-01-01–2025-11-29) (95 összevetett elem) | MEGFELELT | 0 |
| valtozas_id egyediség (95 összevetett elem) | MEGFELELT | 0 |
| valtozas_id regex (95 összevetett elem) | MEGFELELT | 0 |
| honap_id egyediség (180 összevetett elem) | MEGFELELT | 0 |
| honap_id regex (180 összevetett elem) | MEGFELELT | 0 |
| sor_id egyediség (46 összevetett elem) | MEGFELELT | 0 |
| sor_id regex (46 összevetett elem) | MEGFELELT | 0 |
| forrás URL kitöltött (321 összevetett elem) | MEGFELELT | 0 |
| kötelező mezők hiánya (321 összevetett elem) | MEGFELELT | 0 |
| éves tartomány és arány (46 összevetett elem) | MEGFELELT | 0 |
| havi értéktartomány és egész szám (1260 összevetett elem) | MEGFELELT | 0 |
| UTF-8/mojibake jelölők (95 összevetett elem) | MEGFELELT | 0 |
| halálos+súlyos+könnyű=összes (180 összevetett elem) | MEGFELELT | 0 |
| lakott területen belül+kívül=összes (180 összevetett elem) | MEGFELELT | 0 |
| havi értékek éves összege vs Statinfo év-sorok (105 összevetett elem) | MEGFELELT | 0 |
| havi összes éves összege vs KSH 4.1.1.50 Összesen (15 összevetett elem) | MEGFELELT | 0 |
| havi időpontok forráslefedettsége (180 összevetett elem) | MEGFELELT | 0 |
| éves forráscella-rekonstrukció (92 összevetett elem) | MEGFELELT | 0 |
| kapcsolat éves→KRESZ many:1; sorok=46, illesztés=100.0%, ismételt hivatkozás=45, join-expanzió=0, párosítatlan=0 (46 összevetett elem) | MEGFELELT | 0 |
| kapcsolat KRESZ→havi many:1; sorok=95, illesztés=100.0%, ismételt hónap-hivatkozás=72, join-expanzió=0, párosítatlan=0 (2010 várt=0) (95 összevetett elem) | MEGFELELT | 0 |

## Éves összevetés részletei

A hét havi mutató Statinfo éves soraihoz összesen 105 év × mutató értéket vetettem össze; eltérés: 0. A havi teljes éves balesetszámot a KSH 4.1.1.50 `Összesen` oszlopának mind a 15 évével (2011–2025) összevetettem; eltérés: 0.

## Származás-audit

### balesetek_havi
Verdict: FAITHFUL ✅ — a 180 havi sort közvetlenül a három nyers Statinfo XLSX-ből állítottam elő.
Sources: `statinfo_JA2A01_kimenetel.xlsx` · `statinfo_JA2A01_helye.xlsx` · `statinfo_JA2A01_ittas_osszes.xlsx` (natív nyers munkalapok).
Defect: nem találtam sémaeltolódást, kettős számlálást vagy sorvesztést.
Evidence: minden hónap × hét mutató a fejléc alapján kiválasztott eredeti forráscellából származik; a havi kategóriaösszegek, a Statinfo éves sorai és a független KSH éves összesek egyeznek.

| metric | current table | rebuilt from source | Δ |
|---|---:|---:|---:|
| rows | 180 | 180 | 0 |
| coded cells | 1260 | 1260 | 0 |
| misaligned rows | 0 | 0 | 0 |

Written: `data/final/balesetek_havi.csv` · rebuild script `scripts/06_validalas.py`.
Held for sign-off: nincs eltérő sor.

### kerekpar_ittas_eves
Verdict: FAITHFUL ✅ — a két KSH-nyers XLSX természetes kulcsa (év × okozótípus) minden végleges sorhoz értékeket szolgáltat.
Sources: `KSH_STADAT_ege0064_okozo_eves.xlsx` · `KSH_STADAT_ege0066_ittas_okozo_eves.xlsx`.
Defect: nem találtam eltolódást, kettős számlálást vagy kódolási eltérést.
Evidence: mindkét számmező nyers forráscellából újraolvasva.

| metric | current table | rebuilt from source | Δ |
|---|---:|---:|---:|
| rows | 46 | 46 | 0 |
| coded | 92 | 92 | 0 |
| misaligned rows | 0 | 0 | 0 |

Written: `data/final/kerekpar_ittas_eves.csv` · rebuild script `scripts/06_validalas.py`.
Held for sign-off: a 2024–2025-ös éves adat nem része a jelenlegi 46 soros tábla lefedettségének.

## Korlátok

Az előzetes/végleges státusz és a KSH által 2024-től jelzett kerékpáros ittasságvizsgálati törés megmarad a forrás korlátjaként.
A szövegkorpuszra szabott sentiment, Wordfish, topikmodell, TF-IDF, mondattokenizálás és szöveghossz-kiugró elemzés nem értelmezhető normatív rendelkezések vagy aggregált számtáblák validálására; ezért kimaradt. A régi/új jogszöveget UTF-8, üresség és gyanús mojibake-karakter alapján ellenőriztem.


## Eltérő rekordok

Az összevetett ellenőrzések nem találtak eltérést.