#!/usr/bin/env python3
"""KRESZ-időállapotok rendelkezésenkénti összevetése (kis mintán is futtatható)."""
import csv
import re
from functools import lru_cache
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data/raw'
OUT = ROOT / 'data/processed/kresz_valtozasok.csv'
PROBE_OUT = ROOT / 'data/processed/kresz_valtozasok_proba.csv'
FIELDS = ['verzio_elotte', 'verzio_utana', 'hatalybalepes', 'rendelkezes',
          'valtozas_tipusa', 'regi_szoveg', 'uj_szoveg',
          'modosito_jogszabaly', 'modosito_rendelkezes', 'forras_url']
BASE = 'https://njt.jog.gov.hu/jogszabaly/1975-1-20-24'


def text_without_footnote_sup(el):
    clone = BeautifulSoup(str(el), 'html.parser')
    for sup in clone.select('sup'):
        sup.decompose()
    text = re.sub(r'\s+', ' ', clone.get_text(' ', strip=True)).strip()
    # A külön linkbe tett ragok előtt a HTML-ből jövő szóközt eltávolítjuk.
    text = re.sub(r'\b(bekezdés|pont|alpont)\s+(ben|ban|nek|nak|hez|hoz|höz|tól|től|ra|re|ba|be|val|vel|ja|je|ját|jét|jában|jében|jának|jének|jával|jével)\b', r'\1\2', text)
    return text


def decode_label(jhid):
    m = re.match(r'SZ(\d+)(.*)', jhid)
    if not m:
        return jhid
    parts = [f'{m.group(1)}. §']
    rest = m.group(2)
    be = re.search(r'@BE(\d+)', rest)
    if be and be.group(1) != '0':
        parts.append(f"({int(be.group(1))})")
    po = re.search(r'@PO([A-Z])', rest)
    if po:
        parts.append(f'{chr(96 + ord(po.group(1)) - 64)})')
    ap = re.search(r'@AP([A-Z]{2})', rest)
    if ap:
        parts.append(f'{ap.group(1).lower()})')
    return ' '.join(parts)


def visible_label(jhid, element, paragraph):
    section = re.match(r'SZ(\d+)', jhid).group(1)
    marker = paragraph.select_one('.jel')
    marker_text = text_without_footnote_sup(marker) if marker else ''
    classes = element.get('class', [])
    if 'bekezdesNyito' in classes:
        m = re.search(r'\((\d+[a-z]?)\)', marker_text)
        return f'{section}. § ({m.group(1)})' if m else f'{section}. §'
    fallback = decode_label(jhid)
    if 'betusPontNyito' in classes or 'ketbetusAlPont' in classes:
        m = re.match(r'\s*([a-z]{1,2}|\d+[.)])', marker_text, re.I)
        if m:
            suffix = m.group(1)
            prefix = fallback.rsplit(' ', 1)[0] if ' ' in fallback else f'{section}. §'
            return f'{prefix} {suffix}'
    return fallback


def equivalent_text(key, left, right):
    # Listaelem záró pont/vessző eltérése önmagában nem érdemi normaszöveg-változás.
    if '@PO' in key or '@AP' in key:
        clean = lambda value: re.sub(r'[.,;:]\s*$', '', value.strip())
        return clean(left) == clean(right)
    return left == right


def law_from_note(note):
    pattern = (r'((?:\d{1,4}/)?\d{1,4}/\d{4}\.\s*\([^)]*\)\s*'
               r'(?:Korm\.\s*rendelet|KM[–-]?BM(?: együttes)? rendelet))')
    matches = list(re.finditer(pattern, note))
    return matches[-1].group(1).strip() if matches else ''


@lru_cache(maxsize=None)
def read_state(version):
    path = RAW / f'kresz_1975-1-20-24_{version}.html'
    if not path.exists():
        raise FileNotFoundError(f'Hiányzó forrásállapot: {path}')
    soup = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
    effective = soup.select_one('.hataly').get_text(' ', strip=True).rstrip('.').replace('.', '-')
    notes = {x.get('id'): x.get_text(' ', strip=True) for x in soup.select('.footnote[id]')}
    items = {}
    for el in soup.select('div.bekezdesNyito, div.betusPontNyito, div.ketbetusAlPont'):
        marker = el.find_previous_sibling('span', class_='jhId')
        if not marker or not re.match(r'SZ\d+@BE', marker.get('id', '')):
            continue
        key = marker['id']
        p = el.find('p') or el
        note_ids = [s.get('data-note-id') for s in p.select('sup[data-note-id]')]
        note = ' | '.join(notes.get(n, '') for n in note_ids if n in notes)
        images = tuple((img.get('src', ''), img.get('alt', '')) for img in el.select('img'))
        items[key] = {'label': visible_label(key, el, p), 'text': text_without_footnote_sup(p),
                      'note': note, 'images': images}
    # Az alkategóriák lábjegyzetét gyakran a teljes szülőbekezdés hordozza.
    for key, item in items.items():
        if item['note']:
            continue
        parts = key.split('@')
        while len(parts) > 2:
            parts.pop()
            parent = items.get('@'.join(parts))
            if parent and parent['note']:
                item['note'] = parent['note']
                break
    return effective, items


def main():
    # A feldolgozott állapotlista ugyanabból a változatlan nyers válaszból készül.
    import json
    state_data = json.loads((RAW / 'kresz_idoallapotok.json').read_text(encoding='utf-8'))['data']
    state_rows = []
    for item in state_data:
        start = item['comingIntoForce'][:10]
        end = item['expiresOn'][:10] if item['expiresOn'] else ''
        state_rows.append({'verzio': item['version'], 'hataly_kezdete': start,
                           'hataly_vege': end, 'url': f'{BASE}.{item["version"]}',
                           'vizsgalati_idoszakon_kivul': 'igen' if start > '2025-12-31' else ''})
    with (ROOT / 'data/processed/kresz_idoallapotok.csv').open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['verzio', 'hataly_kezdete', 'hataly_vege', 'url', 'vizsgalati_idoszakon_kivul'])
        w.writeheader(); w.writerows(state_rows)
    comparable = sum('2010-01-02' <= r['hataly_kezdete'] <= '2025-12-31' for r in state_rows)
    print(f'Összevethető állapotváltások (2010-01-02–2025-12-31): {comparable}')
    def compare(before, after):
        date, new = read_state(after)
        _, old = read_state(before)
        rows = []
        consumed_old, consumed_new = set(), set()
        # Ha egy korábbi teljes § új bekezdésekre bomlik, ez szövegcserés módosítás,
        # nem a régi KRESZ-§ hatályon kívül helyezése.
        for key, a in old.items():
            if not key.endswith('@BE0') or key in new:
                continue
            section = key.split('@', 1)[0]
            children = [k for k in new if k.startswith(section + '@BE') and k not in old]
            if not children:
                continue
            consumed_old.add(key); consumed_new.update(children)
            note = ' | '.join(new[k]['note'] for k in children if new[k]['note'])
            law = law_from_note(note)
            rows.append({'verzio_elotte': before, 'verzio_utana': after,
                         'hatalybalepes': date, 'rendelkezes': a['label'],
                         'valtozas_tipusa': 'módosított', 'regi_szoveg': a['text'],
                         'uj_szoveg': '\n'.join(new[k]['label'] + ': ' + new[k]['text'] for k in children),
                         'modosito_jogszabaly': law,
                         'modosito_rendelkezes': note,
                         'forras_url': f'{BASE}.{before} -> {BASE}.{after}'})
        keys = (set(old) | set(new)) - consumed_old - consumed_new
        for key in sorted(keys, key=lambda k: [int(x) if x.isdigit() else x for x in re.split(r'(\d+)', k)]):
            a, b = old.get(key), new.get(key)
            if a and b and equivalent_text(key, a['text'], b['text']) and a['images'] == b['images']:
                continue
            kind = 'új' if a is None else 'hatályon kívül helyezett' if b is None else 'módosított'
            old_text = a['text'] if a else ''
            new_text = b['text'] if b else ''
            if a and b and a['images'] != b['images']:
                old_text += f" [Ábrák előtte: {len(a['images'])}]"
                new_text += f" [Ábrák utána: {len(b['images'])}]"
            note = b['note'] if b else ''
            law = law_from_note(note)
            rows.append({'verzio_elotte': before, 'verzio_utana': after,
                         'hatalybalepes': date, 'rendelkezes': (b or a)['label'],
                         'valtozas_tipusa': kind, 'regi_szoveg': old_text,
                         'uj_szoveg': new_text, 'modosito_jogszabaly': law,
                         'modosito_rendelkezes': note,
                         'forras_url': f'{BASE}.{before} -> {BASE}.{after}'})
        return rows

    all_rows = []
    for after in range(17, 40):
        rows = compare(after - 1, after)
        all_rows.extend(rows)
        print(f'{after-1}->{after}: {len(rows)} rendelkezés')
    with OUT.open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=FIELDS); w.writeheader(); w.writerows(all_rows)
    probe = compare(16, 17)
    with PROBE_OUT.open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=FIELDS); w.writeheader(); w.writerows(probe)
    print(f'Összes változott rendelkezés: {len(all_rows)}')


if __name__ == '__main__':
    main()
