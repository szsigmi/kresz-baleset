> **Elavult: a 2026. október 16-i előzetes adatcsomag leírása, változatlanul megőrizve.** Az itt szereplő −2,808 százalékpont a 2001–2013 vs. 2015–2023 felosztásból jött. Később kiderült, hogy a kerékpárosok alkoholszabályának első lazítása már 2012-ben megtörtént, ezért a végleges elemzés 2001–2011-et hasonlítja 2015–2023-hoz: −2,60 százalékpont, 95%-os konfidencia-intervallum [−6,1; +0,9]. Lásd: [`../elemzes_20261117_v2.pdf`](../elemzes_20261117_v2.pdf).

# Előzetes adatcsomag — KRESZ és ittas kerékpáros okozás

Készült: 2026-10-16. Az adat a KSH 2001–2023 közötti éves STADAT-tábláiból készült. A CSV 46 sora járműtípusonként 23 évet tartalmaz.

## Források

- KSH STADAT 4.1.1.50, okozó járműtípus szerinti balesetszám, XLSX: https://www.ksh.hu/stadat_files/ege/hu/ege0064.xlsx — letöltve 2026-10-16. Táblalap: https://www.ksh.hu/stadat_files/ege/hu/ege0064.html
- KSH STADAT 4.1.1.52, ittas okozás és okozótípus, XLSX: https://www.ksh.hu/stadat_files/ege/hu/ege0066.xlsx — letöltve 2026-10-16. Táblalap: https://www.ksh.hu/stadat_files/ege/hu/ege0066.html
- KRESZ időállapotok (26. verzió, előtte): https://njt.jog.gov.hu/jogszabaly/1975-1-20-24.26 — a projekt nyers állományának letöltése: 2026-10-12.
- KRESZ időállapotok (27. verzió, utána): https://njt.jog.gov.hu/jogszabaly/1975-1-20-24.27 — a projekt nyers állományának letöltése: 2026-10-12.
- KRESZ-változások CSV: a fenti NJT-időállapotokból előállítva; forrás-URL-enkénti leltár szerepel az `forras_url` oszlopban, nyers időállapotok letöltve 2026-10-12.
- Havi baleseti CSV: KSH Statinfo JA2A01 kézi exportok; https://statinfo.ksh.hu/Statinfo/QueryServlet?ha=JA2A01 — exportok letöltve 2026-10-12.

## Képzett mutató és előzetes eredmény

Az `ittas_arany` = `ittas_baleset / osszes_baleset`. Az egyszerű DiD a 2015–2023-as éves átlagarány és a 2001–2013-as éves átlagarány különbsége kerékpárosoknál, mínusz ugyanez személygépkocsi-vezetőknél. A számított különbség **-2.808 százalékpont**. Kerékpár: előtte 23.236%, utána 17.434%; személygépkocsi: előtte 10.826%, utána 7.832%.

Az érzékenységi számítás 2015–2022-re (2023 nélkül) a következő: kerékpár 23.236% → 18.518%, személygépkocsi 10.826% → 7.916%; DiD **-1.808 százalékpont**.

Ez leíró, előzetes összehasonlítás, nem okozati hatásbecslés. A 2014-es átmeneti évet kizártuk az előtte/utána átlagokból; a COVID-éveket külön jelöltük. A 2022–2023-as kerékpáros arány hirtelen csökkenése lehetséges adatfelvételi törésre utalhat, de önmagában nem igazolja azt.

A 172/2014. (VII. 18.) Korm. rendelet 2014. július 19-től a főútvonalakra is kiterjesztette a kerékpárosok felmentését az alkohol jelenlétére vonatkozó tilalom alól; a befolyásoltság továbbra is tilos maradt.

## A ZIP tartalma

- `kerekpar_ittas_eves.csv` és `kerekpar_ittas_arany.png`: elemzési tábla és ábra.
- `kresz_valtozasok.csv`: KRESZ-rendelkezésenkénti változások 2010–2025 között.
- `balesetek_havi.csv`: Statinfo JA2A01 havi idősor 2011–2025 között.
- `kodkonyv.md` és `genai_modszertan.md`: változók, források, ellenőrzések és korlátok.
