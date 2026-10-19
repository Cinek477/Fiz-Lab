"""Układ kart XLSX i jednostki wejściowe wersji 1.1."""
import json
import sys
from pathlib import Path

META = [
    ('autorzy', 'Imiona i nazwiska', None), ('wydzial', 'Wydział', None),
    ('rok', 'Rok', None), ('grupa', 'Grupa', None), ('zespol', 'Zespół', None),
    ('data_wykonania', 'Data pomiarów (tekst)', None), ('data_oddania', 'Data oddania (tekst)', None),
    ('przebieg', 'Opis rzeczywistego przebiegu', None),
    ('wnioski', 'Wnioski i interpretacja', None),
    ('przyrzady', 'Przyrządy: model, zakres, dokładność', None),
]


def tab(name, title, headers, keys, rows, note, seed=None):
    return dict(name=name, title=title, headers=headers, keys=keys, rows=rows, note=note, seed=seed)


def spec(code, title, params, tables, theory, goal):
    return dict(code=code, title=title, fields=META+params, tables=tables, theory=theory, goal=goal)


SPECS = {}
SPECS['0'] = spec('0', 'Wahadło matematyczne', [
    ('n', 'Liczba okresów w jednym pomiarze', 10), ('L_m', 'Długość własnego wahadła [m]', None),
    ('u_L_m', 'Standardowa u(L) [m]', None), ('u_t_s', 'Standardowa u pojedynczego czasu [s]', None),
], [tab('Czasy', 'Własna seria przy stałej długości', ['Nr', 'Czas n okresów [s]', 'Uwagi'],
        ['nr','t_s','uwagi'],100,'Każdy czas dotyczy n okresów z Ustawień. Nie wpisuj zera za brak pomiaru.'),
    tab('Grupy', 'Druga metoda: okresy innych grup', ['Nr','L [cm]','u(L) [cm]','T [s]','u(T) [s]','Uwagi'],
        ['nr','L_cm','u_L_cm','T_s','u_T_s','uwagi'],100,'Wpisuj okres jednego drgania, nie czas całej serii.')],
    r'T=\frac{t_n}{n},\qquad g=\frac{4\pi^2 L}{T^2},\qquad T^2=A L,\quad g=\frac{4\pi^2}{A}.',
    'Wyznaczenie przyspieszenia ziemskiego z okresu wahadła oraz zależności kwadratu okresu od długości.')

sample_keys=['nr','material','l_m','u_l_m','d1_mm','d2_mm','d3_mm','u_d_mm','z0_up_mm','z0_down_mm']
SPECS['11'] = spec('11', 'Moduł Younga', [('g','Przyjęte g [m/s²]',None)], [
    tab('Probki','Wymiary dwóch drutów', ['Drut','Materiał','l [m]','u(l) [m]','d1 [mm]','d2 [mm]','d3 [mm]','u(d) [mm]','Zero ↑ [mm]','Zero ↓ [mm]'],
        sample_keys,2,'u(d) dotyczy średniej średnicy. Wpisz rzeczywiste zera obu gałęzi; zero też jest pomiarem.',seed=['A','B']),
    *[tab(f'Drut_{s}',f'Drut {s}: obciążanie i odciążanie',
          ['Nr','Masa całkowita [kg]','Odczyt ↑ [mm]','Odczyt ↓ [mm]','Regresja: tak/nie','Uwagi'],
          ['nr','m_kg','z_up_mm','z_down_mm','fit','uwagi'],21,
          'Masa sumaryczna. „nie” wyłącza punkt tylko z regresji; pozostaje on w tabeli i na wykresie.') for s in ['A','B']]],
    r'F=mg,\quad\Delta l=\frac{z_\uparrow-z_{0,\uparrow}+z_\downarrow-z_{0,\downarrow}}4,\\ \Delta l=aF+b,\quad E=\frac{4l}{\pi d^2a}.',
    'Wyznaczenie modułu Younga dwóch drutów metodą statyczną z uwzględnieniem przełożenia dźwigni.')

for variant, title, count in [('A','Kondensator płaski',50),('B','Kondensator cylindryczny',0),('C','Dowolne elektrody',100)]:
    params=[('V0','Potencjał elektrody odniesienia [V]',None),('U','Różnica potencjałów elektrod [V]',None),
            ('d_mm','A: rozstaw elektrod [mm]',None),('rw_mm','B: promień wewnętrzny [mm]',None),
            ('rz_mm','B: promień zewnętrzny [mm]',None),('h_mm','Mapa: krok w osi x [mm]',None),
            ('k_mm','Mapa: krok w osi y [mm]',None),('u_V','Standardowa u(V) [V]',None),
            ('u_s_mm','Standardowa u odstępu Δs [mm]',None),('osie','Początek i zwroty osi; kierunki a/b/c',None)]
    omitted={'A':{'rw_mm','rz_mm'},'B':{'d_mm','h_mm','k_mm'},'C':{'d_mm','rw_mm','rz_mm','u_s_mm'}}[variant]
    params=[f for f in params if f[0] not in omitted]
    tables=[]
    if variant!='C': tables.append(tab('Profile','Trzy profile potencjału',
        ['Nr','x lub r [mm]','Va [V]','Vb [V]','Vc [V]','Uwagi'],['nr','s_mm','Va','Vb','Vc','uwagi'],20,
        'A: x od elektrody odniesienia. B: r od środka; wewnętrzna elektroda ma V0+U, zewnętrzna V0.'))
    if count: tables.append(tab('Mapa','Mapa potencjału', ['Nr','x [mm]','y [mm]','V [V]','Uwagi'],
        ['nr','x_mm','y_mm','V','uwagi'],count,'Rzeczywiste współrzędne i napięcia. Brak odczytu pozostaw pusty.'))
    theories={'A':r'\mathbf E=-\nabla V,\quad V(x)=V_0+\frac{U x}{d},\quad E_x=-\frac Ud.',
              'B':r'V(r)=V_0+\frac{U\ln(r_z/r)}{\ln(r_z/r_w)},\quad E_r=\frac{U}{r\ln(r_z/r_w)}.',
              'C':r'E_x\approx-\frac{V(x+h,y)-V(x,y)}h,\\ E_y\approx-\frac{V(x,y+k)-V(x,y)}k,\quad |\mathbf E|=\sqrt{E_x^2+E_y^2}.'}
    SPECS['31'+variant]=spec('31'+variant,title,params,tables,theories[variant],
        'Wyznaczenie profili potencjału, natężenia i linii ekwipotencjalnych dla wybranego układu elektrod.')

SPECS['71']=spec('71','Dwie szczeliny',[
    ('lambda_nm','Długość fali λ [nm]',None),('u_lambda_nm','Standardowa u(λ) [nm]',None),
    ('L_mm','Odległość szczeliny–detektor L [mm]',None),('u_L_mm','Standardowa u(L) [mm]',None),
    ('p_start_mm','Umowna pozycja pierwszego pomiaru [mm]',0),('krok_mm','Krok pomiarów [mm]',0.1),
    ('u_p_mm','Standardowa u położenia [mm]',None),('R_ohm','Opór [Ω]',None),
    ('skala','Zakres miernika i jednostka sygnału',None),('tlo_mV','Zmierzony poziom tła [mV]',None),
    ('p0_mm','Położenie centrum obrazu [mm]',None),('Imax','Maksimum centralne [mV]',None),
    ('Imin','Najbliższe minimum [mV]',None)], [
    tab('Pomiary','Rozkład sygnału detektora', ['Nr','Położenie p [mm]','Sygnał U [mV]','Uwagi'],
        ['nr','p_mm','U_mV','uwagi'],1200,'Położenie wylicza się z numeru, początku i kroku. Możesz zastąpić je własnym liczbowym odczytem.'),
    tab('Maksima','Pary maksimów do wyznaczenia rozstawu', ['Nr','Rząd m','Lewe p [mm]','Prawe p [mm]','Uwagi'],
        ['nr','m','left_mm','right_mm','uwagi'],20,'Wpisz rzeczywiste pary −m,+m. Ich rzędy ustal z wykresu; program ich nie zgaduje.')],
    r'r_m=\frac{p_{+m}-p_{-m}}2,\quad d_m=\frac{m\lambda L}{r_m},\\ Q=\frac{I_{\min}}{I_{\max}},\quad \mathcal V=\frac{I_{\max}-I_{\min}}{I_{\max}+I_{\min}}.',
    'Pomiar rozkładu sygnału za dwiema szczelinami i wyznaczenie odległości między ich środkami z par maksimów.')

seed83=[]
for order in [1,2]:
    for line in range(1,9):
        for repeat in range(1,4):seed83.append([line,None,order,repeat,None,None,None,None,None])
SPECS['83']=spec('83','Spektrometr optyczny',[
    ('N','Liczba rys siatki [1/mm]',None),('u_N','Standardowa u liczby rys [1/mm]',None),
    ('szczelina_mm','Szerokość szczeliny [mm]',None),('u_angle_min','Standardowa u odczytu kąta [min]',None),
    ('zero1_deg','I rząd: zero θ0 [stopnie]',None),('zero1_min','I rząd: zero θ0 [minuty]',None),
    ('zero2_deg','II rząd: zero θ0 [stopnie]',None),('zero2_min','II rząd: zero θ0 [minuty]',None),
    ('kontrola_l','Kontrola: α lewa [stopnie dziesiętne]',None),
    ('kontrola_p','Kontrola: α prawa [stopnie dziesiętne]',None)], [
    tab('Odczyty','Wskazania lunety w obu rzędach',
        ['ID','Barwa','Rząd n','Powtórzenie','θL stopnie','θL minuty','θP stopnie','θP minuty','Uwagi'],
        ['id','barwa','order','repeat','ldeg','lmin','rdeg','rmin','uwagi'],48,
        'Wpisuj surowe wskazania skali. Minuty od 0 do <60. Obie żółte linie mają osobne ID.',seed=seed83),
    tab('Odniesienia','Identyfikacja linii', ['ID','λ odniesienia [nm]','Przejście energetyczne','Uwagi'],
        ['id','lambda_ref','przejscie','uwagi'],8,'Wartości odniesienia wpisz z instrukcji; nie są pomiarem.')],
    r'\theta=D+\frac{M}{60},\quad\alpha=|\theta-\theta_0|_{\mathrm{kr}},\quad d=\frac1N,\quad\lambda=\frac{d\sin\alpha}{n}.',
    'Wyznaczenie długości fal linii widmowych rtęci za pomocą siatki dyfrakcyjnej i identyfikacja linii.')


if __name__=='__main__':
    Path(sys.argv[1]).write_text(json.dumps(SPECS,ensure_ascii=False,indent=2),encoding='utf-8')
