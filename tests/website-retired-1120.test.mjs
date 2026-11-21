// Founder ruling 2026-11-20: one-time-only websites (no monthly) are retired; every website mention points to Presence
// ($30 today, then $100 a month, the verified setup-today link). "$10-level WOW Pass" is now "WOW Passport included".
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';
const PUB = new URL('../public/', import.meta.url).pathname;
const walk = (d) => readdirSync(d).flatMap((n) => { const p = join(d, n); return statSync(p).isDirectory() ? walk(p) : [p]; });
const files = walk(PUB).filter((f) => /\.(html|json|js)$/.test(f));
const BANNED = [/97G02/, /97G03/, /\$250 for the site/, /\$500 for the site/, /Starter Website/, /Business Website/, /\$10-level WOW Pass/, /por el sitio y \$25/];
for (const re of BANNED) test(`no built file carries ${re}`, () => {
  assert.deepEqual(files.filter((f) => re.test(readFileSync(f, 'utf8'))).map((f) => f.slice(PUB.length)), []);
});
test('websites point to Presence with its verified link', () => {
  const p = readFileSync(join(PUB, 'pricing/index.html'), 'utf8');
  assert.match(p, /Inside Presence: \$30 today, then \$100 a month/);
  assert.match(p, /5kQ14o4WwdPk1V9e7o97G0k/);
  assert.match(p, /WOW Passport included/);
  const city = readFileSync(join(PUB, 'websites/tulsa/bakeries/index.html'), 'utf8');
  assert.match(city, /inside Presence: \$30 today, then \$100 a month/);
  assert.match(city, /href="https:\/\/buy\.stripe\.com\/5kQ14o4WwdPk1V9e7o97G0k"/);
});
