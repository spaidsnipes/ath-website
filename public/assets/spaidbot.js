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
    '<form class="sb-form"><label class="sb-label" for="sb-in">Your question</label><textarea id="sb-in" rows="2" maxlength="600" placeholder="Type your question" required></textarea><button type="submit" class="sb-send">Send</button></form>' +
    '<p class="sb-fine">AI answers can be wrong. Don\'t share passwords or card numbers. Not financial advice.</p>';
  document.body.append(fab, panel);
  var log = panel.querySelector('.sb-log'), form = panel.querySelector('form'), input = panel.querySelector('textarea'), send = panel.querySelector('.sb-send');
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
})();
