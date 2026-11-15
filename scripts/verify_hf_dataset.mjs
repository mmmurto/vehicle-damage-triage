// Reproduces the dataset verification in docs/02_dataset_inventory.md.
// Usage: node verify_hf_dataset.mjs [repoId]
// Requires network access. Uses only the public HF API + datasets-server (no auth).

const repo = process.argv[2] || 'DrBimmer/comprehensive-car-damage';
const api = 'https://huggingface.co/api/datasets/' + repo;
const srv = 'https://datasets-server.huggingface.co';

const j = await (await fetch(api)).json();
const files = (j.siblings || []).map((s) => s.rfilename);
const images = files.filter((f) => /\.(jpe?g|png|webp|bmp)$/i.test(f));

const byDir = {};
for (const f of images) {
  const dir = f.includes('/') ? f.split('/')[0] : '(root)';
  byDir[dir] = (byDir[dir] || 0) + 1;
}

console.log('repo        :', repo);
console.log('revision    :', j.sha, '| lastModified:', j.lastModified);
console.log('gated       :', j.gated, '| private:', j.private);
console.log('tags        :', (j.tags || []).filter((t) => /license|size_categories|task_cat|format/.test(t)).join(', '));
console.log('image files :', images.length, '(repo listing, filesystem view)');

const rows = Object.entries(byDir).sort((a, b) => b[1] - a[1]);
console.log('per folder  :');
for (const [d, n] of rows) console.log('   ', String(n).padStart(6), d);

try {
  const raw = await (await fetch(srv + '/size?dataset=' + encodeURIComponent(repo))).text();
  const size = JSON.parse(raw);
  const n = size?.dataset?.num_rows ?? size?.size?.dataset?.num_rows;
  const sp = size?.splits ?? size?.size?.splits ?? [];
  console.log('datasets-server num_rows:', n, 'splits:', JSON.stringify(sp.map((s) => s.split + ':' + s.num_rows)));
  if (n === undefined) console.log('  raw size payload (first 300 chars):', raw.slice(0, 300));
} catch (e) {
  console.log('size query failed:', e.message);
}

try {
  const st = await (await fetch(srv + '/statistics?dataset=' + encodeURIComponent(repo) + '&config=default&split=train')).json();
  const cols = (st.statistics || []).map((c) => [c.column_name, c.column_type]);
  console.log('columns     :', JSON.stringify(cols));
  for (const c of st.statistics || []) {
    const s = c.column_statistics || {};
    if (s.frequencies) console.log('class counts:', JSON.stringify(s.frequencies));
    if (s.no_label_count !== undefined) console.log('missing labels:', s.no_label_count);
    if (s.min !== undefined) console.log('image dims  : min', s.min, 'max', s.max, 'mean', Math.round(s.mean), 'median', s.median);
  }
} catch (e) {
  console.log('statistics query failed (rate limit? retry later):', e.message);
}

// Consistency check: do the two independent counts agree?
if (images.length && rows.length) {
  console.log('\nCHECK: filesystem image count vs rows — compare the two numbers above; if they differ, the dataset card cannot be trusted.');
}
