// Founder price matrix 2026-11-07 (ATH-PRICE-MATRIX-1107) + Founder rulings 2026-11-06/07.
// SUPERSEDES the old "customers never read trials or founding offers" rule, narrowly: exactly these are allowed —
//   1. World Pass: try 7 days free, card required.
//   2. FOUNDING 100: 30 days free after a real first action, no charge.
//   3. FOUNDING 500: the Passport for $10/month while subscribed, with a 1-year price guarantee, first 500 per app (Founder 11-13 night).
// Everything else stays banned: other trials, coupons, promo codes, % off / half off, free months, every-top-tier claims.
// Founder 11-14 (narrow exceptions, newest ruling wins):
//   a. the REFUND RULE, published verbatim on /terms/ and /pricing/ ("... Free trials cancel anytime at no charge.");
//   b. the HOLIDAY offer: code HOLIDAY, half off the first 2 months of APP subscriptions, through New Year's
//      (ends 2027-01-02T05:59:59Z). Only the exact ruled line, only inside a date-gated [data-offer-ends] block,
//      never on ATH website plans / setup-fee pages (/pricing/, /build/), and gone after the deadline.
// Plus: no retired price or tier name (WM Pro OS $50, intro first month, WM Pro App, Spaidbot Pro $20 / Super Max $100,
// WAVEMOTION Living Cinema $75) survives on any built page or in catalog.json.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const PUB = new URL('../public/', import.meta.url).pathname;
const files = (d) => readdirSync(d).flatMap((n) => { const p = join(d, n); return statSync(p).isDirectory() ? files(p) : /\.html$/.test(n) ? [p] : []; });
const pages = files(PUB).filter((f) => !/\/(sites|preview)\//.test(f)); // client sites + prospect previews are not ATH offer pages
const targets = [...pages, PUB + 'catalog.json'];
const REFUND_RULE = 'Setup fees are non-refundable once work begins. Monthly plans cancel anytime and stay active through the paid period; no partial-month refunds. Free trials cancel anytime at no charge.';
const HOLIDAY_ENDS = '2027-01-02T05:59:59Z';
const HOLIDAY_LINE = "Use code HOLIDAY at checkout: half off your first 2 months, through New Year's (Jan 1, 2027, 11:59 PM CT).";
const raw = (f) => readFileSync(f, 'utf8').replace(/&#x27;/g, "'");
// The two Founder 11-14 texts are removed (exact match only) before the bans run; everything else is still checked.
const text = (f) => raw(f).replace(/<[^>]+>/g, ' ').replace(/&amp;/g, '&').replace(/\s+/g, ' ').split(REFUND_RULE).join(' ').split(HOLIDAY_LINE).join(' ');
const cat = JSON.parse(readFileSync(PUB + 'catalog.json', 'utf8'));
const offer = (id) => cat.offers.find((o) => o.id === id);

const OFFER_WORDS = /\btrial|\bdays? free|\bfree for \d+ days|\bfree month|\bhalf price|\bfounding/gi;
function allowed(t, i, word) {
  const before = t.slice(Math.max(0, i - 30), i), win = t.slice(Math.max(0, i - 160), i + 160), w = word.toLowerCase();
  if (/\b(no|not a|never)\b[^.;]{0,25}$/i.test(before)) return 'negation';                       // "No trial, no free month…", "a paid pilot, not a trial"
  if (/days? free/.test(w) && /World Pass/i.test(win) && /\b7[- ]days?\b/.test(win) && /card required/i.test(win)) return 'world-pass-7';
  if (w === 'founding') {
    const after = t.slice(i, i + 12);
    if (/^founding[ -](500|100)\b/i.test(after)) return 'founding-n';
    if (t[i - 1] === '#' && /FOUNDING 500|1-year price guarantee/.test(win)) return 'founding-link';
    return false;
  }
  if (w === 'half price' && /FOUNDING 500/.test(win) && /\$10/.test(win)) return 'founding-500';
  if (/days? free|trial/.test(w) && /FOUNDING 100/.test(win) && /30[- ]days?/.test(win) && /no charge/i.test(win)) return 'founding-100';
  return false;
}

test('only the three Founder-approved trials/offers appear; every other trial, free month or founding wording is banned', () => {
  const kinds = new Set();
  for (const f of targets) {
    const t = text(f);
    for (const m of t.matchAll(OFFER_WORDS)) {
      const k = allowed(t, m.index, m[0]);
      assert.ok(k, `${f.slice(PUB.length)}: "${t.slice(Math.max(0, m.index - 60), m.index + 60)}"`);
      kinds.add(k);
    }
  }
  assert.ok(kinds.has('world-pass-7') && kinds.has('founding-n'), 'the World Pass trial and FOUNDING 500 are on the site');
});

test('no coupons, promo codes, percent-off, half-off, first-month deals or every-top-tier claims anywhere', () => {
  const BANNED = [/coupon/i, /promo code/i, /\d+ ?% off/i, /half off/i, /first month (free|\$\d+|for \$)/i, /intro(ductory)?:? first month/i,
    /every app at its (\$\d+|premium|pro|top)/i, /\b(gets?|includes?|unlocks?|opens?) (the )?(premium|pro|top) tier of every app/i, /free for \d+ days/i, /free trial/i];
  for (const f of targets) { const t = text(f); for (const re of BANNED) assert.doesNotMatch(t, re, `${f.slice(PUB.length)}: ${re}`); }
});

test('retired prices and tier names are gone from every built page and the catalog', () => {
  const RETIRED = [/OS \$50/, /WM Pro OS/, /\bApp \(Basic\)/, /WM Pro App\b/, /Spaidbot[^.]{0,40}\b(?:Personal|Builder|Operations)\b/, /Personal \$19|Builder \$49|Operations \$99/, // Founder 11-13: Spaidbot = Free / Pro $20 / Super Max $100
    // Founder 11-13 night: the WAVEMOTION $75 Living Cinema Studio is KEPT (price book row 13), so "$10–$75" and "Living Cinema" are allowed again.
  ];
  for (const f of targets) { const s = readFileSync(f, 'utf8'); for (const re of RETIRED) assert.doesNotMatch(s, re, `${f.slice(PUB.length)}: ${re}`); }
});

test('catalog.json carries the 2026-11-07 matrix (what the public Spaidbot answers from)', () => {
  assert.equal(cat.version, '2026-11-07.1');
  // Founder 11-14: the product is "Wealthy Mindsets Pro (WM Pro)"; tiers "WM Pro Basic $10 / WM Pro Premium $20 / WM Pro Auto-Trading $30".
  assert.equal(offer('wmp-pro').name, 'Wealthy Mindsets Pro (WM Pro)');
  assert.match(offer('wmp-pro').price, /WM Pro Basic \$10 \/ WM Pro Premium \$20 \/ WM Pro Auto-Trading \$30/);
  assert.match(offer('wmp-tiers').price, /WM Pro Basic \$10 \/ WM Pro Premium \$20 \/ WM Pro Auto-Trading \$30/);
  assert.match(offer('wmp-tiers').fulfillment, /Connect your broker for live data — tastytrade and Webull give you free live data\./);
  assert.match(offer('spaidbot').price, /Pro \$20.*Super Max \$100/); assert.doesNotMatch(offer('spaidbot').price, /\$19|\$49|\$99/); // Founder 11-13
  assert.equal(offer('wm-plans').price, '$10–$75/month'); // Founder 11-13 night: Living Cinema Studio $75 kept
  assert.match(offer('wow-studios-plans').price, /\$29 · \$59 · \$119/);
  assert.match(offer('powertribes-plans').price, /Solo \$29 · Team \$79 · Tower \$179/); assert.doesNotMatch(offer('powertribes-plans').price, /standard|Business OS/); // Founder 11-13: one plain price
  assert.match(offer('creator-passport').price, /\$40 · \$75 · \$100 · \$150/);
  assert.equal(offer('wow-passport').price, 'Free');
  assert.match(offer('wow-founding-500').price, /^\$10\/month while subscribed, with a 1-year price guarantee$/);
  assert.match(offer('wow-world-pass').price, /^\$20\/month · try 7 days free \(card required\)$/);
  for (const id of ['spaidbot', 'wow-studios-plans', 'powertribes-plans', 'creator-passport']) assert.equal(offer(id).buy, 'https://thewow.online/plans', id);
});

test('the ATH Developments business offers are untouched by the matrix', () => {
  assert.match(offer('ath-plans').price, /^\$100 to \$8,000 a month$/);
  for (const id of ['ath-website-starter', 'ath-website-business']) assert.equal(cat.offers.find((o) => o.id === id), undefined, `${id} retired 2026-11-20`);
  assert.match(offer('ath-plans').fulfillment, /Presence \(\$30 today, then \$100 a month\)/);
  assert.match(offer('ath-ai-services').price, /^Speed-to-Lead \$200\/month/);
  assert.equal(offer('ath-garden-check').price, '$20 one time');
});

test('Founder 11-14: the refund rule is published verbatim on /terms/ and /pricing/', () => {
  for (const r of ['terms/index.html', 'pricing/index.html']) assert.ok(raw(PUB + r).includes(REFUND_RULE), r);
});

test('Founder 11-14: HOLIDAY is shown only on app-subscription pages, date-gated, and never on ATH plan / setup-fee pages', () => {
  const open = Date.now() <= Date.parse(HOLIDAY_ENDS);
  for (const f of pages) {
    const s = raw(f), r = f.slice(PUB.length);
    const n = s.split(HOLIDAY_LINE).length - 1;
    if (!n) { assert.doesNotMatch(s, /\bHOLIDAY\b/, r); continue; }
    assert.ok(open, `${r}: HOLIDAY shown after ${HOLIDAY_ENDS}`);
    assert.ok(!/^(pricing|build|websites|start|offer)\//.test(r) && r !== 'index.html', `${r}: HOLIDAY on an ATH plan / setup-fee page`);
    assert.equal((s.match(new RegExp(`class="[^"]*holiday-note[^"]*" data-offer-ends="${HOLIDAY_ENDS}"`, 'g')) || []).length, n, `${r}: every HOLIDAY line is inside a date-gated block`);
    assert.match(s, /not to ATH website plans or setup fees/, r);
  }
  const ids = cat.offers.filter((o) => o.holiday).map((o) => o.id).sort();
  if (open) {
    assert.deepEqual(ids, ['creator-passport', 'powertribes-plans', 'spaidbot', 'wm-plans', 'wmp-pro', 'wmp-tiers', 'wow-founding-500', 'wow-studios-plans', 'wow-world-pass']);
    assert.equal(cat.holiday.ends, HOLIDAY_ENDS);
    assert.ok(cat.holiday.line.startsWith(HOLIDAY_LINE));
    for (const id of ['ath-plans']) assert.equal(offer(id).holiday, undefined, id);
  } else assert.deepEqual(ids, []);
});
