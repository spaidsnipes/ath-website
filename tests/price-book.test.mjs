// THE ATH price book (Founder direction 2026-10-31): "a ladder like 100, then 150, 200, 250, 300, 400, 500 … all the
// way up to 8,000. Get a piece of everything we offer, just more and more of it." The Founder saw double prices and
// double names on the front, so: ONE ladder, one name and one price per step, every step adds a little of everything,
// standalone services listed apart, and no card button unless a real Stripe Payment Link exists ("Book a call" until then).
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const PUB = new URL('../public/', import.meta.url).pathname;
const read = (r) => readFileSync(PUB + r, 'utf8');
const book = JSON.parse(readFileSync(new URL('../commercial/price-book.json', import.meta.url), 'utf8'));
const files = (d) => readdirSync(d).flatMap((n) => { const p = join(d, n); return statSync(p).isDirectory() ? files(p) : n === 'index.html' ? [p] : []; });
const site = files(PUB).filter((f) => !/\/(sites|preview)\//.test(f)); // client sites + prospect previews are not ATH price pages
const steps = book.steps;

test('one ladder: 15 steps, $100 → $8,000, the Founder\'s numbers, one name and one price each', () => {
  assert.deepEqual(steps.map((s) => s.monthly), [100, 150, 200, 250, 300, 400, 500, 750, 1000, 1500, 2000, 3000, 4000, 5000, 8000]);
  assert.equal(new Set(steps.map((s) => s.name)).size, steps.length);
  assert.equal(new Set(steps.map((s) => s.key)).size, steps.length);
  for (const n of ['Presence', 'Presence Plus', 'ClientFlow', 'Revenue Engine', 'Command', 'Business OS', 'Multi-Site', 'Enterprise'])
    assert.ok(steps.some((s) => s.name === n), `the decided name ${n} is kept`);
  assert.doesNotMatch(steps.map((s) => s.name).join(' '), /Growth|Wild/, 'the Founder rejected "Growth"; WOW is never "Wild"');
});

test('every step adds a little of everything, nothing is unlimited', () => {
  const more = ['seats', 'receptionist_minutes', 'texts', 'review_requests', 'spaid_daily', 'wavemotion_clips'];
  for (let i = 1; i < steps.length; i++) {
    const a = steps[i - 1], b = steps[i];
    for (const k of more) assert.ok(b[k] > a[k], `${b.key}.${k} must be more than ${a.key}`);
    for (const k of ['lines', 'locations', 'world_passes', 'website_pages', 'office_floors', 'office_meeting_rooms']) assert.ok(b[k] >= a[k], `${b.key}.${k}`);
    for (const f of a.features) assert.ok(b.features.includes(f), `${b.key} keeps ${f}`);
  }
  for (const s of steps) {
    for (const k of ['wow_pass', 'office', 'wavemotion', 'spaidbot', 'wm_pro', 'website']) assert.ok(s[k], `${s.key} has ${k}`);
    assert.doesNotMatch(JSON.stringify(s), /unlimited/i, s.key);
    assert.equal(s.wow_pass_level, s.monthly >= 250 ? '$20 WOW Pass' : '$10-level WOW Pass', s.key);
  }
});

test('the pricing page shows ONLY the ladder plus a separate services list', () => {
  const s = read('pricing/index.html');
  const cards = [...s.matchAll(/<article class="panel pc[^"]*" id="plan-([a-z_]+)"/g)].map((m) => m[1]);
  assert.deepEqual(cards, steps.map((p) => p.key));
  for (const p of steps) {
    const sec = s.slice(s.indexOf(`id="plan-${p.key}"`), s.indexOf('</article>', s.indexOf(`id="plan-${p.key}"`)));
    assert.ok(sec.includes(`$${p.monthly.toLocaleString('en-US')}<span> a month</span>`), p.key);
    if (p.pay_url) assert.ok(sec.includes(`href="${p.pay_url}"`), p.key);
    else { assert.match(sec, /Book a call/, p.key); assert.doesNotMatch(sec, /stripe\.com/, p.key); }
  }
  assert.ok(s.indexOf('id="services"') > s.lastIndexOf('id="plan-'), 'services sit after, and apart from, the ladder');
  assert.match(s, /Services on their own/);
  assert.doesNotMatch(s, /class="pl"|wpv-grid|What the \$20 World Pass/, 'no second ladder on the page');
});

test('no duplicate prices on the front door: the retired $100 / $200 one-time websites are gone from every ATH page', () => {
  for (const f of site) {
    const s = readFileSync(f, 'utf8'), r = f.slice(PUB.length);
    assert.doesNotMatch(s, /Quick Start (website|\$)|Business Growth|\$100 one time|\$200 one time|Start for \$100/, r);
    assert.doesNotMatch(s, /buy\.stripe\.com\/(3cI4gA1KkdPkbvJ2oG97G00|eVq4gAcoY4eKarF1kC97G01)/, r);
  }
});

test('no trials, free months or discounts in the book; the only free thing is the diagnosis', () => {
  const raw = JSON.stringify(book);
  assert.doesNotMatch(raw.replace(/No trials?, no free months?, no discounts?/g, '').replace(/not a trial/g, ''), /trial|free month|discount|% off|half off/i);
  const free = book.services.flatMap((g) => g.items).filter((i) => /^Free$/.test(i.price));
  assert.deepEqual(free.map((i) => i.id), ['business-diagnosis']);
});

test('every card button is a real Stripe Payment Link or a booking request, never a made-up checkout', () => {
  for (const p of steps) assert.ok(p.pay_url === '' || /^https:\/\/buy\.stripe\.com\/[A-Za-z0-9_]+$/.test(p.pay_url), p.key);
  for (const i of book.services.flatMap((g) => g.items)) if (i.pay_url) assert.match(i.pay_url, /^https:\/\/(buy\.stripe\.com\/|www\.wavemotion\.live\/|thewow\.online\/|wealthymindsetspro\.com\/)/, i.id);
});
