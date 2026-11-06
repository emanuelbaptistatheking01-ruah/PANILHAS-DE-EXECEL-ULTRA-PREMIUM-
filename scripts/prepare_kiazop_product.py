#!/usr/bin/env python3
"""Decrypt a supplied KIAZOP source privately, sanitize demo records, and prepare its sellable copy.

The file-open password is requested at runtime with getpass; it is never stored in code or output.
"""
from copy import copy
from getpass import getpass
from pathlib import Path
import tempfile

import msoffcrypto
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "public/12-Centro-de-Formacao-KIAZOP"
SOURCE = FOLDER / "KIAZOP_Sistema_Propinas_v6_(1).xlsx"
OUTPUT = FOLDER / "KIAZOP_Sistema_Propinas_35000Kz.xlsx"

if not SOURCE.is_file():
    raise SystemExit(f"Place the original encrypted workbook at: {SOURCE}")

# Decrypt only into a temporary file outside public/; never expose plaintext source data.
with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
    decrypted_path = Path(tmp.name)
try:
    with SOURCE.open("rb") as src:
        office = msoffcrypto.OfficeFile(src)
        if office.is_encrypted():
            office.load_key(password=getpass("Password to open the source workbook: "))
            with decrypted_path.open("wb") as dest:
                office.decrypt(dest)
        else:
            # Accept an already-unlocked copy without changing its content first.
            decrypted_path.write_bytes(SOURCE.read_bytes())

    wb = load_workbook(decrypted_path, data_only=False, keep_links=True)
    if "CAPA" not in wb.sheetnames or "CURSOS" not in wb.sheetnames:
        raise ValueError("This does not look like the KIAZOP course-fees workbook.")

    # Remove student, employee, account, payment, and centre cashbook records from the
    # public template. Keep formulas, course catalog, layouts, and editable blank rows.
    for name in wb.sheetnames:
        if name.startswith("C") and name[1:].isdigit():
            ws = wb[name]
            for row in range(20, 65):
                for col in list(range(2, 7)) + list(range(10, 16)):
                    cell = ws.cell(row, col)
                    if cell.data_type != "f":
                        cell.value = None
            ws.auto_filter.ref = "B19:S64"
            # Keep the core student-identification columns visible while scrolling.
            if ws.freeze_panes is None:
                ws.freeze_panes = "D20"

    if "FORMADORES" in wb:
        ws = wb["FORMADORES"]
        for row in range(9, 17):
            for col in range(2, 10):
                if ws.cell(row, col).data_type != "f":
                    ws.cell(row, col).value = None
        ws["B7"] = "MAPA DE PAGAMENTOS  ·  PERÍODO EDITÁVEL"
        for col, month in zip(range(5, 9), ["Mês 1", "Mês 2", "Mês 3", "Mês 4"]):
            ws.cell(8, col, month)
        ws.auto_filter.ref = "B8:L16"
        ws.freeze_panes = "B9"

    if "SAIDAS" in wb:
        ws = wb["SAIDAS"]
        for row in range(9, 26):
            for col in range(2, 8):
                if ws.cell(row, col).data_type != "f":
                    ws.cell(row, col).value = None
        for cell, label in zip([f"B{r}" for r in range(30, 34)], ["Mês 1", "Mês 2", "Mês 3", "Mês 4"]):
            ws[cell] = label
        ws.auto_filter.ref = "B8:H25"
        ws.freeze_panes = "B9"

    if "ENTRADAS" in wb:
        ws = wb["ENTRADAS"]
        for row in range(9, 34):
            for col in range(2, 7):
                if ws.cell(row, col).data_type != "f":
                    ws.cell(row, col).value = None
        for cell, label in zip([f"B{r}" for r in range(38, 42)], ["Mês 1", "Mês 2", "Mês 3", "Mês 4"]):
            ws[cell] = label
        ws.auto_filter.ref = "B8:H33"
        ws.freeze_panes = "B9"

    if "FUNDO" in wb:
        ws = wb["FUNDO"]
        ws["C9"] = None
        for row, label in zip(range(13, 17), ["Mês 1", "Mês 2", "Mês 3", "Mês 4"]):
            ws.cell(row, 2, label)

    if "DIVIDAS" in wb:
        ws = wb["DIVIDAS"]
        for row in range(9, 36):
            for col in range(2, 5):
                if ws.cell(row, col).data_type != "f":
                    ws.cell(row, col).value = None
        for row in range(40, 45):
            for col in range(2, 7):
                if ws.cell(row, col).data_type != "f":
                    ws.cell(row, col).value = None
        for row, label in zip(range(40, 45), ["Mês 1", "Mês 1", "Mês 1", "Mês 2", "Mês 3"]):
            ws.cell(row, 2, label)
        ws.auto_filter.ref = "B8:H35"
        ws.freeze_panes = "B9"

    if "HISTORICO" in wb:
        ws = wb["HISTORICO"]
        for row in range(8, 308):
            for col in range(3, 12):
                if ws.cell(row, col).data_type != "f":
                    ws.cell(row, col).value = None
        ws.auto_filter.ref = "B7:K307"
        ws.freeze_panes = "C8"

    if "RECIBO" in wb:
        wb["RECIBO"]["C7"] = None

    # The source cover said it was password-protected; this edition opens without a password.
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for cell in row:
                if isinstance(cell.value, str) and "ACESSO PROTEGIDO" in cell.value.upper():
                    cell.value = "FICHEIRO SEM SENHA  ·  MODELO EDITÁVEL"

    # Replace the stale example month names with reusable period labels.
    month_labels = {"Maio": "Mês 1", "Junho": "Mês 2", "Julho": "Mês 3", "Agosto": "Mês 4"}
    for name in ("SAIDAS", "ENTRADAS", "FUNDO", "DIVIDAS"):
        if name in wb:
            ws = wb[name]
            for row in ws.iter_rows():
                for cell in row:
                    if isinstance(cell.value, str) and cell.value in month_labels:
                        cell.value = month_labels[cell.value]

    # Explain the template state and privacy handling in the original user guide.
    manual = wb["MANUAL"]
    manual["B15"] = "9. Proteção e dados pessoais"
    manual["C15"] = "Esta cópia abre sem senha e os registos pessoais/financeiros de exemplo foram removidos. Antes de inserir dados reais, guarde uma cópia de segurança e proteja a sua cópia de trabalho."
    for row_num, title, note in [
        (16, "10. Períodos editáveis", "Nas folhas de caixa e formadores, actualize os cabeçalhos Mês 1 a Mês 4 para os períodos que vai controlar."),
        (17, "11. Recalcular o painel", "Abra no Excel com cálculo automático activo. O painel, totais, recibos e relatórios actualizam a partir dos registos preenchidos."),
    ]:
        for col in (2, 3):
            src = manual.cell(15, col)
            dest = manual.cell(row_num, col)
            if src.has_style:
                dest._style = copy(src._style)
            if src.number_format:
                dest.number_format = src.number_format
            if src.alignment:
                dest.alignment = copy(src.alignment)
            if src.font:
                dest.font = copy(src.font)
            if src.fill:
                dest.fill = copy(src.fill)
            if src.border:
                dest.border = copy(src.border)
        manual.cell(row_num, 2, title)
        manual.cell(row_num, 3, note)
        manual.row_dimensions[row_num].height = 42
    manual.print_area = "B1:C17"

    # Improve first-use behaviour and ensure Excel refreshes the existing 10k+ formulas.
    wb.calculation.calcMode = "auto"
    wb.calculation.fullCalcOnLoad = True
    wb.calculation.forceFullCalc = True
    wb.properties.title = "Sistema de Propinas KIAZOP — Modelo sem senha"
    wb.properties.subject = "Cursos, turmas, matrículas, propinas, recibos e caixa do centro de formação"
    wb.save(OUTPUT)
    print(f"Saved unlocked, privacy-cleaned product workbook: {OUTPUT.relative_to(ROOT)}")
finally:
    decrypted_path.unlink(missing_ok=True)
