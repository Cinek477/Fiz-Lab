"""Utwórz oddzielne karty i szablony wariantów A, B i C ćwiczenia 31."""
from pathlib import Path
import zipfile
ROOT=Path(__file__).resolve().parent.parent
VARIANTS=[('A','1. Kondensator płaski','Kondensator płaski'),
          ('B','2. Kondensator cylindryczny','Kondensator cylindryczny'),
          ('C','3. Dowolne elektrody','Dowolny układ elektrod')]
def box(height,title):return '\\miejsce{'+str(height)+'mm}{'+title+'}\n'
def table(headers,n,height=7):
    cols='|c|'+'Y|'*(len(headers)-1)
    rows=[r'\par\medskip\begingroup\small\noindent\begin{tabularx}{\linewidth}{'+cols+r'}\hline',r'\naglowek '+' & '.join(headers)+r'\\\hline']
    rows += [str(i)+' & '*(len(headers)-1)+r'\rule{0pt}{'+str(height)+r'mm}\\\hline' for i in range(1,n+1)]
    return '\n'.join(rows)+r'\end{tabularx}\endgroup\par\medskip'+'\n'
def start(kind):
    return r'\documentclass[11pt,a4paper]{article}'+'\n'+r'\newcommand{\Rodzaj}{'+kind+'}\n'+r'\input{../../Wspolne/styl.tex}'+'\n'+r'\input{../../Wspolne/tresc.tex}'+'\n'+r'\begin{document}\metryka'+'\n'
profile_head=['Nr',r'$x$ lub $r$ [mm]',r'$V_a$ [V]',r'$V_b$ [V]',r'$V_c$ [V]']
map_head=['Nr',r'$x$ [mm]',r'$y$ [mm]',r'$V$ [V]','Uwagi']
calc_head=['Nr',r'$x^*$ lub $r^*$ [mm]',r'$E_{s,\mathrm{dosw}}$ [V/m]',r'$E_{s,\mathrm{teor}}$ [V/m]']
for key,folder,title in VARIANTS:
    path=ROOT/folder
    (path/'Tworzenie').mkdir(parents=True,exist_ok=True);(path/'PDF').mkdir(exist_ok=True)
    card=start('Karta pomiarowa — '+key)+r'\section*{Wariant '+key+' — '+title+'}\n'+r'\parametry{'+key+'}\n'
    card+=r'\aparatura'+'\n'+box(25,'Ustalenia prowadzącego, geometria, jednostki współrzędnych, stan papieru i kontakt sondy.')
    if key in ['A','B']:
        card+=r'\clearpage\section*{Profile potencjału — trzy kierunki}'+'\n'
        card+=('Oś $x$ licz od elektrody odniesienia; zapisz kierunek wzrostu $x$.\n' if key=='A' else
               'Promień $r$ licz od środka, nie od brzegu elektrody. Zapisz kąty promieni lub ich położenie na szkicu.\n')
        card+=table(profile_head,20,7)+box(20,'Zero i napięcia elektrod po serii, powtarzalność oraz uwagi do odczytów.')
    if key in ['A','C']:
        count=50 if key=='A' else 100
        for k in range(count//25):
            card+=r'\clearpage\section*{Mapa 2D — pomiary '+str(k*25+1)+'--'+str(k*25+25)+'}\n'
            card+='Zapisuj rzeczywiste współrzędne i potencjał. Brak pomiaru nie oznacza 0 V.\n'
            part=table(map_head,25,7)
            # Numery globalne zamiast powtarzania 1–25.
            for i in range(25,0,-1):part=part.replace('\n'+str(i)+' &','\n'+str(k*25+i)+' &')
            card+=part
    card+=r'\clearpage\section*{Szkic geometrii i współrzędnych}'+'\n'
    card+='Narysuj elektrody, osie, biegunowość, początek skali i kierunki pomiarów. Wartości napięcia zapisuj obok punktów.\n'
    card+=r'\begin{center}\includegraphics[width=\linewidth,height=190mm,keepaspectratio]{../../Wspolne/Rysunki/siatka.pdf}\end{center}'+'\n'
    card+=r'\small Siatka jest miejscem na szkic. Współrzędne i rozstaw otworów odczytaj ze stanowiska, nie mierz ich na wydruku.'+'\n'+r'\end{document}'
    (path/'Tworzenie'/f'31_{key}_karta.tex').write_text(card,encoding='utf-8')
    report=start('Szablon sprawozdania — '+key)
    report+=r'\section{Cel ćwiczenia}'+'\n'+f'Wyznaczenie potencjału, linii ekwipotencjalnych i wektorów pola dla układu: {title.lower()}.\n'
    report+=r'\section{Podstawy teoretyczne}\podstawy'+'\n'+(r'\teoriaA' if key=='A' else r'\teoriaB' if key=='B' else r'\teoriaC')+'\n'
    report+=r'\clearpage\section{Aparatura i przebieg}\aparatura\parametry{'+key+'}\n'+box(30,'Opisz rzeczywiste połączenia, pomiar odniesienia, geometrię i wybór punktów; nie kopiuj przebiegu cudzej serii.')
    report+=r'\clearpage\section{Wyniki pomiarów}'+'\n'
    if key=='C':
        report+='Zestaw rzeczywiste współrzędne i napięcia z badanej płyty. '
        report+='Pełną listę około 100 punktów zachowaj jako załącznik lub tabelę CSV; '
        report+='poniżej wpisz zestaw podstawowy i rozszerz go w razie potrzeby.\n'
        report+=table(map_head,20,7)
    if key in ['A','B']:
        report+=table(profile_head,15,7)+box(25,'Średnie potencjały i wartości teoretyczne dla każdej współrzędnej. Przy większej liczbie pomiarów rozszerz tabelę.')
        report+=r'\clearpage\section{Potencjał i natężenie}\roznice'+'\n'
        report+=table(calc_head,8,7)+box(46,'Wykres potencjału: dane trzech kierunków, ich średnia i linia teoretyczna; osie z jednostkami.')
        report+=box(46,'Wykres natężenia: punkty w połowach przedziałów, właściwy znak składowej i porównanie z teorią.')
    report+=r'\clearpage\section{Linie ekwipotencjalne i wektory pola}'+'\n'+r'\mapowanie'+'\n'
    report+=box(95,'Mapa: punkty pomiarowe, elektrody i osie, linie ekwipotencjalne co 1–2 V, linie pola z kierunkiem. Rozróżnij interpolację pomiarów od mapy teoretycznej.')
    report+=table(['Nr',r'$x,y$ [mm]',r'$E_x$ [V/m]',r'$E_y$ [V/m]',r'$|\mathbf E|$ [V/m]'],5,8)
    report+=r'\clearpage\section{Dokładność i dyskusja}\dokladnosc'+'\n'+box(35,'Podaj rozbieżności danych i modelu: wartości, obszary, możliwe przyczyny i ograniczenia. Nie stwierdzaj zgodności tylko na podstawie podobnego kształtu wykresu.')
    report+=r'\section{Wnioski}'+'\n'+table(['Nr','Wynik i interpretacja'],4,16)+r'\end{document}'
    (path/'Tworzenie'/f'31_{key}_szablon.tex').write_text(report,encoding='utf-8')
    with zipfile.ZipFile(path/f'31_{key}_overleaf.zip','w',zipfile.ZIP_DEFLATED) as archive:
        for name in [f'31_{key}_karta.tex',f'31_{key}_szablon.tex']:
            source=(path/'Tworzenie'/name).read_text(encoding='utf-8').replace('../../Wspolne/','')
            archive.writestr(name,source)
        for common in (ROOT/'Wspolne').rglob('*'):
            if common.is_file():
                relative=common.relative_to(ROOT/'Wspolne')
                if common.suffix=='.tex':
                    archive.writestr(str(relative),common.read_text(encoding='utf-8-sig').replace('../../Wspolne/',''))
                else:archive.write(common,relative)
print('Utworzono osobne warianty A, B i C, każdy z kartą, szablonem i ZIP-em.')
