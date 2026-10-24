#!/usr/bin/env python3
"""ATH website factory: one client intake (sites/clients/<slug>.json) -> a finished site.

Quick Start ($100) = one page. Business Growth ($200) = up to three pages.
Output: public/sites/<slug>/ (and /<page>/ for extra pages), plus a gallery of samples at /sites/.

Rules the factory enforces:
- Real clients: every button does what it says (tel:, sms:, mailto:, a booking or order URL, a map link).
- Samples ("sample": true): fictional businesses. Buttons never dial or link anywhere fake; they jump to
  a note that says what the button does on a real site. Samples are noindex and carry a SAMPLE ribbon.
- No invented reviews, ratings, follower counts or awards. A section only renders when the intake has it.
Run: python3 sites/build_sites.py   (build.py also calls it)
"""
import html, json, os, re, glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(os.path.dirname(HERE), "public", "sites")
SITE = "https://abovethehilldev.online"
E = lambda s: html.escape(str(s or ""), quote=True)

THEMES = {
    # food & cafe: espresso dark, warm gold
    "hearth": {"fonts": "family=Fraunces:opsz,wght@9..144,500;9..144,700&family=Inter:wght@400;500;600",
               "display": "'Fraunces', Georgia, serif", "body": "'Inter', system-ui, sans-serif",
               "bg": "#17110d", "surface": "#221913", "line": "rgba(232,176,74,.22)", "ink": "#f6ecdc",
               "dim": "#c9b9a3", "accent": "#e8b04a", "on_accent": "#1b130c", "radius": "14px", "art_ink": "#fff7ea",
               "art": ["linear-gradient(135deg,#3a2414,#c98b3c)", "linear-gradient(160deg,#5a3a1e,#e8c27a)", "linear-gradient(120deg,#2a1a10,#8c5a2b)", "linear-gradient(150deg,#4a2b17,#d9a35a)"]},
    # barbers, salons, trades: graphite, barber red, condensed display
    "edge": {"fonts": "family=Oswald:wght@500;600&family=Inter:wght@400;500;600",
             "display": "'Oswald', 'Arial Narrow', sans-serif", "body": "'Inter', system-ui, sans-serif",
             "bg": "#0f1013", "surface": "#181a1f", "line": "rgba(255,255,255,.12)", "ink": "#f3f3f1",
             "dim": "#a9adb5", "accent": "#e2452f", "on_accent": "#ffffff", "radius": "6px", "art_ink": "#ffffff",
             "art": ["linear-gradient(140deg,#1c1f26,#5b6472)", "linear-gradient(160deg,#2a1210,#c23b27)", "linear-gradient(120deg,#16181d,#3c4250)", "linear-gradient(150deg,#262a33,#8a929f)"]},
    # boutiques, studios, wellness: light paper, sage, editorial serif
    "atelier": {"fonts": "family=Cormorant+Garamond:wght@500;600&family=Inter:wght@400;500;600",
                "display": "'Cormorant Garamond', Georgia, serif", "body": "'Inter', system-ui, sans-serif",
                "bg": "#f4f4ef", "surface": "#ffffff", "line": "rgba(29,33,28,.12)", "ink": "#1d211c",
                "dim": "#5b6157", "accent": "#55704f", "on_accent": "#ffffff", "radius": "2px", "art_ink": "#1d211c",
                "art": ["linear-gradient(140deg,#e7ebe1,#b9c8ad)", "linear-gradient(160deg,#efe9df,#cfd8c4)", "linear-gradient(120deg,#dfe6d7,#9fb391)", "linear-gradient(150deg,#f3efe8,#c9d3bd)"]},
}
SCHEMA_TYPES = {"Bakery", "Restaurant", "CafeOrCoffeeShop", "BarberShop", "HairSalon", "BeautySalon", "NailSalon",
                "ClothingStore", "Store", "HealthAndBeautyBusiness", "AutoRepair", "HomeAndConstructionBusiness",
                "ProfessionalService", "LocalBusiness", "BookStore", "DaySpa", "ShoeStore"}
DAYS = {"Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday", "Thu": "Thursday", "Fri": "Friday", "Sat": "Saturday", "Sun": "Sunday"}


def href(c, link):
    """Real clients keep their link; samples point every action at the sample note."""
    return "#sample-note" if c.get("sample") else E(link)


def css(t):
    return f"""
:root{{--bg:{t['bg']};--surface:{t['surface']};--line:{t['line']};--ink:{t['ink']};--dim:{t['dim']};--accent:{t['accent']};--on-accent:{t['on_accent']};--r:{t['radius']};--display:{t['display']};--body:{t['body']}}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}
body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 var(--body);-webkit-font-smoothing:antialiased}}
a{{color:inherit}}img{{max-width:100%;display:block}}
.wrap{{max-width:1080px;margin:0 auto;padding-inline:20px}}
.top{{position:sticky;top:0;z-index:5;background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}}
.top .wrap{{display:flex;align-items:center;justify-content:space-between;gap:12px;min-height:64px}}
.mark{{font:600 20px/1.1 var(--display);letter-spacing:.01em;text-decoration:none;flex:1 1 0;min-width:0}}
.pages{{display:flex;gap:18px;align-items:center;margin-left:auto}}.pages a{{text-decoration:none;color:var(--dim);font-size:14px;white-space:nowrap;padding-block:10px}}.pages a[aria-current=page]{{color:var(--ink)}}.top .btn{{white-space:nowrap}}
.btn{{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:48px;padding:0 20px;border-radius:var(--r);font:600 15px/1 var(--body);text-decoration:none;border:1px solid var(--accent)}}
.btn-solid{{background:var(--accent);color:var(--on-accent)}}.btn-line{{color:var(--ink);border-color:var(--line)}}
.btn:focus-visible,a:focus-visible{{outline:2px solid var(--accent);outline-offset:3px}}
.hero{{padding-block:72px 56px}}.eyebrow{{font:600 12px/1 var(--body);letter-spacing:.22em;text-transform:uppercase;color:var(--accent);margin:0 0 16px}}
h1{{font:600 clamp(42px,8vw,84px)/1.02 var(--display);margin:0 0 18px;text-wrap:balance}}
.lede{{font-size:clamp(18px,2.2vw,21px);color:var(--dim);max-width:46ch;margin:0 0 28px}}
.ctas{{display:flex;gap:12px;flex-wrap:wrap}}
.facts{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin-top:44px}}
.fact{{border-top:2px solid var(--accent);padding-top:12px;color:var(--dim);font-size:15px}}.fact b{{display:block;color:var(--ink);font-weight:600}}
section.block{{padding-block:56px;border-top:1px solid var(--line)}}
h2{{font:600 clamp(28px,4vw,40px)/1.1 var(--display);margin:0 0 24px}}
.items{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:2px 32px}}
.item{{display:grid;grid-template-columns:1fr auto;gap:2px 16px;padding:14px 0;border-bottom:1px solid var(--line)}}
.item b{{font-weight:600}}.item .p{{font-variant-numeric:tabular-nums;color:var(--accent);font-weight:600}}.item .d{{grid-column:1/-1;color:var(--dim);font-size:14.5px}}
.gallery{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px}}
.ph{{aspect-ratio:4/3;max-width:100%;border-radius:var(--r);overflow:hidden;position:relative;background:var(--surface);border:1px solid var(--line)}}
.ph img{{width:100%;height:100%;object-fit:cover}}
.ph.art{{display:flex;align-items:flex-end;padding:14px;font:600 15px/1.2 var(--display);color:{t["art_ink"]}}}
.ph.art::before{{content:"";position:absolute;inset:0;opacity:.9;background:var(--g)}}
.ph.art span{{position:relative}}.ph .tag{{position:absolute;top:10px;right:10px;font:600 10px/1 var(--body);letter-spacing:.14em;text-transform:uppercase;background:var(--bg);color:var(--dim);padding:5px 7px;border-radius:99px}}
.about{{max-width:62ch;color:var(--dim);font-size:17px}}
.visit{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:28px}}
table.hours{{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums}}table.hours td{{padding:8px 0;border-bottom:1px solid var(--line)}}table.hours td+td{{text-align:right;color:var(--dim)}}
.contact a{{display:block;padding:10px 0;border-bottom:1px solid var(--line);text-decoration:none}}.contact span{{color:var(--dim);font-size:13px;display:block}}
.foot{{padding-block:28px 40px;border-top:1px solid var(--line);color:var(--dim);font-size:13px}}.foot .wrap{{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}}
/* SP-082: the SAMPLE ribbon stays pinned on screen for the whole visit, above the sticky header. */
.sample-ribbon{{position:sticky;top:0;z-index:6;height:36px;display:flex;align-items:center;justify-content:center;gap:.5em;white-space:nowrap;overflow:hidden;background:repeating-linear-gradient(135deg,var(--accent) 0 14px,color-mix(in srgb,var(--accent) 86%,#000) 14px 28px);color:var(--on-accent);font:600 13px/1 var(--body);padding:0 12px;box-shadow:0 2px 10px rgba(0,0,0,.25)}}
.sample-ribbon b{{letter-spacing:.16em;text-transform:uppercase;font-weight:700;border:1.5px solid currentColor;border-radius:3px;padding:4px 7px}}
.sample-ribbon a{{color:inherit}}.sample-ribbon .sr-short{{display:none}}
.is-sample .top{{top:36px}}
@media (max-width:640px){{.sample-ribbon .sr-long{{display:none}}.sample-ribbon .sr-short{{display:inline}}}}
#sample-note{{scroll-margin-top:80px;border:1px solid var(--accent);border-radius:var(--r);padding:20px;margin-top:8px;background:var(--surface)}}
@media (max-width:640px){{.top .wrap{{flex-wrap:wrap;gap:0 12px;padding-block:8px}}.pages{{order:3;flex-basis:100%;margin:0;overflow-x:auto;gap:20px;border-top:1px solid var(--line)}}.hero{{padding-block:48px 40px}}}}
@media (prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}}}
"""


ART = ["linear-gradient(135deg,#3a2414,#c98b3c)", "linear-gradient(160deg,#5a3a1e,#e8c27a)", "linear-gradient(120deg,#2a1a10,#8c5a2b)",
       "linear-gradient(140deg,#20262e,#7b8796)", "linear-gradient(150deg,#3b1d1a,#c8553d)", "linear-gradient(130deg,#2f3b2c,#9fb08a)"]


def page_html(c, page, pages):
    t = THEMES[c.get("theme", "hearth")]
    a = c.get("address") or {}
    city = a.get("city", "")
    is_home = page.get("slug", "") == ""
    base = f"/sites/{c['slug']}/"
    title = f"{c['name']} — {c.get('category_label', c.get('category', ''))}{' in ' + city if city else ''}"
    if not is_home:
        title = f"{page['title']} · {c['name']}"
    desc = c.get("tagline", "")
    canonical = c.get("domain") and f"https://{c['domain']}/{page.get('slug','') + '/' if not is_home else ''}" or f"{SITE}{base}{page.get('slug','') + '/' if not is_home else ''}"
    robots = '<meta name="robots" content="noindex">' if (c.get("sample") or not c.get("domain")) else ""
    ld = {"@context": "https://schema.org", "@type": c.get("category") if c.get("category") in SCHEMA_TYPES else "LocalBusiness",
          "name": c["name"], "description": desc, "url": canonical}
    if c.get("phone"): ld["telephone"] = c["phone"]
    if a: ld["address"] = {"@type": "PostalAddress", "streetAddress": a.get("street", ""), "addressLocality": city,
                           "addressRegion": a.get("region", ""), "postalCode": a.get("postal", ""), "addressCountry": a.get("country", "US")}
    hrs = [h for h in c.get("hours", []) if h[1].lower() != "closed" and "–" in h[1]]
    if hrs:
        ld["openingHoursSpecification"] = [{"@type": "OpeningHoursSpecification", "dayOfWeek": DAYS.get(d, d),
                                            "opens": to24(v.split("–")[0]), "closes": to24(v.split("–")[1])} for d, v in hrs]
    jsonld = "" if c.get("sample") else f'<script type="application/ld+json">{json.dumps(ld)}</script>'

    nav = "".join(f'<a href="{base}{p.get("slug","") + "/" if p.get("slug") else ""}"{" aria-current=\"page\"" if p is page else ""}>{E(p["title"])}</a>' for p in pages) if len(pages) > 1 else ""
    pc = c.get("primary_cta") or {}
    top_cta = f'<a class="btn btn-solid" href="{href(c, pc.get("href"))}">{E(pc.get("label", "Call"))}</a>' if pc else ""
    ribbon = (f'<div class="sample-ribbon" role="note" aria-label="Sample site: {E(c["name"])} is not a real business"><b>Sample</b>'
              f'<span class="sr-long">Built by Above the Hill · {E(c["name"])} is not a real business ·</span><span class="sr-short">Not a real business ·</span>'
              f' <a href="{SITE}/offer/">Get yours: $100</a></div>') if c.get("sample") else ""

    body = []
    if is_home:
        sc = c.get("secondary_cta") or {}
        facts = "".join(f'<div class="fact"><b>{E(f[0])}</b>{E(f[1])}</div>' for f in c.get("facts", []))
        body.append(f"""<header class="hero"><div class="wrap">
<p class="eyebrow">{E(c.get('category_label', ''))}{' · ' + E(city) if city else ''}</p>
<h1>{E(c['name'])}</h1><p class="lede">{E(c.get('tagline'))}</p>
<div class="ctas">{f'<a class="btn btn-solid" href="{href(c, pc.get("href"))}">{E(pc.get("label"))}</a>' if pc else ''}{f'<a class="btn btn-line" href="{href(c, sc.get("href"))}">{E(sc.get("label"))}</a>' if sc else ''}</div>
{f'<div class="facts">{facts}</div>' if facts else ''}</div></header>""")
    for s in page.get("sections", []):
        body.append(section(c, s))
    if is_home or page.get("show_visit"):
        body.append(visit(c))
    if c.get("sample"):
        body.append(f"""<section class="block"><div class="wrap"><div id="sample-note"><h2 style="font-size:24px;margin-bottom:8px">This is a sample</h2>
<p class="about" style="margin:0">On a real ATH site every button works: <b>Call</b> rings the shop, <b>Text</b> opens a message, <b>Directions</b> opens maps, and <b>Book</b> or <b>Order</b> goes to the booking or ordering tool the business already uses. Photos, prices and hours come from the owner's intake.</p>
<p style="margin:16px 0 0"><a class="btn btn-solid" href="{SITE}/build/#pricing">See ATH website packages</a></p></div></div></section>""")
    links = " · ".join(f'<a href="{href(c, l["href"])}">{E(l["label"])}</a>' for l in c.get("links", []))
    credit = f'Website by <a href="{SITE}/?utm_source=client-site&utm_medium=footer&utm_campaign={E(c["slug"])}">Above the Hill</a>'
    foot = f'<footer class="foot"><div class="wrap"><span>© {E(c["name"])}{" · " + links if links else ""}</span><span>{credit}</span></div></footer>'
    return f"""<!doctype html><html lang="{E(c.get('lang','en'))}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><link rel="canonical" href="{E(canonical)}">{robots}
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:type" content="website"><meta property="og:url" content="{E(canonical)}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?{t['fonts']}&display=swap">
<style>{css(t)}</style>{jsonld}</head><body{' class="is-sample"' if c.get("sample") else ''}>{ribbon}
<div class="top"><div class="wrap"><a class="mark" href="{base}">{E(c['name'])}</a>{f'<nav class="pages" aria-label="Pages">{nav}</nav>' if nav else ''}{top_cta}</div></div>
<main>{''.join(body)}</main>{foot}</body></html>"""


def section(c, s):
    kind = s.get("kind", "items")
    inner = ""
    if kind == "items":
        rows = []
        for i in s.get("items", []):
            price = f'<span class="p">{E(i["price"])}</span>' if i.get("price") else "<span></span>"
            desc = f'<span class="d">{E(i["desc"])}</span>' if i.get("desc") else ""
            rows.append(f'<div class="item"><b>{E(i["name"])}</b>{price}{desc}</div>')
        inner = '<div class="items">' + "".join(rows) + "</div>"
    elif kind == "gallery":
        tiles = []
        for n, g in enumerate(s.get("items", [])):
            if g.get("src"):
                tiles.append(f'<figure class="ph" style="margin:0"><img src="{E(g["src"])}" alt="{E(g.get("alt", ""))}" loading="lazy"></figure>')
            else:  # a styled slot until the owner's photo arrives; samples say so plainly
                tiles.append(f'<div class="ph art" style="--g:{THEMES[c.get("theme","hearth")]["art"][n % 4]}"><span>{E(g.get("caption", ""))}</span>{"<em class=tag>photo here</em>" if c.get("sample") else ""}</div>')
        inner = '<div class="gallery">' + "".join(tiles) + "</div>"
    elif kind == "text":
        inner = "".join(f'<p class="about">{E(p)}</p>' for p in s.get("paragraphs", []))
    cta = s.get("cta")
    cta_html = f'<p style="margin:24px 0 0"><a class="btn btn-solid" href="{href(c, cta["href"])}">{E(cta["label"])}</a></p>' if cta else ""
    return f'<section class="block" id="{E(s.get("id", ""))}"><div class="wrap"><h2>{E(s["title"])}</h2>{inner}{cta_html}</div></section>'


def visit(c):
    a = c.get("address") or {}
    addr = ", ".join(x for x in [a.get("street"), a.get("city"), " ".join(x for x in [a.get("region"), a.get("postal")] if x)] if x)
    rows = "".join(f"<tr><td>{E(DAYS.get(d, d))}</td><td>{E(v)}</td></tr>" for d, v in c.get("hours", []))
    contact = []
    if c.get("phone"): contact.append(f'<a href="{href(c, "tel:" + re.sub(r"[^0-9+]", "", c["phone"]))}"><span>Call</span>{E(c["phone"])}</a>')
    if c.get("sms"): contact.append(f'<a href="{href(c, "sms:" + re.sub(r"[^0-9+]", "", c["sms"]))}"><span>Text</span>{E(c["sms"])}</a>')
    if c.get("email"): contact.append(f'<a href="{href(c, "mailto:" + c["email"])}"><span>Email</span>{E(c["email"])}</a>')
    if c.get("map_url") or addr: contact.append(f'<a href="{href(c, c.get("map_url") or "https://www.google.com/maps/search/?api=1&query=" + addr)}"><span>Directions</span>{E(addr)}</a>')
    return f"""<section class="block" id="visit"><div class="wrap"><h2>Visit</h2><div class="visit">
<div>{f'<table class="hours" aria-label="Opening hours"><tbody>{rows}</tbody></table>' if rows else ''}</div>
<div class="contact">{''.join(contact)}</div></div></div></section>"""


def to24(s):
    m = re.match(r"\s*(\d{1,2})(?::(\d{2}))?\s*([AP]M)\s*", s, re.I)
    if not m: return s.strip()
    h, mi, ap = int(m.group(1)), int(m.group(2) or 0), m.group(3).upper()
    h = (h % 12) + (12 if ap == "PM" else 0)
    return f"{h:02d}:{mi:02d}"


def build():
    clients = []
    for f in sorted(glob.glob(os.path.join(HERE, "clients", "*.json"))):
        if os.path.basename(f).startswith("_"): continue
        c = json.load(open(f))
        assert re.fullmatch(r"[a-z0-9-]{3,60}", c["slug"]), f"bad slug in {f}"
        assert c.get("theme", "hearth") in THEMES, f"unknown theme in {f}"
        pages = [{"slug": "", "title": "Home", "sections": c.get("sections", [])}] + c.get("pages", [])
        limit = 1 if c.get("package") == "quick-start" else 3
        assert len(pages) <= limit, f"{c['slug']}: {c.get('package')} allows {limit} page(s), intake has {len(pages)}"
        for p in pages:
            d = os.path.join(ROOT, c["slug"], p["slug"]) if p["slug"] else os.path.join(ROOT, c["slug"])
            os.makedirs(d, exist_ok=True)
            open(os.path.join(d, "index.html"), "w").write(page_html(c, p, pages))
        clients.append(c)
    samples = [c for c in clients if c.get("sample")]
    cards = "".join(f'<a class="card" href="/sites/{c["slug"]}/"><span class="k">{E({"quick-start": "Quick Start · $100", "business-growth": "Business Growth · $200"}.get(c.get("package"), ""))}</span><b>{E(c["name"])}</b><span>{E(c.get("category_label"))} · {E(c.get("theme"))} style</span></a>' for c in samples)
    os.makedirs(ROOT, exist_ok=True)
    open(os.path.join(ROOT, "index.html"), "w").write(f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">
<title>Sample sites — Above the Hill</title><link rel="icon" href="/favicon.png" type="image/png"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Inter:wght@400;500;600&display=swap">
<style>body{{margin:0;background:#0b0c0f;color:#efe7d6;font:16px/1.6 Inter,system-ui,sans-serif}}.w{{max-width:960px;margin:0 auto;padding:56px 20px}}h1{{font:600 clamp(36px,6vw,56px)/1.05 'Cormorant Garamond',Georgia,serif;margin:0 0 12px}}p{{color:#b3ab9a;max-width:60ch}}
.g{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px;margin-top:28px}}.card{{display:grid;gap:4px;padding:20px;border:1px solid rgba(201,164,92,.35);border-radius:8px;text-decoration:none;color:inherit;background:#121318}}.card:hover,.card:focus-visible{{border-color:#d8b46a;outline:none}}.card b{{font:600 24px/1.2 'Cormorant Garamond',Georgia,serif}}.card span{{color:#b3ab9a;font-size:14px}}.k{{color:#d8b46a!important;font-size:12px!important;letter-spacing:.14em;text-transform:uppercase;font-weight:600}}a.back{{color:#d8b46a}}</style></head>
<body><main class="w"><p><a class="back" href="/build/#pricing">← ATH website packages</a></p><h1>What your website could look like</h1>
<p>Each sample below is a fictional business, built with the same templates ATH uses for paying clients. Your site uses your name, photos, prices, hours and the booking or ordering tool you already have.</p>
<div class="g">{cards}</div></main></body></html>""")
    print("factory wrote", len(clients), "site(s)")


if __name__ == "__main__":
    build()
