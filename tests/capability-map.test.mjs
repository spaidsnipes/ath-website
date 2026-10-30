// SP-055 / R41 capability map, SP-085 offer stack, SP-081 Spaidbot + ticker, SP-082 sample ribbon (2026-10-23).
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const PUB = new URL('../public/', import.meta.url).pathname;
const read = (r) => readFileSync(PUB + r, 'utf8');
const reg = JSON.parse(readFileSync(new URL('../commercial/registry.json', import.meta.url), 'utf8'));
const files = (d) => readdirSync(d).flatMap((n) => { const p = join(d, n); return statSync(p).isDirectory() ? files(p) : /\.(html|json|js)$/.test(n) ? [p] : []; });
const home = read('index.html'), eco = read('ecosystem/index.html'), offer = read('offer/index.html');
const OWNERS = /^(ATH|ATH Web Studio|ATH Commerce|WAVEMOTION|ATHOS|Atlas|SPAID Business|PowerTribes|WOW OS|Wealthy Mindsets Pro)$/;
const cards = [...eco.matchAll(/<article class="cap" data-cap="([^"]+)" data-status="(\w+)">([\s\S]*?)<\/article>/g)].map((m) => ({ name: m[1], st: m[2], html: m[3] }));

test('the full map: every capability has an owner, an honest status, a price or quote, and a real next step', () => {
  assert.ok(cards.length >= 20, `${cards.length} capability cards`);
  for (const c of cards) {
    const owner = c.html.match(/class="cap-owner">([^<]+)</)[1].replace(/&amp;/g, '&');
    for (const o of owner.split(/\s*[+·]\s*/)) assert.match(o, OWNERS, `${c.name}: owner ${o}`);
    assert.ok(['live', 'inc', 'quote', 'dev', 'nb'].includes(c.st), c.name);
    assert.match(c.html, /class="cap-price">[^<]+</, `${c.name} has no price line`);
    const href = c.html.match(/class="cap-go" href="([^"]+)"/)[1];
    if (href.startsWith('/')) assert.ok(existsSync(PUB + href.split(/[?#]/)[0].replace(/^\//, '') + 'index.html'), `${c.name} → ${href}`);
    else assert.match(href, /^https:\/\/(www\.wavemotion\.live|wealthymindsetspro\.com|thewow\.online)\//, `${c.name} → ${href}`);
    if (c.st === 'dev') assert.match(c.html, /Not sold yet/, `${c.name} is in development but shows a price`);
  }
});

test('every dollar figure on the map comes from the registry', () => {
  const known = new Set(JSON.stringify(reg).match(/\$[\d,]+/g).concat(reg.packages.flatMap((p) => [p.price, p.price_max]).filter(Boolean).map((n) => '$' + n.toLocaleString('en-US'))));
  known.add('$12'); // registrar fee, already stated on the city pages
  for (const c of cards) for (const d of c.html.match(/\$[\d,]+/g) || []) assert.ok(known.has(d), `${c.name}: ${d} is not in the registry`);
});

test('homepage shows the grouped map, the comparison and the $100 → $8,000 ladder', () => {
  assert.equal((home.match(/<article class="ct" id="tile-/g) || []).length, 6);
  assert.match(home, /Everything a content platform gives you/);
  const steps = [...home.matchAll(/<span class="pl-price">([^<]+)<\/span>/g)].map((m) => m[1]);
  assert.equal(steps[0], '$100'); assert.equal(steps.at(-1), '$8,000'); assert.equal(steps.length, reg.packages.length);
});

test('the comparison names no competitor and admits what is not built', () => {
  for (const f of files(PUB)) assert.doesNotMatch(readFileSync(f, 'utf8'), /contentstack/i, f);
  assert.match(eco, /Not built yet/);
});

test('one owner per job, and no new standalone Content OS brand', () => {
  assert.equal((eco.match(/<article class="panel panel-pad own">/g) || []).length, 7);
  for (const f of files(PUB)) assert.doesNotMatch(readFileSync(f, 'utf8'), /Content OS/, f);
});

test('WOW OS is the live system; WOW World is only ever the future', () => {
  for (const r of ['index.html', 'ecosystem/index.html', 'passport/index.html', 'path/index.html', 'work/index.html', 'company/index.html']) {
    for (const m of read(r).matchAll(/WOW World(?! Pass)[\s\S]{0,160}/g)) assert.match(m[0], /future|Future/, `${r}: ${m[0].slice(0, 80)}`);
  }
});

test('offer stack: real inclusions from the registry, extras not switched on kept apart, no urgency', () => {
  for (const p of reg.packages.filter((x) => x.pay_url)) {
    const sec = offer.slice(offer.indexOf(`id="${p.id}"`), offer.indexOf('</article>', offer.indexOf(`id="${p.id}"`)));
    for (const i of p.includes) assert.ok(sec.includes(i.replace(/&/g, '&amp;')), `${p.id}: ${i}`);
    const notCounted = sec.slice(sec.indexOf('Not counted'));
    for (const e of p.ecosystem.filter((e) => e.state !== 'LIVE')) assert.ok(notCounted.includes(e.label.replace(/\s*\(\$\d+ value\)/, '')), `${p.id}: ${e.label} must sit under Not counted`);
    assert.ok(sec.includes(p.pay_url));
  }
  assert.doesNotMatch(offer.replace(/no countdown|no “today only”/gi, ''), /today only|countdown|hurry|ends (soon|tonight)|only \d+ left|act now/i);
});

test('Spaidbot shrinks over the hero; the top ticker scrolls instead of being cut off', () => {
  // 2026-10-30: the site uses the one ATHOS embed; data-compact-hero="1" keeps the SP-081 round-dot-over-the-hero rule.
  const css = readFileSync(PUB + 'assets/ath.css', 'utf8');
  assert.match(home, /<script src="https:\/\/mission\.abovethehilldev\.online\/spaidbot\.js"[^>]* data-compact-hero="1"/);
  assert.match(home, /<div class="mantra" aria-hidden="true"><span class="mq"><span>/);
  assert.match(css, /@keyframes mantra/);
});

test('every sample site carries a pinned SAMPLE ribbon', () => {
  const dirs = readdirSync(PUB + 'sites').filter((d) => d.endsWith('-sample'));
  assert.ok(dirs.length >= 3);
  for (const d of dirs) {
    const s = read(`sites/${d}/index.html`);
    assert.match(s, /<body class="is-sample"><div class="sample-ribbon" role="note"[^>]*><b>Sample<\/b>/, d);
    assert.match(s, /\.sample-ribbon\{position:sticky;top:0/, d);
  }
});

test('World Pass rule (Founder, 2026-10-23, corrected 10-24) is stated with its live switch-on line, and the capacity note stays off', () => {
  for (const r of ['ecosystem/index.html', 'passport/index.html', 'path/index.html']) {
    const s = read(r);
    assert.match(s, /your passport across the whole ATH ecosystem: Premium of the one app you choose — WAVEMOTION, WealthyMindsets Pro and more — and Basic of every other ATH app, including apps still to come/, r);
    // 2026-10-24: WAVEMOTION and WM Pro read the one World Pass from WOW OS and switch their tier on.
    assert.match(s, /Each app switches its tier on from your pass when you open it: WAVEMOTION and WealthyMindsets Pro today/, r);
    assert.doesNotMatch(s, /as each app connects/, r);
  }
  for (const r of ['index.html', 'ecosystem/index.html', 'offer/index.html']) assert.doesNotMatch(read(r), /3 clients/, r);
});
