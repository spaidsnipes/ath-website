// The $100 / $200 site packages, described as sites/DELIVERY.md builds them (2026-10-21).
// A client site links to the booking or ordering the business already uses; ATH does not build one.
// The site factory has items, gallery and text sections — no forms. Reviews are never added unless the
// owner supplies them. A client site is noindex until it has its own domain, so no page promises Google.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const ROOT = new URL('../public/', import.meta.url).pathname;
const files = (dir) => readdirSync(dir).flatMap((n) => { const p = join(dir, n); return statSync(p).isDirectory() ? files(p) : /\.html$/.test(n) ? [p] : []; });
const pages = files(ROOT).filter((f) => !f.includes('/sites/'));
const rel = (f) => f.slice(ROOT.length);

const OVERCLAIMS = [
  /pages with booking or ordering/i,      // reads as if ATH builds booking/ordering
  /order request form|quote form/i,        // the factory has no form section
  /search setup/i,                         // not part of the delivery runbook
  /come up on Google/i,                    // client sites are noindex until they have a domain
  /services and reviews in one tap/i,      // reviews only if the owner supplies them
  /Get found by the customers/i,
  /puts you in front of the people already looking/i,
];

test('the scanned pages are really there', () => {
  assert.ok(pages.length >= 30, `only ${pages.length} pages scanned`);
  assert.ok(pages.some((f) => rel(f) === 'websites/tulsa/restaurants-food-trucks/index.html'));
});

for (const re of OVERCLAIMS) {
  test(`no page says ${re}`, () => {
    assert.deepEqual(pages.filter((f) => re.test(readFileSync(f, 'utf8'))).map(rel), []);
  });
}

test('the $200 package says what it links to', () => {
  const free = readFileSync(join(ROOT, 'free-look/index.html'), 'utf8');
  assert.match(free, /Up to 3 pages, linked to the booking or ordering you already use/);
});

test('city pages tell the owner when search engines list the site', () => {
  const city = readFileSync(join(ROOT, 'websites/bixby/bakeries/index.html'), 'utf8');
  assert.match(city, /Search engines list it once it is on your own domain \(about \$12 a year, paid to the registrar\)/);
});

test('every client site without its own domain stays out of search', () => {
  const sites = files(join(ROOT, 'sites')).filter((f) => f.endsWith('index.html'));
  assert.ok(sites.length >= 1);
  for (const f of sites) assert.match(readFileSync(f, 'utf8'), /<meta name="robots" content="noindex">/, rel(f));
});
