#!/usr/bin/env python3
"""Create ready-to-customize .xlsx workbooks for schools and training centres."""
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule
from openpyxl.chart import BarChart, Reference

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"

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


def fill(color):
    return PatternFill("solid", fgColor=color)


thin_gray = Side(style="thin", color=BORDER)


def setup_sheet(ws, title, subtitle, headers, widths, freeze="A5", table_name=None, end_row=60):
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
        tab.tableStyleInfo = TableStyleInfo(
            showFirstColumn=False, showLastColumn=False, showRowStripes=True,
            showColumnStripes=False, name="TabelaAzul",
        )
        ws.add_table(tab)


def write_rows(ws, rows, start=5, end_row=60):
    for r, row in enumerate(rows, start):
        for c, value in enumerate(row, 1):
            cell = ws.cell(r, c, value)
            cell.font = Font(name="Aptos", size=10, color=INK)
            cell.border = Border(bottom=thin_gray)
            cell.alignment = Alignment(vertical="center", wrap_text=True)


def instructions(ws, lines):
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 4
    ws.column_dimensions["B"].width = 100
    c = ws.cell(1, 1, "Planilhas Excel Premium")
    c.font = Font(name="Aptos Display", size=22, bold=True, color=WHITE)
    c.fill = fill(DARK)
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=2)
    ws.row_dimensions[1].height = 44
    c = ws.cell(2, 2, "Instruções de utilização")
    c.font = Font(name="Aptos", size=13, bold=True, color=DARK)
    for i, line in enumerate(lines, 4):
        cell = ws.cell(i, 2, line)
        cell.font = Font(name="Aptos", size=11, color=INK)
        cell.alignment = Alignment(vertical="center", wrap_text=True)
        ws.row_dimensions[i].height = 26


def build_workbook(name, out_folder, filename, sheets_config):
    wb = Workbook()
    ws0 = wb.active
    ws0.title = "Instruções"
    instructions(ws0, sheets_config.get("instruções", []))
    wb.properties.title = name
    wb.properties.creator = "Planilhas Excel Premium"
    wb.calculation.fullCalcOnLoad = True
    wb.calculation.forceFullCalc = True
    wb.calculation.calcMode = "auto"
    for sheet_name, cfg in sheets_config["sheets"].items():
        ws = wb.create_sheet(sheet_name)
        setup_sheet(ws, cfg["title"], cfg["subtitle"], cfg["headers"], cfg["widths"], freeze=cfg.get("freeze", "A5"), table_name=cfg.get("table"), end_row=cfg.get("end_row", 60))
        if cfg.get("rows"):
            write_rows(ws, cfg["rows"])
        if cfg.get("formulas"):
            for ref, formula in cfg["formulas"].items():
                cell = ws[ref]
                cell.value = formula
                cell.font = Font(name="Aptos", size=10, color=INK)
                cell.border = Border(bottom=thin_gray)
                cell.alignment = Alignment(vertical="center")
        if cfg.get("validations"):
            for dv in cfg["validations"]:
                ws.add_data_validation(dv)
        if cfg.get("charts"):
            for chart in cfg["charts"]:
                ws.add_chart(chart, chart.anchor)
    out = PUBLIC / out_folder / filename
    out.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out)
    print(f"created {out.relative_to(ROOT)}")


# ---------------------------------------------------------------------------
# 13 — Gestão de Escola
# ---------------------------------------------------------------------------
build_workbook(
    "Gestão de Escola",
    "13-Escola-Gestao-de-Escola",
    "Gestao_Escola_25000Kz.xlsx",
    {
        "instruções": [
            "1. Personalize no Painel: escola, ano letivo e período.",
            "2. Cadastre alunos, turmas, professores e disciplinas nas folhas correspondentes.",
            "3. Regista frequência e notas e consulte o Painel de indicadores antes das reuniões de pais.",
        ],
        "sheets": {
            "Painel": {
                "title": "Painel — Gestão de Escola",
                "subtitle": "Indicadores automaticos da escola. Nao escreva neste campo.",
                "headers": ["Indicador", "Valor", "Observação"],
                "widths": [28, 18, 46],
                "rows": [
                    ("Total de alunos", "=COUNTA(Alunos!A5:A60)", "Alunos cadastrados"),
                    ("Total de turmas", "=COUNTA(Turmas!A5:A60)", "Turmas em funcionamento"),
                    ("Total de professores", "=COUNTA(Professores!A5:A60)", "Professores cadastrados"),
                    ("Alunos em falta acumulada", "=COUNTIF(Frequência!E5:E60,\"Falta\")", "Acompanhar com a direcção"),
                    ("Média global", "=AVERAGE(Notas!G5:G60)", "Média das notas registadas"),
                    ("Média por turma", "=", "Use a pivot de Notas"),
                ],
            },
            "Alunos": {
                "title": "Alunos",
                "subtitle": "Cadastro basico dos alunos da escola. Preencha de cima para baixo.",
                "headers": ["Nome", "Número de matrícula", "Turma", "Série", "Data de nascimento", "Guardador", "Contacto", "Situação"],
                "widths": [24, 16, 12, 10, 16, 22, 18, 14],
                "rows": [
                    ("Ana Paula Gomes", 1001, "7º A", "7º ano", "2012-03-14", "Amélia Gomes", "923 456 789", "Aprovada"),
                    ("Miguel Manuel Carvalho", 1002, "7º A", "7º ano", "2011-11-02", "José Carvalho", "941 234 567", "Aprovada"),
                    ("Carla Sousa dos Santos", 1003, "7º B", "7º ano", "2012-07-21", "Maria dos Santos", "922 345 678", "Aprovada"),
                    ("João Pedro Fernandes", 1004, "8º A", "8º ano", "2010-05-09", "Rui Fernandes", "946 789 123", "Reprovada"),
                    ("Lúcia Fernandes Muianga", 1005, "8º A", "8º ano", "2011-01-30", "Helena Muianga", "943 891 234", "Aprovada"),
                    ("Rui Miguel da Silva", 1006, "9º A", "9º ano", "2009-09-18", "Paula da Silva", "945 234 567", "Aprovada"),
                ],
            },
            "Turmas": {
                "title": "Turmas",
                "subtitle": "Turmas e turmas do ano letivo.",
                "headers": ["Turma", "Série", "Área / Curso", "Director de turma", "Horário", "Alunos", "Situação"],
                "widths": [12, 10, 22, 22, 18, 12, 14],
                "rows": [
                    ("7º A", "7º ano", "Ciências", "Ana Maria", "07:00 - 12:00", "=COUNTIF(Alunos!C5:C60,A5)", "Activa"),
                    ("7º B", "7º ano", "Ciências", "Bruno Miguel", "07:00 - 12:00", "=COUNTIF(Alunos!C5:C60,A6)", "Activa"),
                    ("8º A", "8º ano", "Linguas", "Carla Sousa", "13:00 - 18:00", "=COUNTIF(Alunos!C5:C60,A7)", "Activa"),
                    ("9º A", "9º ano", "Matemática", "David Domingos", "13:00 - 18:00", "=COUNTIF(Alunos!C5:C60,A8)", "Activa"),
                ],
            },
            "Professores": {
                "title": "Professores",
                "subtitle": "Cadastro dos professores e disciplinas que lecionam.",
                "headers": ["Nome", "Disciplina", "Contacto", "Email", "Horário", "Situação"],
                "widths": [24, 20, 18, 28, 18, 14],
                "rows": [
                    ("Ana Maria Lopes", "Português", "921 111 222", "ana.lopes@escola.co.ao", "07:00 - 12:00", "Activo"),
                    ("Bruno Miguel Silva", "Matemática", "922 333 444", "bruno.silva@escola.co.ao", "07:00 - 12:00", "Activo"),
                    ("Carla Sousa dos Santos", "Ciências", "923 555 666", "carla.santos@escola.co.ao", "13:00 - 18:00", "Activo"),
                    ("David Domingos Nhambiu", "História", "924 777 888", "david.nhambiu@escola.co.ao", "13:00 - 18:00", "Activo"),
                ],
            },
            "Disciplinas": {
                "title": "Disciplinas",
                "subtitle": "Plano de disciplinas por turma.",
                "headers": ["Turma", "Disciplina", "Professor", "Semanas", "Horas semanais", "Observação"],
                "widths": [12, 20, 22, 12, 16, 28],
                "rows": [
                    ("7º A", "Português", "Ana Maria Lopes", 36, 4, "—"),
                    ("7º A", "Matemática", "Bruno Miguel Silva", 36, 4, "—"),
                    ("8º A", "Ciências", "Carla Sousa dos Santos", 36, 3, "—"),
                    ("9º A", "História", "David Domingos Nhambiu", 32, 3, "—"),
                ],
            },
            "Frequência": {
                "title": "Frequência",
                "subtitle": "Registo de frequência dos alunos por dia.",
                "headers": ["Aluno", "Turma", "Data", "Presença", "Observação"],
                "widths": [24, 12, 14, 14, 30],
                "rows": [
                    ("Ana Paula Gomes", "7º A", "2026-10-02", "Presente", "—"),
                    ("Miguel Manuel Carvalho", "7º A", "2026-10-02", "Falta", "Doente"),
                    ("Carla Sousa dos Santos", "7º B", "2026-10-02", "Presente", "—"),
                    ("João Pedro Fernandes", "8º A", "2026-10-02", "Falta", "—"),
                    ("Lúcia Fernandes Muianga", "8º A", "2026-10-02", "Presente", "—"),
                ],
            },
            "Notas": {
                "title": "Notas",
                "subtitle": "Notas dos alunos por disciplina e período.",
                "headers": ["Aluno", "Turma", "Disciplina", "1º período", "2º período", "Média", "Situação"],
                "widths": [24, 12, 18, 12, 12, 10, 12],
                "rows": [
                    ("Ana Paula Gomes", "7º A", "Matemática", 14, 15, "=(D5+E5)/2", "Aprovada"),
                    ("Miguel Manuel Carvalho", "7º A", "Matemática", 11, 12, "=(D6+E6)/2", "Aprovada"),
                    ("Carla Sousa dos Santos", "7º B", "Matemática", 9, 10, "=(D7+E7)/2", "Reprovada"),
                    ("João Pedro Fernandes", "8º A", "Matemática", 8, 7, "=(D8+E8)/2", "Reprovada"),
                    ("Lúcia Fernandes Muianga", "8º A", "Matemática", 15, 16, "=(D9+E9)/2", "Aprovada"),
                ],
                "validations": [DataValidation(type="list", formula1='"Aprovada,Reprovada,Em análise"', allow_blank=True)],
            },
        },
    },
)

# ---------------------------------------------------------------------------
# 14 — Controle de Alunos e Notas
# ---------------------------------------------------------------------------
build_workbook(
    "Controle de Alunos e Notas",
    "14-Escola-Controle-de-Alunos-e-Notas",
    "Controle_Alunos_Notas_12000Kz.xlsx",
    {
        "instruções": [
            "1. Cadastre os alunos e as turmas no início do período letivo.",
            "2. Regista as notas e a frequência por disciplina e aluno.",
            "3. Consulte as médias, aprovações e alunos com dificuldades no Resumo.",
        ],
        "sheets": {
            "Alunos": {
                "title": "Alunos",
                "subtitle": "Cadastro basico dos alunos.",
                "headers": ["Nome", "Matrícula", "Turma", "Data nascimento", "Contacto", "Situação"],
                "widths": [26, 14, 12, 16, 18, 12],
                "rows": [
                    ("Ana Paula Gomes", 2001, "7º A", "2012-03-14", "923 456 789", "Regular"),
                    ("Bruno Miguel da Silva", 2002, "7º A", "2011-08-12", "941 234 567", "Bom"),
                    ("Carla Sousa dos Santos", 2003, "7º B", "2012-07-21", "922 345 678", "Bom"),
                    ("David Domingos Nhambiu", 2004, "8º A", "2010-02-09", "946 789 123", "Regular"),
                    ("Elsa Carolina Bastos", 2005, "8º B", "2011-12-05", "943 891 234", "Excelente"),
                ],
            },
            "Notas": {
                "title": "Notas",
                "subtitle": "Notas por disciplina. A média e a situação calculam-se automaticamente.",
                "headers": ["Aluno", "Turma", "Disciplina", "1º período", "2º período", "Média", "Situação"],
                "widths": [26, 12, 18, 12, 12, 10, 14],
                "rows": [
                    ("Ana Paula Gomes", "7º A", "Português", 15, 16, "=(D5+E5)/2", "=IF(F5>=10,\"Aprovada\",\"Reprovada\")"),
                    ("Bruno Miguel da Silva", "7º A", "Português", 12, 13, "=(D6+E6)/2", "=IF(F6>=10,\"Aprovada\",\"Reprovada\")"),
                    ("Carla Sousa dos Santos", "7º B", "Português", 10, 11, "=(D7+E7)/2", "=IF(F7>=10,\"Aprovada\",\"Reprovada\")"),
                    ("David Domingos Nhambiu", "8º A", "Português", 9, 8, "=(D8+E8)/2", "=IF(F8>=10,\"Aprovada\",\"Reprovada\")"),
                    ("Elsa Carolina Bastos", "8º B", "Português", 16, 17, "=(D9+E9)/2", "=IF(F9>=10,\"Aprovada\",\"Reprovada\")"),
                ],
            },
            "Frequência": {
                "title": "Frequência",
                "subtitle": "Frequência por aluno por dia.",
                "headers": ["Aluno", "Turma", "Data", "Presença", "Faltas", "Observação"],
                "widths": [26, 12, 14, 14, 12, 30],
                "rows": [
                    ("Ana Paula Gomes", "7º A", "2026-10-02", "Presente", "=IF(D5=\"Falta\",1,0)", "—"),
                    ("Bruno Miguel da Silva", "7º A", "2026-10-02", "Presente", "=IF(D6=\"Falta\",1,0)", "—"),
                    ("Carla Sousa dos Santos", "7º B", "2026-10-02", "Falta", "=IF(D7=\"Falta\",1,0)", "Doente"),
                    ("David Domingos Nhambiu", "8º A", "2026-10-02", "Presente", "=IF(D8=\"Falta\",1,0)", "—"),
                    ("Elsa Carolina Bastos", "8º B", "2026-10-02", "Presente", "=IF(D9=\"Falta\",1,0)", "—"),
                ],
            },
            "Resumo": {
                "title": "Resumo",
                "subtitle": "Indicadores automaticos do controlo de alunos e notas.",
                "headers": ["Indicador", "Valor", "Observação"],
                "widths": [30, 16, 44],
                "rows": [
                    ("Total de alunos", "=COUNTA(Alunos!A5:A60)", "Cadastrados"),
                    ("Aprovados", "=COUNTIF(Notas!G5:G60,\"Aprovada\")", "Notas registradas"),
                    ("Reprovados", "=COUNTIF(Notas!G5:G60,\"Reprovada\")", "Acompanhar com a direcção"),
                    ("Média geral", "=AVERAGE(Notas!F5:F60)", "Média das médias"),
                    ("Alunos com faltas", "=COUNTIF(Frequência!D5:D60,\"Falta\")", "Total de faltas registradas"),
                    ("Taxa de aprovação", "=B6/B5", "Aprovados / total"),
                ],
            },
        },
    },
)

# ---------------------------------------------------------------------------
# 15 — Cobrança de Mensalidade Escolar
# ---------------------------------------------------------------------------
build_workbook(
    "Cobrança de Mensalidade Escolar",
    "15-Escola-Cobranca-de-Mensalidade-Escolar",
    "Cobranca_Mensalidade_Escolar_10000Kz.xlsx",
    {
        "instruções": [
            "1. Cadastre os alunos, cursos e os valores das mensalidades.",
            "2. Regista cada recebimento e acompanhe os atrasos por aluno.",
            "3. Emita recibos e consulte a receita no Resumo da escola.",
        ],
        "sheets": {
            "Mensalidades": {
                "title": "Mensalidades",
                "subtitle": "Mensalidades a cobrar por aluno. O saldo calcula-se automaticamente.",
                "headers": ["Aluno", "Turma", "Mensalidade (Kz)", "Data de vencimento", "Pago (Kz)", "Saldo (Kz)", "Situação"],
                "widths": [26, 12, 16, 16, 14, 14, 14],
                "rows": [
                    ("Ana Paula Gomes", "7º A", 12000, "2026-10-05", 12000, "=C5-D5", "Pago"),
                    ("Bruno Miguel da Silva", "7º A", 12000, "2026-10-05", 0, "=C6-D6", "Atrasado"),
                    ("Carla Sousa dos Santos", "7º B", 12000, "2026-10-05", 12000, "=C7-D7", "Pago"),
                    ("David Domingos Nhambiu", "8º A", 14000, "2026-10-05", 7000, "=C8-D8", "Parcial"),
                    ("Elsa Carolina Bastos", "8º B", 14000, "2026-10-05", 14000, "=C9-D9", "Pago"),
                ],
                "validations": [DataValidation(type="list", formula1='"Pago,Parcial,Atrasado,Em análise"', allow_blank=True)],
            },
            "Recebimentos": {
                "title": "Recebimentos",
                "subtitle": "Registo dos recebimentos e pagamentos.",
                "headers": ["Aluno", "Data", "Valor (Kz)", "Forma de pagamento", "Recibo", "Observação"],
                "widths": [26, 14, 14, 22, 14, 26],
                "rows": [
                    ("Ana Paula Gomes", "2026-10-02", 12000, "Dinheiro", "R-001", "—"),
                    ("Carla Sousa dos Santos", "2026-10-02", 12000, "Transferência", "R-002", "—"),
                    ("David Domingos Nhambiu", "2026-10-03", 7000, "Movimento", "R-003", "Saldo em atraso"),
                    ("Elsa Carolina Bastos", "2026-10-04", 14000, "Dinheiro", "R-004", "—"),
                ],
            },
            "Recibos": {
                "title": "Recibos",
                "subtitle": "Recibos emitidos de pagamento de mensalidades.",
                "headers": ["Recibo", "Aluno", "Turma", "Valor (Kz)", "Data", "Situação"],
                "widths": [12, 26, 12, 14, 14, 14],
                "rows": [
                    ("R-001", "Ana Paula Gomes", "7º A", 12000, "2026-10-02", "Emitido"),
                    ("R-002", "Carla Sousa dos Santos", "7º B", 12000, "2026-10-02", "Emitido"),
                    ("R-003", "David Domingos Nhambiu", "8º A", 7000, "2026-10-03", "Emitido"),
                    ("R-004", "Elsa Carolina Bastos", "8º B", 14000, "2026-10-04", "Emitido"),
                ],
            },
            "Resumo": {
                "title": "Resumo",
                "subtitle": "Receita e cobrança da escola.",
                "headers": ["Indicador", "Valor (Kz)", "Observação"],
                "widths": [30, 18, 42],
                "rows": [
                    ("Mensalidades a cobrar", "=SUM(Mensalidades!C5:C60)", "Total de mensalidades"),
                    ("Recebido no período", "=SUM(Recebimentos!C5:C60)", "Total de recebimentos"),
                    ("Em atraso", "=SUM(Mensalidades!F5:F60)", "Saldo em atraso"),
                    ("Alunos em atraso", "=COUNTIF(Mensalidades!G5:G60,\"Atrasado\")", "Acompanhar com a direcção"),
                    ("Receita recebida", "=B6", "Recebido no período"),
                ],
            },
        },
    },
)

# ---------------------------------------------------------------------------
# 16 — Controle de Presença de Formandos
# ---------------------------------------------------------------------------
build_workbook(
    "Controle de Presença de Formandos",
    "16-Centro-Controle-de-Presenca-de-Formandos",
    "Controle_Presenca_Formandos_8000Kz.xlsx",
    {
        "instruções": [
            "1. Configure cursos, turmas, formadores e períodos.",
            "2. Regista a presença diária por formando.",
            "3. Consulte os resumos por turma e identifique as faltas acumuladas.",
        ],
        "sheets": {
            "Turmas": {
                "title": "Turmas",
                "subtitle": "Turmas dos cursos do centro.",
                "headers": ["Turma", "Curso", "Formador", "Início", "Fim", "Formandos", "Situação"],
                "widths": [12, 26, 22, 14, 14, 14, 14],
                "rows": [
                    ("T-01", "Apoio à Criança", "Marta Sousa", "2026-09-01", "2026-12-31", "=COUNTIF(Presença!B5:B60,A5)", "Activa"),
                    ("T-02", "Eletricidade", "Rui Miguel", "2026-09-15", "2027-01-31", "=COUNTIF(Presença!B5:B60,A6)", "Activa"),
                    ("T-03", "Cozinha e Pastaria", "Inês Fernandes", "2026-10-01", "2027-02-28", "=COUNTIF(Presença!B5:B60,A7)", "Activa"),
                ],
            },
            "Presença": {
                "title": "Presença",
                "subtitle": "Registo diário de presença por formando.",
                "headers": ["Formando", "Turma", "Data", "Presença", "Faltas", "Observação"],
                "widths": [26, 12, 14, 14, 12, 30],
                "rows": [
                    ("Ana Paula Gomes", "T-01", "2026-10-02", "Presente", "=IF(D5=\"Falta\",1,0)", "—"),
                    ("Bruno Miguel da Silva", "T-01", "2026-10-02", "Presente", "=IF(D6=\"Falta\",1,0)", "—"),
                    ("Carla Sousa dos Santos", "T-02", "2026-10-02", "Falta", "=IF(D7=\"Falta\",1,0)", "Justificada"),
                    ("David Domingos Nhambiu", "T-02", "2026-10-02", "Presente", "=IF(D8=\"Falta\",1,0)", "—"),
                    ("Elsa Carolina Bastos", "T-03", "2026-10-02", "Presente", "=IF(D9=\"Falta\",1,0)", "—"),
                    ("Francisco dos Santos", "T-03", "2026-10-02", "Falta", "=IF(D10=\"Falta\",1,0)", "—"),
                ],
                "validations": [DataValidation(type="list", formula1='"Presente,Falta,Justificada,Tarde"', allow_blank=True)],
            },
            "Resumo": {
                "title": "Resumo",
                "subtitle": "Presença por turma.",
                "headers": ["Turma", "Formandos presentes", "Faltas", "Taxa de presença", "Observação"],
                "widths": [12, 20, 14, 18, 28],
                "rows": [
                    ("T-01", "=COUNTIF(Presença!D5:D60,\"Presente\")", "=COUNTIF(Presença!D5:D60,\"Falta\")", "=B5/(B5+C5)", "Regular"),
                    ("T-02", "=COUNTIF(Presença!D5:D60,\"Presente\")", "=COUNTIF(Presença!D5:D60,\"Falta\")", "=B6/(B6+C6)", "A acompanhar"),
                    ("T-03", "=COUNTIF(Presença!D5:D60,\"Presente\")", "=COUNTIF(Presença!D5:D60,\"Falta\")", "=B7/(B7+C7)", "Bom"),
                ],
            },
        },
    },
)

# ---------------------------------------------------------------------------
# 17 — Gestão de Certificates
# ---------------------------------------------------------------------------
build_workbook(
    "Gestão de Certificates",
    "17-Centro-Gestao-de-Certificates",
    "Gestao_Certificates_10000Kz.xlsx",
    {
        "instruções": [
            "1. Cadastre os cursos, módulos e formandos habilitados.",
            "2. Regista a emissão dos certificados com data e validade.",
            "3. Valida certificados pelo número e consulta o resumo da base.",
        ],
        "sheets": {
            "Certificates": {
                "title": "Certificates",
                "subtitle": "Base de dados de certificados emitidos.",
                "headers": ["Número", "Formando", "Curso", "Data de emissão", "Validade", "Situação"],
                "widths": [14, 26, 26, 16, 16, 14],
                "rows": [
                    ("CERT-2026-001", "Ana Paula Gomes", "Apoio à Criança", "2026-06-20", "2027-06-20", "Válido"),
                    ("CERT-2026-002", "Bruno Miguel da Silva", "Eletricidade", "2026-06-20", "2027-06-20", "Válido"),
                    ("CERT-2026-003", "Carla Sousa dos Santos", "Cozinha e Pastaria", "2026-07-05", "2027-07-05", "Válido"),
                    ("CERT-2025-148", "David Domingos Nhambiu", "Informática", "2025-06-18", "2026-06-18", "Expirado"),
                ],
                "validations": [DataValidation(type="list", formula1='"Válido,Expirado,Pendente,Revogado"', allow_blank=True)],
            },
            "Emissão": {
                "title": "Emissão",
                "subtitle": "Registo da emissão de certificados.",
                "headers": ["Número", "Formando", "Curso", "Data de emissão", "Formador", "Validade", "Situação"],
                "widths": [14, 26, 26, 16, 22, 16, 14],
                "rows": [
                    ("CERT-2026-001", "Ana Paula Gomes", "Apoio à Criança", "2026-06-20", "Marta Sousa", "2027-06-20", "Emitido"),
                    ("CERT-2026-002", "Bruno Miguel da Silva", "Eletricidade", "2026-06-20", "Rui Miguel", "2027-06-20", "Emitido"),
                    ("CERT-2026-003", "Carla Sousa dos Santos", "Cozinha e Pastaria", "2026-07-05", "Inês Fernandes", "2027-07-05", "Emitido"),
                ],
            },
            "Validação": {
                "title": "Validação",
                "subtitle": "Consulta e validação de certificados pelo número.",
                "headers": ["Número", "Formando", "Curso", "Data de emissão", "Resultado", "Observação"],
                "widths": [16, 26, 26, 16, 14, 26],
                "rows": [
                    ("CERT-2026-001", "Ana Paula Gomes", "Apoio à Criança", "2026-06-20", "Válido", "Conferido"),
                    ("CERT-2026-002", "Bruno Miguel da Silva", "Eletricidade", "2026-06-20", "Válido", "Conferido"),
                    ("CERT-2025-148", "David Domingos Nhambiu", "Informática", "2025-06-18", "Expirado", "Renovar"),
                    ("CERT-2026-003", "Carla Sousa dos Santos", "Cozinha e Pastaria", "2026-07-05", "Válido", "Conferido"),
                ],
                "validations": [DataValidation(type="list", formula1='"Válido,Expirado,Não encontrado,Revogado"', allow_blank=True)],
            },
            "Resumo": {
                "title": "Resumo",
                "subtitle": "Indicadores automaticos da base de certificados.",
                "headers": ["Indicador", "Valor", "Observação"],
                "widths": [30, 16, 44],
                "rows": [
                    ("Certificates emitidos", "=COUNTA(Certificates!A5:A60)", "Total na base"),
                    ("Certificates válidos", "=COUNTIF(Certificates!F5:F60,\"Válido\")", "A validade conferida"),
                    ("Certificates expirados", "=COUNTIF(Certificates!F5:F60,\"Expirado\")", "A renovar"),
                    ("Certificates revogados", "=COUNTIF(Certificates!F5:F60,\"Revogado\")", "A acompanhar"),
                ],
            },
        },
    },
)

# ---------------------------------------------------------------------------
# 18 — Controle de Salas e Horários
# ---------------------------------------------------------------------------
build_workbook(
    "Controle de Salas e Horários",
    "18-Centro-Controle-de-Salas-e-Horarios",
    "Controle_Salas_Horarios_8000Kz.xlsx",
    {
        "instruções": [
            "1. Cadastre as salas, capacidades e restrições de uso.",
            "2. Defina os horários e registe as reservas por turma ou curso.",
            "3. Consulte a ocupação das salas e evite conflitos de agenda.",
        ],
        "sheets": {
            "Salas": {
                "title": "Salas",
                "subtitle": "Salas do centro e características.",
                "headers": ["Sala", "Capacidade", "Tipo", "Equipamento", "Local", "Situação"],
                "widths": [12, 14, 22, 26, 16, 14],
                "rows": [
                    ("Sala A", 30, "Teórica", "Projetor, quadro", "1º andar", "Disponível"),
                    ("Sala B", 20, "Teórica", "Quadro branco", "1º andar", "Disponível"),
                    ("Sala C", 15, "Prática", "Mesas, ferramentas", "Sobrado", "Disponível"),
                    ("Lab 1", 12, "Prática", "Computadores", "Sobrado", "Disponível"),
                ],
            },
            "Horários": {
                "title": "Horários",
                "subtitle": "Horários de funcionamento do centro.",
                "headers": ["Sala", "Dia", "Hora início", "Hora fim", "Utilização", "Observação"],
                "widths": [12, 12, 14, 14, 22, 26],
                "rows": [
                    ("Sala A", "Segunda", "08:00", "12:00", "Teórico", "—"),
                    ("Sala A", "Segunda", "14:00", "18:00", "Teórico", "—"),
                    ("Sala B", "Terça", "08:00", "12:00", "Teórico", "—"),
                    ("Lab 1", "Quarta", "08:00", "12:00", "Prático", "—"),
                    ("Sala C", "Quinta", "14:00", "18:00", "Prático", "—"),
                ],
            },
            "Reservas": {
                "title": "Reservas",
                "subtitle": "Reservas de salas por turma ou curso.",
                "headers": ["Sala", "Turma / Curso", "Dia", "Hora início", "Hora fim", "Formador", "Situação"],
                "widths": [12, 22, 12, 14, 14, 22, 14],
                "rows": [
                    ("Sala A", "T-01 Apoio à Criança", "Segunda", "08:00", "12:00", "Marta Sousa", "Confirmada"),
                    ("Lab 1", "T-02 Eletricidade", "Quarta", "08:00", "12:00", "Rui Miguel", "Confirmada"),
                    ("Sala C", "T-03 Cozinha", "Quinta", "14:00", "18:00", "Inês Fernandes", "Confirmada"),
                    ("Sala B", "Formação Informática", "Terça", "14:00", "18:00", "Carlos Alberto", "Pendente"),
                ],
                "validations": [DataValidation(type="list", formula1='"Confirmada,Pendente,Cancelada"', allow_blank=True)],
            },
            "Resumo": {
                "title": "Resumo",
                "subtitle": "Ocupação das salas do centro.",
                "headers": ["Indicador", "Valor", "Observação"],
                "widths": [30, 16, 44],
                "rows": [
                    ("Total de salas", "=COUNTA(Salas!A5:A60)", "Salas cadastradas"),
                    ("Reservas confirmadas", "=COUNTIF(Reservas!G5:G60,\"Confirmada\")", "Agendas em vigor"),
                    ("Reservas pendentes", "=COUNTIF(Reservas!G5:G60,\"Pendente\")", "A confirmar"),
                    ("Salas disponíveis", "=COUNTIF(Salas!F5:F60,\"Disponível\")", "A uso livre"),
                ],
            },
        },
    },
)
