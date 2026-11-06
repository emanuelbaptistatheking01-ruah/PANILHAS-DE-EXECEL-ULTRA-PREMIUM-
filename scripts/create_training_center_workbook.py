#!/usr/bin/env python3
"""Create a ready-to-customize .xlsx workbook for a technical/professional training centre."""
from pathlib import Path
from datetime import date
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule
from openpyxl.chart import BarChart, Reference
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public/11-Centro-de-Formacao-Tecnico-Profissional/Gestao_Centro_Formacao_Tecnico_Profissional_25000Kz.xlsx"
OUT.parent.mkdir(parents=True, exist_ok=True)

DARK = "163A2A"
GREEN = "26734D"
LIME = "DDF2B2"
PALE = "EAF4EC"
YELLOW = "FFF2CC"
GRAY = "EEF2EF"
WHITE = "FFFFFF"
INK = "23342B"
MUTED = "65756B"
RED = "FCE4D6"
BORDER = "D9E2DC"

wb = Workbook()
ws0 = wb.active
ws0.title = "Instruções"
sheets = {ws0.title: ws0}
for name in ["Painel", "Cursos", "Formandos", "Matrículas", "Pagamentos", "Assiduidade", "Avaliações", "Certificados"]:
    sheets[name] = wb.create_sheet(name)

# Document properties
wb.properties.title = "Gestão de Centro de Formação Técnico-Profissional"
wb.properties.subject = "Gestão de cursos, formandos, matrículas, pagamentos, presenças, avaliações e certificados"
wb.properties.creator = "Planilhas Excel Premium"
wb.calculation.fullCalcOnLoad = True
wb.calculation.forceFullCalc = True
wb.calculation.calcMode = "auto"

# Shared workbook styling helpers
def fill(color): return PatternFill("solid", fgColor=color)
thin_gray = Side(style="thin", color=BORDER)

def setup_sheet(ws, title, subtitle, headers, widths, end_row=50, freeze="A5", table_name=None):
    n = len(headers)
    ws.sheet_view.showGridLines = False
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=n)
    c = ws.cell(1, 1, title)
    c.font = Font(name="Aptos Display", size=19, bold=True, color=WHITE)
    c.fill = fill(DARK)
    c.alignment = Alignment(vertical="center")
    ws.row_dimensions[1].height = 38
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=n)
    c = ws.cell(2, 1, subtitle)
    c.font = Font(name="Aptos", size=10, italic=True, color=MUTED)
    c.fill = fill("F6F8F6")
    c.alignment = Alignment(vertical="center", wrap_text=True)
    ws.row_dimensions[2].height = 30
    for i, h in enumerate(headers, 1):
        cell = ws.cell(4, i, h)
        cell.font = Font(name="Aptos", size=10, bold=True, color=WHITE)
        cell.fill = fill(GREEN)
        cell.alignment = Alignment(vertical="center", wrap_text=True)
        cell.border = Border(bottom=Side(style="medium", color=DARK))
    ws.row_dimensions[4].height = 34
    for idx, width in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(idx)].width = width
    ws.freeze_panes = freeze
    ws.auto_filter.ref = f"A4:{get_column_letter(n)}{end_row}"
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.outlinePr.summaryBelow = True
    if table_name:
        tab = Table(displayName=table_name, ref=f"A4:{get_column_letter(n)}{end_row}")
        tab.tableStyleInfo = TableStyleInfo(name="TableStyleMedium4", showFirstColumn=False, showLastColumn=False, showRowStripes=True, showColumnStripes=False)
        ws.add_table(tab)


def format_data(ws, first, last, cols, input_cols=None):
    input_cols = set(input_cols or range(1, cols + 1))
    for row in range(first, last + 1):
        for col in range(1, cols + 1):
            c = ws.cell(row, col)
            c.font = Font(name="Aptos", size=10, color=INK)
            c.fill = fill(YELLOW if col in input_cols else GRAY)
            c.border = Border(bottom=thin_gray)
            c.alignment = Alignment(vertical="center")
        ws.row_dimensions[row].height = 22

# Instructions sheet
ws = ws0
ws.sheet_view.showGridLines = False
ws.merge_cells("A1:F1")
ws["A1"] = "GESTÃO DE CENTRO DE FORMAÇÃO TÉCNICO-PROFISSIONAL"
ws["A1"].font = Font(name="Aptos Display", size=20, bold=True, color=WHITE)
ws["A1"].fill = fill(DARK); ws["A1"].alignment = Alignment(vertical="center")
for col in range(1, 7): ws.cell(1, col).fill = fill(DARK)
ws.row_dimensions[1].height = 42
ws.merge_cells("A2:F2")
ws["A2"] = "Gestão de cursos, formandos, matrículas, pagamentos e acompanhamento académico num único ficheiro."
ws["A2"].font = Font(name="Aptos", size=11, color=MUTED, italic=True)
ws["A2"].alignment = Alignment(wrap_text=True, vertical="center")
ws.row_dimensions[2].height = 32
ws.merge_cells("A4:F4"); ws["A4"] = "COMECE AQUI — FLUXO RECOMENDADO"
ws["A4"].font = Font(name="Aptos", size=12, bold=True, color=WHITE)
for col in range(1,7): ws.cell(4,col).fill = fill(GREEN)
instructions = [
    (1, "Configure os cursos", "Na aba Cursos, substitua os exemplos pelos cursos, duração, preços, formadores, vagas e estado do seu centro."),
    (2, "Cadastre os formandos", "Na aba Formandos, crie um código único e registe apenas os dados necessários. O curso pode ser seleccionado na lista."),
    (3, "Registe matrículas", "Em Matrículas, associe o código do formando ao curso, indique turma e modalidade e confirme o valor calculado."),
    (4, "Lance pagamentos", "Registe cada pagamento em Pagamentos. Só linhas com estado Pago contam como receita recebida e reduzem o saldo."),
    (5, "Acompanhe as aulas", "Use Assiduidade para presenças e faltas e Avaliações para notas. Registe a emissão dos certificados após validação."),
    (6, "Consulte o Painel", "O Painel resume matrículas activas, cursos, pagamentos e saldos; abra o ficheiro no Excel para actualizar os cálculos."),
]
for r, (num, label, body) in enumerate(instructions, 5):
    ws.cell(r,1,num); ws.cell(r,1).font = Font(size=12,bold=True,color=GREEN); ws.cell(r,1).fill = fill(PALE)
    ws.cell(r,2,label); ws.cell(r,2).font = Font(size=10,bold=True,color=INK)
    ws.merge_cells(start_row=r,start_column=3,end_row=r,end_column=6)
    ws.cell(r,3,body); ws.cell(r,3).font = Font(size=10,color=INK); ws.cell(r,3).alignment=Alignment(wrap_text=True,vertical="center")
    for cc in range(1,7): ws.cell(r,cc).border=Border(bottom=thin_gray)
    ws.row_dimensions[r].height=34
ws.merge_cells("A13:F13"); ws["A13"] = "LEGENDA E CUIDADOS"
ws["A13"].font = Font(size=12,bold=True,color=WHITE)
for col in range(1,7): ws.cell(13,col).fill=fill(GREEN)
notes = [
    ("Células amarelas", "Campos de entrada: pode editar/preencher."),
    ("Células cinzentas", "Cálculos automáticos: evite substituir as fórmulas."),
    ("Exemplos de cursos", "Os cursos e valores pré-preenchidos são ilustrativos; substitua-os pelos dados e preços reais do centro."),
    ("Privacidade", "O ficheiro fica guardado onde o utilizador o colocar. Proteja os dados pessoais e faça cópias de segurança."),
    ("Compatibilidade", "Recomendado Microsoft Excel 2016 ou posterior. As fórmulas recalculam ao abrir o ficheiro."),
]
for r,(label,body) in enumerate(notes,14):
    ws.cell(r,1,label).font=Font(size=10,bold=True,color=INK)
    ws.merge_cells(start_row=r,start_column=2,end_row=r,end_column=6)
    ws.cell(r,2,body).font=Font(size=10,color=MUTED); ws.cell(r,2).alignment=Alignment(wrap_text=True,vertical="center")
    for cc in range(1,7): ws.cell(r,cc).border=Border(bottom=thin_gray)
    ws.row_dimensions[r].height=30
for col,w in enumerate([18,24,23,23,23,23],1): ws.column_dimensions[get_column_letter(col)].width=w
ws.freeze_panes="A4"

# Courses catalog with editable illustrative examples
courses = sheets["Cursos"]
setup_sheet(courses, "CATÁLOGO DE CURSOS", "Exemplos editáveis para demonstração. Ajuste nomes, duração, preços, formadores, vagas e estado ao seu centro.", ["Código", "Curso", "Área", "Duração (meses)", "Valor total (Kz)", "Formador", "Vagas", "Estado"], [15,35,23,19,20,26,13,16], 34, table_name="CatalogoCursos")
examples = [
    ["C001", "Informática e Ferramentas Digitais", "Tecnologia", 3, 75000, "A definir", 25, "Activo"],
    ["C002", "Electricidade de Instalações", "Electricidade", 4, 120000, "A definir", 20, "Activo"],
    ["C003", "Contabilidade e Gestão Administrativa", "Gestão", 4, 110000, "A definir", 25, "Activo"],
    ["C004", "Canalização e Manutenção Predial", "Construção", 3, 90000, "A definir", 20, "Activo"],
]
for r, row in enumerate(examples, 5):
    for c, value in enumerate(row, 1): courses.cell(r,c,value)
format_data(courses,5,34,8)
for r in range(5,35):
    courses.cell(r,5).number_format='#,##0 "Kz"'
    courses.cell(r,4).number_format='0 "meses"'

# Students
students = sheets["Formandos"]
setup_sheet(students,"REGISTO DE FORMANDOS","Use um código único por formando. Total pago e saldo são calculados a partir de pagamentos e matrículas activas.",["Código formando","Nome completo","Telefone","E-mail","Curso de interesse","Género (opcional)","Data de nascimento (opcional)","Estado","Total pago (Kz)","Saldo activo (Kz)"],[18,30,19,31,34,20,24,16,20,21],254,table_name="RegistoFormandos")
format_data(students,5,254,10,input_cols=[1,2,3,4,5,6,7,8])
for r in range(5,255):
    students.cell(r,9,f'=IF(A{r}="","",SUMIFS(Pagamentos!$H$5:$H$404,Pagamentos!$C$5:$C$404,A{r},Pagamentos!$I$5:$I$404,"Pago"))')
    students.cell(r,10,f'=IF(A{r}="","",SUMIFS(Matrículas!$J$5:$J$204,Matrículas!$B$5:$B$204,A{r},Matrículas!$K$5:$K$204,"Activa")-I{r})')
    for c in [9,10]: students.cell(r,c).number_format='#,##0 "Kz"'
    students.cell(r,7).number_format="dd/mm/yyyy"

# Enrolments
mat = sheets["Matrículas"]
setup_sheet(mat,"MATRÍCULAS","Associe cada formando a um curso. O nome e o preço são procurados no cadastro; desconto e estado são editáveis.",["N.º matrícula","Código formando","Nome do formando","Curso","Data matrícula","Turma / turno","Modalidade","Preço do curso (Kz)","Desconto (Kz)","Valor final (Kz)","Estado"],[18,18,28,35,19,20,18,22,19,22,16],204,table_name="RegistoMatriculas")
format_data(mat,5,204,11,input_cols=[1,2,4,5,6,7,9,11])
for r in range(5,205):
    mat.cell(r,3,f'=IFERROR(VLOOKUP(B{r},Formandos!$A$5:$B$254,2,FALSE),"")')
    mat.cell(r,8,f'=IFERROR(VLOOKUP(D{r},Cursos!$B$5:$F$34,4,FALSE),0)')
    mat.cell(r,10,f'=IF(H{r}="","",MAX(0,H{r}-I{r}))')
    mat.cell(r,5).number_format="dd/mm/yyyy"
    for c in [8,9,10]: mat.cell(r,c).number_format='#,##0 "Kz"'

# Payments
pay = sheets["Pagamentos"]
setup_sheet(pay,"REGISTO DE PAGAMENTOS","Registe cada recebimento numa linha. Marque Pago apenas depois de confirmar a entrada do valor.",["N.º recibo","Data","Código formando","Nome do formando","Referência / mês","Método de pagamento","Observação","Valor (Kz)","Estado","Registado por"],[18,16,20,28,22,22,29,20,16,23],404,table_name="RegistoPagamentos")
format_data(pay,5,404,10,input_cols=[1,2,3,5,6,7,8,9,10])
for r in range(5,405):
    pay.cell(r,4,f'=IFERROR(VLOOKUP(C{r},Formandos!$A$5:$B$254,2,FALSE),"")')
    pay.cell(r,2).number_format="dd/mm/yyyy"
    pay.cell(r,8).number_format='#,##0 "Kz"'

# Attendance
att = sheets["Assiduidade"]
setup_sheet(att,"ASSIDUIDADE E PRESENÇAS","Registe uma linha por formando e sessão para acompanhar presenças, atrasos e faltas.",["Data","Código formando","Nome do formando","Curso","Turma / sessão","Presença","Falta justificada?","Observações"],[17,20,29,35,24,18,23,38],304,table_name="RegistoAssiduidade")
format_data(att,5,304,8,input_cols=[1,2,4,5,6,7,8])
for r in range(5,305):
    att.cell(r,3,f'=IFERROR(VLOOKUP(B{r},Formandos!$A$5:$B$254,2,FALSE),"")')
    att.cell(r,1).number_format="dd/mm/yyyy"

# Assessments
assess = sheets["Avaliações"]
setup_sheet(assess,"AVALIAÇÕES E RESULTADOS","Introduza notas entre 0 e 20. A média final usa 40% teórica e 60% prática; o resultado é calculado automaticamente.",["Data","Código formando","Nome do formando","Curso","Módulo / unidade","Nota teórica (0–20)","Nota prática (0–20)","Média final","Resultado","Observações"],[17,20,29,34,30,22,22,18,19,34],254,table_name="RegistoAvaliacoes")
format_data(assess,5,254,10,input_cols=[1,2,4,5,6,7,10])
for r in range(5,255):
    assess.cell(r,3,f'=IFERROR(VLOOKUP(B{r},Formandos!$A$5:$B$254,2,FALSE),"")')
    assess.cell(r,8,f'=IF(OR(F{r}="",G{r}=""),"",ROUND(F{r}*40%+G{r}*60%,1))')
    assess.cell(r,9,f'=IF(H{r}="","",IF(H{r}>=10,"Apto","Reforço"))')
    assess.cell(r,1).number_format="dd/mm/yyyy"
    for c in [6,7,8]: assess.cell(r,c).number_format="0.0"

# Certificates
cert = sheets["Certificados"]
setup_sheet(cert,"CONTROLO DE CERTIFICADOS","Registe a elegibilidade e a emissão após confirmar os requisitos académicos e administrativos do centro.",["N.º certificado","Código formando","Nome do formando","Curso","Resultado final","Data de conclusão","Data de emissão","Estado","Observações"],[22,20,29,35,21,21,21,18,34],204,table_name="RegistoCertificados")
format_data(cert,5,204,9,input_cols=[1,2,4,5,6,7,8,9])
for r in range(5,205):
    cert.cell(r,3,f'=IFERROR(VLOOKUP(B{r},Formandos!$A$5:$B$254,2,FALSE),"")')
    cert.cell(r,6).number_format="dd/mm/yyyy"; cert.cell(r,7).number_format="dd/mm/yyyy"

# Dashboard: four KPI cards and monthly operational overview
p = sheets["Painel"]
p.sheet_view.showGridLines=False
p.merge_cells("A1:H1"); p["A1"]="PAINEL DE GESTÃO DO CENTRO"; p["A1"].font=Font(name="Aptos Display",size=21,bold=True,color=WHITE); p["A1"].fill=fill(DARK); p["A1"].alignment=Alignment(vertical="center")
for c in range(1,9): p.cell(1,c).fill=fill(DARK)
p.row_dimensions[1].height=43
p.merge_cells("A2:H2"); p["A2"]="Indicadores actualizados automaticamente a partir das matrículas e pagamentos registados."; p["A2"].font=Font(size=10,italic=True,color=MUTED); p["A2"].alignment=Alignment(vertical="center")
for c in range(1,9): p.column_dimensions[get_column_letter(c)].width=20
cards=[("A4:B4","A5:B6","MATRÍCULAS ACTIVAS",'=COUNTIF(Matrículas!$K$5:$K$204,"Activa")',"0"),
       ("C4:D4","C5:D6","CURSOS ACTIVOS",'=COUNTIF(Cursos!$H$5:$H$34,"Activo")',"0"),
       ("E4:F4","E5:F6","PAGAMENTOS RECEBIDOS",'=SUMIFS(Pagamentos!$H$5:$H$404,Pagamentos!$I$5:$I$404,"Pago")','#,##0 "Kz"'),
       ("G4:H4","G5:H6","SALDO DE MATRÍCULAS ACTIVAS",'=SUMIFS(Matrículas!$J$5:$J$204,Matrículas!$K$5:$K$204,"Activa")-SUMIFS(Pagamentos!$H$5:$H$404,Pagamentos!$I$5:$I$404,"Pago")','#,##0 "Kz"')]
for label_rng,val_rng,label,formula,numfmt in cards:
    p.merge_cells(label_rng); p.merge_cells(val_rng)
    cell=p[label_rng.split(":")[0]]; cell.value=label; cell.fill=fill(GREEN); cell.font=Font(size=9,bold=True,color=WHITE); cell.alignment=Alignment(horizontal="center",vertical="center",wrap_text=True)
    val=p[val_rng.split(":")[0]]; val.value=formula; val.fill=fill(PALE); val.font=Font(size=19,bold=True,color=DARK); val.alignment=Alignment(horizontal="center",vertical="center"); val.number_format=numfmt
    for row in p[label_rng]:
        for c in row: c.fill=fill(GREEN); c.border=Border(left=thin_gray,right=thin_gray,top=thin_gray,bottom=thin_gray)
    for row in p[val_rng]:
        for c in row: c.fill=fill(PALE); c.border=Border(left=thin_gray,right=thin_gray,top=thin_gray,bottom=thin_gray)
p.row_dimensions[4].height=29; p.row_dimensions[5].height=28; p.row_dimensions[6].height=18
p.merge_cells("A9:C9"); p["A9"]="ACOMPANHAMENTO MENSAL"; p["A9"].font=Font(size=12,bold=True,color=WHITE)
for c in range(1,4): p.cell(9,c).fill=fill(GREEN)
for c,h in enumerate(["Mês","Matrículas activas","Receita recebida (Kz)"],1):
    p.cell(11,c,h); p.cell(11,c).font=Font(size=10,bold=True,color=WHITE); p.cell(11,c).fill=fill(GREEN); p.cell(11,c).alignment=Alignment(wrap_text=True)
for month in range(1,13):
    row=11+month
    p.cell(row,1,f'=DATE(YEAR(TODAY()),{month},1)'); p.cell(row,1).number_format="mmm yyyy"
    p.cell(row,2,f'=COUNTIFS(Matrículas!$E$5:$E$204,">="&A{row},Matrículas!$E$5:$E$204,"<"&EDATE(A{row},1),Matrículas!$K$5:$K$204,"Activa")')
    p.cell(row,3,f'=SUMIFS(Pagamentos!$H$5:$H$404,Pagamentos!$I$5:$I$404,"Pago",Pagamentos!$B$5:$B$404,">="&A{row},Pagamentos!$B$5:$B$404,"<"&EDATE(A{row},1))'); p.cell(row,3).number_format='#,##0 "Kz"'
    for col in range(1,4): p.cell(row,col).fill=fill("F4F7F4" if month%2==0 else WHITE); p.cell(row,col).border=Border(bottom=thin_gray)
chart=BarChart(); chart.type="col"; chart.style=10; chart.title="Receita mensal recebida"; chart.y_axis.title="Kz"; chart.x_axis.title="Mês"; chart.height=8; chart.width=16
chart.add_data(Reference(p,min_col=3,min_row=11,max_row=23),titles_from_data=True); chart.set_categories(Reference(p,min_col=1,min_row=12,max_row=23)); chart.legend=None
p.add_chart(chart,"E9")
p.freeze_panes="A11"; p.sheet_properties.pageSetUpPr.fitToPage=True; p.page_setup.fitToWidth=1; p.page_setup.fitToHeight=1

# Drop-downs based on named ranges, compatible with Excel validation
wb.defined_names.add(DefinedName("ListaCursos", attr_text="'Cursos'!$B$5:$B$34"))
wb.defined_names.add(DefinedName("ListaFormandos", attr_text="'Formandos'!$A$5:$A$254"))

def add_list(ws, cell_range, formula, prompt):
    dv=DataValidation(type="list",formula1=formula,allow_blank=True)
    dv.error="Seleccione um valor da lista ou actualize primeiro o cadastro correspondente."
    dv.errorTitle="Valor não reconhecido"
    dv.prompt=prompt; dv.promptTitle="Selecção de lista"; dv.showInputMessage=True; dv.showErrorMessage=True
    ws.add_data_validation(dv); dv.add(cell_range)

add_list(students,"E5:E254","=ListaCursos","Escolha um curso cadastrado; é possível deixar em branco se ainda não houver matrícula.")
add_list(students,"F5:F254",'"Feminino,Masculino,Prefiro não indicar"',"Campo opcional; recolha apenas os dados de que realmente precisa.")
add_list(students,"H5:H254",'"Activo,Inactivo,Concluído"',"Actualize o estado do formando.")
add_list(mat,"B5:B204","=ListaFormandos","Escolha o código do formando cadastrado.")
add_list(mat,"D5:D204","=ListaCursos","Escolha um curso cadastrado.")
add_list(mat,"G5:G204",'"Presencial,Online,Híbrido"',"Seleccione a modalidade.")
add_list(mat,"K5:K204",'"Activa,Concluída,Cancelada"',"Indique o estado da matrícula.")
add_list(pay,"C5:C404","=ListaFormandos","Escolha o código do formando.")
add_list(pay,"F5:F404",'"Numerário,Transferência,TPA,Multicaixa Express,Outro"',"Seleccione o método recebido.")
add_list(pay,"I5:I404",'"Pago,Pendente,Anulado"',"Actualize o estado conforme a confirmação do recebimento.")
add_list(att,"B5:B304","=ListaFormandos","Escolha o formando presente na sessão.")
add_list(att,"F5:F304",'"Presente,Falta,Atraso"',"Seleccione o estado de presença.")
add_list(att,"G5:G304",'"Sim,Não"',"Indique se a falta foi justificada.")
add_list(assess,"B5:B254","=ListaFormandos","Escolha o formando avaliado.")
add_list(cert,"B5:B204","=ListaFormandos","Escolha o formando.")
add_list(cert,"H5:H204",'"Em preparação,Emitido,Entregue"',"Actualize o estado do certificado.")
add_list(courses,"H5:H34",'"Activo,Inactivo"',"Seleccione o estado do curso.")
# Grade validation
for col in (6,7):
    dv=DataValidation(type="decimal",operator="between",formula1=0,formula2=20,allow_blank=True)
    dv.error="Introduza uma nota entre 0 e 20."; dv.showErrorMessage=True
    assess.add_data_validation(dv); dv.add(f"{get_column_letter(col)}5:{get_column_letter(col)}254")
# Conditional highlights for useful exception spotting
assess.conditional_formatting.add("H5:H254",CellIsRule(operator="lessThan",formula=[10],fill=fill(RED)))
assess.conditional_formatting.add("H5:H254",CellIsRule(operator="greaterThanOrEqual",formula=[10],fill=fill(LIME)))
students.conditional_formatting.add("I5:I254",CellIsRule(operator="greaterThan",formula=[0],fill=fill(YELLOW)))

# Consistent tabs, print areas, and active view
for ws in wb.worksheets:
    ws.sheet_properties.tabColor = GREEN if ws.title == "Painel" else (DARK if ws.title == "Instruções" else "82B596")
    ws.sheet_view.zoomScale = 90
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_margins.left=0.25; ws.page_margins.right=0.25; ws.page_margins.top=0.5; ws.page_margins.bottom=0.5
wb.active = wb.sheetnames.index("Painel")
wb.save(OUT)
print(f"Created {OUT.relative_to(ROOT)} ({OUT.stat().st_size} bytes)")
