"""Eksport treści Worda do samodzielnego źródła LaTeX."""
from pathlib import Path
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph

def esc(s):
    chars={'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}','≪':r'\(\ll\)'}
    return ''.join(chars.get(c,c) for c in s).replace('\n',r'\newline ')

def export(doc, target, equations, header_values=None):
    pre=r'''\documentclass[11pt,a4paper]{article}
\usepackage{fontspec}
\setmainfont{texgyretermes-regular.otf}[BoldFont=texgyretermes-bold.otf,ItalicFont=texgyretermes-italic.otf,BoldItalicFont=texgyretermes-bolditalic.otf]
\setsansfont{texgyreheros-regular.otf}[BoldFont=texgyreheros-bold.otf]
\usepackage[polish]{babel}
\usepackage{amsmath,amssymb,geometry,graphicx,tabularx,array,booktabs,xcolor}
\usepackage[hidelinks]{hyperref}
\geometry{margin=20mm}
\setlength{\parindent}{0pt}
\setlength{\parskip}{7pt}
\renewcommand{\arraystretch}{1.65}
\newcolumntype{Y}{>{\raggedright\arraybackslash}X}
\begin{document}
'''
    content=[pre]; eqiter=iter(equations)
    for node in doc.element.body:
        if node.tag==qn('w:p'):
            par=Paragraph(node,doc)
            if node.xpath('.//w:br[@w:type="page"]'):
                content.append(r'\clearpage'); continue
            if node.xpath('.//m:oMath'):
                content.append('\\[\n'+next(eqiter)+'\n\\]'); continue
            drawings=node.xpath('.//a:blip')
            if drawings:
                for blip in drawings:
                    rel=doc.part.rels[blip.get(qn('r:embed'))]; part=rel.target_part
                    name=Path(str(part.partname)).name
                    asset=target.parent/'latex_images'/name; asset.parent.mkdir(exist_ok=True)
                    asset.write_bytes(part.blob)
                    content.append(r'\begin{center}\includegraphics[width=\linewidth,height=70mm,keepaspectratio]{latex_images/'+name+r'}\end{center}')
                continue
            txt=esc(par.text)
            if not txt: continue
            style=par.style.name
            if style=='Title': content.append(r'{\LARGE\sffamily '+txt+r'\par}\vspace{5mm}')
            elif style=='Heading 1': content.append(r'\section*{'+txt+'}')
            elif style=='Heading 2': content.append(r'\subsection*{'+txt+'}')
            else: content.append(txt+'\n')
        elif node.tag==qn('w:tbl'):
            table=Table(node,doc)
            if len(table.columns)==20 and header_values:
                v=[esc(value) for label,value in header_values]
                def cell(label,value): return r'\textbf{'+label+'}'+(r'\newline '+value if value else '')
                content.append(r'\begingroup\footnotesize\ttfamily\setlength{\parskip}{0pt}\renewcommand{\arraystretch}{1.1}')
                content.append(r'\begin{tabularx}{\linewidth}{|p{30mm}|Y|p{20mm}|p{18mm}|p{23mm}|}\hline')
                content.append(r'\rule[-16mm]{0pt}{19mm}'+ ' & '.join([cell('Wydział',v[0]),cell('Imię i nazwisko',v[1]),cell('Rok',v[2]),cell('Grupa',v[3]),cell('Zespół',v[4])])+r'\\\hline\end{tabularx}\par')
                content.append(r'\begin{tabularx}{\linewidth}{|p{30mm}|Y|p{23mm}|}')
                content.append(r'\rule[-13mm]{0pt}{16mm}\parbox[t]{30mm}{\centering\textbf{PRACOWNIA\\FIZYCZNA\\WFiIS AGH}} & '+cell('Temat:',v[6])+' & '+cell('Nr ćwiczenia',v[7])+r'\\\hline\end{tabularx}\par')
                content.append(r'\begin{tabularx}{\linewidth}{|p{30mm}|Y|Y|Y|Y|p{23mm}|}')
                content.append(r'\rule[-13mm]{0pt}{16mm}'+ ' & '.join(cell(label,v[8+i]) for i,label in enumerate(['Data wykonania','Data oddania','Zwrot do popr.','Data oddania','Data zaliczenia','OCENA']))+r'\\\hline\end{tabularx}\endgroup\par\medskip')
                continue
            if len(table.columns)==1:
                content.append(r'\begin{center}\fbox{\begin{minipage}[c][48mm][c]{0.94\linewidth}\centering '+esc(table.cell(0,0).text.strip())+r'\end{minipage}}\end{center}')
                continue
            n=len(table.columns)
            content.append(r'\begingroup\small\begin{tabularx}{\linewidth}{|'+('|'.join(['Y']*n))+r'|}\hline')
            for i,row in enumerate(table.rows):
                vals=[esc(cell.text) for cell in row.cells]
                if i==0: vals=[r'\textbf{'+v+'}' for v in vals]
                content.append(' & '.join(vals)+r' \\ \hline')
            content.append(r'\end{tabularx}\endgroup\par\medskip')
    content.append(r'\end{document}')
    target.write_text('\n'.join(content),encoding='utf-8')
