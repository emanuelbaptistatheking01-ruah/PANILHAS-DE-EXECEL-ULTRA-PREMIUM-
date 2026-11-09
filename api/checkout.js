// POST /api/checkout
// Valida o produto e o preço no servidor, regista o pedido e devolve a
// referência com que o cliente segue para o WhatsApp.
//
// Nunca confia no preço que vem do browser: usa a tabela PRICES abaixo.
// Persistência: Vercel Blob (BLOB_READ_WRITE_TOKEN). Sem token, o endpoint
// continua a responder com uma referência, mas não guarda nada.

const PRICES = {
  1: 12000, 2: 15000, 3: 10000, 4: 20000, 5: 8000, 6: 12000,
  7: 6000, 8: 8000, 9: 5000, 10: 7000, 11: 25000, 12: 35000,
  13: 25000, 14: 12000, 15: 10000, 16: 8000, 17: 10000, 18: 8000,
};

const TITLES = {
  1: 'Folha de Salário Angola',
  2: 'Gestão Empresarial: Caixa, Stock e Vendas',
  3: 'Calculadora de Impostos Angola',
  4: 'Contabilidade SNC Completa',
  5: 'Diário de Controle de Obra',
  6: 'Orçamento de Obra + Materiais',
  7: 'Comparador de Preços de Fornecedores',
  8: 'Finanças Pessoais Angola',
  9: 'Planner de Hábitos e Devocional',
  10: 'Custos de Receitas Angolanas',
  11: 'Gestão de Centro de Formação Técnico-Profissional',
  12: 'Sistema de Propinas KIAZOP',
  13: 'Gestão de Escola',
  14: 'Controle de Alunos e Notas',
  15: 'Cobrança de Mensalidade Escolar',
  16: 'Controle de Presença de Formandos',
  17: 'Gestão de Certificates',
  18: 'Controle de Salas e Horários',
};

const WA = '244942739225';
const HOST = 'https://planilhas-ultra-angola-emanuelbaptistatheking01-9378.vercel.app';

function ref() {
  const d = new Date();
  const ymd = d.toISOString().slice(0, 10).replace(/-/g, '');
  const rnd = Math.random().toString(36).slice(2, 6).toUpperCase();
  return `MB-${ymd}-${rnd}`;
}

function money(v) {
  return v.toLocaleString('pt-PT').replace(/\u00A0/g, '.');
}

async function store(order) {
  const token = process.env.BLOB_READ_WRITE_TOKEN;
  if (!token) return { saved: false, reason: 'sem BLOB_READ_WRITE_TOKEN' };
  try {
    const { put } = await import('@vercel/blob');
    const path = `pedidos/${order.ref}.json`;
    await put(path, JSON.stringify(order, null, 2), {
      access: 'public',
      token,
      contentType: 'application/json',
      addRandomSuffix: false,
      allowOverwrite: true,
    });
    return { saved: true, path };
  } catch (e) {
    return { saved: false, reason: String(e && e.message ? e.message : e) };
  }
}

export default async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method !== 'POST') {
    res.status(405).json({ ok: false, error: 'Use POST.' });
    return;
  }

  let body = req.body;
  if (typeof body === 'string') {
    try { body = JSON.parse(body); } catch { body = {}; }
  }
  body = body || {};

  const items = Array.isArray(body.items) ? body.items.slice(0, 5) : [];
  if (!items.length) {
    res.status(400).json({ ok: false, error: 'Pedido sem itens.' });
    return;
  }

  const clean = [];
  for (const it of items) {
    const id = Number(it && it.id);
    if (!PRICES[id]) {
      res.status(400).json({ ok: false, error: `Produto inválido: ${it && it.id}` });
      return;
    }
    if (!clean.some((c) => c.id === id)) {
      clean.push({ id, title: TITLES[id], price: PRICES[id] });
    }
  }

  const total = clean.reduce((s, c) => s + c.price, 0);
  const nome = String(body.nome || '').trim().slice(0, 80);
  const tel = String(body.tel || '').trim().slice(0, 30);

  const order = {
    ref: ref(),
    criado: new Date().toISOString(),
    nome,
    tel,
    items: clean,
    total,
    pagina: String(body.pagina || '').slice(0, 200),
    userAgent: String(req.headers['user-agent'] || '').slice(0, 200),
  };

  const salvo = await store(order);

  // mensagem de WhatsApp pronta, com preço calculado no servidor
  const linhas = clean
    .map((c) => `• ${c.title} — ${money(c.price)} Kz`)
    .join('\n');
  const msg =
    `Olá! Quero comprar:\n${linhas}\n\n` +
    `Total: ${money(total)} Kz\n` +
    `Encomenda: ${order.ref}\n` +
    (nome ? `Nome: ${nome}\n` : '') +
    (tel ? `Contacto: ${tel}\n` : '') +
    `🔗 ${HOST}/oferta/${clean[0].id}.html`;

  order.wa = `https://wa.me/${WA}?text=${encodeURIComponent(msg)}`;

  res.status(200).json({
    ok: true,
    ref: order.ref,
    total,
    items: clean,
    wa: order.wa,
    saved: salvo.saved,
    note: salvo.saved ? undefined : salvo.reason,
  });
}
