// OPTION (Founder decision, 2026-10-21): no built page or the public catalog promises a go-live time.
// Reply-time promises ("replies within one business day") are kept; they are not delivery dates.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const ROOT = new URL('../public/', import.meta.url).pathname;
const files = (dir) => readdirSync(dir).flatMap((n) => { const p = join(dir, n); return statSync(p).isDirectory() ? files(p) : /\.(html|json)$/.test(n) ? [p] : []; });

test('no page and no catalog entry promises when a site goes live', () => {
  const hits = files(ROOT).filter((f) => /live within one business day|can be live before Black Friday|ordered by <b>November 20<\/b>/i.test(readFileSync(f, 'utf8')));
  assert.deepEqual(hits.map((f) => f.slice(ROOT.length)), []);
});
