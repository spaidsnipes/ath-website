// Website greeter (ATH-BEST-SYSTEM-SUGGESTIONS-2026-10-30 §7) + the 2026-10-30 price ladder on the revenue pages.
// Every page loads the ONE ATHOS Spaidbot embed in public mode with the proactive greeter on; the greeter's behaviour
// (20 s / pricing in view, once per session, reduced motion, AI disclosure, no tracking) lives in athos-brain
// spaidbot-embed.mjs and is tested there. Here: the tag is on every page, the old local copy is gone, the pricing
// areas the greeter watches exist, and the ladder copy is the 2026-10-31 price book (15 steps) with no trial, no free month, no discount.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const PUB = new URL('../public/', import.meta.url).pathname;
const pages = (d) => readdirSync(d).flatMap((n) => { const p = join(d, n); return statSync(p).isDirectory() ? pages(p) : n === 'index.html' ? [p] : []; });
const read = (r) => readFileSync(PUB + r, 'utf8');
const TAG = /<script src="https:\/\/mission\.abovethehilldev\.online\/spaidbot\.js" data-api="https:\/\/mission\.abovethehilldev\.online" data-product="ath" data-greet="1" data-compact-hero="1" data-audit-href="\/business-diagnosis\/" defer><\/script>/;

test('every built ATH page loads the ATHOS embed once, public ATH product, greeter on; the old local Spaidbot is gone', () => {
  const built = pages(PUB).filter((p) => !/\/(sites|preview)\//.test(p) && !/http-equiv="refresh"/.test(readFileSync(p, 'utf8')));
  assert.ok(built.length >= 40, String(built.length));
  for (const p of built) {
    const s = readFileSync(p, 'utf8');
    assert.match(s, TAG, p);
    assert.equal(s.match(/spaidbot\.js/g).length, 1, p);
    assert.doesNotMatch(s, /\/assets\/spaidbot\.js/, p);
  }
  assert.equal(existsSync(PUB + 'assets/spaidbot.js'), false);
  assert.doesNotMatch(read('assets/ath.css'), /\.sb-fab/);
});

test('the greeter has a pricing area to watch on the revenue pages, and the leak-audit hand-off target exists', () => {
  for (const r of ['industries/dental/index.html', 'industries/index.html', 'consequence-calculator/index.html', 'pricing/index.html']) {
    const s = read(r);
    assert.match(s, /id="pricing" data-sb-pricing/, r);
    assert.equal(s.match(/id="pricing"/g).length, 1, r);
  }
  assert.match(read('build/index.html'), /id="pricing"/);
  assert.match(read('business-diagnosis/index.html'), /name="intent" value="business-diagnosis"/);
});

test('the ONE price book (2026-10-31) on industry + calculator pages: 15 steps $100 → $8,000, one name and one price each, services apart, no trial / free month / discount', () => {
  const book = JSON.parse(readFileSync(new URL('../commercial/price-book.json', import.meta.url), 'utf8'));
  const want = book.steps.map((p) => [p.name, `$${p.monthly.toLocaleString('en-US')} / month`]);
  assert.equal(want.length, 15); assert.deepEqual(want[0], ['Presence', '$100 / month']); assert.deepEqual(want.at(-1), ['Enterprise', '$8,000 / month']);
  assert.equal(new Set(want.map((w) => w[0])).size, 15); assert.equal(new Set(want.map((w) => w[1])).size, 15);
  const inds = readdirSync(PUB + 'industries').filter((d) => statSync(PUB + 'industries/' + d).isDirectory());
  assert.ok(inds.length >= 5);
  for (const r of [...inds.map((d) => `industries/${d}/index.html`), 'industries/index.html', 'consequence-calculator/index.html']) {
    const s = read(r), panel = s.slice(s.indexOf('id="pricing"'), s.indexOf('</ul></div>', s.indexOf('id="pricing"')));
    const levels = [...panel.matchAll(/data-level="([^"]+)"><span><b>[^<]+<\/b><span class="note">[^<]*<\/span><\/span><span class="rv-price">([^<]+)<span class="note">\$[\d,]+ setup today · monthly starts in 30 days<\/span><\/span>/g)].map((m) => [m[1], m[2]]);
    assert.deepEqual(levels, want, r);
    assert.match(panel, /WOW Pass \(WOW = World of Wealth\)/, r);
    assert.match(panel, /You pay the one-time setup today\. Your monthly plan starts 30 days later/, r); // Founder 2026-11-01: setup is the upfront charge
    assert.doesNotMatch(s, /free trial|free month of|\bWild\b|Quick Start|Business Growth/i, r);
    assert.match(s, /Services on their own · not part of a plan/, r);
    for (const t of ['Speed-to-Lead', '$200 a month', 'Review AI', '$300 a month', '$500 a month', 'Starter Website', '$250 + $25 setup, one time', 'Business Website', '$500 + $75 setup, one time']) assert.ok(s.includes(t), `${r}: ${t}`);
  }
});
