// Founder, 2026-10-22: WAVEMOTION clips come with its $10/$20/$50/$75 plans.
// The separate clip-bundle menu (10/$75 … 40/$225) is retired everywhere on this site.
import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync, readdirSync, statSync } from "node:fs";
import { join } from "node:path";

const pages = [];
(function walk(d) { for (const f of readdirSync(d)) { const p = join(d, f); statSync(p).isDirectory() ? walk(p) : p.endsWith(".html") && pages.push(p); } })("public");

test("no public page sells clip bundles", () => {
  for (const p of pages) {
    const s = readFileSync(p, "utf8");
    assert.ok(!/\$(125|175|225)\b|clips from \$75|package=clips-\d+/.test(s), `${p} still lists the retired clip-bundle menu`);
  }
});

test("the registry and served catalog mark managed clipping RETIRED", () => {
  for (const f of ["commercial/registry.json", "public/catalog.json"]) {
    const s = readFileSync(f, "utf8");
    const i = s.indexOf('"wm-clips"');
    assert.ok(i > 0);
    assert.match(s.slice(i, i + 600), /"status": "RETIRED"/, f);
  }
});
