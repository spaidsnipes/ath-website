// Founder final ruling 2026-10-25: WAVEMOTION has NO free trial. Lead with "Starts at $10 a month" (one link,
// analytics, clips). Holiday special (Creator first month $10) is date-gated and states its deadline.
// GUARD: fails if "14-day" or "free trial" wording for WAVEMOTION reappears on the public site.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const PUB = new URL('../public/', import.meta.url).pathname;
const files = (dir) => readdirSync(dir).flatMap((n) => { const p = join(dir, n); return statSync(p).isDirectory() ? files(p) : /\.(html|json|js)$/.test(n) ? [p] : []; });

test('guard: no 14-day / free-trial / free-days wording on any public page or the catalog', () => {
  const banned = [/14[- ]day/i, /free trial/i, /trial needs no card/i, /free for \d+ days/i];
  const sources = [...files(PUB), new URL('../commercial/registry.json', import.meta.url).pathname, new URL('../build.py', import.meta.url).pathname];
  const hits = sources.flatMap((p) => { const s = readFileSync(p, 'utf8'); return banned.filter((re) => re.test(s)).map((re) => `${p} matches ${re}`); });
  assert.deepEqual(hits, []);
});

test('the WAVEMOTION plans block leads with $10; the holiday special states its deadline and removes itself after it', () => {
  const s = readFileSync(PUB + 'build/index.html', 'utf8');
  assert.match(s, /<b>Starts at \$10 a month<\/b>: one link for all your socials, your analytics in one place, and clips from your videos/);
  const built = /data-offer-ends="2026-12-26T05:59:59Z"/.test(s);
  if (Date.now() <= Date.parse('2026-12-26T05:59:59Z')) {
    assert.ok(built, 'holiday note present before the deadline');
    assert.match(s, /first month of WAVEMOTION Creator \(Premium, \$20\) is \$10, half off, when you subscribe by December 25, 2026, 11:59 PM CT\. Then \$20\/month until you cancel\./);
  } else assert.ok(!built, 'a build after the deadline leaves it out');
  const js = readFileSync(PUB + 'assets/ath.js', 'utf8');
  assert.match(js, /querySelectorAll\("\[data-offer-ends\]"\)\.forEach\(\(e\) => \{ const t = Date\.parse\(e\.getAttribute\("data-offer-ends"\)\); if \(!Number\.isFinite\(t\) \|\| Date\.now\(\) > t\) e\.remove\(\); \}\)/);
});
