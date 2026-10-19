# ATH Commercial Reconciliation Ledger — 2026-10-13

Precedence (Founder order §1): latest explicit Founder direction → constitutional law → approved product canon → verified runtime evidence → lineage.
Registry: `commercial/registry.json` v2026-10-13.1. Every price on abovethehilldev.online is generated from it by `build.py`.

| # | Conflict | Older authority | Chosen authority | Affected systems | Migration / status |
|---|---|---|---|---|---|
| R-1 | Entry website price | Oct 7 lock: Starter website from $250 | Oct 13 order §4: Quick Start $100, Business Growth $200 (one time) | ATH /build/, /path/, home, contact form, lead alerts | DONE in registry and site. Oct 7 `starter-website` id is retired. Old links show an "out of date" note instead of a stale price. |
| R-2 | Business website | Oct 7: Business website / system from $500 | Oct 13: Professional Website from $500 | ATH /build/ | DONE. `business-website` id is retired → `professional-website`. |
| R-3 | App ladder | Not priced (custom = diagnose → scope → quote) | Oct 13: App Starter $1,000, Mobile App Bundle $2,500, Business App System $5,000, Omnichannel $8,000 (all "starting at") | ATH /build/ | DONE. Each one routes to a scope request. |
| R-4 | WAVEMOTION plans | Oct 7: single $10/mo membership (also what wavemotion.live showed on Oct 13) | Oct 13: Starter $10/40 clips, Creator $20/80, Pro $50/250, Living Cinema Studio $75 (Pro + Living Cinema with a disclosed credit allowance) | ATH site, WAVEMOTION billing/entitlements, wavemotion.live | ATH site DONE (labelled "checkout not confirmed"). WAVEMOTION billing: handed to the WAVEMOTION thread on 2026-10-13. OPEN. |
| R-5 | Living Cinema credit counts | A conversation proposed 2/4/8/15 cinematic credits across the tiers | Not in the Oct 13 written order | WAVEMOTION | OPEN → decision D-007. No credit counts are published. |
| R-6 | Clipping packages $75–$225 and setup services (Living Destination $75, Channeler $100, Campaign $250) | Oct 7 lock | Not addressed Oct 13 → Oct 7 stays in force | ATH /build/ | KEPT as "done-for-you services." Possible overlap with subscription clip allowances → decision D-006. |
| R-7 | Member discount | Revenue canon 20%; another mission mentioned 10% | Revenue canon (20%) until superseded | Clipping prices | Unchanged. The existing Founder decision D-001 stays OPEN. |
| R-8 | Package ecosystem extras (WAVEMOTION Starter, $20 membership first month, Teach Pass, WOW media pathways) | n/a | Oct 13 §4 + commercial-honesty law §2 | ATH site, Passport, Academy, WAVEMOTION | Published as "Not active yet." Not delivered until operational, with no renewal without consent. |
| R-9 | Payment method | n/a — no checkout on ATH | Oct 13 §15: "valid payment or clearly defined invoice flow" | ATH contact → ATHOS lead | INVOICE_ONLY: the customer agrees to scope-and-invoice terms; the lead is stored with the package + catalog version; ATH sends the scope and invoice. Card checkout is BLOCKED on the Founder's Stripe decision (D-008). |
| R-10 | Naming WOW vs WILD | Drive canon: WOW | WOW stays canonical | All | No change. |

## Decisions for the Founder
- **D-006**: Keep the à-la-carte clipping packages ($75–$225), or fold them into the WAVEMOTION plan allowances?
- **D-007**: Confirm or reject the Living Cinema credit counts (2/4/8/15) and the extra-credit price, after costs are measured from real jobs.
- **D-008**: ATH card payments. Create Stripe Payment Links (or an invoice tool) for Quick Start and Business Growth. The Founder must do this in the Founder's own Stripe account; Claude does not enter payment credentials.

## Supersession — 2026-10-13 (later the same day), Founder in Mission Control
- **R-4 updated:** The Founder says the Starter $10 / Creator $20 / Pro $50 / Living Cinema Studio $75 tiers are **old**; new WAVEMOTION plans exist. Registry v2026-10-13.2 removes all WAVEMOTION plan prices from the ATH site (kept under `superseded` for lineage). The site shows "new plans are being finalized" until the Founder supplies the new plans. R-5 / D-007 (credit counts) now waits on those plans too.
- **Music rights:** The Founder confirms the songs used for ATH ads are his own (Dspaid catalog). Oct 9 preflight decision "e" is resolved for ATH ads.
- **D-009 resolved (Pipeline A scope):** ATH builds websites for businesses anywhere in the world, delivered remotely. No local pilot zone is required.
- **Likeness:** Faceless by default; the Founder is OK appearing on camera. Any synthetic version of his face or voice still needs disclosure.

## Supersession — October 14, 2026, Founder confirmation
The Founder answered the exact pricing reconciliation question in Execute ATH production sequence: **“Keep the current $10/$20/$50/$75 tiers.”** Registry v2026-10-14.1 restores Starter/Creator/Pro/Living Cinema Studio prices and 40/80/250/250 standard clips, matching WAVEMOTION's live registry. This supersedes the October 13 pending-new-plans hold; the older decision remains above as lineage. Paid cinematic generation remains closed, its expensive production credits unactivated, and no unlimited render claim is made. The website links to WAVEMOTION's existing trial/Plans path; no second billing system is created. Public pricing parity does not prove a paid customer lifecycle. D-006, D-007, D-008 and the Passport clipping-discount conflict are not silently resolved.

## 2026-10-14 — Card payment live (Mission Control)
- **R-9 / D-008 resolved:** Stripe Payment Links on account AboveTheHilldevelopments: Quick Start $100 (plink_1UQe8OLRFuTpfZm9fZdUV8os → buy.stripe.com/3cI4gA1KkdPkbvJ2oG97G00), Business Growth $200 (plink_1UQe9SLRFuTpfZm9Rgg9P7mv → buy.stripe.com/eVq4gAcoY4eKarF1kC97G01). Both collect name + business name and show an intake-next-steps confirmation. Scoped packages stay scope → quote → invoice. Registry v2026-10-14.3.
- **Shopify:** "My Store" (0s9nn1-pg.myshopify.com) has 0 products and Shopify Payments isn't set up (that needs the owner's identity and bank details). Not used; Stripe is the payment system of record.

## 2026-10-19 — Founder revenue plan (registry v2026-10-19.1)
- **Package extras:** per the Founder's Oct 19 plan, Quick Start and Business Growth both carry: free Passport identity setup (LIVE — ATH helps create it), one month of WAVEMOTION Starter (NOT ACTIVE: WAVEMOTION's complimentary grant exists but never ends on its own), one month of WM Pro (NOT ACTIVE: WM Pro has no complimentary grant and no $10 Core tier yet). The Oct 13 extras (first month of the $20 membership, Teach Pass, WAVEMOTION Creator allowance, WOW media pathways) are superseded.
- **New package:** Cinematic Business Launch, $500–$700, scoped (quote, no card link): website plus two 30–60 s promotional videos made from the client's footage, plus a WAVEMOTION campaign setup. Its one-month WAVEMOTION Pro and World Pass extras are NOT ACTIVE; WM Pro Elite is not offered because the tier does not exist.
- **Master catalog:** `catalog` in the registry, published at `/catalog.json`: 18 offers across ATH, WAVEMOTION, WM Pro, WOW World, WOW Shop, Academy, AI Influencer and Spaidbot, each with status LIVE / SCOPED / NOT_ACTIVE / PROPOSED. Proposed and not for sale: WM Pro Core $10 / Pro $20 / Elite $50 tiers, Passport Core $10, AI Influencer $199, holiday collection.
- **Names:** the plan's "$100 Digital Launch" is the live Quick Start (Stripe product and site keep that name).

## 2026-10-19 (night) — Founder bonus ladder + Spaidbot (registry v2026-10-19.2)
- **Bonus months, by package (Founder, Oct 19):** Quick Start $100 → one month WAVEMOTION Starter ($10) + WM Pro ($20). Business Growth $200 → WAVEMOTION Creator ($20) + WM Pro ($20) + World Pass ($20). Cinematic Launch $500–$700 → WAVEMOTION Pro ($50) + WM Pro top tier + World Pass. All NOT ACTIVE until each app can grant a month that ends on its own; after the month nothing renews unless the customer chooses a plan (World Pass $20 is the suggested keep-everything option).
- **Spaidbot (Founder: "all completely free, connected to ATHOS and the ATH website"):** live on every page as "Ask Spaidbot". ATHOS `/api/spaidbot` answers only from `/catalog.json` on Workers AI (`@cf/meta/llama-3.1-8b-instruct-fp8`), capped at 30 questions/hour per connection and 600/day so it stays inside the free daily allowance. Stores no message text.

- **Packages from $500 (Founder, Oct 19, corrected):** one month of Pro across the ATH apps (WAVEMOTION Pro, WM Pro top tier, World Pass), then the $20/month World Pass only with consent given at purchase. A "three months" version briefly published in v2026-10-19.4 was a Mission Control error, corrected in v2026-10-19.5.

- **World Pass free month LIVE (v2026-10-19.6):** WOW now issues single-use ATH codes (Founder-only) for a 30-day World Pass trial with the card saved at checkout; $20/month starts only if kept past day 30; no card → cancels. Included with Business Growth and every package from $500. WAVEMOTION and WM Pro months remain NOT ACTIVE.
