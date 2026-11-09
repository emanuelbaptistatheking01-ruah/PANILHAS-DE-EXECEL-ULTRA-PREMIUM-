/* Funil de venda — front-end.
   Todos os botões pedem o pedido ao servidor (/api/checkout), que valida o
   preço. Só depois é que o cliente é levado para o WhatsApp.
   Se o endpoint falhar, há um fallback local para não perder a venda. */
(function () {
  var KEY = 'mb_pedido';

  function money(v) {
    return String(v).replace(/\B(?=(\d{3})+(?!\d))/g, '.');
  }

  function load() {
    try {
      return JSON.parse(localStorage.getItem(KEY) || '{}') || {};
    } catch (e) {
      return {};
    }
  }

  function save(o) {
    try { localStorage.setItem(KEY, JSON.stringify(o)); } catch (e) {}
  }

  function param(name) {
    return new URLSearchParams(location.search).get(name);
  }

  async function checkout(items) {
    var r = await fetch('/api/checkout', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        items: items,
        nome: (document.getElementById('nome') || {}).value || '',
        tel: (document.getElementById('tel') || {}).value || '',
        pagina: location.pathname,
      }),
    });
    if (!r.ok) throw new Error('HTTP ' + r.status);
    return r.json();
  }

  function fallback(items) {
    var total = items.reduce(function (s, i) { return s + i.price; }, 0);
    var msg =
      'Olá! Quero comprar:\n' +
      items.map(function (i) { return '• ' + i.title + ' — ' + money(i.price) + ' Kz'; }).join('\n') +
      '\n\nTotal: ' + money(total) + ' Kz';
    return {
      ok: true,
      ref: 'LOCAL-' + Date.now().toString(36).toUpperCase(),
      total: total,
      wa: 'https://wa.me/244942739225?text=' + encodeURIComponent(msg),
    };
  }

  function busy(el, on) {
    if (!el) return;
    el.style.opacity = on ? '.65' : '';
    el.style.pointerEvents = on ? 'none' : '';
  }

  document.addEventListener('DOMContentLoaded', function () {
    var pedido = load();
    var base = [];

    // ---- formulário da página de oferta
    var form = document.querySelector('form[data-checkout]');
    if (form) {
      form.addEventListener('submit', async function (ev) {
        ev.preventDefault();
        var btn = form.querySelector('button[type=submit]');
        var id = Number(form.dataset.product);
        var title = document.querySelector('.offer h1');
        var items = [{ id: id, title: title ? title.textContent.trim() : 'Planilha', price: Number(form.dataset.price) }];

        busy(btn, true);
        var data;
        try {
          data = await checkout(items);
        } catch (e) {
          data = fallback(items);
        }
        busy(btn, false);

        save({ ref: data.ref, items: items, total: data.total, wa: data.wa, up: 0 });
        location.href = form.dataset.next || 'obrigado.html';
      });
      return;
    }

    // ---- botão de upsell
    var up = document.querySelector('[data-upsell]');
    if (up) {
      base = pedido.items || [];
      up.addEventListener('click', async function (ev) {
        ev.preventDefault();
        var id = Number(up.dataset.product);
        var items = base.concat([{ id: id, title: up.textContent.trim().split('—')[0].trim(), price: Number(up.dataset.price) }]);
        busy(up, true);
        var data;
        try { data = await checkout(items); } catch (e) { data = fallback(items); }
        busy(up, false);
        save({ ref: data.ref, items: items, total: data.total, wa: data.wa, up: 1 });
        location.href = 'obrigado.html?u=1';
      });
      return;
    }

    // ---- botão de downsell (substitui o item base)
    var down = document.querySelector('[data-downsell]');
    if (down) {
      down.addEventListener('click', async function (ev) {
        ev.preventDefault();
        var id = Number(down.dataset.product);
        var b = Number(down.dataset.base);
        var items = (pedido.items || []).filter(function (i) { return i.id !== id; });
        if (!items.some(function (i) { return i.id === b; })) {
          items.push({ id: b, title: 'Planilha ' + b, price: 0 });
        }
        items = [{ id: id, title: down.textContent.trim().split('—')[0].trim(), price: Number(down.dataset.price) }];
        busy(down, true);
        var data;
        try { data = await checkout(items); } catch (e) { data = fallback(items); }
        busy(down, false);
        save({ ref: data.ref, items: items, total: data.total, wa: data.wa, up: 0 });
        location.href = 'obrigado.html?d=1';
      });
      return;
    }

    // ---- página de obrigado
    var ordem = document.getElementById('ordem');
    if (ordem) {
      var p = load();
      ordem.textContent = p.ref || '—';
      var wa = document.getElementById('wa-final');
      if (wa && p.wa) wa.href = p.wa;
      if (!p.ref) {
        var t = document.querySelector('.thanks p');
        if (t) t.textContent = 'Não encontrei nenhum pedido guardado neste dispositivo. Volte à oferta e preencha o formulário.';
      }
    }
  });
})();
