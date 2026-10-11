# Projekt: KRESZ-módosítások és közúti balesetek (2005–2025)

Egyetemi beadandó az „AI a társadalomtudományokban” kurzusra. A cél egy dokumentált, ellenőrizhető adatbázis, amely a KRESZ (1/1975. (II. 5.) KPM–BM együttes rendelet) módosításait a magyarországi személysérüléses közúti balesetek adataival kapcsolja össze. A munkafolyamat átláthatósága ugyanolyan fontos, mint az eredmény.

## Alapszabályok

1. Soha ne találj ki adatot, URL-t, táblakódot, jogszabályszámot vagy dátumot. Ha valamit nem találsz, írd le, hogy nem találtad, és állj meg.
2. Minden adatsorhoz tartozzon forrás: a pontos URL és a letöltés dátuma.
3. A letöltött nyers fájlokat változatlanul a `data/raw/` mappába mentsd. Módosítani csak a `data/processed/` alatti, szkriptből előállított fájlokat szabad.
4. Minden feldolgozás szkriptből történjen (`scripts/`), hogy a teljes folyamat újrafuttatható legyen. A CSV-fájlokat ne szerkeszd kézzel.
5. Hiányzó értéket ne pótolj és ne interpolálj: hagyd üresen, és jelezd.
6. Ha egy forrásban definíció- vagy módszertanváltás látszik (új kategória, törés az idősorban, előzetes és végleges adat keveredése), jelezd külön.
7. Ha egy lépés előtt azt kérem, hogy állj meg és mutasd meg a tervet vagy a forráslistát, ne lépj tovább a jóváhagyásom nélkül.
8. Weboldalak letöltésekor kérések között tarts legalább 1–2 másodperc szünetet, és a már letöltött oldalakat gyorsítótárazd a `data/raw/cache/` mappában.
9. Minden munkamenet végén írj rövid bejegyzést a `docs/valtozasnaplo.md` fájlba: mit csináltál, mely fájlok változtak, mi maradt bizonytalan. Az `AI_NAPLO.md` fájlt ne szerkeszd, az a hallgatóé.

## Technikai keret

- Python 3, virtuális környezet a `.venv/` mappában, függőségek a `requirements.txt` fájlban.
- Kimenetek: UTF-8 kódolású CSV. Dátum: ÉÉÉÉ-HH-NN, hónap: ÉÉÉÉ-HH.
- Adattáblák „hosszú” formátumban (egy sor = egy időpont × egy mutató), forrás-oszloppal.
- Ábrák PNG-ként az `output/` mappába.
- A szkriptek számozottak (`01_...py`, `02_...py`), a kommentek magyarul.

## Mappastruktúra

```
data/raw/          nyers, letöltött fájlok (nem módosítandó)
data/raw/cache/    letöltött weboldalak gyorsítótára
data/processed/    tisztított, elemzésre kész táblák
scripts/           számozott feldolgozó szkriptek
output/            ábrák, táblázatok
docs/              forráslista, kódkönyv, változásnapló
AI_NAPLO.md        a hallgató reflektív munkanaplója (ne szerkeszd)
```
