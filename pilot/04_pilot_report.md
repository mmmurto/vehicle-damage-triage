# Labeling Pilot — design, provisional screening, protocol

Status: **sample built, labels not yet assigned.** No agreement numbers exist yet; nothing in
this file should be quoted as a result.

---

## 1. Why a pilot, and what it must decide

Before scaling to thousands of images, the pilot has to answer four practical questions:

1. Can two people apply the three-category rubric to the same image and agree? (If not, the
   rubric is wrong, not the data.)
2. How often does the coverage rule in the rubric force "inspection required"? If that is
   > 60%, the target class becomes the default and the evaluation is uninformative.
3. Does the source data contain examples of each category at all — in particular, does
   *any* image show a "do not drive" finding?
4. How long does one image take? That determines whether 10,000 images is feasible.

---

## 2. Sample

| Property | Value |
|---|---|
| Source | `DrBimmer/comprehensive-car-damage` (revision `355b0990`) |
| Size | 36 images |
| Design | 6 per source class (all 6 classes), systematic spread through each class's numeric filename order (fractions 0.05, 0.20, 0.35, 0.50, 0.65, 0.80) |
| Files | `pilot/pilot_sample_manifest.csv` (one row per image, label columns empty) |
| Contact sheet | `pilot/pilot_sheet_36_images.png` (6 × 6, thumbnail 230 px with filename and pixel size) |
| Sampling limitation | systematic, not random; not stratified by damage severity (unknown before labeling); 36 images cannot support inference, only instrument design |
| Blinding | the manifest keeps `source_class` in a separate column so the labeling tool can hide it; do not sort or filter by it |

Reproduce: `node scripts/make_pilot_sheet.mjs` (writes the sheet and `sample_meta.json`).

---

## 3. Provisional screening (thumbnail-level, single reviewer)

These are **screening observations from a 230 px contact sheet**, made to find instrument
problems early. They are not labels and must be re-checked at full resolution.

**Photography.** All 36 images are marketplace/dealer listing photography: cars parked on
forecourts, in workshop bays or on streets; number plates obscured by dealer overlays (some
reading "Encarr"); tight framing; most files 800×600, a few 960×720 or wide crops
(1226×616, 1640×1356). Images carry visible JPEG artefacts at this size.

**Coverage.** No image is a deliberate multi-view set. Wheels are partly visible in roughly
half the images; **no image shows a tyre close-up, an underbody view, or an interior view.**
Fluid leaks cannot be assessed at all because the camera is above bonnet height.

**Hazard findings.** In these 36 images no shredded tyre, no visibly displaced wheel, no
fragmented driver-side glass, and no active fluid drip is visible. Under the v1.0 rubric the
whole sample would land in "low visible concern" or "inspection required".

**Label noise / ambiguity.**
- `F_Crushed` (400 images) is loosely defined: at least two of the six sampled images
  (`FC_81`, `FC_321`) show front-end views with no damage visible at thumbnail scale.
- `F_Breakage` (500 images) mostly shows cracked or detached bumper covers and broken lamp
  lenses — cosmetic-to-moderate, i.e. the same practical triage outcome as "Crushed".
  The Crushed/Breakage distinction therefore does not map onto safety relevance.
- Filename prefix does not guarantee the view: `FC_261` is a rear three-quarter view of a
  hatchback, `RC_106` shows a front corner and a door.
- Several `R_Normal` images show light bumper scuffs or paint damage. "Normal" here appears
  to mean "no reportable claim", not "no defects" — which is exactly the gap the triage
  rubric is meant to close.

**Implication for the sampling frame.** The dataset yields, at best, two usable triage
categories. A third category ("do not drive") will be near-empty. Consequences:
- the hazard-miss denominator will be tiny unless a second source with real hazard imagery is
  added (VehiDE is the strongest candidate; Roboflow's `Flat Tire` class is the only verified
  public source with an explicit flat-tyre label);
- class imbalance must be handled by design (case-level labels, weighted metrics, reporting
  counts not only rates);
- a thesis that reports only accuracy would be misleading; the metric plan must be
  hazard-miss rate with counts and confidence intervals.

**Diagnostic value of the source.** High for "is there visible damage and where". Low for
"is this vehicle safe to move". Say this once, clearly, in chapter 3 and again in chapter 8.

---

## 4. Protocol to execute now (≈ 60–90 minutes)

1. Two annotators, independently, no discussion.
2. Open `pilot/pilot_sheet_36_images.png` **or** the individual full-resolution images
   (recommended for anything beyond a first pass; the sheet is 230 px per tile).
3. Fill the label columns of `pilot/pilot_sample_manifest.csv` per `docs/03_labeling_guide.md`:
   `view_visible`, `visible_damage_types`, `glass_location`, `glass_severity_mm`,
   `triage_label`, `hazard_evidence_cited`, `needs_more_views`, `annotator_notes`.
4. `triage_label` ∈ {`low_visible_concern`, `do_not_drive`, `inspection_required`}.
5. Record `seconds_spent` per image (add the column; it is missing from the manifest by design
   so that it is not pre-filled).
6. Adjudication meeting: every disagreement is discussed and the reason logged.
7. Compute and report: raw agreement, Cohen's κ, per-class agreement, the confusion matrix of
   disagreements, mean seconds per image, and the distribution of `triage_label`.

### Results table to fill (leave empty until run)

| Metric | Annotator A | Annotator B | Adjudicated |
|---|---|---|---|
| low_visible_concern | — | — | — |
| inspection_required | — | — | — |
| do_not_drive | — | — | — |
| raw agreement | — | | |
| Cohen's κ (3-class) | — | | |
| κ (do_not_drive vs rest) | — | | |
| mean seconds/image | — | — | |
| items with `resolution_ok = false` | — | — | |
| items needing more views | — | — | |

### Hypotheses (to be tested, not assumed)

- **H1** κ for the 3-class label will be moderate (0.4–0.6) on first pass, and will improve
  after the first rubric revision — driven by the low/inspection boundary, not by
  do-not-drive.
- **H2** ≥ 30% of items will be forced to `inspection_required` by the coverage rule.
- **H3** ≥ 15% of images carrying a damage class label will show no damage in the given view
  at full resolution.

If H1 fails badly (κ < 0.4 after one revision), the correct response is to narrow the task
(for example: binary "visible hazard present / not" plus a mandatory coverage check) and say
so in the thesis as a methodological finding.

---

## 5. Scale-up gate

Do not start large-scale labeling until all of the following hold:

- [ ] κ ≥ 0.6 on the pilot after adjudication, or a documented rubric revision that achieves it
- [ ] every category has at least 3 examples that both annotators agreed on
- [ ] the coverage rule's effect on the label distribution is known and acceptable
- [ ] time per image measured, and `N × time` fits the remaining schedule
- [ ] a second hazard-bearing source (VehiDE and/or CarDD `tire_flat`) is confirmed, otherwise
      the "do not drive" class is not learnable
