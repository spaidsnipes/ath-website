// Founder ship order, 2026-10-21: phrases banned from public copy. Built pages and the catalog are
// scanned. assets/spaidbot.js is left to its owner (the order says not to touch Spaidbot).
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const ROOT = new URL('../public/', import.meta.url).pathname;
const files = (d) => readdirSync(d).flatMap((n) => { const p = join(d, n); return statSync(p).isDirectory() ? files(p) : /\.(html|json)$/.test(n) || n === 'ath.js' ? [p] : []; });
const BANNED = [/built this week/i, /live tomorrow/i, /within one business day/i, /order online/i, /book online/i,
  /show up on google/i, /best seller/i, /ships in the US/, /real makers/i, /real goods/i, /from \$11\.99/, /from \$4\.99/,
  /Fresh Sneaks/i, /we set up your google/i, /we built your checkout/i,
  /limited time/i]; // open-ended scarcity: an offer without an end date never says 'limited time'

test('the scan covers the site', () => assert.ok(files(ROOT).length >= 40));
for (const re of BANNED) test(`no public page says ${re}`, () => {
  assert.deepEqual(files(ROOT).filter((f) => re.test(readFileSync(f, 'utf8'))).map((f) => f.slice(ROOT.length)), []);
});
