"""Jedna karta 71: 1200 kolejnych pomiarów oraz parametry i obliczenia."""
from pathlib import Path
import re
HERE=Path(__file__).resolve().parent
base=(HERE/'uklad_karty.tex').read_text(encoding='utf-8')
prefix,rest=base.split(r'\titlepagepart{Podwójna szczelina -- karta 1 z 20}',1)
card=rest.split(r'\titlepagepart{Podwójna szczelina -- karta 2 z 20}',1)[0]
tail=base.split(r'\titlepagepart{23 Podwójna szczelina -- obliczenia}',1)[1]
prefix=prefix.replace(r'\thepage\ / 25',r'\thepage\ / 65')
prefix=prefix.replace('Długość fali podana w instrukcji: $\\lambda=650\\,\\mathrm{nm}$. Potwierdź parametry aktualnego stanowiska.',
                      'Długość fali i pozostałe parametry potwierdź na aktualnym stanowisku.')
# 0,1 mm jest krokiem, nie wartością tła: usuwamy wcześniejsze przypadkowe wypełnienie.
card=re.sub(r'(\\textbf\{Tło, opcjonalnie\}.*?\\rule\{0pt\}\{7mm\} &  &  & )\$0\{,\}1\$',
            lambda match:match.group(1),card,flags=re.S)
pages=[]
indices=[]
for k in range(60):
    iterator=iter(range(k*20+1,k*20+21))
    def row(match):
        number=next(iterator);indices.append(number)
        return match.group(1)+str(number)+match.group(2)
    page=re.sub(r'(\\rule\{0pt\}\{7mm\})\d+( &)',row,card)
    page=re.sub(r'Pomiary 1--20(?: z 400)?\.',f'Pomiary {k*20+1}--{k*20+20} z 1200.',page)
    pages.append(r'\titlepagepart{Dwie szczeliny -- karta '+str(k+1)+' z 60}\n'.replace('\\n','\n')+page)
assert indices==list(range(1,1201))
tail=tail.replace(r'\titlepagepart{24 Niepewności i końcowe wyniki}',r'\titlepagepart{64 Niepewności i końcowe wyniki}')
tail=tail.replace(r'\titlepagepart{25 Notatki do sprawozdania}',r'\titlepagepart{65 Notatki do sprawozdania}')
result=prefix+''.join(pages)+r'\titlepagepart{63 Dwie szczeliny -- obliczenia}'+tail
(HERE/'71_karta_pomiarowa_1_1200.tex').write_text(result,encoding='utf-8')
print('Połączono karty: 1200 pomiarów, numery bez powtórzeń, 65 stron.')
