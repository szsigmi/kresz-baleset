# Címkézési prompt — v1

Dátum: 2026-11-17

## Feladat és egység

Alkalmazd a `docs/iranykod_kodkonyv.md` v1 kódkönyvét a `data/processed/iranykod/szovegek/` fájljaira. Egy fájl egy egység. Minden fájlnál a benne szereplő régi és új rendelkezést vesd össze; ne az azonos napon hatályba lépő módosításcsomagot értékeld.

## Kódkönyv

A viszonyítási pont a közlekedők mozgástere: a változás után többet vagy kevesebbet szabad-e, mint előtte?

- `SZIGORITAS`: kevesebb mozgástér vagy több kötelezettség; új tilalom/kötelezettség/feltétel, szűkülő/megszűnő kivétel, szigorodó határérték, megengedő szabály hatályon kívül helyezése.
- `ENYHITES`: nagyobb mozgástér vagy kevesebb kötelezettség; tilalom/kötelezettség szűkülése vagy megszűnése, új kivétel/felmentés, enyhülő határérték, tiltó szabály hatályon kívül helyezése.
- `SEMLEGES`: a közlekedők jogosultsága/kötelezettsége nem változik (például név, elírás, átszámozás, hivatkozás, technikai vagy szervezeti pontosítás).
- `VEGYES`: a változás érdemben egyszerre tartalmaz szigorítást és enyhítést.
- `NEM_BESOROLHATO`: a szöveg csonka vagy önmagában nem elég az irány eldöntéséhez.

Döntési szabályok: új kivétel/felmentés enyhítés; új tilalom/kötelezettség szigorítás. Hatályon kívül helyezett tilalom enyhítés, kivétel szigorítás, technikai szöveg semleges. Kétségnél a szöveghiányt `NEM_BESOROLHATO`-val jelezd; a `VEGYES` helyett válaszd az uralkodó irányt, ha a másik elem csak pontosítás. Új fogalommeghatározás önmagában semleges, ha nem állapít meg szabályt.

## Leíró mezők

`csoport` kizárólag ezek egyike: `osszes_kozlekedo`, `gepjarmuvezeto`, `nehez_tehergepkocsi`, `autobusz`, `kerekparos`, `gyalogos`, `kulonleges_jarmu`, `egyeb`.

`terulet` kizárólag ezek egyike: `alkohol_vezetokepesseg`, `sebesseg`, `elozes_haladas`, `megallas_varakozas`, `jarmu_okmany_felszereles`, `gyermekbiztonsag`, `kulonleges_jarmu`, `jelzes_tabla`, `egyeb`.

## Válaszformátum és bizonyíték

Minden fájlhoz pontosan egy sort adj a `file,code,csoport,terulet,reason,sentence,model,prompt_version` oszlopokkal. A `reason` legfeljebb 20 magyar szó legyen. A `sentence` a fájlból szó szerint másolt, az irányt alátámasztó mondat vagy mondatrész; ne parafrazeálj. `NEM_BESOROLHATO` esetén a `sentence` üres lehet. Minden más mező legyen kitöltve. Ne használj a megengedett kód-, csoport- és területlistán kívüli értéket. Ne alkalmazz kulcsszavas/szabályalapú címkézést; olvasd és értelmezd az adott fájl régi és új szövegét.
