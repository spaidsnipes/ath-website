// Taproot Interviews (WOWZER 2026-11-12) — client for ATHOS /api/taproot/*. Real answers only; nothing is invented.
(() => {
  const API = window.ATH_API, $ = (s, r = document) => r.querySelector(s);
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const api = async (path, opt = {}) => {
    const r = await fetch(API + path, { ...opt, headers: { "content-type": "application/json" } });
    const j = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(j.error || "Spaidbot couldn't reach the taproot right now.");
    return j;
  };
  const money = (n) => "$" + Number(n).toLocaleString("en-US");

  // 1) owner creates the survey
  const nf = $("#tp-new");
  if (nf) nf.addEventListener("submit", async (e) => {
    e.preventDefault();
    const st = nf.querySelector(".form-status"), b = nf.querySelector("button[type=submit]"), d = Object.fromEntries(new FormData(nf).entries());
    b.disabled = true; st.className = "form-status"; st.textContent = "Spaidbot is writing your question…";
    try {
      const j = await api("/api/taproot/new", { method: "POST", body: JSON.stringify(d) });
      const ask = location.origin + "/taproot/q/?s=" + j.slug, own = location.origin + "/taproot/results/#s=" + j.slug + "&k=" + j.key;
      $("#tp-made").hidden = false; nf.hidden = true;
      $("#tp-question").textContent = "“" + j.question + "”";
      $("#tp-ask").value = ask; $("#tp-own").value = own; $("#tp-own-open").href = own;
      try { localStorage.setItem("ath_taproot_" + j.slug, own); } catch {}
      $("#tp-made").scrollIntoView({ behavior: "smooth", block: "start" });
    } catch (err) { st.className = "form-status err"; st.textContent = err.message; b.disabled = false; }
  });
  document.querySelectorAll("[data-copy]").forEach((btn) => btn.addEventListener("click", async () => {
    const inp = $(btn.dataset.copy); try { await navigator.clipboard.writeText(inp.value); btn.textContent = "Copied"; } catch { inp.select(); }
  }));

  // 2) a customer answers
  const af = $("#tp-answer");
  if (af) {
    const slug = new URLSearchParams(location.search).get("s") || "";
    const head = $("#tp-q");
    if (!/^[a-z0-9]{10}$/.test(slug)) head.textContent = "This survey link isn't complete. Ask the business to send it again.";
    else api("/api/taproot/q/" + slug).then((j) => { head.textContent = j.question; if (j.biz) $("#tp-biz").textContent = j.biz + " is asking"; af.hidden = false; })
      .catch((err) => { head.textContent = err.message; });
    af.addEventListener("submit", async (e) => {
      e.preventDefault();
      const st = af.querySelector(".form-status"), b = af.querySelector("button[type=submit]"), d = Object.fromEntries(new FormData(af).entries());
      b.disabled = true; st.className = "form-status"; st.textContent = "Sending…";
      try { await api("/api/taproot/q/" + slug, { method: "POST", body: JSON.stringify(d) }); af.innerHTML = '<h2 class="display d-m">Thank you.</h2><p class="body">Your answer went straight to the business, with no name attached. That’s how they learn what to build for you.</p>'; }
      catch (err) { st.className = "form-status err"; st.textContent = err.message; b.disabled = false; }
    });
  }

  // 3) owner results + grow the ladder
  const out = $("#tp-results");
  if (out) {
    const h = new URLSearchParams(location.hash.slice(1)), slug = h.get("s") || "", key = h.get("k") || "";
    const draw = (j) => {
      const ask = location.origin + "/taproot/q/?s=" + slug;
      const ans = j.answers.length ? `<ol class="tp-answers">${j.answers.map((a) => `<li id="a${a.n}"><span class="tp-n">${a.n}</span>${esc(a.answer)}</li>`).join("")}</ol>` : `<p class="body">No answers yet. Send this link to your customers: <a class="gold" href="${esc(ask)}">${esc(ask)}</a></p>`;
      const cite = (arr) => arr.map((n) => `<a href="#a${n}" class="tp-cite">#${n}</a>`).join(" ");
      const g = j.grown;
      const grownHtml = !g ? "" : `<div class="grid g3 mt2">${g.themes.map((t) => `<article class="panel panel-pad"><p class="eyebrow">Taproot theme</p><h3>${esc(t.name)}</h3><p>${esc(t.summary)}</p><p class="note">${t.answers.length} answer${t.answers.length > 1 ? "s" : ""}: ${cite(t.answers)}</p></article>`).join("")}</div>
        <h3 class="display d-m mt3">Your offer ladder, grown from their words</h3>
        <div class="tp-ladder mt2">${g.ladder.map((r) => `<div class="tp-rung panel panel-pad"><p class="tp-price">${money(r.price)}</p><div><h4>${esc(r.name)}</h4><p>${esc(r.promise)}</p><p class="note">Because of answers ${cite(r.why)}</p></div></div>`).join("") || '<p class="body">Spaidbot couldn’t tie any rung to a real answer, so it left the ladder empty rather than guess. Collect a few more answers and grow again.</p>'}</div>
        <p class="note mt1">Grown ${new Date(g.at).toLocaleString()} from ${g.count} answers${j.stale ? " · new answers since, grow again to include them" : ""}. Rung prices follow the $100 / $500 / $2,000 ladder (an idea from Myron Golden, in our words); the offers are drafts for you to shape.</p>`;
      out.innerHTML = `<p class="eyebrow">${esc(j.biz || "Your business")} · ${esc(j.market)}</p><h1 class="display d-l mt1">${esc(j.question)}</h1>
        <p class="lede">${j.answers.length} real answer${j.answers.length === 1 ? "" : "s"} so far.</p>
        <div class="panel panel-pad mt2"><label class="lbl" for="tp-ask2">Your survey link (send it to your own customers)</label><div class="tp-copy"><input id="tp-ask2" readonly value="${esc(ask)}"><button class="btn btn-line btn-sm" type="button" data-copy2>Copy</button></div></div>
        <div class="ctas mt2"><button class="btn btn-gold" id="tp-grow" type="button" ${j.answers.length < j.min ? "disabled" : ""}>Grow my offer ladder</button></div>
        <p class="form-status" id="tp-gs" role="status" aria-live="polite">${j.answers.length < j.min ? `Spaidbot grows a ladder from at least ${j.min} real answers. ${j.min - j.answers.length} to go.` : ""}</p>
        ${grownHtml}<h3 class="display d-m mt3">Every answer</h3>${ans}`;
      out.querySelector("[data-copy2]").onclick = async (e) => { try { await navigator.clipboard.writeText(ask); e.target.textContent = "Copied"; } catch {} };
      $("#tp-grow").onclick = async () => {
        const gs = $("#tp-gs"); $("#tp-grow").disabled = true; gs.className = "form-status"; gs.innerHTML = '<span class="spinner"></span>Spaidbot is reading every answer…';
        try { draw(await api(`/api/taproot/r/${slug}/grow?k=${key}`, { method: "POST", body: "{}" })); } catch (err) { gs.className = "form-status err"; gs.textContent = err.message; $("#tp-grow").disabled = false; }
      };
    };
    if (!slug || !key) out.innerHTML = '<p class="body">Open this page from the private owner link you got when you made the survey.</p>';
    else api(`/api/taproot/r/${slug}?k=${key}`).then(draw).catch((err) => { out.innerHTML = `<p class="body">${esc(err.message)}</p>`; });
  }
})();
