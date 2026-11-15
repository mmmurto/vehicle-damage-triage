// Rebuilds pilot/pilot_sheet_36_images.png from the pinned sample list.
// Usage (from repo root): node scripts/make_pilot_sheet.mjs
// Needs: sharp (bun add sharp / npm i sharp)

import fs from 'fs';
import path from 'path';
import sharp from 'sharp';

const REPO = 'DrBimmer/comprehensive-car-damage';
const OUT = path.join(process.cwd(), 'pilot');
const PINNED = JSON.parse(fs.readFileSync(path.join(OUT, 'sample_meta.json'), 'utf8')).map((r) => r.file);

const T = 230, COLS = 6;
const tiles = [];
const meta = [];
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

for (let i = 0; i < PINNED.length; i++) {
  const file = PINNED[i];
  const url = 'https://huggingface.co/datasets/' + REPO + '/resolve/main/' + encodeURI(file);
  let buf = null;
  for (let a = 0; a < 4 && !buf; a++) {
    try {
      const r = await fetch(url);
      if (r.ok) buf = Buffer.from(await r.arrayBuffer()); else await sleep(700 * (a + 1));
    } catch { await sleep(700 * (a + 1)); }
  }
  if (!buf) { console.log('FAIL', file); continue; }
  await sleep(250);

  const md = await sharp(buf).metadata();
  const img = await sharp(buf).resize(T - 8, T - 24, { fit: 'inside', background: '#111' }).toBuffer();
  const tag = file.replace(/\//g, ' ') + ' ' + md.width + 'x' + md.height;
  const svg = '<svg width="' + T + '" height="' + T + '" xmlns="http://www.w3.org/2000/svg">'
    + '<rect width="' + T + '" height="' + T + '" fill="#1b1b1b"/>'
    + '<text x="6" y="16" font-family="monospace" font-size="12" fill="#7CCFFF">' + tag + '</text></svg>';
  const tile = await sharp(Buffer.from(svg)).composite([{ input: img, top: 22, left: 4 }]).png().toBuffer();
  const idx = meta.length;
  tiles.push({ input: tile, top: Math.floor(idx / COLS) * T, left: (idx % COLS) * T });
  meta.push({ file, w: md.width, h: md.height, bytes: buf.length });
}

const rows = Math.ceil(meta.length / COLS);
await sharp({ create: { width: COLS * T, height: rows * T, channels: 3, background: '#111' } })
  .composite(tiles).png().toFile(path.join(OUT, 'pilot_sheet_36_images.png'));

console.log('wrote pilot/pilot_sheet_36_images.png with', meta.length, 'tiles');
