#!/usr/bin/env python3
"""ATH Official Website — static page generator.

Canon: Visual Canon Atlas v1, slide athWebsiteCanonPass3 (Founder finder doc 2026-10-07).
Prices: commercial/registry.json (v2026-10-13, Founder Super Max order) — see commercial/RECONCILIATION-2026-10-13.md.
Lineage (Founder lock 2026-10-07): focused systems start at $10/mo (Wavemotion $10/mo); World Pass $20/mo; WM Pro from $10/mo (App $10 · OS $50, corrected 2026-10-23); other specialist systems "plans vary";
Services show Founder-approved starting prices; WAVEMOTION clips come with its $10/$20/$50/$75 plans (the separate clip-bundle menu was retired by the Founder on 2026-10-22). Nothing on this
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
HERO_ART = {"/": "home", "/diagnose/": "diagnose", "/path/": "path", "/passport/": "passport", "/build/": "build", "/ecosystem/": "ecosystem", "/language/": "path", "/diagnose/deep/": "deep", "/work/": "path", "/company/": "home", "/404/": "path", "/offer/": "build"}
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
<script src="/assets/spaidbot.js" defer></script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""

def header(route):
    links = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if route.startswith(h) else ""}>{n}</a>' for n, h in NAV)
    return f"""<div class="mantra" aria-hidden="true"><span class="mq"><span>Plain truth · Higher ground · One vision · One language · One ecosystem · Invention company · Systems · Destinations</span><span>Plain truth · Higher ground · One vision · One language · One ecosystem · Invention company · Systems · Destinations</span></span></div>
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
   <div><p class="fh">Start</p><a href="/diagnose/">What's your hill?</a><a href="/diagnose/deep/">Deep diagnostic</a><a href="/build/">ATH Services</a><a href="/offer/">Everything you get</a><a href="/contact/">Contact ATH</a></div>
   <div><p class="fh">Company</p><a href="/company/">Company</a><a href="/work/">Inventions &amp; work</a><a href="/path/">How ATH works</a><a href="/report/">The Hill Report</a></div>
   <div><p class="fh">World</p><a href="https://thewow.online/">WOW OS</a><a href="https://wavemotion.live/">Wavemotion</a><a href="/ecosystem/">Ecosystem</a><a href="/passport/">Passport &amp; World Pass</a><a href="/language/">Builder Dictionary</a><a href="/privacy/">Privacy</a><a href="/terms/">Terms</a></div>
  </div>
  <div class="foot-line"><span class="mantra2">Heavens above · A realm to explore · Multiple destinations · One builder</span><span>© <span data-year>2026</span> Above the Hill Developments Inc. <a class="sha-ar" href="https://mission.abovethehilldev.online/founders/login" rel="nofollow" aria-label="Founders" title="שַׁעַר">שַׁעַר</a></span></div>
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
    ("door", "$10 / mo", "Focused door", "Focused systems start at $10/mo · Wavemotion $10/mo", "", "/ecosystem/#wavemotion"),
    ("lattice", "$20 / mo", "Join the world", "Passport spine · World Pass membership", "", "/passport/"),
    ("triangle", "Specialist", "Serious systems", "WealthyMindsets Pro from $10/mo · plans vary by system", "", "/ecosystem/#specialist"),
    ("peaks", "Services", "Build it for me", "Websites from $100 · WAVEMOTION $10–$75 a month · apps from $1,000", "", "/build/#pricing"),
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


# ---------------------------------------------------------------- commercial registry (single source for every price on this site)
import json
REG = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "commercial", "registry.json")))
RET = REG["services_retained"]
CLIPS = [tuple(c) for c in RET["clips"]]
STARTS = [(x["name"], x["price"], x["id"], x["icon"]) for x in RET["starts"]]
PKG = REG["packages"]
WM = REG["wavemotion_plans"]
CAT = {o["id"]: o for o in REG["catalog"]}
def cat_price(oid):
    o = CAT[oid]
    assert o["status"] in ("LIVE", "SCOPED"), f"{oid} is {o['status']}: not for sale, so it is not shown as a price"
    return o["price"]
# Homepage "Start with what you do": one door per kind of visitor, each with its real price and next step.
# Prices come from the commercial registry above, never typed here; WM Pro shows only its free guest account
# until a paid checkout is proven (Founder ship order, 2026-10-21).
OUTCOMES = [
 ("site", "You run a local business", "Quick Start website", "One mobile page with your hours, services, photos and a call button, linked to the booking or ordering you already use.", lambda: cat_price("ath-quick-start"), "See it for your town", "/websites/"),
 ("content", "You make videos, music or sermons", "WAVEMOTION", "Turn one video into short clips. You approve before anything posts.", lambda: cat_price("wm-plans"), "Open WAVEMOTION", "https://www.wavemotion.live/"),
 ("systems", "You trade or want to learn to", "Wealthy Mindsets Pro", "A trading workspace with a chart, a journal and lessons. Education and tools, not financial advice.", lambda: "Free guest account" if "free guest account" in cat_price("wmp-pro") else None, "Take the guest tour", "https://wealthymindsetspro.com/welcome"),
 ("path", "You want to learn something new", "WOW Academy", "Price-action lessons, languages and a book library, open to browse as a guest.", lambda: cat_price("wow-academy-free"), "Visit the campus", "https://thewow.online/academy"),
 ("link", "You want a place to belong", "Passport", "One identity across WOW OS rooms: Lounge, Academy, Shop, TV, Music and Radio.", lambda: cat_price("wow-passport"), "Get a Passport", "https://thewow.online/passport"),
 ("hill", "Your business has a bigger hill", "ATHOS Diagnostic", "A free diagnosis first. Custom systems are scoped in writing before any price.", lambda: "Free, then by written quote", "What's your hill?", "/diagnose/"),
]
def outcome_cards():
    out = []
    for icon, who, name, does, price, cta, href in OUTCOMES:
        pr = price()
        assert pr, f"{name}: no price available"
        out.append(f'<article class="panel panel-pad card outcome" data-outcome="{name}">{ic(icon, "icon-sm")}<p class="eyebrow mt1">{who}</p><h3>{name}</h3><p>{does}</p>'
                   f'<p class="mt1"><b class="outcome-price">{pr}</b></p><p class="mt2">{btn(cta, href, "line")}</p></article>')
    return "".join(out)
def money(p): return f"${p:,}"
def per_clip(n, p): return f"${p / n:,.2f}"
def clip_rows():
    return "".join(f'<div class="pt-row" role="row"><span role="cell"><b>{n} clips</b></span><span role="cell" class="pt-price">${p}</span><span role="cell" class="pt-allowance">{per_clip(n, p)} per clip</span><span role="cell"><a class="btn btn-line btn-sm" href="/contact/?intent=services&amp;package=clips-{n}" aria-label="Start {n} clips package">Start</a></span></div>' for n, p in CLIPS)
def start_rows():
    return "".join(f'<li>{ic(i,"icon-sm")}<div style="flex:1"><b>{t}</b><span>from ${p}</span></div><a class="btn btn-line btn-sm" href="/contact/?intent=services&amp;package={s}" aria-label="Start {t}">Start</a></li>' for t, p, s, i in STARTS)
def pkg_cards():
    out = []
    for p in [x for x in PKG if not x["from"]]:
        inc = "".join(f"<li>{html.escape(i)}</li>" for i in p["includes"])
        eco = "".join(f'<li><span class="tag {"live" if e.get("state") == "LIVE" else "dim"}">{"Included" if e.get("state") == "LIVE" else "Not active yet"}</span> {html.escape(e["label"])}<span class="note">{html.escape(e["note"])}</span></li>' for e in p.get("ecosystem", []))
        out.append(f'''<article class="panel panel-pad pkg{' pkg-featured' if p.get('featured') else ''}" aria-labelledby="pkg-{p['id']}">
   {ic(p['icon'])}<h3 id="pkg-{p['id']}">{p['name']}</h3><p class="pkg-price">{money(p['price'])} <span>one time</span></p><p class="body">{html.escape(p['summary'])}</p>
   <p class="eyebrow mb0">Included</p><ul class="pkg-list">{inc}</ul>
   {f'<p class="eyebrow mb0">Ecosystem extras</p><ul class="pkg-list pkg-eco">{eco}</ul>' if eco else ''}
   <div class="ctas mt1">{btn(f"Pay {money(p['price'])} — start now", p['pay_url'], attrs='rel="noopener"') if p.get('pay_url') else ''}{btn("Ask a question first", f"/contact/?intent=services&amp;package={p['id']}", "line")}</div>
   {'<p class="note mb0">Secure card checkout by Stripe. ATH emails your intake form after your payment.</p>' if p.get('pay_url') else ''}</article>''')
    return "".join(out)
def ladder_rows():
    return "".join(f'<li>{ic(p["icon"],"icon-sm")}<div style="flex:1"><b>{p["name"]}</b><span>{(money(p["price"]) + "–" + money(p["price_max"])) if p.get("price_max") else "from " + money(p["price"])} · {html.escape(p["summary"])}</span></div><a class="btn btn-line btn-sm" href="/contact/?intent=services&amp;package={p["id"]}" aria-label="Request a scope for {p["name"]}">Scope it</a></li>' for p in PKG if p["from"])
def wm_rows():
    return "".join(f'<div class="pt-row" role="row"><span role="cell"><b>{html.escape(p["name"])}</b></span><span role="cell" class="pt-price">${p["price"]}/mo</span><span role="cell" class="pt-allowance">{p["clips"]} standard clips / month</span><span role="cell"><a class="btn btn-line btn-sm" href="https://www.wavemotion.live/#pricing" rel="noopener" aria-label="View WAVEMOTION {html.escape(p["name"])} plan">View plans</a></span></div>' for p in WM["plans"])
def catalog_js():
    m = {}
    for p in PKG:
        m[p["id"]] = {"label": f'{p["name"]} — {"from " if p["from"] else ""}{money(p["price"])}{"" if p["from"] else " one time"}', "terms": True}
    for t, p, s, i in STARTS: m[s] = {"label": f"{t} — from ${p}"}
    for p in WM["plans"]: m[p["id"]] = {"label": f'WAVEMOTION {p["name"]} — ${p["price"]}/month ({p["clips"]} standard clips)'}
    m["custom"] = {"label": "Custom OS / app / platform — diagnose → scope → quote"}
    data = {"version": REG["version"], "payment": REG["payment"]["state"], "packages": m, "disclosures": REG["package_disclosures"]}
    return '<script type="application/json" id="ath-catalog">' + json.dumps(data).replace("</", "<\\/") + "</script>"

# ---------------------------------------------------------------- capability map (SP-055 / R41, 2026-10-23)
# Founder: "do everything a content platform does, plus everything else, cheaper — it's about presentation."
# One grouped "what we do" map. Every card names the ATH owner (Founder ownership order, 2026-10-21: no new
# standalone Content OS brand), an honest status, a price from the registry or "By quote", and a real next step.
P = {p["id"]: p for p in PKG}
def pk(pid):
    p = P[pid]
    if p.get("price_max"): return f'{money(p["price"])}–{money(p["price_max"])}'
    return ("from " if p["from"] else "") + money(p["price"])
STATUS = {"live": ("Live now", "live"), "inc": ("Included", ""), "quote": ("By quote", ""),
          "dev": ("In development", "dim"), "nb": ("Not built yet", "dim")}
OWNERS = [
 ("ATH", "peaks", "Corporate front door", "This website, discovery, service offers, quotes and the people who answer.", "ATHOS for diagnosis · ATH Commerce for checkout"),
 ("ATH Web Studio", "site", "Websites & presentation", "Client websites, brand themes, reusable sections, previews, hosting and domains.", "WAVEMOTION videos · ATH Commerce links · Passport"),
 ("WAVEMOTION", "content", "Content & campaigns", "Clips, captions, campaign workflow, approvals, publishing and what-worked learning.", "Web Studio pages as destinations · Passport"),
 ("ATHOS · Atlas", "ai", "Intelligence & memory", "Diagnosis, Spaidbot, AI roles and orchestration; Atlas keeps decisions, sources and proof.", "The live price list (catalog.json) · every engagement's evidence"),
 ("ATH Commerce", "own", "Orders & payments", "Card checkout, orders, entitlements and receipts for everything ATH sells.", "Stripe · Shopify · Passport"),
 ("SPADE Business · PowerTribes", "flow", "Customers & teams", "Prospecting, CRM, sales routing, workforce and business operations.", "In development: not sold yet"),
 ("WOW OS", "lattice", "Identity, community & learning", "Passport, World Pass, Lounge, Academy, Shop, TV, Music and Radio.", "Every ATH app as it connects to Passport"),
]
def caps():
    """(group id, group title, eyebrow, [ (name, does, owner, status, price, cta, href, on_home) ])"""
    wm = cat_price("wm-plans").replace("/month", " a month")
    return [
     ("presence", "Build your presence", "Websites & digital experience", [
      ("Business website, done for you", "A mobile site with your services, hours, photos and buttons that work, linked to the booking or ordering you already use.", "ATH Web Studio", "live", f'{money(P["quick-start"]["price"])} or {money(P["business-growth"]["price"])} one time', "Here's everything you get", "/offer/", True),
      ("Professional website", "An expanded branded site: content management, commerce, booking and course presentation as scoped.", "ATH Web Studio", "quote", pk("professional-website"), "Scope it", "/contact/?intent=services&amp;package=professional-website", True),
      ("Brand themes & reusable sections", "Three tuned site styles built from reusable sections: menus and price lists, galleries, hours, story.", "ATH Web Studio", "inc", "In every site", "See sample sites", "/sites/", False),
      ("Preview & approval", "You see your site on a preview link, kept out of search, before it goes live. Revisions as your package states.", "ATH Web Studio", "inc", "In every site", "How delivery works", "/offer/#how", True),
      ("Hosting & your own domain", "Fast static hosting. Move to your own domain whenever you like; the registrar fee (about $12 a year) is yours, at cost.", "ATH Web Studio", "inc", "Hosting included", "See packages", "/offer/", False),
     ]),
     ("content", "Create & distribute content", "Video, clips & campaigns", [
      ("Clips from your videos", "Turn one long video into short captioned clips. You approve every clip before anything posts.", "WAVEMOTION", "live", wm, "See WAVEMOTION plans", "https://www.wavemotion.live/#pricing", True),
      ("Campaign workflow", "Record, prepare, approve, publish and learn, through the accounts you connect and within each platform's permissions.", "WAVEMOTION", "live", "In every plan", "Open WAVEMOTION", "https://www.wavemotion.live/", False),
      ("Website + two promo videos", "A scoped site plus two 30–60 second videos made from your footage and photos, and a launch campaign.", "ATH Web Studio + WAVEMOTION", "quote", pk("cinematic-launch"), "Scope it", "/contact/?intent=services&amp;package=cinematic-launch", True),
      ("Weekly content, made for you", "Four promo videos and eight captioned clips a month, with a posting kit. Twice-weekly is " + CAT["ath-content-twice"]["price"] + ".", "WAVEMOTION + ATH", "quote", CAT["ath-content-weekly"]["price"], "Ask about it", "/contact/?intent=wavemotion", False),
     ]),
     ("intelligence", "Intelligence & AI agents", "Diagnosis, assistants & memory", [
      ("Spaidbot assistant", "A free AI assistant on every page of this site. It answers from ATH's live price list and hands you to a person.", "ATHOS", "live", "Free", "Ask Spaidbot", "/contact/#ask", True),
      ("ATHOS Diagnostic", "Reads one public page, separates what it observed from what it inferred, and says unknown when it doesn't know.", "ATHOS", "live", "Free", "What's your hill?", "/diagnose/", True),
      ("Deep diagnostic", "Read-only inspection of the sources you authorize (code, docs, analytics, flows), delivered as a Hill Report.", "ATHOS · Atlas", "quote", "By written quote", "Request one", "/diagnose/deep/", False),
      ("Automation & business systems", "Apps, back ends, accounts, dashboards, integrations and automations, scoped in writing before any work starts.", "ATHOS + ATH Web Studio", "quote", pk("business-app-system"), "Scope it", "/contact/?intent=services&amp;package=business-app-system", False),
     ]),
     ("commerce", "Sell & get paid", "Checkout, apps & channels", [
      ("Checkout & booking links", "Your site's buttons go to the checkout, booking or ordering tool you already use. Nothing new to learn.", "ATH Commerce + ATH Web Studio", "inc", f'In the {money(P["business-growth"]["price"])} site', "See Business Growth", "/offer/#business-growth", False),
      ("Installable web app", "A scoped installable web app, or a single-platform app quoted on its own.", "ATH Web Studio", "quote", pk("app-starter"), "Scope it", "/contact/?intent=services&amp;package=app-starter", True),
      ("iOS + Android apps", "Basic apps for both stores on one shared architecture, under a written scope.", "ATH Web Studio", "quote", pk("mobile-app-bundle"), "Scope it", "/contact/?intent=services&amp;package=mobile-app-bundle", False),
      ("Web, mobile, TV & SDK", "One scoped system across web, mobile, television and integrations.", "ATH Web Studio", "quote", pk("omnichannel-system"), "Scope it", "/contact/?intent=services&amp;package=omnichannel-system", False),
     ]),
     ("community", "Identity, community & learning", "WOW OS", [
      ("Passport", "One identity across ATH apps: permissions, ownership and receipts that stay with you.", "WOW OS", "live", cat_price("wow-passport"), "Get a Passport", "https://thewow.online/passport", True),
      ("World Pass", "One membership on your Passport across the connected ATH world. Cancel any time.", "WOW OS", "live", cat_price("wow-world-pass").replace("/month", " a month"), "Get World Pass", "https://thewow.online/passport", True),
      ("WOW Academy", "Idea Library, The Polyglot's Mind and Student of the Game. Stamps come from proof, not attendance.", "WOW OS", "live", cat_price("wow-academy-free"), "Visit the campus", "https://thewow.online/academy", False),
      ("Lounge, TV, Music, Radio & Shop", "Rooms to connect, watch, listen and shop, entered from WOW OS. Guests welcome.", "WOW OS", "live", "Free to enter", "Enter WOW OS", "https://thewow.online/", False),
     ]),
     ("teams", "Customers, teams & specialist systems", "SPADE Business · PowerTribes · specialist OS", [
      ("Prospecting, CRM & sales routing", "Find, qualify and follow up with customers, connected to your site and campaigns.", "SPADE Business", "dev", "Not sold yet", "Request access", "/contact/?intent=services", True),
      ("Workforce & operations OS", "Business, sales, workforce and leadership operations in one system.", "PowerTribes", "dev", "Not sold yet", "Request access", "/contact/?intent=powertribes", False),
      ("Wealthy Mindsets Pro", "A trading workspace with a chart, a journal and lessons. Education and tools, not financial advice.", "Wealthy Mindsets Pro", "live", "Free guest account", "Take the guest tour", "https://wealthymindsetspro.com/welcome", True),
     ]),
    ]
def cap_card(name, does, owner, st, price, cta, href, *_):
    label, cls = STATUS[st]
    ext = href.startswith("http")
    sb = ' data-sb-open="1"' if href.endswith("#ask") else ""
    return (f'<article class="cap" data-cap="{html.escape(name)}" data-status="{st}"><div class="cap-top"><span class="tag {cls}">{label}</span><span class="cap-owner">{html.escape(owner)}</span></div>'
            f'<h3>{html.escape(name)}</h3><p>{html.escape(does)}</p>'
            f'<div class="cap-foot"><b class="cap-price">{html.escape(price)}</b><a class="cap-go" href="{href}"{sb}{" rel=\"noopener\"" if ext else ""}>{cta} {ARR}</a></div></article>')
GROUP_ICON = {"presence": "site", "content": "content", "intelligence": "ai", "commerce": "own", "community": "lattice", "teams": "flow"}
def cap_tiles():
    """Homepage: the whole map at a glance, one tile per group, every capability a row with status and price."""
    out = []
    for gid, title, eyebrow, items in caps():
        norm = lambda o: "ATH Web Studio" if o == "Web Studio" else o
        owners = list(dict.fromkeys(norm(o.strip()) for c in items for o in re.split(r"[+·]", c[2])))
        rows = "".join(
            f'<li><a href="{c[6]}"{" data-sb-open=\"1\"" if c[6].endswith("#ask") else ""}{" rel=\"noopener\"" if c[6].startswith("http") else ""}><span class="ct-name">{html.escape(c[0])}</span>'
            f'<span class="ct-meta"><span class="ct-dot ct-{c[3]}" aria-hidden="true"></span>{STATUS[c[3]][0]}<span class="ct-sep" aria-hidden="true">·</span><b>{html.escape(c[4])}</b></span></a></li>' for c in items)
        out.append(f'<article class="ct" id="tile-{gid}"><header class="ct-head">{ic(GROUP_ICON[gid])}<div><p class="eyebrow mb0">{eyebrow}</p><h3>{title}</h3></div></header>'
                   f'<ul class="ct-list">{rows}</ul><p class="ct-own"><span>Owned by</span> {html.escape(" · ".join(owners))}</p></article>')
    return '<div class="ct-grid">' + "".join(out) + '</div>'
def cap_map(home=False):
    out = []
    for gid, title, eyebrow, items in caps():
        shown = [c for c in items if c[7]] if home else items
        out.append(f'<section class="cap-group" id="cap-{gid}" aria-labelledby="cg-{gid}"><header class="cap-head">{ic(GROUP_ICON[gid])}<div><p class="eyebrow mb0">{eyebrow}</p><h3 class="cap-title" id="cg-{gid}">{title}</h3></div></header>'
                   f'<div class="cap-grid" data-n="{len(shown)}">{"".join(cap_card(*c) for c in shown)}</div></section>')
    return '<div class="cap-map">' + "".join(out) + '</div>'
# "Everything a headless CMS / digital experience platform gives you — plus the business systems."
# No competitor is named. Each row says how ATH delivers it today, and says so when it does not.
COMPARE_PLATFORM = [
 ("Structured, reusable content", "Every site is built from structured content and reusable sections, so a change lands everywhere it belongs.", "inc"),
 ("Visual editing & live preview", "You review a preview link and ATH makes the edits for you. A self-serve visual editor is not built yet.", "inc"),
 ("Media & asset library", "Your photos and logo are placed, sized and given alt text. Video assets live in WAVEMOTION.", "inc"),
 ("Brand rules & templates", "Three tuned themes, applied consistently across every page of your site.", "inc"),
 ("Drafts, approvals & publishing", "Preview, approve, publish. In WAVEMOTION you approve every clip before it posts.", "live"),
 ("Multichannel delivery", "Web and phone today, video channels through WAVEMOTION; apps, TV and SDKs by written scope.", "live"),
 ("AI agents", "Spaidbot and the ATHOS Diagnostic are free and live; deeper automation is scoped.", "live"),
 ("Localization", "Additional languages are scoped and quoted per project.", "quote"),
 ("Audience data & personalization", "WAVEMOTION learns from campaign results. Customer profiles and personalization are not built yet.", "nb"),
 ("Hosting & delivery", "Fast static hosting included; your own domain at the registrar's price.", "inc"),
]
def compare_plus():
    return [
     ("Websites built for you", f'Card-payable sites at {money(P["quick-start"]["price"])} and {money(P["business-growth"]["price"])}, no sales call needed.', "live"),
     ("Video clips & campaigns", "WAVEMOTION plans " + cat_price("wm-plans").replace("/month", " a month") + ", clips included.", "live"),
     ("A free diagnosis before you buy", "ATHOS tells you what's actually in the way, including when you need nothing.", "live"),
     ("Identity, membership & community", "Passport (free), World Pass and the rooms of WOW OS.", "live"),
     ("Learning", "WOW Academy tracks, free to practise.", "live"),
     ("Apps & whole business systems", f'Starting points from {money(P["app-starter"]["price"])} to {money(P["omnichannel-system"]["price"])}, scoped in writing first.', "quote"),
     ("A person who reads every message", "A person at ATH reads every request and replies.", "live"),
    ]
def compare_rows(rows):
    return "".join(f'<div class="cmp-row" role="row"><span role="rowheader" class="cmp-k">{k}</span><span role="cell" class="cmp-v">{v}</span><span role="cell"><span class="tag {STATUS[st][1]}">{STATUS[st][0]}</span></span></div>' for k, v, st in rows)
def compare_section(sid="compare"):
    return f"""<section class="block" id="{sid}"><div class="wrap">
 <div class="block-head"><div><p class="eyebrow">One ecosystem</p><h2 class="display d-m mt1">Everything a content platform gives you.<br><span class="gold">Plus the business systems.</span></h2></div>
  <p class="note" style="max-width:44ch">What a headless CMS or digital experience platform covers, and how ATH delivers each part today, row by row. Where something isn't built, this table says so.</p></div>
 <div class="grid cmp-grid" style="grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:18px;align-items:start" data-collapse>
  <div class="panel panel-pad"><p class="panel-title">The content platform essentials</p><div class="cmp" role="table" aria-label="Content platform capabilities and how ATH delivers them">{compare_rows(COMPARE_PLATFORM)}</div></div>
  <div class="panel panel-pad cmp-plus"><p class="panel-title">Plus what a content platform leaves to you</p><div class="cmp" role="table" aria-label="Business systems ATH adds">{compare_rows(compare_plus())}</div>
   <div class="ctas mt2">{btn("Here's everything you get", "/offer/")}{btn("All prices", "/build/#pricing", "line")}</div></div>
 </div>
</div></section>"""
def pkg_ladder():
    """The transparent package ladder, $100 → $8,000, every step from the registry."""
    steps = []
    for p in PKG:
        pay = p.get("pay_url")
        href = "/offer/#" + p["id"] if pay else f'/contact/?intent=services&amp;package={p["id"]}'
        price = (money(p["price"]) + "–" + money(p["price_max"])) if p.get("price_max") else money(p["price"])
        lead = "scoped range" if p.get("price_max") else ("starting at" if p["from"] else "one time")
        steps.append(f'<a class="pl-step{" pl-card" if pay else ""}" href="{href}"><span class="pl-lead">{lead}</span><span class="pl-price">{price}</span><span class="pl-name">{html.escape(p["name"])}</span><span class="pl-how">{"Pay by card" if pay else "Written scope"}</span></a>')
    return '<nav class="pl" aria-label="Website and app packages, lowest to highest">' + "".join(steps) + '</nav>'

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
<section class="block" id="start"><div class="wrap">
 <div class="block-head"><div><p class="eyebrow">Start with what you do</p><h2 class="display d-m mt1">Find your door</h2></div>{btn("All prices", "/build/#pricing", "line")}</div>
 <div class="grid g3">{outcome_cards()}</div>
</div></section>
<section class="block cap-block" id="what-we-do"><div class="wrap">
 <div class="block-head"><div><p class="eyebrow">What ATH does</p><h2 class="display d-m mt1">One ecosystem.<br>Every part has an owner.</h2></div>
  <div style="max-width:46ch"><p class="body mb0">Websites, content, AI, checkout, community and the systems behind them, each run by one ATH product. Every card shows who owns it, whether it's live, and what it costs.</p><p class="mt1 mb0">{btn("The full map", "/ecosystem/#map", "line")}</p></div></div>
 {cap_tiles()}
</div></section>
""" + compare_section() + f"""
<section class="block"><div class="wrap">
 <div class="block-head"><div><p class="eyebrow">Transparent prices</p><h2 class="display d-m mt1">From $100 to $8,000.<br>Every step on the page.</h2></div>{btn("Here's everything you get", "/offer/", "line")}</div>
 {pkg_ladder()}
 <p class="note mt2">Quick Start and Business Growth are paid by card. Everything above them starts with a written scope, and that scope sets the real number before anything is charged.</p>
</div></section>
<section class="block"><div class="wrap">
 <div class="block-head"><div><p class="eyebrow">Inventions</p><h2 class="display d-m mt1">Built by ATH</h2></div>{btn("All inventions", "/work/", "line")}</div>
 <div class="grid g3">
  <article class="panel panel-pad card"><span class="tag live">Live today</span><h3>ATHOS Diagnostic</h3><p>The free hill-finder on this site. Inspects public evidence, separates what it observed from what it inferred, and says "unknown" when it doesn't know.</p><p class="mt2">{btn("Run it", "/diagnose/", "line")}</p></article>
  <article class="panel panel-pad card"><span class="tag">Open door</span><h3>WealthyMindsets Pro</h3><p>One complete professional trading operating system — the chart as the room, intelligence that respects price truth. Start with a free guest account. No profits promised.</p><p class="mt2"><a class="btn btn-line" href="https://wealthymindsetspro.com" rel="noopener">Visit WM Pro {ARR}</a></p></article>
  <article class="panel panel-pad card"><span class="tag live">Open door</span><h3>Wavemotion</h3><p>Creator + business movement OS — record, prepare, launch, distribute, learn. One permanent Living Destination. Starter $10 · Creator $20 · Pro $50 · Living Cinema Studio $75 per month.</p><p class="mt2">{btn("Open Wavemotion", "https://www.wavemotion.live/", "line")}</p></article>
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
  <div class="panel panel-pad"><p class="panel-title">$10 opens a focused door. $20 joins the world.</p>
   <p class="body"><b>Focused systems start at $10/month</b> — one product for one job, like Wavemotion. <b>World Pass at $20/month</b> is one predictable membership across the connected ATH world. Specialist operating systems carry their own plans — WealthyMindsets Pro starts at $10/month.</p>
   <p class="panel-title mt2">What $20 is — and isn't</p>
   <p class="body">World Pass is paid ecosystem membership layered on your Passport identity. It does <b>not</b> automatically include every specialist product, professional system, ATH service, third-party cost, or unlimited expensive infrastructure.</p>
   <dl class="hpa mt2"><dt>Identity</dt><dd>≠ membership</dd><dt>Membership</dt><dd>≠ owning every product</dd><dt>Membership</dt><dd>≠ professional infrastructure</dd></dl></div>
  <div class="panel panel-pad"><p class="panel-title">No surprise costs</p>
   <p class="body">Some things cost real money to run — market data, heavy AI compute, video/image/audio generation, mass messaging, unusual storage or bandwidth. We handle those with included allowances, bring-your-own credentials where lawful, add-ons or pass-through costs. Never hidden behind "unlimited".</p></div>
 </div>
 <div class="panel panel-pad mt2"><p class="panel-title">Availability today</p>
  <ul class="rows">
   <li>{ic("free","icon-sm")}<div><b>Free ATH Diagnostic</b><span>Available now — no account required. <a class="gold" href="/diagnose/">Run it</a>.</span></div></li>
   <li>{ic("door","icon-sm")}<div><b>Focused systems — from $10 / month</b><span>Wavemotion: the creator + business movement OS. Starter $10 · Creator $20 · Pro $50 · Living Cinema Studio $75 per month. No permanent free operator tier; public Living Destinations stay viewable. <a class="gold" href="/contact/?intent=wavemotion">Start Wavemotion with ATH</a>.</span></div></li>
   <li>{ic("lattice","icon-sm")}<div><b>World Pass — $20 / month</b><span>Available now in WOW OS, on your free Passport. <a class="gold" href="https://thewow.online/passport" rel="noopener">Get World Pass</a>.</span></div></li>
   <li>{ic("triangle","icon-sm")}<div><b>Specialist systems — plans vary by operating system</b><span>WealthyMindsets Pro is from $10/month: WM Pro App $10/month, WM Pro OS $50/month, plus a free guest account. Exchange, data or broker fees ATH doesn't control stay separate. No profit or return is ever promised. <a class="gold" href="https://wealthymindsetspro.com" rel="noopener">Go to WM Pro</a>.</span></div></li>
   <li>{ic("peaks","icon-sm")}<div><b>ATH Services — starting prices published</b><span>Websites from $100 (Quick Start) and $200 (Business Growth), WAVEMOTION plans $10–$75 a month with clips included, apps from $1,000, custom systems scoped and quoted. <a class="gold" href="/build/#pricing">See service prices</a>.</span></div></li>
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
   ("triangle","Specialist Entitlements","Plans vary","WealthyMindsets Pro is from $10/month (App $10 · OS $50). PowerTribes, Dreamboard and future systems carry their own plans."),
   ("own","Purchases &amp; Ownership","Yours","What you bought and what remains yours, carried by Passport where supported.")])}
 </div>
 <div class="grid g2 mt3" id="benefits">
  <div class="panel panel-pad"><p class="panel-title">If a member cancels</p><p class="body mb0">The person doesn't stop existing. Identity, lawful ownership, receipts and applicable durable rights persist. Membership-only benefits end.</p></div>
  <div class="panel panel-pad"><p class="panel-title">Availability</p><p class="body">Passport is free and World Pass is $20/month — both live in WOW OS today, with a real Stripe checkout and cancel any time.</p><div class="ctas mt1">{btn("Get your free Passport", "https://thewow.online/passport/claim")}{btn("Get World Pass", "https://thewow.online/passport", "line")}</div></div>
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
  {"".join(f'<div class="panel panel-pad card svc" style="display:flex;gap:16px">{ic(i)}<div><h3 style="margin-top:0">{t}</h3><p>{d}</p></div></div>' for i,t,d in [
   ("site","Websites &amp; Destinations","Sites, Living Destinations, conversion paths."),
   ("content","Content &amp; Campaigns","Clips with WAVEMOTION plans, launch systems, distribution."),
   ("systems","Systems &amp; Automation","Business ops, integrations, custom applications."),
   ("app","Custom Applications &amp; Platforms","Products and larger platforms, engineered to last."),
   ("link","Implementation &amp; Integration","Make the tools you already pay for work together."),
   ("q","Consulting","When the honest first step is clarity, not code.")])}
 </div>
 <section class="mt3" id="pricing" aria-labelledby="pricing-h">
  <h2 class="display d-m" id="pricing-h">Website &amp; app packages</h2>
  <p class="body">Quick Start and Business Growth can be paid by card right now. Prefer to talk first? Ask a question and ATH replies with a written scope — nothing is charged until you pay. <a class="gold" href="/sites/">See sample sites</a> to picture yours, or <a class="gold" href="/offer/">see everything you get</a>, line by line.</p>
  <div class="grid g2 mt2" style="align-items:stretch">{pkg_cards()}</div>
  <div class="grid mt2" style="grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr);gap:18px;align-items:start" data-collapse>
   <div class="panel panel-pad">
    <p class="panel-title">Bigger builds — starting prices</p>
    <ul class="rows">{ladder_rows()}</ul>
    {"".join(f'<p class="note mt1"><span class="tag {"live" if e.get("state") == "LIVE" else "dim"}">{"Included" if e.get("state") == "LIVE" else "Not active yet"}</span> <b>Every package from $500:</b> {html.escape(e["label"])}. {html.escape(e["note"])}</p>' for e in next(p for p in PKG if p["price"] >= 500)["ecosystem"][1:])}
    <div class="custom-os mt2"><p class="eyebrow mb0">Not sure which?</p><p class="h-serif mt1" style="font-size:24px">Diagnose → scope → quote</p><p class="note">Every “from” price becomes a real number only after a written scope.</p><div class="ctas mt1">{btn("Get a free diagnostic", "/diagnose/")}{btn("Request a quote", "/contact/?intent=services&amp;package=custom", "line")}</div></div>
   </div>
   <div class="panel panel-pad">
    <p class="panel-title">What every package discloses</p>
    <ul class="pkg-list">{"".join(f"<li>{html.escape(d)}</li>" for d in REG["package_disclosures"])}<li>Ecosystem extras marked “Not active yet” are not delivered until that product is operational. No subscription renews without your separate consent.</li></ul>
   </div>
  </div>
  <h2 class="display d-m mt3" id="services-h">Done-for-you services</h2>
  <div class="grid mt2" style="grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr);gap:18px;align-items:start" data-collapse>
   <div class="panel panel-pad">
    <p class="panel-title">Clips come with your WAVEMOTION plan</p>
    <p class="body mb0">There is no separate clip menu. Every WAVEMOTION plan includes its clips each month — see <a class="gold" href="#wavemotion-plans">WAVEMOTION plans</a> below. Orders placed before the change are honored as bought.</p>
   </div>
   <div class="panel panel-pad">
    <p class="panel-title">Setup services — starting prices</p>
    <ul class="rows">{start_rows()}</ul>
   </div>
  </div>
  <div class="panel panel-pad mt2" id="wavemotion-plans">
   <p class="panel-title" id="wavemotion-plans">WAVEMOTION plans</p>
   <div class="price-table wm-plan-table" role="table" aria-label="WAVEMOTION monthly plans"><div class="pt-row pt-head" role="row"><span role="columnheader">Plan</span><span role="columnheader">Monthly</span><span role="columnheader">Allowance</span><span role="columnheader">Next step</span></div>{wm_rows()}</div>
   <p class="note">Standard clip allowances are 40 / 80 / 250 / 250 per month. Cinematic generation is not open; production credits await measured provider costs. Platform publishing depends on the permissions of your connected accounts. Your clips come with your plan.</p>
   <p class="body mb0">A 14-day trial needs no card. Choose a plan inside <a class="gold" href="https://www.wavemotion.live/#pricing" rel="noopener">WAVEMOTION</a>; this site does not charge a second subscription.</p>
  </div>
  <p class="note mt2">“From” prices are starting points for a defined scope, not unlimited work. Third-party costs (ads, domains, paid tools) are passed through at cost, never hidden. Catalog version {REG["version"]}.</p>
 </section>
 <div class="panel panel-pad mt3"><p class="panel-title">How an engagement works</p>
  <div class="grid g5" style="gap:0">
   {"".join(f'<div style="padding:12px 10px;border-left:1px solid var(--gold-faint)"><p class="eyebrow mb0">0{n}</p><p class="h-serif" style="font-size:22px;margin-top:6px">{t}</p><p class="note">{d}</p></div>' for n,t,d in [
    (1,"Diagnostic","Free. Evidence first."),(2,"Scope","What changes, and what doesn't."),(3,"Quote","A real number for a real scope."),(4,"Build","ATH implements."),(5,"Proof &amp; handoff","Hill receipt: what improved.")])}
  </div>
  <p class="note mt2 mb0">Published prices are starting points; anything larger starts with a diagnosis, then a scope, then a quote.</p></div>
 <div class="panel panel-pad mt3"><p class="panel-title">Example paths (conceptual)</p>
  <div class="grid g3">
   {"".join(f'<dl class="hpa"><dt>The Hill</dt><dd>{a}</dd><dt>The Path</dt><dd>{b}</dd><dt>Above</dt><dd>{c}</dd></dl>' for a,b,c in [
    ("Interest without conversion.","Aligned message and destination.","Clearer next step for visitors."),
    ("Tools without a system.","Routed to focused software.","A moving operating path."),
    ("Idea with no build path.","ATH scoped and built a first version.","Something real to test in the market.")])}
  </div>
  <p class="note mt2 mb0">Case frames are structural examples only — no real client claims, logos, or statistics.</p></div>
</div></section>""" + cta_block("Build my path", "Start with the free diagnostic, or tell us about the project directly."))

# ---------------------------------------------------------------- SP-085 honest offer stack (2026-10-23)
# "Here's everything you get", from the registry only: no countdown, no invented values, no "today only".
# A dollar value appears only where the registry itself states one; extras that are not switched on are
# listed apart and not counted.
CHECK = '<svg class="vs-ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 12.5 4 4 8-9"/></svg>'
def vs_line(label, note="", dim=False):
    m = re.search(r"\s*\((\$\d+) value\)", label)
    val = f'<span class="vs-val">{m.group(1)} value</span>' if m else ""
    label = label.replace(m.group(0), "") if m else label
    return (f'<li class="vs-row{" vs-dim" if dim else ""}">{CHECK if not dim else ic("lock", "vs-ic")}<div><b>{html.escape(label)}</b>'
            + (f'<span>{html.escape(note)}</span>' if note else "") + f'</div>{val}</li>')
def offer_stack(p):
    live = [e for e in p.get("ecosystem", []) if e.get("state") == "LIVE"]
    off = [e for e in p.get("ecosystem", []) if e.get("state") != "LIVE"]
    return f'''<article class="panel vs{" vs-featured" if p.get("featured") else ""}" id="{p["id"]}" aria-labelledby="vs-{p["id"]}">
 <header class="vs-head">{ic(p["icon"])}<div><h2 class="vs-name" id="vs-{p["id"]}">{p["name"]}</h2><p class="body mb0">{html.escape(p["summary"])}</p></div></header>
 <p class="vs-sec">Your website</p><ul class="vs-list">{"".join(vs_line(i) for i in p["includes"])}</ul>
 <p class="vs-sec">Set up with you</p><ul class="vs-list">{"".join(vs_line(e["label"], e["note"]) for e in live)}</ul>
 {f'<p class="vs-sec vs-sec-dim">Not counted: not switched on yet</p><ul class="vs-list">{"".join(vs_line(e["label"], e["note"], True) for e in off)}</ul>' if off else ""}
 <footer class="vs-foot"><div><p class="vs-price">{money(p["price"])}</p><p class="note mb0">one time · no monthly fee · no contract</p></div>
  <div class="ctas" style="margin:0">{btn(f"Pay {money(p['price'])} by card", p["pay_url"], attrs='rel="noopener"')}{btn("Ask a question first", f"/contact/?intent=services&amp;package={p['id']}", "line")}</div></footer>
</article>'''

pages["/offer/"] = ("Here's everything you get — ATH website packages",
 "Every line in the $100 Quick Start and $200 Business Growth websites, straight from ATH's price list. One price for everyone, no countdown.",
 f"""<section class="hero offer-hero" style="--pos:62% 55%;--mpos:55% 40%;min-height:auto">
 <div class="hero-art"><img src="/assets/art/build.webp" alt="" fetchpriority="high"></div>
 <div class="wrap"><div class="hero-copy">
  <p class="eyebrow">Website packages · one price for everyone</p>
  <h1 class="display d-l">Here's everything<br>you get</h1>
  <p class="lede">Two websites you can pay for by card right now. Every line below is in the package, and anything that isn't switched on yet is shown apart and not counted.</p>
  <div class="ctas">{btn("See the $200 site", "#business-growth")}{btn("See the $100 site", "#quick-start", "line")}</div>
 </div></div>
</section>
<section class="block" style="padding-top:48px"><div class="wrap">
 <div class="vs-grid">{"".join(offer_stack(p) for p in sorted([x for x in PKG if x.get("pay_url")], key=lambda x: not x.get("featured")))}</div>
 <p class="note mt2" style="text-align:center">Secure card checkout by Stripe. ATH emails your intake form after your payment. The price above is the price: no countdown and no “today only”.</p>
</div></section>
<section class="block" id="how"><div class="wrap">
 <div class="block-head"><div><p class="eyebrow">How delivery works</p><h2 class="display d-m mt1">Pay, tell us,<br>approve, go live</h2></div>{btn("See sample sites", "/sites/", "line")}</div>
 <ol class="steps">{"".join(f'<li><span class="st-n">0{n}</span><b>{t}</b><span>{d}</span></li>' for n, t, d in [
  (1, "Pay by card", "Checkout by Stripe. Nothing renews."),
  (2, "Send your details", "A short intake: your services, hours, photos and the links your buttons should open."),
  (3, "See a preview", "ATH builds your site and sends a preview link, kept out of search. Your go-live date is confirmed with you."),
  (4, "Approve your changes", "Quick Start includes one revision. Business Growth is scoped up to three pages."),
  (5, "Your own domain, when you want it", "Search engines list it once it is on your own domain (about $12 a year, paid to the registrar).")])}</ol>
</div></section>
<section class="block"><div class="wrap">
 <div class="grid" style="grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:18px;align-items:start" data-collapse>
  <div class="panel panel-pad"><p class="panel-title">What these two packages don't do</p><ul class="pkg-list">
   <li>They link to the booking or ordering tool you already use. ATH doesn't build a new one at this price.</li>
   <li>Reviews, ratings and follower counts appear only if you give them to us. Nothing is invented.</li>
   {"".join(f"<li>{html.escape(d)}</li>" for d in REG["package_disclosures"])}
  </ul></div>
  <div class="panel panel-pad"><p class="panel-title">Need more than a website?</p><ul class="rows">{ladder_rows()}</ul>
   <p class="note mt1 mb0">Each of these starts with a written scope that sets the real number. Nothing is charged before you approve it.</p></div>
 </div>
</div></section>""" + cta_block("Not sure which?", "Start with the free diagnostic. Sometimes the honest answer is that you need nothing at all."))

ECO = [
 ("ATH", "Parent builder", "live", "You're here", "The invention company. Builds, owns and routes.", ("Diagnose", "/diagnose/")),
 ("ATHOS", "Intelligence", "live", "Diagnostic live", "Diagnosis, evidence, routing. The free diagnostic on this site is ATHOS working today; deeper capabilities are in development.", ("Run it", "/diagnose/")),
 ("Passport", "Identity spine · Free", "live", "Open door", "Identity, permissions, ownership, receipts, continuity. Free, in WOW OS.", ("Get Passport", "https://thewow.online/passport/claim")),
 ("World Pass", "Membership · $20/mo", "live", "Open door", "Paid ecosystem membership on your Passport. Cancel any time.", ("Get World Pass", "https://thewow.online/passport")),
 ("Wavemotion", "Creator + Business Movement OS", "live", "Open door", "Record → prepare → launch → distribute → learn. Living Destination + Channeler.", ("Visit Wavemotion", "https://wavemotion.live/")),
 ("WM Pro", "Wealthy Mindsets Pro · from $10/mo", "", "Open door", "App $10/mo · OS $50/mo · free guest account. Third-party data/broker fees separate. No profits promised.", ("Go to WM Pro", "https://wealthymindsetspro.com")),
 ("PowerTribes", "Business · sales · workforce · leadership OS", "dim", "In development", "Specialist system — plans vary; not yet priced.", ("Request access", "/contact/?intent=powertribes")),
 ("Dreamboard", "Human-potential &amp; creative OS", "dim", "In development", "Idea → clarity → project → finished work. Specialist system — plans vary; not yet priced.", ("Request access", "/contact/?intent=dreamboard")),
 ("WOW OS", "The operating system · Guest welcome", "live", "Open door", "One home, many rooms — Lounge, Academy (Idea Library, Visual Learns, Student of the Game), Marketplace, Events, WOW TV, WOW Music, WOW Radio.", ("Enter", "https://thewow.online/")),
 ("WOW TV · WOW Radio", "Watch · Listen", "live", "Open door", "Viewer and listener destinations — separate rooms in WOW OS.", ("Enter", "https://thewow.online/wow-tv")),
 ("Lounge · Academy · Shop", "Connect · Learn · Own", "live", "Open door", "Community, learning and commerce places, entered from WOW OS.", ("Enter", "https://thewow.online/lounge")),
 ("WOW Academy", "Learn · Free to practise", "live", "Open door", "Three real tracks, open now: The Idea Library (read, question, remember, apply), Visual Learns · The Polyglot&#8217;s Mind (Spanish, Hebrew, Japanese), and Student of the Game (risk, candles, orders). A stamp is earned from proof and memory, never attendance.", ("Open the Academy", "https://thewow.online/academy")),
 ("WOW Studios", "Creation infrastructure", "dim", "Future", "Deeper production infrastructure.", None),
 ("WOW World", "The future metaverse", "dim", "Future", "A future world for the whole ecosystem. Not open and not for sale; WOW OS is the live home today.", None),
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

pages["/ecosystem/"] = ("The Ecosystem — What ATH does, who owns it, what it costs",
 "Websites, content, AI, checkout, community and business systems: one ATH ecosystem, every capability with its owner, live status and price.",
 hero("ecosystem", "", "The<br>Ecosystem",
      "ATH builds the world.<br>Destinations open the doors.<br><span style=\"font-size:.8em;color:var(--ivory-dim)\">Not an app store. Parent builder · intelligence · identity · membership · destinations.</span>",
      btn("See the full map", "#map") + btn("Here's everything you get", "/offer/", "line"), extra='<div class="plaques">' + "".join(f'<a class="plaque" href="#d"><b>{n}</b><span>{t}</span></a>' for n,t in [("WOW OS","Open door"),("WM Pro","Open door"),("WOW TV · WOW Radio","Open door"),("Lounge · Academy · Shop","Open door")]) + '</div>', pos="50% 50%", mpos="50% 40%", size="d-l")
 + '<div class="strip">One builder · Seven owners · One ecosystem</div>'
 + f"""<section class="block" id="owners"><div class="wrap">
 <div class="block-head"><div><p class="eyebrow">Who owns what</p><h2 class="display d-m mt1">Seven owners.<br>No overlap.</h2></div>
  <p class="note" style="max-width:46ch">Each capability belongs to one ATH product and the others use it, so nothing is built twice and nothing falls between two teams. There is no extra platform to learn.</p></div>
 <div class="own-grid">{"".join(f'<article class="panel panel-pad own"><div class="own-top">{ic(i)}<div><h3>{n}</h3><p class="eyebrow mb0">{r}</p></div></div><p class="own-does">{d}</p><p class="own-uses"><span>Uses</span> {u}</p></article>' for n, i, r, d, u in OWNERS)}<a class="panel panel-pad own own-cta" href="/diagnose/"><p class="eyebrow mb0">Not sure who you need?</p><h3>Start with the hill, not the org chart</h3><p class="own-does">ATHOS diagnoses first and routes you to the one owner that fits. Free.</p><span class="cap-go">What's your hill? {ARR}</span></a></div>
</div></section>
<section class="block cap-block" id="map"><div class="wrap">
 <div class="block-head"><div><p class="eyebrow">The full map</p><h2 class="display d-m mt1">What ATH does,<br>and what it costs</h2></div>
  <p class="note" style="max-width:46ch">Live now: you can use or buy it today. Included: it comes inside a package. By quote: a written scope sets the price first. In development: named, not for sale.</p></div>
 {cap_map()}
</div></section>
""" + compare_section() + f"""<section class="block" id="d"><div class="wrap">
 <div class="block-head"><div><p class="eyebrow">Destinations</p><h2 class="display d-m mt1">Every door, status plainly</h2></div><p class="note" style="max-width:46ch">Statuses reflect what is actually reachable today. Future systems are never shown as purchasable.</p></div>
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
   ("","Open door","WM Pro","Traders drown in tools that paste intelligence around a chart.","A market OS where the chart is the room and every mark respects price truth.","Open at wealthymindsetspro.com. From $10/month, free guest account.", f'<p class="mt2 mb0"><a class="btn btn-line" href="https://wealthymindsetspro.com" rel="noopener">Visit {ARR}</a></p>'),
   ("","Open door","Wavemotion","Creators and businesses lose momentum between recording and real distribution.","Record → cloud inbox → edit → variants → approval → publish → receipt → learning loop.","Plans $10 / $20 / $50 / $75 per month. Cinematic generation is not open.", f'<p class="mt2 mb0">{btn("Open Wavemotion","https://www.wavemotion.live/","line")}</p>'),
   ("dim","In development","Dreamboard","Ideas die between inspiration and a finished thing.","Idea → clarity → project → creation → finishing evidence.","In development.", ""),
   ("live","Live","Passport","Every app makes you a stranger again.","One identity spine — permissions, ownership, receipts, continuity.","Free and live in WOW OS; one Passport across ATH apps as each connects.", f'<p class="mt2 mb0"><a class="btn btn-line" href="https://thewow.online/passport/claim" rel="noopener">Get Passport {ARR}</a></p>'),
   ("","Open door","WOW OS","Products feel like islands.","A connected world of destinations under one builder.","Open at thewow.online — guests welcome, free Passport, World Pass $20/month.", f'<p class="mt2 mb0"><a class="btn btn-line" href="https://thewow.online/" rel="noopener">Enter {ARR}</a></p>')])}
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
  <li>{ic("door","icon-sm")}<div><b>Destinations</b><span>Wavemotion, WM Pro, PowerTribes, Dreamboard, WOW OS and more — each owns its own experience.</span></div></li></ul></div>
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
    <option value="wavemotion">WAVEMOTION</option>
    <option value="worldpass">World Pass — questions ($20/mo, live now)</option>
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
  <input type="hidden" name="package" id="l-package" value="">
  <input type="hidden" name="catalog_version" id="l-catalog" value="">
  <div class="pkg-note" id="pkg-note" hidden></div>
  <label class="check pkg-ack" id="pkg-ack" hidden><input type="checkbox" id="l-ack" name="terms_ack" value="yes"> <span>I understand ATH will send a written scope and an invoice. Nothing is charged now, and work starts only after I approve the scope and pay.</span></label>
  <input type="text" name="company_fax" tabindex="-1" autocomplete="off" class="vh" aria-hidden="true">
  <button class="btn btn-gold" type="submit">Send to ATH {ARR}</button>
  <p class="note mt1">We use this only to reply to you. See <a class="gold" href="/privacy/">Privacy</a>.</p>
  <p class="form-status" role="status" aria-live="polite"></p>
 </form>
</div></section>""" + catalog_js())

pages["/free-look/"] = ("Free website look — Above the Hill",
 "Tell us about your business. ATH sends a free look at what your website could be, and what it costs.",
 f"""<section class="block" style="padding-top:56px"><div class="wrap split" style="align-items:start">
 <div><p class="eyebrow">Free · no obligation</p><h1 class="display d-l mt1">See your business<br>online, free</h1>
  <p class="lede">Leave your name and number. A person at ATH looks at how customers find you today and sends you a free look at your new site.</p>
  <ul class="pkg-list mt2"><li>Websites from <b>$100 one time</b>, go-live date confirmed when your form arrives</li><li>Up to 3 pages, linked to the booking or ordering you already use: <b>$200</b></li><li>Site + 2 promo videos: <b>$500–$700</b></li><li>Weekly videos made for you: <b>$500/month</b></li></ul>
  <p class="body mt2">See real examples: <a class="gold" href="/sites/">sample sites ATH built</a>.</p></div>
 <form class="panel panel-pad" id="lead-form" novalidate>
  <input type="hidden" name="intent" value="free-look">
  <div class="grid g2"><div class="field"><label class="lbl" for="f-name">Your name</label><input id="f-name" name="name" type="text" autocomplete="name" required></div>
   <div class="field"><label class="lbl" for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" maxlength="40"></div></div>
  <div class="field"><label class="lbl" for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
  <div class="grid g2"><div class="field"><label class="lbl" for="f-org">Business name and city</label><input id="f-org" name="org" type="text" autocomplete="organization"></div>
   <div class="field"><label class="lbl" for="f-site">Your current site or social page <span class="mute">(optional)</span></label><input id="f-site" name="website" type="url" inputmode="url"></div></div>
  <div class="field"><label class="lbl" for="f-want">What do you want most?</label>
   <select id="f-want" name="interest"><option>A website customers can find</option><option>Bookings or online orders</option><option>Promo videos for my business</option><option>Weekly videos and posting done for me</option><option>Not sure, show me</option></select></div>
  <p class="lbl" style="margin-top:6px">Pick a time for a quick call <span class="mute">(10 minutes, optional)</span></p>
  <div class="grid g2"><div class="field"><label class="lbl" for="f-day">Day</label><input id="f-day" name="call_date" type="date"></div>
   <div class="field"><label class="lbl" for="f-time">Time</label><select id="f-time" name="call_time"><option value="">Any time</option><option>9:00 AM</option><option>9:30 AM</option><option>10:00 AM</option><option>10:30 AM</option><option>11:00 AM</option><option>11:30 AM</option><option>12:00 PM</option><option>12:30 PM</option><option>1:00 PM</option><option>1:30 PM</option><option>2:00 PM</option><option>2:30 PM</option><option>3:00 PM</option><option>3:30 PM</option><option>4:00 PM</option><option>4:30 PM</option><option>5:00 PM</option><option>5:30 PM</option><option>6:00 PM</option><option>6:30 PM</option></select></div></div>
  <input type="hidden" name="tz" id="f-tz" value="">
  <script>try{{document.getElementById("f-tz").value=Intl.DateTimeFormat().resolvedOptions().timeZone;var d=new Date();document.getElementById("f-day").min=d.toISOString().slice(0,10);}}catch(e){{}}</script>
  <input type="hidden" name="package" id="l-package" value="">
  <input type="hidden" name="catalog_version" id="l-catalog" value="">
  <div class="pkg-note" id="pkg-note" hidden></div>
  <input type="text" name="company_fax" tabindex="-1" autocomplete="off" class="vh" aria-hidden="true">
  <button class="btn btn-gold" type="submit">Get my free look {ARR}</button>
  <p class="note mt1">Nothing is charged. We use this only to reply to you about your business. Reply STOP to any text and we won't contact you again. See <a class="gold" href="/privacy/">Privacy</a>.</p>
  <p class="form-status" role="status" aria-live="polite"></p>
 </form>
</div></section>""" + catalog_js())

# ---------------------------------------------------------------- holiday gift guide (live ATH Store feed snapshot)
def gift_guide():
    here = os.path.dirname(os.path.abspath(__file__))
    try: feed = json.load(open(os.path.join(here, "commercial", "ath-store-snapshot.json")))
    except Exception: return None
    # Products with a known store-page problem stay off the guide until it is fixed (commercial/gift-holds.json).
    try: held = {str(h["id"]) for h in json.load(open(os.path.join(here, "commercial", "gift-holds.json")))["holds"]}
    except FileNotFoundError: held = set()
    groups = [("For creators who film", ("microphone","mic","light","tripod","gimbal","selfie","backdrop","grip","foam","interface","boom","ring")),
              ("Desk, journal and reset", ("journal","notebook","laptop","glasses","charger","charging","wallet","frother","tumbler")),
              ("Home and host", ("candle","pillowcase","lamp")),
              ("Wellness picks", ("massage","posture","resistance"))]
    used, out = set(), []
    for name, keys in groups:
        items = [p for p in feed.get("products", []) if p.get("available") and p["id"] not in used and p["id"] not in held and any(k in p["title"].lower() for k in keys)]
        for p in items: used.add(p["id"])
        if items: out.append((name, sorted(items, key=lambda p: p.get("price_from") or 0)))
    cards = lambda items: "".join(f'<a class="gift" href="{html.escape(p["product_url"])}" rel="noopener"><img src="{html.escape(p["image"])}&width=480" alt="" loading="lazy" width="240" height="240"><span class="gift-t">{html.escape(p["title"])}</span><span class="gift-p">${p["price_from"]:,.2f}{"+" if p.get("multiple_prices") else ""}</span></a>' for p in items)
    secs = "".join(f'<section class="block" style="padding-top:28px"><div class="wrap"><h2 class="display d-m">{n}</h2><div class="gift-grid mt2">{cards(i)}</div></div></section>' for n, i in out)
    return secs, feed.get("as_of", "")[:10]

_g = gift_guide()
if _g:
    pages["/gifts/"] = ("Holiday gift guide — Above the Hill",
     "Holiday gifts from the ATH Store: creator gear, journals, home and wellness picks, plus gifts for business owners.",
     f"""<section class="block" style="padding-top:56px"><div class="wrap"><p class="eyebrow">Holiday 2026 · ATH Store</p><h1 class="display d-l mt1">Gifts for the<br>builders you love</h1>
  <p class="lede">Real products from the ATH Store, checkout by Shopify. Prices shown are from {_g[1]}; your cart shows the current price and shipping before you pay. Order early: shipping times vary by item.</p>
  <div class="ctas mt2">{btn("Browse all in WOW Marketplace", "https://thewow.online/marketplace")}{btn("Gift a business a website", "/free-look/", "line")}</div></div></section>""" + _g[0] + f"""
<section class="block"><div class="wrap"><div class="panel panel-pad"><p class="eyebrow">For the business owner on your list</p><h2 class="display d-m mt1">Get them found before the holiday rush</h2>
  <p class="body">A mobile website for their business, <b>$100 one time</b>. Up to 3 pages, linked to the booking or ordering they already use, is $200 and comes with a free month of World Pass. Order early for the holidays: ATH confirms the go-live date when their info arrives.</p>
  <div class="ctas mt1">{btn("Get a free look", "/free-look/")}{btn("See sample sites", "/sites/", "line")}</div></div></div></section>""")

pages["/start/"] = ("Start your build — ATH intake",
 "Tell ATH about your business so we can start building.",
 f"""<section class="block" style="padding-top:56px"><div class="wrap split" style="align-items:start">
 <div><p class="eyebrow">Payment received · Next step</p><h1 class="display d-l mt1">Let's build<br>your site</h1>
  <p class="lede">Thank you. Tell us about your business and ATH starts the build.</p>
  <p class="body mt2">Share links to your logo and photos (Google Drive, Dropbox, Instagram or your current site). A person at ATH reads every intake and replies.</p>
  <p class="note mt2">Didn't pay yet? <a class="gold" href="/build/#pricing">See packages</a>.</p></div>
 <form class="panel panel-pad" id="intake-form" novalidate>
  <input type="hidden" name="intent" value="paid-intake">
  <div class="grid g2"><div class="field"><label class="lbl" for="i-name">Your name</label><input id="i-name" name="name" type="text" autocomplete="name" required></div>
   <div class="field"><label class="lbl" for="i-email">Email used at checkout</label><input id="i-email" name="email" type="email" autocomplete="email" required></div></div>
  <div class="grid g2"><div class="field"><label class="lbl" for="i-org">Business name</label><input id="i-org" name="org" type="text" autocomplete="organization"></div>
   <div class="field"><label class="lbl" for="i-site">Current website or social page <span class="mute">(optional)</span></label><input id="i-site" name="website" type="url" inputmode="url"></div></div>
  <div class="field"><label class="lbl" for="i-msg">Your services, hours, contact info, photo/logo links, and anything else the site should say</label><textarea id="i-msg" name="message" maxlength="3000" required></textarea></div>
  <input type="hidden" name="package" id="l-package" value="">
  <input type="hidden" name="catalog_version" id="l-catalog" value="">
  <div class="pkg-note" id="pkg-note" hidden></div>
  <input type="text" name="company_fax" tabindex="-1" autocomplete="off" class="vh" aria-hidden="true">
  <button class="btn btn-gold" type="submit">Send intake to ATH {ARR}</button>
  <p class="note mt1">Used only to build your site. See <a class="gold" href="/privacy/">Privacy</a>.</p>
  <p class="form-status" role="status" aria-live="polite"></p>
 </form>
</div></section>""" + catalog_js())

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
<p>Effective October 7, 2026; packages section added October 13, 2026. These terms cover use of abovethehilldev.online, operated by Above the Hill Developments Inc. ("ATH").</p>
<h2>The free diagnostic</h2><p>ATHOS reports what it observed on one public page, what it infers from that, and what it cannot know. It is informational, not a guarantee of results. Where evidence is missing, the result says "unknown".</p>
<h2>Ownership</h2><ul>
<li>You own your materials. A diagnostic or deep diagnostic transfers no ownership of your code, content or data to ATH.</li>
<li>ATH owns ATH intellectual property — including ATHOS, its methods, the ATH Builder Dictionary, product designs and inventions. Purchasing the Dictionary or any product licenses its use; it does not transfer ownership of ATH inventions.</li></ul>
<h2>Deep diagnostics and services</h2><p>Deeper inspection happens only under a written scope you approve, with access you grant and may revoke. Default posture is read-only; ATH does not modify your systems during a diagnostic. Services are delivered under a separate scope and quote.</p>
<h2>Website and app packages</h2><p>Package prices are listed on the <a class="gold" href="/build/#pricing">Build page</a>. Submitting a package request creates no charge and no obligation. ATH replies with a written scope and an invoice; work begins only after you approve the scope and pay. Timeline, revisions, ownership terms, third-party costs and refund terms are stated in that written scope. Ecosystem extras described as “not active yet” are delivered only once that product is operational, and no subscription renews without your separate consent.</p>
<h2>Prices and availability</h2><p>Only products marked available can be bought. Waitlists and access requests create no obligation for either side. Membership (World Pass) does not include specialist products, ATH services or third-party costs unless stated in writing.</p>
<h2>Contact</h2><p>Questions: use the <a class="gold" href="/contact/">contact form</a>.</p>
</div></section>""")

pages["/404/"] = ("This path doesn't exist yet — ATH", "Page not found.",
 hero("path", "404", "This path doesn't<br>exist yet", "But the way over is still here.",
      btn("What's your hill?", "/diagnose/") + btn("Home", "/", "line"), size="d-m"))

# ---------------------------------------------------------------- city pages: be findable for owners already searching (Myron: make yourself findable)
QS_LINK, BG_LINK = "https://buy.stripe.com/3cI4gA1KkdPkbvJ2oG97G00", "https://buy.stripe.com/eVq4gAcoY4eKarF1kC97G01"
CITIES = [("tulsa", "Tulsa"), ("broken-arrow", "Broken Arrow"), ("bixby", "Bixby")]
NICHES = [
 ("barbers-salons", "barbers and salons", "Your chair stays full", "Clients find your hours, see your work and tap Book, even at 10 pm when the shop is closed.", "A Book button to Booksy, Square, Vagaro or StyleSeat, your price list and a photo gallery"),
 ("restaurants-food-trucks", "restaurants and food trucks", "Hungry people find you first", "Your menu, hours and a call or order button on one page you own, not someone else's.", "Menu, hours, where the truck is today, and a call button or a link to the ordering you already use"),
 ("bakeries", "bakeries", "Holiday orders come to you", "Customers see your cakes, prices and how to order without messaging you on Facebook.", "A photo menu, your pickup hours and a text-or-call button for orders"),
 ("auto-repair", "auto repair shops", "The phone rings with real jobs", "Drivers searching for help at the roadside find your number, services and hours in one tap.", "Services, hours, both locations, tap-to-call and directions"),
 ("cleaning-lawn-care", "cleaning and lawn care", "Quotes come in while you work", "Homeowners see what you do and send a quote request instead of scrolling past.", "Services, service area, before-and-after photos and a text-or-email button for quotes"),
 ("small-business", "small businesses", "Customers find you, trust you and call", "A real site with your services, hours and photos, so the people already looking can pick you.", "Services, hours, photos and tap-to-call"),
]
def city_page(cslug, city, n):
    nslug, who, payoff, line, gets = n
    others = "".join(f'<li><a class="gold" href="/websites/{cslug}/{o[0]}/">Websites for {o[1]} in {city}</a></li>' for o in NICHES if o[0] != nslug)
    return (f"Websites for {who} in {city}, OK — from $100 | Above the Hill",
     f"{payoff}. A mobile website for {who} in {city}, Oklahoma: $100 one time, go-live date confirmed with you. Local team, no contract.",
     f"""<section class="block" style="padding-top:56px"><div class="wrap split" style="align-items:start">
 <div><p class="eyebrow">{city}, Oklahoma · local team</p><h1 class="display d-l mt1">{payoff}.</h1>
  <p class="lede">{line}</p>
  <ul class="pkg-list mt2"><li><b>What you get:</b> {gets}</li><li><b>How soon:</b> a 5-minute form, then ATH confirms your go-live date</li><li><b>Price:</b> $100 one time, no contract, no monthly fee. Up to 3 pages, linked to the booking or ordering you already use: $200</li></ul>
  <div class="ctas mt2">{btn("Start for $100", QS_LINK)}{btn("Get the $200 site", BG_LINK, "line")}</div>
  <p class="body mt2">Not ready? <a class="gold" href="/free-look/">Get a free look</a> at what your site could be, or <a class="gold" href="/sites/">open the sample sites</a> on your phone.</p></div>
 <div class="panel panel-pad"><p class="eyebrow">Why it works</p><h2 class="display d-m mt1">People are already searching</h2>
  <p class="body">Before they call, customers in {city} Google you to check your hours, prices and reviews. If all they find is a social page, they find less than you offer. A real site gives the people already looking something better to find. Search engines list it once it is on your own domain (about $12 a year, paid to the registrar).</p>
  <h3 class="mt2">What you stop doing</h3><p class="body">Answering "what are your hours?" in DMs, and losing customers who can't find you at night.</p>
  <h3 class="mt2">More in {city}</h3><ul class="pkg-list">{others}</ul></div>
</div></section>""")
for cslug, city in CITIES:
    for n in NICHES: pages[f"/websites/{cslug}/{n[0]}/"] = city_page(cslug, city, n)
pages["/websites/"] = ("Websites for local businesses in Tulsa, Broken Arrow and Bixby | Above the Hill",
 "Websites from $100 for barbers, salons, restaurants, bakeries, auto shops, cleaners and small businesses in Tulsa, Broken Arrow and Bixby, Oklahoma.",
 f"""<section class="block" style="padding-top:56px"><div class="wrap"><p class="eyebrow">Local · Tulsa area</p><h1 class="display d-l mt1">A website for the customers<br>already looking for you</h1>
 <p class="lede">$100 one time, go-live date confirmed with you. Pick your town and your kind of business.</p>
 <div class="grid g3 mt2">""" + "".join(f'<div class="panel panel-pad"><h2 class="display d-m">{city}</h2><ul class="pkg-list">' + "".join(f'<li><a class="gold" href="/websites/{cslug}/{n[0]}/">{n[1].capitalize()}</a></li>' for n in NICHES) + "</ul></div>" for cslug, city in CITIES) + f"""</div>
 <div class="ctas mt2">{btn("Start for $100", QS_LINK)}{btn("Get a free look", "/free-look/", "line")}</div></div></section>""")

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
    # master catalog (registry "catalog"): every ATH offer with an honest status, for Spaidbot and partners
    open(os.path.join(ROOT, "catalog.json"), "w").write(json.dumps({"version": REG["version"], "statuses": {"LIVE": "can be bought now", "SCOPED": "sold through a written quote", "NOT_ACTIVE": "named but not deliverable yet", "PROPOSED": "a plan, not for sale", "LIVE_IN_WM_PRO": "available inside WM Pro", "RETIRED": "no longer sold; orders already placed are honored"}, "offers": REG.get("catalog", [])}, indent=1, ensure_ascii=False))
    open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    urls = "".join(f"<url><loc>{SITE}{r}</loc></url>" for r in pages if r != "/404/")
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    print("wrote", len(pages), "pages")

if __name__ == "__main__":
    write()

if __name__ == "__main__":
    # Website factory: client and sample sites from sites/clients/*.json (see sites/DELIVERY.md)
    import runpy
    runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sites", "build_sites.py"), run_name="__main__")
