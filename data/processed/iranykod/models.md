# Címkézési futások modellnaplója

## 1. futás – félbemaradt (címke nem készült)
- Kódoló: Codex CLI (OpenAI), a munkamenet rendszeradata szerint GPT-6; pontos revízió, gondolkodási szint és generálási beállítások a futtatókörnyezetből nem voltak ellenőrizhetők
- Dátum: 2026-11-17
- Prompt: `prompt.md` v1 (a Codex írta)
- Eredmény: a prompt és ez a napló elkészült, a 95 fájl számossága és az első 20 tartalma átnézve; a címkézés és a `labels.csv` nem készült el (lásd `docs/valtozasnaplo.md`)

## 2. futás – a `labels.csv` forrása
- Kódoló: Claude (Anthropic) csevegő-asszisztens; a munkamenetben beállított modellazonosító: claude-opus-5-5 (a ténylegesen kiszolgáló modell ettől eltérhet; hőmérséklet és további beállítások nem hozzáférhetők)
- Dátum: 2026-11-17
- Prompt: `prompt.md` v1 változatlanul, a kódkönyv: `docs/iranykod_kodkonyv.md` v1
- Mód: a 95 szövegfájl egyenkénti elolvasása és értelmezése; külső API, kulcsszavas vagy szabályalapú címkézés nem volt
- Ellenőrzés: `label_check.py` (vclassify skill) – 95 fájl · 95 sor · 62 kódolt · 33 félretett · 0 hiba; minden idézett mondat szó szerint szerepel a fájlban
- Vakság: a kézi minta kódjait a címkézés előtt nem láttam
