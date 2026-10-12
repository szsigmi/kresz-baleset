# KRESZ-módosítások: forrásfeltárás

## Cél és időszak

A következő feldolgozás célja az 1/1975. (II. 5.) KPM–BM együttes rendelet 2010. január 1. és 2025. december 31. között hatályba lépett módosításainak tételes jegyzéke: módosító jogszabály száma és címe, kihirdetés napja, a hatálybalépés napja rendelkezésenként, valamint az érintett §-ok. Ez a dokumentum forrásfeltárás, nem a végleges jogszabályjegyzék.

**Korlát:** a 16. időállapot 2010-01-01-jén kezdődik, de az NJT verziólistájában nincs 15. állapot, a `.15` URL pedig a főoldalra irányít. Emiatt a 2010-01-01-i váltás előző szöveggel nem hasonlítható össze. A vizsgálat a 16. verziót használja kiinduló állapotként; ez a korlát a 2011-ben kezdődő baleseti adatsort nem érinti.

## Hálózati hozzáférés

2026-10-12-én a projekt `.venv`-jében lévő `requests` csomaggal és annak certifi tanúsítványtárával sikerült lekérni a [robots.txt](https://njt.jog.gov.hu/robots.txt) fájlt (HTTP 200). A szabály `User-Agent: *` mellett kifejezetten engedélyezi többek között a `/jogszabaly/*` útvonalat, és tiltja a `/search/*` útvonalat. A robots.txt az `/ajax/` útvonalat nem tiltja; a verziólista-végpont használata ezért megengedett. A keresőt és a tiltott útvonalat nem használtam. A KRESZ-oldalhoz kapcsolódó, alább felsorolt jogszabály- és verziólistát adó URL-eket közvetlenül megnyitottam.

## A KRESZ-oldal és időállapotai

A [KRESZ NJT-oldala](https://njt.jog.gov.hu/jogszabaly/1975-1-20-24) HTTP 200-zal HTML formában nyílt meg. Az oldalon a „Hatályosság választás” gomb jelenik meg; a verziólista nem a kezdeti HTML-ben található, azt az oldal kliensoldali működése tölti be. A lista az oldalról meghatározott azonosítóval a [verziólista végpontról](https://njt.jog.gov.hu/ajax/collectAllDocumentVersion.json) kérhető le; a megnyitott kérés a KRESZ dokumentumazonosítóját adta át, és 26 állapotot sorolt fel (a legkisebb verziószám 16). A felület által használt URL-minta a jogszabályoldal azonosítójához ponttal fűzött verziószám, például `1975-1-20-24.16`.

Mintaként megnyitott korábbi időállapotok:

- [16. verzió](https://njt.jog.gov.hu/jogszabaly/1975-1-20-24.16): 2010.01.01-től;
- [25. verzió](https://njt.jog.gov.hu/jogszabaly/1975-1-20-24.25): 2013.07.01-től;
- [33. verzió](https://njt.jog.gov.hu/jogszabaly/1975-1-20-24.33): 2021.02.01-től.

Mindhárom URL HTML-jogszabályszöveget adott vissza. A megnyitott oldalakon van másolási/export kezelőfelület, de ebből a felmérésből önálló letölthető adatfájlt (például CSV vagy géppel feldolgozható teljes módosítási jegyzéket) nem igazoltam. A HTML a feldolgozás elsődleges elérhető formátuma; az exportálás pontos formátumát egy későbbi próbalépésben kell megállapítani.

A hatályos szövegben lábjegyzetjelölések kapcsolódnak a rendelkezésekhez, a lábjegyzetek pedig sok esetben a módosító jogszabály oldalára és annak konkrét rendelkezésére hivatkoznak. Például a [369/2025. (XI. 28.) Korm. rendelet oldala](https://njt.jog.gov.hu/jogszabaly/2025-369-20-22) megnyitható. A KRESZ-oldal lábjegyzetei tehát használható hivatkozási nyomvonalat adnak az aktuális szöveg eredetéhez.

## A három módszer lefedettsége

| Módszer | Mit ad | Korlát |
|---|---|---|
| A jelenlegi, egységes szerkezetű szöveg lábjegyzetei | A jelenlegi szövegben jelölt rendelkezésekhez kapcsolt beiktatási vagy módosítási hivatkozásokat; gyakran az eredeti módosító jogszabály és az érintett rendelkezés is szerepel. | Önmagában nem tekinthető teljes történeti jegyzéknek: a ma már nem hatályos, később lecserélt vagy hatályon kívül helyezett rendelkezések módosításai hiányozhatnak a jelenlegi szövegből. Egy lábjegyzet a teljes módosító rendelet összes, a KRESZ-t érintő rendelkezését sem feltétlenül sorolja fel. |
| Az időállapotok listája | Folytonos szövegállapotokat és az egyes állapotok kezdő, illetve záró hatályossági dátumát adja. A vizsgált listában a 2010-es állapot is szerepel. | Nem mondja meg önmagában, mely módosító jogszabály mely §-ai hozták létre a változást, mikor hirdették ki, vagy az adott rendelet egyes rendelkezései mikor léptek hatályba. Az egymást követő állapotok összehasonlítása változásokat mutat, de a jogszabályi okot és a rendelkezésenkénti hatálybalépést külön kell visszakeresni. |
| A módosító rendeletek saját oldalai | A módosító jogszabály címét, kihirdetési adatait, normaszövegét, hatálybaléptető rendelkezéseit és a módosított §-okat közvetlenül tartalmazhatják. Ez adja a végleges tételes jegyzékhez szükséges jogi bizonyítékot. | A KRESZ-re vonatkozó módosítások egy rendeletben több cikkben/§-ban lehetnek, eltérő hatálybalépéssel; az oldal önmagában nem garantálja, hogy csak a KRESZ-módosító jogszabályokat találjuk meg. Ki kell szűrni a KRESZ-t valóban módosító rendelkezéseket, majd rendelkezésenként rögzíteni a hatályt. |

Következtetés: a teljes jegyzéket nem szabad kizárólag a hatályos szöveg lábjegyzeteiből előállítani. Az időállapotok listája adhat ellenőrizhető teljességi keretet az időbeli változásokhoz; a végleges sorokat a módosító rendeletek saját szövegével és hatálybaléptető rendelkezéseivel kell alátámasztani. A lábjegyzeteket keresztellenőrzésre és a releváns módosító jogszabályok felderítésére kell használni.

## Javasolt letöltési és feldolgozási terv

1. A megengedett NJT-jogszabályoldalakról géppel olvasható módon mentsük el az időállapotok listáját, és szűrjük ki azokat az állapotváltásokat, amelyek kezdődátuma 2010-01-01 és 2025-12-31 közé esik. Ez legyen az időbeli teljességi ellenőrzés alapja, ne önmagában a rendeletlista.
2. A releváns hatályállapotok előtti és utáni HTML-szövegeket csak a változó szakaszok azonosításához dolgozzuk fel. A szövegdifferenciát párosítsuk a KRESZ-oldal lábjegyzet-hivatkozásaival.
3. Minden lehetséges módosító jogszabály saját NJT-oldalán ellenőrizzük a jogszabály címét, kihirdetési napját, a KRESZ-t érintő rendelkezéseit és azok külön hatálybalépését. A hatálybalépési záradékokat rendelkezésenként rögzítsük; ne következtessünk a rendelet címéből vagy az általános hatálybalépésből.
4. A kimeneti táblában legyen forrás URL, lekérés dátuma, módosító jogszabály és §, érintett KRESZ §, kihirdetés dátuma, valamint a konkrét rendelkezés hatálybalépési dátuma. Külön jelöljük a hatályon kívül helyezést és azokat a helyzeteket, ahol a KRESZ-szöveg összevetése nem elég a módosító rendelkezés azonosításához.
5. Teljességi ellenőrzésként hasonlítsuk össze az összegyűjtött hatálybalépési napokat az időállapot-lista minden 2010–2025 közötti váltásával, majd ellenőrizzük a lábjegyzetekben feltárt, de a változáslistából esetleg hiányzó vagy több időpontban hatályba lépő módosításokat.

## A munkamenet során megnyitott forrás-URL-ek

- https://njt.jog.gov.hu/robots.txt
- https://njt.jog.gov.hu/jogszabaly/1975-1-20-24
- https://njt.jog.gov.hu/ajax/collectAllDocumentVersion.json (a KRESZ dokumentumazonosítóval lekért lista)
- https://njt.jog.gov.hu/jogszabaly/1975-1-20-24.16
- https://njt.jog.gov.hu/jogszabaly/1975-1-20-24.17
- https://njt.jog.gov.hu/jogszabaly/1975-1-20-24.18
- https://njt.jog.gov.hu/jogszabaly/1975-1-20-24.19
- https://njt.jog.gov.hu/jogszabaly/1975-1-20-24.20
- https://njt.jog.gov.hu/jogszabaly/1975-1-20-24.21
- https://njt.jog.gov.hu/jogszabaly/1975-1-20-24.22
- https://njt.jog.gov.hu/jogszabaly/1975-1-20-24.23
- https://njt.jog.gov.hu/jogszabaly/1975-1-20-24.24
- https://njt.jog.gov.hu/jogszabaly/1975-1-20-24.25
- https://njt.jog.gov.hu/jogszabaly/1975-1-20-24.26
- https://njt.jog.gov.hu/jogszabaly/1975-1-20-24.27
- https://njt.jog.gov.hu/jogszabaly/1975-1-20-24.28
- https://njt.jog.gov.hu/jogszabaly/1975-1-20-24.29
- https://njt.jog.gov.hu/jogszabaly/1975-1-20-24.30
- https://njt.jog.gov.hu/jogszabaly/1975-1-20-24.31
- https://njt.jog.gov.hu/jogszabaly/1975-1-20-24.32
- https://njt.jog.gov.hu/jogszabaly/1975-1-20-24.33
- https://njt.jog.gov.hu/jogszabaly/1975-1-20-24.34
- https://njt.jog.gov.hu/jogszabaly/1975-1-20-24.35
- https://njt.jog.gov.hu/jogszabaly/1975-1-20-24.36
- https://njt.jog.gov.hu/jogszabaly/1975-1-20-24.37
- https://njt.jog.gov.hu/jogszabaly/1975-1-20-24.38
- https://njt.jog.gov.hu/jogszabaly/1975-1-20-24.39
- https://njt.jog.gov.hu/jogszabaly/2010-280-20-22
- https://njt.jog.gov.hu/ajax/collectAllDocumentVersion.json (a 228/2012. és 317/2020. rendelet verziólistájának lekérdezése)
- https://njt.jog.gov.hu/jogszabaly/2012-228-20-22
- https://njt.jog.gov.hu/jogszabaly/2012-228-20-22.1
- https://njt.jog.gov.hu/jogszabaly/2016-447-20-22
- https://njt.jog.gov.hu/jogszabaly/2020-317-20-22
- https://njt.jog.gov.hu/jogszabaly/2020-317-20-22.7
- https://njt.jog.gov.hu/jogszabaly/2025-369-20-22

Az időállapot-HTML-ek és a verziólisták változatlan válaszai a `data/raw/` és `data/raw/cache/` alatt vannak. A 2010-01-02–2025-12-31 időablak mind a 23 összevethető váltását feldolgoztam; a módosító rendeletek tömeges letöltése nem történt, saját szövegükkel négy mintát ellenőriztem. Az összesítő és a kontrollcsoportok részletei: [docs/kresz_valtozasok_osszegzes.md](kresz_valtozasok_osszegzes.md).
