"""Odtworzenie pustych tabel ćwiczenia 83; Python bez dodatkowych bibliotek."""
from pathlib import Path
HERE = Path(__file__).resolve().parent
def save(name, text):
    (HERE / name).write_text(text, encoding='utf-8')
rows = []
for line in range(1,9):
    for repeat in range(1,4):
        marker = r'\multirow{3}{*}{\textbf{'+str(line)+'}}' if repeat==1 else ''
        border = r'\hline' if repeat==3 else r'\cline{3-7}'
        rows.append(f'{marker} & & {repeat} & & & & '+r'\rule{0pt}{7mm}\\'+border)
save('odczyty.tex', '\n'.join(rows)+'\n')
for name, cols in [('wyniki_rzedy.tex', 7), ('identyfikacja.tex', 6)]:
    save(name, '\n'.join(str(i)+' & '*(cols-1)+r'\rule{0pt}{9mm}\\\hline' for i in range(1,9))+'\n')
save('odchylenia_szablon.tex', '\n'.join(
    f'{i} & {n} & & & '+r'\rule{0pt}{6mm}\\\hline'
    for n in [1,2] for i in range(1,9))+'\n')
print('Utworzono tabele: 8 linii, po 3 powtórzenia w I i II rzędzie.')
