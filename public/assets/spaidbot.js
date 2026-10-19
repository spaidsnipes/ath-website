// Spaidbot: ATH's free AI assistant. Answers come from ATHOS (/api/spaidbot), grounded in /catalog.json.
(function () {
  if (document.querySelector('.sb-fab')) return;
  var API = (window.ATH_API || 'https://mission.abovethehilldev.online') + '/api/spaidbot';
  var history = [];
  var fab = document.createElement('button');
  fab.className = 'sb-fab'; fab.type = 'button'; fab.setAttribute('aria-expanded', 'false'); fab.setAttribute('aria-controls', 'sb-panel');
  fab.innerHTML = '<span class="sb-dot" aria-hidden="true"></span>Ask Spaidbot';
  var panel = document.createElement('section');
  panel.className = 'sb-panel'; panel.id = 'sb-panel'; panel.hidden = true; panel.setAttribute('aria-label', 'Spaidbot, ATH AI assistant');
  panel.innerHTML =
    '<header class="sb-head"><div><p class="sb-name">Spaidbot</p><p class="sb-sub">ATH\'s AI assistant · free · answers from our live price list</p></div>' +
    '<button type="button" class="sb-x" aria-label="Close Spaidbot">×</button></header>' +
    '<div class="sb-log" role="log" aria-live="polite"><p class="sb-msg sb-bot">Hi, I\'m Spaidbot, an AI. Ask me which website package fits your business, what WAVEMOTION or Wealthy Mindsets Pro cost, or how to start.</p>' +
    '<div class="sb-chips"><button type="button">Which website fits my business?</button><button type="button">What does $100 get me?</button><button type="button">What is WAVEMOTION?</button></div></div>' +
    '<form class="sb-lead" hidden><p class="sb-lead-h">Start my site. ATH replies within one business day.</p>' +
    '<label for="sb-l-name">Your name</label><input id="sb-l-name" autocomplete="name" required maxlength="120">' +
    '<label for="sb-l-email">Email</label><input id="sb-l-email" type="email" autocomplete="email" required maxlength="200">' +
    '<label for="sb-l-biz">Business name and city</label><input id="sb-l-biz" autocomplete="organization" maxlength="160">' +
    '<label for="sb-l-phone">Phone (optional)</label><input id="sb-l-phone" type="tel" autocomplete="tel" maxlength="40">' +
    '<label for="sb-l-pkg">What you want</label><select id="sb-l-pkg"><option value="quick-start">Quick Start website · $100</option><option value="business-growth">Business Growth website · $200</option><option value="cinematic-launch">Website + promo videos · $500–$700</option><option value="custom">Not sure yet</option></select>' +
    '<input class="sb-hp" tabindex="-1" autocomplete="off" aria-hidden="true" name="company_fax">' +
    '<div class="sb-lead-row"><button type="submit" class="sb-send">Send to ATH</button><button type="button" class="sb-cancel">Back to chat</button></div>' +
    '<p class="sb-fine" style="padding:0">Nothing is charged. We use this only to reply about your site.</p></form>' +
    '<form class="sb-form"><label class="sb-label" for="sb-in">Your question</label><textarea id="sb-in" rows="2" maxlength="600" placeholder="Type your question" required></textarea><button type="submit" class="sb-send">Send</button></form>' +
    '<button type="button" class="sb-start">Start my site →</button>' +
    '<p class="sb-fine">AI answers can be wrong. Don\'t share passwords or card numbers. Not financial advice.</p>';
  document.body.append(fab, panel);
  var log = panel.querySelector('.sb-log'), form = panel.querySelector('form.sb-form'), input = panel.querySelector('textarea'), send = panel.querySelector('.sb-form .sb-send');
  function open(v) { panel.hidden = !v; fab.setAttribute('aria-expanded', String(v)); if (v) input.focus(); else fab.focus(); }
  fab.addEventListener('click', function () { open(panel.hidden); });
  panel.querySelector('.sb-x').addEventListener('click', function () { open(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !panel.hidden) open(false); });
  function linkify(text) {
    var p = document.createElement('p');
    text.split(/(https:\/\/[^\s)]+)/g).forEach(function (part, i) {
      if (i % 2) { var a = document.createElement('a'); a.href = part.replace(/[.,]$/, ''); a.textContent = part.replace(/[.,]$/, ''); a.rel = 'noopener'; if (!/abovethehilldev\.online/.test(part)) a.target = '_blank'; p.append(a); if (/[.,]$/.test(part)) p.append(part.slice(-1)); }
      else p.append(part);
    });
    return p;
  }
  function add(role, text) { var p = linkify(text); p.className = 'sb-msg ' + (role === 'user' ? 'sb-me' : 'sb-bot'); log.append(p); log.scrollTop = log.scrollHeight; return p; }
  async function ask(q) {
    q = q.trim(); if (!q) return;
    var chips = log.querySelector('.sb-chips'); if (chips) chips.remove();
    add('user', q); history.push({ role: 'user', content: q });
    input.value = ''; send.disabled = true;
    var wait = add('bot', 'Thinking…'); wait.classList.add('sb-wait');
    try {
      var r = await fetch(API, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ messages: history.slice(-8) }) });
      var b = await r.json().catch(function () { return {}; });
      wait.remove();
      if (r.ok && b.reply) { add('bot', b.reply); history.push({ role: 'assistant', content: b.reply }); }
      else { history.pop(); add('bot', b.error || 'Spaidbot couldn\'t answer. Please use https://abovethehilldev.online/contact/'); }
    } catch (e) { wait.remove(); history.pop(); add('bot', 'Spaidbot couldn\'t connect. Please try again, or use https://abovethehilldev.online/contact/'); }
    send.disabled = false; input.focus();
  }
  form.addEventListener('submit', function (e) { e.preventDefault(); ask(input.value); });
  input.addEventListener('keydown', function (e) { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); ask(input.value); } });
  log.addEventListener('click', function (e) { if (e.target.matches('.sb-chips button')) ask(e.target.textContent); });
  var lead = panel.querySelector('.sb-lead'), start = panel.querySelector('.sb-start');
  function showLead(v) { lead.hidden = !v; form.hidden = v; start.hidden = v; log.hidden = v; if (v) lead.querySelector('#sb-l-name').focus(); else input.focus(); }
  start.addEventListener('click', function () { showLead(true); });
  lead.querySelector('.sb-cancel').addEventListener('click', function () { showLead(false); });
  lead.addEventListener('submit', async function (e) {
    e.preventDefault();
    var v = function (id) { return lead.querySelector(id).value.trim(); };
    var btn = lead.querySelector('.sb-send'); btn.disabled = true;
    var q = new URLSearchParams(location.search), src = {};
    ['utm_source', 'utm_campaign', 'utm_medium'].forEach(function (k) { if (q.get(k)) src[k] = q.get(k).slice(0, 80); });
    src.referrer = document.referrer.slice(0, 200); src.via = 'spaidbot';
    var chat = history.filter(function (m) { return m.role === 'user'; }).map(function (m) { return '- ' + m.content; }).join('\n').slice(0, 1500);
    var pkg = v('#sb-l-pkg');
    try {
      var r = await fetch((window.ATH_API || 'https://mission.abovethehilldev.online') + '/api/lead', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({
        name: v('#sb-l-name'), email: v('#sb-l-email'), org: v('#sb-l-biz'), intent: 'services', package: pkg, page: 'spaidbot:' + location.pathname.slice(0, 60),
        message: 'Via Spaidbot.' + (v('#sb-l-phone') ? ' Phone: ' + v('#sb-l-phone') + '.' : '') + (chat ? '\nAsked Spaidbot:\n' + chat : ''),
        company_fax: lead.querySelector('.sb-hp').value, source: src }) });
      var b = await r.json().catch(function () { return {}; });
      btn.disabled = false;
      if (!r.ok || !b.ok) { add('bot', b.error || 'That didn\'t send. Please try again, or use https://abovethehilldev.online/contact/'); showLead(false); return; }
      showLead(false); lead.reset();
      var pay = { 'quick-start': 'https://buy.stripe.com/3cI4gA1KkdPkbvJ2oG97G00', 'business-growth': 'https://buy.stripe.com/eVq4gAcoY4eKarF1kC97G01' }[pkg];
      add('bot', 'Got it. ATH has your details and will reply within one business day.' + (pay ? ' Ready to start now? Pay securely through Stripe here: ' + pay : ''));
    } catch (err) { btn.disabled = false; showLead(false); add('bot', 'That didn\'t send. Please try again, or use https://abovethehilldev.online/contact/'); }
  });
})();
