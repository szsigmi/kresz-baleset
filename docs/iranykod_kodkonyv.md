# Kódkönyv – a KRESZ-változások iránya · v1 · 2026-11-17

**Egység:** egy változás a `data/final/kresz_valtozasok.csv` táblában, vagyis egy rendelkezés változása egy hatálybalépéskor (a `valtozas_id` azonosítja). A kódoló a `data/processed/iranykod/szovegek/<valtozas_id>.txt` fájlt olvassa: a rendelkezés jelölése, a változás típusa, a régi és az új szöveg.

**Viszonyítási pont:** a közlekedők (járművezetők, gyalogosok, utasok) mozgástere. A kérdés mindig ez: *a változás után többet vagy kevesebbet szabad-e, mint előtte?* Mindig csak az adott egység szövegét kell összevetni a saját előző állapotával (új rendelkezésnél: a rendelkezés hiányával; hatályon kívül helyezettnél: a rendelkezés megszűnésével).

**Félretett kód:** `NEM_BESOROLHATO` – a szövegből nem dönthető el az irány (például csonka szöveg vagy egy önmagában értelmezhetetlen szövegtöredék).

## Kódok

### SZIGORITAS
- *Definíció:* a változás után a közlekedőknek kevesebb a mozgásterük vagy több a kötelezettségük.
- *Akkor, ha:* új tilalom, kötelezettség vagy feltétel jelenik meg; egy kivétel szűkül vagy megszűnik; egy határérték szigorodik; egy megengedő rendelkezést hatályon kívül helyeznek.
- *Példa:* „A nehéz tehergépkocsik e rendelet eltérő rendelkezése hiányában lakott területen kívül csak autópályán, autóúton és főútvonalon közlekedhetnek.” (`K2013-07-01_48-14-14`)
- *Majdnem, de nem:* „Iskolabusszal abban az esetben szabad közlekedni, ha:” (`K2013-05-01_48-12-12`) – a feltétel korábban is megvolt, csak elírást javítottak („ez” → „az”): SEMLEGES.

### ENYHITES
- *Definíció:* a változás után a közlekedőknek nagyobb a mozgásterük vagy kevesebb a kötelezettségük.
- *Akkor, ha:* egy tilalom vagy kötelezettség megszűnik vagy szűkül; új kivétel vagy felmentés jelenik meg; egy határérték enyhül; egy tiltó rendelkezést hatályon kívül helyeznek.
- *Példa:* „Az (1) bekezdés b) pontjában foglalt feltétel fennállása esetén – a főútvonalon kerékpározás esetét kivéve – a kerékpárosra nem kell alkalmazni az (1) bekezdés c) pontjában meghatározott korlátozást.” (`K2012-08-24_4-4`)
- *Majdnem, de nem:* „Nem vonatkozik a (14) bekezdésben meghatározott tilalom azon nehéz tehergépkocsira, amely útlezárás miatt terelőúton közlekedik …” (`K2013-07-01_48-16-16`) – ez valóban ENYHITES (új kivétel egy tilalom alól), annak ellenére, hogy ugyanazon a napon lépett hatályba, mint maga a tilalom. Az egységet önmagában kell kódolni, nem a csomag egészét.

### SEMLEGES
- *Definíció:* a változás nem érinti, mit szabad és mit kötelező a közlekedőknek.
- *Akkor, ha:* névváltozás, elírás- vagy központozás-javítás, átszámozás, jogszabályi hivatkozás frissítése, fogalommeghatározás pontosítása szabálytartalom változása nélkül, uniós irányelvre utalás, hatósági vagy szervezeti feladat rögzítése.
- *Példa:* „1. § A rendelet Magyarország területén levő közutakon …” (régi: „a Magyar Köztársaság területén”) (`K2012-01-01_1`)
- *Majdnem, de nem:* egy fogalommeghatározás, amely új járműkört von egy meglévő tilalom alá (pl. `K2013-07-01_1-sz-m-f-ggel-k-i-1`, „Nehéz tehergépkocsi”), csak akkor SEMLEGES, ha a szövegből nem derül ki tilalom vagy kötelezettség. A tilalmat hordozó rendelkezés kapja az irányt.

### VEGYES
- *Definíció:* ugyanaz a változás egyszerre szigorít és enyhít, érdemben.
- *Akkor, ha:* a szövegben egy új vagy szűkülő kötelezettség és egy új vagy bővülő mozgástér is megjelenik, és egyik sem pusztán pontosítás.
- *Példa:* „… a kerékpárosra nem kell alkalmazni az (1) bekezdés c) pontjában a járművezető szervezetében szeszesital fogyasztásából származó alkohol jelenlétére vonatkozó korlátozást.” (`K2014-07-19_4-4`) – a felmentés a főútvonalra is kiterjed (enyhítés), de már csak az alkoholra vonatkozik, a bódító szerekre nem (szigorítás).
- *Majdnem, de nem:* egy szöveg, amely a meglévő szabályt csak átfogalmazza, és mellette egy apró pontosítást tesz: SEMLEGES.

## Döntési szabályok
1. Mindig az egység saját régi és új szövegét kell összevetni, nem a jogszabálycsomag egészét.
2. Ha a változás csak egy szűk csoportot érint (pl. megkülönböztető jelzést használó járművek), az irányt erre a csoportra kell megítélni.
3. Új kivétel vagy felmentés (bármely csoportnak) → ENYHITES. Új tilalom vagy kötelezettség (bármely csoportnak) → SZIGORITAS.
4. Hatályon kívül helyezett tilalom → ENYHITES; hatályon kívül helyezett kivétel → SZIGORITAS; hatályon kívül helyezett technikai szöveg → SEMLEGES.
5. Ha a szöveg egy felsorolás töredéke (pl. „tilos.”), és önmagában nem dönthető el az irány → NEM_BESOROLHATO.
6. Kétség esetén SEMLEGES helyett a NEM_BESOROLHATO-t kell választani, ha a szöveg nem elég; és VEGYES helyett az uralkodó irányt, ha az egyik rész csak pontosítás.

## Kiegészítő mezők (nincs egyezésvizsgálat, csak leíró célra)
- `csoport`: kire vonatkozik elsősorban: `osszes_kozlekedo`, `gepjarmuvezeto`, `nehez_tehergepkocsi`, `autobusz`, `kerekparos`, `gyalogos`, `kulonleges_jarmu` (megkülönböztető vagy figyelmeztető jelzést használó, hatósági), `egyeb`.
- `terulet`: szabályterület: `alkohol_vezetokepesseg`, `sebesseg`, `elozes_haladas`, `megallas_varakozas`, `jarmu_okmany_felszereles`, `gyermekbiztonsag`, `kulonleges_jarmu`, `jelzes_tabla`, `egyeb`.

## Kézi kódolási terv
Egységek: 25 · kódoló: a projekt szerzője · a gépi címkéket nem látva (vakon) · minta: véletlen, mag (seed) = 1, a `scripts/08_iranykod_elokeszites.py` húzza. Az egyezést a `scripts/09_iranykod_osszesites.py` számolja (pontos egyezés, Cohen-féle kappa, kategóriánként). Ha a kódkönyv változik, új verzió és új minta kell.

## A szabályozási szint-skála (B) – külön mérés
A vizsgált szabályterületre (alkohol) csoportonként és időszakonként rendezett skála, kézzel kódolva a jogszabályszövegből: 0 = nincs szabályozás · 1 = megengedett, csak a vezetésre képtelen állapot tilos · 2 = részleges zéró tolerancia (bizonyos utakon vagy helyzetekben) · 3 = teljes zéró tolerancia. Tábla: `data/raw/kezi_kodolas/szabalyozasi_szint_alkohol.csv`.
