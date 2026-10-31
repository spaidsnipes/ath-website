// World Pass value (Founder order 2026-10-24, with his corrections the same day).
// One ladder with real names: Free (Passport) · Basic $10 (one app's essentials) · World Pass $20 · Pro/OS $50+.
// The World Pass is THE ecosystem pass: Premium of the app you choose + Basic of every other ATH app, WOW OS,
// Academy, Dreamboard, future apps, WOW World when it opens. Never "$10 tier"/"$20 tier" to customers, no trials,
// no founding discounts, never the Premium/Pro tier of every app. Quick Start: a Basic month; $200 and up: a World Pass month.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const PUB = new URL('../public/', import.meta.url).pathname;
const read = (r) => readFileSync(PUB + r, 'utf8');
const files = (dir) => readdirSync(dir).flatMap((n) => { const p = join(dir, n); return statSync(p).isDirectory() ? files(p) : /\.html$/.test(n) ? [p] : []; });
const reg = JSON.parse(readFileSync(new URL('../commercial/registry.json', import.meta.url), 'utf8'));
const all = () => [...files(PUB), PUB + 'catalog.json', PUB + 'assets/ath.js'];

test('the ladder and value block sit on every page that sells or explains the pass', () => {
  // 2026-10-31 price book: the full value block lives on /path/ and /passport/; the front page and /pricing/ show the WOW Pass once (no double prices).
  for (const r of ['path/index.html', 'passport/index.html']) {
    const s = read(r);
    assert.match(s, /id="world-pass-value"/, r);
    assert.match(s, /What the \$20 World Pass(<br>| )gets you/, r);
    for (const t of ['Free Passport', 'Basic', 'World Pass', "One app's essentials, per app", 'Premium of the app you choose', 'Basic of every other ATH app',
      'Explore the Lounge', 'Listen to WOW Music and WOW Radio', 'Watch WOW TV', 'WOW Academy', 'The WOW Marketplace', 'Dreamboard, when it opens', 'Every new ATH app', 'WOW World, when it opens'])
      assert.ok(s.includes(t), `${r}: ${t}`);
    assert.match(s, /not the Premium or Pro tier of every app/, r);
  }
});

test('the top ladder says Free Passport / Basic / World Pass with real content', () => {
  const s = read('index.html');
  const lad = s.slice(s.indexOf('class="ladder"'), s.indexOf('</nav>', s.indexOf('class="ladder"')));
  assert.match(lad, /Free Passport/); assert.match(lad, /the Lounge/); assert.match(lad, /WOW Academy's free lessons/);
  assert.match(lad, /<span class="s">Basic<\/span>/); assert.match(lad, /One app's essentials, per app/);
  assert.match(lad, /<span class="s">World Pass<\/span>/);
  assert.doesNotMatch(lad, /Focused door|Join the world|Come in<|news/i);
});

test('customers never read "$10 tier" / "$20 tier", trials, founding offers or every-top-tier claims', () => {
  const BANNED = [/\$10 tier/, /\$20 tier/, /\$20 or \$50 tier/, /every app at its \$20/i, /Passport \$20/, /30[- ]day (world pass )?trial/i, /world pass trial/i, /Founding (500|1,?000)/i, /\bSPADE\b|Spade Business|Spade ?bot/];
  for (const f of all()) { const s = readFileSync(f, 'utf8'); for (const re of BANNED) assert.doesNotMatch(s, re, `${f.slice(PUB.length)}: ${re}`); }
});

test('packages: no free months (Founder 2026-10-30), and the pricing page offers none', () => {
  for (const p of reg.packages) {
    for (const e of p.ecosystem || []) assert.doesNotMatch(e.label + ' ' + e.note, /free month|30[- ]day/i, p.id);
  }
  assert.doesNotMatch(JSON.stringify(reg.package_step_up), /free month/i);
  for (const r of ['pricing/index.html', 'build/index.html', 'index.html']) assert.doesNotMatch(read(r), /free month of|first month free|half off/i, r);
});
