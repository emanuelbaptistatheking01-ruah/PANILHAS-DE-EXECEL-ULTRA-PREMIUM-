#!/usr/bin/env python3
"""Render representative, original worksheet previews and build the static catalog."""
from pathlib import Path
from html import escape
from xml.etree import ElementTree as ET
from zipfile import ZipFile
import re
import unicodedata
import io

from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
import pymupdf

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
PREVIEWS = PUBLIC / "previews"
PREVIEWS.mkdir(parents=True, exist_ok=True)
NS = {
    "m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}

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

def make_preview(product):
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
    slug = unicodedata.normalize("NFKD", product["title"].lower()).encode("ascii", "ignore").decode("ascii")
    filename = re.sub(r"[^a-z0-9]+", "-", slug).strip("-") + ".png"
    product["preview"] = "previews/" + filename
    drawing = svg2rlg(io.StringIO("\n".join(out)))
    pdf = renderPDF.drawToString(drawing)
    doc = pymupdf.open(stream=pdf, filetype="pdf")
    pixmap = doc[0].get_pixmap(matrix=pymupdf.Matrix(1.5, 1.5), alpha=False)
    (PUBLIC / product["preview"]).write_bytes(pixmap.tobytes("png"))

for product in PRODUCTS:
    make_preview(product)

cards = []
for i, p in enumerate(PRODUCTS, 1):
    download = escape(p["file"], quote=True)
    cards.append(f'''<article class="card">
      <a class="preview" href="{download}" download aria-label="Baixar {escape(p['title'])} em Excel"><img src="{escape(p['preview'])}" alt="Pré-visualização real da folha {escape(p['sheet'])} da planilha {escape(p['title'])}" loading="lazy"><span class="zoom">Pré-visualização da folha original</span></a>
      <div class="card-body"><div class="meta"><span class="tag">{escape(p['tag'])}</span><span class="number">#{i:02d}</span></div>
      <h2>{escape(p['title'])}</h2><p>{escape(p['description'])}</p>
      <div class="buy"><strong>{format(p['price'], ',').replace(',', '.')} Kz</strong><a class="button" href="{download}" download>Baixar Excel <span aria-hidden="true">↓</span></a></div></div>
    </article>''')

html = '''<!doctype html>
<html lang="pt-AO"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#10291e"><meta name="description" content="Planilhas Excel Premium para negócios, finanças, construção e formação profissional em Angola. Veja imagens originais, preços em Kz e baixe directamente."><title>Planilhas Excel Premium — Angola</title>
<style>
:root{color-scheme:light;--ink:#14281e;--muted:#697970;--line:#e5ebe7;--green:#17633c;--lime:#c8ee79;--paper:#f6f8f5}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif}.hero{background:radial-gradient(ellipse at 85% 0%,#28563d 0,transparent 35%),#10291e;color:#fff;padding:52px max(24px,calc((100% - 1160px)/2)) 54px}.topline{display:flex;align-items:center;gap:10px;color:#c8ee79;font-size:12px;font-weight:800;letter-spacing:.13em;text-transform:uppercase}.dot{height:8px;width:8px;border-radius:50%;background:#c8ee79;box-shadow:0 0 14px #c8ee79}.hero h1{max-width:740px;font-size:clamp(36px,6vw,64px);line-height:1.02;letter-spacing:-.055em;margin:22px 0 16px}.hero h1 span{color:var(--lime)}.hero p{max-width:650px;color:#d1ddd5;line-height:1.7;font-size:16px;margin:0}.download-all{display:inline-flex;align-items:center;gap:8px;margin-top:18px;padding:10px 14px;border-radius:8px;background:#c8ee79;color:#163a2a;font-size:12px;font-weight:800;text-decoration:none}.download-all:hover{background:#d8f6a1}.hero-foot{display:flex;gap:18px;align-items:center;margin-top:28px;color:#d6e2d9;font-size:13px}.hero-foot b{color:white}.wrap{max-width:1160px;margin:0 auto;padding:34px 24px 64px}.section-head{display:flex;justify-content:space-between;align-items:end;gap:20px;margin:6px 0 22px}.section-head h2{font-size:25px;letter-spacing:-.04em;margin:0}.section-head p{margin:0;color:var(--muted);font-size:13px}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px}.card{background:white;border:1px solid var(--line);border-radius:16px;overflow:hidden;box-shadow:0 7px 24px #14322108;transition:transform .2s,box-shadow .2s}.card:hover{transform:translateY(-3px);box-shadow:0 15px 32px #14322112}.preview{height:258px;display:flex;position:relative;align-items:center;justify-content:center;overflow:hidden;background:#edf1ee;padding:18px}.preview img{display:block;width:100%;height:100%;object-fit:contain;filter:drop-shadow(0 4px 10px #203c2c16)}.zoom{position:absolute;bottom:12px;right:12px;background:#ffffffdd;color:#53645a;border:1px solid #e4ebe6;border-radius:99px;font-size:10px;padding:6px 9px;backdrop-filter:blur(8px)}.card-body{padding:19px 20px 18px}.meta{display:flex;justify-content:space-between;align-items:center}.tag{border-radius:99px;background:#eef6ed;color:#24653f;padding:5px 9px;font-size:10px;font-weight:750}.number{font-size:11px;color:#a2aca6;font-weight:750}.card h2{font-size:20px;line-height:1.2;letter-spacing:-.035em;margin:12px 0 8px}.card p{min-height:46px;color:#68766e;font-size:13px;line-height:1.55;margin:0}.buy{display:flex;align-items:center;justify-content:space-between;border-top:1px solid #edf0ee;margin-top:15px;padding-top:14px}.buy strong{font-size:19px;letter-spacing:-.03em}.button{background:var(--green);color:white;text-decoration:none;font-weight:700;font-size:12px;padding:10px 14px;border-radius:8px;transition:background .15s}.button:hover{background:#0e4f2e}.button span{margin-left:6px;font-size:15px}.note{margin-top:27px;padding:16px 18px;border:1px solid #e2eae3;border-radius:12px;color:#66756b;font-size:12px;line-height:1.6;background:#fff}.note strong{color:#2d4637}footer{background:#fff;border-top:1px solid var(--line);padding:22px 24px;color:#7a877f;text-align:center;font-size:11px}@media(max-width:720px){.hero{padding-top:38px;padding-bottom:40px}.grid{grid-template-columns:1fr;gap:16px}.preview{height:235px}.section-head{align-items:start;flex-direction:column;gap:6px}.card p{min-height:0}}@media(min-width:1100px){.grid{grid-template-columns:repeat(3,minmax(0,1fr))}.preview{height:220px}}
</style></head><body>
<header class="hero"><div class="topline"><i class="dot"></i> Colecção Excel Premium · Angola</div><h1>Planilhas que fazem<br><span>o trabalho por si.</span></h1><p>Ferramentas prontas para usar no Excel, pensadas para a realidade angolana. Veja a pré-visualização da folha original, consulte o preço e descarregue directamente o ficheiro.</p><a class="download-all" href="imagens-planilhas-para-site.zip" download>↓ Baixar as 12 imagens PNG (ZIP)</a><div class="hero-foot"><span><b>10</b> planilhas disponíveis</span><span>·</span><span>Preços em <b>Kwanzas (Kz)</b></span><span>·</span><span>Ficheiros <b>.xlsx</b></span></div></header>
<main class="wrap"><div class="section-head"><h2>Escolha a sua planilha</h2><p>Toque em “Baixar Excel” para descarregar o ficheiro original.</p></div><div class="grid">''' + "\n".join(cards) + '''</div>
<div class="note"><strong>Nota:</strong> Os botões descarregam directamente os ficheiros Excel (.xlsx) incluídos nesta colecção. As imagens são pré-visualizações das folhas existentes nos próprios ficheiros; os nomes das abas visíveis correspondem à planilha original. Abra com Microsoft Excel ou uma aplicação compatível.</div></main><footer>Planilhas Excel Premium · Feito para Angola · Valores indicados em Kz</footer></body></html>'''
html = html.replace("10</b> planilhas disponíveis", f"{len(PRODUCTS)}</b> planilhas disponíveis")
(PUBLIC / "index.html").write_text(html, encoding="utf-8")
print(f"Generated {len(PRODUCTS)} previews and public/index.html")
