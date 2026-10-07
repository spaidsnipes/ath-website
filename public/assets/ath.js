// ATH Official Website — client. Evidence-first: the UI never shows more confidence than the API returned.
(() => {
  const API = window.ATH_API;
  const $ = (s, r = document) => r.querySelector(s);
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

  // menu
  const mb = $(".menu-btn"), nav = $("#nav");
  mb?.addEventListener("click", () => { const o = nav.classList.toggle("open"); mb.setAttribute("aria-expanded", o); });
  document.querySelectorAll("[data-year]").forEach((e) => (e.textContent = new Date().getFullYear()));
  document.querySelectorAll("[data-print]").forEach((b) => b.addEventListener("click", () => window.print()));

  // source attribution carried through the funnel
  const qs = new URLSearchParams(location.search);
  try {
    if (!sessionStorage.getItem("ath_src")) sessionStorage.setItem("ath_src", JSON.stringify({ ref: document.referrer || "", utm: qs.get("utm_source") || "", landing: location.pathname, at: new Date().toISOString() }));
  } catch {}
  const source = () => { try { return JSON.parse(sessionStorage.getItem("ath_src") || "{}"); } catch { return {}; } };

  async function post(path, body) {
    const r = await fetch(API + path, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(body) });
    const j = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(j.error || "ATHOS could not complete that request.");
    return j;
  }

  // ---------------- diagnose intake
  const df = $("#diag-form");
  if (df) {
    const desc = $("#desc"), count = $("#desc-count"), st = $("#diag-status"), go = $("#diag-go");
    desc.addEventListener("input", () => (count.textContent = desc.value.length));
    df.addEventListener("submit", async (e) => {
      e.preventDefault();
      let url = $("#url").value.trim();
      const description = desc.value.trim(), unsure = $("#unsure").checked;
      if (url && !/^https?:\/\//i.test(url)) url = "https://" + url;
      if (!url && !description && !unsure) { st.className = "form-status err"; st.textContent = "Give ATHOS a website, a description, or tick “I don't know what I need yet”."; return; }
      const checks = [...df.querySelectorAll("input[name=checks]:checked")].map((c) => c.value);
      st.className = "form-status"; st.innerHTML = '<span class="spinner"></span>' + (url ? "ATHOS is reading that public page…" : "ATHOS is mapping what you told us…");
      go.disabled = true;
      try {
        const res = await post("/api/diagnose", { url, description, unsure, checks, source: source() });
        try { sessionStorage.setItem("ath_diag", res.id); } catch {}
        location.href = "/diagnose/result/?id=" + encodeURIComponent(res.id);
      } catch (err) { st.className = "form-status err"; st.textContent = err.message; go.disabled = false; }
    });
  }

  // ---------------- result
  const out = $("#result");
  if (out) {
    const id = qs.get("id");
    if (!id) out.innerHTML = '<p class="body">No diagnosis selected. <a class="gold" href="/diagnose/">Start one</a>.</p>';
    else fetch(API + "/api/diagnosis/" + encodeURIComponent(id)).then((r) => r.json()).then((d) => {
      if (!d || d.error) throw new Error(d?.error || "Not found");
      out.innerHTML = renderResult(d);
    }).catch((e) => (out.innerHTML = `<p class="body">We couldn't load that diagnosis (${esc(e.message)}). <a class="gold" href="/diagnose/">Run a new one</a>.</p>`));
  }

  const K = { evidence: ["e", "Evidence"], inference: ["i", "Inference"], reported: ["i", "You told us"], unknown: ["u", "Unknown"] };
  function fnd(f) {
    const [c, l] = K[f.kind] || K.inference;
    return `<div class="finding"><span class="k ${c}"><span class="dot ${c}"></span>${l}</span><b>${esc(f.title)}</b>${f.detail ? `<p>${esc(f.detail)}</p>` : ""}${f.source ? `<div class="src">Source: ${esc(f.source)}</div>` : ""}</div>`;
  }
  function stageMap(stages) {
    // fixed terrain positions (percent of 1000x620); a node lights only when the stage has evidence
    const P = [[110, 520], [330, 470], [470, 330], [640, 250], [780, 160], [900, 80]];
    const pts = P.map((p) => p.join(",")).join(" ");
    const nodes = stages.map((s, i) => {
      const [x, y] = P[i] || P[P.length - 1];
      const lit = s.state === "evidence", inf = s.state === "inference";
      const r = lit ? 9 : 7;
      return `<g><circle cx="${x}" cy="${y}" r="${r + 10}" fill="${lit ? "rgba(230,200,138,.18)" : "none"}"/>
        <circle cx="${x}" cy="${y}" r="${r}" fill="${lit ? "#e6c88a" : "#0b0c10"}" stroke="${lit ? "#f4dfae" : inf ? "#b9a27a" : "#7d8696"}" stroke-width="2" ${!lit && !inf ? 'stroke-dasharray="3 3"' : ""}/>
        <text class="node-label" x="${x + 16}" y="${y - 4}">${esc(s.name)}</text><text class="node-sub" x="${x + 16}" y="${y + 12}">${esc(s.note)}</text></g>`;
    }).join("");
    return `<div class="map"><img src="/assets/art/home.webp" alt=""><svg viewBox="0 0 1000 620" role="img" aria-label="Opportunity map: lit stages are supported by evidence; dashed stages are unknown">
      <polyline points="${pts}" fill="none" stroke="rgba(230,200,138,.25)" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
      <polyline points="${pts}" fill="none" stroke="#e6c88a" stroke-width="2" stroke-dasharray="2 8" stroke-linecap="round"/>${nodes}</svg></div>`;
  }
  function renderResult(d) {
    const ev = d.findings.filter((f) => f.kind === "evidence"), inf = d.findings.filter((f) => f.kind === "inference" || f.kind === "reported"), unk = d.findings.filter((f) => f.kind === "unknown");
    const rec = d.route?.door;
    const door = (k, title, text, href) => `<a class="door${rec === k ? " rec" : ""}" href="${href}">${rec === k ? '<span class="tag live">Recommended</span>' : '<span class="tag dim">Option</span>'}<h3>${title}</h3><p>${text}</p></a>`;
    const leadHref = `/contact/?intent=services&diagnosis=${encodeURIComponent(d.id)}`;
    return `
    <h1 class="display d-m">Your hill map</h1>
    <p class="body">${d.target ? `Public page inspected: <b>${esc(d.target)}</b> · ` : "No website inspected — built only from what you told us · "}${esc(new Date(d.created_at).toLocaleString())}</p>
    <div class="legend mt1"><span><span class="dot e"></span>Evidence — observed</span><span><span class="dot i"></span>Inference — reasoned from evidence</span><span><span class="dot u"></span>Unknown / needs input</span></div>
    <div class="grid mt2" style="grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);gap:18px" data-collapse>
      <div class="grid" style="gap:18px;align-content:start">
        <div class="panel panel-pad"><p class="panel-title">What's working</p>${d.working.length ? d.working.map(fnd).join("") : '<p class="body mb0">Nothing we could confirm from public evidence. That is not the same as nothing working.</p>'}</div>
        <div class="panel panel-pad"><p class="panel-title">The hill · primary obstacle</p><p class="h-serif" style="font-size:24px">${esc(d.hill.title)}</p><p class="body mb0">${esc(d.hill.detail)}</p>${d.hill.term ? `<p class="note mt1 mb0">ATH term: <a class="gold" href="/language/#samples">${esc(d.hill.term)}</a></p>` : ""}</div>
      </div>
      <div class="panel panel-pad"><p class="panel-title">Opportunity map · your path above</p>${stageMap(d.stages)}
        <ol class="mt2" style="color:var(--ivory-dim);padding-left:20px">${d.sequence.map((s) => `<li style="margin:6px 0">${esc(s)}</li>`).join("")}</ol></div>
    </div>
    <div class="grid g3 mt2">
      <div class="panel panel-pad"><p class="panel-title">Evidence (${ev.length})</p>${ev.map(fnd).join("") || '<p class="body mb0">None observed.</p>'}</div>
      <div class="panel panel-pad"><p class="panel-title">Inferences (${inf.length})</p>${inf.map(fnd).join("") || '<p class="body mb0">None.</p>'}</div>
      <div class="panel panel-pad"><p class="panel-title">Unknowns · needs input (${unk.length})</p>${unk.map(fnd).join("")}</div>
    </div>
    <div class="panel panel-pad mt2"><p class="panel-title">Recommended ATH path</p><p class="h-serif" style="font-size:24px">${esc(d.route.title)}</p><p class="body mb0">${esc(d.route.why)}</p></div>
    <p class="panel-title mt3">Choose how to cross it</p>
    <div class="doors">
      ${door("diy", "Do it myself", "Use these findings with your own team and tools. The Builder Dictionary helps you and your AI speak precisely.", "/language/")}
      ${door("world", "Join the world", "Passport identity and World Pass membership — the connected ATH ecosystem.", "/passport/")}
      ${door("build", "Build it for me", "ATH scopes, quotes and implements. This diagnosis travels with your request.", leadHref)}
    </div>
    <p class="note mt2">Need more depth? <a class="gold" href="/diagnose/deep/">Deep diagnostic — open the hood</a>. Visual elements on this page are a metaphor; only items labelled Evidence are observations.</p>
    <style>@media (max-width:860px){[data-collapse]{grid-template-columns:1fr!important}}</style>`;
  }

  // ---------------- lead forms (contact + deep)
  for (const f of document.querySelectorAll("#lead-form, #deep-form")) {
    const sel = f.querySelector("select[name=intent]");
    if (sel && qs.get("intent")) sel.value = qs.get("intent");
    f.addEventListener("submit", async (e) => {
      e.preventDefault();
      const st = f.querySelector(".form-status"), b = f.querySelector("button[type=submit]");
      const fd = new FormData(f);
      const data = Object.fromEntries(fd.entries());
      data.sources = fd.getAll("sources");
      if (!data.name?.trim() || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(data.email || "")) { st.className = "form-status err"; st.textContent = "Please add your name and a valid email."; return; }
      let diag = qs.get("diagnosis"); try { diag = diag || sessionStorage.getItem("ath_diag"); } catch {}
      b.disabled = true; st.className = "form-status"; st.innerHTML = '<span class="spinner"></span>Sending…';
      try {
        await post("/api/lead", { ...data, diagnosis_id: diag || null, source: source(), page: location.pathname });
        f.innerHTML = `<p class="panel-title">Received</p><p class="h-serif" style="font-size:26px">Thank you — a person at ATH will reply to ${esc(data.email)}.</p><p class="body">Nothing has been charged and no access has been granted.</p>`;
      } catch (err) { st.className = "form-status err"; st.textContent = err.message; b.disabled = false; }
    });
  }
})();
