# Above the Hill Developments — Official Website

Public front door for ATH at https://abovethehilldev.online.

- `build.py` generates every page into `public/` (no npm, no framework). Run `python3 build.py`.
- Visual authority: Visual Canon Atlas v1, slide `athWebsiteCanonPass3` (Founder canon finder, 2026-10-07).
- Commercial authority: `commercial/registry.json` v2026-11-07.1 records the Founder price matrix of 2026-11-07 (WM Pro $10/$20/$30, WAVEMOTION $10/$20/$50/$75, Spaidbot Free/$20/$100 (Founder 11-13), WOW Studios, PowerTribes, Creator Passport, FOUNDING 500, World Pass $20 with a 7-day trial, card required). Plans link to the existing WAVEMOTION app; ATH does not create a second subscription. Paid cinematic generation is not open. ATH service packages use a written scope-and-invoice path; nothing is charged by the contact form.
- The ATHOS diagnostic and lead intake live in a separate private Worker (`ath-athos`), called from `public/assets/ath.js`.
- Deploys to GitHub Pages on every push to `main`.
