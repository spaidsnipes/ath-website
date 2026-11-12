// Line Check + Key Fob Tour (WOWZER lab, 2026-11-12). Evidence-first like ath.js: every lit checkpoint and every lit
// room is a measurement taken just now; anything not measured says so. No prices on these pages (value before price).
(() => {
  const API = window.ATH_API;
  const $ = (s, r = document) => r.querySelector(s);
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const qs = new URLSearchParams(location.search);
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const calm = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const store = { get(k) { try { return JSON.parse(sessionStorage.getItem(k) || "null"); } catch { return null; } }, set(k, v) { try { sessionStorage.setItem(k, JSON.stringify(v)); } catch {} } };
  const source = () => store.get("ath_src") || {};

  // Rented addresses: the business is reached through someone else's building (the "shared line").
  const PLATFORMS = [
    [/(^|\.)(facebook|fb)\.com$/, "Facebook"], [/(^|\.)instagram\.com$/, "Instagram"], [/(^|\.)tiktok\.com$/, "TikTok"], [/(^|\.)(x|twitter)\.com$/, "X"],
    [/(^|\.)youtube\.com$|(^|\.)youtu\.be$/, "YouTube"], [/(^|\.)linkedin\.com$/, "LinkedIn"], [/(^|\.)yelp\.com$/, "Yelp"], [/(^|\.)nextdoor\.com$/, "Nextdoor"],
    [/(^|\.)linktr\.ee$/, "Linktree"], [/(^|\.)beacons\.ai$/, "Beacons"], [/(^|\.)stan\.store$/, "Stan"], [/^g\.page$|(^|\.)business\.site$|^maps\.app\.goo\.gl$|^goo\.gl$|^share\.google$|^maps\.google\./, "Google"],
    [/(^|\.)(doordash|ubereats|grubhub|toasttab|vagaro|styleseat|booksy|square\.site|clover|fresha|glossgenius|gettimely|setmore|schedulicity|mindbodyonline|acuityscheduling|booker|squareup)\.com$|\.square\.site$/, "a booking or ordering app"],
  ];
  const BUILDERS = [
    [/\.wixsite\.com$/, "Wix"], [/\.godaddysites\.com$/, "GoDaddy"], [/\.weebly\.com$/, "Weebly"], [/\.wordpress\.com$/, "WordPress.com"], [/\.squarespace\.com$/, "Squarespace"],
    [/\.myshopify\.com$/, "Shopify"], [/\.webflow\.io$/, "Webflow"], [/\.carrd\.co$/, "Carrd"], [/\.blogspot\.com$/, "Blogger"], [/\.(netlify\.app|vercel\.app|github\.io|pages\.dev)$/, "a free host"], [/\.framer\.(website|app)$/, "Framer"], [/\.ueniweb\.com$/, "UENI"],
  ];

  function parseTarget(raw) {
    let s = String(raw || "").trim();
    if (!s) return null;
    if (/^@[\w.]{2,}$/.test(s)) s = "https://instagram.com/" + s.slice(1);
    if (!/^https?:\/\//i.test(s)) s = "https://" + s;
    try { const u = new URL(s); if (!/\./.test(u.hostname)) return null; return u; } catch { return null; }
  }
  function classify(u) {
    const h = u.hostname.replace(/^www\./, "").toLowerCase();
    for (const [re, name] of PLATFORMS) if (re.test(h)) return { host: h, kind: "platform", who: name };
    for (const [re, name] of BUILDERS) if (re.test(h)) return { host: h, kind: "builder", who: name };
    return { host: h, kind: "own", who: null };
  }
  async function dns(name, type) {
    try {
      const r = await fetch(`https://cloudflare-dns.com/dns-query?name=${encodeURIComponent(name)}&type=${type}`, { headers: { accept: "application/dns-json" } });
      if (!r.ok) return null;
      const j = await r.json();
      return { status: j.Status, answers: (j.Answer || []).map((a) => String(a.data || "")) };
    } catch { return null; }
  }
  const apex = (h) => h.split(".").slice(-2).join("."); // good enough for .com/.net/.online-style names; noted as such on screen
  async function athos(url) {
    const r = await fetch(API + "/api/diagnose", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ url, checks: ["structure", "conversion", "messaging", "brand"], source: { ...source(), tool: "line-check" } }) });
    const j = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(j.error || "ATHOS could not read that page right now.");
    const d = await (await fetch(API + "/api/diagnosis/" + encodeURIComponent(j.id))).json();
    return d;
  }
  const allF = (d) => [...(d.findings || []), ...(d.working || [])];
  const has = (d, re) => [...allF(d), ...(d.hill ? [d.hill] : [])].find((f) => re.test(f.title || ""));

  // ------------------------------------------------------------------ Line Check
  const form = $("#lc-form");
  if (form) {
    const svg = $("#lc-svg"), list = $("#lc-points"), verdict = $("#lc-verdict"), st = $("#lc-status"), go = $("#lc-go"), next = $("#lc-next");
    const PTS = [
      ["addr", "Your address", "Do customers reach you at your own address — or someone else's?"],
      ["answer", "It answers", "Does your own address answer, and how fast?"],
      ["secure", "Secure line", "Does it open without a “Not secure” warning?"],
      ["phone", "Phone-ready", "Is the page set up for phones?"],
      ["reach", "A way to reach you", "Call, book, buy, message: is there a next step?"],
      ["mail", "Email on your name", "Does your email run on your own address?"],
      ["guard", "Name protected", "Can scammers easily send email pretending to be you?"],
    ];
    list.innerHTML = PTS.map(([k, t, q], i) => `<li class="lc-pt" data-k="${k}" data-s="wait"><span class="lc-dot" aria-hidden="true">${i + 1}</span><div><b>${t}</b><p class="lc-q">${q}</p><p class="lc-a" aria-live="polite">Waiting…</p></div></li>`).join("");
    const nodes = PTS.map((_, i) => 40 + i * (520 / (PTS.length - 1)));
    svg.innerHTML = `<defs><linearGradient id="lcg" x1="0" x2="1"><stop offset="0" stop-color="#8a6a2f"/><stop offset="1" stop-color="#f3dca0"/></linearGradient><filter id="lcglow"><feGaussianBlur stdDeviation="3.2"/></filter></defs>
      <path id="lc-coax" d="M40 104 C 150 70, 220 140, 330 100 S 470 70, 560 104" fill="none" stroke="#6b5a3b" stroke-width="2" opacity=".0"/>
      <g id="lc-houses" opacity="0">${[0, 1, 2, 3, 4].map((i) => `<g transform="translate(${370 + i * 40},${i % 2 ? 128 : 116})"><path d="M0 10 L9 2 L18 10 V20 H0Z" fill="#14161b" stroke="#c9a45c" stroke-width="1.2"/><rect x="7" y="13" width="4" height="7" fill="#e6c88a"/></g>`).join("")}</g>
      <line x1="40" y1="60" x2="560" y2="60" stroke="rgba(201,164,92,.18)" stroke-width="2"/>
      <line id="lc-fiber" x1="40" y1="60" x2="40" y2="60" stroke="url(#lcg)" stroke-width="3.5" stroke-linecap="round"/>
      <line id="lc-fiber-glow" x1="40" y1="60" x2="40" y2="60" stroke="#f3dca0" stroke-width="7" opacity=".45" filter="url(#lcglow)"/>
      ${nodes.map((x, i) => `<g class="lc-node" data-i="${i}"><circle cx="${x}" cy="60" r="11" fill="#0c0d11" stroke="rgba(201,164,92,.45)" stroke-width="1.5"/><circle class="core" cx="${x}" cy="60" r="5" fill="#2a2418"/></g>`).join("")}`;
    const fiber = $("#lc-fiber", svg), glow = $("#lc-fiber-glow", svg);
    const COLORS = { pass: "#f3dca0", warn: "#d9a441", fail: "#b8573f", unknown: "#5d5a52" };
    function light(i, s, text) {
      const li = list.children[i], node = svg.querySelectorAll(".lc-node")[i];
      li.dataset.s = s; li.querySelector(".lc-a").innerHTML = text;
      node.querySelector(".core").setAttribute("fill", COLORS[s]);
      node.querySelector("circle").setAttribute("stroke", s === "pass" ? "#f3dca0" : COLORS[s]);
      if (s === "pass") node.classList.add("lit"); else node.classList.remove("lit");
      const reach = s === "pass" ? nodes[i] : null;
      if (reach && i === Number(fiber.dataset.n || 0)) { fiber.setAttribute("x2", reach); glow.setAttribute("x2", reach); fiber.dataset.n = i + 1; }
    }
    function reset() {
      [...list.children].forEach((li) => { li.dataset.s = "wait"; li.querySelector(".lc-a").textContent = "Waiting…"; });
      svg.querySelectorAll(".lc-node").forEach((n) => { n.classList.remove("lit"); n.querySelector(".core").setAttribute("fill", "#2a2418"); n.querySelector("circle").setAttribute("stroke", "rgba(201,164,92,.45)"); });
      fiber.setAttribute("x2", 40); glow.setAttribute("x2", 40); fiber.dataset.n = 0;
      $("#lc-coax", svg).setAttribute("opacity", "0"); $("#lc-houses", svg).setAttribute("opacity", "0");
      verdict.hidden = true; next.hidden = true;
    }
    const step = () => sleep(calm ? 0 : 420);

    async function run(raw, biz) {
      const u = parseTarget(raw);
      if (!u) { st.className = "form-status err"; st.textContent = "Type the link people use to find the business: a website, or a Facebook / Instagram / Yelp page."; return; }
      reset(); go.disabled = true; st.className = "form-status"; st.innerHTML = '<span class="spinner"></span>Checking the line… (about 15 seconds)';
      const t0 = performance.now();
      const c = classify(u), res = { at: new Date().toISOString(), input: u.href, host: c.host, kind: c.kind, who: c.who, biz: biz || "", points: {} };
      const put = (i, s, text) => { res.points[PTS[i][0]] = { s, text: text.replace(/<[^>]+>/g, "") }; light(i, s, text); };
      // 1 address
      if (c.kind === "platform") put(0, "fail", `<b>Shared line.</b> This link lives on ${esc(c.who)} (${esc(c.host)}). Customers reach you inside someone else's building, next to your competitors, under their rules.`);
      else if (c.kind === "builder") put(0, "warn", `<b>Rented address.</b> ${esc(c.host)} is a ${esc(c.who)} address, not your own name. It works, but the building's name is on the door.`);
      else put(0, "pass", `<b>Your own address:</b> ${esc(c.host)}.`);
      await step();
      // 2–5 page evidence from the ATHOS reader (not for social platforms: they don't let readers in, and it isn't your page)
      let d = null;
      if (c.kind !== "platform") {
        try { d = await athos(u.href); res.diagnosis = d.id; } catch (e) { res.readerError = e.message; }
      }
      if (!d) {
        const why = c.kind === "platform" ? "There's no page of your own to test: this address belongs to " + esc(c.who) + "." : esc(res.readerError || "ATHOS couldn't read it right now.");
        [1, 2, 3, 4].forEach((i) => put(i, c.kind === "platform" ? "fail" : "unknown", why));
      } else {
        const ans = has(d, /^Page answered/), down = has(d, /could not be read/);
        if (ans) { const m = ans.title.match(/in (under 0\.1|[\d.]+) seconds/); const sec = m ? (m[1] === "under 0.1" ? 0.1 : parseFloat(m[1])) : null; res.answerSec = sec;
          put(1, sec != null && sec > 2.5 ? "warn" : "pass", `<b>${esc(ans.title)}.</b> ${sec != null && sec > 2.5 ? "Slow enough that people on a phone may leave first." : ""} <span class="lc-src">Measured by the ATHOS reader just now.</span>`); }
        else if (down) put(1, "fail", `<b>Not answering.</b> ${esc(down.title)}. Visitors may be hitting the same wall.`);
        else put(1, "unknown", "ATHOS couldn't tell whether it answered.");
        await step();
        const sec = has(d, /Secure connection/);
        put(2, sec ? "pass" : (ans ? "fail" : "unknown"), sec ? "<b>Yes.</b> It opens on HTTPS, so visitors don't see a “Not secure” warning." : ans ? "<b>No.</b> Browsers label it “Not secure”, which costs trust at first glance." : "Unknown: the page didn't answer.");
        await step();
        const blind = has(d, /rendered by JavaScript|could not be read|complete inspection/i);
        const vp = has(d, /Mobile viewport is set/);
        put(3, vp ? "pass" : blind || !ans ? "unknown" : "fail", vp ? "<b>Yes.</b> The page tells phones to fit the screen." : blind || !ans ? "Unknown: ATHOS couldn't see enough of the page to say." : "<b>No.</b> There's no phone setting, so phones may show a shrunken desktop page.");
        await step();
        const act = has(d, /Visitors have a way to act/), contact = has(d, /Direct contact links/), readable = ans && !blind;
        put(4, act ? "pass" : readable ? "fail" : "unknown", act ? `<b>Yes.</b> ${esc(act.detail)}${contact ? " " + esc(contact.title) + "." : ""}` : readable ? "<b>Not clearly.</b> ATHOS found no button, form, phone or email link that tells a visitor what to do next." : "Unknown: ATHOS couldn't see the page's buttons and links.");
      }
      await step();
      // 6–7 public DNS (Cloudflare DNS-over-HTTPS, read from this browser)
      if (c.kind === "own") {
        const root = apex(c.host);
        const [mx, txt, dm] = await Promise.all([dns(root, "MX"), dns(root, "TXT"), dns("_dmarc." + root, "TXT")]);
        if (!mx) put(5, "unknown", "The public DNS lookup didn't answer. Unknown.");
        else if (mx.answers.length) { const prov = /google/i.test(mx.answers.join(" ")) ? " (Google Workspace)" : /outlook|microsoft/i.test(mx.answers.join(" ")) ? " (Microsoft 365)" : ""; put(5, "pass", `<b>Yes.</b> ${esc(root)} receives its own email${prov}. <span class="lc-src">Public DNS, MX record.</span>`); }
        else put(5, "fail", `<b>No.</b> ${esc(root)} has no mail record, so the business email (if any) runs on a shared address like Gmail. <span class="lc-src">Public DNS, MX record.</span>`);
        await step();
        const spf = txt && txt.answers.some((a) => /v=spf1/i.test(a)), dmarc = dm && dm.answers.some((a) => /v=DMARC1/i.test(a));
        if (!txt && !dm) put(6, "unknown", "The public DNS lookup didn't answer. Unknown.");
        else put(6, spf && dmarc ? "pass" : spf || dmarc ? "warn" : "fail", spf && dmarc ? "<b>Yes.</b> SPF and DMARC are both published." : spf || dmarc ? `<b>Partly.</b> ${spf ? "SPF is published but DMARC isn't" : "DMARC is published but SPF isn't"}, so look-alike email is only partly blocked.` : "<b>No.</b> Neither SPF nor DMARC is published, so anyone can send email that claims to be from your name.");
      } else {
        put(5, "fail", `<b>Not on your name.</b> ${esc(c.host)} isn't your own address, so there's no business email to carry on it.`); await step();
        put(6, "fail", "<b>Not yours to protect.</b> The name on this door belongs to " + esc(c.who || "the platform") + ".");
      }
      // verdict
      const p = res.points, lit = Object.values(p).filter((x) => x.s === "pass").length;
      const dedicated = c.kind === "own" && p.answer?.s !== "fail" && p.answer?.s !== "unknown" && p.secure?.s === "pass";
      res.lit = lit; res.verdict = dedicated ? "DEDICATED LINE" : c.kind === "own" && (p.answer?.s === "fail") ? "LINE NOT ANSWERING" : "SHARED LINE";
      res.seconds = Math.round((performance.now() - t0) / 100) / 10;
      if (res.verdict !== "DEDICATED LINE") { $("#lc-coax", svg).setAttribute("opacity", ".9"); $("#lc-houses", svg).setAttribute("opacity", "1"); }
      verdict.hidden = false;
      verdict.dataset.v = res.verdict === "DEDICATED LINE" ? "dedicated" : "shared";
      verdict.innerHTML = `<p class="eyebrow mb0">Line Check · ${esc(c.host)}${biz ? " · " + esc(biz) : ""}</p><h2 class="display d-l lc-v">${res.verdict}</h2>
        <p class="lede">${lit} of 7 checkpoints lit, measured in ${res.seconds} seconds.</p>
        <p class="body">${res.verdict === "DEDICATED LINE" ? "Your own line is up. Now the question is what runs on it: does it bring you calls, bookings and members while you sleep? Walk the apartment and see what a full building looks like." : res.verdict === "LINE NOT ANSWERING" ? "Your name is yours, but the line isn't answering right now. Customers who type it may be hitting a wall." : "Right now you're on a shared line: customers find you through someone else's building, next to everyone else, under their rules. A dedicated line is your own address, your own email and your own front door that works on every phone."}</p>
        <p class="note">What this check can't see: your traffic, your sales, or what customers think. Those stay unknown here. ${res.diagnosis ? `<a class="gold" href="/diagnose/result/?id=${encodeURIComponent(res.diagnosis)}">Full ATHOS evidence for this page</a>.` : ""}</p>`;
      store.set("ath_line", res);
      const tq = new URLSearchParams({ u: c.host + (u.pathname.length > 1 ? u.pathname : "") }); if (biz) tq.set("b", biz);
      next.hidden = false; $("#lc-tour").href = "/tour/?" + tq.toString();
      st.className = "form-status"; st.textContent = ""; go.disabled = false;
      verdict.scrollIntoView({ behavior: calm ? "auto" : "smooth", block: "start" });
    }
    form.addEventListener("submit", (e) => { e.preventDefault(); run($("#lc-url").value, $("#lc-biz").value.trim().slice(0, 80)); });
    // Founder on a call: /line-check/?u=their-site.com&b=Business runs it straight away.
    if (qs.get("u")) { $("#lc-url").value = qs.get("u"); if (qs.get("b")) $("#lc-biz").value = qs.get("b").slice(0, 80); run(qs.get("u"), (qs.get("b") || "").slice(0, 80)); }
  }

  // ------------------------------------------------------------------ Key Fob Tour
  const tour = $("#tour");
  if (tour) {
    const fob = $("#fob"), rooms = [...tour.querySelectorAll(".room")], st = $("#tour-status");
    const line = store.get("ath_line");
    const want = (qs.get("u") || "").replace(/^https?:\/\//, "").replace(/^www\./, "").toLowerCase();
    const mine = line && (!want || line.host === want.split("/")[0]) ? line : null;
    const biz = (qs.get("b") || mine?.biz || "").slice(0, 80);
    if (biz) document.querySelectorAll("[data-biz]").forEach((e) => (e.textContent = biz));
    const lobby = $("#lobby-line");
    if (mine) lobby.innerHTML = `<b class="gold">${esc(mine.verdict)}</b> · ${mine.lit} of 7 checkpoints lit on ${esc(mine.host)}, measured ${new Date(mine.at).toLocaleTimeString([], { hour: "numeric", minute: "2-digit" })}.`;
    else lobby.innerHTML = `No Line Check on this device yet. <a class="gold" href="/line-check/${want ? "?u=" + encodeURIComponent(want) + (biz ? "&b=" + encodeURIComponent(biz) : "") : ""}">Run the 15-second Line Check</a> and the lobby shows your own line.`;
    async function ping(url) {
      const ctl = new AbortController(), t = setTimeout(() => ctl.abort(), 7000), t0 = performance.now();
      try { await fetch(url, { mode: "no-cors", cache: "no-store", signal: ctl.signal }); return { ok: true, ms: Math.round(performance.now() - t0) }; }
      catch { return { ok: false }; } finally { clearTimeout(t); }
    }
    const lit = {};
    async function open(room) {
      if (room.dataset.state === "on" || room.dataset.state === "checking") return;
      room.dataset.state = "checking"; const chip = room.querySelector(".room-chip"); chip.textContent = "Checking the lights…";
      const url = room.dataset.ping; const r = url ? await ping(url) : { ok: true, ms: null };
      room.dataset.state = r.ok ? "on" : "off"; lit[room.id] = r.ok;
      chip.textContent = r.ok ? (r.ms != null ? `Lights on · answered in ${r.ms < 10 ? "under 0.01" : (r.ms / 1000).toFixed(2)} s, just now` : (mine ? "Lit by your Line Check" : "Run your Line Check to light it")) : "Dark · not answering from your device right now";
      const n = Object.values(lit).filter(Boolean).length; $("#tour-count").textContent = `${n} of ${rooms.length} rooms lit`;
    }
    fob.addEventListener("click", async () => {
      fob.disabled = true; fob.classList.add("used"); tour.classList.add("unlocked"); st.textContent = "Key accepted. Walking every room…";
      for (const room of rooms) { room.hidden = false; if (!calm) await sleep(260); open(room); }
      await sleep(calm ? 0 : 400); $("#key-room").hidden = false; st.textContent = "";
      rooms[0].scrollIntoView({ behavior: calm ? "auto" : "smooth", block: "start" });
    });
    // close: "get your key" — assumptive, one step. Goes to the Call Desk with the Line Check attached.
    const kf = $("#key-form");
    kf?.addEventListener("submit", async (e) => {
      e.preventDefault();
      const s = kf.querySelector(".form-status"), b = kf.querySelector("button[type=submit]"), d = Object.fromEntries(new FormData(kf).entries());
      if (!d.name?.trim() || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(d.email || "")) { s.className = "form-status err"; s.textContent = "All we need is your name and the email you check."; return; }
      const when = d.when || "tomorrow-am", ct = new Date(Date.now() + (when === "today" ? 0 : 864e5));
      const call_date = ct.toLocaleDateString("en-CA", { timeZone: "America/Chicago" });
      const rl = Object.entries(lit).filter(([, v]) => v).map(([k]) => k.replace("room-", "")).join(", ");
      b.disabled = true; s.className = "form-status"; s.textContent = "Saving your key…";
      try {
        const r = await fetch(API + "/api/lead", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({
          name: d.name, email: d.email, phone: d.phone || "", company_fax: d.company_fax, org: biz || d.org || "", website: mine ? mine.input : want, intent: "key-fob-tour", interest: "Key Fob Tour",
          call_date, call_time: when === "today" ? "today" : when === "tomorrow-pm" ? "afternoon" : "morning", tz: "America/Chicago", diagnosis_id: mine?.diagnosis || undefined, page: "/tour/",
          message: `Walked the Key Fob Tour. Rooms lit on their device: ${rl || "none recorded"}. Line Check: ${mine ? `${mine.verdict}, ${mine.lit}/7 lit on ${mine.host}` : "not run on this device"}.`,
          source: { ...source(), tool: "key-fob-tour" } }) });
        const j = await r.json().catch(() => ({}));
        if (!r.ok) throw new Error(j.error || "ATH could not save that right now. Call or text (918) 960-0164.");
        kf.innerHTML = `<p class="eyebrow">Key saved</p><h3 class="display d-m">See you ${when === "today" ? "today" : "tomorrow " + (when === "tomorrow-pm" ? "afternoon" : "morning")}, ${esc(d.name.split(" ")[0])}.</h3><p class="body">A real person from Above The Hill will reach you at the time you picked, with your Line Check open. Want it sooner? Call or text <a class="gold" href="tel:+19189600164">(918) 960-0164</a>.</p>`;
      } catch (err) { s.className = "form-status err"; s.textContent = err.message; b.disabled = false; }
    });
  }
})();
