# Előzetes adatcsomag — KRESZ és ittas kerékpáros okozás

Készült: 2026-10-16. Az adat a KSH 2001–2023 közötti éves STADAT-tábláiból készült. A CSV 46 sora járműtípusonként 23 évet tartalmaz.

## Források

- KSH STADAT 4.1.1.50, okozó járműtípus szerinti balesetszám, XLSX: https://www.ksh.hu/stadat_files/ege/hu/ege0064.xlsx — letöltve 2026-10-16. Táblalap: https://www.ksh.hu/stadat_files/ege/hu/ege0064.html
- KSH STADAT 4.1.1.52, ittas okozás és okozótípus, XLSX: https://www.ksh.hu/stadat_files/ege/hu/ege0066.xlsx — letöltve 2026-10-16. Táblalap: https://www.ksh.hu/stadat_files/ege/hu/ege0066.html
- KRESZ időállapotok (26. verzió, előtte): https://njt.jog.gov.hu/jogszabaly/1975-1-20-24.26 — a projekt nyers állományának letöltése: 2026-10-12.
- KRESZ időállapotok (27. verzió, utána): https://njt.jog.gov.hu/jogszabaly/1975-1-20-24.27 — a projekt nyers állományának letöltése: 2026-10-12.

## Képzett mutató és előzetes eredmény

Az `ittas_arany` = `ittas_baleset / osszes_baleset`. Az egyszerű DiD a 2015–2023-as éves átlagarány és a 2001–2013-as éves átlagarány különbsége kerékpárosoknál, mínusz ugyanez személygépkocsi-vezetőknél. A számított különbség **-2.808 százalékpont**. Kerékpár: előtte 23.236%, utána 17.434%; személygépkocsi: előtte 10.826%, utána 7.832%.

Ez leíró, előzetes összehasonlítás, nem okozati hatásbecslés. A 2014-es átmeneti évet kizártuk az előtte/utána átlagokból; a COVID-évek a 2015–2023 utáni csoport részei.
