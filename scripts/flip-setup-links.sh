#!/bin/zsh
# After the Founder runs ~/Desktop/CREATE-PLAN-SETUP-LINKS.command: verify the 15 new Stripe links, then rebuild + test.
# Copy and links flip together (build.py refuses a partial flip). Pushing to main (= GitHub Pages deploy) stays a separate step.
set -e
cd "$(dirname "$0")/.."
[ -f commercial/plan-setup-links.json ] || cp ~/ath-canon-live/shift-1113/plan-setup-links.json commercial/plan-setup-links.json
node scripts/verify-setup-links.cjs commercial/plan-setup-links.json
python3 build.py
for t in tests/*.test.mjs; do node --test "$t" >/dev/null || { echo "FAIL $t"; exit 1; }; done
grep -c "today to set up, then" public/pricing/index.html
echo "Ready: commit, rebase on origin/main, push, then curl /pricing/ for the new buy.stripe.com links."
