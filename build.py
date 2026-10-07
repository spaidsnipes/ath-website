#!/usr/bin/env python3
"""ATH Official Website — static page generator.

Canon: Visual Canon Atlas v1, slide athWebsiteCanonPass3 (Founder finder doc 2026-10-07).
Truth: only $10/mo (every ATH app is a $10/month focused door — Wavemotion first) and $20/mo (World Pass) are published prices. Nothing on this
site is sold through a fake checkout; unavailable things say Join waitlist / Request access / Get quote.
Run: python3 build.py  -> writes public/<route>/index.html
"""
import os, html, re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
SITE = "https://abovethehilldev.online"
API = "https://ath-athos.dhill5711.workers.dev"

# ---------------------------------------------------------------- icons (gold line)
def ic(name, cls="icon"):
    p = {
        "free": '<circle cx="12" cy="12" r="9"/><path d="M5.6 18.4 18.4 5.6"/><path d="M9 12h6"/>',
        "door": '<path d="M5 21V8a7 7 0 0 1 14 0v13"/><path d="M3 21h18"/><path d="M12 13v2"/>',
        "lattice": '<path d="M4 12c4-5 12-5 16 0-4 5-12 5-16 0Z"/><path d="M12 4v16"/><path d="M4 12h16"/><path d="M7 7.5c3 2.5 7 2.5 10 0M7 16.5c3-2.5 7-2.5 10 0"/>',
        "triangle": '<path d="M12 3 21.5 20h-19Z"/><path d="M12 9.5 16.5 17.5h-9Z"/>',
        "peaks": '<path d="M2 20 9 7l4 7 3-4 6 10Z"/><path d="M9 7l1.8 3.2"/>',
        "me": '<circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 5-6 8-6s6.5 2 8 6"/>',
        "key": '<circle cx="8" cy="15" r="4"/><path d="m11 12 9-9M17 6l2 2M15 8l2 2"/>',
        "own": '<path d="M12 3 4 7v5c0 5 3.5 8 8 9 4.5-1 8-4 8-9V7Z"/><path d="m8.5 12 2.5 2.5 4.5-5"/>',
        "continue": '<path d="M4 12a8 8 0 0 1 14-5.3L20 9"/><path d="M20 4v5h-5"/><path d="M20 12a8 8 0 0 1-14 5.3L4 15"/><path d="M4 20v-5h5"/>',
        "site": '<rect x="3" y="4" width="18" height="16" rx="1.5"/><path d="M3 9h18M7 6.5h.01M10 6.5h.01"/>',
        "content": '<rect x="3" y="5" width="18" height="12" rx="1.5"/><path d="m10 9 5 2.5-5 2.5Z"/><path d="M8 21h8"/>',
        "systems": '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1 7 17M17 7l2.1-2.1"/>',
        "app": '<rect x="3" y="3" width="8" height="8" rx="1"/><rect x="13" y="3" width="8" height="8" rx="1"/><rect x="3" y="13" width="8" height="8" rx="1"/><path d="M17 13v8M13 17h8"/>',
        "link": '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
        "hill": '<path d="M2 19 8 9l4 6 3-3 7 7Z"/>',
        "path": '<path d="M5 21c3-3 2-6 5-8s7-1 9-5"/><circle cx="19" cy="5" r="2"/>',
        "above": '<path d="M12 3v10"/><path d="m7 8 5-5 5 5"/><path d="M3 21h18M6 17h12"/>',
        "book": '<path d="M4 4h11a3 3 0 0 1 3 3v14H7a3 3 0 0 1-3-3Z"/><path d="M18 7h2v14"/><path d="M8 8h6M8 11h6"/>',
        "chip": '<rect x="6" y="6" width="12" height="12" rx="1"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/>',
        "bolt": '<path d="M13 2 4 14h7l-1 8 9-12h-7Z"/>',
        "refresh": '<path d="M20 11a8 8 0 1 0-2.3 5.7"/><path d="M20 4v7h-7"/>',
        "repo": '<path d="M5 4h11l3 3v13H5Z"/><path d="M9 9h6M9 13h6M9 17h4"/>',
        "doc": '<path d="M6 3h8l4 4v14H6Z"/><path d="M14 3v4h4M9 12h6M9 16h6"/>',
        "arch": '<path d="M3 21h18M5 21V10l7-6 7 6v11"/><path d="M9 21v-6h6v6"/>',
        "ai": '<path d="M12 3a5 5 0 0 1 5 5v1a4 4 0 0 1 0 8v1a3 3 0 0 1-6 0"/><path d="M12 3a5 5 0 0 0-5 5v1a4 4 0 0 0 0 8v1a3 3 0 0 0 6 0V3"/>',
        "deploy": '<path d="M12 15V3"/><path d="m7 8 5-5 5 5"/><rect x="3" y="15" width="18" height="6" rx="1"/>',
        "chart": '<path d="M3 21h18"/><path d="M6 17V11M11 17V7M16 17v-4M21 17V5"/>',
        "flow": '<circle cx="5" cy="6" r="2"/><circle cx="19" cy="6" r="2"/><circle cx="12" cy="18" r="2"/><path d="M7 6h10M6 8l5 8M18 8l-5 8"/>',
        "x": '<circle cx="12" cy="12" r="9"/><path d="m9 9 6 6M15 9l-6 6"/>',
        "eye": '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/>',
        "q": '<circle cx="12" cy="12" r="9"/><path d="M9.5 9a2.5 2.5 0 1 1 3.5 2.3c-.6.3-1 .9-1 1.6V14M12 17h.01"/>',
        "export": '<path d="M12 3v12"/><path d="m7 10 5 5 5-5"/><path d="M4 21h16"/>',
        "lock": '<rect x="4" y="10" width="16" height="11" rx="1.5"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
    }[name]
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>'

ARR = '<span class="arr" aria-hidden="true">→</span>'
FONTS = "https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600&family=Cormorant+Garamond:wght@400;500&family=Inter:wght@400;500;600&display=swap"
HERO_ART = {"/": "home", "/diagnose/": "diagnose", "/path/": "path", "/passport/": "passport", "/build/": "build", "/ecosystem/": "ecosystem", "/language/": "path", "/diagnose/deep/": "deep", "/work/": "path", "/company/": "home", "/404/": "path"}
NAV = [("Company", "/company/"), ("Inventions", "/work/"), ("Services", "/build/"),
       ("Diagnose", "/diagnose/"), ("Language", "/language/"), ("Ecosystem", "/ecosystem/")]

def head(title, desc, route):
    art = HERO_ART.get(route)
    preload = f'<link rel="preload" as="image" href="/assets/art/{art}.webp" fetchpriority="high">' if art else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{SITE}{route}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}{route}">
<meta property="og:image" content="{SITE}/assets/art/home.jpg">
<meta name="theme-color" content="#08090c">
<link rel="icon" href="/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="{FONTS}" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="{FONTS}"></noscript>
{preload}
<link rel="stylesheet" href="/assets/ath.css">
<script>window.ATH_API="{API}";</script>
<script src="/assets/ath.js" defer></script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""

def header(route):
    links = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if route.startswith(h) else ""}>{n}</a>' for n, h in NAV)
    return f"""<div class="mantra" aria-hidden="true">Plain truth · Higher ground · One vision · One language · One ecosystem · Invention company · Systems · Destinations</div>
<header class="site-head">
 <div class="wrap">
  <a class="brand" href="/" aria-label="Above the Hill Developments — home"><img src="/assets/ath-logo-lockup.webp" width="168" height="88" alt="Above the Hill Developments"></a>
  <button class="menu-btn" aria-expanded="false" aria-controls="nav" aria-label="Menu"><span></span><span></span><span></span></button>
  <nav class="nav" id="nav" aria-label="Primary">{links}<a class="btn btn-gold btn-sm" href="/diagnose/">Enter ATH</a></nav>
 </div>
</header>
<main id="main">
"""

FOOT = """</main>
<footer class="site-foot">
 <div class="wrap">
  <div class="foot-grid">
   <div><img src="/assets/ath-logo-lockup.webp" width="138" height="72" alt="Above the Hill Developments" loading="lazy">
    <p class="note mt2" style="max-width:34ch">Every dream, business and creator eventually meets a hill. We build the way over it.</p></div>
   <div><p class="fh">Start</p><a href="/diagnose/">What's your hill?</a><a href="/diagnose/deep/">Deep diagnostic</a><a href="/build/">ATH Services</a><a href="/contact/">Contact ATH</a></div>
   <div><p class="fh">Company</p><a href="/company/">Company</a><a href="/work/">Inventions &amp; work</a><a href="/path/">How ATH works</a><a href="/report/">The Hill Report</a></div>
   <div><p class="fh">World</p><a href="/ecosystem/">Ecosystem</a><a href="/passport/">Passport &amp; World Pass</a><a href="/language/">Builder Dictionary</a><a href="/privacy/">Privacy</a><a href="/terms/">Terms</a></div>
  </div>
  <div class="foot-line"><span class="mantra2">Heavens above · A realm to explore · Multiple destinations · One builder</span><span>© <span data-year>2026</span> Above the Hill Developments Inc.</span></div>
 </div>
</footer>
</body>
</html>
"""

def hero(art, eyebrow, title, lede, ctas="", extra="", pos="70% 40%", mpos="62% 30%", size="d-xl"):
    return f"""<section class="hero" style="--pos:{pos};--mpos:{mpos}">
 <div class="hero-art"><img src="/assets/art/{art}.webp" alt="" fetchpriority="high"></div>
 <div class="wrap"><div class="hero-copy">
  {f'<p class="eyebrow">{eyebrow}</p>' if eyebrow else ''}
  <h1 class="display {size}">{title}</h1>
  {f'<p class="lede">{lede}</p>' if lede else ''}
  {f'<div class="ctas">{ctas}</div>' if ctas else ''}
 </div>{extra}</div>
</section>
"""

def btn(label, href, kind="gold", attrs=""):
    return f'<a class="btn btn-{kind}" href="{href}" {attrs}>{label} {ARR}</a>'

# ---------------------------------------------------------------- shared blocks
RUNGS = [
    ("free", "Free", "Come in", "Free ATH Diagnostic · Public discovery · Guest exploration", "", "/diagnose/"),
    ("door", "$10 / mo", "Focused door", "Any ATH app, $10/month each · Wavemotion first", "", "/ecosystem/#wavemotion"),
    ("lattice", "$20 / mo", "Join the world", "Passport spine · World Pass membership", "", "/passport/"),
    ("triangle", "Specialist", "Serious systems", "WM Pro · PowerTribes · Dreamboard", "Own economics", "/ecosystem/#specialist"),
    ("peaks", "Services", "Build it for me", "Diagnostic → Scope → Quote → ATH implementation", "", "/build/"),
]

def ladder(detail=True):
    out = ['<nav class="ladder" aria-label="The ATH economic ladder">']
    for i, t, s, d, x, h in RUNGS:
        out.append(f'<a class="rung" href="{h}">{ic(i)}<span class="t">{t}</span><span class="s">{s}</span>'
                   + (f'<span class="d">{d}</span>' if detail else '') + (f'<span class="x">{x}</span>' if x else '') + '</a>')
    out.append('</nav>')
    return "".join(out)

def cta_block(title="What's your hill?", text="Tell ATHOS what's stopping you. Value first — no account, no sign-up wall."):
    return f"""<section class="block"><div class="wrap"><div class="panel panel-pad" style="display:flex;gap:24px;align-items:center;justify-content:space-between;flex-wrap:wrap">
 <div><p class="eyebrow">Start here</p><h2 class="display d-m mt1">{title}</h2><p class="body mt1 mb0">{text}</p></div>
 <div class="ctas" style="margin:0">{btn("What's your hill?", "/diagnose/")}{btn("Build it for me", "/build/", "line")}</div>
</div></div></section>"""

# ---------------------------------------------------------------- pages
pages = {}

pages["/"] = ("Above the Hill Developments — We build the way over it",
 "ATH is an invention company. Tell ATHOS what's stopping you — get an evidence-aware diagnosis, a clear path, and a builder who can take you above.",
 hero("home", "", "Above<br>the Hill",
      "Every dream, business and creator eventually meets a hill.<br>We build the way over it.",
      btn("What's your hill?", "/diagnose/") + btn("Explore ATH", "/company/", "line"),
      extra='<div class="stack" aria-hidden="true">Plain truth<br>Higher ground<br>Real creation<br>For generations</div>',
      pos="72% 35%", mpos="58% 30%")
 + f'<div class="wrap ladder-dock">{ladder()}</div>'
 + f"""
<section class="block"><div class="wrap split">
 <div><p class="eyebrow">Who we are</p><h2 class="display d-l mt1">Plain truth.<br>Higher ground.</h2>
  <p class="body mt2">Above the Hill Developments is an invention company. We build software, websites, systems, media, products and ventures — for local businesses, creators, startups, teams, churches, organizations, and people with only an idea.</p>
  <p class="body">We diagnose before we prescribe. Sometimes the honest answer is that you don't need anything at all. We'll say so.</p>
  <div class="ctas">{btn("How ATH works", "/path/", "line")}</div></div>
 <div class="panel panel-pad"><p class="panel-title">The grammar of every engagement</p>
  <ul class="rows">
   <li>{ic("hill","icon-sm")}<div><b>The Hill</b><span>What is actually in the way — observed, not assumed.</span></div></li>
   <li>{ic("path","icon-sm")}<div><b>The Path</b><span>What gets changed or built, in what order, and why.</span></div></li>
   <li>{ic("above","icon-sm")}<div><b>Above</b><span>What genuinely improved — shown with evidence, never invented.</span></div></li>
  </ul></div>
</div></section>
<section class="block"><div class="wrap">
 <div class="block-head"><div><p class="eyebrow">Inventions</p><h2 class="display d-m mt1">Built by ATH</h2></div>{btn("All inventions", "/work/", "line")}</div>
 <div class="grid g3">
  <article class="panel panel-pad card"><span class="tag live">Live today</span><h3>ATHOS Diagnostic</h3><p>The free hill-finder on this site. Inspects public evidence, separates what it observed from what it inferred, and says "unknown" when it doesn't know.</p><p class="mt2">{btn("Run it", "/diagnose/", "line")}</p></article>
  <article class="panel panel-pad card"><span class="tag">Open door</span><h3>WM Pro</h3><p>A professional market operating system: the chart as the room, with intelligence that respects price truth. Specialist economics.</p><p class="mt2"><a class="btn btn-line" href="https://wealthymindsetspro.com" rel="noopener">Visit WM Pro {ARR}</a></p></article>
  <article class="panel panel-pad card"><span class="tag dim">In development</span><h3>Wavemotion</h3><p>Creator + business movement OS — record, prepare, launch, distribute, learn. One permanent Living Destination. $10/month focused door.</p><p class="mt2">{btn("Request access", "/contact/?intent=wavemotion", "line")}</p></article>
 </div>
</div></section>
<section class="block"><div class="wrap">
 <div class="block-head"><div><p class="eyebrow">ATH Services</p><h2 class="display d-m mt1">You don't need another tool</h2></div>{btn("Services", "/build/", "line")}</div>
 <div class="grid g5">
  {"".join(f'<a class="panel panel-pad card" style="text-decoration:none" href="/build/">{ic(i)}<h3>{t}</h3><p>{d}</p></a>' for i,t,d in [
   ("site","Websites &amp; Destinations","Sites, Living Destinations, conversion paths."),
   ("content","Content &amp; Campaigns","Clipping, launch systems, distribution."),
   ("systems","Systems &amp; Automation","Business ops, integrations, workflows."),
   ("app","Custom Applications","Products and platforms, built to last."),
   ("link","Implementation &amp; Integration","Make what you have work together.")])}
 </div>
</div></section>
""" + cta_block())

pages["/diagnose/"] = ("What's your hill? — ATHOS Diagnostic",
 "Tell us what's stopping you. ATHOS inspects publicly available evidence where supported and never pretends to know what it cannot observe.",
 f"""<section class="hero" style="--pos:60% 40%;--mpos:50% 30%;min-height:auto">
 <div class="hero-art"><img src="/assets/art/diagnose.webp" alt="" fetchpriority="high"></div>
 <div class="wrap">
  <div style="display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap;margin-bottom:28px">
   <p class="eyebrow mb0">Diagnose / Start</p>
   <ol class="stepper" aria-label="Progress: step 1 of 3"><li class="on"><span>1</span></li><li><span>2</span></li><li><span>3</span></li></ol>
  </div>
  <h1 class="display d-l">What's your hill?</h1>
  <p class="lede">Tell us what's stopping you.</p>
  <p class="body">ATHOS inspects publicly available evidence where supported and never pretends to know what it cannot observe.</p>
  <form id="diag-form" class="mt3" novalidate>
   <div class="grid" style="grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:18px" data-collapse>
    <div class="grid" style="gap:18px">
     <div class="panel panel-pad">
      <p class="panel-title">Show ATHOS what you have</p>
      <label class="lbl" for="url">Website URL</label>
      <p class="hint">Public pages only. Leave blank if you don't have one.</p>
      <input id="url" name="url" type="url" inputmode="url" placeholder="https://example.com" autocomplete="url">
     </div>
     <div class="panel panel-pad">
      <p class="panel-title">Business description</p>
      <label class="lbl" for="desc">What you do, who you serve, what's in the way…</label>
      <textarea id="desc" name="description" maxlength="1000" placeholder="We build … for … Our biggest challenge right now is …"></textarea>
      <div class="counter"><span id="desc-count">0</span> / 1000</div>
     </div>
     <div class="panel panel-pad">
      <label class="check"><input type="checkbox" name="unsure" id="unsure"><span><b>I don't know what I need yet</b><br><span class="mute">Explore without a specific brief.</span></span></label>
     </div>
    </div>
    <div class="grid" style="gap:18px;align-content:start">
     <fieldset class="panel panel-pad" style="margin:0">
      <legend class="panel-title" style="float:left;width:100%">Optional public inspection</legend>
      <p class="hint" style="clear:both">With a URL, ATHOS fetches that one public page and checks:</p>
      {"".join(f'<label class="check"><input type="checkbox" name="checks" value="{v}" checked><span>{t}</span></label>' for v,t in [
        ("structure","Site structure"),("messaging","Messaging"),("navigation","Navigation"),("conversion","Visible conversion paths"),("content","Public content"),("brand","Brand positioning")])}
     </fieldset>
     <p class="body" style="margin:0 4px">Unknown remains a valid answer.<br>You control what you share.</p>
     <p class="note" style="margin:0 4px">ATHOS reads one public page. It cannot see your analytics, traffic, sales, private systems or code — anything it can't observe is marked <b>unknown</b>.</p>
    </div>
   </div>
   <div class="ctas">
    <button class="btn btn-gold" type="submit" id="diag-go">Begin diagnosis {ARR}</button>
    <a class="btn btn-line" href="/contact/?intent=describe">I prefer to describe it myself {ARR}</a>
   </div>
   <p class="form-status" id="diag-status" role="status" aria-live="polite"></p>
  </form>
 </div>
</section>
<style>@media (max-width:860px){{[data-collapse]{{grid-template-columns:1fr!important}}}}</style>
""")

pages["/diagnose/result/"] = ("Your Hill Map — ATHOS Diagnostic Result",
 "What's working, the hill, evidence, inferences, unknowns, and your path above.",
 f"""<section class="block" style="padding-top:48px"><div class="wrap">
 <div style="display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap">
  <p class="eyebrow mb0">Diagnose / Result</p>
  <div style="display:flex;gap:14px;align-items:center"><ol class="stepper" aria-label="Progress: step 3 of 3"><li class="on"><span>1</span></li><li class="on"><span>2</span></li><li class="on"><span>3</span></li></ol>
  <button class="btn btn-line btn-sm" type="button" data-print>Export</button></div>
 </div>
 <div id="result" class="mt2" aria-live="polite"><p class="body"><span class="spinner"></span>Loading your diagnosis…</p></div>
</div></section>
""")

pages["/path/"] = ("How ATH works — One path. Different relationships.",
 "Come in free. Open a door for $10. Join the world for $20. Use specialist systems when you need them. Or let ATH build the path.",
 hero("path", "How ATH works", "One path.<br>Different<br>relationships.",
      "Come in free. Open a door. Join the world.<br>Use specialist systems when you need them.<br>Or let ATH build the path.", "", pos="66% 45%", size="d-l")
 + f'<div class="wrap ladder-dock">{ladder()}</div>'
 + f"""
<section class="block"><div class="wrap">
 <div class="grid g2">
  <div class="panel panel-pad"><p class="panel-title">$10 opens one app. $20 joins the world.</p>
   <p class="body">Every ATH app is a <b>$10/month focused door</b> — you pay for the one app you use. <b>World Pass at $20/month</b> is the membership across the connected world.</p>
   <p class="panel-title mt2">What $20 is — and isn't</p>
   <p class="body">World Pass is paid ecosystem membership layered on your Passport identity. It does <b>not</b> automatically include every specialist product, professional system, ATH service, third-party cost, or unlimited expensive infrastructure.</p>
   <dl class="hpa mt2"><dt>Identity</dt><dd>≠ membership</dd><dt>Membership</dt><dd>≠ owning every product</dd><dt>Membership</dt><dd>≠ professional infrastructure</dd></dl></div>
  <div class="panel panel-pad"><p class="panel-title">No surprise costs</p>
   <p class="body">Some things cost real money to run — market data, heavy AI compute, video/image/audio generation, mass messaging, unusual storage or bandwidth. We handle those with included allowances, bring-your-own credentials where lawful, add-ons or pass-through costs. Never hidden behind "unlimited".</p></div>
 </div>
 <div class="panel panel-pad mt2"><p class="panel-title">Availability today</p>
  <ul class="rows">
   <li>{ic("free","icon-sm")}<div><b>Free ATH Diagnostic</b><span>Available now — no account required. <a class="gold" href="/diagnose/">Run it</a>.</span></div></li>
   <li>{ic("door","icon-sm")}<div><b>Focused door — $10 / month per app</b><span>Every ATH app opens as its own $10/month focused door. Wavemotion is first; it is not yet purchasable, has no permanent free operator tier, and public Living Destinations stay viewable. <a class="gold" href="/contact/?intent=wavemotion">Request access</a>.</span></div></li>
   <li>{ic("lattice","icon-sm")}<div><b>World Pass — $20 / month</b><span>Available now in WOW World, on your free Passport. <a class="gold" href="https://wow-world-os.dhill5711.workers.dev/passport" rel="noopener">Get World Pass</a>.</span></div></li>
   <li>{ic("triangle","icon-sm")}<div><b>Specialist systems</b><span>Own economics, set per product. WM Pro is open at <a class="gold" href="https://wealthymindsetspro.com" rel="noopener">wealthymindsetspro.com</a>.</span></div></li>
   <li>{ic("peaks","icon-sm")}<div><b>ATH Services</b><span>Diagnostic → scope → quote. <a class="gold" href="/build/">Build my path</a>.</span></div></li>
  </ul></div>
</div></section>""" + cta_block())

pages["/passport/"] = ("Passport & World Pass — Identity first. Membership second.",
 "Passport is not a subscription card. It is the spine. World Pass is the paid relationship layered on the world.",
 f"""<section class="hero" style="--pos:50% 60%">
 <div class="hero-art"><img src="/assets/art/passport.webp" alt="" fetchpriority="high"></div>
 <div class="wrap"><div class="grid" style="grid-template-columns:1.1fr .8fr 1fr;gap:clamp(20px,3vw,44px);align-items:center" data-collapse>
  <div><h1 class="display d-l">Passport</h1><p class="lede" style="font-size:clamp(26px,3vw,40px);margin-top:10px">Identity first.<br>Membership second.</p>
   <p class="body mt2">Passport is not a subscription card. It is the spine. World Pass is the paid relationship layered on the world.</p>
   <div class="ctas">{btn("Explore Passport", "#tiers")}{btn("View benefits", "#benefits", "line")}</div></div>
  <div class="book" role="img" aria-label="The Above the Hill Passport"><img src="/assets/ath-mark.webp" alt=""><span class="bt">Above the Hill</span><span class="bs">Passport</span></div>
  <ul class="rows panel panel-pad" style="padding-top:8px;padding-bottom:8px">
   <li>{ic("me")}<div><b>This is me</b><span>Identity</span></div></li>
   <li>{ic("key")}<div><b>This is what I can access</b><span>Permissions</span></div></li>
   <li>{ic("own")}<div><b>This is what I own</b><span>Ownership</span></div></li>
   <li>{ic("continue")}<div><b>This continues with me</b><span>Continuity</span></div></li>
  </ul>
 </div></div>
</section>
<style>@media (max-width:960px){{[data-collapse]{{grid-template-columns:1fr!important}}}}</style>
<section class="block" id="tiers"><div class="wrap">
 <div class="grid g5">
  {"".join(f'<div class="panel panel-pad card" style="text-align:center">{ic(i)}<h3>{t}</h3><p class="gold" style="font-size:13px;margin-bottom:8px">{p}</p><p>{d}</p></div>' for i,t,p,d in [
   ("eye","Guest","No account","Explore appropriate public experiences without an account. Guest is a legitimate state, not a broken one."),
   ("me","Passport Free","Identity","Persistent identity only where it is actually required — receipts, permissions, ownership proof."),
   ("lattice","World Pass","$20 / month","Ecosystem membership, member access, cross-world benefits, continuity — as actually released."),
   ("triangle","Specialist Entitlements","Own economics","WM Pro, PowerTribes, Dreamboard and others carry separate product economics."),
   ("own","Purchases &amp; Ownership","Yours","What you bought and what remains yours, carried by Passport where supported.")])}
 </div>
 <div class="grid g2 mt3" id="benefits">
  <div class="panel panel-pad"><p class="panel-title">If a member cancels</p><p class="body mb0">The person doesn't stop existing. Identity, lawful ownership, receipts and applicable durable rights persist. Membership-only benefits end.</p></div>
  <div class="panel panel-pad"><p class="panel-title">Availability</p><p class="body">Passport is free and World Pass is $20/month — both live in WOW World today, with a real Stripe checkout and cancel any time.</p><div class="ctas mt1">{btn("Get your free Passport", "https://wow-world-os.dhill5711.workers.dev/passport/claim")}{btn("Get World Pass", "https://wow-world-os.dhill5711.workers.dev/passport", "line")}</div></div>
 </div>
</div></section>""")

pages["/build/"] = ("ATH Services — You need the right path",
 "ATH diagnoses before prescribing — for local businesses, creators, teams, churches, startups, and people with only an idea.",
 hero("build", "ATH Services", "You don't need<br>another tool.<br>You need the right path.",
      "ATH diagnoses before prescribing — for local businesses, creators, teams, churches, startups, and people with only an idea.",
      btn("Get a free ATH diagnostic", "/diagnose/") + btn("Build my path", "/contact/?intent=services", "line"),
      extra='<div class="stack" aria-hidden="true">Diagnose · Align<br>Implement · Above</div>', pos="62% 55%", size="d-m")
 + f"""
<section class="block"><div class="wrap">
 <div class="grid g3">
  {"".join(f'<div class="panel panel-pad card" style="display:flex;gap:16px">{ic(i)}<div><h3 style="margin-top:0">{t}</h3><p>{d}</p></div></div>' for i,t,d in [
   ("site","Websites &amp; Destinations","Sites, Living Destinations, conversion paths."),
   ("content","Content &amp; Campaigns","Clipping packages, launch systems, distribution."),
   ("systems","Systems &amp; Automation","Business ops, integrations, custom applications."),
   ("app","Custom Applications &amp; Platforms","Products and larger platforms, engineered to last."),
   ("link","Implementation &amp; Integration","Make the tools you already pay for work together."),
   ("q","Consulting","When the honest first step is clarity, not code.")])}
 </div>
 <div class="panel panel-pad mt3"><p class="panel-title">How an engagement works</p>
  <div class="grid g5" style="gap:0">
   {"".join(f'<div style="padding:12px 10px;border-left:1px solid var(--gold-faint)"><p class="eyebrow mb0">0{n}</p><p class="h-serif" style="font-size:22px;margin-top:6px">{t}</p><p class="note">{d}</p></div>' for n,t,d in [
    (1,"Diagnostic","Free. Evidence first."),(2,"Scope","What changes, and what doesn't."),(3,"Quote","A real number for a real scope."),(4,"Build","ATH implements."),(5,"Proof &amp; handoff","Hill receipt: what improved.")])}
  </div>
  <p class="note mt2 mb0">We don't publish invented prices. Every engagement starts with a diagnosis, then a scope, then a quote.</p></div>
 <div class="panel panel-pad mt3"><p class="panel-title">Example paths (conceptual)</p>
  <div class="grid g3">
   {"".join(f'<dl class="hpa"><dt>The Hill</dt><dd>{a}</dd><dt>The Path</dt><dd>{b}</dd><dt>Above</dt><dd>{c}</dd></dl>' for a,b,c in [
    ("Interest without conversion.","Aligned message and destination.","Clearer next step for visitors."),
    ("Tools without a system.","Routed to focused software.","A moving operating path."),
    ("Idea with no build path.","ATH scoped and built a first version.","Something real to test in the market.")])}
  </div>
  <p class="note mt2 mb0">Case frames are structural examples only — no real client claims, logos, or statistics.</p></div>
</div></section>""" + cta_block("Build my path", "Start with the free diagnostic, or tell us about the project directly."))

ECO = [
 ("ATH", "Parent builder", "live", "You're here", "The invention company. Builds, owns and routes.", ("Diagnose", "/diagnose/")),
 ("ATHOS", "Intelligence", "live", "Diagnostic live", "Diagnosis, evidence, routing. The free diagnostic on this site is ATHOS working today; deeper capabilities are in development.", ("Run it", "/diagnose/")),
 ("Passport", "Identity spine · Free", "live", "Open door", "Identity, permissions, ownership, receipts, continuity. Free, in WOW World.", ("Get Passport", "https://wow-world-os.dhill5711.workers.dev/passport/claim")),
 ("World Pass", "Membership · $20/mo", "live", "Open door", "Paid ecosystem membership on your Passport. Cancel any time.", ("Get World Pass", "https://wow-world-os.dhill5711.workers.dev/passport")),
 ("Wavemotion", "Creator + Business Movement OS · $10/mo", "dim", "In development", "Record → prepare → launch → distribute → learn. Living Destination + Channeler.", ("Request access", "/contact/?intent=wavemotion")),
 ("WM Pro", "Professional market OS · Specialist", "", "Open door", "A professional trading operating system. Own economics.", ("Visit", "https://wealthymindsetspro.com")),
 ("PowerTribes", "Business · sales · workforce · leadership OS", "dim", "In development", "Specialist economics.", ("Request access", "/contact/?intent=powertribes")),
 ("Dreamboard", "Human-potential &amp; creative OS", "dim", "In development", "Idea → clarity → project → finished work. Specialist economics.", ("Request access", "/contact/?intent=dreamboard")),
 ("WOW World", "Consumer world · Guest welcome", "live", "Open door", "One world, many rooms — Lounge, Academy, Marketplace, Events, WOW TV, WOW Music, WOW Radio.", ("Enter", "https://wow-world-os.dhill5711.workers.dev/")),
 ("WOW TV · WM Radio", "Watch · Listen", "dim", "Future", "Viewer and listener destinations.", None),
 ("Lounge · Academy · Shop", "Connect · Learn · Own", "dim", "Future", "Community, learning and commerce places.", None),
 ("WOW Studios", "Creation infrastructure", "dim", "Future", "Deeper production infrastructure.", None),
]
def eco_cards():
    out = []
    for n, r, cls, st, d, c in ECO:
        anchor = "wavemotion" if n == "Wavemotion" else ("specialist" if n == "WM Pro" else "")
        cbtn = ""
        if c:
            ext = c[1].startswith("http")
            cbtn = f'<p class="mt2 mb0"><a class="btn btn-line btn-sm" href="{c[1]}"{" rel=\"noopener\"" if ext else ""}>{c[0]} {ARR}</a></p>'
        out.append(f'<article class="panel panel-pad card"{f" id=\"{anchor}\"" if anchor else ""}><span class="tag {cls}">{st}</span><h3>{n}</h3><p class="gold" style="font-size:13px;margin-bottom:8px">{r}</p><p>{d}</p>{cbtn}</article>')
    return "".join(out)

pages["/ecosystem/"] = ("The Ecosystem — ATH builds the world. Destinations open the doors.",
 "Not an app store. Parent builder, intelligence, identity, membership, destinations.",
 hero("ecosystem", "", "The<br>Ecosystem",
      "ATH builds the world.<br>Destinations open the doors.<br><span style=\"font-size:.8em;color:var(--ivory-dim)\">Not an app store. Parent builder · intelligence · identity · membership · destinations.</span>",
      "", extra='<div class="plaques">' + "".join(f'<a class="plaque" href="#d"><b>{n}</b><span>{t}</span></a>' for n,t in [("WOW World","Open door"),("WM Pro","Open door"),("WOW TV · WOW Radio","Open door"),("Lounge · Academy · Shop","Open door")]) + '</div>', pos="50% 50%", mpos="50% 40%", size="d-l")
 + '<div class="strip">Connected destinations · One ecosystem · A living world</div>'
 + f"""<section class="block" id="d"><div class="wrap">
 <div class="block-head"><div><p class="eyebrow">Destinations</p><h2 class="display d-m mt1">Status, plainly</h2></div><p class="note" style="max-width:46ch">Statuses reflect what is actually reachable today. Future systems are never shown as purchasable.</p></div>
 <div class="grid g3">{eco_cards()}</div>
</div></section>""" + cta_block())

pages["/language/"] = ("ATH Builder Dictionary — Build a better language",
 "A purpose-built dictionary of ATH terms that gives humans and AI a more precise shared language for building software and systems.",
 f"""<section class="hero" style="min-height:auto"><div class="hero-art"><img src="/assets/art/path.webp" alt="" style="opacity:.35"></div>
 <div class="wrap split">
  <div><p class="eyebrow">ATH Builder Dictionary</p><h1 class="display d-m mt1">Stop writing longer prompts.<br>Build a better language.</h1>
   <p class="lede">A purpose-built dictionary of ATH terms that gives humans and AI a more precise shared language for building software and systems.</p>
   <div class="ctas">{btn("Get the dictionary — join waitlist", "/contact/?intent=dictionary")}{btn("View sample terms", "#samples", "line")}</div>
   <p class="note mt1">Founder pricing pending. Not yet for sale — no checkout until it is.</p></div>
  <div class="book" role="img" aria-label="ATH Builder Dictionary"><img src="/assets/ath-mark.webp" alt=""><span class="bt">ATH Builder<br>Dictionary</span><span class="bs">v1.0</span></div>
 </div></section>
<section class="block"><div class="wrap">
 <div class="grid g5">
  {"".join(f'<div class="panel panel-pad card" style="text-align:center">{ic(i)}<h3>{t}</h3><p>{d}</p></div>' for i,t,d in [
   ("book","Dictionary","Definitions &amp; examples"),("chip","AI-Readable Pack","Structured language file"),("bolt","Quick Start","Setup instructions"),("doc","Builder Commands","Prompt examples"),("refresh","Updates","As released")])}
 </div>
 <h2 class="display d-m mt3" id="samples">Sample terms</h2>
 <div class="grid g3 mt2">
  {"".join(f'<div class="panel panel-pad card"><p class="eyebrow mb0">{t}</p><p class="mt1" style="color:var(--ivory)">{d}</p><p class="note mb0">{e}</p></div>' for t,d,e in [
   ("Split brain","Two parts of one system tell different stories.","“Your discovery experience and destination are telling different stories.”"),
   ("Single organism","Many surfaces, one truth — no duplicate records or parallel apps.","Anti-example: a lead that becomes five unrelated records."),
   ("Truth state","Whether a claim is observed, inferred, or unknown.","Labels confirm truth. Labels do not create truth."),
   ("Evidence lineage","Every finding carries where and when it was observed.","A finding without a source is an opinion."),
   ("Finish line","The defined state where work is genuinely done — not when a screen exists.","“Done” requires proof, not presence."),
   ("Guest ready","A stranger can arrive, understand, and act without help or a login wall.","Anti-example: a dead button.")])}
 </div>
 <div class="panel panel-pad mt3"><p class="panel-title">Sell the language. Not the inventions.</p>
  <p class="body mb0">The dictionary teaches vocabulary. It does not include ATH source code, architecture, ATHOS internals, private prompts, security details, unreleased inventions or customer information. Buying the dictionary does not transfer ownership of ATH inventions.</p></div>
</div></section>""")

pages["/diagnose/deep/"] = ("ATHOS Deep Diagnostic — Open the hood",
 "The free check found the hill. Want us to look underneath? You control the scope. ATHOS only inspects the sources you authorize.",
 hero("deep", "ATHOS Deep Diagnostic", "The free check<br>found the hill.<br>Want us to look underneath?",
      "You control the scope. ATHOS only inspects the sources you authorize.", "", pos="60% 60%", size="d-m")
 + f"""<section class="block"><div class="wrap">
 <form class="panel panel-pad" id="deep-form" novalidate>
  <p class="panel-title">Choose what ATH may inspect</p>
  <div class="grid g2">
   <div>{"".join(f'<label class="check"><input type="checkbox" name="sources" value="{v}"><span>{t}</span></label>' for v,t in [("repo","Repository / source"),("docs","Documentation"),("arch","Architecture"),("ai","AI instructions")])}</div>
   <div>{"".join(f'<label class="check"><input type="checkbox" name="sources" value="{v}"><span>{t}</span></label>' for v,t in [("deploy","Build / deployment"),("analytics","Analytics / business information"),("flows","Product / business flow")])}</div>
  </div>
  <div class="grid g2 mt2">
   <div class="field"><label class="lbl" for="d-name">Name</label><input id="d-name" name="name" type="text" autocomplete="name" required></div>
   <div class="field"><label class="lbl" for="d-email">Email</label><input id="d-email" name="email" type="email" autocomplete="email" required></div>
  </div>
  <div class="field"><label class="lbl" for="d-msg">What should we look at, and why?</label><textarea id="d-msg" name="message"></textarea></div>
  <input type="hidden" name="intent" value="deep-diagnostic">
  <button class="btn btn-gold" type="submit">Request deep diagnostic {ARR}</button>
  <p class="note mt1">This sends a request — no access is granted and nothing is charged. ATH replies with a written scope and quote first.</p>
  <p class="form-status" role="status" aria-live="polite"></p>
 </form>
 <div class="grid g2 mt3">
  <div class="panel panel-pad"><p class="panel-title">What ATHOS may do</p><ul class="rows">
   <li>{ic("eye","icon-sm")}<div><b>Read / inspect</b><span>Only the sources you select, through access you grant and can revoke.</span></div></li>
   <li>{ic("lock","icon-sm")}<div><b>Least privilege</b><span>Read-only wherever possible. Explicit, written scope.</span></div></li>
   <li>{ic("export","icon-sm")}<div><b>Deliver a Hill Report</b><span>Findings with evidence, confidence and unknowns.</span></div></li></ul></div>
  <div class="panel panel-pad"><p class="panel-title">What ATHOS may not do</p><ul class="rows">
   <li>{ic("x","icon-sm")}<div><b>No changes</b><span>Diagnosis does not modify your code or systems.</span></div></li>
   <li>{ic("x","icon-sm")}<div><b>No hidden copying or training</b><span>Your materials aren't reused or used to train models without a separate written agreement.</span></div></li>
   <li>{ic("x","icon-sm")}<div><b>No wandering</b><span>Nothing outside the authorized scope is crawled.</span></div></li></ul></div>
 </div>
 <p class="note mt2">Retention: materials are kept only for the engagement and deleted on request or at its end. You own your materials; a diagnostic transfers no ownership to ATH. See <a class="gold" href="/terms/">Terms</a> and <a class="gold" href="/privacy/">Privacy</a>. We describe controls, not guarantees — no one can honestly promise "100% safe".</p>
 <p class="note">Depth is sold by scope, passes and review level — never by fake hours. Final pricing is quoted per engagement.</p>
</div></section>""")

pages["/report/"] = ("The ATH Hill Report — Customer report",
 "The professional report a deep diagnostic produces: scope, what's working, the hill, findings, evidence, confidence, unknowns and your path above.",
 f"""<section class="block" style="padding-top:56px"><div class="wrap">
 <div style="display:flex;justify-content:space-between;gap:16px;align-items:center;flex-wrap:wrap"><p class="eyebrow mb0">Customer report · format</p><button class="btn btn-line btn-sm" type="button" data-print>Export</button></div>
 <h1 class="display d-l mt1">ATH Hill Report</h1>
 <p class="body">An example of the delivery format. Every real report traces each finding to evidence.</p>
 <div class="grid mt2" style="grid-template-columns:1fr 1fr;gap:18px" data-collapse>
  <ul class="rows panel panel-pad">
   {"".join(f'<li>{ic(i,"icon-sm")}<div><b>{t}</b><span>{d}</span></div></li>' for i,t,d in [
    ("x","Scope","What we inspected — and what we did not."),("own","What's working","Strengths worth preserving."),("hill","The hill","The primary obstacle."),
    ("eye","Findings","Plain language + ATH classification."),("doc","Evidence","Sources, levels and timestamps."),("q","Unknowns","What remained uncertain."),("above","Your path above","Priority order and three ways across.")])}
  </ul>
  <div class="panel panel-pad"><p class="panel-title">ATH classification (example)</p>
   <p class="display d-m" style="font-size:clamp(28px,3vw,42px)">Split_Brain</p>
   <dl class="hpa mt2"><dt>Evidence</dt><dd>4 observations</dd><dt>Confidence</dt><dd>High</dd><dt>Affected</dt><dd>Discovery → destination</dd><dt>Status</dt><dd>Open</dd></dl>
   <p class="body mt2">Plain language: your discovery experience and your destination are telling different stories.</p>
   <span class="tag dim">Example — not a real client</span></div>
 </div>
 <p class="panel-title mt3">Choose how to cross it</p>
 <div class="doors">
  <a class="door solid" href="/language/"><h3>Do it myself</h3><p>Use the findings yourself + tools and language.</p></a>
  <a class="door solid" href="/language/"><h3>Fix it with my AI</h3><p>Get a remediation prompt using ATH language.</p></a>
  <a class="door solid" href="/contact/?intent=services"><h3>Have ATH fix it</h3><p>Turn it into a scope / quote.</p></a>
 </div>
</div></section>
<style>@media (max-width:860px){{[data-collapse]{{grid-template-columns:1fr!important}}}}</style>""" + cta_block("Start with the free check", "The Hill Report comes from a deep diagnostic. The free diagnostic comes first."))

pages["/work/"] = ("Inventions & Work — Above the Hill Developments",
 "Real ATH inventions and projects, shown at their true current state.",
 hero("path", "Inventions &amp; work", "Built by<br>ATH",
      "These people can actually build. Every status here is shown exactly as it is — nothing presented as live until it is.", "", pos="60% 50%", size="d-l")
 + f"""<section class="block"><div class="wrap"><div class="grid g2">
  {"".join(f'<article class="panel panel-pad card"><span class="tag {c}">{s}</span><h3>{t}</h3><dl class="hpa mt1"><dt>The hill</dt><dd>{h}</dd><dt>The path</dt><dd>{p}</dd><dt>Now</dt><dd>{n}</dd></dl>{l}</article>' for c,s,t,h,p,n,l in [
   ("live","Live","ATHOS Diagnostic","Businesses can't see what's actually stopping them — and most \"audits\" invent certainty.","An evidence-first diagnostic that separates observed, inferred and unknown.","Running on this site.", f'<p class="mt2 mb0">{btn("Run it","/diagnose/","line")}</p>'),
   ("","Open door","WM Pro","Traders drown in tools that paste intelligence around a chart.","A market OS where the chart is the room and every mark respects price truth.","Open at wealthymindsetspro.com. Specialist economics.", f'<p class="mt2 mb0"><a class="btn btn-line" href="https://wealthymindsetspro.com" rel="noopener">Visit {ARR}</a></p>'),
   ("dim","In development","Wavemotion","Creators and businesses lose momentum between recording and real distribution.","Record → cloud inbox → edit → variants → approval → publish → receipt → learning loop.","In development. $10/month focused door.", f'<p class="mt2 mb0">{btn("Request access","/contact/?intent=wavemotion","line")}</p>'),
   ("dim","In development","Dreamboard","Ideas die between inspiration and a finished thing.","Idea → clarity → project → creation → finishing evidence.","In development.", ""),
   ("dim","In development","Passport","Every app makes you a stranger again.","One identity spine — permissions, ownership, receipts, continuity.","In development.", ""),
   ("dim","Future","WOW World","Products feel like islands.","A connected world of destinations under one builder.","Future.", "")])}
 </div>
 <p class="note mt2">No client logos, testimonials or results are shown until they are real and approved.</p>
</div></section>""" + cta_block())

pages["/company/"] = ("Company — Above the Hill Developments",
 "Above the Hill Developments is an invention company. Plain truth. Higher ground.",
 hero("home", "Company", "Plain truth.<br>Higher ground.",
      "Every dream, business and creator eventually meets a hill. We build the way over it.", "", pos="75% 40%", size="d-l")
 + f"""<section class="block"><div class="wrap split">
 <div class="prose"><p class="eyebrow">Above the Hill Developments Inc.</p>
  <p class="lede" style="max-width:none">An invention company — broader than software.</p>
  <p>ATH builds, invents, operates, researches, diagnoses, designs, automates, teaches, launches and integrates. We do client work and we build our own products and ventures.</p>
  <p>We serve local businesses, creators, startups, teams, churches, organizations, operators, founders — and people with only an idea or with broken systems they've outgrown.</p>
  <p>The hill is the obstacle. The path is the route. Above is the improved state. Light means discovery, elevation means progress, terrain means real obstacles.</p></div>
 <div class="panel panel-pad"><p class="panel-title">How the company fits together</p><ul class="rows">
  <li>{ic("peaks","icon-sm")}<div><b>ATH</b><span>Parent company, builder, front door.</span></div></li>
  <li>{ic("eye","icon-sm")}<div><b>ATHOS</b><span>Intelligence — diagnosis, evidence, routing.</span></div></li>
  <li>{ic("doc","icon-sm")}<div><b>Atlas</b><span>Memory — provenance, decisions, lessons.</span></div></li>
  <li>{ic("me","icon-sm")}<div><b>Passport</b><span>Identity, permissions, ownership, continuity.</span></div></li>
  <li>{ic("lattice","icon-sm")}<div><b>World Pass</b><span>Paid ecosystem membership.</span></div></li>
  <li>{ic("door","icon-sm")}<div><b>Destinations</b><span>Wavemotion, WM Pro, PowerTribes, Dreamboard, WOW World and more — each owns its own experience.</span></div></li></ul></div>
</div></section>""" + cta_block())

pages["/contact/"] = ("Contact ATH — Start",
 "Request access, join a waitlist, or ask ATH to build your path.",
 f"""<section class="block" style="padding-top:56px"><div class="wrap split" style="align-items:start">
 <div><p class="eyebrow">Contact / Start</p><h1 class="display d-l mt1">Start the<br>climb</h1>
  <p class="lede">Tell us where you are. A person at ATH reads every message.</p>
  <p class="body mt2">Prefer to see evidence first? <a class="gold" href="/diagnose/">Run the free diagnostic</a> — your result links to this request automatically.</p></div>
 <form class="panel panel-pad" id="lead-form" novalidate>
  <div class="field"><label class="lbl" for="l-intent">I'm here about</label>
   <select id="l-intent" name="intent">
    <option value="services">ATH Services — build it for me</option>
    <option value="describe">Describing my hill to a person</option>
    <option value="deep-diagnostic">Deep diagnostic</option>
    <option value="wavemotion">Wavemotion access ($10/mo)</option>
    <option value="worldpass">World Pass waitlist ($20/mo)</option>
    <option value="dictionary">Builder Dictionary waitlist</option>
    <option value="powertribes">PowerTribes access</option>
    <option value="dreamboard">Dreamboard access</option>
    <option value="other">Something else</option>
   </select></div>
  <div class="grid g2"><div class="field"><label class="lbl" for="l-name">Name</label><input id="l-name" name="name" type="text" autocomplete="name" required></div>
   <div class="field"><label class="lbl" for="l-email">Email</label><input id="l-email" name="email" type="email" autocomplete="email" required></div></div>
  <div class="grid g2"><div class="field"><label class="lbl" for="l-org">Business / organization <span class="mute">(optional)</span></label><input id="l-org" name="org" type="text" autocomplete="organization"></div>
   <div class="field"><label class="lbl" for="l-site">Website <span class="mute">(optional)</span></label><input id="l-site" name="website" type="url" inputmode="url" autocomplete="url"></div></div>
  <div class="field"><label class="lbl" for="l-msg">What's your hill?</label><textarea id="l-msg" name="message" maxlength="3000"></textarea></div>
  <input type="text" name="company_fax" tabindex="-1" autocomplete="off" class="vh" aria-hidden="true">
  <button class="btn btn-gold" type="submit">Send to ATH {ARR}</button>
  <p class="note mt1">We use this only to reply to you. See <a class="gold" href="/privacy/">Privacy</a>.</p>
  <p class="form-status" role="status" aria-live="polite"></p>
 </form>
</div></section>""")

pages["/privacy/"] = ("Privacy — Above the Hill Developments", "What ATH collects, why, and how to remove it.",
 """<section class="block"><div class="wrap prose" style="max-width:820px"><p class="eyebrow">Policy</p><h1 class="display d-m">Privacy</h1>
<p>Effective October 7, 2026. Above the Hill Developments Inc. ("ATH") collects only what each workflow needs.</p>
<h2>What we collect</h2><ul>
<li><b>Free diagnostic:</b> the URL and description you submit, and what ATHOS observed on that one public page. Stored so your result has a shareable link.</li>
<li><b>Contact and waitlist requests:</b> name, email, optional organization and website, your message, the request type, and the diagnosis it came from (if any).</li>
<li><b>Basic request data:</b> your approximate country and browser type, used to prevent abuse.</li></ul>
<p>No account is required to use this site. We do not use advertising trackers.</p>
<h2>How we use it</h2><p>To produce your diagnosis, reply to you, and scope work you ask for. We don't sell personal information, and submitting a form does not give consent to unrelated reuse.</p>
<h2>Deep diagnostics</h2><p>Customer materials provided for a deep diagnostic are accessed only within the written scope you authorize, read-only wherever possible, are never used to train models without a separate written agreement, and are deleted at the end of the engagement or on request.</p>
<h2>Your choices</h2><p>To see, correct or delete your data, write via the <a class="gold" href="/contact/">contact form</a> (choose "Something else"). We'll confirm when it's done.</p>
</div></section>""")

pages["/terms/"] = ("Terms — Above the Hill Developments", "Ownership, diagnostics, and use of the ATH website.",
 """<section class="block"><div class="wrap prose" style="max-width:820px"><p class="eyebrow">Policy</p><h1 class="display d-m">Terms</h1>
<p>Effective October 7, 2026. These terms cover use of abovethehilldev.online, operated by Above the Hill Developments Inc. ("ATH").</p>
<h2>The free diagnostic</h2><p>ATHOS reports what it observed on one public page, what it infers from that, and what it cannot know. It is informational, not a guarantee of results. Where evidence is missing, the result says "unknown".</p>
<h2>Ownership</h2><ul>
<li>You own your materials. A diagnostic or deep diagnostic transfers no ownership of your code, content or data to ATH.</li>
<li>ATH owns ATH intellectual property — including ATHOS, its methods, the ATH Builder Dictionary, product designs and inventions. Purchasing the Dictionary or any product licenses its use; it does not transfer ownership of ATH inventions.</li></ul>
<h2>Deep diagnostics and services</h2><p>Deeper inspection happens only under a written scope you approve, with access you grant and may revoke. Default posture is read-only; ATH does not modify your systems during a diagnostic. Services are delivered under a separate scope and quote.</p>
<h2>Prices and availability</h2><p>Only products marked available can be bought. Waitlists and access requests create no obligation for either side. Membership (World Pass) does not include specialist products, ATH services or third-party costs unless stated in writing.</p>
<h2>Contact</h2><p>Questions: use the <a class="gold" href="/contact/">contact form</a>.</p>
</div></section>""")

pages["/404/"] = ("This path doesn't exist yet — ATH", "Page not found.",
 hero("path", "404", "This path doesn't<br>exist yet", "But the way over is still here.",
      btn("What's your hill?", "/diagnose/") + btn("Home", "/", "line"), size="d-m"))

SECTION_H2 = {"/build/": "Service families", "/language/": "What the dictionary includes", "/passport/": "Membership tiers", "/report/": "What a Hill Report contains", "/work/": "ATH inventions"}

# ---------------------------------------------------------------- write
def write():
    for route, (title, desc, body) in pages.items():
        d = os.path.join(ROOT, route.strip("/"))
        os.makedirs(d, exist_ok=True)
        # keep heading levels sequential for screen readers: a visually hidden h2 names card groups that follow the h1
        label = SECTION_H2.get(route)
        if label and re.search(r"<h1\b[\s\S]*?<h([23])\b", body) and re.search(r"<h1\b[\s\S]*?<h([23])\b", body).group(1) == "3":
            i = body.find("<h3", body.find("<h1"))
            j = body.rfind("<section", 0, i); j = j if j > body.find("<h1") else body.rfind("<div", 0, i)
            body = body[:j] + f'<h2 class="vh">{label}</h2>' + body[j:]
        with open(os.path.join(d, "index.html"), "w") as f:
            f.write(head(title, desc, route) + header(route) + body + FOOT)
    # GitHub Pages serves /404.html for unknown paths
    with open(os.path.join(ROOT, "404", "index.html")) as f:
        open(os.path.join(ROOT, "404.html"), "w").write(f.read().replace('href="/assets', 'href="/assets'))
    # redirects for alternate names (order lists /projects; old Base44 used /diagnosis)
    for src, dst in {"projects": "/work/", "diagnosis": "/diagnose/", "services": "/build/", "inventions": "/work/", "pricing": "/path/"}.items():
        os.makedirs(os.path.join(ROOT, src), exist_ok=True)
        open(os.path.join(ROOT, src, "index.html"), "w").write(f'<!doctype html><meta charset="utf-8"><title>Redirecting…</title><link rel="canonical" href="{SITE}{dst}"><meta http-equiv="refresh" content="0; url={dst}"><script>location.replace("{dst}"+location.search)</script><a href="{dst}">Continue</a>')
    open(os.path.join(ROOT, "CNAME"), "w").write("abovethehilldev.online\n")
    open(os.path.join(ROOT, ".nojekyll"), "w").write("")
    open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    urls = "".join(f"<url><loc>{SITE}{r}</loc></url>" for r in pages if r != "/404/")
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    print("wrote", len(pages), "pages")

if __name__ == "__main__":
    write()
