// The catalog Spaidbot reads (2026-10-21): the store gets no "from $…" floor and no item count, both of
// which go stale with every listing. Founder ship order bans "from $11.99" and "from $4.99" in copy.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const cat = JSON.parse(readFileSync(new URL('../public/catalog.json', import.meta.url), 'utf8'));
const store = cat.offers.find((o) => o.id === 'wow-ath-store');

test('the store line names no floor price and no item count', () => {
  assert.ok(store, 'wow-ath-store is in the catalog');
  assert.equal(store.price, 'priced per item on each product page');
  assert.doesNotMatch(store.name, /\d+\s*items/);
  assert.doesNotMatch(JSON.stringify(cat), /from \$11\.99|from \$4\.99/);
});

test('the catalog version moved, so readers can tell it changed', () => {
  assert.equal(cat.version, '2026-10-21.2');
});
