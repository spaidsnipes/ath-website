// Read each NEW plan Payment Link (commercial/plan-setup-links.json) read-only in Playwright's BUNDLED headless Chromium
// (never Chrome) and mark it verified only if Stripe's own page says: live mode, the setup is the total due today, and the
// monthly price follows after 30 days. Fails closed: anything unclear stays verified=false and the site does not flip.
// Usage: node scripts/verify-setup-links.cjs [path-to-json]   (needs a Playwright install; default: ~/wealthymindsets-pro)
const fs = require('fs'), path = require('path'), os = require('os');
const PW = process.env.PW_MODULE || path.join(os.homedir(), 'wealthymindsets-pro/node_modules/playwright');
const { chromium } = require(PW);
const FILE = process.argv[2] || path.join(__dirname, '..', 'commercial', 'plan-setup-links.json');
const usd = (c) => '$' + (c / 100).toLocaleString('en-US', { minimumFractionDigits: 2 });
(async () => {
  const doc = JSON.parse(fs.readFileSync(FILE, 'utf8'));
  if (!doc.livemode) { console.log('Not live mode: nothing to verify for the site.'); process.exit(1); }
  const b = await chromium.launch({ headless: true });
  let ok = 0;
  try {
    for (const [k, e] of Object.entries(doc.links)) {
      const p = await b.newPage({ viewport: { width: 1440, height: 1000 } });
      e.verified = false;
      try {
        await p.goto(e.url, { waitUntil: 'load', timeout: 60000 }); await p.waitForTimeout(5000);
        const t = (await p.innerText('body')).replace(/\s+/g, ' ');
        const due = /due today\s*(\$[\d,]+\.\d\d)/i.exec(t)?.[1];
        const checks = { live: !/test mode/i.test(t), dueToday: due === usd(e.setup_cents), monthly: t.includes(usd(e.monthly_cents)), thirty: /30 days|30-day/i.test(t), noTotal: !t.includes(usd(e.setup_cents + e.monthly_cents)) };
        e.verified = Object.values(checks).every(Boolean);
        e.verified_at = new Date().toISOString(); e.checks = checks; e.seen = t.slice(0, 400);
        console.log(k, e.verified ? 'VERIFIED' : 'NOT VERIFIED', JSON.stringify(checks), '| due today:', due || '(not found)');
        await p.screenshot({ path: path.join(os.homedir(), 'ath-canon-live/shift-1113/proof/purchase-readiness', `setup-link-${k}-1440.png`) }).catch(() => {});
      } catch (err) { console.log(k, 'ERR', String(err.message).split('\n')[0]); }
      if (e.verified) ok++;
      await p.close();
    }
  } finally { await b.close(); }
  fs.writeFileSync(FILE, JSON.stringify(doc, null, 1));
  console.log(`${ok}/${Object.keys(doc.links).length} verified. The site flips only when all 15 are.`);
  process.exit(ok === Object.keys(doc.links).length ? 0 : 2);
})();
