#!/usr/bin/env python3
"""Home page: a professional one-page structure for Manuel Baptista Licanga."""
from html import escape

from catalog_theme import (
    BASE_CSS, FOOT_CSS, NAV_CSS, BRAND, footer, head, mobile_nav_css,
)


def _money(v: int) -> str:
    return format(v, ",").replace(",", ".")


def category_rows(products):
    """Group products by tag so the catalogue reads as a curated library."""
    groups = {}
    for i, p in enumerate(products, 1):
        groups.setdefault(p["tag"], []).append((i, p))
    order = sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    out = []
    for tag, items in order:
        titles = "".join(f"<li>{escape(p['title'])}</li>" for _, p in items)
        nums = "".join(f'<a href="#planilhas" aria-label="{escape(p["title"])}"></a>' for _, p in items)
        out.append(
            f'<article class="cat"><div class="cat-hd"><span class="cat-n">{len(items)}</span>'
            f'<h3>{escape(tag)}</h3></div><ul>{titles}</ul>'
            f'<a class="cat-l" href="#planilhas">Ver planilhas →</a></article>'
        )
    return "\n".join(out)


HOME_CSS = NAV_CSS + FOOT_CSS + """
/* ---------------- hero ---------------- */
.hero{position:relative;overflow:hidden;background:#082a1a;color:#f3efe2;padding:76px 0 84px}
.hero-bg{position:absolute;inset:0;background:
   radial-gradient(ellipse 66% 84% at 86% -14%,rgba(26,78,53,.40) 0,transparent 64%),
   radial-gradient(ellipse 58% 76% at -8% 108%,rgba(19,62,42,.34) 0,transparent 62%),
   linear-gradient(168deg,#0a2b1b 0%,#072116 54%,#04120b 100%)}
.hero-bg::after{content:"";position:absolute;inset:0;opacity:.42;
   background-image:linear-gradient(rgba(232,217,176,.032) 1px,transparent 1px),linear-gradient(90deg,rgba(232,217,176,.032) 1px,transparent 1px);
   background-size:74px 74px;mask-image:radial-gradient(ellipse 70% 70% at 60% 30%,#000 10%,transparent 78%)}
.hero-in{position:relative;display:grid;grid-template-columns:1.06fr .94fr;gap:62px;align-items:center}
.hero-eyebrow{display:inline-flex;align-items:center;gap:10px;font-size:10.5px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:var(--gold-3)}
.hero-eyebrow i{width:6px;height:6px;border-radius:50%;background:var(--gold-2);box-shadow:0 0 0 3px rgba(205,174,108,.16)}
.hero h1{font-family:var(--serif);font-weight:600;font-size:clamp(38px,4.6vw,60px);line-height:1.06;letter-spacing:-.025em;margin:20px 0 20px;max-width:17ch}
.hero h1 em{font-style:normal;color:var(--gold-3);position:relative;white-space:nowrap}
.hero h1 em::after{content:"";position:absolute;left:0;right:0;bottom:.06em;height:2px;background:linear-gradient(90deg,var(--gold-2),transparent)}
.hero-lead{max-width:52ch;color:#bfcfc5;font-size:16.5px;line-height:1.72;margin:0}
.hero-cta{display:flex;flex-wrap:wrap;gap:12px;margin-top:30px}
.hero-stats{display:flex;flex-wrap:wrap;gap:0;margin-top:42px;border-top:1px solid rgba(232,217,176,.16);padding-top:24px}
.hero-stats div{padding-right:30px;margin-right:30px;border-right:1px solid rgba(232,217,176,.14)}
.hero-stats div:last-child{border:0;margin:0;padding:0}
.hero-stats b{display:block;font-family:var(--serif);font-size:26px;font-weight:600;color:#f6f1e2;line-height:1.1}
.hero-stats span{font-size:11px;letter-spacing:.11em;text-transform:uppercase;color:#8fa89a}
/* mock spreadsheet card in hero */
.hero-visual{position:relative}
.sheet-shell{position:relative;border-radius:14px;overflow:hidden;background:#0e1a13;border:1px solid rgba(232,217,176,.2);box-shadow:0 1px 2px rgba(0,0,0,.28),0 18px 40px -20px rgba(0,0,0,.62),0 44px 78px -46px rgba(0,0,0,.72);transform:perspective(1500px) rotateY(-4deg) rotateX(1.2deg)}
.sheet-top{display:flex;align-items:center;gap:7px;padding:10px 13px;background:linear-gradient(180deg,#16412b,#0e2f1f);border-bottom:1px solid rgba(232,217,176,.18)}
.sheet-top i{width:8px;height:8px;border-radius:50%;background:#3f6b51}
.sheet-top i:nth-child(1){background:#c96b5a}
.sheet-top i:nth-child(2){background:#d4a94a}
.sheet-top i:nth-child(3){background:#5fa87a}
.sheet-top em{margin-left:8px;font-style:normal;font-size:10px;letter-spacing:.13em;text-transform:uppercase;color:#a8bfae}
.sheet-body{background:#fffdf7;padding:0}
.sheet-body svg{display:block;width:100%;height:auto}
.hero-badge{position:absolute;right:14px;bottom:-26px;background:var(--surface);color:var(--ink);border:1px solid var(--line);border-radius:12px;padding:13px 16px;display:flex;align-items:center;gap:11px;box-shadow:0 1px 0 #fff inset,0 18px 34px -18px rgba(0,0,0,.6);max-width:230px;z-index:2}
.hero-badge b{font-family:var(--serif);font-size:15px;line-height:1.2;display:block}
.hero-badge span{font-size:10.5px;color:var(--muted);letter-spacing:.02em}
.hero-badge i{width:34px;height:34px;flex:0 0 34px;display:grid;place-items:center;border-radius:9px;background:linear-gradient(155deg,#1f6b45,#0b3320);color:var(--gold-3);font-style:normal;font-size:15px}
/* ---------------- trust strip ---------------- */
.strip{background:var(--surface-2);border-bottom:1px solid var(--line)}
.strip-in{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:18px;padding:16px 0;font-size:12px;letter-spacing:.05em;color:var(--ink-soft)}
.strip-in span{display:inline-flex;align-items:center;gap:8px}
.strip-in b{color:var(--green);font-weight:700}
.strip-in i{color:var(--gold);font-style:normal}
/* ---------------- generic section ---------------- */
.sec{padding:78px 0}
.sec-alt{background:var(--surface-2);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.sec-head{max-width:660px;margin-bottom:44px}
.sec-head h2{font-size:clamp(28px,3.1vw,40px);line-height:1.12;margin:16px 0 14px}
.sec-head p{margin:0;color:var(--muted);font-size:15.5px;line-height:1.72}
.sec-head.center{margin-left:auto;margin-right:auto;text-align:center}
.sec-head.center .eyebrow{justify-content:center}
.sec-head.center .eyebrow::before{display:none}
/* ---------------- services ---------------- */
.svc-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.svc{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:26px 24px;box-shadow:0 1px 0 #fff inset,0 10px 24px -20px rgba(var(--shadow),.8);transition:transform .25s,box-shadow .25s,border-color .25s}
.svc:hover{transform:translateY(-4px);border-color:var(--gold-3);box-shadow:0 1px 0 #fff inset,0 22px 40px -26px rgba(var(--shadow),.9)}
.svc-no{font-size:11px;font-weight:700;letter-spacing:.16em;color:var(--gold);text-transform:uppercase}
.svc h3{font-size:19px;margin:11px 0 9px;line-height:1.28}
.svc p{margin:0;font-size:13.5px;line-height:1.68;color:var(--muted)}
/* ---------------- catalogue ---------------- */
.cat-strip{display:flex;flex-wrap:wrap;gap:9px;margin-bottom:26px}
.cat-pill{font-size:11.5px;font-weight:600;color:var(--ink-soft);background:var(--surface);border:1px solid var(--line);border-radius:99px;padding:7px 14px;letter-spacing:.02em}
.cat-pill b{color:var(--green);margin-left:5px}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px}
.card{position:relative;display:flex;flex-direction:column;background:var(--surface);border:1px solid var(--line);border-radius:14px;overflow:hidden;box-shadow:0 1px 0 #fff inset,0 1px 2px rgba(var(--shadow),.05),0 14px 30px -22px rgba(var(--shadow),.85);transition:transform .3s cubic-bezier(.2,.8,.3,1),box-shadow .3s,border-color .3s}
.card:hover{transform:translateY(-6px);border-color:var(--gold-3);box-shadow:0 1px 0 #fff inset,0 2px 4px rgba(var(--shadow),.06),0 26px 48px -26px rgba(var(--shadow),.95)}
.preview{position:relative;display:flex;align-items:center;justify-content:center;height:212px;padding:20px;overflow:hidden;background:radial-gradient(ellipse at 50% 0%,#fdfbf4 0,var(--surface-2) 62%,#ece4d0 100%);border-bottom:1px solid var(--line-soft)}
.preview img{width:100%;height:100%;object-fit:contain;filter:drop-shadow(0 1px 2px rgba(20,40,28,.10)) drop-shadow(0 10px 18px rgba(20,40,28,.14));transition:transform .3s,filter .3s}
.card:hover .preview img{transform:scale(1.03);filter:drop-shadow(0 2px 4px rgba(20,40,28,.12)) drop-shadow(0 16px 26px rgba(20,40,28,.18))}
.preview .zoom{position:absolute;bottom:10px;right:10px;background:rgba(255,253,247,.94);color:#4b4636;border:1px solid var(--line);border-radius:99px;font-size:9.5px;letter-spacing:.03em;padding:5px 9px}
.preview .fallback{display:none}
.preview.noimg .fallback{display:grid;place-items:center;position:absolute;inset:0;padding:20px;text-align:center;color:#5b6b60;font-size:11.5px;background:var(--surface-2)}
.preview.noimg .zoom,.preview.noimg img{display:none}
.card-body{display:flex;flex-direction:column;flex:1;padding:18px 20px 20px}
.meta{display:flex;align-items:center;justify-content:space-between;gap:10px}
.tag{font-size:9.5px;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:var(--green);background:#eef3e8;border:1px solid #dfe6d3;border-radius:4px;padding:4px 8px}
.number{font-family:var(--serif);font-size:12px;color:#a2946e}
.card h3{font-size:18.5px;line-height:1.26;margin:11px 0 8px;letter-spacing:-.015em}
.card h3 a{text-decoration:none}
.card h3 a:hover{color:var(--green-mid)}
.card p{font-size:12.8px;line-height:1.62;color:var(--muted);margin:0 0 16px;flex:1}
.buy{display:flex;align-items:center;justify-content:space-between;gap:10px;border-top:1px solid var(--line-soft);padding-top:14px}
.buy strong{font-family:var(--serif);font-size:19px;font-weight:600;color:var(--green-deep);white-space:nowrap}
.buy-actions{display:flex;gap:7px}
.btn-sm{font-size:11px;font-weight:700;padding:9px 12px;border-radius:6px;text-decoration:none;display:inline-flex;align-items:center;gap:5px;transition:filter .18s,transform .18s}
.btn-wa{background:linear-gradient(180deg,#1f6b45,#0d3a26);color:#f4f0e2;border:1px solid #0b3320}
.btn-wa:hover{filter:brightness(1.15);transform:translateY(-1px)}
.btn-out{background:var(--surface);color:var(--ink);border:1px solid var(--line-strong,#d8ceb4)}
.btn-out:hover{border-color:var(--gold-2);color:var(--green)}
/* ---------------- process ---------------- */
.steps{display:grid;grid-template-columns:repeat(4,1fr);gap:0;counter-reset:s}
.step{position:relative;padding:0 26px 0 0}
.step::before{counter-increment:s;content:counter(s,decimal-leading-zero);display:block;font-family:var(--serif);font-size:13px;color:var(--gold);letter-spacing:.1em;margin-bottom:14px}
.step::after{content:"";position:absolute;left:38px;right:14px;top:9px;height:1px;background:linear-gradient(90deg,var(--line-strong,#d8ceb4),transparent)}
.step:last-child::after{display:none}
.step h3{font-size:17px;margin:0 0 8px;line-height:1.3}
.step p{margin:0;font-size:13px;line-height:1.66;color:var(--muted)}
/* ---------------- audience ---------------- */
.aud-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
.aud{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:22px 20px}
.aud b{display:block;font-family:var(--serif);font-size:16px;margin-bottom:7px}
.aud span{font-size:12.5px;line-height:1.6;color:var(--muted)}
/* ---------------- about ---------------- */
.about-in{display:grid;grid-template-columns:.85fr 1.15fr;gap:60px;align-items:start}
.about-card{position:relative;background:linear-gradient(170deg,#0d3823,#08251a);color:#e8eee9;border-radius:16px;padding:34px 30px;border:1px solid rgba(232,217,176,.2);box-shadow:0 1px 0 rgba(232,217,176,.18) inset,0 30px 60px -34px rgba(8,42,26,.9)}
.about-card .sig{font-family:var(--serif);font-size:25px;color:#f4efe0;line-height:1.2;margin:0 0 4px}
.about-card .sig-role{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold-2);margin-bottom:22px}
.about-card dl{display:grid;grid-template-columns:auto 1fr;gap:11px 16px;margin:0;font-size:12.5px;border-top:1px solid rgba(232,217,176,.16);padding-top:20px}
.about-card dt{color:#8fa89a;letter-spacing:.04em}
.about-card dd{margin:0;color:#e8eee9}
.about-copy h2{font-size:clamp(27px,2.9vw,36px);line-height:1.14;margin:14px 0 20px}
.about-copy p{font-size:14.8px;line-height:1.8;color:var(--ink-soft);margin:0 0 16px}
.about-copy p strong{color:var(--ink);font-weight:700}
.about-list{list-style:none;margin:24px 0 0;padding:0;display:grid;gap:12px}
.about-list li{display:flex;gap:11px;font-size:13.5px;line-height:1.62;color:var(--ink-soft)}
.about-list li::before{content:"✓";flex:0 0 20px;height:20px;display:grid;place-items:center;border-radius:50%;background:#eaf1e2;color:var(--green);font-size:11px;font-weight:700;margin-top:2px}
.about-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:32px;border-top:1px solid var(--line);padding-top:24px}
.about-stats b{display:block;font-family:var(--serif);font-size:28px;color:var(--green);line-height:1.1}
.about-stats span{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
/* ---------------- categories ---------------- */
.cats{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.cat{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:22px}
.cat-hd{display:flex;align-items:baseline;gap:10px;margin-bottom:12px}
.cat-n{font-family:var(--serif);font-size:12px;color:var(--gold);border:1px solid var(--gold-3);border-radius:5px;padding:1px 7px}
.cat h3{font-size:16.5px;margin:0}
.cat ul{margin:0 0 14px;padding:0 0 0 16px;font-size:12.5px;line-height:1.7;color:var(--muted)}
.cat-l{font-size:11.5px;font-weight:700;color:var(--green);text-decoration:none;letter-spacing:.02em}
.cat-l:hover{color:var(--gold)}
/* ---------------- faq ---------------- */
.faq{display:grid;grid-template-columns:repeat(2,1fr);gap:0 44px}
.faq details{border-bottom:1px solid var(--line);padding:18px 0}
.faq summary{cursor:pointer;font-family:var(--serif);font-size:16.5px;font-weight:600;list-style:none;display:flex;justify-content:space-between;gap:14px;align-items:baseline}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";color:var(--gold);font-family:var(--sans);font-size:18px;line-height:1}
.faq details[open] summary::after{content:"–"}
.faq p{margin:11px 0 0;font-size:13px;line-height:1.72;color:var(--muted)}
/* ---------------- final cta ---------------- */
.cta{position:relative;overflow:hidden;background:#082a1a;color:#f4f0e2;border-radius:0}
.cta-bg{position:absolute;inset:0;background:radial-gradient(ellipse 58% 110% at 82% -6%,rgba(25,76,52,.44),transparent 64%),linear-gradient(160deg,#0a2b1b,#04140c)}
.cta-in{position:relative;display:flex;align-items:center;justify-content:space-between;gap:40px;padding:64px 0}
.cta h2{font-size:clamp(26px,3vw,38px);line-height:1.14;margin:12px 0 12px;max-width:20ch}
.cta p{margin:0;color:#b9cbc0;font-size:14.5px;max-width:48ch}
.cta .btn{flex:0 0 auto}
/* ---------------- responsive ---------------- */
@media(max-width:1080px){
  .grid{grid-template-columns:repeat(2,minmax(0,1fr))}
  .svc-grid{grid-template-columns:repeat(2,1fr)}
  .cats{grid-template-columns:repeat(2,1fr)}
  .steps{grid-template-columns:repeat(2,1fr);gap:34px 0}
  .step:nth-child(2)::after{display:none}
  .aud-grid{grid-template-columns:repeat(2,1fr)}
}
@media(max-width:900px){
  .hero{padding:54px 0 62px}
  .hero-in{grid-template-columns:1fr;gap:44px}
  .hero h1{max-width:none}
  .hero-visual{order:2}
  .sheet-shell{transform:none}
  .about-in{grid-template-columns:1fr;gap:34px}
  .faq{grid-template-columns:1fr}
  .cta-in{flex-direction:column;align-items:flex-start;gap:26px;padding:52px 0}
  .sec{padding:56px 0}
  .sec-head{margin-bottom:32px}
}
@media(max-width:640px){
  .grid{grid-template-columns:1fr;gap:18px}
  .preview{height:200px}
  .svc-grid,.cats{grid-template-columns:1fr}
  .steps{grid-template-columns:1fr}
  .step::after{display:none}
  .hero-stats div{padding-right:20px;margin-right:20px}
  .hero-stats b{font-size:22px}
  .strip-in{justify-content:flex-start;gap:10px 16px;font-size:11px}
  .about-stats{grid-template-columns:1fr;gap:14px;text-align:left}
}
"""

HERO_SVG = """<svg viewBox="0 0 560 340" role="img" aria-label="Exemplo de dashboard de gestão em Excel">
  <rect width="560" height="340" fill="#fffdf8"/>
  <rect x="0" y="0" width="560" height="34" fill="#12402a"/>
  <text x="16" y="22" font-family="Georgia,serif" font-size="12" fill="#e8d9b0">Gestão Empresarial · Dashboard</text>
  <text x="470" y="22" font-family="Helvetica,Arial" font-size="9" fill="#8fae9b">2026</text>
  <rect x="0" y="34" width="560" height="22" fill="#1a5a3a"/>
  <g font-family="Helvetica,Arial" font-size="8.5" fill="#dfeede">
    <text x="16" y="49">Indicador</text><text x="180" y="49">Meta</text><text x="268" y="49">Real</text><text x="366" y="49">Variação</text><text x="474" y="49">Estado</text>
  </g>
  <g font-family="Helvetica,Arial" font-size="9" fill="#33453a">
    <rect x="0" y="56" width="560" height="26" fill="#f8f6ee"/><text x="16" y="73">Vendas do mês</text><text x="180" y="73">4.500.000</text><text x="268" y="73">5.180.400</text><text x="366" y="73" fill="#1a7a44">+15,1%</text><text x="474" y="73" fill="#1a7a44">Acima</text>
    <rect x="0" y="82" width="560" height="26" fill="#ffffff"/><text x="16" y="99">Margem bruta</text><text x="180" y="99">32%</text><text x="268" y="99">34,6%</text><text x="366" y="99" fill="#1a7a44">+2,6 pp</text><text x="474" y="99" fill="#1a7a44">Acima</text>
    <rect x="0" y="108" width="560" height="26" fill="#f8f6ee"/><text x="16" y="125">Stock parado</text><text x="180" y="125">8%</text><text x="268" y="125">11,4%</text><text x="366" y="125" fill="#b05a2a">−3,4 pp</text><text x="474" y="125" fill="#b05a2a">A rever</text>
    <rect x="0" y="134" width="560" height="26" fill="#ffffff"/><text x="16" y="151">Contas a receber</text><text x="180" y="151">2.000.000</text><text x="268" y="151">1.745.900</text><text x="366" y="151" fill="#1a7a44">+12,7%</text><text x="474" y="151" fill="#1a7a44">Bom</text>
  </g>
  <g>
    <rect x="16" y="182" width="164" height="66" rx="7" fill="#f4f1e4" stroke="#e3dcc8"/>
    <text x="28" y="202" font-family="Helvetica,Arial" font-size="8" fill="#7a8677">FACTURAÇÃO</text>
    <text x="28" y="228" font-family="Georgia,serif" font-size="19" fill="#123f2a">18,4 M</text>
    <text x="28" y="241" font-family="Helvetica,Arial" font-size="8" fill="#1a7a44">+ 9,2% vs. trimestre</text>
    <rect x="196" y="182" width="164" height="66" rx="7" fill="#f4f1e4" stroke="#e3dcc8"/>
    <text x="208" y="202" font-family="Helvetica,Arial" font-size="8" fill="#7a8677">DESPESAS</text>
    <text x="208" y="228" font-family="Georgia,serif" font-size="19" fill="#123f2a">11,9 M</text>
    <text x="208" y="241" font-family="Helvetica,Arial" font-size="8" fill="#7a8677">Dentro do orçamento</text>
    <rect x="376" y="182" width="168" height="66" rx="7" fill="#0f3a25"/>
    <text x="388" y="202" font-family="Helvetica,Arial" font-size="8" fill="#8fae9b">RESULTADO</text>
    <text x="388" y="228" font-family="Georgia,serif" font-size="19" fill="#e8d9b0">6,5 M</text>
    <text x="388" y="241" font-family="Helvetica,Arial" font-size="8" fill="#a8c4ae">Kz · lucro do trimestre</text>
  </g>
  <g>
    <rect x="16" y="266" width="528" height="58" rx="7" fill="#fbf8ee" stroke="#e3dcc8"/>
    <text x="28" y="284" font-family="Helvetica,Arial" font-size="8" fill="#7a8677">EVOLUÇÃO MENSAL</text>
    <g fill="#2c7a52">
      <rect x="30" y="306" width="26" height="10" rx="1.5"/><rect x="66" y="301" width="26" height="15" rx="1.5"/><rect x="102" y="303" width="26" height="13" rx="1.5"/><rect x="138" y="296" width="26" height="20" rx="1.5"/><rect x="174" y="299" width="26" height="17" rx="1.5"/><rect x="210" y="292" width="26" height="24" rx="1.5"/><rect x="246" y="294" width="26" height="22" rx="1.5"/><rect x="282" y="288" width="26" height="28" rx="1.5"/>
      <rect x="318" y="290" width="26" height="26" rx="1.5"/><rect x="354" y="284" width="26" height="32" rx="1.5"/><rect x="390" y="287" width="26" height="29" rx="1.5"/><rect x="426" y="281" width="26" height="35" rx="1.5"/>
    </g>
    <rect x="462" y="279" width="26" height="37" rx="1.5" fill="#c1a258"/>
    <rect x="498" y="276" width="26" height="40" rx="1.5" fill="#c1a258"/>
  </g>
</svg>"""


def build_home(products) -> str:
    money = [_money(p["price"]) for p in products]
    lo = min(products, key=lambda p: p["price"])
    n = len(products)

    cards = []
    for i, (p, price) in enumerate(zip(products, money), 1):
        cards.append("__CARD__" + str(i - 1) + "__")

    hero_stats = (
        f"<div><b>{n}</b><span>planilhas prontas</span></div>"
        f"<div><b>{BRAND['delivered']}+</b><span>ficheiros entregues</span></div>"
        f"<div><b>{BRAND['years']} anos</b><span>a construir em Excel</span></div>"
    )

    html = f"""<!doctype html>
<html lang="pt-AO"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#082a1a">
<title>{BRAND['name']} — Planilhas Excel profissionais para Angola</title>
<meta name="description" content="Planilhas em Excel feitas para empresas, escolas e profissionais angolanos. Gestão, salários, impostos, obra e formação. Compra pelo WhatsApp com entrega imediata do ficheiro .xlsx.">
<meta property="og:title" content="{BRAND['name']} — Planilhas Excel profissionais para Angola">
<meta property="og:description" content="18 planilhas em Excel prontas a usar, com pré-visualização real da folha e entrega pelo WhatsApp.">
<meta property="og:type" content="website">
<style>{BASE_CSS}{HOME_CSS}{mobile_nav_css()}</style></head>
<body>

<header class="hero" id="inicio">
  <div class="hero-bg" aria-hidden="true"></div>
  <div class="wrap hero-in">
    <div class="hero-copy">
      <span class="hero-eyebrow"><i></i> Colecção Excel Premium · Angola</span>
      <h1>Planilhas que põem a sua gestão <em>em ordem</em>.</h1>
      <p class="hero-lead">Construo planilhas em Excel para empresas, escolas e profissionais angolanos — com fórmulas já testadas, valores em Kwanzas e instruções em português. Escolha a sua, veja a folha real e receba o ficheiro no WhatsApp.</p>
      <div class="hero-cta">
        <a class="btn btn-gold" href="#planilhas">Ver as {n} planilhas <span aria-hidden="true">→</span></a>
        <a class="btn btn-ghost" href="https://wa.me/{BRAND['wa']}?text=Ol%C3%A1%21%20Gostaria%20de%20falar%20sobre%20uma%20planilha%20%C3%A0%20medida.">Pedir uma planilha à medida <span aria-hidden="true">↗</span></a>
      </div>
      <div class="hero-stats">{hero_stats}</div>
    </div>
    <div class="hero-visual">
      <div class="sheet-shell">
        <div class="sheet-top"><i></i><i></i><i></i><em>Excel · ficheiro real</em></div>
        <div class="sheet-body">{HERO_SVG}</div>
      </div>
      <div class="hero-badge"><i>↗</i><div><b>Entrega no WhatsApp</b><span>Ficheiro .xlsx + instruções</span></div></div>
    </div>
  </div>
</header>

<div class="strip"><div class="wrap strip-in">
  <span><i>◆</i> <b>Feito em Angola</b> · valores em Kz</span>
  <span><i>◆</i> Pré-visualização <b>da folha real</b></span>
  <span><i>◆</i> Fórmulas <b>já testadas</b></span>
  <span><i>◆</i> <b>7 dias</b> de suporte incluído</span>
  <span><i>◆</i> Compatível com <b>Excel e LibreOffice</b></span>
</div></div>

<main>

<section class="sec" id="servicos">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">O que faço</span>
      <h2>Ferramentas de trabalho, não ficheiros bonitos.</h2>
      <p>Cada planilha nasce de um problema concreto de gestão. O objectivo é sempre o mesmo: reduzir contas manuais, evitar erros e dar-lhe informação para decidir.</p>
    </div>
    <div class="svc-grid">
      <article class="svc"><div class="svc-no">01</div><h3>Gestão financeira e contabilidade</h3><p>Controlo de caixa, stock, vendas, impostos e contabilidade segundo o SNC. Mapas prontos para conferir com o contabilista.</p></article>
      <article class="svc"><div class="svc-no">02</div><h3>Recursos humanos e salários</h3><p>Folha salarial com INSS, IRT e salário líquido, assiduidade e processamento mensal da equipa num único ficheiro.</p></article>
      <article class="svc"><div class="svc-no">03</div><h3>Escolas e centros de formação</h3><p>Matrículas, notas, presenças, mensalidades, certificados e horários. Feito para a rotina de secretaria.</p></article>
      <article class="svc"><div class="svc-no">04</div><h3>Construção e obra</h3><p>Orçamentos com BDI, diário de obra e controlo de materiais para acompanhar a execução sem surpresas.</p></article>
      <article class="svc"><div class="svc-no">05</div><h3>Compras e fornecedores</h3><p>Comparação de cotações lado a lado e histórico de preços para negociar com informação na mão.</p></article>
      <article class="svc"><div class="svc-no">06</div><h3>Planilhas à medida</h3><p>Não encontrou o que precisa? Descrevo o processo, construo o ficheiro e entrego com instruções próprias.</p></article>
    </div>
  </div>
</section>

<section class="sec sec-alt" id="planilhas">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Catálogo</span>
      <h2>As {n} planilhas disponíveis.</h2>
      <p>Todas mostram a folha real do ficheiro. Clique em “Ver detalhes” para ler o passo a passo e pedir pelo WhatsApp.</p>
    </div>
    <div class="cat-strip">__PILLS__</div>
    <div class="grid">
__CARDS__
    </div>
  </div>
</section>

<section class="sec" id="processo">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Como funciona</span>
      <h2>Quatro passos entre a escolha e o ficheiro a funcionar.</h2>
      <p>Sem formulários, sem espera de dias. A conversa acontece onde já está: no WhatsApp.</p>
    </div>
    <div class="steps">
      <article class="step"><h3>Escolhe a planilha</h3><p>Veja a pré-visualização da folha real e leia o que a planilha resolve antes de decidir.</p></article>
      <article class="step"><h3>Fala comigo no WhatsApp</h3><p>Um clique abre a conversa com a planilha, o preço e o link já preenchidos. Tiro dúvidas antes do pagamento.</p></article>
      <article class="step"><h3>Recebe o ficheiro</h3><p>Após confirmação, envio o .xlsx na conversa com o guia de utilização e os campos a preencher primeiro.</p></article>
      <article class="step"><h3>Conta comigo 7 dias</h3><p>Se algo não funcionar como esperava, ajusto ou explico até a planilha ficar a trabalhar por si.</p></article>
    </div>
  </div>
</section>

<section class="sec sec-alt">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Para quem</span>
      <h2>Quem já trabalha com estas planilhas.</h2>
    </div>
    <div class="aud-grid">
      <article class="aud"><b>PME e comércio</b><span>Lojas, armazéns e prestadores de serviços que controlam caixa, stock e vendas em Excel.</span></article>
      <article class="aud"><b>Escritórios de contabilidade</b><span>Profissionais que precisam de mapas organizados para entregar aos clientes.</span></article>
      <article class="aud"><b>Escolas e centros</b><span>Secretarias que gerem matrículas, notas, mensalidades e certificados todos os meses.</span></article>
      <article class="aud"><b>Construtoras e técnicos</b><span>Orçamentistas e encarregados de obra que acompanham custos e execução no terreno.</span></article>
    </div>
  </div>
</section>

<section class="sec" id="sobre">
  <div class="wrap about-in">
    <aside class="about-card">
      <span class="brand-mark" style="margin-bottom:18px">MB</span>
      <p class="sig">{BRAND['name']}</p>
      <div class="sig-role">{BRAND['role']}</div>
      <dl>
        <dt>Base</dt><dd>{BRAND['city']}</dd>
        <dt>Experiência</dt><dd>{BRAND['years']} anos em Excel aplicado à gestão</dd>
        <dt>Ficheiros</dt><dd>{BRAND['delivered']}+ entregues</dd>
        <dt>Especialidade</dt><dd>Automação de rotinas com fórmulas e tabelas dinâmicas</dd>
        <dt>Contacto</dt><dd>{BRAND['phone']}</dd>
      </dl>
    </aside>
    <div class="about-copy">
      <span class="eyebrow">Sobre o autor</span>
      <h2>Planilhas feitas por quem já sentou do lado de quem usa.</h2>
      <p>Há {BRAND['years']} anos que trabalho com Excel aplicado à gestão — quase sempre do lado de dentro das empresas, onde os problemas aparecem. Folhas de salário que não fechavam, stock que ninguém conseguia contar, relatórios que levavam três dias a preparar: foi aí que aprendi o que uma planilha tem de resolver.</p>
      <p>Com o tempo, transformei essas soluções em modelos reutilizáveis e passei a construí-los para outras pessoas. Hoje entrego planilhas a empresas, escolas e profissionais em Angola: ficheiros que calculam sozinhos, assinalam o que está fora do previsto e devolvem informação pronta a ler — em Kwanzas, em português e alinhados com a realidade fiscal angolana.</p>
      <p>O compromisso com que trabalho é simples: <strong>cada planilha tem de poupar tempo logo na primeira semana</strong>. Se não poupar, não faz sentido entregá-la.</p>
      <ul class="about-list">
        <li>Modelos construídos com fórmulas nativas do Excel — abrem em qualquer computador, sem macros nem instalações.</li>
        <li>Cada ficheiro é entregue com instruções escritas e os primeiros passos já preenchidos como exemplo.</li>
        <li>Adaptação do modelo ao seu processo real, quando o catálogo não chega.</li>
        <li>Acompanhamento directo por WhatsApp durante 7 dias após a entrega.</li>
      </ul>
      <div class="about-stats">
        <div><b>{BRAND['years']}</b><span>anos de prática</span></div>
        <div><b>{BRAND['delivered']}+</b><span>ficheiros entregues</span></div>
        <div><b>7 dias</b><span>de suporte directo</span></div>
      </div>
    </div>
  </div>
</section>

<section class="sec sec-alt">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Áreas</span>
      <h2>Biblioteca organizada por área de trabalho.</h2>
      <p>Se ainda não sabe qual planilha escolher, comece pela área onde passa mais tempo.</p>
    </div>
    <div class="cats">
__CATS__
    </div>
  </div>
</section>

<section class="sec" id="faq">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Perguntas frequentes</span>
      <h2>Antes de decidir.</h2>
    </div>
    <div class="faq">
      <details open><summary>Como recebo a planilha?</summary><p>Pelo WhatsApp. Depois de confirmar a compra, envio o ficheiro .xlsx na própria conversa, junto com o guia de utilização. Não há download no site — a entrega é directa e confirmada consigo.</p></details>
      <details><summary>Preciso de algum programa especial?</summary><p>Não. As planilhas funcionam no Microsoft Excel e em aplicações compatíveis como LibreOffice Calc ou Excel para telemóvel. Usam apenas fórmulas nativas, sem macros.</p></details>
      <details><summary>Os valores já estão em Kwanzas?</summary><p>Sim. Todos os modelos estão preparados para Kwanzas (Kz), com os parâmetros legais angolanos — INSS e IRT incluídos — editáveis na folha de configuração.</p></details>
      <details><summary>Posso pedir alterações ao modelo?</summary><p>Pode. Se a sua rotina for diferente, ajusto as colunas, categorias ou cálculos. Este trabalho é combinado no WhatsApp antes do envio.</p></details>
      <details><summary>Como pago?</summary><p>O pagamento é combinado directamente no WhatsApp, com os dados enviados na conversa. O ficheiro só segue depois da confirmação.</p></details>
      <details><summary>E se eu não souber usar a planilha?</summary><p>Junto instruções escritas e explico os primeiros passos na conversa. Durante 7 dias fico disponível para dúvidas sobre o ficheiro que recebeu.</p></details>
    </div>
  </div>
</section>

<section class="cta">
  <div class="cta-bg" aria-hidden="true"></div>
  <div class="wrap cta-in">
    <div>
      <span class="hero-eyebrow" style="color:var(--gold-3)">Próximo passo</span>
      <h2>Diga-me o que precisa de controlar. Eu faço a planilha.</h2>
      <p>Se nenhuma destas {n} planilhas servir para o seu caso, descreva o processo no WhatsApp. Respondo com uma proposta concreta, preço e prazo.</p>
    </div>
    <a class="btn btn-gold" href="https://wa.me/{BRAND['wa']}?text=Ol%C3%A1%21%20Preciso%20de%20uma%20planilha%20para%20o%20meu%20processo.">Falar com {BRAND['name'].split()[0]} <span aria-hidden="true">↗</span></a>
  </div>
</section>

</main>
{footer()}
<script>document.getElementById('ano').textContent=new Date().getFullYear()</script>
</body></html>"""

    # catalogue chips
    tags = {}
    for p in products:
        tags[p["tag"]] = tags.get(p["tag"], 0) + 1
    pills = "".join(
        f'<span class="cat-pill">{escape(t)}<b>{c}</b></span>'
        for t, c in sorted(tags.items(), key=lambda kv: (-kv[1], kv[0]))
    )
    html = html.replace("__PILLS__", pills)
    html = html.replace("__CATS__", category_rows(products))
    html = html.replace("__CARDS__", "\n".join(cards))
    return html
