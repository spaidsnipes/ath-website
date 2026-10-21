// Every built page must fit a 390px phone without sideways scrolling.
// Run: node --test tests/*.test.mjs  (needs Playwright + Chromium; skips cleanly without them)
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createServer } from 'node:http';
import { readFile, readdir, stat } from 'node:fs/promises';
import { join, extname } from 'node:path';

const ROOT = new URL('../public/', import.meta.url).pathname;
const TYPES = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.svg': 'image/svg+xml', '.webp': 'image/webp', '.png': 'image/png', '.json': 'application/json' };

async function pages(dir, base = '/') {
  const out = [];
  for (const name of await readdir(dir)) {
    const p = join(dir, name);
    if ((await stat(p)).isDirectory()) out.push(...await pages(p, base + name + '/'));
    else if (name === 'index.html') out.push(base);
  }
  return out;
}

let chromium;
try { ({ chromium } = await import(process.env.PLAYWRIGHT_MODULE || 'playwright')); } catch {}

test('no page scrolls sideways at 390px', { skip: !chromium && 'playwright not installed' }, async () => {
  const server = createServer(async (req, res) => {
    let path = decodeURIComponent(new URL(req.url, 'http://x').pathname);
    if (path.endsWith('/')) path += 'index.html';
    try { const body = await readFile(join(ROOT, path)); res.writeHead(200, { 'content-type': TYPES[extname(path)] || 'application/octet-stream' }); res.end(body); }
    catch { res.writeHead(404); res.end(); }
  }).listen(0);
  const port = server.address().port;
  const browser = await chromium.launch(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {});
  const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
  // External images (Shopify CDN) are irrelevant to layout: their width/height attributes reserve the box.
  await page.route(/^https?:\/\/(?!127\.0\.0\.1)/, r => r.abort());
  const wide = [];
  for (const path of await pages(ROOT)) {
    await page.goto(`http://127.0.0.1:${port}${path}`, { waitUntil: 'load' });
    const w = await page.evaluate(() => document.documentElement.scrollWidth);
    if (w > 392) wide.push(`${path} is ${w}px wide`);
  }
  await browser.close(); server.close();
  assert.deepEqual(wide, []);
});
