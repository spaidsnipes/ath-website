// A product on hold (commercial/gift-holds.json) must not appear in the built gift guide.
// Run: node --test tests/*.test.mjs   (after python3 build.py)
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const read = (p) => readFileSync(new URL(`../${p}`, import.meta.url), 'utf8');

test('held products are left out of /gifts/', () => {
  const page = read('public/gifts/index.html');
  const feed = JSON.parse(read('commercial/ath-store-snapshot.json'));
  const holds = JSON.parse(read('commercial/gift-holds.json')).holds;
  assert.ok(holds.length > 0);
  for (const h of holds) {
    const p = feed.products.find((x) => String(x.id) === String(h.id));
    assert.ok(p, `hold ${h.id} (${h.title}) is not in the store snapshot`);
    assert.ok(!page.includes(p.product_url), `${h.title} is still on /gifts/`);
  }
});
