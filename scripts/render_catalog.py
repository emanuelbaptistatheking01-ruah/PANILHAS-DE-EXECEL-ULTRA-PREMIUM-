#!/usr/bin/env python3
"""Render representative, original worksheet previews and build the static catalog."""
from pathlib import Path
from html import escape
from xml.etree import ElementTree as ET
from zipfile import ZipFile
import hashlib
import re
import unicodedata
import io
import urllib.parse

import sys

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
PREVIEWS = PUBLIC / "previews"
PREVIEWS.mkdir(parents=True, exist_ok=True)
WA_NUMBER = "244942739225"
VERSION = "9"
SITE_HOST = "https://planilhas-ultra-angola-emanuelbaptistatheking01-9378.vercel.app"
NS = {
    "m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


def wa_link(i, p, price):
    """WhatsApp deep link with the product photo, price and product page link."""
    image_url = f"{SITE_HOST}/{p['preview']}"
    product_url = f"{SITE_HOST}/produtos/{i}.html"
    text = (
        f"Olá! Tenho interesse na planilha {p['title']}.\n"
        f"Preço: {price} Kz.\n"
        f"📷 Foto: {image_url}\n"
        f"🔗 Ver a planilha: {product_url}"
    )
    return f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(text, safe='')}"

PRODUCTS = [
    dict(file="01-Folha-de-Salario-Angola/Folha_de_Salario_Angola_12000Kz.xlsx", sheet="Folha", title="Folha de Salário Angola", price=12000, description="Feche a folha salarial com mais organização e menos contas manuais. Registe a equipa e obtenha cálculos de INSS, IRT e salário líquido, com parâmetros editáveis e resumo para conferência.", tag="Recursos Humanos"),
    dict(file="02-Gestao-Empresarial/Gestao_Empresarial_Caixa_Stock_15000Kz.xlsx", sheet="Dashboard", title="Gestão Empresarial: Caixa, Stock e Vendas", price=15000, description="Tenha compras, vendas e stock sob controlo sem folhas dispersas. Veja produtos a repor e acompanhe os resultados do negócio num dashboard fácil de consultar.", tag="Gestão de Negócios"),
    dict(file="03-Calculadora-de-Impostos-Angola/Calculadora_Impostos_Angola_10000Kz.xlsx", sheet="IVA", title="Calculadora de Impostos Angola", price=10000, description="Perceba o impacto dos impostos antes de fechar as contas. Simule IVA, Imposto Industrial e retenções na fonte, ajuste as taxas e teste cenários de preço num só ficheiro.", tag="Impostos"),
    dict(file="04-Contabilidade-SNC-Completa/Contabilidade_SNC_Completa_20000Kz.xlsx", sheet="Plano de Contas", title="Contabilidade SNC Completa", price=20000, description="Dê estrutura aos registos contabilísticos da sua empresa. Organize contas e lançamentos, confira débitos e créditos e prepare DRE e balanço com apoio de cálculos automáticos.", tag="Contabilidade"),
    dict(file="05-Diario-de-Controle-de-Obra/Diario_de_Controle_de_Obra_8000Kz.xlsx", sheet="Diário", title="Diário de Controle de Obra", price=8000, description="Saiba o que aconteceu em cada dia da obra. Registe actividades, clima, ocorrências, presenças e materiais recebidos; consulte um resumo mensal para acompanhar a execução.", tag="Construção"),
    dict(file="06-Orcamento-de-Obra-Materiais/Orcamento_de_Obra_Materiais_12000Kz.xlsx", sheet="Orçamento", title="Orçamento de Obra + Materiais", price=12000, description="Prepare propostas de obra com mais clareza: estime materiais pela área, some serviços e mão-de-obra e veja o custo directo e o BDI organizados no orçamento.", tag="Construção"),
    dict(file="07-Comparador-de-Precos-Fornecedores/Comparador_Precos_Fornecedores_6000Kz.xlsx", sheet="Cotações", title="Comparador de Preços de Fornecedores", price=6000, description="Poupe tempo ao decidir onde comprar. Compare preços de até quatro fornecedores lado a lado, identifique a melhor cotação por produto e consulte o ranking de fornecedores.", tag="Compras"),
    dict(file="08-Financas-Pessoais-Angola/Financas_Pessoais_Angola_8000Kz.xlsx", sheet="Dashboard", title="Finanças Pessoais Angola", price=8000, description="Saia do fim do mês sem saber para onde foi o dinheiro. Registe entradas e despesas, acompanhe dívidas e metas e visualize saldo e poupança com a regra 50/30/20.", tag="Finanças Pessoais"),
    dict(file="09-Planner-de-Habitos-Devocional/Planner_Habitos_Devocional_5000Kz.xlsx", sheet="Hábitos", title="Planner de Hábitos e Devocional", price=5000, description="Transforme intenção em rotina, um dia de cada vez. Marque hábitos durante 31 dias, registe leituras e reflexões e acompanhe metas e progresso pessoal.", tag="Organização Pessoal"),
    dict(file="10-Custos-de-Receitas-Angolanas/Custos_Receitas_Angolanas_7000Kz.xlsx", sheet="Receitas", title="Custos de Receitas Angolanas", price=7000, description="Saiba quanto cada prato realmente custa antes de definir o preço. Registe ingredientes, calcule o custo por receita e por porção e consulte preços de venda sugeridos.", tag="Restauração"),
    dict(file="11-Centro-de-Formacao-Tecnico-Profissional/Gestao_Centro_Formacao_Tecnico_Profissional_25000Kz.xlsx", sheet="Cursos", title="Gestão de Centro de Formação Técnico-Profissional", price=25000, description="Deixe de controlar o centro em folhas separadas. Organize cursos, formandos, matrículas, propinas e pagamentos; acompanhe presenças, notas e certificados num único ficheiro, com painel automático. Os cursos e preços de exemplo são editáveis.", tag="Formação Profissional"),
    dict(file="12-Centro-de-Formacao-KIAZOP/KIAZOP_Sistema_Propinas_35000Kz.xlsx", sheet="CURSOS", start_column=2, title="Sistema de Propinas KIAZOP", price=35000, description="Gerencie 26 cursos, turmas, matrículas e cobranças num sistema integrado. Consulte recibos, dívidas e relatórios; organize salas, formadores e o caixa do centro. Esta edição abre sem senha e foi limpa de registos pessoais de exemplo.", tag="Gestão de Formação"),
    dict(file="13-Escola-Gestao-de-Escola/Gestao_Escola_25000Kz.xlsx", sheet="Alunos", title="Gestão de Escola", price=25000, description="Gestão escolar completa para directores e secretarias: alunos, turmas, professores, disciplinas, frequência e notas num só ficheiro, com painel de indicadores.", tag="Educação"),
    dict(file="14-Escola-Controle-de-Alunos-e-Notas/Controle_Alunos_Notas_12000Kz.xlsx", sheet="Notas", title="Controle de Alunos e Notas", price=12000, description="Tenha o cadastro de alunos, notas e frequência organizado. Acompanhe o desempenho por turma e disciplina e identifique alunos com dificuldades antes da reunião de pais.", tag="Educação"),
    dict(file="15-Escola-Cobranca-de-Mensalidade-Escolar/Cobranca_Mensalidade_Escolar_10000Kz.xlsx", sheet="Mensalidades", title="Cobrança de Mensalidade Escolar", price=10000, description="Cobre mensalidades sem confusão. Registe mensalidades, recebimentos, atrasos e emissão de recibos e acompanhe a receita da escola.", tag="Educação"),
    dict(file="16-Centro-Controle-de-Presenca-de-Formandos/Controle_Presenca_Formandos_8000Kz.xlsx", sheet="Presença", title="Controle de Presença de Formandos", price=8000, description="Controle de presença de formandos por turma e módulo. Marque presença diariamente, consulte resumos por curso e identifique faltas acumuladas.", tag="Formação Profissional"),
    dict(file="17-Centro-Gestao-de-Certificates/Gestao_Certificates_10000Kz.xlsx", sheet="Certificates", title="Gestão de Certificates", price=10000, description="Emitir e validar certificados com confiança. Organize a base de dados de certificados, emissão, validade e consulta por número de certificado.", tag="Formação Profissional"),
    dict(file="18-Centro-Controle-de-Salas-e-Horarios/Controle_Salas_Horarios_8000Kz.xlsx", sheet="Reservas", title="Controle de Salas e Horários", price=8000, description="Otimize a ocupação das salas do centro. Defina horários e salas, registre reservas e evite conflitos de uso entre turmas e formadores.", tag="Formação Profissional"),
]

STEPS = [
    ["Abra a folha no Excel e seleccione o mês de processamento.",
     "Registe os colaboradores e introduza os valores salariais e dados do período.",
     "Confira INSS, IRT, descontos e salário líquido antes de fechar a folha."],
    ["Cadastre os produtos, preços e stock inicial.",
     "Registe compras e vendas à medida que acontecem.",
     "Acompanhe caixa, stock baixo e indicadores no painel."],
    ["Introduza os valores da operação ou do rendimento a analisar.",
     "Confira ou ajuste as taxas aplicáveis no ficheiro.",
     "Compare o cálculo e valide as taxas legais em vigor antes de tomar decisões."],
    ["Configure o plano de contas da empresa.",
     "Registe cada movimento nas contas correspondentes.",
     "Confira o equilíbrio dos lançamentos e consulte os relatórios financeiros."],
    ["Abra o diário e escolha a data da actividade.",
     "Registe trabalhos, clima, ocorrências, equipa e materiais recebidos.",
     "Consulte o resumo mensal para acompanhar a execução da obra."],
    ["Introduza área, quantidades e elementos do projecto.",
     "Adicione materiais, serviços, mão-de-obra e os parâmetros de BDI.",
     "Confira os custos calculados e prepare a proposta para o cliente."],
    ["Adicione os produtos ou serviços que pretende comprar.",
     "Registe as cotações de até quatro fornecedores por produto.",
     "Compare os valores e use o ranking para apoiar a escolha."],
    ["Defina o saldo inicial e as suas metas financeiras.",
     "Registe cada rendimento e despesa na categoria correspondente.",
     "Acompanhe o saldo, as dívidas e a distribuição mensal do orçamento."],
    ["Escolha os hábitos que quer acompanhar e defina a sua rotina.",
     "Marque o progresso diariamente ao longo do mês.",
     "Registe a leitura e as reflexões no espaço devocional."],
    ["Cadastre os ingredientes e os respectivos preços de compra.",
     "Indique as quantidades usadas em cada receita.",
     "Confira custo por receita e por porção antes de definir o preço de venda."],
    ["Configure cursos, turmas, formadores e propinas.",
     "Registe formandos, matrículas, presenças, notas e pagamentos.",
     "Acompanhe o painel e consulte os dados para recibos e certificados."],
    ["Configure cursos, turmas, salas e formadores do centro.",
     "Registe matrículas e acompanhe cobranças e pagamentos.",
     "Consulte recibos, dívidas, relatórios e movimento de caixa."],
    ["Abra a planilha e personalize a escola, o ano letivo e o período no Painel.",
     "Cadastre alunos, turmas, professores e disciplinas nas folhas correspondentes.",
     "Acompanhe frequência e notas e consulte o Painel de indicadores antes das reuniões de pais."],
    ["Cadastre os alunos e as turmas no início do período letivo.",
     "Registe as notas e a frequência por disciplina e aluno.",
     "Consulte médias, aprovações e alunos com dificuldades no Resumo."],
    ["Cadastre alunos, cursos e os valores das mensalidades.",
     "Registe cada recebimento e acompanhe os atrasos por aluno.",
     "Emitir recibos e consultar a receita no Resumo da escola."],
    ["Configure cursos, turmas, formadores e períodos.",
     "Registe a presença diária por formando.",
     "Consulte os resumos por turma e identifique as faltas acumuladas."],
    ["Cadastre os cursos, módulos e formandos habilitados.",
     "Registe a emissão dos certificados com data e validade.",
     "Valide certificados pelo número e consulte o resumo da base."],
    ["Cadastre as salas, capacidades e restrições de uso.",
     "Defina os horários e registe as reservas por turma ou curso.",
     "Consulte a ocupação das salas e evite conflitos de agenda."],
]

def col_num(ref):
    letters = re.match(r"[A-Z]+", ref or "")
    n = 0
    for c in (letters.group(0) if letters else "A"):
        n = n * 26 + ord(c) - 64
    return n

def color_from(color, fallback):
    if color is None:
        return fallback
    rgb = color.attrib.get("rgb")
    if rgb:
        return "#" + rgb[-6:]
    indexed = color.attrib.get("indexed")
    return {"8": "#000000", "9": "#ffffff", "10": "#ff0000", "11": "#00ff00", "12": "#0000ff", "13": "#ffff00"}.get(indexed, fallback)

def preview_name(product):
    slug = unicodedata.normalize("NFKD", product["title"].lower()).encode("ascii", "ignore").decode("ascii")
    filename = re.sub(r"[^a-z0-9]+", "-", slug).strip("-") + ".png"
    return "previews/" + filename


def preview_dimensions(preview_rel):
    """Return the real pixel size of a preview so <img> has an aspect ratio."""
    try:
        from PIL import Image

        with Image.open(ROOT / "public" / preview_rel) as im:
            return im.size
    except Exception:
        return (900, 420)


def thumb_name(preview_rel):
    return preview_rel.replace("previews/", "previews/thumbs/").replace(".png", ".webp")


def make_thumb(preview_rel):
    """Build a light WebP thumbnail for catalog cards.

    Cards render the preview at roughly 340px wide, so shipping the full
    PNG there wasted bandwidth and left cards blank for seconds on slow
    mobile connections. The product page keeps the full-resolution PNG.
    """
    from PIL import Image

    src = ROOT / "public" / preview_rel
    dst = ROOT / "public" / thumb_name(preview_rel)
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
        return thumb_name(preview_rel)
    with Image.open(src) as im:
        im = im.convert("RGB")
        w, h = im.size
        if w > 720:
            im = im.resize((720, max(1, round(h * 720 / w))), Image.LANCZOS)
        im.save(dst, "WEBP", quality=82, method=6)
    return thumb_name(preview_rel)


def preview_src(preview_rel, prefix=""):
    """Return the preview URL with a content hash query string.

    The hash busts stale browser/CDN caches. Earlier visits cached 404s for
    several previews (the files did not exist yet), and browsers keep serving
    an errored image until the URL changes, which left cards without photos.
    """
    path = ROOT / "public" / preview_rel
    try:
        digest = hashlib.sha1(path.read_bytes()).hexdigest()[:10]
    except OSError:
        digest = VERSION
    return f"{prefix}{preview_rel}?v={digest}"


def make_preview(product):
    """Render a spreadsheet-style preview PNG for a workbook product.

    Uses svglib/reportlab when available; falls back to a Pillow renderer so the
    site can be rebuilt on machines without the heavy rendering dependencies.
    """
    try:
        _make_preview_svg(product)
    except ImportError:
        _make_preview_pil(product)


def _make_preview_svg(product):
    from reportlab.graphics import renderPDF
    from svglib.svglib import svg2rlg
    import pymupdf
    path = PUBLIC / product["file"]
    with ZipFile(path) as z:
        workbook = ET.fromstring(z.read("xl/workbook.xml"))
        rels_xml = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        rels = {x.attrib["Id"]: x.attrib["Target"] for x in rels_xml}
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            strings = ET.fromstring(z.read("xl/sharedStrings.xml"))
            shared = ["".join(t.text or "" for t in si.findall(".//m:t", NS)) for si in strings.findall("m:si", NS)]
        styles = ET.fromstring(z.read("xl/styles.xml"))
        fills = styles.find("m:fills", NS)
        fonts = styles.find("m:fonts", NS)
        xfs = styles.find("m:cellXfs", NS)
        fill_defs = list(fills) if fills is not None else []
        font_defs = list(fonts) if fonts is not None else []
        xf_defs = list(xfs) if xfs is not None else []
        sheets = workbook.findall("m:sheets/m:sheet", NS)
        sheet_names = [s.attrib["name"] for s in sheets]
        selected = next((s for s in sheets if s.attrib["name"] == product["sheet"]), sheets[0])
        target = rels[selected.attrib["{" + NS["r"] + "}id"]].lstrip("/")
        target = target if target.startswith("xl/") else "xl/" + target
        sheet = ET.fromstring(z.read(target))

        max_cols, max_rows = 8, 10
        start_col = int(product.get("start_column", 1))
        start_col0 = start_col - 1
        row_nodes = [r for r in sheet.findall("m:sheetData/m:row", NS) if int(r.attrib.get("r", "1")) <= max_rows]
        cells = {}
        for row in row_nodes:
            r_idx = int(row.attrib.get("r", "1")) - 1
            for c in row.findall("m:c", NS):
                ref = c.attrib.get("r", "A1")
                ci = col_num(ref) - start_col
                if ci < 0 or ci >= max_cols:
                    continue
                value = ""
                v = c.find("m:v", NS)
                inline = c.find("m:is", NS)
                if v is not None:
                    value = shared[int(v.text)] if c.attrib.get("t") == "s" and v.text else v.text or ""
                elif inline is not None:
                    value = "".join(t.text or "" for t in inline.findall(".//m:t", NS))
                value = str(value).replace("\n", " ").replace("\r", " ")
                cells[(r_idx, ci)] = (value, int(c.attrib.get("s", "0")))

        merged_starts, merged_covered = {}, set()
        for merge in sheet.findall("m:mergeCells/m:mergeCell", NS):
            first, last = merge.attrib["ref"].split(":")
            r1, r2 = int(re.search(r"\d+", first).group()) - 1, int(re.search(r"\d+", last).group()) - 1
            c1, c2 = col_num(first) - 1, col_num(last) - 1
            ri, ci = r1, c1 - start_col0
            if 0 <= ri < max_rows and 0 <= ci < max_cols:
                rowspan = min(max_rows - ri, r2 - r1 + 1)
                colspan = min(max_cols - ci, c2 - c1 + 1)
                merged_starts[(ri, ci)] = (rowspan, colspan)
                for mr in range(ri, ri + rowspan):
                    for mc in range(ci, ci + colspan):
                        if (mr, mc) != (ri, ci):
                            merged_covered.add((mr, mc))

        col_widths = [112] * max_cols
        cols = sheet.find("m:cols", NS)
        if cols is not None:
            for item in cols:
                lo, hi = int(item.attrib.get("min", 1)) - 1, int(item.attrib.get("max", 1))
                width = max(70, min(176, int(float(item.attrib.get("width", 16)) * 7)))
                for abs_ci in range(lo, hi):
                    ci = abs_ci - start_col0
                    if 0 <= ci < max_cols:
                        col_widths[ci] = width
        row_heights = [34] * max_rows
        for row in row_nodes:
            ri = int(row.attrib.get("r", "1")) - 1
            row_heights[ri] = max(27, min(52, int(float(row.attrib.get("ht", 24)) * 1.35)))

        margin, top = 32, 72
        width = margin * 2 + sum(col_widths)
        height = top + sum(row_heights) + 74
        out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
               '<defs><filter id="shadow" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#12251c" flood-opacity=".12"/></filter></defs>',
               f'<rect width="{width}" height="{height}" rx="18" fill="#f4f6f5"/>',
               f'<rect x="12" y="12" width="{width-24}" height="{height-24}" rx="12" fill="#fff" filter="url(#shadow)"/>',
               '<circle cx="36" cy="37" r="5" fill="#ff6b65"/><circle cx="54" cy="37" r="5" fill="#ffc24d"/><circle cx="72" cy="37" r="5" fill="#44c78a"/>',
               f'<text x="{width/2}" y="42" text-anchor="middle" font-family="Arial,sans-serif" font-size="13" fill="#718078">Microsoft Excel  •  {escape(product["title"])}</text>',
               f'<rect x="{margin}" y="58" width="{sum(col_widths)}" height="{sum(row_heights)}" fill="#fff" stroke="#cbd5cf" stroke-width="1"/>']
        x_positions = [margin]
        for cw in col_widths:
            x_positions.append(x_positions[-1] + cw)
        y_positions = [top]
        for rh in row_heights:
            y_positions.append(y_positions[-1] + rh)
        for ri in range(max_rows):
            for ci in range(max_cols):
                if (ri, ci) in merged_covered:
                    continue
                value, style_i = cells.get((ri, ci), ("", 0))
                xf = xf_defs[style_i] if style_i < len(xf_defs) else None
                fill = "#ffffff"
                font_color, bold, italic = "#26352e", False, False
                font_size = 13
                if xf is not None:
                    fi = int(xf.attrib.get("fillId", 0))
                    if fi < len(fill_defs):
                        fg = fill_defs[fi].find("m:patternFill/m:fgColor", NS)
                        pattern = fill_defs[fi].find("m:patternFill", NS)
                        if fg is not None and pattern is not None and pattern.attrib.get("patternType"):
                            fill = color_from(fg, fill)
                    fni = int(xf.attrib.get("fontId", 0))
                    if fni < len(font_defs):
                        fd = font_defs[fni]
                        font_color = color_from(fd.find("m:color", NS), font_color)
                        bold = fd.find("m:b", NS) is not None
                        italic = fd.find("m:i", NS) is not None
                        sz = fd.find("m:sz", NS)
                        if sz is not None:
                            font_size = max(10, min(16, int(float(sz.attrib.get("val", 11)))))
                rowspan, colspan = merged_starts.get((ri, ci), (1, 1))
                x, y = x_positions[ci], y_positions[ri]
                cw = sum(col_widths[ci:ci+colspan])
                rh = sum(row_heights[ri:ri+rowspan])
                out.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{rh}" fill="{fill}" stroke="#d9e0dc" stroke-width="1"/>')
                if value:
                    align = "center" if colspan > 1 or rowspan > 1 else "start"
                    if xf is not None:
                        al = xf.find("m:alignment", NS)
                        if al is not None and al.attrib.get("horizontal") in ("center", "right"):
                            align = al.attrib["horizontal"]
                    tx = x + 8 if align == "start" else (x + cw / 2 if align == "center" else x + cw - 8)
                    anchor = "start" if align == "start" else "middle" if align == "center" else "end"
                    max_chars = max(3, int((cw - 16) / (font_size * 0.58)))
                    safe = escape(value[:max_chars]) + ("…" if len(value) > max_chars else "")
                    out.append(f'<text x="{tx}" y="{y+rh/2+4}" text-anchor="{anchor}" font-family="Arial,sans-serif" font-size="{font_size}px" font-weight="{700 if bold else 400}" font-style="{"italic" if italic else "normal"}" fill="{font_color}">{safe}</text>')
        tab_y = y_positions[-1] + 20
        cursor = margin
        for name in sheet_names:
            tw = max(72, min(142, len(name) * 8 + 24))
            active = name == product["sheet"]
            out.append(f'<rect x="{cursor}" y="{tab_y}" width="{tw}" height="28" rx="5" fill="{"#e9f4ed" if active else "#f5f7f6"}" stroke="{"#85b99a" if active else "#e1e6e3"}"/>')
            out.append(f'<text x="{cursor+tw/2}" y="{tab_y+18}" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" font-weight="{"700" if active else "400"}" fill="{"#17633c" if active else "#77827c"}">{escape(name[:18])}</text>')
            cursor += tw + 6
            if cursor > width - 72:
                break
        out.append('</svg>')
    product["preview"] = preview_name(product)
    drawing = svg2rlg(io.StringIO("\n".join(out)))
    pdf = renderPDF.drawToString(drawing)
    doc = pymupdf.open(stream=pdf, filetype="pdf")
    pixmap = doc[0].get_pixmap(matrix=pymupdf.Matrix(1.5, 1.5), alpha=False)
    (PUBLIC / product["preview"]).write_bytes(pixmap.tobytes("png"))


def _make_preview_pil(product):
    """Render a vivid, high-resolution spreadsheet preview (2x supersampled)."""
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    from openpyxl import load_workbook
    from openpyxl.utils import get_column_letter

    # Renders at 2x then downsamples: crisp text and smooth shadows.
    SS = 2

    def px(v):
        return int(round(v * SS))

    FONT_DIRS = ["/usr/share/fonts/truetype/dejavu/", "/usr/share/fonts/truetype/liberation/"]
    def load_font(size, bold=True):
        names = ["DejaVuSans-Bold.ttf"] if bold else ["DejaVuSans.ttf"]
        if bold:
            names.insert(0, "DejaVuSans-Bold.ttf")
        for d in FONT_DIRS:
            for n in names:
                try:
                    return ImageFont.truetype(d + n, px(size))
                except OSError:
                    continue
        return ImageFont.load_default()

    # ---- premium palette ----------------------------------------------
    DEEP      = (9, 52, 32)        # header base
    EMERALD   = (28, 107, 65)      # header highlight
    MINT      = (233, 247, 224)    # soft cell tint
    GOLD      = (201, 162, 39)
    GOLD_L    = (230, 207, 139)
    INK       = (24, 42, 32)
    GRID      = (222, 231, 224)
    WHITE     = (255, 255, 255)
    CANVAS_A  = (245, 240, 226)
    CANVAS_B  = (237, 230, 212)

    path = PUBLIC / product["file"]
    wb = load_workbook(path, data_only=True)
    ws = wb[product["sheet"]]

    # Trim to the columns/rows that actually carry data.
    used_cols, used_rows = 0, 0
    for row in ws.iter_rows(min_row=1, max_row=4 + 20, max_col=20):
        for cell in row:
            if cell.value is not None and str(cell.value).strip() != "":
                used_cols = max(used_cols, cell.column)
                used_rows = max(used_rows, cell.row)
    n_cols = max(4, min(10, used_cols))
    data_start = 5                      # row 4 is the column-header row
    filled = 0
    for r in range(data_start, data_start + 20):
        # A row counts only if it carries real content beyond the row-number column.
        if any(str(ws.cell(r, c).value or "").strip() for c in range(2, n_cols + 1)):
            filled = r - data_start + 1
        elif filled:
            break
    n_rows = max(3, min(9, filled or 3))

    col_widths = []
    for idx in range(1, n_cols + 1):
        dim = ws.column_dimensions.get(get_column_letter(idx))
        width = dim.width if dim is not None and dim.width else 12
        col_widths.append(max(112, min(250, int(width * 8) + 16)))
    row_heights = []
    for r in range(data_start, data_start + n_rows):
        dim = ws.row_dimensions.get(r)
        height = dim.height if dim is not None and dim.height else 22
        row_heights.append(max(40, min(72, int(height) + 16)))

    margin, top, header_h = 34, 86, 48
    sheet_w = margin * 2 + sum(col_widths)
    sheet_h = top + header_h + sum(row_heights)
    pad = 30
    tabs_h = 44
    img_w = sheet_w
    img_h = sheet_h + pad * 2 + tabs_h + 10

    # ---- canvas with a soft warm gradient -----------------------------
    img = Image.new("RGB", (px(img_w), px(img_h)), CANVAS_A)
    d = ImageDraw.Draw(img)
    for yy in range(px(img_h)):
        t = yy / max(1, px(img_h))
        c = tuple(round(CANVAS_A[i] + (CANVAS_B[i] - CANVAS_A[i]) * t) for i in range(3))
        d.line([(0, yy), (px(img_w), yy)], fill=c)

    # ---- floating sheet: drop shadow then rounded card -----------------
    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle(
        [px(pad + 8), px(pad + 18), px(pad + sum(col_widths) - 8), px(sheet_h + pad + 6)],
        radius=px(16), fill=(28, 52, 36, 78))
    shadow = shadow.filter(ImageFilter.GaussianBlur(px(9)))
    img.paste(shadow, (0, 0), shadow)

    d.rounded_rectangle([px(pad), px(pad), px(pad + sum(col_widths)), px(sheet_h + pad)],
                        radius=px(18), fill=WHITE)
    # hairline border
    d.rounded_rectangle([px(pad), px(pad), px(pad + sum(col_widths)), px(sheet_h + pad)],
                        radius=px(18), outline=(216, 210, 190), width=px(1))

    # ---- title bar: emerald gradient + gold hairline ------------------
    bar_x0, bar_y0 = px(pad), px(pad)
    bar_x1, bar_y1 = px(pad + sum(col_widths)), px(pad + 62)
    grad = Image.new("RGB", (max(1, bar_x1 - bar_x0), max(1, bar_y1 - bar_y0)), DEEP)
    gd = ImageDraw.Draw(grad)
    for xx in range(bar_x1 - bar_x0):
        t = xx / max(1, bar_x1 - bar_x0)
        c = tuple(round(DEEP[i] + (EMERALD[i] - DEEP[i]) * t * 0.85) for i in range(3))
        gd.line([(xx, 0), (xx, bar_y1 - bar_y0)], fill=c)
    mask = Image.new("L", grad.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, grad.size[0] - 1, grad.size[1] - 1],
                                           radius=px(18), fill=255)
    # square off the bottom corners so it meets the sheet edge
    ImageDraw.Draw(mask).rectangle([0, grad.size[1] - px(20), grad.size[0], grad.size[1]], fill=255)
    img.paste(grad, (bar_x0, bar_y0), mask)

    # window dots
    for i, col in enumerate([(255, 107, 101), (255, 194, 77), (68, 199, 138)]):
        cx = bar_x0 + px(26 + i * 22)
        cy = bar_y0 + px(31)
        d.ellipse([cx - px(6), cy - px(6), cx + px(6), cy + px(6)], fill=col)

    # gold hairline under the bar
    d.rectangle([bar_x0, bar_y1 - px(2), bar_x1, bar_y1], fill=GOLD_L)

    # title, centred on the bar
    f_title = load_font(17)
    title = f"Microsoft Excel   ·   {product['title']}"
    tw = d.textlength(title, font=f_title)
    max_tw = (bar_x1 - bar_x0) - px(150)
    while tw > max_tw and len(title) > 8:
        title = title[:-2]
        tw = d.textlength(title + "…", font=f_title)
    if not title.endswith("…") and d.textlength(title + "…", font=f_title) > max_tw:
        title += "…"
    d.text(((bar_x0 + bar_x1 - tw) / 2, bar_y0 + px(20)), title, font=f_title,
           fill=(233, 247, 224))

    # ---- header row: emerald gradient cell by cell -------------------
    headers = [str(ws.cell(4, c).value or "") for c in range(1, n_cols + 1)]
    f_head = load_font(13)
    x = margin
    for cw, text in zip(col_widths, headers):
        hx0, hy0 = px(x), px(top)
        hx1, hy1 = px(x + cw), px(top + header_h)
        grad = Image.new("RGB", (max(1, hx1 - hx0), max(1, hy1 - hy0)), EMERALD)
        gd = ImageDraw.Draw(grad)
        for yy in range(hy1 - hy0):
            t = yy / max(1, hy1 - hy0)
            c = tuple(round(EMERALD[i] + ((16, 74, 46)[i] - EMERALD[i]) * t) for i in range(3))
            gd.line([(0, yy), (hx1 - hx0, yy)], fill=c)
        img.paste(grad, (hx0, hy0))
        if text:
            t = text
            while d.textlength(t, font=f_head) > (hx1 - hx0) - px(18) and len(t) > 3:
                t = t[:-1]
            if t != text:
                t += "…"
            tw = d.textlength(t, font=f_head)
            d.text((hx0 + ((hx1 - hx0) - tw) / 2, hy0 + (hy1 - hy0 - px(18)) / 2),
                   t, font=f_head, fill=WHITE)
        x += cw

    # ---- data rows: zebra tint + vivid source fills -------------------
    f_cell = load_font(12, bold=False)
    f_bold = load_font(12, bold=True)
    y = top + header_h
    for ri, rh in enumerate(row_heights):
        row_idx = data_start + ri
        x = margin
        for ci, cw in enumerate(col_widths, 1):
            cell = ws.cell(row_idx, ci)
            value = cell.value
            fill_color = MINT if ri % 2 else WHITE
            bold = False
            try:
                fc = cell.fill
                if fc and fc.fill_type == "solid" and fc.fgColor and fc.fgColor.rgb:
                    rgb = fc.fgColor.rgb
                    if isinstance(rgb, str) and len(rgb) >= 6 and rgb[-6:] not in ("FFFFFF", "000000"):
                        fill_color = "#" + rgb[-6:]
            except Exception:
                pass
            try:
                bold = bool(cell.font and cell.font.bold)
            except Exception:
                pass

            cx0, cy0 = px(x), px(y)
            cx1, cy1 = px(x + cw), px(y + rh)
            d.rectangle([cx0, cy0, cx1, cy1], fill=fill_color)
            d.line([(cx0, cy1), (cx1, cy1)], fill=GRID, width=px(1))
            d.line([(cx1, cy0), (cx1, cy1)], fill=GRID, width=px(1))

            if value is not None and not (isinstance(value, str) and value.startswith("=")):
                text = str(value)
                if isinstance(value, float):
                    text = f"{value:,.2f}".replace(",", " ").replace(".", ",")
                elif isinstance(value, int):
                    text = f"{value:,}".replace(",", " ")
                font = f_bold if bold else f_cell
                avail = (cx1 - cx0) - px(18)
                if d.textlength(text, font=font) > avail:
                    while text and d.textlength(text + "…", font=font) > avail:
                        text = text[:-1]
                    text += "…"
                d.text((cx0 + px(9), cy0 + (cy1 - cy0 - px(17)) / 2), text,
                       font=font, fill=INK)
            x += cw
        y += rh

    # ---- sheet tabs ---------------------------------------------------
    tab_y = sheet_h + pad + 2
    cursor = margin
    f_tab = load_font(12, bold=True)
    for name in wb.sheetnames[:9]:
        tw = max(96, min(180, len(name) * 10 + 34))
        active = name == product["sheet"]
        tx0, ty0 = px(cursor), px(tab_y)
        tx1, ty1 = px(cursor + tw), px(tab_y + 34)
        if active:
            d.rounded_rectangle([tx0, ty0, tx1, ty1], radius=px(9), fill=EMERALD)
            d.rounded_rectangle([tx0, ty0, tx1, ty1], radius=px(9),
                                outline=GOLD, width=px(1))
            col = WHITE
        else:
            d.rounded_rectangle([tx0, ty0, tx1, ty1], radius=px(9), fill=(252, 250, 243))
            d.rounded_rectangle([tx0, ty0, tx1, ty1], radius=px(9),
                                outline=(222, 214, 194), width=px(1))
            col = (108, 106, 90)
        t = name[:18]
        while d.textlength(t, font=f_tab) > (tx1 - tx0) - px(16) and len(t) > 3:
            t = t[:-1]
        twn = d.textlength(t, font=f_tab)
        d.text((tx0 + ((tx1 - tx0) - twn) / 2, ty0 + ((ty1 - ty0) - px(17)) / 2),
               t, font=f_tab, fill=col)
        cursor += tw + 9
        if cursor > sheet_w - 90:
            break

    # ---- downsample for crisp anti-aliased output ---------------------
    out = img.resize((img_w, img_h), Image.LANCZOS)
    out.save(PUBLIC / product["preview"], "PNG", optimize=True)


SKIP_PREVIEWS = "--skip-previews" in sys.argv
FORCE_PREVIEWS = "--force-previews" in sys.argv
for product in PRODUCTS:
    product["preview"] = preview_name(product)
if not SKIP_PREVIEWS:
    for product in PRODUCTS:
        path = PUBLIC / product["preview"]
        if path.exists() and not FORCE_PREVIEWS:
            continue
        make_preview(product)

cards = []
for i, p in enumerate(PRODUCTS, 1):
    page = escape(f"produtos/{i}.html", quote=True)
    price = format(p["price"], ",").replace(",", ".")
    wa = wa_link(i, p, price)
    thumb_rel = make_thumb(p["preview"])
    pw, ph = preview_dimensions(thumb_rel)
    cards.append(f'''<article class="card">
      <a class="preview" href="{page}" aria-label="Ver detalhes da planilha {escape(p['title'])}"><img src="{escape(preview_src(thumb_rel))}" alt="Pré-visualização real da folha {escape(p['sheet'])} da planilha {escape(p['title'])}" width="{pw}" height="{ph}" decoding="async" fetchpriority="{'high' if i <= 3 else 'auto'}" onerror="this.closest('.preview').classList.add('noimg');this.remove()"><span class="zoom">Pré-visualização da folha original</span><span class="fallback">Pré-visualização indisponível — toque para ver os detalhes</span></a>
      <div class="card-body"><div class="meta"><span class="tag">{escape(p['tag'])}</span><span class="number">#{i:02d}</span></div>
      <h2><a href="{page}">{escape(p['title'])}</a></h2><p>{escape(p['description'])}</p>
      <div class="buy"><strong>{price} Kz</strong><div class="buy-actions"><a class="button wa-mini" href="{wa}">WhatsApp <span aria-hidden="true">↗</span></a><a class="button" href="{page}">Ver detalhes <span aria-hidden="true">→</span></a></div></div></div>
    </article>''')

html = '''<!doctype html>
<html lang="pt-AO"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#08281a"><meta name="description" content="Planilhas Excel Premium para negócios, finanças, construção e formação profissional em Angola. Veja imagens originais, preços em Kz e baixe directamente."><title>Planilhas Excel Premium — Angola</title>
<style>
:root{color-scheme:light;--ink:#12241b;--ink-soft:#3f5348;--muted:#58665c;--line:#e8e0cc;--line-strong:#d8ceb4;--gold:#c9a227;--gold-soft:#e6cf8b;--green:#14532f;--green-deep:#0b3320;--green-mid:#1c6b41;--lime:#c8ee79;--lime-bright:#dcf9a0;--paper:#f7f3e8;--surface:#fffdf7;--surface-2:#f2ecdc;--surface-3:#ece4cf;--shadow:34 52 40}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif}.hero{position:relative;overflow:hidden;background:radial-gradient(ellipse 60% 120% at 88% -25%,#2fa06a 0,transparent 58%),radial-gradient(ellipse 55% 110% at 6% 130%,#25895b 0,transparent 55%),radial-gradient(ellipse 90% 80% at 50% 120%,#0f5a38 0,transparent 60%),linear-gradient(160deg,#0e4529 0%,#0a3220 48%,#072619 100%);color:#fdfbf4;padding:52px max(24px,calc((100% - 1160px)/2)) 54px}.topline{display:flex;align-items:center;gap:10px;color:var(--lime-bright);font-size:12px;font-weight:800;letter-spacing:.13em;text-transform:uppercase}.dot{height:8px;width:8px;border-radius:50%;background:var(--lime-bright);box-shadow:0 0 16px var(--lime-bright),0 0 34px rgb(200 238 121/.5)}.hero::before{content:"";position:absolute;inset:0;background:radial-gradient(ellipse 42% 70% at 78% 6%,rgb(220 249 160/.16),transparent 70%);pointer-events:none}.hero::after{content:"";position:absolute;inset:0 0 auto;height:1px;background:linear-gradient(90deg,transparent,rgb(230 207 139/.55) 22%,rgb(230 207 139/.75) 50%,rgb(230 207 139/.55) 78%,transparent);pointer-events:none}.hero h1{text-shadow:0 2px 30px rgb(220 249 160/.18);max-width:740px;font-size:clamp(36px,6vw,64px);line-height:1.02;letter-spacing:-.055em;margin:22px 0 16px}.hero h1 span{color:var(--lime)}.hero p{max-width:650px;color:#c8d6c9;line-height:1.7;font-size:16px;margin:0}.download-all{display:inline-flex;align-items:center;gap:8px;margin-top:18px;padding:11px 16px;border-radius:9px;background:linear-gradient(180deg,var(--lime-bright),#b6e35d);color:#12351f;border:1px solid #a5d64f;box-shadow:0 1px 0 rgb(255 255 255/.5) inset,0 6px 16px -6px rgb(0 0 0/.5);font-size:12px;font-weight:800;text-decoration:none}.download-all:hover{filter:brightness(1.06);transform:translateY(-1px)}.hero-foot{display:flex;gap:18px;align-items:center;margin-top:28px;color:#bfd0c2;font-size:13px}.hero-foot b{color:#fdfbf4}.wrap{max-width:1160px;margin:0 auto;padding:34px 24px 64px}.section-head{display:flex;justify-content:space-between;align-items:end;gap:20px;margin:6px 0 22px}.section-head h2{font-size:25px;letter-spacing:-.04em;margin:0}.section-head p{margin:0;color:var(--muted);font-size:13px}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px}.card{position:relative;background:var(--surface);border:1px solid var(--line);border-radius:20px;overflow:hidden;box-shadow:0 1px 1px rgb(var(--shadow)/.05),0 3px 6px -2px rgb(var(--shadow)/.08),0 12px 22px -8px rgb(var(--shadow)/.16),0 30px 56px -22px rgb(var(--shadow)/.30);transition:transform .3s cubic-bezier(.2,.8,.3,1),box-shadow .3s ease,border-color .3s ease}.card::before{content:"";position:absolute;inset:0 0 auto;height:1px;background:linear-gradient(90deg,transparent,rgb(255 255 255/.9) 18%,rgb(255 255 255/.95) 50%,rgb(255 255 255/.9) 82%,transparent);z-index:3}.card::after{content:"";position:absolute;inset:0 0 auto;height:3px;background:linear-gradient(90deg,transparent,rgb(201 162 39/.75) 25%,rgb(230 207 139/.95) 50%,rgb(201 162 39/.75) 75%,transparent);opacity:0;transition:opacity .3s;z-index:3}.card:hover::after{opacity:1}.card:hover{transform:translateY(-10px) scale(1.012);border-color:var(--gold-soft);box-shadow:0 2px 3px rgb(var(--shadow)/.06),0 6px 12px -3px rgb(var(--shadow)/.10),0 22px 38px -12px rgb(var(--shadow)/.26),0 52px 84px -30px rgb(var(--shadow)/.42)}.preview{height:258px;display:flex;position:relative;align-items:center;justify-content:center;overflow:hidden;background:radial-gradient(ellipse at 50% 0%,#fbf7ea 0,var(--surface-2) 55%,var(--surface-3) 100%);box-shadow:inset 0 -18px 26px -22px rgb(34 52 40/.35),inset 0 1px 0 rgb(255 255 255/.7);padding:18px}.preview img{display:block;width:100%;height:100%;object-fit:contain;filter:drop-shadow(0 2px 4px rgb(20 40 28/.10)) drop-shadow(0 12px 22px rgb(20 40 28/.16));transition:filter .3s,transform .3s}.card:hover .preview img{filter:drop-shadow(0 3px 6px rgb(20 40 28/.12)) drop-shadow(0 18px 32px rgb(20 40 28/.22));transform:scale(1.025)}.preview .fallback{display:none}.preview.noimg .fallback{display:block;position:absolute;inset:0;align-content:center;text-align:center;padding:18px;color:#53645a;font-size:12px;font-weight:650;line-height:1.5;background:var(--surface-2);z-index:1}.preview.noimg .zoom{display:none}.zoom{position:absolute;bottom:12px;right:12px;background:rgb(255 253 247/.92);color:#4f4736;border:1px solid var(--line-strong);border-radius:99px;font-size:10px;padding:6px 9px;backdrop-filter:blur(8px)}.card-body{padding:19px 20px 18px}.meta{display:flex;justify-content:space-between;align-items:center}.tag{border-radius:99px;background:linear-gradient(180deg,#f4f8ec,#e9f2dc);border:1px solid #dcd9c0;color:#1d5c37;padding:5px 9px;font-size:10px;font-weight:750}.number{font-size:11px;color:#8f8362;font-weight:750}.card h2{font-size:20px;line-height:1.2;letter-spacing:-.035em;margin:12px 0 8px}.card h2 a{color:inherit;text-decoration:none}.card h2 a:hover{color:var(--green-mid)}.card p{min-height:46px;color:var(--muted);font-size:13px;line-height:1.55;margin:0}.buy{display:flex;align-items:center;justify-content:space-between;border-top:1px solid var(--line);margin-top:15px;padding-top:14px}.buy strong{font-size:19px;letter-spacing:-.03em;color:var(--green-deep)}.buy-actions{display:flex;gap:8px}.button{background:linear-gradient(180deg,var(--green-mid),var(--green-deep));color:#fdfbf4;text-decoration:none;font-weight:750;font-size:12px;padding:10px 14px;border-radius:9px;border:1px solid #0e4526;box-shadow:0 1px 0 rgb(255 255 255/.14) inset,0 4px 10px -3px rgb(var(--shadow)/.4);transition:filter .18s,transform .18s}.button:hover{filter:brightness(1.14);transform:translateY(-1px)}.button span{margin-left:6px;font-size:15px}.button.wa-mini{background:linear-gradient(180deg,var(--lime-bright),#b6e35d);color:#12351f;padding:8px 12px;font-size:11px;border:1px solid #a5d64f;box-shadow:0 1px 0 rgb(255 255 255/.45) inset,0 4px 10px -4px rgb(var(--shadow)/.35)}.button.wa-mini:hover{filter:brightness(1.05);transform:translateY(-1px)}.note{margin-top:27px;padding:16px 18px;border:1px solid var(--line);border-radius:14px;color:var(--muted);font-size:12px;line-height:1.6;background:var(--surface)}.note strong{color:var(--green)}footer{background:var(--surface);border-top:1px solid var(--line);padding:22px 24px;color:#706a5a;text-align:center;font-size:11px}@media(max-width:720px){.hero{padding-top:38px;padding-bottom:40px}.grid{grid-template-columns:1fr;gap:16px}.preview{height:235px}.section-head{align-items:start;flex-direction:column;gap:6px}.card p{min-height:0}}@media(min-width:1100px){.grid{grid-template-columns:repeat(3,minmax(0,1fr))}.preview{height:220px}}
</style></head><body>
<header class="hero"><div class="topline"><i class="dot"></i> Colecção Excel Premium · Angola</div><h1>Planilhas que fazem<br><span>o trabalho por si.</span></h1><p>Ferramentas prontas para usar no Excel, pensadas para a realidade angolana. Veja a pré-visualização da folha original, consulte o preço e peça a sua planilha directamente no WhatsApp.</p><a class="download-all" href="https://wa.me/244942739225?text=Ol%C3%A1%21%20Tenho%20interesse%20em%20comprar%20planilhas%20Excel%20Premium%20para%20Angola.">↗ Pedir no WhatsApp</a><div class="hero-foot"><span><b>10</b> planilhas disponíveis</span><span>·</span><span>Preços em <b>Kwanzas (Kz)</b></span><span>·</span><span>Ficheiros <b>.xlsx</b> entregues pelo WhatsApp</span></div></header>
<main class="wrap"><div class="section-head"><h2>Escolha a sua planilha</h2><p>Toque em “Ver detalhes” para abrir a página da planilha e pedir pelo WhatsApp.</p></div><div class="grid">''' + "\n".join(cards) + '''</div>
<div class="note"><strong>Nota:</strong> Cada planilha tem uma página própria com a pré-visualização da folha original, o preço e o passo a passo de como usá-la. As planilhas não estão disponíveis para download: ao confirmar a compra no WhatsApp, o ficheiro Excel (.xlsx) é entregue directamente na conversa, junto com as instruções de utilização. As imagens são pré-visualizações das folhas existentes nos próprios ficheiros; os nomes das abas visíveis correspondem à planilha original. Abra com Microsoft Excel ou uma aplicação compatível.</div></main><footer>Planilhas Excel Premium · Feito para Angola · Valores indicados em Kz</footer></body></html>'''
html = html.replace("10</b> planilhas disponíveis", f"{len(PRODUCTS)}</b> planilhas disponíveis")
(PUBLIC / "index.html").write_text(html, encoding="utf-8")

PROD_STYLES = (
    ":root{color-scheme:light;--ink:#12241b;--ink-soft:#3f5348;--muted:#58665c;--line:#e8e0cc;--line-strong:#d8ceb4;--gold:#c9a227;--gold-soft:#e6cf8b;--green:#14532f;--green-deep:#0b3320;--green-mid:#1c6b41;--lime:#c8ee79;--lime-bright:#dcf9a0;--paper:#f7f3e8;--surface:#fffdf7;--surface-2:#f2ecdc;--surface-3:#ece4cf;--shadow:34 52 40}"
    "*{box-sizing:border-box}"
    "body{margin:0;background:var(--paper);color:var(--ink);font-family:Inter,ui-sans-serif,system-ui,-apple-system,\"Segoe UI\",sans-serif}"
    ".hero{position:relative;overflow:hidden;background:radial-gradient(ellipse 60% 120% at 88% -25%,#2fa06a 0,transparent 58%),radial-gradient(ellipse 55% 110% at 6% 130%,#25895b 0,transparent 55%),radial-gradient(ellipse 90% 80% at 50% 120%,#0f5a38 0,transparent 60%),linear-gradient(160deg,#0e4529 0%,#0a3220 48%,#072619 100%);color:#fdfbf4;padding:44px max(24px,calc((100% - 1160px)/2)) 46px}"
    ".topline{display:flex;align-items:center;gap:10px;color:var(--lime-bright);font-size:12px;font-weight:800;letter-spacing:.13em;text-transform:uppercase}"
    ".dot{height:8px;width:8px;border-radius:50%;background:var(--lime-bright);box-shadow:0 0 16px var(--lime-bright),0 0 34px rgb(200 238 121/.5)}.hero::after{content:"";position:absolute;inset:0 0 auto;height:1px;background:linear-gradient(90deg,transparent,rgb(230 207 139/.55) 22%,rgb(230 207 139/.75) 50%,rgb(230 207 139/.55) 78%,transparent);pointer-events:none}"
    ".crumb{display:inline-flex;align-items:center;margin:16px 0 0;color:#bfd0c2;font-size:12px;font-weight:700;text-decoration:none;transition:color .2s}"
    ".crumb:hover{color:#fdfbf4}"
    ".hero h1{max-width:760px;font-size:clamp(30px,5vw,52px);line-height:1.05;letter-spacing:-.045em;margin:14px 0 12px}"
    ".hero p{max-width:650px;color:#c8d6c9;line-height:1.7;font-size:16px;margin:0}"
    ".cta-row{display:flex;gap:12px;flex-wrap:wrap;margin-top:22px}"
    ".button{background:linear-gradient(180deg,var(--green-mid),var(--green-deep));color:#fdfbf4;text-decoration:none;font-weight:750;font-size:12px;padding:12px 16px;border-radius:10px;border:1px solid #0e4526;box-shadow:0 1px 0 rgb(255 255 255/.14) inset,0 5px 14px -4px rgb(var(--shadow)/.45);transition:filter .18s,transform .18s;display:inline-flex;align-items:center;gap:8px}"
    ".button span{margin-left:4px;font-size:15px}"
    ".button.wa{background:linear-gradient(180deg,var(--lime-bright),#b6e35d);color:#12351f;border:1px solid #a5d64f;box-shadow:0 1px 0 rgb(255 255 255/.5) inset,0 6px 16px -6px rgb(0 0 0/.5)}"
    ".button.wa:hover{filter:brightness(1.06);transform:translateY(-1px)}"
    ".hero-foot{display:flex;gap:18px;align-items:center;margin-top:26px;color:#bfd0c2;font-size:13px;flex-wrap:wrap}"
    ".hero-foot b{color:#fdfbf4}"
    ".wrap{max-width:1160px;margin:0 auto;padding:34px 24px 64px}"
    ".preview-block{position:relative;background:var(--surface);border:1px solid var(--line);border-radius:20px;padding:30px;box-shadow:0 1px 1px rgb(var(--shadow)/.05),0 4px 8px -2px rgb(var(--shadow)/.09),0 16px 30px -10px rgb(var(--shadow)/.18),0 40px 70px -28px rgb(var(--shadow)/.34);margin-bottom:40px}"
    ".preview-block img{display:block;width:100%;max-height:540px;object-fit:contain;border-radius:12px;background:linear-gradient(160deg,var(--surface-2),var(--surface-3))}"
    ".caption{margin:14px 0 0;color:var(--muted);font-size:12px;text-align:center}"
    ".steps h2{font-size:24px;letter-spacing:-.035em;margin:0 0 16px}"
    ".steps ol{margin:0;padding-left:22px;color:var(--ink-soft);font-size:14px;line-height:2}"
    ".steps li{margin-bottom:8px}"
    ".steps li::marker{color:var(--green);font-weight:800}"
    ".nota{margin:22px 0 0;padding:16px 18px;border:1px solid var(--line);border-radius:14px;color:var(--muted);font-size:12px;line-height:1.6;background:var(--surface)}"
    ".nota strong{color:var(--green)}"
    ".related{margin-top:44px}"
    ".related h2{font-size:22px;letter-spacing:-.035em;margin:0 0 16px}"
    ".mini-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}"
    ".mini{background:var(--surface);border:1px solid var(--line);border-radius:16px;overflow:hidden;box-shadow:0 1px 1px rgb(var(--shadow)/.05),0 3px 6px -2px rgb(var(--shadow)/.08),0 10px 20px -8px rgb(var(--shadow)/.16),0 22px 40px -18px rgb(var(--shadow)/.26);text-decoration:none;color:inherit;display:flex;transition:transform .2s,box-shadow .2s}"
    ".mini:hover{transform:translateY(-6px);border-color:var(--gold-soft);box-shadow:0 2px 3px rgb(var(--shadow)/.06),0 8px 14px -4px rgb(var(--shadow)/.12),0 22px 38px -14px rgb(var(--shadow)/.26),0 44px 68px -28px rgb(var(--shadow)/.38)}"
    ".mini .mi{width:104px;flex:none;background:linear-gradient(160deg,var(--surface-2),var(--surface-3));display:flex;align-items:center;justify-content:center;height:118px}"
    ".mini .mi img{width:100%;height:100%;object-fit:contain}"
    ".mini .mb{padding:12px 14px;display:flex;flex-direction:column;justify-content:center;gap:5px;min-width:0}"
    ".mini .mb strong{font-size:14px;line-height:1.25}"
    ".mini .mb span{font-size:12px;color:var(--muted)}"
    ".mini .mb em{font-style:normal;font-size:11px;font-weight:700;color:var(--green)}"
    "footer{background:var(--surface);border-top:1px solid var(--line);padding:22px 24px;color:#706a5a;text-align:center;font-size:11px}"
    "@media(max-width:720px){.hero{padding-top:36px;padding-bottom:38px}.mini-grid{grid-template-columns:1fr}.steps ol{font-size:13px;line-height:1.9}}"
)

def build_product_pages():
    (PUBLIC / "produtos").mkdir(parents=True, exist_ok=True)
    for i, p in enumerate(PRODUCTS, 1):
        steps = STEPS[i - 1]
        steps_html = "\n".join(f"      <li>{escape(s)}</li>" for s in steps)
        preview = escape(preview_src(p["preview"], "../"), quote=True)
        pw, ph = preview_dimensions(p["preview"])
        price = format(p["price"], ",").replace(",", ".")
        wa = wa_link(i, p, price)
        rel = []
        for j, q in enumerate(PRODUCTS, 1):
            if j == i or len(rel) == 4:
                continue
            q_price = format(q["price"], ",").replace(",", ".")
            qt = make_thumb(q["preview"])
            qw, qh = preview_dimensions(qt)
            rel.append(
                f'''      <a class="mini" href="{j}.html"><div class="mi"><img src="{escape(preview_src(qt, '../'))}" alt="Pré-visualização da planilha {escape(q['title'])}" width="{qw}" height="{qh}" decoding="async"></div><div class="mb"><strong>{escape(q['title'])}</strong><span>{q_price} Kz</span><em>Ver detalhes →</em></div></a>'''
            )
        page_html = f'''<!doctype html>
<html lang="pt-AO"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#08281a"><meta name="description" content="{escape(p['description'])} Veja a pré-visualização da folha original da planilha {escape(p['title'])} em Excel por {price} Kz. Peça pelo WhatsApp."><title>{escape(p['title'])} — Planilhas Excel Premium Angola</title>
<style>{PROD_STYLES}</style></head>
<body>
<header class="hero"><div class="topline"><i class="dot"></i> Colecção Excel Premium · Angola</div><a class="crumb" href="../index.html">← Ver todas as planilhas</a>
<h1>{escape(p['title'])}</h1>
<p>{escape(p['description'])}</p>
<div class="cta-row"><a class="button wa" href="{wa}">Pedir no WhatsApp <span aria-hidden="true">↗</span></a></div>
<div class="hero-foot"><span><b>{price} Kz</b></span><span>·</span><span>{escape(p['tag'])}</span><span>·</span><span>Planilha #{i:02d}</span><span>·</span><span>Ficheiro <b>.xlsx</b> entregue pelo WhatsApp</span></div></header>
<main class="wrap">
<section class="preview-block"><img src="{preview}" alt="Pré-visualização real da folha {escape(p['sheet'])} da planilha {escape(p['title'])}" width="{pw}" height="{ph}" decoding="async" fetchpriority="high"><p class="caption">Pré-visualização da folha original — aba “{escape(p['sheet'])}” da planilha {escape(p['title'])}.</p></section>
<section class="steps"><h2>Como usar esta planilha</h2>
<ol>
{steps_html}
</ol></section>
<section class="nota"><strong>Como receber a planilha:</strong> ao confirmar a compra no WhatsApp, o ficheiro Excel (.xlsx) é entregue directamente na conversa, junto com as instruções de utilização.</section>
<section class="related"><h2>Outras planilhas</h2><div class="mini-grid">
{chr(10).join(rel)}
</div></section>
</main>
<footer>Planilhas Excel Premium · Feito para Angola · Valores indicados em Kz</footer>
</body></html>'''
        (PUBLIC / "produtos" / f"{i}.html").write_text(page_html, encoding="utf-8")

build_product_pages()
print(f"Generated {len(PRODUCTS)} previews, public/index.html and {len(PRODUCTS)} product pages")
