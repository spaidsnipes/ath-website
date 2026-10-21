// Founder ship order, 2026-10-21 — the bans this branch clears: no reply- or intake-time promise on
// /start/ and /build/, no "from $X" phrasing in the gift guide, no "book online" in the samples.
// (The go-live promise is cleared by option/no-delivery-time-promise-20261021.)
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const pub = (p) => readFileSync(new URL('../public/' + p, import.meta.url), 'utf8');

test('/start/ and /build/ promise no reply or intake-email time', () => {
  for (const p of ['start/index.html', 'build/index.html']) assert.doesNotMatch(pub(p), /within one business day/, p);
  assert.match(pub('build/index.html'), /ATH emails your intake form after your payment\./);
});

test('the post-payment message promises no reply time', () => {
  assert.doesNotMatch(pub('assets/ath.js'), /within one business day/);
});

test('gift prices never read "from $…"; several variants read "$X+"', () => {
  const g = pub('gifts/index.html');
  assert.doesNotMatch(g, /class="gift-p">from \$/);
  assert.match(g, /class="gift-p">\$11\.99\+</);
});

test('no sample site says "book online"', () => {
  assert.doesNotMatch(pub('sites/fade-lab-sample/index.html'), /book online/i);
});
