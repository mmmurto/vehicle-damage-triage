// Audit VehiDE (or any VIA-format damage dataset): class distribution, images per class,
// unannotated images, filename/annotation agreement, and image size statistics.
//
// Usage: node audit_vehide.mjs <extracted_root> [sampleForDims]
// Writes: data/raw/vehide_audit.json and prints a summary.

import fs from 'fs';
import path from 'path';

const root = process.argv[2] || 'data/raw/vehide_extracted';
const dimSample = parseInt(process.argv[3] || '600', 10);

const splits = [
  { name: 'train', json: '0Train_via_annos.json', imgDir: path.join(root, 'image', 'image') },
  { name: 'val', json: '0Val_via_annos.json', imgDir: path.join(root, 'validation', 'validation') },
];

const out = { root, generated: new Date().toISOString(), splits: {} };
const globalClassImages = new Map();
const globalClassRegions = new Map();

for (const s of splits) {
  const raw = JSON.parse(fs.readFileSync(path.join(root, s.json), 'utf8'));
  const names = Object.keys(raw);
  const onDisk = new Set(fs.readdirSync(s.imgDir));

  let regions = 0, withRegions = 0, empty = 0, missingFile = 0;
  const classRegions = new Map();
  const classImages = new Map();
  const noRegionFiles = [];

  for (const n of names) {
    const entry = raw[n];
    const regs = entry.regions || [];
    const file = entry.name || n;
    if (!onDisk.has(file)) missingFile++;
    if (regs.length === 0) { empty++; noRegionFiles.push(file); }
    else withRegions++;
    regions += regs.length;
    const seen = new Set();
    for (const r of regs) {
      const cls = r.class || r.region_attributes?.class || '(none)';
      classRegions.set(cls, (classRegions.get(cls) || 0) + 1);
      globalClassRegions.set(cls, (globalClassRegions.get(cls) || 0) + 1);
      if (!seen.has(cls)) {
        seen.add(cls);
        classImages.set(cls, (classImages.get(cls) || 0) + 1);
        globalClassImages.set(cls, (globalClassImages.get(cls) || 0) + 1);
      }
    }
  }

  out.splits[s.name] = {
    annotationEntries: names.length,
    imagesOnDisk: onDisk.size,
    missingFiles: missingFile,
    imagesWithRegions: withRegions,
    imagesWithoutRegions: empty,
    totalRegions: regions,
    classRegions: Object.fromEntries([...classRegions].sort((a, b) => b[1] - a[1])),
    classImages: Object.fromEntries([...classImages].sort((a, b) => b[1] - a[1])),
    unannotatedExamples: noRegionFiles.slice(0, 10),
  };
}

out.combined = {
  images: Object.values(out.splits).reduce((a, s) => a + s.annotationEntries, 0),
  filesOnDisk: Object.values(out.splits).reduce((a, s) => a + s.imagesOnDisk, 0),
  regions: Object.values(out.splits).reduce((a, s) => a + s.totalRegions, 0),
  classRegions: Object.fromEntries([...globalClassRegions].sort((a, b) => b[1] - a[1])),
  classImages: Object.fromEntries([...globalClassImages].sort((a, b) => b[1] - a[1])),
};

// image dimension sample
if (dimSample > 0) {
  let sharp;
  try { sharp = (await import('sharp')).default; } catch { sharp = null; }
  if (sharp) {
    const files = [];
    for (const s of splits) {
      const onDisk = fs.readdirSync(s.imgDir);
      const step = Math.max(1, Math.floor(onDisk.length / (dimSample / 2)));
      for (let i = 0; i < onDisk.length && files.length < dimSample; i += step) files.push(path.join(s.imgDir, onDisk[i]));
    }
    const dims = [];
    for (const f of files) {
      try { const md = await sharp(f).metadata(); if (md.width) dims.push([md.width, md.height]); } catch {}
    }
    dims.sort((a, b) => a[0] - b[0]);
    const w = dims.map((d) => d[0]);
    out.dimensions = {
      sampled: dims.length,
      minWidth: w[0], maxWidth: w[w.length - 1],
      medianWidth: w[Math.floor(w.length / 2)],
      meanWidth: Math.round(w.reduce((a, b) => a + b, 0) / w.length),
      under600px: w.filter((x) => x < 600).length,
    };
  } else {
    out.dimensions = { error: 'sharp not installed' };
  }
}

fs.mkdirSync('data/raw', { recursive: true });
fs.writeFileSync('data/raw/vehide_audit.json', JSON.stringify(out, null, 1));

for (const [name, s] of Object.entries(out.splits)) {
  console.log(`\n[${name}] entries=${s.annotationEntries} onDisk=${s.imagesOnDisk} regions=${s.totalRegions}`);
  console.log(`  with regions: ${s.imagesWithRegions} | without: ${s.imagesWithoutRegions} | missing files: ${s.missingFiles}`);
  console.log('  classes (regions):', JSON.stringify(s.classRegions));
}
console.log('\nCOMBINED images:', out.combined.images, 'files:', out.combined.filesOnDisk, 'regions:', out.combined.regions);
console.log('classes:', JSON.stringify(out.combined.classRegions, null, 0));
if (out.dimensions) console.log('dims:', JSON.stringify(out.dimensions));
