// Mansion Garden Check (Founder order 2026-10-24): a one-time live website check, "like an oil change".
// One price number in the registry drives every page and the catalog entry Spaidbot reads. With no
// Stripe Payment Link pasted, it is booked by request (BOOKABLE), never shown as card-payable.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const PUB = new URL('../public/', import.meta.url).pathname;
const read = (r) => readFileSync(PUB + r, 'utf8');
const reg = JSON.parse(readFileSync(new URL('../commercial/registry.json', import.meta.url), 'utf8'));
const cat = JSON.parse(read('catalog.json'));
const gc = reg.garden_check;
const price = '$' + gc.price.toLocaleString('en-US');
const link = (gc.payment_link || '').trim();

test('one price number: the catalog entry is generated from registry garden_check.price', () => {
  const o = cat.offers.find((x) => x.id === gc.catalog_id);
  assert.ok(o, 'Garden Check is in catalog.json');
  assert.equal(o.price, `${price} one time`);
  assert.equal(o.status, link ? 'LIVE' : 'BOOKABLE');
  assert.equal(o.buy, link || 'https://abovethehilldev.online/garden-check/');
  assert.ok(cat.statuses[o.status], `status ${o.status} is explained`);
  assert.equal(JSON.stringify(reg.catalog).includes('garden'), false, 'no second, hand-typed catalog line');
});

test('the Garden Check page: oil-change framing, every check, the privacy line, fixes quoted apart', () => {
  const s = read('garden-check/index.html');
  assert.match(s, /Like an oil change for your website: pull in, 5–10 minutes, done\./);
  for (const c of gc.checks) assert.ok(s.includes(c.replace(/&/g, '&amp;')), c);
  for (const t of ['Your logins stay yours: we never ask for passwords', 'Everything we look at stays private between us', 'You can watch the whole check live', 'Fixes are quoted separately', 'Zoom', 'Google Meet', 'Mansion Garden Pass', 'included with Passport Pro']) assert.ok(s.includes(t), t);
  assert.match(s, /<input type="hidden" name="package" id="l-package" value="garden-check">/);
  assert.doesNotMatch(s.slice(s.indexOf('<main'), s.indexOf('</main>')), /ATHOS/, 'describe a diagnostic, not the internal method');
  if (link) assert.ok(s.includes(`href="${link}"`));
  else { assert.match(s, /Book a Garden Check/); assert.doesNotMatch(s, /buy\.stripe\.com/); assert.match(s, /Nothing is charged by this form/); }
});

test('it sits beside Quick Start and Business Growth: home map + ladder note, offer page, build pricing, catalog_js', () => {
  const home = read('index.html');
  assert.match(home, /data-cap="Website health check"|ct-name">Website health check</);
  assert.match(home, /Already have a site\? Start smaller: the <a class="gold" href="\/garden-check\/">Mansion Garden Check<\/a> is \$\d+ one time/);
  for (const r of ['offer/index.html', 'build/index.html']) { const s = read(r); assert.match(s, /Mansion Garden Check/, r); assert.ok(s.includes(price), r); }
  for (const r of ['start/index.html', 'contact/index.html']) assert.match(read(r), /"garden-check": \{"label": "Mansion Garden Check/, r);
  assert.match(read('start/index.html'), /id="start-h1"/);
  assert.match(read('assets/ath.js'), /qs\.get\("offer"\)/, 'the Stripe redirect ?offer=garden-check preselects it');
});
