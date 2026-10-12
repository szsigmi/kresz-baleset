"""Adatösszeggel ellenőrzött Statinfo kategóriahierarchia."""
import re

_HONAP_SZAM = {nev: i for i, nev in enumerate(("január", "február", "március", "április", "május", "június",
                "július", "augusztus", "szeptember", "október", "november", "december"), 1)}
HONAPOK = set(_HONAP_SZAM)
VIZSGALT_HONAPOK = [(ev, ho) for ev in range(2011, 2026) for ho in range(1, 13)]

# Az oszlopszámok az export munkalapján értendők. A szülő–gyerek feltevést a
# havi értékek összege fogadja el; a 2. oszlop a Mindösszesen, nem kategóriaszülő.
OK_EGYENLETEK = [
    (2, [3, 18, 21, 26, 33, 36]),
    (3, [4, 8, 10, 12, 14]),
    (4, [5, 6, 7]),
    (14, [15, 16, 17]),
    (21, [22]),
    (22, [23, 24, 25]),
    (26, [28, 29, 30, 31, 32]),
]
TERMESZET_EGYENLET = (2, list(range(3, 16)))


def fejlec_sor(ws):
    return next(r for r in range(6, min(ws.max_row, 12) + 1)
                if str(ws.cell(r, 1).value or "").strip().lower() == "időszak")


def honapkulcs(ertek):
    m = re.fullmatch(r"(20\d{2})\.\s+([\wáéíóöőúüű]+)",
                     str(ertek or "").strip(), re.I)
    if not m or m.group(2).lower() not in HONAPOK:
        return None
    ev = int(m.group(1))
    return (ev, _HONAP_SZAM[m.group(2).lower()]) if 2011 <= ev <= 2025 else None


def havi_adatok(ws):
    """Hónapkulcs → munkalapsor; éves sorokat és hiányzó hónapokat nem pótol."""
    head = fejlec_sor(ws)
    out = {}
    for r in range(head + 1, ws.max_row + 1):
        key = honapkulcs(ws.cell(r, 1).value)
        if key:
            out[key] = r
    return out


def osszegproba(ws, szulo_oszlop, gyerek_oszlopok, honapok=None):
    """Csak a numerikus forrásértékeket összegzi; a hiányzó cellák üresek maradnak."""
    honapok = VIZSGALT_HONAPOK if honapok is None else honapok
    rows = havi_adatok(ws)
    nem_osszevetheto = []
    hianyzo_gyerek = 0
    maradekok = []
    for key in honapok:
        r = rows.get(key)
        parent = ws.cell(r, szulo_oszlop).value if r else None
        if not isinstance(parent, (int, float)):
            nem_osszevetheto.append(key)
            continue
        values = [ws.cell(r, c).value for c in gyerek_oszlopok]
        hianyzo_gyerek += sum(not isinstance(v, (int, float)) for v in values)
        osszeg = sum(v for v in values if isinstance(v, (int, float)))
        if parent != osszeg:
            maradekok.append((key, parent, osszeg, parent - osszeg))
    return {"vizsgalt": len(honapok), "osszevetheto": len(honapok) - len(nem_osszevetheto),
            "nem_osszevetheto": nem_osszevetheto, "hianyzo_gyerek": hianyzo_gyerek,
            "maradekok": maradekok,
            "elfogadva": not nem_osszevetheto and not maradekok}


def elfogadott_szulok(ws, dimenzio):
    """Csak a mind a 180 hónapban igazolt kategóriaélek szülőit adja vissza."""
    if dimenzio != "Baleset oka":
        return {}
    parents = {}
    for parent, children in OK_EGYENLETEK:
        result = osszegproba(ws, parent, children)
        if result["elfogadva"] and parent != 2:
            parent_name = str(ws.cell(fejlec_sor(ws), parent).value or "").strip()
            for child in children:
                parents[child] = parent_name
    return parents
