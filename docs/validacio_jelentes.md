# Végleges adatbázis validációs jelentése

Futtatás: `python scripts/06_validalas.py`. A CSV-k UTF-8, vesszővel tagolt fájlok. A validálás nem javít adatot automatikusan.

## Ellenőrzések

| Ellenőrzés | Eredmény | Hibák száma |
|---|---|---:|
| sorszám: KRESZ (várt 95) (95 összevetett elem) | MEGFELELT | 0 |
| sorszám: havi (várt 180) (180 összevetett elem) | MEGFELELT | 0 |
| sorszám: éves (várt 46) (46 összevetett elem) | MEGFELELT | 0 |
| valtozas_id egyediség (95 összevetett elem) | MEGFELELT | 0 |
| valtozas_id regex (95 összevetett elem) | MEGFELELT | 0 |
| honap_id egyediség (180 összevetett elem) | MEGFELELT | 0 |
| honap_id regex (180 összevetett elem) | MEGFELELT | 0 |
| sor_id egyediség (46 összevetett elem) | MEGFELELT | 0 |
| sor_id regex (46 összevetett elem) | MEGFELELT | 0 |
| forrás URL kitöltött (321 összevetett elem) | MEGFELELT | 0 |
| kötelező mezők hiánya (321 összevetett elem) | MEGFELELT | 0 |
| éves tartomány és arány (46 összevetett elem) | MEGFELELT | 0 |
| havi értéktartomány (180 összevetett elem) | MEGFELELT | 0 |
| UTF-8/mojibake jelölők (95 összevetett elem) | MEGFELELT | 0 |
| NEM VÉGEZHETŐ EL: havi összeg vs KSH éves összes (nincs megfelelő éves nyers XLSX) (0 összevetett elem) | NEM VÉGEZHETŐ EL | 0 |
| havi időpontok forráslefedettsége (180 összevetett elem) | MEGFELELT | 0 |
| éves forráscella-rekonstrukció (92 összevetett elem) | MEGFELELT | 0 |
| kapcsolat éves→KRESZ many:1; sorok=46, illesztés=100.0%, ismételt hivatkozás=45, join-expanzió=0, párosítatlan=0 (46 összevetett elem) | MEGFELELT | 0 |
| kapcsolat KRESZ→havi many:1; sorok=95, illesztés=100.0%, ismételt hónap-hivatkozás=72, join-expanzió=0, párosítatlan=0 (2010 várt=0) (95 összevetett elem) | MEGFELELT | 0 |

## Származás-audit

### balesetek_havi
Verdict: FAITHFUL ✅ — a végleges havi tábla a feldolgozott Statinfo táblával soronként egyezik; a nyers XLSX-ekből a 01-es beolvasó logikáját használja.
Sources: `data/raw/statinfo_JA2A01_*.xlsx` (native) · Statinfo JA2A01 kézi exportok.
Defect: nem találtam sémaeltolódásra, duplázódásra vagy sorvesztésre utaló eltérést.
Evidence: időszak és rekordérték összevetése; az éves KSH-független összevetést a fenti tábla mutatja.

| metric | current table | rebuilt from source | Δ |
|---|---:|---:|---:|
| rows | 180 | 180 | 0 |
| misaligned rows | 0 | 0 | 0 |

Written: `data/final/balesetek_havi.csv` · rebuild script `scripts/06_validalas.py`.
Held for sign-off: nincs módosult megfigyelésszám.

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

A havi és az éves tábla eltérő mutatókat és időbontást tartalmaz; a 2011–2025-ös havi összesítés független KSH éves táblával csak átfedő évekre vethető össze. Az előzetes/végleges státusz és a 2024-től jelzett kerékpáros ittasságvizsgálati törés megmarad a forrás korlátjaként.
A szövegkorpuszra szabott sentiment, Wordfish, topikmodell, TF-IDF, mondattokenizálás és szöveghossz-kiugró elemzés nem értelmezhető normatív rendelkezések vagy aggregált számtáblák validálására; ezért kimaradt. A régi/új jogszöveget UTF-8, üresség és gyanús mojibake-karakter alapján ellenőriztem.
