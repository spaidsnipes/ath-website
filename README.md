# Above the Hill Developments — Official Website

Public front door for ATH at https://abovethehilldev.online.

- `build.py` generates every page into `public/` (no npm, no framework). Run `python3 build.py`.
- Visual authority: Visual Canon Atlas v1, slide `athWebsiteCanonPass3` (Founder canon finder, 2026-10-07).
- Product truth: only Wavemotion ($10/mo) and World Pass ($20/mo) show prices; neither is sold here yet. No fake checkouts.
- The ATHOS diagnostic and lead intake live in a separate private Worker (`ath-athos`), called from `public/assets/ath.js`.
- Deploys to GitHub Pages on every push to `main`.
