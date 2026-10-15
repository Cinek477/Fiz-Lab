"""Puste tabele do ćwiczenia 11: po 21 obciążeń dla dwóch drutów."""
from pathlib import Path
ROOT=Path(__file__).resolve().parent
(ROOT/'tabela_pusta.tex').write_text('\n'.join(
    str(i)+' & & & & & '+r'\rule{0pt}{7mm}\\\hline' for i in range(1,22))+'\n',encoding='utf-8')
print('Przygotowano 21 wierszy na każdy drut.')
