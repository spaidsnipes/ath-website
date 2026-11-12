#!/usr/bin/env python3
"""ATH Official Website — static page generator.

Canon: Visual Canon Atlas v1, slide athWebsiteCanonPass3 (Founder finder doc 2026-10-07).
Prices: commercial/registry.json (v2026-11-07.1, Founder price matrix ATH-PRICE-MATRIX-1107) — see commercial/RECONCILIATION-2026-10-13.md for history.
Lineage: one ecosystem ladder (Founder 2026-10-24): Free (Passport) · Basic $10 (one app's essentials) · Premium $20 · app plans $19+. The $20 World Pass = Premium of the app you choose + Basic of every other ATH app. WM Pro: Free / Basic $10 / Premium $20 / Auto-trading $30; Spaidbot Personal $19 / Builder $49 / Operations $99; WOW Studios $29/$59/$119; PowerTribes launch $29/$79/$179; Creator Passport $40/$75/$100/$150;
Services show Founder-approved starting prices; WAVEMOTION clips come with its $10/$20/$50 plans (the separate clip-bundle menu was retired by the Founder on 2026-10-22). Nothing on this
site is sold through a fake checkout; unavailable things say Join waitlist / Request access / Get quote.
Run: python3 build.py  -> writes public/<route>/index.html
"""
import os, html, re, datetime

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
SITE = "https://abovethehilldev.online"
API = "https://mission.abovethehilldev.online"  # canonical domain of the ath-athos Worker (same service; no workers.dev on guest pages)
# Spaidbot: the one ATHOS embed (public mode). data-greet="1" = the proactive website greeter (free leak audit /
# pricing / talk to a person), once per session, AI-labelled, no tracking. See athos-brain spaidbot-embed.mjs.
SPAIDBOT_EMBED = "https://mission.abovethehilldev.online/spaidbot.js"

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
        "gauge": '<path d="M4 18a8 8 0 1 1 16 0"/><path d="m12 18 4-6"/><path d="M7 21h10"/>',
        "lock": '<rect x="4" y="10" width="16" height="11" rx="1.5"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
    }[name]
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>'

ARR = '<span class="arr" aria-hidden="true">→</span>'
FONTS = "https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600&family=Cormorant+Garamond:wght@400;500&family=Inter:wght@400;500;600&display=swap"
HERO_ART = {"/": "home", "/diagnose/": "diagnose", "/path/": "path", "/passport/": "passport", "/build/": "build", "/ecosystem/": "ecosystem", "/language/": "path", "/diagnose/deep/": "deep", "/work/": "path", "/company/": "home", "/404/": "path", "/pricing/": "build"}
NAV = [("Company", "/company/"), ("Inventions", "/work/"), ("Services", "/build/"), ("Prices", "/pricing/"), ("AI", "/ai/"),
       ("Diagnose", "/diagnose/"), ("Language", "/language/"), ("Ecosystem", "/ecosystem/")]

# Utility pages a guest should never land on from search (post-payment intake, empty result shell, 404).
NOINDEX = {"/start/", "/diagnose/result/", "/404/"}

def head(title, desc, route):
    art = HERO_ART.get(route)
    robots = '<meta name="robots" content="noindex">' if route in NOINDEX else ""
    preload = f'<link rel="preload" as="image" href="/assets/art/{art}.webp" fetchpriority="high">' if art else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{SITE}{route}">{robots}
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
<script src="{SPAIDBOT_EMBED}" data-api="{API}" data-product="ath" data-greet="1" data-compact-hero="1" data-audit-href="/business-diagnosis/" defer></script>
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
   <div><p class="fh">Start</p><a href="/diagnose/">What's your hill?</a><a href="/diagnose/deep/">Deep diagnostic</a><a href="/build/">ATH Services</a><a href="/pricing/">Prices</a><a href="/ai/">AI services</a><a href="/ai/growing-with-ai/">Growing with AI</a><a href="/garden-check/">Garden Check</a><a href="/industries/">Industries</a><a href="/consequence-calculator/">Consequence Calculator</a><a href="/business-diagnosis/">Free business diagnosis</a><a href="/contact/">Contact ATH</a><a href="tel:+19189600164" aria-label="Call or text ATH at (918) 960-0164">Call or text (918) 960-0164</a></div>
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
    ("free", "Free", "Free Passport", "Your free Passport · the Lounge · WOW Music, WOW Radio &amp; WOW TV · WOW Academy's free lessons", "", "/passport/#ladder"),
    ("door", "$10 / mo", "Basic", "One app's essentials, per app · WAVEMOTION Starter · WM Pro Basic", "", "/passport/#ladder"),
    ("lattice", "$20 / mo", "World Pass", "Premium of the app you choose + Basic of every other ATH app, WOW OS, Academy and every new app", "Best value", "/passport/#world-pass-value"),
    ("triangle", "$19–$179 / mo", "App plans", "WM Pro Auto-trading $30 · WAVEMOTION Pro $50 · Spaidbot from $19 · WOW Studios from $29 · PowerTribes from $29 · Creator Passport from $40", "", "/ecosystem/#plans"),
    ("peaks", "$100–$8,000 / mo", "ATH plans", "One ladder for your business: a piece of everything ATH makes, more of it at every step", "", "/pricing/"),
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
# Mansion Garden Check (Founder order 2026-10-24): one-time live website check. Its price is ONE number,
# registry garden_check.price; every page and the catalog entry Spaidbot reads are generated from it.
# garden_check.payment_link empty -> "Book a Garden Check" (a booking request, nothing charged);
# a Stripe Payment Link pasted there -> card checkout, and the catalog marks it LIVE.
GC = REG["garden_check"]
GC_PAY = (GC.get("payment_link") or "").strip()
assert not GC_PAY or re.match(r"^https://buy\.stripe\.com/[A-Za-z0-9_]+$", GC_PAY), "garden_check.payment_link must be a Stripe Payment Link (https://buy.stripe.com/...)"
GC_PRICE = f'${GC["price"]:,}'
GC_PAGE = "/garden-check/"
GC_CTA = f"Pay {GC_PRICE} by card" if GC_PAY else "Book a Garden Check"
GC_HREF = GC_PAY or GC_PAGE + "#book"
GC_CAT = {"id": GC["catalog_id"], "business": "ATH Developments", "name": f'{GC["name"]} (website health check)', "price": f"{GC_PRICE} one time",
          "status": "LIVE" if GC_PAY else "BOOKABLE", "buy": GC_PAY or SITE + GC_PAGE,
          "fulfillment": f'A {GC["minutes"]} minute live check of the client\'s website on Zoom or Google Meet that the client watches: links, speed, mobile, SSL and security, forms, booking and checkout buttons, Google listing, search basics and broken pages, then a plain list of what needs fixing and what does not. Passwords are never asked for. Fixes are quoted separately. Monthly upkeep is the Mansion Garden Pass, included with Passport Pro.',
          "verified": GC["verified"]}
OFFERS = list(REG["catalog"])
OFFERS.insert(next(i for i, o in enumerate(OFFERS) if o["id"] == "ath-business-growth") + 1, GC_CAT)
CAT = {o["id"]: o for o in OFFERS}
def cat_price(oid):
    o = CAT[oid]
    assert o["status"] in ("LIVE", "SCOPED", "BOOKABLE"), f"{oid} is {o['status']}: not for sale, so it is not shown as a price"
    return o["price"]
# Homepage "Start with what you do": one door per kind of visitor, each with its real price and next step.
# Prices come from the commercial registry above, never typed here; WM Pro shows only its free guest account
# until a paid checkout is proven (Founder ship order, 2026-10-21).
OUTCOMES = [
 ("site", "You run a local business", "Presence", "Your website, missed-call text-back, the appointment setter, a PowerTribes office and a WOW Pass. Step one of one ladder.", lambda: f'${PLANS[0]["monthly"]:,} a month', "See every plan", "/pricing/"),
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
# HOLIDAY SPECIAL (Founder ruling 2026-10-25): WAVEMOTION Creator (Premium, $20) first month $10, half off, through
# Dec 25 2026 11:59 PM CT. WAVEMOTION charges it (WOW one-time coupon HOLIDAY50). Date-gated twice: a build after the
# deadline leaves it out, and assets/ath.js removes any [data-offer-ends] element once the deadline passes.
HOLIDAY_ENDS = "2026-12-26T05:59:59Z"
HOLIDAY_LINE = "Holiday special: your first month of WAVEMOTION Creator (Premium, $20) is $10, half off, when you subscribe by December 25, 2026, 11:59 PM CT. Then $20/month until you cancel."
HOLIDAY_OPEN = False  # Founder 2026-10-30: no free months, no discounts; WAVEMOTION switched the special off (3974e98).
def holiday_note(now=None):
    if not HOLIDAY_OPEN: return ""
    now = now or datetime.datetime.now(datetime.timezone.utc)
    if now > datetime.datetime(2026, 12, 26, 5, 59, 59, tzinfo=datetime.timezone.utc): return ""
    return f'<p class="body holiday-note" data-offer-ends="{HOLIDAY_ENDS}"><b>{html.escape(HOLIDAY_LINE)}</b></p>'
def wm_rows():
    return "".join(f'<div class="pt-row" role="row"><span role="cell"><b>{html.escape(p["name"])}</b></span><span role="cell" class="pt-price">${p["price"]}/mo</span><span role="cell" class="pt-allowance">{p["clips"]} standard clips / month</span><span role="cell"><a class="btn btn-line btn-sm" href="https://www.wavemotion.live/#pricing" rel="noopener" aria-label="View WAVEMOTION {html.escape(p["name"])} plan">View plans</a></span></div>' for p in WM["plans"])
def catalog_js():
    m = {}
    for p in PKG:
        m[p["id"]] = {"label": f'{p["name"]} — {"from " if p["from"] else ""}{money(p["price"])}{(" + " + money(p["setup"]) + " setup") if p.get("setup") else ""}{"" if p["from"] else " one time"}', "terms": True}
    for t, p, s, i in STARTS: m[s] = {"label": f"{t} — from ${p}"}
    for p in WM["plans"]: m[p["id"]] = {"label": f'WAVEMOTION {p["name"]} — ${p["price"]}/month ({p["clips"]} standard clips)'}
    for p in PLANS: m["plan-" + p["key"].replace("_", "-")] = {"label": f'{p["name"]} plan — ${p["setup"]:,} setup today, then ${p["monthly"]:,} a month starting 30 days later', "terms": True}
    for g in SERVICES:
        for i in g["items"]:
            if i["id"] not in m and i["id"] not in ("garden-check", "business-diagnosis"): m[i["id"]] = {"label": f'{i["name"]} — {i["price"]}', "terms": True}
    m["custom"] = {"label": "Custom OS / app / platform — diagnose → scope → quote"}
    m[GC["id"]] = {"label": f'{GC["name"]} — {GC_PRICE} one time ({GC["minutes"]} minute live website check)',
                   "note": {"ask": "ATH replies with a time for your live check. Nothing is charged now, and we never ask for passwords.",
                            "paid": "Thank you for booking. ATH replies with your call time and a Zoom or Google Meet link."},
                   "start": {"title": "Let's book your<br>Garden Check", "lede": "Thank you. Send your website address and a few times that work, and ATH sets up your live check.",
                             "body": GC["privacy"], "msg": "Your website address, and two or three times that work for a " + GC["minutes"] + " minute video call (say Zoom or Google Meet)"}}
    data = {"version": REG["version"], "payment": REG["payment"]["state"], "packages": m, "disclosures": REG["package_disclosures"]}
    return '<script type="application/json" id="ath-catalog">' + json.dumps(data).replace("</", "<\\/") + "</script>"

# ---------------------------------------------------------------- THE ATH price book (Founder direction 2026-10-31)
# ONE ladder, $100 → $8,000 a month, 15 steps, no duplicate names, no duplicate prices. Every step has a piece of
# everything ATH makes (WOW Pass, PowerTribes office, WAVEMOTION, Spaidbot, WM Pro, AI receptionist + text-back,
# review requests, a website, seats and locations), more of each at every step ("the more you get, the better").
# Standalone services live in their own list, never mixed into the ladder. Source of every number below:
# commercial/price-book.json (= ~/ath-canon-live/ATH-PRICE-BOOK-2026-10-31.md). No trials, no free months, no discounts.
# Checkout: a step or service shows card checkout ONLY when its pay_url is a Stripe Payment Link; otherwise "Book a call".
PB = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "commercial", "price-book.json")))
PLANS = PB["steps"]
SERVICES = PB["services"]
STRIPE_RE = r"^https://buy\.stripe\.com/[A-Za-z0-9_]+$"
assert len({p["name"] for p in PLANS}) == len(PLANS) and len({p["monthly"] for p in PLANS}) == len(PLANS), "one name and one price per step"
for p in PLANS: assert not p["pay_url"] or re.match(STRIPE_RE, p["pay_url"]), p["key"]
def plan_href(p): return p["pay_url"] or f'/contact/?intent=services&amp;package=plan-{p["key"].replace("_", "-")}'
def plan_cta(p, kind="gold"):
    if p["pay_url"]: return btn(f'Start {html.escape(p["name"])}', p["pay_url"], kind, 'rel="noopener"')
    return btn("Book a call", plan_href(p), kind, f'aria-label="Book a call about {html.escape(p["name"])}"')
PLAN_ROWS = [  # (label, value) — the same rows on every card, so any two steps compare line by line
    ("WOW Pass", lambda p: p["wow_pass"]),
    ("PowerTribes office", lambda p: p["office"]),
    ("WAVEMOTION", lambda p: f'{p["wavemotion"]} · {p["wavemotion_clips"]:,} clips a month'),
    ("Spaidbot", lambda p: f'{p["spaidbot"]} · {p["spaid_daily"]:,} business answers a day'),
    ("WM Pro", lambda p: p["wm_pro"]),
    ("AI receptionist + text-back", lambda p: f'{p["receptionist_minutes"]:,} receptionist minutes · {p["texts"]:,} texts a month'),
    ("Reviews", lambda p: f'{p["review_requests"]:,} review requests a month'),
    ("Website", lambda p: p["website"]),
    ("Seats & locations", lambda p: f'{p["seats"]:,} {"seat" if p["seats"] == 1 else "seats"} · {p["locations"]} {"location" if p["locations"] == 1 else "locations"} · {p["lines"]} phone {"line" if p["lines"] == 1 else "lines"}'),
]
EVERY_PLAN = [("lattice", "WOW Pass"), ("flow", "PowerTribes office"), ("content", "WAVEMOTION"), ("ai", "Spaidbot"), ("chart", "WM Pro"),
              ("bolt", "AI receptionist + text-back"), ("eye", "Review requests"), ("site", "Website"), ("me", "Seats & locations")]
def plan_strip():
    """The staircase: every step, lowest to highest, each linking to its card on /pricing/."""
    steps = "".join(f'<a class="pb-step" href="/pricing/#plan-{p["key"]}" style="--h:{i}"><span class="pb-price">${p["monthly"]:,}</span><span class="pb-name">{html.escape(p["name"])}</span></a>' for i, p in enumerate(PLANS))
    return f'<nav class="pb-strip" aria-label="ATH plans, $100 to $8,000 a month, lowest to highest">{steps}</nav>'
def plan_card(p):
    rows = "".join(f'<div class="pc-row"><dt>{html.escape(l)}</dt><dd>{html.escape(f(p))}</dd></div>' for l, f in PLAN_ROWS)
    setup = f'${p["setup"]:,} setup today · your ${p["monthly"]:,} a month starts 30 days later'
    return f'''<article class="panel pc{" pc-feature" if p["key"] in ("presence", "clientflow", "revenue_engine") else ""}" id="plan-{p["key"]}" data-plan="{p["key"]}" aria-labelledby="pc-{p["key"]}">
 <header class="pc-head"><p class="pc-step">Step {p["rank"]} of {len(PLANS)}</p><h3 class="pc-name" id="pc-{p["key"]}">{html.escape(p["name"])}</h3>
  <p class="pc-price">${p["monthly"]:,}<span> a month</span></p><p class="pc-setup">{setup}</p></header>
 <p class="pc-new"><b>{"Starts with" if p["rank"] == 1 else "Adds"}:</b> {html.escape(p["unlocks"])}</p>
 <dl class="pc-list">{rows}</dl>
 <div class="ctas pc-cta">{plan_cta(p)}</div>
</article>'''
def plan_cards(): return '<div class="pc-grid">' + "".join(plan_card(p) for p in PLANS) + '</div>'
def plan_table(pid="pricing"):
    """Compact ladder (industry + calculator pages): name · price · setup · what this step adds."""
    rows = "".join(f'<div class="rv-row" data-level="{html.escape(p["name"])}"><span><b>{html.escape(p["name"])}</b><span class="note">{html.escape(p["unlocks"])}</span></span><span class="rv-price">${p["monthly"]:,} / month<span class="note">${p["setup"]:,} setup today · monthly starts in 30 days</span></span></div>' for p in PLANS)
    fine = "".join(f"<li>{html.escape(f)}</li>" for f in PB["fine"][:3])
    return f'''<div class="panel panel-pad mt2" id="{pid}" data-sb-pricing><p class="panel-title">ATH plans · one ladder, $100 to $8,000 a month</p>
 <p class="body">Every plan has a piece of everything: a WOW Pass (WOW = World of Wealth), a PowerTribes office, WAVEMOTION, Spaidbot, WM Pro, AI receptionist minutes and text-back, review requests and a website. Each step up gives you more of all of it. <a class="gold" href="/pricing/">See exactly what each step includes</a>.</p>
 <div class="rv-table">{rows}</div>
 <ul class="pkg-list mt2 rv-fine">{fine}</ul></div>'''
def svc_href(i):
    if i.get("pay_url"): return i["pay_url"]
    if i.get("href"): return i["href"]
    return f'/contact/?intent=services&amp;package={i["id"]}'
def svc_cta(i):
    if i.get("pay_url") and i.get("live_checkout"): return ("Subscribe", i["pay_url"])
    if i.get("pay_url") and re.match(STRIPE_RE, i["pay_url"]): return ("Pay by card", i["pay_url"])
    if i.get("cta"): return (i["cta"], i["href"])
    if i.get("pay_url"): return ("See plans", i["pay_url"])
    return ("Book a call", svc_href(i))
def services_list(groups=None, head=True):
    """Standalone services: bought on their own, separate from the plans."""
    out = []
    for g in SERVICES:
        if groups and g["group"] not in groups: continue
        rows = []
        for i in g["items"]:
            lab, href = (GC_CTA, GC_HREF) if i["id"] == "garden-check" else svc_cta(i)
            price = f'{GC_PRICE} one time' if i["id"] == "garden-check" else i["price"]
            ext = href.startswith("http")
            rows.append(f'<div class="sv-row" data-svc="{i["id"]}"><div class="sv-what"><b>{html.escape(i["name"])}</b><span class="note">{html.escape(i["what"])}</span></div>'
                        f'<p class="sv-price">{html.escape(price)}</p><a class="btn btn-line btn-sm sv-go" href="{href}"{" rel=\"noopener\"" if ext else ""}>{lab} {ARR}</a></div>')
        out.append(f'<section class="sv-group" aria-label="{html.escape(g["group"])}"><p class="eyebrow sv-g">{html.escape(g["group"])}</p>{"".join(rows)}</section>')
    title = '<p class="panel-title">Services on their own · not part of a plan</p>' if head else ""
    return f'<div class="panel panel-pad sv" id="services">{title}{"".join(out)}</div>'

# World Pass rule (Founder 2026-10-23, corrected 2026-10-24). One ecosystem ladder with real tier names:
# Free (Passport) · Basic $10 (one app's essentials) · Premium $20 · app plans $19+. The $20 World Pass is THE ecosystem
# pass (that is why it is a passport): Premium of the one app you choose + Basic of every other ATH app, WOW OS,
# WOW Academy, Dreamboard and every future app, and WOW World (the future metaverse) when it opens.
# Never "$10 tier" / "$20 tier" to customers; never the Premium or Pro tier of every app; no other trials or founding offers. Founder rulings 2026-11-06/07: the ONLY trial/offers are the World Pass 7-day trial (card required),
# FOUNDING 100 (30 days free after a real first action, no charge) and FOUNDING 500 ($10/mo while subscribed, first 500 per app).
WP_RULE = "The $20 World Pass is your passport across the whole ATH ecosystem: Premium of the one app you choose — WAVEMOTION, WealthyMindsets Pro and more — and Basic of every other ATH app, including apps still to come."
WP_NOTE = "Each app switches its tier on from your pass when you open it: WAVEMOTION and WealthyMindsets Pro today, and every app as it opens."
WP_SHORT = "$20: Premium of the app you choose, Basic of every other ATH app."
CHECK = '<svg class="vs-ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 12.5 4 4 8-9"/></svg>'
STEP = REG["package_step_up"]
def has_wp(p): return any("World Pass" in e["label"] for e in p.get("ecosystem", []))
def wp_value(head=True, eyebrow="Passport · the whole ecosystem"):
    """Free / Basic / World Pass ladder plus everything the $20 World Pass gets you. Reused on /path/ and /passport/ (the pricing page lists the WOW Pass once, as a service)."""
    free = [("Create your free Passport", "One identity, receipts and ownership across every ATH app"),
            ("Explore the Lounge", "WOW's social room, open to every visitor"),
            ("Listen to WOW Music and WOW Radio", "Real WOW artists, in rotation"),
            ("Watch WOW TV", "Films and shows in WOW OS"),
            ("Step into WOW Academy", "Free lessons: the Idea Library, languages, Student of the Game")]
    basic = [("WAVEMOTION Basic · Starter", "40 clips a month: turn one video into short clips"),
             ("WM Pro Basic", "The chart, workspace and journal on your own account"),
             ("Every app has one", "Pick Basic for just the app you need")]
    wp = [("Premium of the app you choose", "WAVEMOTION Premium (Creator, 80 clips a month) or WM Pro Premium — your favourite app, fully opened"),
          ("Basic of every other ATH app", "WAVEMOTION Starter or WM Pro Basic, whichever you didn't choose — and every app after them"),
          ("All of WOW OS on one pass", "Lounge, WOW TV, WOW Music, WOW Radio and the WOW Shop, carried by your Passport"),
          ("WOW Academy", "Classes and tracks: ideas, languages, the game of the market"),
          ("The WOW Marketplace", "Shop it, and apply to sell there as a WOW Creator Partner"),
          ("Dreamboard, when it opens", "At Basic, the day it launches"),
          ("Every new ATH app", "Each one joins your pass at Basic. Your price stays $20"),
          ("WOW World, when it opens", "The future metaverse: your Passport is already your way in")]
    li = lambda rows: "".join(f'<li class="wpv-row">{CHECK}<div><b>{n}</b><span>{d}</span></div></li>' for n, d in rows)
    return f"""<section class="block wpv" id="world-pass-value" aria-labelledby="wpv-h"><div class="wrap"><div class="panel wpv-panel">
 {f'<p class="eyebrow">{eyebrow}</p><h2 class="display d-m mt1" id="wpv-h">What the $20 World Pass<br>gets you</h2>' if head else '<h2 class="sr-only" id="wpv-h">What the $20 World Pass gets you</h2>'}
 <p class="lede wpv-lede">Your Passport is who you are across ATH. The World Pass turns it into a pass to the whole ecosystem: Premium of the app you love, Basic of everything else, and every new door the day it opens.</p>
 <div class="wpv-grid" id="ladder">
  <article class="wpv-tier"><p class="wpv-price">Free</p><p class="wpv-t">Free Passport</p><p class="wpv-d">Come in and look around. No card.</p><ul class="wpv-list">{li(free)}</ul></article>
  <article class="wpv-tier"><p class="wpv-price">$10<span> / month, per app</span></p><p class="wpv-t">Basic</p><p class="wpv-d">One app's essentials, per app.</p><ul class="wpv-list">{li(basic)}</ul></article>
  <article class="wpv-tier wpv-feature"><span class="wpv-badge">The whole ecosystem</span><p class="wpv-price">$20<span> / month</span></p><p class="wpv-t">World Pass</p><p class="wpv-d">Everything in the free Passport, plus:</p><ul class="wpv-list">{li(wp)}</ul>
   <p class="wpv-math">One $20 WOW Pass opens the whole world: Premium of the app you choose, Basic of every other ATH app, and all of WOW OS: the Lounge, the Academy, Games, Events, WOW TV, WOW Music and WOW Radio, plus your way into WM Pro. That is <b>more than $30 in app tiers alone</b>, before everything else, and it grows with every app ATH ships.</p></article>
 </div>
 <p class="note wpv-fine">World Pass is $20 a month after a 7-day free try (card required), cancel any time; your Passport identity is free. It opens Premium of the one app you choose, not the Premium or Pro tier of every app. Top tiers (WM Pro Auto-trading $30, WAVEMOTION Pro $50) are bought on their own; ATH services and third-party costs stay separate. {WP_NOTE}</p>
 <div class="ctas mt1">{btn("Get the World Pass", "https://thewow.online/passport", attrs='rel="noopener"')}{btn("Get your free Passport", "https://thewow.online/passport/claim", "line", 'rel="noopener"')}</div>
</div></div></section>"""
# ---------------------------------------------------------------- capability map (SP-055 / R41, 2026-10-23)
# Founder: "do everything a content platform does, plus everything else, cheaper — it's about presentation."
# One grouped "what we do" map. Every card names the ATH owner (Founder ownership order, 2026-10-21: no new
# standalone Content OS brand), an honest status, a price from the registry or "By quote", and a real next step.
P = {p["id"]: p for p in PKG}
# ATH websites always show the one-time hosting setup the card checkout charges (Founder 2026-11-01; "+ setup" on every page, 2026-11-12).
def site_price(pid): return f'{money(P[pid]["price"])} + {money(P[pid]["setup"])} setup'
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
 ("SPAID Business · PowerTribes", "flow", "Customers & teams", "Your company's office: AI staff, CRM, dialer, sales routing, team chat and operations. Live, included in every ATH plan.", "ATHOS AI staff · WAVEMOTION · Passport"),
 ("WOW OS", "lattice", "Identity, community & learning", "Passport, World Pass, Lounge, Academy, Shop, TV, Music and Radio.", "Every ATH app as it connects to Passport"),
]
def caps():
    """(group id, group title, eyebrow, [ (name, does, owner, status, price, cta, href, on_home) ])"""
    wm = cat_price("wm-plans").replace("/month", " a month")
    return [
     ("presence", "Build your presence", "Websites & digital experience", [
      ("Business website, done for you", "A mobile site with your services, hours, photos and buttons that work, linked to the booking or ordering you already use.", "ATH Web Studio", "live", f'{site_price("website-starter")} or {site_price("website-business")}, one time, or in every plan', "See every price", "/pricing/#services", True),
      ("Website health check", f'The {GC["name"]}: a {GC["minutes"]} minute live check of the site you already have, on a video call you watch. You learn what needs fixing and what doesn\'t.', "ATH Web Studio", "live", f"{GC_PRICE} one time", GC_CTA if not GC_PAY else "See the Garden Check", GC_PAGE, True),
      ("Brand themes & reusable sections", "Three tuned site styles built from reusable sections: menus and price lists, galleries, hours, story.", "ATH Web Studio", "inc", "In every site", "See sample sites", "/sites/", False),
      ("Preview & approval", "You see your site on a preview link, kept out of search, before it goes live. Revisions as your package states.", "ATH Web Studio", "inc", "In every site", "See every price", "/pricing/#services", True),
      ("Hosting & your own domain", "Fast static hosting. Move to your own domain whenever you like; the registrar fee (about $12 a year) is yours, at cost.", "ATH Web Studio", "inc", "Hosting included", "See every price", "/pricing/#services", False),
     ]),
     ("content", "Create & distribute content", "Video, clips & campaigns", [
      ("Clips from your videos", "Turn one long video into short captioned clips. You approve every clip before anything posts.", "WAVEMOTION", "live", wm, "See WAVEMOTION plans", "https://www.wavemotion.live/#pricing", True),
      ("Campaign workflow", "Record, prepare, approve, publish and learn, through the accounts you connect and within each platform's permissions.", "WAVEMOTION", "live", "In every plan", "Open WAVEMOTION", "https://www.wavemotion.live/", False),
      ("WOW Studios", "Timelines, music workflows, character continuity and collaborative workspaces. Bought with your Passport.", "WOW OS", "live", cat_price("wow-studios-plans"), "See the plans", "https://thewow.online/plans", False),
      ("WAVEMOTION in every ATH plan", "Every ATH plan includes WAVEMOTION, from Starter (40 clips a month) at $100 up to many Pro workspaces (250 clips a month each).", "WAVEMOTION", "inc", "In every plan", "See every plan", "/pricing/", True),
     ]),
     ("intelligence", "Intelligence & AI agents", "Diagnosis, assistants & memory", [
      ("Spaidbot assistant", "A free AI assistant on every page of this site. It answers from ATH's live price list and hands you to a person.", "ATHOS", "live", cat_price("spaidbot"), "Ask Spaidbot", "/contact/#ask", True),
      ("ATHOS Diagnostic", "Reads one public page, separates what it observed from what it inferred, and says unknown when it doesn't know.", "ATHOS", "live", "Free", "What's your hill?", "/diagnose/", True),
      ("Deep diagnostic", "Read-only inspection of the sources you authorize (code, docs, analytics, flows), delivered as a Hill Report.", "ATHOS · Atlas", "quote", "By written quote", "Request one", "/diagnose/deep/", False),
      ("Automation & business systems", "Apps, back ends, accounts, dashboards, integrations and automations, scoped in writing before any work starts.", "ATHOS + ATH Web Studio", "quote", pk("business-app-system"), "Scope it", "/contact/?intent=services&amp;package=business-app-system", False),
     ]),
     ("commerce", "Sell & get paid", "Checkout, apps & channels", [
      ("Checkout & booking links", "Your site's buttons go to the checkout, booking or ordering tool you already use. Nothing new to learn.", "ATH Commerce + ATH Web Studio", "inc", "In every site", "See every price", "/pricing/#services", False),
      ("Installable web app", "A scoped installable web app, or a single-platform app quoted on its own.", "ATH Web Studio", "quote", pk("app-starter"), "Scope it", "/contact/?intent=services&amp;package=app-starter", True),
      ("iOS + Android apps", "Basic apps for both stores on one shared architecture, under a written scope.", "ATH Web Studio", "quote", pk("mobile-app-bundle"), "Scope it", "/contact/?intent=services&amp;package=mobile-app-bundle", False),
      ("Web, mobile, TV & SDK", "One scoped system across web, mobile, television and integrations.", "ATH Web Studio", "quote", pk("omnichannel-system"), "Scope it", "/contact/?intent=services&amp;package=omnichannel-system", False),
     ]),
     ("community", "Identity, community & learning", "WOW OS", [
      ("Passport", "One identity across ATH apps: permissions, ownership and receipts that stay with you.", "WOW OS", "live", cat_price("wow-passport"), "Get a Passport", "https://thewow.online/passport", True),
      ("World Pass", WP_RULE + " " + WP_NOTE, "WOW OS", "live", cat_price("wow-world-pass").replace("/month", " a month"), "Get World Pass", "https://thewow.online/passport", True),
      ("FOUNDING 500", "The Passport at half price for the first 500 members of each app, for as long as you stay subscribed.", "WOW OS", "live", cat_price("wow-founding-500"), "Claim a seat", "https://thewow.online/passport#founding", False),
      ("Creator Passport", "WOW Studios + WAVEMOTION + Spaidbot on one bill, Passport included.", "WOW OS", "live", cat_price("creator-passport"), "See the plans", "https://thewow.online/plans", False),
      ("WOW Academy", "Idea Library, The Polyglot's Mind and Student of the Game. Stamps come from proof, not attendance.", "WOW OS", "live", cat_price("wow-academy-free"), "Visit the campus", "https://thewow.online/academy", False),
      ("Lounge, TV, Music, Radio & Shop", "Rooms to connect, watch, listen and shop, entered from WOW OS. Guests welcome.", "WOW OS", "live", "Free to enter", "Enter WOW OS", "https://thewow.online/", False),
     ]),
     ("teams", "Customers, teams & specialist systems", "SPAID Business · PowerTribes · specialist OS", [
      ("Prospecting, CRM & sales routing", "Find, qualify and follow up with customers, connected to your site and campaigns.", "SPAID Business", "dev", "Not sold yet", "Request access", "/contact/?intent=services", True),
      ("Workforce & operations OS", "Your PowerTribes office: Call Desk, appointment setter, tasks and team. A bigger office at every step of the ladder.", "PowerTribes", "inc", "In every plan", "See every plan", "/pricing/", False),
      ("PowerTribes on its own", "Solo, Team or Business OS: CRM and pipeline, then team, dialer and coaching, then the full business OS. Launch prices; Enterprise by quote.", "PowerTribes", "live", cat_price("powertribes-plans"), "See the plans", "https://thewow.online/plans", False),
      ("Wealthy Mindsets Pro", "A trading workspace with a chart, a journal and lessons. Education and tools, not financial advice.", "Wealthy Mindsets Pro", "live", "Free guest · Basic $10 · Premium $20 · Auto-trading $30 a month", "Take the guest tour", "https://wealthymindsetspro.com/welcome", True),
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
     ("Websites built for you", f'A Starter Website at {site_price("website-starter")} or a Business Website at {site_price("website-business")}, one time, or a website inside every ATH plan.', "live"),
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
   <div class="ctas mt2">{btn("See every price", "/pricing/")}{btn("ATH Services", "/build/", "line")}</div></div>
 </div>
</div></section>"""
def gc_panel(eyebrow="Already have a website?"):
    """The Mansion Garden Check, from the registry: the oil-change offer for a site that already exists."""
    return f'''<section class="block" id="garden-check"><div class="wrap"><div class="panel panel-pad gc-panel" style="display:flex;gap:24px;align-items:center;justify-content:space-between;flex-wrap:wrap">
 <div style="flex:1 1 420px;max-width:62ch">{ic(GC["icon"])}<p class="eyebrow mt1">{eyebrow}</p><h2 class="display d-m mt1">{GC["name"]}</h2>
  <p class="body mt1"><b>{html.escape(GC["tagline"])}</b> {html.escape(GC["summary"])}</p>
  <p class="note mb0">{html.escape(GC["privacy"])} {html.escape(GC["fixes_note"])}</p></div>
 <div><p class="vs-price mb0">{GC_PRICE}</p><p class="note">one time · {GC["minutes"]} minutes · live</p>
  <div class="ctas" style="margin:0">{btn(GC_CTA, GC_HREF, attrs='rel="noopener"' if GC_PAY else "")}{btn("What we check", GC_PAGE, "line")}</div></div>
</div></div></section>'''

# ---------------------------------------------------------------- pages
pages = {}

# Commercials (2026-11-12): the Master "Welcome to Above The Hill" walkthrough as the home page feature film, plus the 30 s
# app spots. Real live-app footage, AI voice (labelled in the frame), captions burned in. Files live in the public Supabase
# bucket "radio" (commercials/ath-1112/), web encodes of ~/Desktop/COMMERCIALS-1112. Nothing loads until the film is on screen.
FILM_BASE = "https://zrzaifaxecwgpfrqctkp.supabase.co/storage/v1/object/public/radio/commercials/ath-1112/"
FILM_SCRIPT = ("Ah, you made it. Here's your key. Welcome to Above The Hill. They told you that you needed a website. But what if your business had a whole headquarters? "
  "Step inside. First door: WOW TV, your own channel, live 24/7, on a real rolling guide. Down the hall: WAVEMOTION. Your website. Your content. One link. "
  "Pick an atmosphere (Stage, Studio, Business) and it's yours for $20 a month. Now take the elevator. PowerTribes Tower: fifteen floors, one business. "
  "The Sales Floor. AI Workforce Command. Your whole company under one roof. Next door: WOW Studios. Record it. Mix it. Cut the video. Build the world. "
  "This is Spaidbot. Say what you need, and Spaidbot builds it. And the penthouse: WM Pro. Read the market before you risk a dollar. WM Pro: $10, $20, $30. "
  "One key opens every door: your WOW Passport. Free to start. Founding 500: just $10 a month, locked in while you stay. One key. Every door. Above The Hill. There's more.")
SPOTS = [
 ("ath-02-wow-tv", "WOW TV", "Your channel, live 24/7", "25 s", "https://thewow.online/wow-tv",
  "Hold up. Is that a TV channel on a website? That's WOW TV, World of Wealth Television, live 24/7. A real rolling guide. Real channels. Got music, a podcast, a show? Request your own channel. And your WOW Passport is free."),
 ("ath-03-wavemotion-sites", "WAVEMOTION", "Your website. Your content. One link.", "28 s", "https://www.wavemotion.live/sites",
  "They said you needed a link in bio. You need a home. WAVEMOTION builds your whole website: music, video, episodes, shop, booking. Five cinematic atmospheres. Real click analytics. Your Creator site: $20 a month."),
 ("ath-04-powertribes-tower", "PowerTribes", "Your company's own tower", "27 s", "https://powertribes.cloud",
  "Your business isn't a contact list. It's a tower. Fifteen floors, one business: the Sales Floor, the dialer, the deals board, AI Workforce Command, the Executive Suite. Plans from $29 a month."),
 ("ath-05-wow-studios", "WOW Studios", "A production house in your browser", "29 s", "https://wowstudios.cloud",
  "Make the record. Cut the video. Build the world. The Edit Suite, the Arrange window, the Mixer, the Booth. Your WOW Passport is free to start. Plans from $29 a month."),
 ("ath-08-founding-500", "Founding 500", "$10 a month, every door", "29 s", "https://thewow.online/passport",
  "One key opens every door: your WOW Passport, free to start. WOW TV, WAVEMOTION and more. Founding 500: just $10 a month, locked in while you stay."),
]
def film_section():
    spots = "".join(
        f'<li class="spot"><button type="button" class="spot-btn" data-film-spot="{FILM_BASE}{k}-16x9.mp4" aria-label="Play the {html.escape(n)} commercial, {d}, with sound">'
        f'<img src="{FILM_BASE}{k}-16x9.jpg" alt="" loading="lazy" decoding="async" width="960" height="540"><span class="spot-play" aria-hidden="true">&#9654;</span></button>'
        f'<p class="spot-name"><b>{html.escape(n)}</b> <span class="note">{d}</span></p><p class="spot-line">{html.escape(t)}</p>'
        f'<details class="film-script"><summary>Read the script</summary><p>{html.escape(sc)}</p></details>'
        f'<a class="gold spot-door" href="{u}" rel="noopener">Open {html.escape(n)} {ARR}</a></li>' for k, n, t, d, u, sc in SPOTS)
    return f"""<section class="block film-block" id="watch" aria-labelledby="watch-h"><div class="wrap">
 <div class="block-head"><div><p class="eyebrow">Welcome to Above The Hill</p><h2 class="display d-m mt1" id="watch-h">One key. Every door.</h2></div>
  <p class="body mb0" style="max-width:46ch">A one-minute walk through every ATH app: WOW TV, WAVEMOTION, PowerTribes, WOW Studios, Spaidbot and WM Pro. Real app screens.</p></div>
 <figure class="film-frame" data-film data-src16="{FILM_BASE}ath-master-16x9.mp4" data-src9="{FILM_BASE}ath-master-9x16.mp4" data-poster16="{FILM_BASE}ath-master-16x9.jpg" data-poster9="{FILM_BASE}ath-master-9x16.jpg">
  <video class="film-video" muted playsinline loop preload="none" poster="{FILM_BASE}ath-master-16x9.jpg" aria-label="Commercial: Welcome to Above The Hill, 69 seconds. Captions are in the picture."></video>
  <button type="button" class="film-sound" data-film-sound aria-pressed="false"><span aria-hidden="true">&#128263;</span> <span data-film-sound-label>Tap for sound</span></button>
 </figure>
 <div class="film-under"><p class="note mb0">AI voice · real app screens · captions on · 69 s</p><details class="film-script"><summary>Read the script</summary><p>{html.escape(FILM_SCRIPT)}</p></details></div>
 <h3 class="display d-s mt3 film-row-h">Watch the apps</h3>
 <ul class="spot-row" role="list">{spots}</ul>
</div></section>""" + FILM_JS
FILM_JS = r"""<script>(() => {
  const f = document.querySelector('[data-film]'); if (!f) return;
  const v = f.querySelector('video'), snd = f.querySelector('[data-film-sound]'), lab = f.querySelector('[data-film-sound-label]');
  const tall = matchMedia('(max-width:700px) and (orientation:portrait)'), calm = matchMedia('(prefers-reduced-motion:reduce)');
  const pick = () => { const t = tall.matches; f.classList.toggle('is-tall', t); v.poster = f.dataset[t ? 'poster9' : 'poster16']; return f.dataset[t ? 'src9' : 'src16']; };
  let want = pick(), loaded = false;
  const load = () => { if (loaded && v.dataset.src === want) return; const at = v.currentTime || 0, was = !v.paused; v.src = want; v.dataset.src = want; loaded = true; if (at) v.currentTime = at; if (was) v.play().catch(() => {}); };
  const sound = (on) => { v.muted = !on; snd.setAttribute('aria-pressed', String(on)); lab.textContent = on ? 'Sound on' : 'Tap for sound'; snd.firstElementChild.innerHTML = on ? '&#128266;' : '&#128263;'; };
  tall.addEventListener?.('change', () => { want = pick(); if (loaded) load(); });
  new IntersectionObserver((es) => es.forEach((e) => {
    if (e.isIntersecting && e.intersectionRatio >= 0.35) { load(); if (!calm.matches || !v.muted) v.play().catch(() => {}); }
    else if (!v.paused) v.pause();
  }), { threshold: [0, 0.35, 0.7] }).observe(f);
  snd.addEventListener('click', () => { load(); const on = v.muted; if (on) { v.loop = false; if (v.ended) v.currentTime = 0; } else v.loop = true; sound(on); v.play().catch(() => {}); });
  v.addEventListener('click', () => snd.click());
  v.addEventListener('ended', () => { sound(false); v.loop = true; v.currentTime = 0; v.play().catch(() => {}); });
  document.querySelectorAll('[data-film-spot]').forEach((b) => b.addEventListener('click', () => {
    document.querySelectorAll('.spot video').forEach((o) => o.pause()); v.pause(); sound(false); v.loop = true;
    const sv = document.createElement('video'); sv.src = b.dataset.filmSpot; sv.controls = true; sv.playsInline = true; sv.autoplay = true; sv.preload = 'auto';
    sv.className = 'spot-video'; sv.setAttribute('aria-label', b.getAttribute('aria-label').replace('Play the ', ''));
    b.replaceWith(sv); sv.play().catch(() => {}); sv.addEventListener('play', () => { document.querySelectorAll('.spot video').forEach((o) => { if (o !== sv) o.pause(); }); v.pause(); sound(false); v.loop = true; });
  }));
})();</script>"""
pages["/"] = ("Above the Hill Developments — We build the way over it",
 "ATH is an invention company. Tell ATHOS what's stopping you — get an evidence-aware diagnosis, a clear path, and a builder who can take you above.",
 hero("home", "", "Above<br>the Hill",
      "Every dream, business and creator eventually meets a hill.<br>We build the way over it.",
      btn("What's your hill?", "/diagnose/") + btn("Explore ATH", "/company/", "line"),
      extra='<div class="stack" aria-hidden="true">Plain truth<br>Higher ground<br>Real creation<br>For generations</div>',
      pos="72% 35%", mpos="58% 30%")
 + f'<div class="wrap ladder-dock">{ladder()}</div>'
 + film_section()
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
 <div class="block-head"><div><p class="eyebrow">Start with what you do</p><h2 class="display d-m mt1">Find your door</h2></div>{btn("All prices", "/pricing/", "line")}</div>
 <div class="grid g3">{outcome_cards()}</div>
</div></section>
<section class="block cap-block" id="what-we-do"><div class="wrap">
 <div class="block-head"><div><p class="eyebrow">What ATH does</p><h2 class="display d-m mt1">One ecosystem.<br>Every part has an owner.</h2></div>
  <div style="max-width:46ch"><p class="body mb0">Websites, content, AI, checkout, community and the systems behind them, each run by one ATH product. Every card shows who owns it, whether it's live, and what it costs.</p><p class="mt1 mb0">{btn("The full map", "/ecosystem/#map", "line")}</p></div></div>
 {cap_tiles()}
</div></section>
""" + compare_section() + f"""
<section class="block" id="plans"><div class="wrap">
 <div class="block-head"><div><p class="eyebrow">One ladder</p><h2 class="display d-m mt1">From $100 to $8,000 a month.<br>More of everything at every step.</h2></div>{btn("See every plan", "/pricing/", "line")}</div>
 {plan_strip()}
 <p class="note mt2">Every plan includes a piece of everything ATH makes: a WOW Pass, a PowerTribes office, WAVEMOTION, Spaidbot, WM Pro, AI receptionist minutes and text-back, review requests and a website. The higher the step, the more of it you get. No trial, no free month, no discount.</p>
 <p class="note mt1">Already have a site? Start smaller: the <a class="gold" href="{GC_PAGE}">{GC["name"]}</a> is {GC_PRICE} one time. Like an oil change: pull in, {GC["minutes"]} minutes, done.</p>
</div></section>
<section class="block"><div class="wrap">
 <div class="block-head"><div><p class="eyebrow">Inventions</p><h2 class="display d-m mt1">Built by ATH</h2></div>{btn("All inventions", "/work/", "line")}</div>
 <div class="grid g3">
  <article class="panel panel-pad card"><span class="tag live">Live today</span><h3>ATHOS Diagnostic</h3><p>The free hill-finder on this site. Inspects public evidence, separates what it observed from what it inferred, and says "unknown" when it doesn't know.</p><p class="mt2">{btn("Run it", "/diagnose/", "line")}</p></article>
  <article class="panel panel-pad card"><span class="tag">Open door</span><h3>WealthyMindsets Pro</h3><p>One complete professional trading operating system — the chart as the room, intelligence that respects price truth. Free guest account, then Basic $10, Premium $20 or Auto-trading $30 a month. No profits promised.</p><p class="mt2"><a class="btn btn-line" href="https://wealthymindsetspro.com" rel="noopener">Visit WM Pro {ARR}</a></p></article>
  <article class="panel panel-pad card"><span class="tag live">Open door</span><h3>WAVEMOTION</h3><p>One video in, a week of clips out. Drop in one long video (a sermon, a podcast, a live, a song) and get it back as short vertical clips for TikTok, Reels and YouTube Shorts: 40 a month on Starter ($10), 80 on Creator ($20), 250 on Pro ($50). You approve every clip before anything posts, and it goes out on the schedule you pick. Starter $10 · Creator $20 · Pro $50 a month, clips included.</p><p class="mt2">{btn("Open Wavemotion", "https://www.wavemotion.live/", "line")}</p></article>
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
 "Come in free with your Passport. Open one app with Basic for $10. Open the whole ecosystem with the World Pass for $20. Or let ATH build the path.",
 hero("path", "How ATH works", "One path.<br>Different<br>relationships.",
      "Come in free. Open one app with Basic.<br>Open everything with the World Pass.<br>Or let ATH build the path.", "", pos="66% 45%", size="d-l")
 + f'<div class="wrap ladder-dock">{ladder()}</div>'
 + f"""
<section class="block"><div class="wrap">
 <div class="grid g2">
  <div class="panel panel-pad"><p class="panel-title">Basic opens one app. The World Pass opens the ecosystem.</p>
   <p class="body"><b>Basic, $10/month per app</b>: one app's essentials, like WAVEMOTION Starter or WM Pro Basic. <b>World Pass, $20/month</b>: Premium of the app you choose and Basic of every other ATH app, including apps still to come. {WP_NOTE} Try the World Pass 7 days free (card required). WM Pro Auto-trading is $30/month and WAVEMOTION Pro $50/month.</p>
   <p class="panel-title mt2">What $20 is — and isn't</p>
   <p class="body">The World Pass is the $20 purchase itself, carried on your free Passport: Premium of one app, Basic of every other app. It does <b>not</b> unlock the Premium or Pro tier of every app, ATH services, third-party costs, or unlimited expensive infrastructure.</p>
   <dl class="hpa mt2"><dt>Identity</dt><dd>≠ membership</dd><dt>Membership</dt><dd>≠ owning every product</dd><dt>Membership</dt><dd>≠ professional infrastructure</dd></dl></div>
  <div class="panel panel-pad"><p class="panel-title">No surprise costs</p>
   <p class="body">Some things cost real money to run — market data, heavy AI compute, video/image/audio generation, mass messaging, unusual storage or bandwidth. We handle those with included allowances, bring-your-own credentials where lawful, add-ons or pass-through costs. Never hidden behind "unlimited".</p></div>
 </div>
 <div class="panel panel-pad mt2"><p class="panel-title">Availability today</p>
  <ul class="rows">
   <li>{ic("free","icon-sm")}<div><b>Free ATH Diagnostic</b><span>Available now — no account required. <a class="gold" href="/diagnose/">Run it</a>.</span></div></li>
   <li>{ic("door","icon-sm")}<div><b>Basic — $10 a month per app</b><span>WAVEMOTION turns one long video into a week of short clips you approve before they post. Starter (Basic) $10 · Creator (Premium) $20 · Pro $50 per month. No permanent free operator tier; public Living Destinations stay viewable. <a class="gold" href="/contact/?intent=wavemotion">Start Wavemotion with ATH</a>.</span></div></li>
   <li>{ic("lattice","icon-sm")}<div><b>World Pass — $20 / month</b><span>{WP_RULE} {WP_NOTE} Available now on WOW OS, on your free Passport. <a class="gold" href="https://thewow.online/passport" rel="noopener">Get World Pass</a>.</span></div></li>
   <li>{ic("triangle","icon-sm")}<div><b>Specialist systems — plans vary by operating system</b><span>WealthyMindsets Pro: a free guest account, WM Pro Basic $10/month, Premium $20/month and Auto-trading $30/month. Spaidbot: Personal $19, Builder $49, Operations $99 a month. WOW Studios: Solo $29, Creator $59, Pro $119 a month. PowerTribes launch prices: Solo $29 (standard <s>$49</s>), Team $79 (<s>$149</s>), Business OS $179 (<s>$349</s>) a month. Creator Passport: Launch $40, Grow $75, Pro $100, Studio $150 a month. <a class="gold" href="https://thewow.online/plans" rel="noopener">See the plans</a>. Exchange, data or broker fees ATH doesn't control stay separate. No profit or return is ever promised. <a class="gold" href="https://wealthymindsetspro.com" rel="noopener">Go to WM Pro</a>.</span></div></li>
   <li>{ic("peaks","icon-sm")}<div><b>ATH plans and services — every price published</b><span>ATH plans from $100 to $8,000 a month, one ladder; websites {site_price("website-starter")} (Starter) and {site_price("website-business")} (Business), one time; WAVEMOTION starts at $10 a month, apps from $1,000, custom systems scoped and quoted. <a class="gold" href="/pricing/">See every price</a>.</span></div></li>
  </ul></div>
</div></section>""" + wp_value() + cta_block())

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
   ("lattice","World Pass","$20 / month",WP_RULE + " " + WP_NOTE),
   ("triangle","Specialist Entitlements","Plans vary","WealthyMindsets Pro: free guest, Basic $10, Premium $20, Auto-trading $30. Spaidbot $19 / $49 / $99, WOW Studios $29 / $59 / $119, PowerTribes from $29 at launch and Creator Passport $40 to $150 are bought with your Passport. Dreamboard and future systems carry their own plans."),
   ("own","Purchases &amp; Ownership","Yours","What you bought and what remains yours, carried by Passport where supported.")])}
 </div>
 <div class="grid g2 mt3" id="benefits">
  <div class="panel panel-pad"><p class="panel-title">If a member cancels</p><p class="body mb0">The person doesn't stop existing. Identity, lawful ownership, receipts and applicable durable rights persist. Membership-only benefits end.</p></div>
  <div class="panel panel-pad"><p class="panel-title">Availability</p><p class="body">Passport is free. The World Pass is $20/month; try it 7 days free (card required). FOUNDING 500: the first 500 members of each app get the Passport at half price, $10/month while subscribed. All live on WOW OS today, with a real Stripe checkout, and you can cancel any time.</p><p class="body">{WP_RULE} {WP_NOTE}</p><div class="ctas mt1">{btn("Get your free Passport", "https://thewow.online/passport/claim")}{btn("Get World Pass", "https://thewow.online/passport", "line")}</div></div>
 </div>
</div></section>""" + wp_value(eyebrow="Passport · the whole ecosystem"))

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
  <h2 class="display d-m" id="pricing-h">Prices</h2>
  <p class="body">ATH has one ladder of monthly plans, and a short list of services you can buy on their own. <a class="gold" href="/pricing/">See exactly what every plan includes</a>.</p>
  <div class="panel panel-pad mt2"><p class="panel-title">ATH plans · $100 to $8,000 a month</p>{plan_strip()}
   <p class="note mt2 mb0">Every plan has a piece of everything ATH makes, and more of it at every step. Book a call to start; card checkout opens plan by plan.</p></div>
  <div class="mt2">{services_list()}</div>
  <p class="body mt2"><b>Starts at $10 a month</b>: one link for all your socials, your analytics in one place, and clips from your videos. WAVEMOTION clips come with the plan; there is no separate clip menu, and orders placed before the change are honored as bought.</p>
  {holiday_note()}
  <p class="note mt2">Custom-build prices are starting points for a written scope, not unlimited work. Third-party costs (ads, domains, paid tools) are passed through at cost, never hidden. Catalog version {REG["version"]}.</p>
 </section>
</div></section><section class="block"><div class="wrap">
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

# A checklist line (Garden Check page): a dollar value appears only where the registry itself states one.
def vs_line(label, note="", dim=False):
    m = re.search(r"\s*\((\$\d+) value\)", label)
    val = f'<span class="vs-val">{m.group(1)} value</span>' if m else ""
    label = label.replace(m.group(0), "") if m else label
    return (f'<li class="vs-row{" vs-dim" if dim else ""}">{CHECK if not dim else ic("lock", "vs-ic")}<div><b>{html.escape(label)}</b>'
            + (f'<span>{html.escape(note)}</span>' if note else "") + f'</div>{val}</li>')

# ---------------------------------------------------------------- /pricing/: THE price book (Founder direction 2026-10-31)
# One ladder (15 steps, one name and one price each) and, apart from it, the services you can buy on their own.
# Replaces the /offer/ website-package page (its $100 / $200 one-time sites doubled the $100 and $200 plan prices).
pages["/pricing/"] = ("Prices — ATH plans from $100 to $8,000 a month",
 "One ladder of ATH plans, $100 to $8,000 a month: every step has a WOW Pass, a PowerTribes office, WAVEMOTION, Spaidbot, WM Pro, AI receptionist minutes, review requests and a website, more at every step. Services you can buy on their own are listed separately.",
 f"""<section class="hero pb-hero" style="--pos:62% 55%;--mpos:55% 40%;min-height:auto">
 <div class="hero-art"><img src="/assets/art/build.webp" alt="" fetchpriority="high"></div>
 <div class="wrap"><div class="hero-copy">
  <p class="eyebrow">Prices · one ladder · one price for everyone</p>
  <h1 class="display d-l">A piece of everything.<br>More at every step.</h1>
  <p class="lede">Fifteen plans, from $100 to $8,000 a month. Every plan includes a little of everything ATH makes; the higher you go, the more of it you get.</p>
  <div class="ctas">{btn("See the plans", "#pricing")}{btn("Services on their own", "#services", "line")}</div>
 </div></div>
</section>
<section class="block pb-block" id="pricing" data-sb-pricing aria-labelledby="pb-h"><div class="wrap">
 <div class="block-head"><div><p class="eyebrow">ATH plans · monthly</p><h2 class="display d-m mt1" id="pb-h">One ladder,<br>$100 to $8,000</h2></div>
  <p class="note" style="max-width:46ch">Each step keeps everything below it and adds more. Tap a step to jump to what it includes.</p></div>
 {plan_strip()}
 <div class="pb-every panel panel-pad mt2"><p class="panel-title">In every plan, from the first step</p>
  <ul class="pb-every-list">{"".join(f'<li>{ic(i, "icon-sm")}<span>{t}</span></li>' for i, t in EVERY_PLAN)}</ul></div>
 {plan_cards()}
 <ul class="pkg-list mt2 pb-fine">{"".join(f"<li>{html.escape(f)}</li>" for f in PB["fine"])}<li>Price book version {PB["version"]}, {PB["as_of"]}. Card checkout opens plan by plan; until then, every plan starts with a call and a written scope.</li></ul>
</div></section>
<section class="block pb-block" aria-labelledby="sv-h"><div class="wrap">
 <div class="block-head"><div><p class="eyebrow">Not part of a plan</p><h2 class="display d-m mt1" id="sv-h">Services on their own</h2></div>
  <p class="note" style="max-width:46ch">Buy one thing by itself. These are separate from the plans above, and a plan already includes a piece of most of them.</p></div>
 {services_list(head=False)}
</div></section>""" + cta_block("Not sure which step?", "Start with the free business diagnosis. A person tells you where you leak first, and which step fixes it."))

ECO = [
 ("ATH", "Parent builder", "live", "You're here", "The invention company. Builds, owns and routes.", ("Diagnose", "/diagnose/")),
 ("ATHOS", "Intelligence", "live", "Diagnostic live", "Diagnosis, evidence, routing. The free diagnostic on this site is ATHOS working today; deeper capabilities are in development.", ("Run it", "/diagnose/")),
 ("Passport", "Identity spine · Free", "live", "Open door", "Identity, permissions, ownership, receipts, continuity. Free, in WOW OS.", ("Get Passport", "https://thewow.online/passport/claim")),
 ("World Pass", "On WOW OS · $20/mo", "live", "Open door", WP_RULE + " " + WP_NOTE + " Cancel any time.", ("Get World Pass", "https://thewow.online/passport")),
 ("WAVEMOTION", "One video in, a week of clips out", "live", "Open door", "Drop in one long video (a sermon, a podcast, a live, a song) and get it back as short vertical clips for TikTok, Reels and YouTube Shorts: 40 a month on Starter ($10), 80 on Creator ($20), 250 on Pro ($50). You approve every clip before anything posts, and it goes out on the schedule you pick.", ("Visit Wavemotion", "https://wavemotion.live/")),
 ("WM Pro", "Wealthy Mindsets Pro · free guest tour", "", "Open door", "Free guest account · Basic $10/mo · Premium $20/mo · Auto-trading $30/mo. Third-party data/broker fees separate. No profits promised.", ("Go to WM Pro", "https://wealthymindsetspro.com")),
 ("PowerTribes", "Business · sales · workforce · leadership OS", "live", "Live · in every plan", "Your company's office: AI staff at their desks, CRM, dialer, team chat and operations. Included in every ATH plan; team sizes by plan.", ("See the plans", "/pricing/")),
 ("Dreamboard", "Human-potential &amp; creative OS", "dim", "Built · opening to members", "Idea → clarity → project → finished work. When it opens, World Pass members get its Basic tier.", ("Join the list", "/contact/?intent=dreamboard")),
 ("WOW OS", "The operating system · Guest welcome", "live", "Open door", "One home, many rooms — Lounge, Academy (Idea Library, Visual Learns, Student of the Game), Marketplace, Events, WOW TV, WOW Music, WOW Radio.", ("Enter", "https://thewow.online/")),
 ("WOW TV · WOW Radio", "Watch · Listen", "live", "Open door", "Viewer and listener destinations — separate rooms in WOW OS.", ("Enter", "https://thewow.online/wow-tv")),
 ("Lounge · Academy · Shop", "Connect · Learn · Own", "live", "Open door", "Community, learning and commerce places, entered from WOW OS.", ("Enter", "https://thewow.online/lounge")),
 ("WOW Academy", "Learn · Free to practise", "live", "Open door", "Three real tracks, open now: The Idea Library (read, question, remember, apply), Visual Learns · The Polyglot&#8217;s Mind (Spanish, Hebrew, Japanese), and Student of the Game (risk, candles, orders). A stamp is earned from proof and memory, never attendance.", ("Open the Academy", "https://thewow.online/academy")),
 ("WOW Studios", "Creation studio · Solo $29 · Creator $59 · Pro $119 a month", "live", "Open door", "Timelines, then music workflows and character continuity, then collaborative workspaces and top exports. Bought with your Passport.", ("See the plans", "https://thewow.online/plans")),
 ("Spaidbot", "AI assistant · Personal $19 · Builder $49 · Operations $99 a month", "live", "Open door", "Free on every page of this site. Personal: generous chat, research and drafts. Builder adds automation, projects and integrations. Operations adds cloud jobs and team runs.", ("See the plans", "https://thewow.online/plans")),
 ("PowerTribes plans", "Solo $29 · Team $79 · Business OS $179 a month (launch prices)", "live", "Open door", "Standard value <s>$49</s> · <s>$149</s> · <s>$349</s>. CRM and pipeline, then team, dialer and coaching, then the full business OS. Enterprise by quote.", ("See the plans", "https://thewow.online/plans")),
 ("Creator Passport", "Launch $40 · Grow $75 · Pro $100 · Studio $150 a month", "live", "Open door", "One bill for creators, Passport included: WOW Studios + WAVEMOTION + Spaidbot together. Launch: Studios Solo, WAVEMOTION Starter, Spaidbot Personal. Grow: Creator, Creator, Builder. Pro: Pro, Pro, Builder. Studio: Pro, Pro, Operations, with team seats.", ("See the plans", "https://thewow.online/plans")),
 ("FOUNDING 500", "$10 a month while subscribed", "live", "First 500 per app", "The Passport at half price for the first 500 members of each app (WM Pro, WOW OS, WAVEMOTION), for as long as you stay subscribed.", ("Claim a seat", "https://thewow.online/passport#founding")),
 ("WOW World", "The future metaverse", "dim", "Future", "A future world for the whole ecosystem. Not open and not for sale; WOW OS is the live home today.", None),
]
def eco_cards():
    out = []
    for n, r, cls, st, d, c in ECO:
        anchor = "wavemotion" if n == "Wavemotion" else ("specialist" if n == "WM Pro" else ("plans" if n == "Creator Passport" else ""))
        cbtn = ""
        if c:
            ext = c[1].startswith("http")
            cbtn = f'<p class="mt2 mb0"><a class="btn btn-line btn-sm" href="{c[1]}"{" rel=\"noopener\"" if ext else ""}>{c[0]} {ARR}</a></p>'
        out.append(f'<article class="panel panel-pad card"{f" id=\"{anchor}\"" if anchor else ""}><span class="tag {cls}">{st}</span><h3>{n}</h3><p class="gold" style="font-size:13px;margin-bottom:8px">{r}</p><p>{d}</p>{cbtn}</article>')
    return "".join(out)

pages["/ecosystem/"] = ("The Ecosystem — What ATH does, who owns it, what it costs",
 "Websites, content, AI, checkout, community and business systems: one ATH ecosystem, every capability with its owner, live status and price.",
 hero("ecosystem", "", "The<br>Ecosystem",
      "ATH builds the world.<br>Destinations open the doors.<br><span style=\"font-size:max(13px, .8em);color:var(--ivory-dim)\">Not an app store. Parent builder · intelligence · identity · membership · destinations.</span>",
      btn("See the full map", "#map") + btn("See every price", "/pricing/", "line"), extra='<div class="plaques">' + "".join(f'<a class="plaque" href="#d"><b>{n}</b><span>{t}</span></a>' for n,t in [("WOW OS","Open door"),("WM Pro","Open door"),("WOW TV · WOW Radio","Open door"),("Lounge · Academy · Shop","Open door")]) + '</div>', pos="50% 50%", mpos="50% 40%", size="d-l")
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
   ("","Open door","WM Pro","Traders drown in tools that paste intelligence around a chart.","A market OS where the chart is the room and every mark respects price truth.","Open at wealthymindsetspro.com. Free guest account, then Basic $10, Premium $20 or Auto-trading $30 a month.", f'<p class="mt2 mb0"><a class="btn btn-line" href="https://wealthymindsetspro.com" rel="noopener">Visit {ARR}</a></p>'),
   ("","Open door","Wavemotion","Creators and businesses lose momentum between recording and real distribution.","Record → cloud inbox → edit → variants → approval → publish → receipt → learning loop.","Plans $10 / $20 / $50 per month, clips included. Cinematic generation is not open.", f'<p class="mt2 mb0">{btn("Open Wavemotion","https://www.wavemotion.live/","line")}</p>'),
   ("dim","Built · opening","Dreamboard","Ideas die between inspiration and a finished thing.","Idea → clarity → project → creation → finishing evidence.","Built; opening to members next.", ""),
   ("live","Live","Passport","Every app makes you a stranger again.","One identity spine — permissions, ownership, receipts, continuity.","Free and live in WOW OS; one Passport across ATH apps as each connects.", f'<p class="mt2 mb0"><a class="btn btn-line" href="https://thewow.online/passport/claim" rel="noopener">Get Passport {ARR}</a></p>'),
   ("","Open door","WOW OS","Products feel like islands.","A connected world of destinations under one builder.","Open at thewow.online — guests welcome, free Passport. The $20 World Pass: Premium of the app you choose plus Basic of every other ATH app.", f'<p class="mt2 mb0"><a class="btn btn-line" href="https://thewow.online/" rel="noopener">Enter {ARR}</a></p>')])}
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
  <li>{ic("lattice","icon-sm")}<div><b>World Pass</b><span>{WP_SHORT}</span></div></li>
  <li>{ic("door","icon-sm")}<div><b>Destinations</b><span>Wavemotion, WM Pro, PowerTribes, Dreamboard, WOW OS and more — each owns its own experience.</span></div></li></ul></div>
</div></section>""" + cta_block())

pages["/contact/"] = ("Contact ATH — Start",
 "Request access, join a waitlist, or ask ATH to build your path.",
 f"""<section class="block" style="padding-top:56px"><div class="wrap split" style="align-items:start">
 <div><p class="eyebrow">Contact / Start</p><h1 class="display d-l mt1">Start the<br>climb</h1>
  <p class="lede">Tell us where you are. A person at ATH reads every message.</p>
  <p class="body mt2"><b>Call or text us:</b> <a class="gold" href="tel:+19189600164">(918) 960-0164</a> · <a class="gold" href="sms:+19189600164">Send a text</a></p>
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
  <ul class="pkg-list mt2"><li>Starter Website: <b>{site_price("website-starter")}, one time</b>, preview first; you pay only if you love it</li><li>Up to 5 pages, linked to the booking or ordering you already use, with a year of small updates: <b>{site_price("website-business")}, one time</b></li><li>Or an ATH plan with your website, missed-call text-back and review requests in it: <b>from $100 a month</b> (Presence). <a class="gold" href="/pricing/">See every plan</a></li></ul>
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
  <p class="body">A mobile website for their business, <b>{site_price("website-starter")}, one time</b>. Up to 5 pages, linked to the booking or ordering they already use, with a year of small updates, is {site_price("website-business")}. Order early for the holidays: ATH confirms the go-live date when their info arrives.</p>
  <div class="ctas mt1">{btn("Get a free look", "/free-look/")}{btn("See sample sites", "/sites/", "line")}</div></div></div></section>""")

pages["/start/"] = ("Start your build — ATH intake",
 "Tell ATH about your business so we can start building.",
 f"""<section class="block" style="padding-top:56px"><div class="wrap split" style="align-items:start">
 <div><p class="eyebrow">Payment received · Next step</p><h1 class="display d-l mt1" id="start-h1">Let's build<br>your site</h1>
  <p class="lede" id="start-lede">Thank you. Tell us about your business and ATH starts the build.</p>
  <p class="body mt2" id="start-body">Share links to your logo and photos (Google Drive, Dropbox, Instagram or your current site). A person at ATH reads every intake and replies.</p>
  <p class="note mt2">Didn't pay yet? <a class="gold" href="/pricing/">See prices</a>.</p></div>
 <form class="panel panel-pad" id="intake-form" novalidate>
  <input type="hidden" name="intent" value="paid-intake">
  <div class="grid g2"><div class="field"><label class="lbl" for="i-name">Your name</label><input id="i-name" name="name" type="text" autocomplete="name" required></div>
   <div class="field"><label class="lbl" for="i-email">Email used at checkout</label><input id="i-email" name="email" type="email" autocomplete="email" required></div></div>
  <div class="grid g2"><div class="field"><label class="lbl" for="i-org">Business name</label><input id="i-org" name="org" type="text" autocomplete="organization"></div>
   <div class="field"><label class="lbl" for="i-site">Current website or social page <span class="mute">(optional)</span></label><input id="i-site" name="website" type="url" inputmode="url"></div></div>
  <div class="field"><label class="lbl" for="i-msg" id="start-msg">Your services, hours, contact info, photo/logo links, and anything else the site should say</label><textarea id="i-msg" name="message" maxlength="3000" required></textarea></div>
  <input type="hidden" name="package" id="l-package" value="">
  <input type="hidden" name="catalog_version" id="l-catalog" value="">
  <div class="pkg-note" id="pkg-note" hidden></div>
  <input type="text" name="company_fax" tabindex="-1" autocomplete="off" class="vh" aria-hidden="true">
  <button class="btn btn-gold" type="submit">Send intake to ATH {ARR}</button>
  <p class="note mt1">Used only to build your site. See <a class="gold" href="/privacy/">Privacy</a>.</p>
  <p class="form-status" role="status" aria-live="polite"></p>
 </form>
</div></section>""" + catalog_js())

pages[GC_PAGE] = (f'{GC["name"]} — a {GC["minutes"]} minute website check',
 f'{GC["tagline"]} A live check of your website on a video call you watch, then a plain list of what needs fixing. {GC_PRICE} one time.',
 f"""<section class="block" style="padding-top:56px"><div class="wrap split" style="align-items:start">
 <div><p class="eyebrow">{GC["name"]} · {GC_PRICE} one time</p><h1 class="display d-l mt1">A quick check&#8209;up<br>for your website</h1>
  <p class="lede">{html.escape(GC["tagline"])}</p>
  <p class="body mt2">{html.escape(GC["summary"])}</p>
  <div class="ctas">{btn(GC_CTA, GC_HREF, attrs='rel="noopener"' if GC_PAY else "")}{btn("What we check", "#checks", "line")}</div>
  <div class="panel panel-pad mt2"><p class="panel-title">Private, and you watch it all</p><ul class="pkg-list">{"".join(f"<li>{html.escape(x.strip()[:1].upper() + x.strip()[1:].rstrip('.'))}.</li>" for x in GC["privacy"].split(";"))}</ul></div></div>
 <div class="panel panel-pad" id="checks"><p class="panel-title">What we check</p><ul class="vs-list">{"".join(vs_line(c) for c in GC["checks"])}</ul>
  <p class="body mt2 mb0">Then we break it down: what needs fixing, and what doesn't. {html.escape(GC["fixes_note"])}</p></div>
</div></section>
<section class="block" id="how"><div class="wrap">
 <div class="block-head"><div><p class="eyebrow">How it works</p><h2 class="display d-m mt1">Pull in, check,<br>drive off</h2></div></div>
 <ol class="steps">{"".join(f'<li><span class="st-n">0{n}</span><b>{html.escape(t)}</b></li>' for n, t in enumerate(GC["how"], 1))}</ol>
 <p class="note mt2">{html.escape(GC["monthly"]["note"])} <a class="gold" href="/contact/?intent=services">Ask about it</a></p>
</div></section>
<section class="block" id="book"><div class="wrap split" style="align-items:start">
 <div><p class="eyebrow">{"Prefer to pick a time first?" if GC_PAY else "Book a Garden Check"}</p><h2 class="display d-m mt1">Pick a time</h2>
  <p class="body mt1">{"Pay by card above, or send a time here and ATH replies with your call link." if GC_PAY else f"Send your website and a time that works. ATH confirms your call and how to pay the {GC_PRICE} before the check starts. Nothing is charged by this form."}</p></div>
 <form class="panel panel-pad" id="lead-form" novalidate>
  <input type="hidden" name="intent" value="garden-check">
  <div class="grid g2"><div class="field"><label class="lbl" for="g-name">Your name</label><input id="g-name" name="name" type="text" autocomplete="name" required></div>
   <div class="field"><label class="lbl" for="g-email">Email</label><input id="g-email" name="email" type="email" autocomplete="email" required></div></div>
  <div class="grid g2"><div class="field"><label class="lbl" for="g-site">Your website address</label><input id="g-site" name="website" type="url" inputmode="url" autocomplete="url" required></div>
   <div class="field"><label class="lbl" for="g-phone">Phone <span class="mute">(optional)</span></label><input id="g-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" maxlength="40"></div></div>
  <div class="grid g2"><div class="field"><label class="lbl" for="g-org">Business name <span class="mute">(optional)</span></label><input id="g-org" name="org" type="text" autocomplete="organization"></div>
   <div class="field"><label class="lbl" for="g-call">Video call</label><select id="g-call" name="interest"><option>Zoom</option><option>Google Meet</option><option>Either is fine</option></select></div></div>
  <div class="grid g2"><div class="field"><label class="lbl" for="g-day">Day</label><input id="g-day" name="call_date" type="date"></div>
   <div class="field"><label class="lbl" for="g-time">Time</label><select id="g-time" name="call_time"><option value="">Any time</option>{"".join(f"<option>{h}:{m} {ap}</option>" for h, ap in [(9, "AM"), (10, "AM"), (11, "AM"), (12, "PM"), (1, "PM"), (2, "PM"), (3, "PM"), (4, "PM"), (5, "PM"), (6, "PM")] for m in ("00", "30"))}</select></div></div>
  <div class="field"><label class="lbl" for="g-msg">Anything you want us to look at first? <span class="mute">(optional)</span></label><textarea id="g-msg" name="message" maxlength="3000"></textarea></div>
  <input type="hidden" name="tz" id="g-tz" value="">
  <script>try{{document.getElementById("g-tz").value=Intl.DateTimeFormat().resolvedOptions().timeZone;document.getElementById("g-day").min=new Date().toISOString().slice(0,10);}}catch(e){{}}</script>
  <input type="hidden" name="package" id="l-package" value="{GC["id"]}">
  <input type="hidden" name="catalog_version" id="l-catalog" value="">
  <div class="pkg-note" id="pkg-note" hidden></div>
  <input type="text" name="company_fax" tabindex="-1" autocomplete="off" class="vh" aria-hidden="true">
  <button class="btn btn-gold" type="submit">Book my Garden Check {ARR}</button>
  <p class="note mt1">We never ask for passwords. We use this only to set up your check. See <a class="gold" href="/privacy/">Privacy</a>.</p>
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
<p>Effective October 7, 2026; packages section added October 13, 2026; World Pass app tiers updated October 24, 2026. These terms cover use of abovethehilldev.online, operated by Above the Hill Developments Inc. ("ATH").</p>
<h2>The free diagnostic</h2><p>ATHOS reports what it observed on one public page, what it infers from that, and what it cannot know. It is informational, not a guarantee of results. Where evidence is missing, the result says "unknown".</p>
<h2>Ownership</h2><ul>
<li>You own your materials. A diagnostic or deep diagnostic transfers no ownership of your code, content or data to ATH.</li>
<li>ATH owns ATH intellectual property — including ATHOS, its methods, the ATH Builder Dictionary, product designs and inventions. Purchasing the Dictionary or any product licenses its use; it does not transfer ownership of ATH inventions.</li></ul>
<h2>Deep diagnostics and services</h2><p>Deeper inspection happens only under a written scope you approve, with access you grant and may revoke. Default posture is read-only; ATH does not modify your systems during a diagnostic. Services are delivered under a separate scope and quote.</p>
<h2>Website and app packages</h2><p>Package prices are listed on the <a class="gold" href="/pricing/">Prices page</a>. Submitting a package request creates no charge and no obligation. ATH replies with a written scope and an invoice; work begins only after you approve the scope and pay. Timeline, revisions, ownership terms, third-party costs and refund terms are stated in that written scope. Ecosystem extras described as “not active yet” are delivered only once that product is operational, and no subscription renews without your separate consent.</p>
<h2>Prices and availability</h2><p>Only products marked available can be bought. Waitlists and access requests create no obligation for either side. The World Pass is a $20-a-month plan: it includes the Premium tier of one app you choose and the Basic tier of every other app, which each app switches on from your pass; it does not include the Premium or Pro tier of every app, ATH services or third-party costs unless stated in writing.</p>
<h2>Contact</h2><p>Questions: use the <a class="gold" href="/contact/">contact form</a>, or call or text <a class="gold" href="tel:+19189600164">(918) 960-0164</a>.</p>
</div></section>""")

pages["/404/"] = ("This path doesn't exist yet — ATH", "Page not found.",
 hero("path", "404", "This path doesn't<br>exist yet", "But the way over is still here.",
      btn("What's your hill?", "/diagnose/") + btn("Home", "/", "line"), size="d-m"))

# ---------------------------------------------------------------- city pages: be findable for owners already searching (Myron: make yourself findable)
# Websites (one time) come from the price book; no card checkout until the Founder creates their Stripe prices.
WEB_STARTER, WEB_BUSINESS = P["website-starter"], P["website-business"]
WEB_BOOK = "/contact/?intent=services&amp;package=website-starter"
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
    return (f"Websites for {who} in {city}, OK — {site_price('website-starter')}, one time | Above the Hill",
     f"{payoff}. A mobile website for {who} in {city}, Oklahoma: {site_price('website-starter')}, one time, go-live date confirmed with you. Local team, no contract.",
     f"""<section class="block" style="padding-top:56px"><div class="wrap split" style="align-items:start">
 <div><p class="eyebrow">{city}, Oklahoma · local team</p><h1 class="display d-l mt1">{payoff}.</h1>
  <p class="lede">{line}</p>
  <ul class="pkg-list mt2"><li><b>What you get:</b> {gets}</li><li><b>How soon:</b> a 5-minute form, then ATH confirms your go-live date</li><li><b>Price:</b> {site_price('website-starter')}, one time, no contract, no monthly fee. Up to 5 pages, linked to the booking or ordering you already use, with a year of small updates: {site_price('website-business')}. Or get your site inside an ATH plan, from $100 a month.</li></ul>
  <div class="ctas mt2">{btn("Book a call", WEB_BOOK)}{btn("See every price", "/pricing/", "line")}</div>
  <p class="body mt2">Not ready? <a class="gold" href="/free-look/">Get a free look</a> at what your site could be, or <a class="gold" href="/sites/">open the sample sites</a> on your phone.</p></div>
 <div class="panel panel-pad"><p class="eyebrow">Why it works</p><h2 class="display d-m mt1">People are already searching</h2>
  <p class="body">Before they call, customers in {city} Google you to check your hours, prices and reviews. If all they find is a social page, they find less than you offer. A real site gives the people already looking something better to find. Search engines list it once it is on your own domain (about $12 a year, paid to the registrar).</p>
  <h3 class="mt2">What you stop doing</h3><p class="body">Answering "what are your hours?" in DMs, and losing customers who can't find you at night.</p>
  <h3 class="mt2">More in {city}</h3><ul class="pkg-list">{others}</ul></div>
</div></section>""")
for cslug, city in CITIES:
    for n in NICHES: pages[f"/websites/{cslug}/{n[0]}/"] = city_page(cslug, city, n)
pages["/websites/"] = ("Websites for local businesses in Tulsa, Broken Arrow and Bixby | Above the Hill",
 f"Websites for {site_price('website-starter')}, one time for barbers, salons, restaurants, bakeries, auto shops, cleaners and small businesses in Tulsa, Broken Arrow and Bixby, Oklahoma.",
 f"""<section class="block" style="padding-top:56px"><div class="wrap"><p class="eyebrow">Local · Tulsa area</p><h1 class="display d-l mt1">A website for the customers<br>already looking for you</h1>
 <p class="lede">{site_price('website-starter')}, one time, go-live date confirmed with you. Pick your town and your kind of business.</p>
 <div class="grid g3 mt2">""" + "".join(f'<div class="panel panel-pad"><h2 class="display d-m">{city}</h2><ul class="pkg-list">' + "".join(f'<li><a class="gold" href="/websites/{cslug}/{n[0]}/">{n[1].capitalize()}</a></li>' for n in NICHES) + "</ul></div>" for cslug, city in CITIES) + f"""</div>
 <div class="ctas mt2">{btn("Book a call", WEB_BOOK)}{btn("Get a free look", "/free-look/", "line")}</div></div></section>""")

SECTION_H2 = {"/build/": "Service families", "/language/": "What the dictionary includes", "/passport/": "Membership tiers", "/report/": "What a Hill Report contains", "/work/": "ATH inventions"}

# ---------------------------------------------------------------- revenue front door (MASTER-12HR-SHIFT 2026-10-30 §5 + §6)
# Industry pages + Consequence Calculator + Free Business Diagnosis.
# Prices below come from THE price book (commercial/price-book.json, Founder direction 2026-10-31): one 15-step ladder,
# $100 → $8,000 a month, and the standalone services apart from it. athos-brain spaid-skills.mjs PRICE_BOOK and the
# PowerTribes pt_tiers table carry the same book.
# Rules: no trial offers, no free months, no discounts, no review gating, no fake proof, no guaranteed results.
SVC_GROUPS = ("AI services (monthly, one location)", "Websites (one time)")
SVC_FINE = [
    f"Prices as of {PB['as_of']}. Every install starts with a written scope; nothing is charged on this page.",
    "There is no trial offer and no free month. The receptionist pilot is a paid pilot. No discounts.",
    "Missed-call text-back and reactivation texts are set up inside Speed-to-Lead or the Receptionist; anything extra is quoted in your scope.",
    "Results depend on your leads, your team and your market. ATH does not guarantee bookings, sales or revenue.",
    "Any third-party costs (phone numbers, messaging fees, software you already use) are listed in your scope before you pay.",
]
def ladder_panel(): return plan_table()
def svc_table():
    rows = "".join(
        f'<div class="rv-row" data-svc="{i["id"]}"><span><b>{html.escape(i["name"])}</b><span class="note">{html.escape(i["what"])}</span></span><span class="rv-price">{html.escape(GC_PRICE + " one time" if i["id"] == "garden-check" else i["price"])}</span></div>'
        for g in SERVICES if g["group"] in SVC_GROUPS for i in g["items"] if i["id"] != "garden-check")
    fine = "".join(f"<li>{html.escape(f)}</li>" for f in SVC_FINE)
    return f"""<div class="panel panel-pad" id="prices"><p class="panel-title">Services on their own · not part of a plan</p><div class="rv-table">{rows}</div>
 <ul class="pkg-list mt2 rv-fine">{fine}</ul><p class="note mb0"><a class="gold" href="/pricing/#services">Every service and price</a></p></div>"""

DIAG_HREF = "/business-diagnosis/"
def diag_btn(ind=""):
    return btn("Request a free business diagnosis", DIAG_HREF + (f"?industry={ind}" if ind else ""))

INDUSTRIES = [
    {
        "slug": "dental", "name": "Dental practices", "short": "Dental",
        "title": "Dental practices — answer every call, fill every chair",
        "desc": "AI receptionist, missed-call text-back, speed-to-lead, review requests and patient reactivation for dental practices. Working prices, written scope, no trial offers.",
        "h1": "Every unanswered call<br>is a patient who<br>calls the next office",
        "lede": "Your front desk is checking someone in, on another line, or at lunch. The phone rings out. A new patient doesn't leave a voicemail; they try the next practice on the list.",
        "problems": [
            ("Missed calls", "Calls during procedures, lunch and after hours go to voicemail, and many callers never leave one."),
            ("Slow follow-up", "Web and ad inquiries wait until someone has a free minute. By then the patient has booked somewhere else."),
            ("No easy booking", "Patients who want to book at 9 PM have no way to start except calling back tomorrow."),
            ("Lapsed recall", "Patients overdue for cleanings sit in your system with no reminder that reaches them."),
            ("Reviews by chance", "Reviews get asked for when someone remembers, so your profile doesn't reflect how many patients you serve."),
        ],
        "does": [
            ("AI receptionist", "Answers when the desk can't, handles scheduling and general questions (hours, location, insurance accepted, new-patient steps), and books or takes a message. It does not give clinical advice."),
            ("Missed-call text-back", "A caller who hangs up gets an automatic text back from your practice number, so the conversation keeps going."),
            ("Speed-to-lead", "Form and ad inquiries get an immediate reply and a handoff to your team."),
            ("Review requests, no gating", "Every patient gets the same review request after a visit. We never screen out unhappy patients."),
            ("Recall reactivation", "Overdue patients you choose get a friendly reminder to book."),
            ("Website", "A mobile site with one clear call and booking path."),
        ],
        "note": "<b>Patient privacy.</b> ATH does not claim HIPAA compliance on this page. Before any dental install we map exactly what patient information each system would see, keep clinical details out of automated messages, and confirm with you whether a Business Associate Agreement is needed with ATH or any vendor involved. If it can't be done the right way for your practice, we say so in the scope.",
    },
    {
        "slug": "home-services", "name": "Home services", "short": "Home services",
        "title": "Home services — the first to call back gets the job",
        "desc": "Missed-call text-back, speed-to-lead, AI receptionist, review requests and past-customer reactivation for HVAC, plumbing, roofing, lawn, cleaning and other home-service businesses.",
        "h1": "You're on a roof.<br>The phone rings.<br>The job goes to someone else.",
        "lede": "Many homeowners call more than one company and hire whoever answers first. When you're on a job, the call you can't take is often the job you don't get.",
        "problems": [
            ("Missed calls on the job", "You can't answer from a crawlspace or a ladder, and callers rarely wait for a callback."),
            ("Quote requests go cold", "Form fills and ad leads sit for hours before anyone replies."),
            ("No booking path", "Customers who'd book an estimate tonight can't, so they keep shopping."),
            ("Past customers forget you", "Seasonal tune-ups and repeat work go to whoever reminds them first."),
            ("Few reviews", "Great jobs don't turn into reviews unless someone asks every time."),
        ],
        "does": [
            ("Missed-call text-back", "Every missed call gets a text from your business number so the customer knows you saw it."),
            ("Speed-to-lead", "Web and ad leads get an immediate reply, the job details are collected, and your team gets the handoff."),
            ("AI receptionist", "Answers calls while you work, collects the address and the problem, and books estimates into the calendar you use."),
            ("Review requests, no gating", "Every customer gets asked after the job, not just the happy ones."),
            ("Reactivation", "Past customers get a seasonal reminder you approve."),
            ("Website", "A mobile site with your service area, your services, and a call button that works."),
        ],
    },
    {
        "slug": "local-business", "name": "Local businesses", "short": "Local business",
        "title": "Local businesses — stop losing customers between hello and booked",
        "desc": "Websites, missed-call text-back, speed-to-lead, review requests and reactivation for salons, restaurants, shops, studios and other local businesses.",
        "h1": "Customers are<br>trying to reach you.<br>Some never get through.",
        "lede": "You're serving the customer in front of you while the phone rings, the DMs pile up, and the website still shows last year's hours.",
        "problems": [
            ("Missed calls", "The phone rings while you're with a customer, and the caller moves on."),
            ("Slow replies", "Messages and form fills get answered at the end of the day, or not at all."),
            ("No booking", "People who want to book after hours have nowhere to go."),
            ("Out-of-date website", "Old hours, missing services, no clear way to call or book."),
            ("Regulars drift", "Customers who used to come weekly stop, and nobody notices."),
        ],
        "does": [
            ("Website", "Starter or Business site: mobile first, your hours, services, photos and one clear next step."),
            ("Missed-call text-back", "Missed callers get a text back so the conversation keeps going."),
            ("Speed-to-lead", "New inquiries get an instant, friendly reply and land with you."),
            ("Review requests, no gating", "Every customer is asked the same way. No filtering out the unhappy ones."),
            ("Reactivation", "Customers who haven't been back get a message you approve."),
            ("AI receptionist", "For busy phones: answers, books and takes messages when you can't."),
        ],
    },
    {
        "slug": "sales-organizations", "name": "Sales organizations", "short": "Sales orgs",
        "title": "Sales organizations — you paid for the lead; make it count",
        "desc": "Speed-to-lead, AI appointment setting, reactivation of aged leads and show-rate follow-up for sales teams that buy or generate leads.",
        "h1": "You paid for the lead.<br>Then nobody<br>called it for hours.",
        "lede": "Many sales teams don't have a lead problem. They have a contact problem: leads called late, called once, and never called again.",
        "problems": [
            ("Slow first contact", "Leads land in the CRM and wait until a rep is free."),
            ("Low contact rate", "One or two attempts, then the lead is marked dead."),
            ("No-shows", "Appointments get set and no one confirms them, so the calendar looks full and the room is empty."),
            ("Aged leads ignored", "Thousands of old leads you already paid for never get another touch."),
            ("No idea where it leaks", "Cost per lead is tracked. Cost per contact, appointment and customer usually isn't."),
        ],
        "does": [
            ("Speed-to-lead", "Every new lead gets an immediate text or call, then routes to the next available rep."),
            ("AI appointment setting", "The receptionist qualifies, answers common questions and books onto rep calendars."),
            ("Confirmation and show-rate follow-up", "Booked appointments get reminders and an easy reschedule path."),
            ("Aged-lead reactivation", "Compliant re-engagement of leads you already own, with opt-outs honored."),
            ("Review requests, no gating", "Closed customers get asked for an honest review."),
            ("The numbers", "Start with the Consequence Calculator: see your cost per contact, per appointment and per customer."),
        ],
        "note": "<b>Compliance.</b> Calls and texts to leads must follow consent and opt-out rules (TCPA, carrier rules and your state's laws). ATH sets up opt-outs on every flow and asks how your leads gave consent before anything is switched on. Call recording happens only with consent.",
    },
    {
        "slug": "creators", "name": "Creators", "short": "Creators",
        "title": "Creators — turn attention into booked work",
        "desc": "Websites, inquiry follow-up, missed-call text-back and honest testimonial requests for creators, coaches and personal brands. WAVEMOTION plans for clips.",
        "h1": "The views are there.<br>The bookings<br>aren't.",
        "lede": "Brand deals, coaching calls and bookings come in through DMs, email and a link in bio. The ones you don't answer fast enough go to someone else.",
        "problems": [
            ("Inquiries buried in DMs", "Paid opportunities sit under hundreds of comments and messages."),
            ("Slow follow-up", "A brand or client who doesn't hear back in a day moves on."),
            ("No booking path", "Your link in bio doesn't take anyone to a clear offer and a time to book."),
            ("No home base", "Your business lives on platforms you don't control."),
            ("Testimonials by accident", "Happy clients rarely leave a review unless asked."),
        ],
        "does": [
            ("Website", "A home base you own with your offers, media kit and a clear book-me button."),
            ("Speed-to-lead", "Inquiries from your site and forms get an instant reply and land in one place."),
            ("Missed-call text-back", "For your business line: missed callers get a text back."),
            ("Review and testimonial requests", "Every client is asked the same way, and nothing is published without their permission."),
            ("Clips", "Short-form clips come with WAVEMOTION plans from $10 a month at wavemotion.live."),
            ("AI receptionist", "For coaches and service creators with a busy phone line."),
        ],
    },
]

def industry_page(ind):
    probs = "".join(f'<div class="panel panel-pad card"><h3 style="margin-top:0">{t}</h3><p>{d}</p></div>' for t, d in ind["problems"])
    does = "".join(f'<li><b>{t}.</b> {d}</li>' for t, d in ind["does"])
    note = f'<div class="panel panel-pad mt2 rv-note"><p class="body mb0">{ind["note"]}</p></div>' if ind.get("note") else ""
    others = " · ".join(f'<a class="gold" href="/industries/{o["slug"]}/">{o["short"]}</a>' for o in INDUSTRIES if o["slug"] != ind["slug"])
    body = f"""<section class="block" style="padding-top:56px"><div class="wrap">
 <p class="eyebrow">ATH for {ind["name"].lower()}</p>
 <h1 class="display d-l mt1">{ind["h1"]}</h1>
 <p class="lede">{ind["lede"]}</p>
 <div class="ctas mt2">{diag_btn(ind["slug"])}{btn("Run the Consequence Calculator", "/consequence-calculator/", "line")}</div>
</div></section>
<section class="block" style="padding-top:12px"><div class="wrap">
 <h2 class="display d-m">The real problem</h2>
 <div class="grid g3 mt2">{probs}</div>
</div></section>
<section class="block"><div class="wrap split" style="align-items:start">
 <div><h2 class="display d-m">What ATH does</h2>
  <ul class="pkg-list mt2 rv-does">{does}</ul>{note}</div>
 {svc_table()}
</div></section>
<section class="block" style="padding-top:0"><div class="wrap">{ladder_panel()}</div></section>
<section class="block"><div class="wrap"><div class="panel panel-pad rv-cta">
 <div><p class="eyebrow">Start here</p><h2 class="display d-m mt1">Request a free business diagnosis</h2>
  <p class="body mt1 mb0">Tell us how customers reach you today. A person at ATH looks at where calls and leads are slipping and replies with a plain diagnosis and a written scope. No obligation, nothing charged.</p></div>
 <div class="ctas" style="margin:0">{diag_btn(ind["slug"])}</div>
</div>
<p class="note mt2">Other industries: {others} · <a class="gold" href="/industries/">All industries</a></p></div></section>"""
    return (ind["title"] + " | Above the Hill", ind["desc"], body)

for _ind in INDUSTRIES:
    pages[f'/industries/{_ind["slug"]}/'] = industry_page(_ind)

pages["/industries/"] = ("Industries — Above the Hill Developments",
 "How ATH helps dental practices, home-service companies, local businesses, sales organizations and creators stop losing customers to missed calls and slow follow-up.",
 f"""<section class="block" style="padding-top:56px"><div class="wrap">
 <p class="eyebrow">Who we help</p><h1 class="display d-l mt1">Stop losing customers<br>between hello and booked</h1>
 <p class="lede">Missed calls, slow follow-up and no way to book. The leak looks different in every industry. Pick yours.</p>
 <div class="grid g3 mt2">{"".join(f'<a class="panel panel-pad card rv-ind" href="/industries/{i["slug"]}/"><h3 style="margin-top:0">{i["name"]}</h3><p>{i["problems"][0][1]}</p><span class="gold mt1" style="display:inline-block">See how ATH helps {ARR}</span></a>' for i in INDUSTRIES)}
  <a class="panel panel-pad card rv-ind" href="/consequence-calculator/"><h3 style="margin-top:0">Consequence Calculator</h3><p>Put in your own numbers and see your cost per contact, per appointment and per customer.</p><span class="gold mt1" style="display:inline-block">Run the numbers {ARR}</span></a>
 </div>
</div></section>
<section class="block" style="padding-top:12px"><div class="wrap">{svc_table()}{ladder_panel()}</div></section>
<section class="block"><div class="wrap"><div class="panel panel-pad rv-cta"><div><h2 class="display d-m">Not sure where you leak?</h2><p class="body mt1 mb0">That's what the diagnosis is for.</p></div><div class="ctas" style="margin:0">{diag_btn()}</div></div></div></section>""")

# ---------------------------------------------------------------- Consequence Calculator (§6: cost per contact = cost per lead ÷ contact rate)
CALC_FIELDS = [
    # (id, label, unit, default, min, max, step, hint)
    ("cpl", "Cost per lead", "$", 50, 0, 100000, "any", "What you pay, on average, for one lead."),
    ("leads", "Leads per month", "#", 100, 0, 1000000, 1, "New leads, calls or inquiries in a typical month."),
    ("contact", "Contact rate", "%", 50, 0, 100, "any", "Out of 100 leads, how many do you actually talk to?"),
    ("book", "Booking rate", "%", 40, 0, 100, "any", "Out of 100 people you talk to, how many book an appointment?"),
    ("show", "Show rate", "%", 70, 0, 100, "any", "Out of 100 booked, how many show up?"),
    ("close", "Close rate", "%", 30, 0, 100, "any", "Out of 100 who show, how many buy?"),
    ("value", "Average sale value", "$", 1000, 0, 100000000, "any", "What one new customer is worth to you (first sale)."),
]

def calc_field(fid, label, unit, dv, mn, mx, step, hint):
    pre = '<span class="rv-unit">$</span>' if unit == "$" else ""
    post = '<span class="rv-unit">%</span>' if unit == "%" else ""
    return f"""<div class="field"><label class="lbl" for="c-{fid}">{label}</label>
  <div class="rv-in">{pre}<input id="c-{fid}" name="{fid}" type="number" inputmode="decimal" min="{mn}" max="{mx}" step="{step}" value="{dv}" aria-describedby="c-{fid}-h">{post}</div>
  <p class="note mb0" id="c-{fid}-h">{hint}</p></div>"""

CALC_JS = r"""<script>
(() => {
  const f = document.getElementById("calc-form"); if (!f) return;
  const v = (id) => { const n = parseFloat(f.elements[id].value); return isFinite(n) && n >= 0 ? n : 0; };
  const usd = (n) => isFinite(n) ? "$" + n.toLocaleString("en-US", { maximumFractionDigits: n < 100 ? 2 : 0, minimumFractionDigits: n < 100 ? 2 : 0 }) : "—";
  const num = (n) => isFinite(n) ? n.toLocaleString("en-US", { maximumFractionDigits: 1 }) : "—";
  const out = (id, t) => { const e = document.getElementById(id); if (e) e.textContent = t; };
  function run() {
    const cpl = v("cpl"), L = v("leads"), V = v("value");
    const cr = Math.min(v("contact"), 100) / 100, br = Math.min(v("book"), 100) / 100, sr = Math.min(v("show"), 100) / 100, kr = Math.min(v("close"), 100) / 100;
    const spend = cpl * L, contacts = L * cr, appts = contacts * br, shows = appts * sr, customers = shows * kr;
    const perContact = cr > 0 ? cpl / cr : Infinity;
    const perAppt = cr * br > 0 ? cpl / (cr * br) : Infinity;
    const perCust = cr * br * sr * kr > 0 ? cpl / (cr * br * sr * kr) : Infinity;
    // Leak: revenue each stage's drop-off would have produced at YOUR downstream rates (one stage fixed at a time, others unchanged).
    const leakContact = L * (1 - cr) * br * sr * kr * V;
    const leakBook = L * cr * (1 - br) * sr * kr * V;
    const leakShow = L * cr * br * (1 - sr) * kr * V;
    const leak = leakContact + leakBook + leakShow;
    out("o-spend", usd(spend)); out("o-contact", usd(perContact)); out("o-appt", usd(perAppt)); out("o-cust", usd(perCust));
    out("o-leak", usd(leak)); out("o-l-contact", usd(leakContact)); out("o-l-book", usd(leakBook)); out("o-l-show", usd(leakShow));
    out("o-n-contacts", num(contacts)); out("o-n-appts", num(appts)); out("o-n-shows", num(shows)); out("o-n-cust", num(customers)); out("o-rev", usd(customers * V));
    const summary = `cost/lead ${usd(cpl)}, leads/mo ${num(L)}, contact ${num(cr * 100)}%, booking ${num(br * 100)}%, show ${num(sr * 100)}%, close ${num(kr * 100)}%, avg sale ${usd(V)} → est. cost/contact ${usd(perContact)}, cost/appointment ${usd(perAppt)}, cost/customer ${usd(perCust)}, est. monthly leak ${usd(leak)}`;
    try { sessionStorage.setItem("ath_calc", summary); } catch {}
  }
  f.addEventListener("input", run); f.addEventListener("submit", (e) => { e.preventDefault(); run(); });
  run();
})();
</script>"""

pages["/consequence-calculator/"] = ("Consequence Calculator — what missed contact costs you | Above the Hill",
 "Enter your cost per lead, contact, booking, show and close rates and average sale. See your estimated cost per contact, per appointment, per customer, and your estimated monthly leak.",
 f"""<section class="block" style="padding-top:56px"><div class="wrap">
 <p class="eyebrow">Consequence Calculator</p><h1 class="display d-l mt1">What does a lead<br>you never reach<br>really cost?</h1>
 <p class="lede">Cost per lead is the number everyone tracks. Cost per contact is the one that hurts: <b>cost per lead ÷ contact rate</b>. Put in your own numbers.</p>
</div></section>
<section class="block" style="padding-top:8px"><div class="wrap split rv-calc" style="align-items:start">
 <form class="panel panel-pad" id="calc-form" novalidate aria-describedby="calc-ex">
  <p class="panel-title">Your numbers</p>
  <p class="note" id="calc-ex">The starting values are example numbers only. Replace them with yours; everything updates as you type. Nothing you enter leaves this page.</p>
  <div class="grid g2">{"".join(calc_field(*c) for c in CALC_FIELDS)}</div>
 </form>
 <div class="panel panel-pad rv-out" aria-live="polite">
  <p class="panel-title">Estimates from your inputs</p>
  <div class="rv-kpis">
   <div class="rv-kpi"><span class="lbl">Est. cost per contact</span><b id="o-contact">—</b></div>
   <div class="rv-kpi"><span class="lbl">Est. cost per appointment</span><b id="o-appt">—</b></div>
   <div class="rv-kpi"><span class="lbl">Est. cost per customer</span><b id="o-cust">—</b></div>
   <div class="rv-kpi rv-leak"><span class="lbl">Est. monthly leak</span><b id="o-leak">—</b></div>
  </div>
  <div class="rv-table mt2">
   <div class="rv-row"><span>Monthly lead spend</span><span class="rv-price" id="o-spend">—</span></div>
   <div class="rv-row"><span>People reached · booked · showed · bought</span><span class="rv-price"><span id="o-n-contacts">—</span> · <span id="o-n-appts">—</span> · <span id="o-n-shows">—</span> · <span id="o-n-cust">—</span></span></div>
   <div class="rv-row"><span>Est. revenue at your current rates</span><span class="rv-price" id="o-rev">—</span></div>
   <div class="rv-row"><span>Leak · leads never reached</span><span class="rv-price" id="o-l-contact">—</span></div>
   <div class="rv-row"><span>Leak · reached, never booked</span><span class="rv-price" id="o-l-book">—</span></div>
   <div class="rv-row"><span>Leak · booked, didn't show</span><span class="rv-price" id="o-l-show">—</span></div>
  </div>
  <details class="mt2"><summary class="gold">How these estimates are calculated</summary>
   <ul class="pkg-list mt1">
    <li>Cost per contact = cost per lead ÷ contact rate.</li>
    <li>Cost per appointment = cost per lead ÷ (contact rate × booking rate).</li>
    <li>Cost per customer = cost per lead ÷ (contact rate × booking rate × show rate × close rate).</li>
    <li>Each leak line is the revenue that stage's drop-off would have produced if it had continued at <i>your own</i> later-stage rates, one stage at a time. The monthly leak is the sum of the three. Your close rate is left as you entered it.</li>
    <li>These are estimates from the numbers you typed, not a forecast and not a promise of what ATH will recover. Real results depend on your leads, team and market.</li>
   </ul></details>
  <div class="ctas mt2">{diag_btn()}</div>
  <p class="note mb0">If you request a diagnosis in this browser tab, you can choose to attach these numbers to your request.</p>
 </div>
</div></section>
<section class="block" style="padding-top:0"><div class="wrap"><h2 class="display d-m">What fixing it costs</h2>
 <p class="body mt1">Compare your estimated monthly leak with the membership that closes it. The diagnosis tells you which level fits; nothing is charged on this page.</p>{ladder_panel()}{svc_table()}</div></section>""" + CALC_JS)

# ---------------------------------------------------------------- Free Business Diagnosis → the existing public ATHOS lead intake (POST /api/lead)
DIAG_IND = [("dental", "Dental practice"), ("home-services", "Home services"), ("local-business", "Local business"), ("sales-organizations", "Sales organization"), ("creators", "Creator / personal brand"), ("other", "Something else")]
DIAG_REACH = ["Phone calls", "Website forms", "Paid ads", "Social media DMs", "Walk-ins", "Referrals", "Bought or shared leads"]
DIAG_HAPPEN = ["Calls get missed", "Leads wait too long for a reply", "No way to book after hours", "Appointments don't show", "Few or old reviews", "Old leads and past customers never followed up", "Website is out of date or missing"]
def chk_group(name, q, items):
    boxes = "".join(f'<label class="check"><input type="checkbox" name="{name}" value="{html.escape(i)}"> <span>{html.escape(i)}</span></label>' for i in items)
    return f'<fieldset class="field rv-fs" data-q="{q}" data-group="{name}"><legend class="lbl">{q}</legend><div class="rv-checks">{boxes}</div></fieldset>'

pages[DIAG_HREF] = ("Request a free business diagnosis | Above the Hill",
 "Tell ATH how customers reach you. A person reviews where calls and leads slip and replies with a plain diagnosis and a written scope. No obligation, nothing charged.",
 f"""<section class="block" style="padding-top:56px"><div class="wrap split" style="align-items:start">
 <div><p class="eyebrow">Free · no obligation</p><h1 class="display d-l mt1">Request a free<br>business diagnosis</h1>
  <p class="lede">Tell us how customers reach you today. A person at ATH finds where calls and leads slip away and replies with a plain answer.</p>
  <ol class="pkg-list mt2 rv-steps"><li><b>You send this form.</b> It goes straight to ATH's lead desk.</li><li><b>A person reviews it</b> and contacts you to book a short call.</li><li><b>You get a written diagnosis and scope</b> with the working price. Nothing is charged unless you approve it and pay through the link in your scope.</li><li><b>Onboarding</b> starts after payment.</li></ol>
  <p class="body mt2">Want the numbers first? <a class="gold" href="/consequence-calculator/">Run the Consequence Calculator</a>.</p>
  <p class="body">Prefer to talk? <a class="gold" href="tel:+19189600164">Call or text (918) 960-0164</a>.</p></div>
 <form class="panel panel-pad" id="lead-form" data-compose novalidate>
  <input type="hidden" name="intent" value="business-diagnosis">
  <div class="grid g2"><div class="field"><label class="lbl" for="d-name">Your name</label><input id="d-name" name="name" type="text" autocomplete="name" required></div>
   <div class="field"><label class="lbl" for="d-email">Email</label><input id="d-email" name="email" type="email" autocomplete="email" required></div></div>
  <div class="grid g2"><div class="field"><label class="lbl" for="d-phone">Phone <span class="mute">(optional)</span></label><input id="d-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" maxlength="40"></div>
   <div class="field"><label class="lbl" for="d-org">Business name and city</label><input id="d-org" name="org" type="text" autocomplete="organization"></div></div>
  <div class="grid g2"><div class="field"><label class="lbl" for="d-ind">Industry</label><select id="d-ind" name="interest" data-q="Industry">{"".join(f'<option value="{v}">{l}</option>' for v, l in DIAG_IND)}</select></div>
   <div class="field"><label class="lbl" for="d-site">Website <span class="mute">(optional)</span></label><input id="d-site" name="website" type="url" inputmode="url"></div></div>
  <div class="grid g2"><div class="field"><label class="lbl" for="d-leads">About how many leads or calls a month?</label><select id="d-leads" name="leads_band" data-q="Leads or calls per month"><option value="">Not sure</option><option>Under 50</option><option>50–200</option><option>200–1,000</option><option>Over 1,000</option></select></div>
   <div class="field"><label class="lbl" for="d-loc">Locations</label><select id="d-loc" name="locations" data-q="Locations"><option>1</option><option>2–3</option><option>4–10</option><option>More than 10</option></select></div></div>
  {chk_group("reach", "How do new customers reach you?", DIAG_REACH)}
  {chk_group("happening", "What's happening now?", DIAG_HAPPEN)}
  <div class="field"><label class="lbl" for="d-msg">Anything else we should know? <span class="mute">(optional)</span></label><textarea id="d-msg" name="message" maxlength="2000"></textarea></div>
  <label class="check" id="d-grow-row" hidden><input type="checkbox" id="bd-grow" checked> <span>Attach my Growing with AI answers: <span class="mute" id="d-grow-sum"></span></span></label>
  <label class="check" id="d-calc-row" hidden><input type="checkbox" id="bd-calc" checked> <span>Attach my Consequence Calculator numbers: <span class="mute" id="d-calc-sum"></span></span></label>
  <input type="hidden" name="package" id="l-package" value="">
  <input type="hidden" name="catalog_version" id="l-catalog" value="">
  <div class="pkg-note" id="pkg-note" hidden></div>
  <input type="text" name="company_fax" tabindex="-1" autocomplete="off" class="vh" aria-hidden="true">
  <button class="btn btn-gold" type="submit">Request my free diagnosis {ARR}</button>
  <p class="note mt1">Nothing is charged. We use this only to reply about your business. Reply STOP to any text and we won't contact you again. Please don't include patient or medical details. See <a class="gold" href="/privacy/">Privacy</a>.</p>
  <p class="form-status" role="status" aria-live="polite"></p>
 </form>
</div></section>
<script>(() => {{
  const q = new URLSearchParams(location.search).get("industry"), s = document.getElementById("d-ind");
  if (q && s && [...s.options].some((o) => o.value === q)) s.value = q;
  let c = ""; try {{ c = sessionStorage.getItem("ath_calc") || ""; }} catch (e) {{}}
  if (c) {{ document.getElementById("d-calc-row").hidden = false; document.getElementById("d-calc-sum").textContent = c; }}
  else document.getElementById("bd-calc").checked = false;
  let g = ""; try {{ g = sessionStorage.getItem("ath_grow") || ""; }} catch (e) {{}}
  if (g) {{ document.getElementById("d-grow-row").hidden = false; document.getElementById("d-grow-sum").textContent = g; }}
  else document.getElementById("bd-grow").checked = false;
}})();</script>""" + catalog_js())


# ---------------------------------------------------------------- AI services, LIVE-CATALOG OPTION (Founder order 2026-10-31,
# option B "AI pages only"): the four IONOS-style doors on today's live catalog (registry 2026-10-24.x). A price is shown
# ONLY where the live catalog has it AND it has a working checkout link (Stripe Payment Link or the app's own live checkout).
# Everything else says "Request this service" and goes to the contact form; nothing is charged there.
# Every AI is labelled. No testimonials, no invented metrics, no trial, no free month, no discount.
SPAIDBOT_BUILD_URL = ""  # Spaidbot Build's public URL (its own domain, never workers.dev) the day it opens.
REQ_HREF = "/contact/?intent=services"
AI_NOTE = "Every ATH AI says it is an AI. A person at ATH sets it up, and your customers can always reach a person."
def live_buy(oid):
    """(price, stripe_url) for a live-catalog offer with a working card checkout, else None."""
    o = CAT.get(oid)
    if o and o["status"] == "LIVE" and re.match(r"^https://buy\.stripe\.com/[A-Za-z0-9_]+$", o.get("buy") or ""): return o["price"], o["buy"]
    return None
def pb_site(pid):
    """(name, price, pay_url or '', what) for a price-book website; the price book (commercial/price-book.json) is the one source."""
    pb = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "commercial", "price-book.json")))
    it = next(i for g in pb["services"] for i in g["items"] if i["id"] == pid)
    return it["name"], it["price"], it.get("pay_url") or "", it["what"]
SITE_S, SITE_B = pb_site("website-starter"), pb_site("website-business")
def req_btn(kind="line", label="Request this service"): return btn(label, REQ_HREF, kind)
def ai_try_chat(label="Try Spaidbot now", kind="gold"): return f'<a class="btn btn-{kind}" href="/contact/#ask" data-sb-open>{label} {ARR}</a>'
def ai_card(icon, eyebrow, name, does, price, cta_html, href):
    pr = f'<p class="mt1"><b class="outcome-price">{price}</b></p>' if price else ""
    return (f'<article class="panel panel-pad card ai-card">{ic(icon, "icon-sm")}<p class="eyebrow mt1">{eyebrow}</p><h3><a href="{href}">{name}</a></h3>'
            f'<p>{does}</p>{pr}<div class="ctas mt2">{cta_html}</div></article>')
def ai_tabs(route):
    items = [("/ai/", "All AI services"), ("/ai/receptionist/", "AI receptionist"), ("/ai/site-builder/", "AI app & site builder"),
             ("/ai/chat-assistant/", "AI chat assistant"), ("/ai/growing-with-ai/", "Growing with AI")]
    return '<nav class="ai-tabs" aria-label="ATH AI services">' + "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == route else ""}>{n}</a>' for h, n in items) + '</nav>'
def ai_head(route, eyebrow, h1, lede, ctas):
    return f"""<section class="block ai-top" style="padding-top:40px"><div class="wrap">{ai_tabs(route)}
 <p class="eyebrow mt2">{eyebrow}</p><h1 class="display d-l mt1">{h1}</h1><p class="lede">{lede}</p>
 <div class="ctas mt2">{ctas}</div><p class="note ai-label">{ic("ai", "icon-sm")} {AI_NOTE}</p></div></section>"""
def site_rows():
    rows = []
    for name, price, pay, what in (SITE_S, SITE_B):
        cta = f'<a class="btn btn-line btn-sm" href="{pay}" rel="noopener">Pay by card {ARR}</a>' if pay else f'<a class="btn btn-line btn-sm" href="{REQ_HREF}">Request it {ARR}</a>'
        rows.append(f'<div class="rv-row"><span><b>{name}</b><span class="note">{html.escape(what)}</span></span><span class="rv-price">{html.escape(price)}<span class="note">{cta}</span></span></div>')
    return "".join(rows)
REQ_NOTE = "Prices for this service are set in a written scope after a short call. Nothing is charged when you send a request."

pages["/ai/"] = ("AI services for your business — receptionist, site builder, chat assistant | Above the Hill",
 "ATH's AI services: an AI receptionist that answers and books, an AI app and site builder, the Spaidbot AI chat assistant, and Growing with AI recommendations from a short quiz. Labelled AI, a person behind every one.",
 ai_head("/ai/", "AI services · built by ATH, run on ATH's own engines", "AI that answers,<br>builds and follows up",
   "Four ways ATH puts AI to work for your business. Each one is labelled as an AI and set up by a person.",
   btn("Find what fits you", "/ai/growing-with-ai/") + ai_try_chat("Try the chat assistant", "line"))
 + f"""<section class="block" style="padding-top:8px"><div class="wrap"><h2 class="vh">The four AI services</h2><div class="grid g2 ai-grid">
 {ai_card("bolt", "Never miss a call", "AI receptionist", "Answers your phone when you can't, takes the message or books the appointment into the calendar you already use, and texts back anyone who hangs up.", "", btn("See how it works", "/ai/receptionist/") + req_btn(), "/ai/receptionist/")}
 {ai_card("site", "Get online fast", "AI app &amp; site builder", "Sketch your homepage in seconds, then get a real mobile site. Spaidbot Build, the AI builder, is being built; until it opens, ATH builds your site with you.", f'{SITE_S[0]} {html.escape(SITE_S[1])}' , btn("Sketch my site", "/ai/site-builder/"), "/ai/site-builder/")}
 {ai_card("ai", "Answer questions all day", "AI chat assistant", "Spaidbot answers questions from real prices and pages, cites what it used, says when it does not know, and hands people to a person.", "Free to try on this site", ai_try_chat("Try it now"), "/ai/chat-assistant/")}
 {ai_card("path", "Know your next step", "Growing with AI: our recommendations for you", "Answer six short questions and see which ATH services fit your business, and why.", "Free, two minutes", btn("Take the quiz", "/ai/growing-with-ai/"), "/ai/growing-with-ai/")}
</div>
<div class="panel panel-pad mt2"><p class="panel-title">The plain rules</p><ul class="pkg-list">
 <li>Every ATH AI tells people it is an AI. It never pretends to be a person.</li>
 <li>No trial, no free month and no discount. The free business diagnosis is the one free step: a person names your biggest leak.</li>
 <li>A card button appears only where checkout is open today. Everything else starts with "Request this service" and a written scope; nothing is charged when you ask.</li>
 <li>ATH does not promise bookings, sales or revenue. Results depend on your leads, your team and your market.</li>
</ul></div></div></section>""" + cta_block("Not sure where AI helps first?", "Start with the free business diagnosis. A person looks at how you answer calls, follow up and get reviews, and names the biggest leak."))

pages["/ai/receptionist/"] = ("AI receptionist — answers, books and texts back | Above the Hill",
 "ATH's AI receptionist answers calls you can't, books into the scheduling you already use, takes messages and texts back missed callers. Request it and ATH sends a written scope.",
 ai_head("/ai/receptionist/", "AI receptionist · voice AI for your phone line", "Your phone,<br>answered every time",
   "When you're with a customer, on a job or closed for the night, the AI receptionist picks up. It says it is an AI, answers common questions, books the appointment or takes a clear message, and texts you the details.",
   req_btn("gold") + diag_btn())
 + f"""<section class="block" style="padding-top:8px"><div class="wrap split" style="align-items:start">
 <div><h2 class="display d-m">What it does</h2><ul class="pkg-list mt2">
  <li><b>Answers when you can't.</b> During jobs, lunch, busy hours and after hours.</li>
  <li><b>Books into what you already use.</b> Your calendar or booking tool stays the same.</li>
  <li><b>Takes a clear message.</b> Name, number, what they need and how urgent, sent to you by text.</li>
  <li><b>Texts back missed callers</b> from your business number so the conversation keeps going.</li>
  <li><b>Hands off to a person.</b> Anything it can't handle goes to you or your team, with the notes.</li></ul>
  <h2 class="display d-m mt2">What it won't do</h2><ul class="pkg-list mt2">
  <li>Pretend to be a person. It says it is an AI.</li><li>Give medical, legal or financial advice.</li>
  <li>Record a call without consent, or text people who haven't agreed to it. Opt-outs work on every flow.</li></ul></div>
 <div class="panel panel-pad"><p class="panel-title">How to start</p><ol class="pkg-list"><li>Request the service, or the free business diagnosis.</li><li>A person at ATH calls you and maps how your phone is answered today.</li><li>You get a written scope with the price before anything is charged.</li></ol>
  <div class="ctas mt2">{req_btn("gold")}</div><p class="note mb0">{REQ_NOTE} It starts as a short paid pilot, not a trial.</p></div>
</div></section>
<section class="block" style="padding-top:0"><div class="wrap"><div class="panel panel-pad ai-script"><p class="panel-title">What a call sounds like</p>
  <p class="note">An example script ATH wrote to show the flow. It is not a recording of a real customer.</p>
  <dl class="ai-call">
   <dt>Receptionist</dt><dd>Thanks for calling Example Plumbing. I'm the business's AI assistant. How can I help?</dd>
   <dt>Caller</dt><dd>My water heater is leaking. Can someone come out today?</dd>
   <dt>Receptionist</dt><dd>I can help with that. Can I get your name and the address of the job?</dd>
   <dt>Caller</dt><dd>Jordan, 1200 Main Street.</dd>
   <dt>Receptionist</dt><dd>Thanks, Jordan. The first opening on the calendar is 2:30 this afternoon. Should I book it?</dd>
   <dt>Caller</dt><dd>Yes, please.</dd>
   <dt>Receptionist</dt><dd>You're booked for 2:30. I've texted you the confirmation, and the owner has your details.</dd>
  </dl></div></div></section>""" + cta_block("Find your missed calls first", "The free business diagnosis looks at how your calls are answered today."))

AI_BUILD_STATUS = ("Spaidbot Build is open." if SPAIDBOT_BUILD_URL else
  "Spaidbot Build, the AI builder inside the Spaidbot app, is being built and is not open yet. Until it opens, ATH builds your site with you.")
AI_SKETCH_JS = r"""<script>
(() => {
  const f = document.getElementById("sketch-form"), out = document.getElementById("sketch-out"); if (!f || !out) return;
  const KIND = {
    "home-services": { tag: "Fast, honest service at your door", items: ["Repairs", "Installations", "Maintenance plans", "Estimates"], cta: "Request an estimate" },
    "beauty": { tag: "Look good. Feel better.", items: ["Cuts & styling", "Color", "Treatments", "Gift cards"], cta: "Book a visit" },
    "food": { tag: "Made fresh, served with love", items: ["Today's menu", "Catering", "Hours & location", "Specials"], cta: "See the menu" },
    "health": { tag: "Care that makes time for you", items: ["New patients", "Services", "Insurance we accept", "Hours"], cta: "Request an appointment" },
    "creator": { tag: "Work with me", items: ["About", "Services", "Media kit", "Contact"], cta: "Book a call" },
    "other": { tag: "Here to help, every time", items: ["What we do", "About us", "Hours", "Contact"], cta: "Get in touch" },
  };
  const t = (s) => (s || "").toString().trim().slice(0, 60);
  function draw() {
    const fd = new FormData(f), k = KIND[fd.get("kind")] || KIND.other;
    const name = t(fd.get("bname")) || "Your Business", city = t(fd.get("city"));
    out.dataset.tone = fd.get("tone") || "gold";
    out.querySelector("[data-s=name]").textContent = name;
    out.querySelector("[data-s=tag]").textContent = k.tag + (city ? " in " + city : "");
    out.querySelector("[data-s=cta]").textContent = k.cta;
    const ul = out.querySelector("[data-s=items]"); ul.textContent = "";
    k.items.forEach((i) => { const li = document.createElement("li"); li.textContent = i; ul.appendChild(li); });
    out.querySelector("[data-s=foot]").textContent = name + (city ? " · " + city : "") + " · Call · Directions · Hours";
  }
  f.addEventListener("input", draw); f.addEventListener("submit", (e) => { e.preventDefault(); draw(); }); draw();
})();
</script>"""
pages["/ai/site-builder/"] = ("AI app and site builder — Spaidbot Build | Above the Hill",
 "Sketch your homepage in seconds, then get a real mobile website from ATH. Spaidbot Build, ATH's AI builder, is being built.",
 ai_head("/ai/site-builder/", "AI app &amp; site builder · Spaidbot Build", "Tell us your business.<br>See your site.",
   "Type your business name and what you do, and watch a first sketch of your homepage appear. When you're ready, ATH turns it into a real site.",
   btn("Sketch my site", "#sketch") + btn("See real sites ATH built", "/sites/", "line"))
 + f"""<section class="block" id="sketch" style="padding-top:8px"><div class="wrap split" style="align-items:start">
 <form class="panel panel-pad" id="sketch-form" novalidate><p class="panel-title">Build me a site · try it</p>
  <p class="note">This sketch is a template filled in by your browser, not AI, so you can see the idea in seconds. Nothing you type leaves this page.</p>
  <div class="field"><label class="lbl" for="s-name">Business name</label><input id="s-name" name="bname" type="text" maxlength="60" placeholder="Example: Sunrise Plumbing"></div>
  <div class="grid g2"><div class="field"><label class="lbl" for="s-kind">What you do</label><select id="s-kind" name="kind"><option value="home-services">Home services</option><option value="beauty">Salon, barber or beauty</option><option value="food">Restaurant or food truck</option><option value="health">Dental or health practice</option><option value="creator">Creator or coach</option><option value="other">Something else</option></select></div>
   <div class="field"><label class="lbl" for="s-city">City <span class="mute">(optional)</span></label><input id="s-city" name="city" type="text" maxlength="40" placeholder="Tulsa"></div></div>
  <fieldset class="field rv-fs"><legend class="lbl">Style</legend><div class="rv-checks">
   <label class="check"><input type="radio" name="tone" value="gold" checked> <span>Black &amp; gold</span></label>
   <label class="check"><input type="radio" name="tone" value="light"> <span>Clean &amp; light</span></label>
   <label class="check"><input type="radio" name="tone" value="bold"> <span>Bold colour</span></label></div></fieldset>
 </form>
 <div class="sketch" id="sketch-out" data-tone="gold" aria-live="polite" aria-label="Your homepage sketch">
  <div class="sk-bar"><span></span><span></span><span></span><em>Sketch · not a real site yet</em></div>
  <div class="sk-hero"><p class="sk-name" data-s="name">Your Business</p><p class="sk-tag" data-s="tag"></p><span class="sk-btn" data-s="cta">Get in touch</span></div>
  <ul class="sk-items" data-s="items"></ul><p class="sk-foot" data-s="foot"></p>
 </div>
</div></section>
<section class="block" style="padding-top:0"><div class="wrap split" style="align-items:start">
 <div class="panel panel-pad"><p class="panel-title">Spaidbot Build · the AI builder</p><p class="body">{AI_BUILD_STATUS}</p>
  <div class="ctas mt2">{btn("Get a free look first", "/free-look/", "line")}{req_btn("line", "Request an app or bigger build")}</div></div>
 <div class="panel panel-pad" id="prices" data-sb-pricing><p class="panel-title">Websites you can buy today</p><div class="rv-table">{site_rows()}</div>
  <p class="note mb0">Card checkout by Stripe. Apps and bigger systems: "Request this service" and ATH sends a written scope.</p></div>
</div></section>""" + cta_block("Want ATH to look first?", "The free business diagnosis checks how customers find and reach you today, website included.") + AI_SKETCH_JS)

pages["/ai/chat-assistant/"] = ("AI chat assistant — Spaidbot | Above the Hill",
 "Spaidbot is ATH's AI chat assistant. It answers from real prices and pages, cites what it used, says when it doesn't know and hands people to a person. Free to try on this site.",
 ai_head("/ai/chat-assistant/", "AI chat assistant · Spaidbot", "Questions answered,<br>day and night",
   "Spaidbot is the AI assistant on this website. Ask it anything about ATH right now: it answers from ATH's real price list and pages, shows what it used, and says so when it doesn't know.",
   ai_try_chat() + req_btn("line", "Request it for your website"))
 + f"""<section class="block" style="padding-top:8px"><div class="wrap split" style="align-items:start">
 <div><h2 class="display d-m">Why people use it</h2><ul class="pkg-list mt2">
  <li><b>Real answers, not guesses.</b> It reads from real prices and pages, and names the source it used.</li>
  <li><b>It knows when to stop.</b> When it doesn't know, it says so, and offers a person.</li>
  <li><b>Labelled as an AI.</b> Every chat opens by saying it is an AI assistant.</li>
  <li><b>Voice if you want it.</b> Tap the mic and talk; nothing is sent until you press Send.</li>
  <li><b>No tracking.</b> On this site it sets no cookies and stores no chat history.</li></ul>
  <div class="ctas mt2">{ai_try_chat("Ask Spaidbot a question")}</div></div>
 <div class="panel panel-pad"><p class="panel-title">For your own business</p><p class="body">Spaidbot is free to try here. Your own Spaidbot: Personal at $19 a month, Builder at $49 a month or Operations at $99 a month, bought with your WOW Passport at <a class="gold" href="https://thewow.online/plans" rel="noopener">thewow.online/plans</a>. Putting a chat assistant on your own website is set up in a written scope.</p>
  <div class="ctas mt2">{req_btn("gold")}</div><p class="note mb0">{REQ_NOTE}</p></div>
</div></section>""" + cta_block("See where a chat assistant would help", "The free business diagnosis looks at how people reach you and what they ask before they buy."))

GROW_NEEDS = [  # (value, label, recommendation key)
    ("missed", "Calls get missed", "receptionist"), ("allday", "The phone is busy all day", "receptionist"),
    ("leads", "New leads wait too long for a reply", "speed"), ("reviews", "We have few or old reviews", "reviews"),
    ("website", "No website, or it's out of date", "website"), ("reactivate", "Past customers don't come back", "reactivate"),
    ("questions", "People ask the same questions over and over", "chat"),
]
GROW_RECS = {
    "receptionist": {"name": "AI receptionist", "why": "Answers when you can't, books into your calendar and texts back missed callers.", "href": "/ai/receptionist/", "cta": "Request this service"},
    "speed": {"name": "Speed-to-Lead", "why": "New web, ad and form leads get a reply right away, then a person on your team takes over.", "href": REQ_HREF, "cta": "Request this service"},
    "reviews": {"name": "Review AI", "why": "Asks every customer for a review after a visit or a job. Every customer, happy or not.", "href": REQ_HREF, "cta": "Request this service"},
    "reactivate": {"name": "Reactivation texts", "why": "Past customers you choose get a message you approve, with opt-outs honoured.", "href": REQ_HREF, "cta": "Request this service"},
    "chat": {"name": "AI chat assistant (Spaidbot)", "why": "Answers the same questions every time, from your real prices and pages, and hands off to a person.", "href": "/ai/chat-assistant/", "cta": "Try it now"},
    "website": {"name": SITE_S[0], "why": "A fast mobile site with a clear call or booking button.", "href": SITE_S[2] or REQ_HREF, "cta": "Pay by card" if SITE_S[2] else "Request this service", "price": SITE_S[1]},
}
GROW_JS = r"""<script>
(() => {
  const D = JSON.parse(document.getElementById("grow-data").textContent), f = document.getElementById("grow-form"), out = document.getElementById("grow-out");
  if (!f || !out) return;
  const el = (tag, cls, txt) => { const e = document.createElement(tag); if (cls) e.className = cls; if (txt != null) e.textContent = txt; return e; };
  f.addEventListener("submit", (e) => {
    e.preventDefault();
    const needs = new FormData(f).getAll("need"), msg = document.getElementById("grow-msg");
    if (!needs.length) { msg.textContent = "Tick at least one thing that's happening now."; return; } msg.textContent = "";
    const keys = [...new Set(needs.map((n) => (D.needs.find((x) => x[0] === n) || [])[2]).filter(Boolean))];
    out.textContent = ""; const grid = el("div", "grid g3");
    keys.forEach((k, i) => { const r = D.recs[k]; const a = el("article", "panel panel-pad card grow-card");
      a.append(el("p", "eyebrow", i === 0 ? "Start here" : "Also fits"), el("h3", "", r.name)); if (r.price) a.append(el("p", "outcome-price", r.price));
      a.append(el("p", "", r.why)); const b = el("a", "btn btn-line btn-sm mt1", r.cta + " →"); b.href = r.href; if (/^https:/.test(r.href)) b.rel = "noopener"; a.append(b); grid.append(a); });
    out.append(el("h2", "display d-m", "Our recommendations for you"), grid);
    out.append(el("p", "note mt2", "These come from simple rules ATH wrote, not an AI guess. They are a starting point, not a quote; a person confirms the right fit in your free diagnosis."));
    const go = el("div", "ctas mt2"), a = el("a", "btn btn-gold", "Request my free diagnosis →"); a.href = "/business-diagnosis/"; go.append(a); out.append(go);
    const labels = needs.map((n) => (D.needs.find((x) => x[0] === n) || [, n])[1]);
    try { sessionStorage.setItem("ath_grow", `needs: ${labels.join(", ")} → recommended ${keys.map((k) => D.recs[k].name).join(", ")}`); } catch {}
    out.hidden = false; out.scrollIntoView({ behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth", block: "start" });
  });
})();
</script>"""
pages["/ai/growing-with-ai/"] = ("Growing with AI: our recommendations for you | Above the Hill",
 "Answer a few short questions about your business. ATH shows which AI services fit, and why. Free, two minutes, no sign-up.",
 ai_head("/ai/growing-with-ai/", "Growing with AI · free · two minutes", "Our recommendations<br>for you",
   "Tell us a little about your business. We'll show you which ATH services fit, and why.", btn("Start the quiz", "#grow"))
 + f"""<section class="block" id="grow" style="padding-top:8px"><div class="wrap">
 <form class="panel panel-pad" id="grow-form" novalidate><p class="panel-title">A few questions</p>
  <p class="note">Your answers stay in this browser tab. Nothing is sent unless you later choose to attach them to a free diagnosis request.</p>
  <div class="grid g2">
   <div class="field"><label class="lbl" for="g-kind">What kind of business?</label><select id="g-kind" name="kind"><option>Local business</option><option>Home services</option><option>Dental or health practice</option><option>Sales team</option><option>Creator or coach</option><option>Something else</option></select></div>
   <div class="field"><label class="lbl" for="g-calls">About how many calls a day?</label><select id="g-calls" name="calls"><option>Under 5</option><option>5 to 20</option><option>20 to 50</option><option>More than 50</option></select></div>
  </div>
  <fieldset class="field rv-fs"><legend class="lbl">What's happening now? Tick all that apply.</legend><div class="rv-checks">{"".join(f'<label class="check"><input type="checkbox" name="need" value="{v}"> <span>{html.escape(l)}</span></label>' for v, l, _ in GROW_NEEDS)}</div></fieldset>
  <button class="btn btn-gold" type="submit">Show my recommendations {ARR}</button>
  <p class="form-status" id="grow-msg" role="status" aria-live="polite"></p>
 </form>
 <div class="grow-out mt2" id="grow-out" hidden aria-live="polite"></div>
</div></section>
<script type="application/json" id="grow-data">{json.dumps({"needs": GROW_NEEDS, "recs": GROW_RECS}).replace("</", "<\\/")}</script>""" + GROW_JS)


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
    for src, dst in {"projects": "/work/", "diagnosis": "/diagnose/", "services": "/build/", "inventions": "/work/", "offer": "/pricing/"}.items():
        os.makedirs(os.path.join(ROOT, src), exist_ok=True)
        open(os.path.join(ROOT, src, "index.html"), "w").write(f'<!doctype html><meta charset="utf-8"><title>Redirecting…</title><link rel="canonical" href="{SITE}{dst}"><meta http-equiv="refresh" content="0; url={dst}"><script>location.replace("{dst}"+location.search)</script><a href="{dst}">Continue</a>')
    open(os.path.join(ROOT, "CNAME"), "w").write("abovethehilldev.online\n")
    open(os.path.join(ROOT, ".nojekyll"), "w").write("")
    # master catalog (registry "catalog"): every ATH offer with an honest status, for Spaidbot and partners
    open(os.path.join(ROOT, "catalog.json"), "w").write(json.dumps({"version": REG["version"], "statuses": {"LIVE": "can be bought now", "SCOPED": "sold through a written quote", "NOT_ACTIVE": "named but not deliverable yet", "PROPOSED": "a plan, not for sale", "LIVE_IN_WM_PRO": "available inside WM Pro", "RETIRED": "no longer sold; orders already placed are honored", "BOOKABLE": "book now: ATH confirms a time; card checkout switches on when its payment link is added"}, "offers": OFFERS}, indent=1, ensure_ascii=False))
    open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    urls = "".join(f"<url><loc>{SITE}{r}</loc></url>" for r in pages if r not in NOINDEX)
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    print("wrote", len(pages), "pages")

if __name__ == "__main__":
    write()

if __name__ == "__main__":
    # Website factory: client and sample sites from sites/clients/*.json (see sites/DELIVERY.md)
    import runpy
    runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sites", "build_sites.py"), run_name="__main__")
