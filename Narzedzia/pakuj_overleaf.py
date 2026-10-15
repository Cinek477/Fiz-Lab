"""Odtwarzanie publicznych paczek Overleaf; Python 3.11+, bez bibliotek zewnętrznych."""
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent.parent


def packages(root=ROOT):
    """Zwróć (ścieżka ZIP, {nazwa w archiwum: zawartość}) dla pustych szablonów."""
    for number in ('11', '83'):
        folder = root / number if number == '11' else next(root.glob('83*'))
        names = ([f'{number}_karta_pomiarowa.tex', f'{number}_szablon_sprawozdania.tex', 'styl.tex']
                 + (['wspolne.tex', 'tabela_pusta.tex', 'Rysunki/przyrzad.pdf'] if number == '11'
                    else ['identyfikacja.tex', 'odchylenia_szablon.tex', 'odczyty.tex', 'wyniki_rzedy.tex']))
        files = {}
        for name in names:
            source = folder / 'Tworzenie' / name
            files[name] = (source.read_text(encoding='utf-8-sig').encode('utf-8')
                           if source.suffix == '.tex' else source.read_bytes())
        yield folder / f'{number}_overleaf.zip', files
    for folder in sorted((root / '31').glob('[123]. *')):
        key = folder.name[0]
        letter = {'1': 'A', '2': 'B', '3': 'C'}[key]
        files = {}
        for name in [f'31_{letter}_karta.tex', f'31_{letter}_szablon.tex']:
            p = folder / 'Tworzenie' / name
            files[p.name] = p.read_text(encoding='utf-8-sig').replace('../../Wspolne/', '').encode('utf-8')
        for p in sorted((root / '31' / 'Wspolne').rglob('*')):
            if p.is_file() and p.suffix in ('.tex', '.pdf'):
                name = p.relative_to(root / '31' / 'Wspolne').as_posix()
                files[name] = (p.read_text(encoding='utf-8-sig').replace('../../Wspolne/', '').encode('utf-8')
                               if p.suffix == '.tex' else p.read_bytes())
        yield folder / f'31_{letter}_overleaf.zip', files
    files = {}
    for rel in ('Templatka/Tworzenie/71_karta_pomiarowa_1_1200.tex',
                'Sprawko/Tworzenie/71_szablon_sprawozdania.tex'):
        p = root / '71' / rel
        files[p.name] = p.read_text(encoding='utf-8-sig').encode('utf-8')
    yield root / '71' / '71_overleaf.zip', files


def main():
    for path, files in packages():
        # Stały czas wpisów i kolejność: ten sam zestaw źródeł daje ten sam ZIP.
        with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
            for name, data in sorted(files.items()):
                entry = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
                entry.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(entry, data)
        print(f'OK: {path.relative_to(ROOT)} ({len(files)} files)')


if __name__ == '__main__':
    main()
