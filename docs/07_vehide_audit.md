# VehiDE Audit (E0, part 1)

Audit date: 2026-11-15. Source: `hendrichscullen/vehide-dataset-automatic-vehicle-damage-detection`
(Kaggle), 2.25 GB download, `lastUpdated 2023-08-31`, licence field **Apache 2.0**.
Article: *Powering AI-driven car damage identification based on VehiDE dataset*,
J. Information and Telecommunication (2024), doi 10.1080/24751839.2024.2367387.

Everything below was computed from the extracted archive, not copied from the paper.
Reproduce with:
```bash
node scripts/audit_vehide.mjs data/raw/vehide_extracted 600
node scripts/vehide_group_analysis.mjs data/raw/vehide_extracted
```

---

## 1. Structure and counts (verified)

| Item | Value |
|---|---|
| Annotation files | `0Train_via_annos.json` (35 MB), `0Val_via_annos.json` (7 MB) — VIA (VGG Image Annotator) JSON |
| Image folders | `image/image/` (train), `validation/validation/` (val) |
| Images, train | **11,621** |
| Images, val | **2,324** |
| **Images, total** | **13,945** — matches the published figure exactly |
| Annotation entries | 13,945 (1:1 with files; 0 missing, 0 orphans) |
| Images with ≥1 region | **13,945 (100%)** |
| Images with 0 regions | **0** |
| Total regions | **36,081** |
| Region format | polygon (`all_x`/`all_y` point lists) + `class` |

**Consequence:** VehiDE contains **no undamaged cars at all**. It cannot supply the negative
class on its own; that has to come from another source (DrBimmer `*_Normal`, 1,100 images;
TartesiaDS, 24; Roboflow sets that include intact vehicles).

## 2. Damage classes (7, not 8)

The class names are Vietnamese, abbreviated and unaccented. Translation below is a working
interpretation that **must be confirmed with a Vietnamese speaker or the paper's authors
before it appears in the thesis**.

| Raw class | Interpretation | Regions | % of regions | Images containing it |
|---|---|---|---|---|
| `tray_son` | paint scratch (trầy sơn) | 14,647 | 40.6% | 6,946 |
| `mop_lom` | dent / depression (móp lõm) | 5,681 | 15.7% | 4,426 |
| `rach` | tear / panel split (rách) | 5,509 | 15.3% | 3,849 |
| `mat_bo_phan` | missing part (mất bộ phận) | 2,818 | 7.8% | 2,483 |
| `be_den` | broken lamp (bể đèn) | 2,782 | 7.7% | 2,396 |
| `thung` | puncture / hole (thủng) | 2,423 | 6.7% | 1,888 |
| `vo_kinh` | broken glass (vỡ kính) | 2,221 | 6.2% | 2,133 |
| | **total** | **36,081** | 100% | (multi-label: sums > 13,945) |

The paper states eight categories; the distributed annotations contain **seven**. Either one
class was dropped from the release or two were merged. Log it as a discrepancy and do not
claim eight.

## 3. Hazard coverage — the decisive finding

| Triage-relevant evidence | Class present in VehiDE? |
|---|---|
| Broken glass | **yes** (`vo_kinh`, 2,221 regions) — but no location/severity/zone attribute, so it cannot be graded with the glass rubric without manual re-labeling |
| Missing part | **yes** (`mat_bo_phan`) — sometimes structural, mostly trim |
| Punctured/torn panel | **yes** (`thung`, `rach`) |
| **Tyre damage** (shredded, deflated, tread separation) | **no class** |
| **Wheel damage / displacement** | **no class** |
| **Suspension / structural misalignment** | **no class** |
| **Fluid leakage** | **no class** |
| Lamp broken | yes (`be_den`) — a legality/visibility issue, not a driveability verdict |

So VehiDE is a strong corpus for *visible body and glass damage*, and it gives the project its
volume, resolution and region annotations. It **cannot** by itself teach the "do not drive"
category: the tyre/wheel/fluid evidence that category depends on is simply not annotated.
That gap has to be closed from Roboflow's 18-class set (`flat-tire`, `detachment`) and/or
CarDD (`tire_flat`), or the thesis must adopt the narrower formulation described in §6.

## 4. Image quality (sample of 600)

| Statistic | Value |
|---|---|
| Median width | **1,632 px** |
| Mean width | 1,371 px |
| Range | 204 – 2,016 px |
| Below 600 px | 7 of 600 (1.2%) |

Much better than DrBimmer (median 800 px). Resolution is adequate for panel-level damage and
for reading glass cracks; it is still not adequate for tyre tread depth or thin fluid seepage
observed from a distance, which is a limitation of the photographic method, not of this dataset.

## 5. Split leakage — the most important result of this audit

VehiDE ships a fixed train/val split. Filenames encode a capture timestamp
(`DDMMYYYY_HHMMSSimage<random>.jpg`), and photographs of one vehicle in one appraisal session
are taken seconds apart. Grouping images by timestamp therefore approximates "same vehicle",
which lets us test whether the shipped split is independent.

| Grouping | Groups | Median size | Groups spanning train+val | Val images sharing a group with train |
|---|---|---|---|---|
| by hour | 1,021 | 3 | 501 | **2,089 / 2,139 parsed val = 97.7%** |
| by minute | 4,928 | 2 | 1,266 | **1,707 / 2,139 = 79.8%** |
| no timestamp in filename | 1,160 images | — | ungroupable | — |

Read this carefully: **at minute granularity, ~80% of validation images belong to a session
that also appears in training.** The shipped split is effectively random at image level, so
any metric computed on it is optimistic — the model has usually seen the same car, often the
same bumper, from another angle. At hour granularity it is worse (97.7%), which also tells us
sessions cluster within hours.

Caveats to state in the thesis: timestamp grouping is a *proxy*. Two photos with the same
minute are very likely one vehicle; two photos of one vehicle an hour apart would be missed;
the 1,160 hash-named files cannot be grouped at all.

**Consequences for our protocol**
1. Do **not** use VehiDE's shipped split for reported results. Build our own split by
   session group (grouped stratified split, ~70/15/15), so a vehicle never straddles a
   boundary. Report the shipped-split numbers only as a comparison to show the size of the
   leakage effect — that is a genuinely useful contribution.
2. The 1,160 ungroupable files go to a separate "ungrouped" bucket, used for training only,
   never for test reporting.
3. The independent generalisation test must come from a *different source* (DrBimmer or
   Roboflow), because every VehiDE image is entangled by session.

## 6. What this changes in the research plan

- Volume: 13,945 images secured, 36,081 region annotations — the 10,000 target is met from
  this source alone; the remaining sources now serve *diversity and hazard coverage*, not count.
- The three-class triage target cannot be derived from VehiDE's 7 classes by any mapping.
  It must be produced by (a) expert labeling on a stratified subset, and (b) rule-based
  evidence flags computed from regions + manual attributes (glass zone/size, tyre visibility).
- "Do not drive" evidence still needs an external source. If none arrives, the honest
  fallback is a two-part formulation: (i) visible-hazard-present vs not, (ii)
  coverage-sufficient vs inspect — with the hazmat categories explicitly declared out of scope
  and the limitation written into chapter 8.

## 7. Next audit steps (E0, parts 2–3)

- [ ] Perceptual-hash duplicate detection within VehiDE (expect re-uploads of the same panel
      at different crops), and cross-source overlap against DrBimmer.
- [ ] Glass subset: how many `vo_kinh` regions fall on the windscreen vs side/rear glass, and
      what fraction of them are large enough to matter. Needs a location attribute we do not
      have — plan a 300-image manual attribute pass instead.
- [ ] Tyre/wheel visibility census: sample 500 images, count how often all four wheels are
      visible at all. This decides whether the coverage rule in the rubric is realistic on
      this corpus.
