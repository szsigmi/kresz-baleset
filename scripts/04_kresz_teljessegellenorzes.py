#!/usr/bin/env python3
"""A rendelkezés-összevetés teljességi próbái."""
import csv
import re
from pathlib import Path
from bs4 import BeautifulSoup
from lxml import html
from difflib import SequenceMatcher

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data/raw'
CSV = ROOT / 'data/processed/kresz_valtozasok.csv'


def norm(text):
    text = re.sub(r'\[Ábrák (?:előtte|utána): \d+\]', '', text)
    return ''.join(re.findall(r'\w+', text.lower(), flags=re.UNICODE))


def doc_blocks(version):
    root = html.fromstring((RAW / f'kresz_1975-1-20-24_{version}.html').read_text(encoding='utf-8'))
    main = root.get_element_by_id('orig')
    selector = (".//div[contains(concat(' ',normalize-space(@class),' '),' bekezdesNyito ') or "
                "contains(concat(' ',normalize-space(@class),' '),' betusPontNyito ') or "
                "contains(concat(' ',normalize-space(@class),' '),' ketbetusAlPont ') or "
                "contains(concat(' ',normalize-space(@class),' '),' szelet ') or "
                "contains(concat(' ',normalize-space(@class),' '),' tagoloCim ') or "
                "contains(concat(' ',normalize-space(@class),' '),' reszcim ') or "
                "contains(concat(' ',normalize-space(@class),' '),' fejezetCim ') or "
                "contains(concat(' ',normalize-space(@class),' '),' mellekletCimke ')]")
    blocks = []
    for node in main.xpath(selector):
        paragraphs = node.xpath('.//p[not(ancestor::p)]')
        fragments = paragraphs or [node]
        for fragment in fragments:
            parts = fragment.xpath('.//text()[not(ancestor::sup) and not(ancestor::*[contains(concat(" ",normalize-space(@class)," ")," fnSup ")]) and not(ancestor::*[contains(concat(" ",normalize-space(@class)," ")," footnote ")])]')
            value = norm(' '.join(parts))
            if value:
                blocks.append(value)
    return blocks


def main():
    with CSV.open(encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    print('CSV-sorok:', len(rows))
    print('Függelék kulcsú sorok:', sum('függelék' in r['rendelkezes'].lower() for r in rows))
    for after in range(17, 40):
        old, new = doc_blocks(after-1), doc_blocks(after)
        deltas = []
        candidates = [r for r in rows if r['verzio_elotte'] == str(after-1) and r['verzio_utana'] == str(after)]
        matcher = SequenceMatcher(a=old, b=new, autojunk=False)
        old_cover = norm(' '.join(r['regi_szoveg'] for r in candidates))
        new_cover = norm(' '.join(r['uj_szoveg'] for r in candidates))
        changed_chunks = 0
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                continue
            changed_chunks += 1
            before, after_text = ' '.join(old[i1:i2]), ' '.join(new[j1:j2])
            # A módosított szövegdarab akkor fedett, ha szerepel a változássorok
            # megfelelő oldalán; rövid, legfeljebb 2 tokenes diff nem informatív.
            bad_old = len(old[i1:i2]) > 1 and norm(before) not in old_cover
            bad_new = len(new[j1:j2]) > 1 and norm(after_text) not in new_cover
            if bad_old or bad_new:
                deltas.append((before[:400] if bad_old else '', after_text[:400] if bad_new else ''))
        if deltas:
            print(f'\n{after-1}->{after}: {len(deltas)} le nem fedett dokumentum-diff')
            for a, b in deltas:
                print(' ELŐTTE:', a)
                print(' UTÁNA: ', b)
        else:
            print(f'{after-1}->{after}: {changed_chunks} eltérő szövegrész, mindet lefedi CSV-sor')

    soup = BeautifulSoup((RAW / 'kresz_1975-1-20-24_39.html').read_text(encoding='utf-8'), 'lxml')
    current = []
    for note in soup.select('#orig .footnote[id]'):
        text = note.get_text(' ', strip=True)
        years = [int(y) for y in re.findall(r'\d+/(20(?:1\d|2[0-5]))\.', text)]
        if any(2010 <= y <= 2025 for y in years):
            current.append((note.get('id'), text))
    print('\nLábjegyzetek 2010–2025 kihirdetett módosítóval:', len(current))
    missing = []
    for note_id, text in current:
        # A célrendelkezés rövid azonosítóját a lábjegyzet KRESZ-helyéből
        # képezzük, majd a CSV rendelkezéscímkéiben és szövegében keressük.
        law_pos = re.search(r'\d+/(?:19|20)\d{2}\.\s*\(', text)
        target = text[:law_pos.start()] if law_pos else text
        section = re.search(r'(\d+(?:/[A-Z]|[A-Z])?\.\s*§)', target, flags=re.I)
        if section:
            sections = list(re.finditer(r'\d+(?:/[A-Z]|[A-Z])?\.\s*§', target, flags=re.I))
            section = sections[0]
            tail = target[section.end():]
            markers = re.findall(r'\(\d+[a-z]?\)|\b[a-z]{1,2}(?:/\d+)?(?=[).]?\s+(?:pont|alpont))', tail, flags=re.I)
            wanted = [norm(x) for x in markers]
            found = False
            for row in rows:
                label = row['rendelkezes']
                row_section = re.search(r'\d+(?:/[A-Z]|[A-Z])?\.\s*§', label, flags=re.I)
                row_markers = [norm(x) for x in re.findall(r'\(\d+[a-z]?\)|\b[a-z]{1,2}(?:/\d+)?[).]?', label, flags=re.I)]
                if row_section and norm(row_section.group()) == norm(section.group()) and (not wanted or any(m in row_markers for m in wanted)):
                    found = True
                    break
        else:
            # A függeléki tétel az elem szövegében szerepel, mert az NJT nem
            # ad hozzá §-azonosítót.
            marker_tokens = re.findall(r'\b[a-z]{1,2}(?:/\d+)?[).]', target, flags=re.I)
            wanted = norm(marker_tokens[-1]) if marker_tokens else ''
            found = any((wanted and wanted in norm(r['uj_szoveg'] + r['regi_szoveg'])) for r in rows if 'függelék' in r['rendelkezes'].lower())
        if not found:
            missing.append((note_id, text))
    print('CSV-ből hiányzó lábjegyzetek:', len(missing))
    for entry in missing:
        print(' ', *entry)


if __name__ == '__main__':
    main()
