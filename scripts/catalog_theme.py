#!/usr/bin/env python3
"""Shared design system for the catalogue: tokens, navigation, footer, page shells.

Keeping the stylesheet here (instead of inline f-strings in the renderer) lets the
home page and the 18 product pages share one typographic and colour system.
"""
from html import escape

BRAND = {
    "name": "Manuel Baptista Licanga",
    "short": "MB",
    "role": "Especialista em Excel e automação de processos",
    "city": "Luanda, Angola",
    "phone": "+244 942 739 225",
    "wa": "244942739225",
    "years": "8",
    "delivered": "400",
}

# --------------------------------------------------------------------------
# Design tokens
# --------------------------------------------------------------------------
BASE_CSS = """
:root{
  color-scheme:light;
  --ink:#111f18;
  --ink-soft:#33453a;
  --muted:#5b6b60;
  --line:#e3dcc8;
  --line-soft:#efe9d9;
  --line-strong:#d3c9ae;
  --gold:#a8862f;
  --gold-2:#cdae6c;
  --gold-3:#e8d9b0;
  --green:#0f3725;
  --green-deep:#062016;
  --green-mid:#16503a;
  --cream:#f8f5ec;
  --surface:#fffdf8;
  --surface-2:#f3eee0;
  --shadow:26 44 34;
  --serif:'Iowan Old Style','Palatino Linotype',Palatino,'Book Antiqua',Georgia,serif;
  --sans:Inter,ui-sans-serif,system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{margin:0;background:var(--cream);color:var(--ink);font-family:var(--sans);font-size:16px;line-height:1.6;-webkit-font-smoothing:antialiased}
img{max-width:100%}
a{color:inherit}
.wrap{max-width:1180px;margin:0 auto;padding:0 26px}
.eyebrow{display:inline-flex;align-items:center;gap:9px;font-size:11px;font-weight:700;letter-spacing:.19em;text-transform:uppercase;color:var(--gold)}
.eyebrow::before{content:"";width:22px;height:1px;background:var(--gold-2)}
h1,h2,h3{font-family:var(--serif);font-weight:600;letter-spacing:-.015em}
.btn{display:inline-flex;align-items:center;gap:9px;text-decoration:none;font-family:var(--sans);font-size:14px;font-weight:700;padding:13px 22px;border-radius:8px;border:1px solid transparent;transition:transform .18s ease,filter .18s ease,background .18s ease,color .18s ease,border-color .18s ease;cursor:pointer}
.btn-gold{background:linear-gradient(180deg,#d9bd7f,#b8973d);color:#1d1a0e;border-color:#a5852f;box-shadow:0 1px 0 rgba(255,255,255,.45) inset,0 6px 16px -8px rgba(20,30,20,.55)}
.btn-gold:hover{filter:brightness(1.05);transform:translateY(-1px)}
.btn-ghost{background:transparent;color:#efe9d8;border-color:rgba(232,217,176,.36)}
.btn-ghost:hover{border-color:var(--gold-2);color:#fff;background:rgba(232,217,176,.08)}
.btn-green{background:linear-gradient(180deg,var(--green-mid),var(--green-deep));color:#fbf8ee;border-color:#0c3a24;box-shadow:0 1px 0 rgba(255,255,255,.13) inset,0 6px 16px -8px rgba(20,30,20,.5)}
.btn-green:hover{filter:brightness(1.1);transform:translateY(-1px)}
.rule{height:1px;background:linear-gradient(90deg,var(--line-strong,rgba(0,0,0,.1)),transparent);border:0;margin:0}
"""

# --------------------------------------------------------------------------
# Navigation
# --------------------------------------------------------------------------
NAV_HTML = """
<header class="nav" id="topo">
  <div class="wrap nav-in">
    <a class="brand" href="__P__index.html" aria-label="__NAME__ — página inicial">
      <span class="brand-mark">__SHORT__</span>
      <span class="brand-txt">
        <strong>__NAME__</strong>
        <em>Excel · Automação · Angola</em>
      </span>
    </a>
    <nav class="nav-links" aria-label="Navegação principal">
      <a href="__P__index.html#planilhas">Planilhas</a>
      <a href="__P__index.html#servicos">Serviços</a>
      <a href="__P__index.html#processo">Como funciona</a>
      <a href="__P__index.html#sobre">Sobre</a>
    </nav>
    <a class="btn btn-green nav-cta" href="https://wa.me/__WA__?text=__WAMSG__">Falar comigo<span aria-hidden="true">↗</span></a>
  </div>
</header>
"""

# --------------------------------------------------------------------------
# Footer
# --------------------------------------------------------------------------
FOOTER_HTML = """
<footer class="site-foot">
  <div class="wrap foot-in">
    <div class="foot-brand">
      <span class="brand-mark">__SHORT__</span>
      <div>
        <strong>__NAME__</strong>
        <p>__ROLE__. Planilhas em Excel construídas para a realidade das empresas angolanas, entregues com instruções e suporte.</p>
      </div>
    </div>
    <div class="foot-col">
      <h4>Catálogo</h4>
      <a href="__P__index.html#planilhas">Todas as planilhas</a>
      <a href="__P__index.html#servicos">Serviços</a>
      <a href="__P__index.html#processo">Como funciona</a>
      <a href="__P__index.html#faq">Perguntas frequentes</a>
    </div>
    <div class="foot-col">
      <h4>Contacto</h4>
      <a href="https://wa.me/__WA__">WhatsApp · __PHONE__</a>
      <a href="__P__index.html#sobre">Sobre o autor</a>
      <span class="foot-note">__CITY__</span>
      <span class="foot-note">Seg. a Sáb. · 08h00–19h00</span>
    </div>
    <div class="foot-col">
      <h4>Entrega</h4>
      <span class="foot-note">Ficheiro .xlsx</span>
      <span class="foot-note">Preços em Kwanzas (Kz)</span>
      <span class="foot-note">7 dias de suporte incluído</span>
      <span class="foot-note">Entrega pelo WhatsApp</span>
    </div>
  </div>
  <div class="wrap foot-base">
    <span>© <span id="ano">2026</span> __NAME__ · Todos os direitos reservados.</span>
    <span>Planilhas Excel Premium — Feito em Angola</span>
  </div>
</footer>
"""


def _fill(template: str, prefix: str = "") -> str:
    wa_msg = "Ol%C3%A1%21%20Vi%20o%20seu%20cat%C3%A1logo%20e%20gostaria%20de%20saber%20mais%20sobre%20as%20planilhas."
    return (
        template.replace("__P__", prefix)
        .replace("__NAME__", BRAND["name"])
        .replace("__SHORT__", BRAND["short"])
        .replace("__ROLE__", BRAND["role"])
        .replace("__PHONE__", BRAND["phone"])
        .replace("__CITY__", BRAND["city"])
        .replace("__WA__", BRAND["wa"])
        .replace("__WAMSG__", wa_msg)
    )


def nav(prefix: str = "") -> str:
    out = _fill(NAV_HTML, prefix)
    # na página inicial os links do menu devem ser âncoras puras
    if not prefix:
        out = out.replace('href="index.html#', 'href="#')
    return out


def footer(prefix: str = "") -> str:
    out = _fill(FOOTER_HTML, prefix)
    if not prefix:
        out = out.replace('href="index.html#', 'href="#')
    return out


def head(title: str, description: str, css: str, prefix: str = "") -> str:
    return (
        '<!doctype html>\n<html lang="pt-AO"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<meta name="theme-color" content="#082a1a">'
        f'<meta name="description" content="{escape(description, quote=True)}">'
        '<meta property="og:type" content="website">'
        f'<meta property="og:title" content="{escape(title, quote=True)}">'
        f'<meta property="og:description" content="{escape(description, quote=True)}">'
        f"<title>{escape(title)}</title>\n"
        f"<style>{BASE_CSS}{css}</style></head>\n<body>\n"
        + nav(prefix)
    )


NAV_CSS = """
.nav{position:sticky;top:0;z-index:60;background:rgba(248,245,236,.9);backdrop-filter:blur(16px) saturate(1.2);border-bottom:1px solid var(--line)}
.nav-in{display:flex;align-items:center;justify-content:space-between;gap:22px;min-height:74px}
.brand{display:flex;align-items:center;gap:12px;text-decoration:none}
.brand-mark{display:grid;place-items:center;width:42px;height:42px;border-radius:10px;background:linear-gradient(155deg,var(--green-mid),var(--green-deep));color:var(--gold-3);font-family:var(--serif);font-size:16px;font-weight:600;letter-spacing:.04em;box-shadow:0 1px 0 rgba(232,217,176,.28) inset,0 8px 18px -12px rgba(8,42,26,.9)}
.brand-txt{display:flex;flex-direction:column;line-height:1.25}
.brand-txt strong{font-size:14.5px;letter-spacing:-.01em}
.brand-txt em{font-family:var(--sans);font-style:normal;font-size:10.5px;letter-spacing:.13em;text-transform:uppercase;color:var(--muted)}
.nav-links{display:flex;align-items:center;gap:26px}
.nav-links a{font-size:13.5px;font-weight:600;color:var(--ink-soft);text-decoration:none;padding:6px 0;border-bottom:1px solid transparent;transition:color .18s,border-color .18s}
.nav-links a:hover{color:var(--green);border-bottom-color:var(--gold-2)}
.nav-cta{padding:11px 18px;font-size:13px}
.foot-in{display:grid;grid-template-columns:1.55fr 1fr 1.1fr 1fr;gap:44px;padding-top:56px;padding-bottom:44px}
.foot-brand{display:flex;gap:14px;align-items:flex-start}
.foot-brand strong{font-family:var(--serif);font-size:17px}
.foot-brand p{margin:7px 0 0;font-size:12.5px;line-height:1.7;color:#a9bcb0;max-width:34ch}
.foot-col{display:flex;flex-direction:column;gap:9px}
.foot-col h4{margin:0 0 5px;font-family:var(--sans);font-size:11px;font-weight:700;letter-spacing:.17em;text-transform:uppercase;color:var(--gold-2)}
.foot-col a{font-size:13px;color:#cdd9d1;text-decoration:none;transition:color .18s}
.foot-col a:hover{color:var(--gold-3)}
.foot-note{font-size:12.5px;color:#93a79b}
.foot-base{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;padding-top:20px;padding-bottom:26px;border-top:1px solid rgba(232,217,176,.14);font-size:11.5px;color:#8ea295}
"""

FOOT_CSS = """
.site-foot{background:linear-gradient(180deg,#0a2f1d,#061d13);color:#e8eee9;margin-top:0}
.site-foot .brand-mark{background:rgba(232,217,176,.1);border:1px solid rgba(232,217,176,.3);box-shadow:none}
"""


def mobile_nav_css() -> str:
    return """
@media(max-width:900px){
  .nav-links{display:none}
  .brand-txt em{display:none}
  .foot-in{grid-template-columns:1fr 1fr;gap:32px}
}
@media(max-width:560px){
  .foot-in{grid-template-columns:1fr;gap:26px;padding-top:40px}
  .nav-cta{font-size:12px;padding:10px 13px}
  .brand-txt strong{font-size:13px}
  .wrap{padding:0 18px}
}
"""
