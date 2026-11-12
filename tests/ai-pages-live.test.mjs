// AI services pages, live-catalog option (2026-10-31): AI receptionist, AI app & site builder, AI chat assistant,
// Growing with AI. A price appears only where the live catalog has it AND a working card checkout (Stripe Payment Link);
// everything else is "Request this service" → the contact form. AI labelled; no trial / free month / discount / testimonials.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const PUB = new URL('../public/', import.meta.url).pathname;
const cat = JSON.parse(readFileSync(PUB + 'catalog.json', 'utf8'));
const LIVE_STRIPE = cat.offers.filter((o) => o.status === 'LIVE' && /^https:\/\/buy\.stripe\.com\//.test(o.buy || ''));
// 2026-11-01: the price book (commercial/price-book.json) is the one source of prices; a card button appears only where its pay_url is set.
const PB = JSON.parse(readFileSync(new URL('../commercial/price-book.json', import.meta.url), 'utf8'));
const PB_ITEMS = PB.services.flatMap((g) => g.items);
const PB_PRICES = new Set(PB_ITEMS.flatMap((i) => [...(String(i.price || '').match(/\$[\d,]+/g) || []), ...(i.hosting_setup ? [`$${i.hosting_setup}`] : [])]));
const PB_PAY = new Set(PB_ITEMS.map((i) => i.pay_url).filter((u) => /^https:\/\/buy\.stripe\.com\//.test(u || '')));
const ROUTES = ['ai/', 'ai/receptionist/', 'ai/site-builder/', 'ai/chat-assistant/', 'ai/growing-with-ai/'];
const page = (r) => readFileSync(PUB + r + 'index.html', 'utf8');
const main = (s) => s.slice(s.indexOf('<main'), s.indexOf('</main>'));
const text = (s) => main(s).replace(/<script(?![^>]*application\/json)[\s\S]*?<\/script>/g, '').replace(/<[^>]+>/g, ' ');

test('the retired $100 / $200 website checkouts are not live; the websites come from the price book', () => {
  for (const id of ['ath-quick-start', 'ath-business-growth']) assert.notEqual(cat.offers.find((o) => o.id === id)?.status, 'LIVE', id);
  assert.ok(PB_ITEMS.some((i) => i.id === 'website-starter' && i.price === '$250 + $25 setup, one time'));
});
for (const r of ROUTES) test(`/${r}: AI labelled; every price is a price-book price; every card button is a price-book or live Stripe link`, () => {
  const s = page(r), t = text(s);
  assert.match(s, /Every ATH AI says it is an AI/);
  for (const p of t.match(/\$[\d,]+/g) || []) assert.ok(PB_PRICES.has(p), `${r}: ${p} is not in the price book`);
  for (const [, u] of main(s).matchAll(/href="(https:\/\/buy\.stripe\.com\/[^"]+)"/g)) assert.ok(PB_PAY.has(u) || LIVE_STRIPE.some((o) => o.buy === u), u);
  for (const re of [/free trial/i, /free month/i, /% off/i, /half off/i, /testimonial/i, /guarantee(d)? (more|bookings|sales|revenue)/i]) assert.doesNotMatch(t.replace(/No trial, no free month and no discount/g, ''), re, `${r}: ${re}`);
  assert.doesNotMatch(main(s), /href="[^"]*workers\.dev/);
});
test('services without a live checkout say "Request this service" and go to the contact form', () => {
  for (const r of ['ai/', 'ai/receptionist/', 'ai/chat-assistant/']) assert.match(page(r), /href="\/contact\/\?intent=services"[^>]*>Request this service/);
  const d = JSON.parse(page('ai/growing-with-ai/').match(/id="grow-data">([\s\S]*?)<\/script>/)[1]);
  for (const r of Object.values(d.recs)) { if (/stripe/.test(r.href)) assert.ok(PB_PAY.has(r.href), r.name); if (r.price) assert.ok(PB_ITEMS.some((i) => i.price === r.price), r.name); }
});
test('chat assistant opens the live Spaidbot; catalog lists AI services as bookable at price-book prices and Spaidbot Build as not active', () => {
  assert.match(page('ai/chat-assistant/'), /data-sb-open/);
  assert.equal(cat.offers.find((o) => o.id === 'ath-ai-services').status, 'BOOKABLE');
  assert.equal(cat.offers.find((o) => o.id === 'spaidbot-build').status, 'NOT_ACTIVE');
});
