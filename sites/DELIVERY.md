# From paid order to live client site (target: one business day)

Quick Start ($100) = one page, one revision. Business Growth ($200) = up to three pages.
The factory refuses an intake with more pages than its package allows.

## 1. Confirm the order
1. Stripe emails "payment received". Open Stripe → Payments and find the charge.
2. The lead alert (GitHub issue, label `paid-intake`) carries the checkout session id. Match it to the Stripe payment.
   No matching payment = not paid. Reply to the customer before building anything.

## 2. Build the site
1. Copy `sites/clients/_template.json` to `sites/clients/<business-city>.json` and fill it from the intake.
   - `theme`: `hearth` (food, cafés), `edge` (barbers, salons, trades), `atelier` (boutiques, studios, wellness).
   - Buttons must work: `tel:+1…`, `sms:+1…`, `mailto:…`, the booking or ordering link the business already uses, a Google Maps link.
   - Photos: put the owner's files in `public/sites/<slug>/photos/` and list them in the gallery section with alt text.
   - Never add reviews, ratings, awards or follower counts the owner did not give you.
2. Run `python3 build.py` from `ath-website/` and open `public/sites/<slug>/index.html` locally. Check it at phone width (375 px).
3. Commit and push. The preview goes live at `https://abovethehilldev.online/sites/<slug>/` (marked noindex until it has its own domain).

## 3. Review and revise
1. Send the owner the preview link. Quick Start includes one round of changes.
2. Edit the JSON, rebuild, push.

## 4. Their own domain (optional; the owner pays the registrar, about $12 a year)
1. Create a repo `spaidsnipes/<slug>-site`, copy `public/sites/<slug>/` into it, add a `CNAME` file with the domain, turn on GitHub Pages.
2. At the owner's registrar: `www` CNAME → `spaidsnipes.github.io`, apex A records → GitHub Pages IPs.
3. Set `"domain": "<their domain>"` in the intake and rebuild. That removes noindex and points the canonical URL and search data at their domain.

## 5. Hand off
Send the live link, what was included, how to ask for changes, and any recurring cost (domain, if any). Record the delivery on the lead in Mission Control.

## Ecosystem extras (Founder order 2026-10-24)
Every package includes the first month of ONE app's $10 tier free, chosen by the buyer. Today the only app with a working free-month code is WAVEMOTION Starter: follow `~/ath-canon-live/recovery/FREE-MONTH-RUNBOOK.md` (issue a WM-XXXX-XXXX code from WAVEMOTION Plans after you confirm the Stripe payment). Issue a Starter code for every package, including Business Growth.

The buyer may instead step up to the $20 World Pass. That is a purchase they make on WOW OS (thewow.online/passport): one app at its $20 tier plus the $10 tier of every other app. Never tell a buyer the World Pass is free and never say it unlocks the $20/$50 tier of every app.

The WOW "Make ATH free-month code" (30-day World Pass trial) still exists in WOW OS code, but the site no longer offers it. Do not send it unless the Founder rules otherwise.
