# Változásnapló

## 2026-10-12 — Projektindítás

- Létrejött a projekt mappastruktúrája, a `.venv` virtuális környezet és a `requirements.txt` függőségi lista.
- Telepítettem és importtal ellenőriztem a pandas, requests, beautifulsoup4, lxml, openpyxl, pdfplumber, matplotlib és statsmodels csomagokat.
- A `cryptography<47` kiegészítő korlát biztosítja, hogy a `pdfplumber` függősége Python 3.14-en előre fordított kerékből települjön.
- Git-repót inicializáltam; a `.gitignore` kizárja a `.venv/` és a `data/raw/cache/` tartalmát.
- Létrehozott fájlok: `.gitignore`, `requirements.txt`, `docs/valtozasnaplo.md`, valamint a mappákat jelölő `.gitkeep` fájlok.
- Bizonytalanság: nincs; adatforrás-letöltés és adatelemzés még nem történt.
