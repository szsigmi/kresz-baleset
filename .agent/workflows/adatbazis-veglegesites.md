# Adatbázis véglegesítési munkafolyamat

## Cél

A KRESZ-változások és a közúti balesetek végleges CSV-tábláinak újrafuttatható előállítása és dokumentált ellenőrzése.

## Futtatás

1. Ellenőrizd, hogy a szükséges nyers forrásfájlok megvannak a `data/raw/` alatt. A nyers XLSX- és NJT-fájlokat ne módosítsd.
2. Futtasd a projekt virtuális környezetében: `.venv/bin/python scripts/06_validalas.py`.
3. Olvasd át a `docs/validacio_jelentes.md` ellenőrzési táblázatát, illesztési számait, származás-auditját és eltéréslistáját.
4. Ha bármely ellenőrzés eltérést jelez, állj meg. Ne írd át kézzel a CSV-t és ne javíts adatot a forrás ellenőrzése és a kutató döntése előtt.
5. Sikeres validálásnál ellenőrizd a végleges CSV-k sor- és oszlopszámát, a forrásmezőket és az azonosítókat.
6. Frissítsd a kódkönyvet és a `docs/valtozasnaplo.md` fájlt az érintett módszerrel, változott fájlokkal és fennmaradó bizonytalanságokkal.
7. A változásokat csak áttekintés után commitold. Az `AI_NAPLO.md` a hallgató saját naplója, ne módosítsd.

## Adatkezelési szabályok

- A végleges CSV-ket kizárólag szkripttel állítsd elő a `data/final/` alatt.
- Hiányzó értéket ne pótolj és ne interpolálj.
- Minden tábla őrizzen meg forrás URL-t és letöltési dátumot.
- A független forrás-összevetésnél a vizsgált éveket és az összehasonlított elemszámot is jelentsd.
- A jogszabályi és KSH-adatdefiníciók változásait külön dokumentáld.
