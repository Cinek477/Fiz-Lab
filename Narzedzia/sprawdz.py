"""Kontrola plików i publicznych paczek. Nie zmienia źródeł ani indeksu Git."""
import argparse
import ast
import csv
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from urllib.parse import unquote
import zipfile
from xml.etree import ElementTree as ET
from pakuj_overleaf import ROOT, packages

SKIP = {'.git', '__pycache__', '.venv', 'tmp', 'temp', 'Archiwum'}
OWN_REPORTS = (
    '0/wahadlo/PDF/sprawozdanie.pdf',
    '71/PDF/INF3z1c71v1.pdf',
)


def files():
    return sorted(p for p in ROOT.rglob('*') if p.is_file()
                  and not SKIP.intersection(p.relative_to(ROOT).parts))


def ignored_paths(paths):
    """Test prawdziwym Gitem, w oddzielnym repozytorium bez plików użytkownika."""
    if not paths:
        return set()
    with tempfile.TemporaryDirectory(prefix='fiza-ignore-') as name:
        shadow = Path(name)
        subprocess.run(['git', 'init', '-q', name], check=True, capture_output=True)
        for p in ROOT.rglob('.gitignore'):
            rel = p.relative_to(ROOT)
            if SKIP.intersection(rel.parts):
                continue
            target = shadow / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(p, target)
        rels = [p.relative_to(ROOT).as_posix() for p in paths]
        result = subprocess.run(['git', '-C', name, 'check-ignore', '--no-index', '-z', '--stdin'],
                                input='\0'.join(rels).encode('utf-8') + b'\0', capture_output=True)
        if result.returncode not in (0, 1):
            raise RuntimeError(result.stderr.decode('utf-8', errors='replace'))
        return set(result.stdout.decode('utf-8').strip('\0').split('\0')) - {''}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--compile', metavar='TECTONIC', help='Dodatkowo skompiluj wszystkie dokumenty z ZIP-ów.')
    args = parser.parse_args()
    errors = []
    all_files = files()
    counts = {'readme': 0, 'python': 0, 'json': 0, 'csv': 0, 'xlsx': 0, 'zip': 0, 'compiled': 0}
    ignored = ignored_paths(all_files)
    public_links = []
    for p in all_files:
        rel = p.relative_to(ROOT).as_posix()
        try:
            if p.name == 'README.md':
                counts['readme'] += 1
                for a, b in re.findall(r'\]\((?:<([^>]+)>|([^\s)]+))\)', p.read_text(encoding='utf-8-sig')):
                    value = unquote(a or b).split('#')[0]
                    if not value or re.match(r'^[a-zA-Z]+:', value):
                        continue
                    target = (p.parent / value).resolve()
                    if not target.exists():
                        errors.append(f'{rel}: missing link {value}')
                    elif rel not in ignored:
                        public_links.append((rel, target))
            elif p.suffix == '.py':
                ast.parse(p.read_text(encoding='utf-8-sig'), filename=str(p))
                counts['python'] += 1
            elif p.suffix == '.json':
                json.loads(p.read_text(encoding='utf-8-sig'))
                counts['json'] += 1
            elif p.suffix == '.csv':
                with p.open(encoding='utf-8-sig', newline='') as source:
                    rows = list(csv.reader(source))
                if not rows or any(len(row) != len(rows[0]) for row in rows):
                    raise ValueError('CSV has an empty header or inconsistent columns')
                counts['csv'] += 1
            elif p.suffix == '.xlsx' and p.parent == ROOT / 'Excel':
                with zipfile.ZipFile(p) as z:
                    if z.testzip() is not None:raise ValueError('XLSX CRC error')
                    if any('vbaProject' in n for n in z.namelist()):raise ValueError('Unexpected macro in XLSX')
                    ET.fromstring(z.read('xl/workbook.xml'))
                counts['xlsx'] += 1
        except (ValueError, SyntaxError, OSError) as exc:
            errors.append(f'{rel}: {exc}')
        if 'Przykład' in p.parts and rel not in ignored:
            errors.append(f'{rel}: private example is not ignored')
    link_ignored = ignored_paths([p for _, p in public_links]) if public_links else set()
    for origin, target in public_links:
        rel = target.relative_to(ROOT).as_posix()
        if rel in link_ignored:
            errors.append(f'{origin}: public link points to an ignored file: {rel}')
    # Także pliki, które dopiero mogą zostać wygenerowane.
    probes = [ROOT / '71/Sprawko/PDF/71_sprawozdanie_uzupelnione.pdf',
              ROOT / '71/Sprawko/Dane/seria_pelna.csv',
              ROOT / '71/Sprawko/PDF/Wykresy/v2_dopasowanie.pdf',
              ROOT / '71/Dane_zrodlowe/temp1.pdf',
              ROOT / '71/Sprawko/PDF/71_sprawozdanie_v2.pdf', ROOT / '31/Przykład/PDF/test.pdf', ROOT / '71/Templatka/Archiwum/test.pdf',
              ROOT / '71/Sprawko/Tworzenie/wyniki/71_sprawozdanie_do_weryfikacji.docx',
              ROOT / '71/Sprawko/Tworzenie/71_sprawozdanie_do_weryfikacji.tex']
    probes += [ROOT / 'Excel/Wyniki/11/obliczenia.json', ROOT / 'Moje_pomiary/11.xlsx',
               ROOT / 'Excel/11_pomiary.xlsx.inspect.ndjson']
    hidden = ignored_paths(probes)
    for p in probes:
        if p.relative_to(ROOT).as_posix() not in hidden:
            errors.append(f'Unprotected generated/private path: {p.relative_to(ROOT)}')
    # Publikujemy wyłącznie wskazane PDF-y na własnych danych.
    own = [ROOT / name for name in OWN_REPORTS]
    hidden_own = ignored_paths(own)
    for p in own:
        if not p.exists() or p.relative_to(ROOT).as_posix() in hidden_own:
            errors.append(f'Own report missing or ignored: {p.relative_to(ROOT)}')
    protected = [p for p in ROOT.rglob('*') if p.is_file()
                 and {'Przykład', 'Przyklad', 'przyklad', 'Archiwum'}.intersection(p.relative_to(ROOT).parts)]
    hidden_private = ignored_paths(protected)
    for p in protected:
        if p.relative_to(ROOT).as_posix() not in hidden_private:
            errors.append(f'Example/archive is public: {p.relative_to(ROOT)}')
    for path, expected in packages():
        try:
            with zipfile.ZipFile(path) as archive:
                if archive.testzip() is not None:
                    raise ValueError('ZIP CRC error')
                if set(archive.namelist()) != set(expected):
                    raise ValueError('ZIP members differ from current sources')
                for name, data in expected.items():
                    if archive.read(name) != data:
                        raise ValueError(f'stale ZIP entry: {name}')
                counts['zip'] += 1
                if args.compile:
                    with tempfile.TemporaryDirectory(prefix='fiza-overleaf-') as temp:
                        archive.extractall(temp)
                        for name, data in expected.items():
                            if name.endswith('.tex') and b'\\documentclass' in data:
                                result = subprocess.run([args.compile, name], cwd=temp,
                                                        capture_output=True, text=True, encoding='utf-8', errors='replace')
                                if result.returncode:
                                    raise ValueError(f'{name}: compilation failed\n{result.stderr[-2000:]}')
                                counts['compiled'] += 1
            print(f'OK: {path.relative_to(ROOT)}')
        except (OSError, ValueError, zipfile.BadZipFile) as exc:
            errors.append(f'{path.relative_to(ROOT)}: {exc}')
    print('Checked:', ', '.join(f'{k}={v}' for k, v in counts.items()))
    for error in errors:
        print('ERROR:', error)
    if errors:
        raise SystemExit(1)
    print('OK: links, Python, data, Git ignore and ZIPs.')


if __name__ == '__main__':
    main()
