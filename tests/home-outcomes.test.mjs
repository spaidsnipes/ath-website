// Homepage "Find your door" (2026-10-21): one door per kind of visitor, with the registry's own price
// and a next step that exists. Founder ruling 2026-10-23: the live Passport sits in WOW OS; WOW World is the
// future metaverse, so the door is named "Passport", never "WOW World Passport".
// and a next step that exists. WM Pro shows only its free guest account until a paid checkout is proven.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';

const PUB = new URL('../public/', import.meta.url).pathname;
const home = readFileSync(PUB + 'index.html', 'utf8');
const reg = JSON.parse(readFileSync(new URL('../commercial/registry.json', import.meta.url), 'utf8'));
const cat = Object.fromEntries(reg.catalog.map((o) => [o.id, o]));
const start = home.slice(home.indexOf('id="start"'), home.indexOf('Built by ATH'));
const cards = [...start.matchAll(/<article class="panel panel-pad card outcome" data-outcome="([^"]+)">([\s\S]*?)<\/article>/g)].map((m) => ({ name: m[1], html: m[2] }));
const price = (c) => (c.html.match(/<b class="outcome-price">([^<]+)<\/b>/) || [])[1];
const href = (c) => (c.html.match(/href="([^"]+)"/) || [])[1];
const unesc = (s) => s.replace(/&amp;/g, '&').replace(/&#x27;|&#39;/g, "'");

test('six doors, after "Who we are" and before "Built by ATH"', () => {
  assert.ok(home.indexOf('Who we are') < home.indexOf('id="start"'));
  assert.deepEqual(cards.map((c) => c.name), ['Quick Start website', 'WAVEMOTION', 'Wealthy Mindsets Pro', 'WOW Academy', 'Passport', 'ATHOS Diagnostic']);
});

test('every price is the registry price of a product that is for sale', () => {
  assert.equal(cards.length, 6);
  const want = { 'Quick Start website': 'ath-quick-start', WAVEMOTION: 'wm-plans', 'WOW Academy': 'wow-academy-free', Passport: 'wow-passport' };
  for (const c of cards) if (want[c.name]) {
    const o = cat[want[c.name]];
    assert.equal(o.status, 'LIVE', c.name);
    assert.equal(unesc(price(c)), o.price, c.name);
  }
});

test('WM Pro shows no paid price anywhere on the homepage', () => {
  const wm = cards.find((c) => c.name === 'Wealthy Mindsets Pro');
  assert.equal(price(wm), 'Free guest account');
  assert.match(cat['wmp-pro'].price, /free guest account/);
  assert.doesNotMatch(home, /\$20\/month/);
});

test('every next step exists: internal pages are built, external ones are ATH products', () => {
  assert.equal(cards.length, 6);
  for (const c of cards) {
    const h = href(c);
    if (h.startsWith('/')) assert.ok(existsSync(PUB + h.replace(/^\//, '').replace(/\/?$/, '/') + 'index.html'), `${c.name} → ${h}`);
    else assert.match(h, /^https:\/\/(www\.wavemotion\.live|wealthymindsetspro\.com|thewow\.online)\//, `${c.name} → ${h}`);
  }
});

test('no door promises what the packages do not deliver', () => {
  assert.ok(start.length > 500, 'the section is missing');
  assert.doesNotMatch(start, /order online|book online|on Google|live tomorrow|built this week|every account|guarantee/i);
});
