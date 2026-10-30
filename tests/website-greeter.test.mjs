// Website greeter (ATH-BEST-SYSTEM-SUGGESTIONS-2026-10-30 §7) + the 2026-10-30 price ladder on the revenue pages.
// Every page loads the ONE ATHOS Spaidbot embed in public mode with the proactive greeter on; the greeter's behaviour
// (20 s / pricing in view, once per session, reduced motion, AI disclosure, no tracking) lives in athos-brain
// spaidbot-embed.mjs and is tested there. Here: the tag is on every page, the old local copy is gone, the pricing
// areas the greeter watches exist, and the ladder copy is the locked 8 levels with no trial, no free month, no $200 rung.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const PUB = new URL('../public/', import.meta.url).pathname;
const pages = (d) => readdirSync(d).flatMap((n) => { const p = join(d, n); return statSync(p).isDirectory() ? pages(p) : n === 'index.html' ? [p] : []; });
const read = (r) => readFileSync(PUB + r, 'utf8');
const TAG = /<script src="https:\/\/mission\.abovethehilldev\.online\/spaidbot\.js" data-api="https:\/\/ath-athos\.dhill5711\.workers\.dev" data-product="ath" data-greet="1" data-compact-hero="1" data-audit-href="\/business-diagnosis\/" defer><\/script>/;

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
  for (const r of ['industries/dental/index.html', 'industries/index.html', 'consequence-calculator/index.html']) {
    const s = read(r);
    assert.match(s, /id="pricing" data-sb-pricing/, r);
    assert.equal(s.match(/id="pricing"/g).length, 1, r);
  }
  assert.match(read('build/index.html'), /id="pricing"/);
  assert.match(read('business-diagnosis/index.html'), /name="intent" value="business-diagnosis"/);
});

test('price ladder (PRICE DECISIONS APPLIED 2026-10-30) on industry + calculator pages: 8 levels, no $200 rung, no trial / free month / discount', () => {
  const want = [['Presence', '$100 / month'], ['Presence Plus', '$150 / month'], ['ClientFlow', '$250 / month'], ['Revenue Engine', '$500 / month'], ['Command', '$1,000 / month'], ['Business OS', '$2,000 / month'], ['Multi-Site', '$4,000 / month'], ['Enterprise', '$8,000+ / month']];
  const inds = readdirSync(PUB + 'industries').filter((d) => statSync(PUB + 'industries/' + d).isDirectory());
  assert.ok(inds.length >= 5);
  for (const r of [...inds.map((d) => `industries/${d}/index.html`), 'industries/index.html', 'consequence-calculator/index.html']) {
    const s = read(r), panel = s.slice(s.indexOf('id="pricing"'), s.indexOf('</ul></div>', s.indexOf('id="pricing"')));
    const levels = [...panel.matchAll(/data-level="([^"]+)"><span><b>[^<]+<\/b>(?:<span class=note>[^<]*<\/span>)?<\/span><span class="rv-price">([^<]+)<\/span>/g)].map((m) => [m[1], m[2]]);
    assert.deepEqual(levels, want, r);
    assert.match(panel, /\+ \$30 one-time setup/, r);
    assert.match(panel, /\$10-level WOW Pass/, r); assert.match(panel, /\$20 WOW Pass \(WOW = World of Wealth\)/, r);
    assert.match(panel, /No trial, no free months, no discounts/, r);
    assert.doesNotMatch(s, /\$200 \/ month tier|Starter \$250|Business \$500 one time|free trial|\bWild\b/i, r);
    // Websites: the live checkout packages; their final price is the one open Founder item (stated, not hidden).
    assert.match(s, /Quick Start \$100 · Business Growth \$200 one time/, r);
    assert.match(s, /\$2\.5k · \$5k · \$8k · \$12k · \$15k\+/, r);
  }
});
