// Founder 11-13 night: checkout charges exactly what the words say. Copy and Payment Link flip TOGETHER, all 15 steps or none.
// Builds a throwaway copy of the site with a fake commercial/plan-setup-links.json and checks what the pages say.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { cpSync, mkdtempSync, readFileSync, writeFileSync, rmSync, existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';

const ROOT = new URL('..', import.meta.url).pathname;
const book = JSON.parse(readFileSync(join(ROOT, 'commercial/price-book.json'), 'utf8'));
const fake = (n) => `https://buy.stripe.com/test_fake${String(n).padStart(2, '0')}`;
function links(over = {}) {
  return { version: 1, links: Object.fromEntries(book.steps.map((p, i) => [p.key, { url: fake(i), setup_cents: p.setup * 100, monthly_cents: p.monthly * 100, trial_days: 30, verified: true, ...over }])) };
}
function buildWith(json) {
  const dir = mkdtempSync(join(tmpdir(), 'ath-flip-'));
  for (const d of ['build.py', 'commercial', 'sites', 'public']) cpSync(join(ROOT, d), join(dir, d), { recursive: true });
  if (json) writeFileSync(join(dir, 'commercial/plan-setup-links.json'), JSON.stringify(json));
  else if (existsSync(join(dir, 'commercial/plan-setup-links.json'))) rmSync(join(dir, 'commercial/plan-setup-links.json'));
  const r = spawnSync('python3', ['build.py'], { cwd: dir, encoding: 'utf8' });
  return { dir, ok: r.status === 0, err: r.stderr, read: (f) => readFileSync(join(dir, 'public', f), 'utf8') };
}

test('no setup-links file: cards say setup + first month today and keep the live links', () => {
  const b = buildWith(null); assert.ok(b.ok, b.err);
  const s = b.read('pricing/index.html');
  assert.match(s, /\$130 today: \$30 to set up plus your first month, then \$100 a month/);
  assert.ok(s.includes(book.steps[0].pay_url));
  assert.doesNotMatch(s, /starting day 30/);
  rmSync(b.dir, { recursive: true, force: true });
});

test('all 15 verified: cards say "$30 today to set up, then $100 a month starting day 30" and use the NEW links', () => {
  const b = buildWith(links()); assert.ok(b.ok, b.err);
  const s = b.read('pricing/index.html');
  assert.match(s, /\$30 today to set up, then \$100 a month starting day 30/);
  assert.ok(s.includes(fake(0)) && s.includes(fake(14)));
  for (const p of book.steps) assert.ok(!s.includes(p.pay_url), `old link still on the page: ${p.key}`);
  assert.doesNotMatch(s, /plus your first month/);
  assert.match(b.read('terms/index.html'), /the monthly price starts on day 30/);
  rmSync(b.dir, { recursive: true, force: true });
});

test('unverified or wrong-amount entries never flip; a partial flip fails the build', () => {
  const u = buildWith(links({ verified: false })); assert.ok(u.ok, u.err);
  assert.doesNotMatch(u.read('pricing/index.html'), /starting day 30/);
  rmSync(u.dir, { recursive: true, force: true });
  const j = links(); j.links[book.steps[3].key].setup_cents += 100;
  const p = buildWith(j); assert.ok(!p.ok, 'a partial flip must stop the build');
  rmSync(p.dir, { recursive: true, force: true });
});
