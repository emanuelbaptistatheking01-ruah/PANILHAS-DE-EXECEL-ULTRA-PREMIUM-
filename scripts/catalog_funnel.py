#!/usr/bin/env python3
"""Funil de venda: página de oferta (front-end), upsell e downsell.

Fluxo: qualquer cartão do catálogo -> oferta.html -> (upsell | downsell) -> obrigado.html

Todos os botões passam por /api/checkout, que valida o produto no servidor,
regista o pedido e devolve o número de encomenda antes de mandar o cliente
para o WhatsApp. Assim cada venda fica rastreável sem precisar de gateway.
"""
from html import escape
import urllib.parse

from catalog_theme import BASE_CSS, FOOT_CSS, NAV_CSS, BRAND, footer, head, mobile_nav_css

SITE = "https://planilhas-ultra-angola-emanuelbaptistatheking01-9378.vercel.app"
WA = BRAND["wa"]
PHONE = BRAND["phone"]

# ordem de venda: produto 1 -> 2 -> 3 (upsell) | -> 8 (downsell)
FUNNEL = {
    1: {"up": 2, "down": 8},
    2: {"up": 3, "down": 7},
    3: {"up": 4, "down": 7},
    4: {"up": 12, "down": 3},
    5: {"up": 6, "down": 7},
    6: {"up": 11, "down": 7},
    7: {"up": 2, "down": 9},
    8: {"up": 2, "down": 9},
    9: {"up": 8, "down": 10},
    10: {"up": 2, "down": 9},
    11: {"up": 12, "down": 4},
    12: {"up": 11, "down": 4},
    13: {"up": 11, "down": 14},
    14: {"up": 13, "down": 15},
    15: {"up": 13, "down": 17},
    16: {"up": 11, "down": 18},
    17: {"up": 13, "down": 16},
    18: {"up": 13, "down": 16},
}


def money(v):
    return format(v, ",").replace(",", ".")


def wa_text(msg):
    return f"https://wa.me/{WA}?text={urllib.parse.quote(msg, safe='')}"


FUNNEL_CSS = NAV_CSS + FOOT_CSS + """
/* ---------- progresso do funil ---------- */
.fsteps{display:flex;align-items:center;justify-content:center;gap:0;margin:0 0 34px}
.fstep{display:flex;align-items:center;gap:9px;font-size:11.5px;font-weight:600;letter-spacing:.04em;color:var(--muted)}
.fstep i{display:grid;place-items:center;width:24px;height:24px;border-radius:50%;border:1px solid var(--line-strong);background:var(--surface);font-style:normal;font-size:11px;color:var(--muted)}
.fstep.on{color:var(--green)}
.fstep.on i{background:var(--green);border-color:var(--green);color:#f4f0e2}
.fstep.done i{background:#e8efe2;border-color:#cfdcc4;color:var(--green)}
.fstep-line{width:52px;height:1px;background:var(--line-strong);margin:0 14px}
/* ---------- cartao de oferta ---------- */
.offer{display:grid;grid-template-columns:1.05fr .95fr;gap:48px;align-items:start;padding:12px 0 64px}
.offer-media{border:1px solid var(--line);border-radius:14px;overflow:hidden;background:radial-gradient(ellipse at 50% 0%,#fdfbf4,var(--surface-2) 62%,#ece4d0);padding:24px;box-shadow:0 1px 0 #fff inset,0 2px 4px rgba(var(--shadow),.05),0 20px 40px -28px rgba(var(--shadow),.85)}
.offer-media img{width:100%;height:auto;display:block;filter:drop-shadow(0 1px 2px rgba(20,40,28,.10)) drop-shadow(0 14px 24px rgba(20,40,28,.16))}
.offer-media figcaption{margin:14px 0 0;font-size:11px;color:var(--muted);text-align:center;letter-spacing:.02em}
.offer h1{font-family:var(--serif);font-size:clamp(27px,3.2vw,38px);line-height:1.12;letter-spacing:-.02em;margin:14px 0 14px}
.offer .lead{font-size:15px;line-height:1.75;color:var(--ink-soft);margin:0 0 22px}
.pricebox{border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:20px 0;margin:0 0 22px;display:flex;align-items:flex-end;justify-content:space-between;gap:18px}
.pricebox .now{font-family:var(--serif);font-size:44px;line-height:1;color:var(--green-deep);letter-spacing:-.02em}
.pricebox .now small{display:block;font-family:var(--sans);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin-top:8px}
.pricebox .was{text-align:right;font-size:12px;color:var(--muted);line-height:1.6}
.pricebox .was b{display:block;font-size:15px;color:#a2946e;text-decoration:line-through;font-weight:600}
.benefits{list-style:none;margin:0 0 24px;padding:0;display:grid;gap:11px}
.benefits li{display:flex;gap:10px;font-size:13.5px;line-height:1.6;color:var(--ink-soft)}
.benefits li::before{content:"✓";flex:0 0 19px;height:19px;display:grid;place-items:center;border-radius:50%;background:#eaf1e2;color:var(--green);font-size:10px;font-weight:700;margin-top:2px}
.buyform{display:flex;flex-direction:column;gap:12px}
.field{display:flex;flex-direction:column;gap:6px}
.field label{font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.field input{border:1px solid var(--line-strong);border-radius:8px;padding:12px 14px;font-size:14px;font-family:var(--sans);background:var(--surface);color:var(--ink);outline:none;transition:border-color .18s,box-shadow .18s}
.field input:focus{border-color:var(--green-mid);box-shadow:0 0 0 3px rgba(22,80,58,.12)}
.buyform .btn{width:100%;justify-content:center;padding:16px 20px;font-size:15px}
.secure{display:flex;align-items:center;justify-content:center;gap:8px;font-size:11.5px;color:var(--muted);margin-top:4px}
.secure i{font-style:normal;color:var(--gold)}
/* ---------- escada de valor (upsell/downsell) ---------- */
.ladder{background:var(--surface-2);border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:52px 0}
.ladder h2{font-size:clamp(23px,2.6vw,31px);line-height:1.16;margin:12px 0 10px;max-width:26ch}
.ladder p.sub{margin:0 0 30px;color:var(--muted);font-size:14.5px;max-width:62ch}
.duo{display:grid;grid-template-columns:1fr 1fr;gap:22px}
.panel{position:relative;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:28px 26px;display:flex;flex-direction:column}
.panel.up{border-color:var(--gold-2);box-shadow:0 1px 0 #fff inset,0 2px 4px rgba(var(--shadow),.05),0 22px 44px -28px rgba(var(--shadow),.9)}
.panel .flag{position:absolute;top:-11px;left:26px;background:linear-gradient(180deg,#d9bd7f,#b8973d);color:#1d1a0e;font-size:9.5px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;padding:4px 11px;border-radius:99px}
.panel .kind{font-size:10.5px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--gold);margin-bottom:12px}
.panel.down .kind{color:var(--muted)}
.panel h3{font-size:19px;line-height:1.26;margin:0 0 8px}
.panel .pdesc{font-size:12.8px;line-height:1.65;color:var(--muted);margin:0 0 16px;flex:1}
.panel .pprice{font-family:var(--serif);font-size:27px;color:var(--green-deep);margin-bottom:16px}
.panel .pprice small{font-family:var(--sans);font-size:11px;color:var(--muted);display:block;margin-top:3px}
.panel .btn{width:100%;justify-content:center;padding:14px 18px;font-size:13.5px}
.skip{display:block;text-align:center;font-size:12px;color:var(--muted);text-decoration:underline;text-underline-offset:3px;margin-top:12px}
.skip:hover{color:var(--ink)}
/* ---------- obrigado ---------- */
.thanks{max-width:660px;margin:0 auto;text-align:center;padding:56px 0 72px}
.thanks .tick{width:64px;height:64px;margin:0 auto 22px;border-radius:50%;display:grid;place-items:center;background:linear-gradient(155deg,#1f6b45,#0b3320);color:#e8d9b0;font-size:27px;box-shadow:0 1px 0 rgba(232,217,176,.3) inset,0 16px 30px -18px rgba(8,42,26,.8)}
.thanks h1{font-size:clamp(27px,3.4vw,39px);line-height:1.14;margin:0 0 14px}
.thanks p{color:var(--ink-soft);font-size:15px;line-height:1.75;margin:0 0 10px}
.orderbox{display:inline-flex;align-items:center;gap:12px;background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:13px 18px;margin:22px 0 6px;font-size:12.5px;color:var(--muted)}
.orderbox b{font-family:var(--mono,ui-monospace,monospace);font-size:14px;color:var(--green-deep);letter-spacing:.06em}
.next{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:34px 0 0;text-align:left}
.next div{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:16px 15px}
.next b{display:block;font-size:12.5px;margin-bottom:4px}
.next span{font-size:11.5px;line-height:1.55;color:var(--muted)}
@media(max-width:900px){
  .offer{grid-template-columns:1fr;gap:28px}
  .duo{grid-template-columns:1fr}
  .next{grid-template-columns:1fr}
  .fsteps .fstep span{display:none}
  .fstep-line{width:26px;margin:0 8px}
}
"""


def steps(active, done=()):
    labels = ["Escolha", "Oferta", "Reforço", "Entrega"]
    out = []
    for i, lab in enumerate(labels):
        if i in done:
            cls = "fstep done"
        elif i == active:
            cls = "fstep on"
        else:
            cls = "fstep"
        out.append(f'<div class="{cls}"><i>{i+1}</i><span>{lab}</span></div>')
        if i < len(labels) - 1:
            out.append('<div class="fstep-line"></div>')
    return '<div class="fsteps">' + "".join(out) + "</div>"


def _shell(title, desc, body):
    from catalog_theme import nav as _nav
    return (
        f'<!doctype html>\n<html lang="pt-AO"><head><meta charset="utf-8">'
        f'<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<meta name="theme-color" content="#082a1a">'
        f'<meta name="robots" content="noindex,follow">'
        f'<meta name="description" content="{escape(desc, quote=True)}">'
        f"<title>{escape(title)}</title>\n"
        f"<style>{BASE_CSS}{FUNNEL_CSS}{mobile_nav_css()}</style></head>\n<body>\n"
        f"{_nav('../')}\n{body}\n{footer('../')}\n"
        "</body></html>"
    )


# ---------------------------------------------------------------- oferta
OFFER_BENEFITS = [
    "Ficheiro Excel (.xlsx) entregue no WhatsApp, na hora",
    "Guia de utilização em português, já preenchido com exemplos",
    "Fórmulas nativas — abre em Excel, LibreOffice e telemóvel",
    "Valores, taxas e escalões em Kwanzas, editáveis",
    "7 dias de suporte directo comigo pelo WhatsApp",
]


def build_offer(i, p, products):
    price = money(p["price"])
    nxt = FUNNEL[i]
    up = products[nxt["up"] - 1]
    down = products[nxt["down"] - 1]
    up_price = money(up["price"])
    prev = PROTECT.get(i, {})

    benefits = "".join(f"<li>{escape(b)}</li>" for b in OFFER_BENEFITS)
    was = ""
    if prev.get("was"):
        was = (
            f'<div class="was">Valor normal<b>{money(prev["was"])} Kz</b>'
            f'poupa {money(prev["was"] - p["price"])} Kz</div>'
        )

    body = f"""
<main class="wrap">
  {steps(1, done=(0,))}
  <section class="offer">
    <figure class="offer-media" style="margin:0">
      <img src="../{escape(p['preview'])}" alt="Pré-visualização da folha {escape(p['sheet'])} da planilha {escape(p['title'])}" width="1526" height="640" decoding="async" fetchpriority="high">
      <figcaption>Pré-visualização real — aba “{escape(p['sheet'])}” do ficheiro que vai receber.</figcaption>
    </figure>

    <div class="offer-copy">
      <span class="eyebrow">Oferta · Planilha #{i:02d}</span>
      <h1>{escape(p['title'])}</h1>
      <p class="lead">{escape(p['description'])}</p>

      <div class="pricebox">
        <div class="now">{price} Kz<small>Pagamento único · sem mensalidade</small></div>
        {was}
      </div>

      <ul class="benefits">{benefits}</ul>

      <form class="buyform" data-checkout data-product="{i}" data-price="{p['price']}" data-next="oferta/{nxt['up']}.html">
        <div class="field">
          <label for="nome">O seu nome</label>
          <input id="nome" name="nome" type="text" placeholder="Ex.: Manuel Baptista" autocomplete="name" required>
        </div>
        <div class="field">
          <label for="tel">WhatsApp com indicativo</label>
          <input id="tel" name="tel" type="tel" placeholder="+244 9XX XXX XXX" autocomplete="tel" required>
        </div>
        <button class="btn btn-green" type="submit">Quero esta planilha — {price} Kz <span aria-hidden="true">→</span></button>
        <div class="secure"><i>◆</i> Entrega imediata no WhatsApp · apoio em português</div>
      </form>
    </div>
  </section>

  <section class="ladder" style="margin:0 -26px;padding-left:26px;padding-right:26px">
    <span class="eyebrow">Depois da compra</span>
    <h2>Quem leva esta, normalmente leva mais uma.</h2>
    <p class="sub">Escolha agora e recebe tudo na mesma conversa, sem pagar segunda entrega.</p>
    <div class="duo">
      <article class="panel up">
        <span class="flag">Recomendado</span>
        <div class="kind">Upsell · sobe um nível</div>
        <h3>{escape(up['title'])}</h3>
        <p class="pdesc">{escape(up['description'])}</p>
        <div class="pprice">{up_price} Kz<small>Somado ao pedido — entrega conjunta</small></div>
        <a class="btn btn-gold" href="upsell-{i}.html">Adicionar ao meu pedido <span aria-hidden="true">→</span></a>
      </article>
      <article class="panel down">
        <div class="kind">Downsell · versão mais simples</div>
        <h3>{escape(down['title'])}</h3>
        <p class="pdesc">{escape(down['description'])}</p>
        <div class="pprice">{money(down['price'])} Kz<small>Alternativa de entrada mais baixa</small></div>
        <a class="btn btn-ghost" style="color:var(--green);border-color:var(--line-strong)" href="downsell-{i}.html">Ver esta opção <span aria-hidden="true">→</span></a>
      </article>
    </div>
  </section>
</main>
<script src="/funil.js" defer></script>
"""
    return _shell(f"{p['title']} — {price} Kz · Oferta", f"{p['description']} Entrega imediata no WhatsApp por {price} Kz.", body)


PROTECT = {}


def build_upsell(i, p, products):
    price = money(p["price"])
    nxt = FUNNEL[i]
    up = products[nxt["up"] - 1]
    up_price = money(up["price"])
    combined = money(p["price"] + up["price"])
    save = money(round((p["price"] + up["price"]) * 0.10))
    body = f"""
<main class="wrap">
  {steps(2, done=(0, 1))}
  <section class="offer">
    <figure class="offer-media" style="margin:0">
      <img src="../{escape(up['preview'])}" alt="Pré-visualização da planilha {escape(up['title'])}" width="1526" height="640" decoding="async">
      <figcaption>Pré-visualização real da planilha {escape(up['title'])}.</figcaption>
    </figure>
    <div class="offer-copy">
      <span class="eyebrow">Passo 2 · Reforço recomendado</span>
      <h1>Leve também <em style="font-style:normal;color:var(--green)">{escape(up['title'])}</em></h1>
      <p class="lead">{escape(up['description'])}</p>
      <div class="pricebox">
        <div class="now">{up_price} Kz<small>Somado ao pedido de {price} Kz</small></div>
        <div class="was">Total do conjunto<b>{combined} Kz</b>poupa {save} Kz hoje</div>
      </div>
      <ul class="benefits">
        <li>As duas planilhas chegam na <b>mesma conversa de WhatsApp</b></li>
        <li>Um único pagamento — não paga segunda entrega</li>
        <li>Os dados passam de uma para a outra (produtos, clientes, alunos)</li>
        <li>Continua com <b>7 dias de suporte</b> em cada ficheiro</li>
        <li>Pode desistir agora e receber só a planilha de {price} Kz</li>
      </ul>
      <div class="buyform">
        <a class="btn btn-gold" href="#" data-upsell data-product="{nxt['up']}" data-price="{up['price']}" data-base="{i}">Sim, quero as duas — {combined} Kz <span aria-hidden="true">→</span></a>
        <a class="skip" href="obrigado.html?p={i}&u=0">Não, obrigado. Só a planilha de {price} Kz</a>
      </div>
    </div>
  </section>
</main>
<script src="/funil.js" defer></script>
"""
    return _shell(f"Reforço — {up['title']} · {up_price} Kz", f"Adicione {up['title']} ao pedido por {up_price} Kz com entrega na mesma conversa.", body)


def build_downsell(i, p, products):
    price = money(p["price"])
    nxt = FUNNEL[i]
    down = products[nxt["down"] - 1]
    down_price = money(down["price"])
    body = f"""
<main class="wrap">
  {steps(2, done=(0, 1))}
  <section class="offer">
    <figure class="offer-media" style="margin:0">
      <img src="../{escape(down['preview'])}" alt="Pré-visualização da planilha {escape(down['title'])}" width="1526" height="640" decoding="async">
      <figcaption>Pré-visualização real da planilha {escape(down['title'])}.</figcaption>
    </figure>
    <div class="offer-copy">
      <span class="eyebrow">Alternativa · Entrada mais baixa</span>
      <h1>Se {price} Kz é muito agora, comece por aqui.</h1>
      <p class="lead">{escape(down['description'])}</p>
      <div class="pricebox">
        <div class="now">{down_price} Kz<small>Em vez de {price} Kz</small></div>
        <div class="was">Diferença<b>−{money(p['price'] - down['price'])} Kz</b></div>
      </div>
      <ul class="benefits">
        <li>Mesmo formato: ficheiro .xlsx entregue no WhatsApp</li>
        <li>Guia de utilização incluído</li>
        <li>Pode sempre acrescentar a de {price} Kz mais tarde</li>
        <li>7 dias de suporte directo comigo</li>
      </ul>
      <div class="buyform">
        <a class="btn btn-green" href="#" data-downsell data-product="{nxt['down']}" data-price="{down['price']}" data-base="{i}">Quero esta — {down_price} Kz <span aria-hidden="true">→</span></a>
        <a class="skip" href="obrigado.html?p={i}&u=0">Prefiro ficar com a de {price} Kz</a>
      </div>
    </div>
  </section>
</main>
<script src="/funil.js" defer></script>
"""
    return _shell(f"Alternativa — {down['title']} · {down_price} Kz", f"Comece por {down['title']} por {down_price} Kz.", body)


def build_thanks(products):
    body = f"""
<main class="wrap">
  {steps(3, done=(0, 1, 2))}
  <section class="thanks">
    <div class="tick">✓</div>
    <h1>Pedido registado.</h1>
    <p>Falta só um passo: abrir a conversa de WhatsApp e enviar a mensagem já preparada. É por lá que combino o pagamento e entrego o ficheiro.</p>
    <div class="orderbox">Encomenda <b id="ordem">—</b></div>
    <p style="font-size:12.5px;color:var(--muted)">Guarde este número. Serve para identificar o seu pedido.</p>
    <div style="margin-top:24px"><a class="btn btn-gold" id="wa-final" href="https://wa.me/{WA}">Abrir WhatsApp <span aria-hidden="true">↗</span></a></div>
    <div class="next">
      <div><b>1. Confirmação</b><span>Respondo em poucos minutos dentro do horário (seg–sáb, 08h–19h).</span></div>
      <div><b>2. Pagamento</b><span>Combino consigo no WhatsApp e envio os dados na conversa.</span></div>
      <div><b>3. Entrega</b><span>Recebe o .xlsx com o guia de utilização e 7 dias de apoio.</span></div>
    </div>
  </section>
</main>
<script src="/funil.js" defer></script>
"""
    return _shell("Pedido registado — Planilhas Excel Premium", "Confirme o pedido no WhatsApp.", body)


def build_all(products):
    out = {}
    for i, p in enumerate(products, 1):
        out[f"oferta/{i}.html"] = build_offer(i, p, products)
        out[f"oferta/upsell-{i}.html"] = build_upsell(i, p, products)
        out[f"oferta/downsell-{i}.html"] = build_downsell(i, p, products)
    out["oferta/obrigado.html"] = build_thanks(products)
    return out
