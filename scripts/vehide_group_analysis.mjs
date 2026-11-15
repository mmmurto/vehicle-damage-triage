// VehiDE has no vehicle ID, but filenames encode a capture timestamp:
//   DDMMYYYY_HHMMSSimage<random>.jpg
// Photos of the same car in one appraisal session are taken within seconds/minutes of each
// other, so a timestamp-derived "session group" is a defensible proxy for "same vehicle".
//
// This script measures:
//   1. how many session groups exist at several grouping granularities
//   2. whether the dataset's own train/val split leaks groups across the boundary
//      (if it does, published VehiDE numbers are optimistic and our split must differ)
//
// Usage: node vehide_group_analysis.mjs <extracted_root>

import fs from 'fs';
import path from 'path';

const root = process.argv[2] || 'data/raw/vehide_extracted';
const splits = [
  { name: 'train', dir: path.join(root, 'image', 'image') },
  { name: 'val', dir: path.join(root, 'validation', 'validation') },
];

const load = () => {
  const recs = [];
  for (const s of splits) {
    for (const f of fs.readdirSync(s.dir)) {
      const m = f.match(/^(\d{2})(\d{2})(\d{4})_(\d{2})(\d{2})(\d{2})image/);
      if (!m) { recs.push({ split: s.name, file: f, group: null }); continue; }
      const [, dd, mm, yyyy, HH, MM] = m;
      recs.push({
        split: s.name, file: f,
        date: `${yyyy}-${mm}-${dd}`, hour: `${yyyy}${mm}${dd}${HH}`, minute: `${yyyy}${mm}${dd}${HH}${MM}`,
        t: `${yyyy}${mm}${dd}${HH}${MM}${m[6]}`,
      });
    }
  }
  return recs;
};

const recs = load();
const unparsed = recs.filter((r) => r.group === null);
const parsed = recs.filter((r) => r.group !== null);
console.log('images parsed:', parsed.length, '| filenames without timestamp:', unparsed.length);

for (const key of ['hour', 'minute']) {
  const groups = new Map();
  for (const r of parsed) {
    const g = r[key];
    if (!groups.has(g)) groups.set(g, { train: 0, val: 0, files: [] });
    const e = groups.get(g);
    e[r.split]++;
    e.files.push(r.file);
  }
  const sizes = [...groups.values()].map((g) => g.train + g.val).sort((a, b) => a - b);
  const mixed = [...groups.entries()].filter(([, g]) => g.train > 0 && g.val > 0);
  const imagesInMixed = mixed.reduce((a, [, g]) => a + g.train + g.val, 0);
  const imagesInValMixed = mixed.reduce((a, [, g]) => a + g.val, 0);
  const valTotal = parsed.filter((r) => r.split === 'val').length;

  console.log(`\n=== grouping by ${key} ===`);
  console.log('groups:', groups.size);
  console.log('group size: min', sizes[0], 'median', sizes[Math.floor(sizes.length / 2)], 'p90', sizes[Math.floor(sizes.length * 0.9)], 'max', sizes[sizes.length - 1]);
  console.log('single-image groups:', sizes.filter((x) => x === 1).length);
  console.log('groups spanning train+val (leakage):', mixed.length,
    '| images in them:', imagesInMixed,
    '| val images exposed to a seen group:', imagesInValMixed,
    `(${(imagesInValMixed / valTotal * 100).toFixed(1)}% of parsed val)`);
  fs.writeFileSync(`data/raw/vehide_groups_${key}.json`, JSON.stringify(
    [...groups.entries()].map(([k, v]) => ({ group: k, train: v.train, val: v.val })), null, 0));
}

console.log('\nfilenames without a timestamp (need separate handling):', unparsed.length);
console.log('examples:', unparsed.slice(0, 8).map((r) => r.file).join(', '));
console.log('total images:', recs.length);
