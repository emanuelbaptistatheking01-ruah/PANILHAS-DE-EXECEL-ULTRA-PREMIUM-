#!/usr/bin/env python3
"""Product detail page template — one per spreadsheet."""
from html import escape

from catalog_theme import BASE_CSS, FOOT_CSS, NAV_CSS, BRAND, footer, mobile_nav_css, nav


def _money(v: int) -> str:
    return format(v, ",").replace(",", ".")


PROD_CSS = NAV_CSS + FOOT_CSS + """
/* ---------- product hero ---------- */
.phero{position:relative;overflow:hidden;background:#082a1a;color:#f2eee0;padding:38px 0 46px}
.phero-bg{position:absolute;inset:0;background:radial-gradient(ellipse 58% 100% at 90% -24%,rgba(25,76,52,.40),transparent 62%),linear-gradient(165deg,#0a2b1b,#04140c)}
.phero-in{position:relative}
.crumbs{display:flex;align-items:center;gap:9px;font-size:11.5px;letter-spacing:.05em;color:#8fa89a;margin-bottom:22px}
.crumbs a{text-decoration:none;color:#cddbc8}
.crumbs a:hover{color:var(--gold-3)}
.crumbs span{color:#5f7a6b}
.phero h1{font-family:var(--serif);font-weight:600;font-size:clamp(29px,3.6vw,44px);line-height:1.1;letter-spacing:-.02em;margin:12px 0 14px;max-width:24ch}
.phero p{max-width:64ch;margin:0;color:#b9cbc0;font-size:15px;line-height:1.74}
.phero-tags{display:flex;flex-wrap:wrap;gap:8px;margin-top:22px}
.phero-tags span{font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--gold-3);border:1px solid rgba(232,217,176,.28);border-radius:99px;padding:5px 11px}
/* ---------- layout ---------- */
.pmain{display:grid;grid-template-columns:1.62fr .88fr;gap:44px;align-items:start;padding:46px 0 20px}
.pblock{background:var(--surface);border:1px solid var(--line);border-radius:14px;overflow:hidden;box-shadow:0 1px 0 #fff inset,0 2px 4px rgba(var(--shadow),.04),0 22px 44px -30px rgba(var(--shadow),.9)}
.pblock-im{display:flex;align-items:center;justify-content:center;padding:26px;background:radial-gradient(ellipse at 50% 0%,#fdfbf4,var(--surface-2) 62%,#ece4d0)}
.pblock-im img{width:100%;height:auto;filter:drop-shadow(0 1px 2px rgba(20,40,28,.10)) drop-shadow(0 14px 24px rgba(20,40,28,.16))}
.caption{margin:0;padding:13px 18px;border-top:1px solid var(--line-soft);font-size:11.5px;color:var(--muted);background:#fdfbf3;letter-spacing:.01em}
/* ---------- buy panel ---------- */
.buy-card{position:sticky;top:96px;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:26px 24px;box-shadow:0 1px 0 #fff inset,0 2px 4px rgba(var(--shadow),.04),0 22px 44px -30px rgba(var(--shadow),.9)}
.buy-card .eyebrow{margin-bottom:10px}
.price{font-family:var(--serif);font-size:40px;line-height:1.05;color:var(--green-deep);letter-spacing:-.02em;margin:0}
.price small{font-family:var(--sans);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);display:block;margin-top:8px}
.buy-card .btn{width:100%;justify-content:center;margin-top:20px;font-size:13.5px;padding:14px 18px}
.buy-note{font-size:11.5px;line-height:1.6;color:var(--muted);margin:12px 0 0;text-align:center}
.buy-list{list-style:none;margin:22px 0 0;padding:22px 0 0;border-top:1px solid var(--line-soft);display:grid;gap:10px}
.buy-list li{display:flex;gap:9px;font-size:12.5px;line-height:1.55;color:var(--ink-soft)}
.buy-list li::before{content:"✓";flex:0 0 17px;height:17px;display:grid;place-items:center;border-radius:50%;background:#eaf1e2;color:var(--green);font-size:10px;font-weight:700;margin-top:2px}
/* ---------- sections ---------- */
.psec{padding:44px 0}
.psec h2{font-size:clamp(21px,2.2vw,27px);line-height:1.2;margin:0 0 20px}
.steps-list{counter-reset:st;list-style:none;margin:0;padding:0;display:grid;gap:0}
.steps-list li{counter-increment:st;position:relative;padding:16px 0 16px 46px;border-bottom:1px solid var(--line-soft);font-size:13.8px;line-height:1.7;color:var(--ink-soft)}
.steps-list li:last-child{border-bottom:0}
.steps-list li::before{content:counter(st,decimal-leading-zero);position:absolute;left:0;top:16px;font-family:var(--serif);font-size:12px;color:var(--gold);border:1px solid var(--gold-3);border-radius:5px;padding:2px 7px}
.note-box{display:flex;gap:14px;align-items:flex-start;background:#f6f2e5;border:1px solid var(--line);border-left:3px solid var(--gold-2);border-radius:10px;padding:18px 20px;font-size:12.8px;line-height:1.7;color:var(--ink-soft)}
.note-box b{color:var(--ink)}
.note-box i{font-style:normal;color:var(--gold);font-size:15px;line-height:1.3}
.related{padding:44px 0 64px}
.mini-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}
.mini{display:flex;gap:13px;align-items:center;background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:11px;text-decoration:none;transition:border-color .2s,transform .2s,box-shadow .2s}
.mini:hover{border-color:var(--gold-3);transform:translateY(-2px);box-shadow:0 12px 24px -20px rgba(var(--shadow),.9)}
.mi{flex:0 0 88px;height:60px;display:flex;align-items:center;justify-content:center;background:var(--surface-2);border-radius:6px;overflow:hidden;padding:5px}
.mi img{max-width:100%;max-height:100%;object-fit:contain}
.mb{display:flex;flex-direction:column;gap:2px;min-width:0}
.mb strong{font-size:12.5px;line-height:1.35;color:var(--ink);font-weight:700}
.mb span{font-family:var(--serif);font-size:13px;color:var(--green)}
.mb em{font-style:normal;font-size:10.5px;color:var(--gold);letter-spacing:.04em}
@media(max-width:980px){
  .pmain{grid-template-columns:1fr;gap:28px}
  .buy-card{position:static;order:-1}
}
@media(max-width:640px){
  .mini-grid{grid-template-columns:1fr}
  .phero{padding:26px 0 34px}
  .pblock-im{padding:16px}
}
"""


def build_product(i, p, price, wa, steps, related, img_w, img_h):
    steps_html = "\n".join(f"<li>{escape(s)}</li>" for s in steps)
    rel_html = "\n".join(related)
    return f"""<!doctype html>
<html lang="pt-AO"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#082a1a">
<title>{escape(p['title'])} — Planilha Excel · {BRAND['name']}</title>
<meta name="description" content="{escape(p['description'], quote=True)} Pré-visualização da folha real, entrega pelo WhatsApp por {price} Kz.">
<meta property="og:title" content="{escape(p['title'])} — Planilha Excel">
<meta property="og:description" content="{escape(p['description'], quote=True)}">
<style>{BASE_CSS}{PROD_CSS}{mobile_nav_css()}</style></head>
<body>
{nav('../')}
<header class="phero">
  <div class="phero-bg" aria-hidden="true"></div>
  <div class="wrap phero-in">
    <div class="crumbs"><a href="../index.html">Início</a><span>/</span><a href="../index.html#planilhas">Planilhas</a><span>/</span><span>{escape(p['tag'])}</span></div>
    <h1>{escape(p['title'])}</h1>
    <p>{escape(p['description'])}</p>
    <div class="phero-tags"><span>Planilha #{i:02d}</span><span>{escape(p['tag'])}</span><span>Ficheiro .xlsx</span><span>{escape(p['sheet'])}</span></div>
  </div>
</header>

<main class="wrap">
  <div class="pmain">
    <section class="pblock">
      <div class="pblock-im"><img src="../{escape(p['preview'])}" alt="Pré-visualização real da folha {escape(p['sheet'])} da planilha {escape(p['title'])}" width="{img_w}" height="{img_h}" decoding="async" fetchpriority="high"></div>
      <p class="caption">Pré-visualização da folha original — aba “{escape(p['sheet'])}” da planilha {escape(p['title'])}.</p>
    </section>

    <aside class="buy-card">
      <span class="eyebrow">Preço único</span>
      <p class="price">{price} Kz<small>Ficheiro .xlsx completo</small></p>
      <a class="btn btn-green" href="../oferta/{i}.html">Comprar agora <span aria-hidden="true">→</span></a>
      <p class="buy-note" style="margin-top:9px">Página de compra com entrega imediata no WhatsApp.</p>
      <p class="buy-note">Resposta habitual em poucos minutos, dentro do horário de atendimento.</p>
      <ul class="buy-list">
        <li>Ficheiro Excel (.xlsx) entregue na conversa</li>
        <li>Guia de utilização em português</li>
        <li>Fórmulas nativas — sem macros</li>
        <li>Valores e parâmetros em Kwanzas</li>
        <li>7 dias de suporte directo comigo</li>
      </ul>
    </aside>
  </div>

  <section class="psec">
    <h2>Como usar esta planilha</h2>
    <ol class="steps-list">
{steps_html}
    </ol>
  </section>

  <section class="psec">
    <div class="note-box"><i>◆</i><div><b>Como recebe o ficheiro:</b> não há download no site. Ao confirmar a compra no WhatsApp, envio o ficheiro .xlsx na própria conversa, com as instruções de utilização e os primeiros campos já preenchidos como exemplo.</div></div>
  </section>

  <section class="related">
    <h2>Outras planilhas</h2>
    <div class="mini-grid">
{rel_html}
    </div>
  </section>
</main>
{footer('../')}
</body></html>"""
