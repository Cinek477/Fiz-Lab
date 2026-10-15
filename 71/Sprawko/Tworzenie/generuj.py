# /// script
# requires-python = ">=3.11"
# dependencies = ["python-docx>=1.1,<2", "matplotlib>=3.9,<4", "latex2mathml>=3.77,<4", "mathml2omml>=0.0.2,<1"]
# ///
"""uv run generuj.py --template albo uv run generuj.py"""
import argparse
import json
import math
import statistics
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.oxml import parse_xml
from latex2mathml.converter import convert as latex_to_mathml
from mathml2omml import convert as mathml_to_omml
from rownania import WZORY
from latex_export import export as export_latex

PROJECT=Path(__file__).resolve().parent.parent
BASE=PROJECT/'Dane'
def load(name):
    return json.loads((BASE/name).read_text(encoding='utf-8-sig'))
def fmt(v, digits=5):
    if v is None: return '[uzupełnij]'
    if isinstance(v, (int,float)): return f'{v:.{digits}g}'.replace('.',',')
    return str(v)
def numeric(v):
    return isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(v)
def positive(v): return numeric(v) and v>0
def mean_a(values):
    if not values: return None,None
    return statistics.mean(values), statistics.stdev(values)/math.sqrt(len(values)) if len(values)>1 else None
def calc_ext(e, conf, wave, double=False):
    left,right=e.get('p_lewe_mm'),e.get('p_prawe_mm')
    m=e.get('m')
    if not positive(m) or int(m)!=m: raise ValueError('Numer m musi być dodatnią liczbą całkowitą.')
    if left is None or right is None: return None,None,None
    if not numeric(left) or not numeric(right) or right<=left:
        raise ValueError('Ekstrema: prawe położenie musi być większe od lewego.')
    r=(right-left)/2
    if not positive(conf.get('L_mm')) or not positive(wave): return r,None,None
    factor=m if double or e['rodzaj']=='minimum' else m+0.5
    # Wszystkie długości w mm: nm -> mm przez 10^-6.
    value=factor*wave*1e-6*conf['L_mm']/r
    return r,value,factor

def create(template=False, input_dir=None, output_dir=None):
    global BASE
    BASE=Path(input_dir).resolve() if input_dir else PROJECT/'Dane'
    if template: BASE=PROJECT/'Dane'/'szablon'
    params=load('parametry.json'); points=load('pomiary.json'); extrema=load('ekstrema.json')
    for key in ['podwojna']:
        conf=params[key]
        for name in ['L_mm','krok_mm','R_ohm']:
            v=conf.get(name)
            if v is not None and not positive(v): raise ValueError(f'{key}.{name}: wymagana wartość dodatnia.')
        for name in ['u_L_mm','u_p_mm']:
            v=conf.get(name)
            if v is not None and (not numeric(v) or v<0): raise ValueError(f'{key}.{name}: niepewność musi być nieujemna.')
        valid=[]
        for row in points[key]:
            p,i=row.get('p_mm'),row.get('I_ju')
            if p is None and i is None: continue
            if not numeric(p) or not numeric(i): raise ValueError(f'{key}: każdy pomiar wymaga liczbowych p_mm oraz I_ju.')
            valid.append((p,i))
        if len({p for p,i in valid})!=len(valid):
            raise ValueError(f'{key}: powtórzone położenia. Najpierw opracuj powtórzenia i zachowaj surowe dane osobno.')
        points[key]=sorted(valid)
    if not template and not positive(params.get('lambda_nm')): raise ValueError('lambda_nm musi być dodatnia.')
    if not template and not any(points.values()): raise ValueError('Brak pomiarów. Uzupełnij pomiary.json lub uruchom --template.')
    out=Path(output_dir).resolve() if output_dir else PROJECT/'Tworzenie'/'wyniki'
    out.mkdir(parents=True,exist_ok=True)
    charts={}; notices=[]
    for key in ['podwojna']:
        if not points[key]: continue
        for log in ([False,True] if key=='pojedyncza' else [False]):
            fig,ax=plt.subplots(figsize=(6.4,2.8),layout='constrained')
            rows=[(p,i) for p,i in points[key] if not log or i>0]
            skipped=len(points[key])-len(rows)
            if rows:
                px,iv=zip(*rows)
                ax.plot(px,iv,'o-',markersize=3,linewidth=.8,color='#205478',label='Pomiar; odcinki pomocnicze')
                ax.legend(fontsize=8)
            if log: ax.set_yscale('log')
            ax.set_xlabel('Położenie p [mm]'); ax.set_ylabel('Sygnał I [j.u.]')
            ax.grid(True,alpha=.25,which='both')
            tag=key+('_log' if log else '_lin')
            file=out/(tag+'.png'); fig.savefig(file,dpi=220); plt.close(fig)
            charts[tag]=file
            if skipped: notices.append(f'{tag}: pominięto {skipped} niedodatnich punktów wyłącznie na wykresie logarytmicznym.')
    d=Document(); sec=d.sections[0]
    sec.page_width=Cm(21); sec.page_height=Cm(29.7)
    sec.top_margin=Cm(1.8); sec.bottom_margin=Cm(1.8); sec.left_margin=sec.right_margin=Cm(2)
    normal=d.styles['Normal']; normal.font.name='Arial'; normal.font.size=Pt(11)
    normal.paragraph_format.space_after=Pt(8); normal.paragraph_format.line_spacing=1.12
    for style,size in [('Title',20),('Heading 1',14),('Heading 2',11)]:
        d.styles[style].font.name='Arial'; d.styles[style].font.size=Pt(size); d.styles[style].font.color.rgb=RGBColor(0,0,0)
        for border in list(d.styles[style].element.iter(qn('w:pBdr'))):
            border.getparent().remove(border)
    footer=sec.footer.paragraphs[0]; footer.alignment=2
    r=footer.add_run(); fld=OxmlElement('w:fldSimple'); fld.set(qn('w:instr'),'PAGE'); r._r.addnext(fld)
    def p(s): return d.add_paragraph(s)
    def h(s): d.add_heading(s,1)
    def sub(s): d.add_heading(s,2)
    equations=[]
    def eq(s):
        # LaTeX -> natywne równanie Word z ułamkami i indeksami.
        par=d.add_paragraph(); par.alignment=1
        source=WZORY[s]; equations.append(source)
        omml=mathml_to_omml(latex_to_mathml(source))
        # mathml2omml 0.0.2 błędnie zamyka właściwości akcentu (np. kreskę średniej).
        omml=omml.replace('</m:groupChr><m:e>', '</m:groupChrPr><m:e>')
        if 'xmlns:m=' not in omml:
            omml=omml.replace('<m:oMath>', '<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">',1)
        mathnode=parse_xml(omml)
        for group in mathnode.iter(qn('m:groupChr')):
            props=group.find(qn('m:groupChrPr'))
            if props is not None:
                group.tag=qn('m:acc'); props.tag=qn('m:accPr')
                for pos in list(props.findall(qn('m:pos'))): props.remove(pos)
        par._p.append(mathnode)
    def tab(head, rows):
        table=d.add_table(rows=1,cols=len(head)); table.style='Table Grid'
        for cell,label in zip(table.rows[0].cells,head):
            cell.text=label
            for rr in cell.paragraphs[0].runs: rr.bold=True; rr.font.size=Pt(9)
        repeat=OxmlElement('w:tblHeader'); table.rows[0]._tr.get_or_add_trPr().append(repeat)
        for row in rows:
            cells=table.add_row().cells
            for cell,v in zip(cells,row):
                cell.text=fmt(v)
                for par in cell.paragraphs:
                    par.paragraph_format.space_after=Pt(3)
                    for rr in par.runs: rr.font.size=Pt(9)
        for row in table.rows:
            props=row._tr.get_or_add_trPr(); props.append(OxmlElement('w:cantSplit'))
            if template:
                from docx.enum.table import WD_ROW_HEIGHT_RULE
                row.height=Cm(0.8); row.height_rule=WD_ROW_HEIGHT_RULE.AT_LEAST
        p('')
    def picture(tag,caption):
        if tag in charts: d.add_picture(str(charts[tag]),width=Cm(16.5))
        else:
            box=d.add_table(rows=1,cols=1); box.style='Table Grid'
            box.cell(0,0).text='[Wstaw wykres z własnych pomiarów]\n\n\n\n\n\n\n'
        cp=p(caption); cp.paragraph_format.space_after=Pt(8)
        for rr in cp.runs: rr.italic=True; rr.font.size=Pt(9)
    def page(): d.add_page_break()

    from docx.enum.table import WD_ROW_HEIGHT_RULE
    header=d.add_table(rows=3,cols=20); header.style='Table Grid'; header.autofit=False
    for col in header.columns: col.width=Cm(.85)
    for row in header.rows:
        row.height=Cm(1.8); row.height_rule=WD_ROW_HEIGHT_RULE.AT_LEAST
    header_values=[]
    def header_cell(row,start,end,label,value=''):
        cell=header.cell(row,start).merge(header.cell(row,end)); cell.text=''
        par=cell.paragraphs[0]; par.paragraph_format.space_after=Pt(2)
        rr=par.add_run(label); rr.bold=True; rr.font.name='Courier New'; rr.font.size=Pt(9)
        if value: rr=par.add_run('\n'+value); rr.font.name='Courier New'; rr.font.size=Pt(9)
        header_values.append((label,value))
    val=lambda key: '' if template else str(params.get(key,''))
    header_cell(0,0,3,'Wydział',val('wydzial'))
    header_cell(0,4,10,'Imię i nazwisko',val('autorzy'))
    header_cell(0,11,13,'Rok',val('rok'))
    header_cell(0,14,16,'Grupa',val('grupa'))
    header_cell(0,17,19,'Zespół',val('zespol'))
    header_cell(1,0,3,'PRACOWNIA\nFIZYCZNA\nWFiIS AGH')
    header_cell(1,4,15,'Temat:', '' if template else 'Dyfrakcja i interferencja światła na dwóch szczelinach')
    header_cell(1,16,19,'Nr ćwiczenia','' if template else '71')
    for start,end,label,key in [(0,3,'Data wykonania','data_wykonania'),(4,6,'Data oddania','data_oddania'),(7,9,'Zwrot do popr.',''),(10,12,'Data oddania',''),(13,15,'Data zaliczenia',''),(16,19,'OCENA','')]:
        header_cell(2,start,end,label,val(key) if key else '')
    p('')
    h('1 Cel ćwiczenia')
    p('Celem ćwiczenia jest pomiar rozkładu natężenia światła laserowego po przejściu przez dwie szczeliny oraz wyznaczenie odległości między ich środkami.')
    h('2 Podstawy teoretyczne')
    p('Dyfrakcja wynika z falowej natury światła. Fale pochodzące z różnych części szczeliny nakładają się, tworząc maksimum centralne oraz słabsze maksima boczne rozdzielone minimami. Dla dwóch szczelin dodatkowo obserwuje się prążki interferencyjne modulowane obwiednią dyfrakcyjną.')
    p('Przyjmujemy małe kąty, x ≪ L. Symbol a oznacza szerokość jednej szczeliny, d odległość między środkami dwóch szczelin, λ długość fali, L odległość szczelina–detektor, a x odległość względem centrum obrazu. Surowy odczyt skali oznaczamy p; x = p − p0.')
    eq('I(x) = I0 [sin(α)/α]² cos²(β),     β = πdx/(λL)')
    eq('α = πax/(λL); β = πdx/(λL)')
    p('W układzie podwójnym przybliżone położenia maksimów interferencyjnych spełniają x_m = mλL/d. Dla pary −m i +m średnia odległość od centrum wynosi r_m = (p_prawe − p_lewe)/2.')
    page(); h('3 Aparatura i przebieg pomiarów')
    p('Zestaw obejmuje laser czerwony, przesłonę ze szczelinami, ekran z fotodiodą i mechanizmem przesuwu, woltomierz oraz układ zasilania i oporów. Fotodioda wytwarza prąd zależny od natężenia padającego światła; na oporze powstaje napięcie mierzone woltomierzem.')
    p('[Wstaw schemat optyczny i elektryczny albo odwołaj się do schematów instrukcji z podaniem źródła.]')
    tab(['Parametr','Dwie szczeliny'],[['λ [nm]',params['lambda_nm']],['L [mm]',params['podwojna']['L_mm']],['Krok [mm]',params['podwojna']['krok_mm']],['Opór R [Ω]',params['podwojna']['R_ohm']]])
    p(params['opis_przebiegu'])
    p('Do opisu przebiegu: dobór oporu i zakresu, ustawienie centrum, kierunek skanowania, zakres obejmujący prążki boczne, stały opór w serii oraz rzeczywiste odstępstwa. Usuń tę podpowiedź po uzupełnieniu.')

    page(); h('4 Wyniki pomiarów')
    p('Sygnał I [j.u.] odpowiada [napięciu w mV / wskazaniom miernika w ustalonej skali — wybierz]. Położenia p są bezpośrednimi odczytami skali. [Opisz ewentualną korektę tła.]')
    for key,label in [('podwojna','Tabela 1 Dwie szczeliny')]:
        sub(label)
        rows=points[key]
        if rows:
            count=math.ceil(len(rows)/3); packed=[]
            for i in range(count):
                row=[]
                for j in range(3): row+=list(rows[i+j*count]) if i+j*count<len(rows) else ['','']
                packed.append(row)
        else: packed=[['[p]','[I]']*3 for _ in range(8)]
        tab(['p [mm]','I [j.u.]']*3,packed)
    p('[Zapisz rozdzielczość skali i woltomierza oraz zauważone wahania odczytów. Długie tabele mogą przejść na kolejne strony.]')

    derived={'podwojna':[]}
    page(); h('5 Opracowanie dwóch szczelin')
    picture('podwojna_lin','Wykres 1 Rozkład sygnału dla podwójnej szczeliny w skali liniowej')
    eq('r_m = (p_prawe,m − p_lewe,m)/2;     d_m = mλL/r_m')
    rows=[]; dv=[]
    for e in extrema['podwojna']:
        r,v,_=calc_ext(e,params['podwojna'],params['lambda_nm'],True)
        rows.append([e['m'],e.get('p_lewe_mm'),e.get('p_prawe_mm'),r,v])
        if v is not None: dv.append(v)
        derived['podwojna'].append({'m':e['m'],'r_mm':r,'d_mm':v})
    sub('Tabela 2 Pary maksimów interferencyjnych')
    tab(['m','p lewe [mm]','p prawe [mm]','r_m [mm]','d_m [mm]'],rows)
    dm,du=mean_a(dv)
    p(f'd średnie = {fmt(dm)} mm; uA(d) = {fmt(du)} mm; u(d) = {fmt(params["podwojna"].get("u_koncowe_d_mm"))} mm.')
    imax,imin=params['podwojna'].get('Imax_ju'),params['podwojna'].get('Imin_ju')
    if imin is not None and (not numeric(imin) or imin<0): raise ValueError('Imin musi być nieujemne.')
    if imax is not None and not positive(imax): raise ValueError('Imax musi być dodatnie.')
    if numeric(imin) and positive(imax) and imin>imax: raise ValueError('Imin nie może przekraczać Imax.')
    q=imin/imax if numeric(imin) and positive(imax) else None
    p(f'Jakość obrazu: Imax = {fmt(imax)} j.u.; Imin w najbliższym minimum = {fmt(imin)} j.u.; Q = Imin/Imax = {fmt(q)}.')
    p('[Zinterpretuj Q i opisz wpływ tła oraz skończonej szerokości detektora.]')

    page(); h('6 Niepewności pomiarów')
    p(params['opis_niepewnosci'])
    tab(['Wielkość','Wartość niepewności standardowej'],[['u(λ) [nm]',params.get('u_lambda_nm')],['u(L) [mm]',params['podwojna'].get('u_L_mm')],['u(p) [mm]',params['podwojna'].get('u_p_mm')]])
    eq('uA(z średniego) = √[Σ(z_i − z średnie)² / (N(N − 1))]')
    eq('u(r) = √[u(p_lewe)² + u(p_prawe)²]/2')
    eq('u(z)/z = √[(u(λ)/λ)² + (u(L)/L)² + (u(r)/r)²]')
    p('Ostatni wzór dotyczy pojedynczego oszacowania odległości między szczelinami przy niezależnych danych wejściowych. λ i L są wspólne dla wyników w serii. Odczyty maksimów pochodzą z tego samego rozkładu; przy niepewności średniej uwzględnij korelacje i sposób ustalenia położeń maksimów. Sama uA nie obejmuje wszystkich tych efektów.')
    p('Niepewność rozszerzona: U = k·u, k = [podaj, jeżeli stosujesz]. Końcowe wyniki zaokrąglij do miejsca dziesiętnego wynikającego z niepewności.')
    h('7 Wnioski')
    p(params['wnioski'])
    p('[Podaj końcowe d z niepewnościami, oceń obraz względem teorii, skomentuj stosunki natężeń i Q. Uzasadnij dominujące źródła rozbieżności własnymi obserwacjami.]')
    target=out/('71_szablon_sprawozdania.docx' if template else '71_sprawozdanie_do_weryfikacji.docx')
    d.save(target)
    export_latex(d,target.with_suffix('.tex'),equations,header_values)
    result={'d_srednie_mm':dm,'uA_d_mm':du,'Q':q,'ekstrema':derived,'uwagi':notices}
    (out/'obliczenia.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(target)
    print('Weryfikacja: ekstrema, gładkie krzywe, końcowe niepewności, zaokrąglenia i wnioski wymagają przeglądu.')
    for notice in notices: print(notice)
    return target,result

if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Generator sprawozdania z ćwiczenia 71')
    parser.add_argument('--template',action='store_true',help='Utwórz szablon z pustymi polami.')
    parser.add_argument('--input-dir',help='Folder z trzema wejściowymi plikami JSON.')
    parser.add_argument('--output-dir',help='Folder wynikowy; domyślnie wyniki przy danych.')
    args=parser.parse_args()
    try: create(args.template,args.input_dir,args.output_dir)
    except (ValueError,KeyError,TypeError) as exc: parser.exit(2,f'Błąd danych: {exc}\n')
