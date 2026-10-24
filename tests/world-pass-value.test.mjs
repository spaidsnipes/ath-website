// World Pass value (Founder order 2026-10-24, final). The World Pass is the $20 purchase: pick ONE app at its
// $20 tier, get the $10 tier of every other ATH app, future apps included. It is never free and never unlocks
// the $20/$50 tier of every app. Website packages give one app's $10 tier free for a month, or a step up.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const PUB = new URL('../public/', import.meta.url).pathname;
const read = (r) => readFileSync(PUB + r, 'utf8');
const files = (dir) => readdirSync(dir).flatMap((n) => { const p = join(dir, n); return statSync(p).isDirectory() ? files(p) : /\.html$/.test(n) ? [p] : []; });
const reg = JSON.parse(readFileSync(new URL('../commercial/registry.json', import.meta.url), 'utf8'));

test('the value block sits on every page that sells or explains the pass', () => {
  for (const r of ['index.html', 'path/index.html', 'passport/index.html', 'offer/index.html', 'build/index.html']) {
    const s = read(r);
    assert.match(s, /id="world-pass-value"/, r);
    assert.match(s, /What the \$20 World Pass(<br>| )gets you/, r);
    assert.match(s, /Pick your app at \$20/, r);
    assert.match(s, /Get the \$10 tier of everything else/, r);
    assert.match(s, /Dreamboard/, r);
    assert.match(s, /WOW Academy/, r);
    assert.match(s, /Every new ATH app/, r);
    assert.match(s, /It is never free/, r);
    assert.match(s, /not the \$20 or \$50 tier of every app/, r);
  }
});

test('no page calls the World Pass free or says it unlocks every top tier', () => {
  const BANNED = [/world pass,? free/i, /free (month of )?(the )?world pass/i, /month of the world pass/i, /\$20 or \$50 tier of every app(?!,)/i, /every app at its \$20/i, /Passport \$20/];
  for (const f of [...files(PUB), PUB + 'catalog.json']) {
    const s = readFileSync(f, 'utf8').replace(/not the \$20 or \$50 tier of every app|not<\/b> unlock the \$20 or \$50 tier of every app|does not include the \$20 or \$50 tier of every app|never unlocks the \$20 or \$50 tier of every app/g, '');
    for (const re of BANNED) assert.doesNotMatch(s, re, `${f.slice(PUB.length)}: ${re}`);
  }
});

test('website packages: one app\'s $10 tier free for a month, or step up to the World Pass', () => {
  for (const p of reg.packages) {
    const labels = p.ecosystem.map((e) => e.label);
    assert.ok(labels.includes("Your first month of one app's $10 tier, free ($10 value)"), p.id);
    assert.ok(!labels.some((l) => /World Pass/.test(l)), `${p.id}: World Pass is a step up, never an included extra`);
  }
  const offer = read('offer/index.html');
  for (const id of ['quick-start', 'business-growth']) {
    const sec = offer.slice(offer.indexOf(`id="${id}"`), offer.indexOf('</article>', offer.indexOf(`id="${id}"`)));
    assert.match(sec, /Or step up/, id);
    assert.match(sec, /Step up to the \$20 World Pass/, id);
  }
});
