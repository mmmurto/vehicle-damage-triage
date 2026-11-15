# Dataset Sourcing Plan — how to reach 5,000–10,000 mixed damage images

Answer to "find datasets for 5k–10k images, mixed (usable and unusable cars)". Verified on
2026-11-15. Counts marked **verified** were read from the publisher's own metadata or file
listing; **reported** means the publisher states it but I could not yet enumerate the files
(Roboflow is behind a bot check without an account).

---

## 1. What "mixed" has to mean for this project

The corpus must contain three kinds of visible evidence, not three kinds of damage *names*:

| Evidence class | Needed because | Where it comes from |
|---|---|---|
| Undamaged / cosmetically damaged | the "low visible concern" class needs a real denominator, and a model trained only on crashes collapses everything to "damaged" | DrBimmer `*_Normal` (1,100 images), Roboflow sets that include `car`/undamaged images, TartesiaDS (24 undamaged images) |
| Moderate damage with intact safety-critical parts | the "inspection required" class — the hard, ambiguous middle | CarDD, VehiDE, Roboflow 14/23-class sets |
| Severe / hazmat / structural damage | the "do not drive" class — currently the thinnest and most important | VehiDE severe instances, Roboflow 18-class set (`flat-tire`, `detachment`, `car-part-crack`), CSP650 `03-severe`, plus the auction damage taxonomy in §5 |

Key point: **no free source labels "undriveable."** Severity labels (`severe`) and auction
damage classes (`rollover`, `water/flood`, `burn`, `undercarriage`) are the closest proxies,
and they are *visible-condition* labels, not driveability verdicts. That is why the thesis
evaluates expert visual triage. Do not let a source's `severe` class be renamed "do not
drive" anywhere in the code or the report.

---

## 2. Acquisition queue, ranked

### Tier A — free and obtainable now (no application)

| # | Source | URL | Count | Labels | Licence / access | Unique value |
|---|---|---|---|---|---|---|
| A1 | **VehiDE** | kaggle.com/datasets/hendrichscullen/vehide-dataset-automatic-vehicle-damage-detection | **13,945 verified** (paper: 8 categories, >32,000 instances) | instance seg. + detection + classification | Kaggle account + terms; listing says Apache 2.0 (`verify` against the article) | the volume backbone; insurance photography, real damage severity range |
| A2 | **Zenodo Minor Dent Detection** | doi.org/10.5281/zenodo.16934368 | **2,241 verified** (1,568 / 449 / 224) | YOLOv8 boxes, single class (minor dent) | **CC BY 4.0**, direct download | clean "low concern" end of the spectrum; useful hard negatives |
| A3 | **DrBimmer comprehensive-car-damage** | huggingface.co/datasets/DrBimmer/comprehensive-car-damage | **2,300 verified** (in hand) | 6 image-level classes | MIT tag (provenance caveat) | undamaged/damaged split; already used for the pilot |
| A4 | TartesiaDS | github.com/tartesia/TartesiaDS → Google form | **108 verified** | boxes: scratch / deformation / other, + 24 undamaged | free for academic research on request | tiny, but an insurer-sourced set; good for a sanity test, not for volume |

**Tier A total: 18,594 images.**

### Tier B — free but requires an account or a signed form

| # | Source | URL | Count | Labels | Access action | Unique value |
|---|---|---|---|---|---|---|
| B1 | **CarDD** | cardd-ustc.github.io | **4,000 verified** (>9,000 instances) | COCO boxes + instance masks, 6 classes incl. `tire_flat`, `glass_shatter` | **download the licence form, sign, email the authors**, then get the link | best annotation quality; the only free source with a proper `tire_flat` class and masks |
| B2 | Roboflow **Curacel AI car-damage-detection-5ioys** | universe.roboflow.com/curacel-ai/car-damage-detection-5ioys | **6.8k reported**, model metadata says 16,326 images for v1 | 23 classes: per-part dent/scratch, windscreen, headlight, pillar-dent, paint-chip | Roboflow account → download in YOLO/COCO | part-level granularity; the largest single free label set |
| B3 | Roboflow **Automobile Damage Detection** | universe.roboflow.com/automobile-damage-detection/automobile-damage-detection | **7k reported** (v3: 6,957) | 14 part-level dent + windscreen + lamp classes | Roboflow account | overlapping but different part taxonomy; use for cross-checks |
| B4 | Roboflow **Car Damaged Severity Detection** | universe.roboflow.com/car-damaged-detection-e66m0/car-damaged-severity-detection | **3.1k reported** | 18 classes incl. `flat-tire`, `detachment`, `car-part-crack` | Roboflow account | **the most useful set for the "do not drive" evidence**: detachment + flat tyre + cracks |
| B5 | Roboflow **CSP650 Car Damage Severity Assessment** | universe.roboflow.com/csp650-5tzt9/car-damage-severity-assessment | **1,692 reported** (v6) | 3 classes: `01-minor`, `02-moderate`, `03-severe` | Roboflow account | the only clean 3-level severity label set; maps naturally onto triage |
| B6 | Roboflow **DentDetection** | universe.roboflow.com/dentdetection-ouw7c/car-damage-8qbpa | **431 verified** | 9 classes incl. `Flat Tire`, `Minor/Major Scratch` | Roboflow account | minor-vs-major wording check |

**Tier B total: ~19,000 reported images**, but assume heavy overlap with A1 and B1 (see §3).

### Tier C — record the decision to *not* use, with the reason

| Source | Claim | Why not |
|---|---|---|
| Kled `useKled/vehicle-damage` (HF) | 5,000+ consented photo sets, whole vehicle → panel → close-up, with questionnaire, from SEA | **commercial training licence, gated, priced**; a free "sample set" exists on request. Worth one email, not a dependency |
| VinAssessment | 536M+ auction damage images, VIN-linked, with the auction house's primary/secondary damage class | commercial vendor; the closest thing to outcome-linked data that exists, and exactly what a follow-up PhD would license |
| Copart / IAAI listing photo scraping | the auction's own damage class | **terms of use prohibit scraping**; do not do this, in any form, even "just for the test set" |
| Kaggle "Car Damage Severity Dataset" (prajwalbhamere) | 1,631 images, minor/moderate/severe | self-described scraping, no licence stated → provenance chain broken. Use CSP650 (B5) instead |
| AutoDamageIQ (HF) | 12,094 images | derivative of CarDD + VehiDE + GPT-4o pseudo-labels; double counting, licence chain broken |
| SYNDCAR (Mendeley) | 245 images | synthetic/rendered — keep out of test sets per the brief |
| Naiscorp, ikuldeep1 | 44,794 / 8,079 rows | mislabelled or undefined; unusable (see main inventory) |

---

## 3. The overlap problem (this is what decides whether you really have 10,000)

Roboflow's B2–B4 and the HF `DrBimmer/car-parts-and-damage-dataset` are **re-uploads of the
same underlying "car damage" image pool** that circulates with 14/18/23-class label sets. The
same photograph can appear with a `dent` box in one version and a `front-bumper-dent` box in
another. Consequences:

1. Never add counts across B2, B3, B4 and call it 17k. Deduplicate first (perceptual hash +
   embedding distance), then count.
2. Never place two versions of the same pool in train and test. Split by **duplicate cluster**,
   not by file.
3. Expected unique yield:

| Stage | Images (estimate, to be measured) |
|---|---|
| Tier A raw | 18,594 |
| Tier B raw (reported) | ~19,000 |
| after exact + near-duplicate removal | **12,000–16,000** |
| after unusable/blurred/unlabelled removal | **9,000–13,000** |
| final labelled triage subset (2 annotators, ~60 images/hour) | **2,000–3,000** for the primary experiment; the rest used for pretraining/representation learning |

So the answer to "5,000 or 10,000?" is: **10,000 images is reachable, 3,000 unique vehicles is
not** — vehicle identity does not exist in any free source, so the honest reporting unit is
images plus inferred duplicate clusters. State this early in the thesis; it is a limitation of
the field, not of your work.

---

## 4. Exact steps, in the order I recommend doing them

### Step 1 — accounts (today, ~20 minutes, you do this)
- Kaggle account → *Settings → API → Create New Token* → saves `kaggle.json`.
  Put it at `C:\Users\mmirz\.kaggle\kaggle.json` and tell me when it is there.
- Roboflow account (free) → *Settings → Roboflow API* → copy the private key.
  Then tell me; I will store it in `.env` (already git-ignored) and never commit it.
- Send the CarDD licence form (link on `cardd-ustc.github.io`); it may need a supervisor
  signature. This is the one step that can take days, so start it first.

### Step 2 — download Tier A (I can do this as soon as Kaggle auth exists)
```bash
# VehiDE (13,945 images, ~2 GB)
kaggle datasets download -d hendrichscullen/vehide-dataset-automatic-vehicle-damage-detection -p data/raw/vehide --unzip

# Zenodo minor dent (2,241 images, CC BY 4.0)
# take the download URL from the DOI landing page, then:
curl -L -o data/raw/minor_dent.zip "<zenodo-file-url>"

# DrBimmer (2,300 images, ~670 MB)
huggingface-cli download DrBimmer/comprehensive-car-damage --repo-type dataset --local-dir data/raw/drbimmer
```

### Step 3 — download Tier B once accounts exist
```bash
pip install roboflow
# Curacel AI (23 classes)
python -c "from roboflow import Roboflow; rf=Roboflow(api_key=__import__('os').environ['ROBOFLOW_API_KEY']); \
rf.workspace('curacel-ai').project('car-damage-detection-5ioys').version(1).download('yolov8', location='data/raw/roboflow_curacel')"
# Car Damaged Severity Detection (18 classes, flat-tire + detachment)
# CSP650 severity (3 classes)
# Automobile Damage Detection (14 classes)
```
(Each project has several versions; the version number decides the count. I will pin one
version per project and record it, so the thesis can cite an exact snapshot.)

### Step 4 — audit before anything else (this is experiment E0)
- enumerate files, hash, count, per-class distribution;
- perceptual-hash near-duplicate clustering, then cross-source overlap matrix
  (how many DrBimmer images reappear in Roboflow, etc.);
- resolution and blur statistics;
- **hazard coverage count**: how many images actually show a tyre, wheel, fluid, or glass
  finding — if this is under ~200, the "do not drive" class cannot be trained and the thesis
  must switch to the binary hazard + coverage formulation. Measure this before writing code.

---

## 5. The label taxonomy worth stealing (for the rubric, not the images)

Salvage-auction listing data (the Kaggle Copart/IAAI metadata sets; vendor: VinAssessment)
records a *primary damage* field normalised to roughly 30 values, e.g.: front end, rear end,
side, roof/top, undercarriage, rollover, water/flood, burn, mechanical, hail, vandalism,
all over, minor dent/scratches, frame damage, suspension, electrical, transmission.

This is useful in three ways even though the images are not obtainable:
1. It is evidence that **"damage class" and "can it be driven" are different fields** even in
   industry data — the auction records damage class *and* title status *and* condition grade.
   Cite this when arguing why damage-type datasets cannot answer the driveability question.
2. It gives a defensible list of **hazard-relevant categories** to check coverage against:
   rollover, water/flood, burn, undercarriage, suspension/wheel, frame — the ones that map to
   "do not drive" or "inspection required".
3. It is the concrete target of future work ("a study with auction/insurance records").

Caveat to write down: auction damage classes are entered by the auction house, for pricing,
not for safety, and are not verified by inspection of roadworthiness.

---

## 6. What I need from you to continue

| Item | Why | Blocking? |
|---|---|---|
| Kaggle API token in `C:\Users\mmirz\.kaggle\kaggle.json` | download VehiDE (13,945 images) | **yes**, for volume |
| Roboflow API key | download the 4 Roboflow sets | yes, for hazard coverage |
| CarDD form sent (needs supervisor signature) | 4,000 best-annotated images | no, but start now |
| Answer: page limit (40 or 70) and citation style | freezes the outline | no |
| Do you have a GPU / Colab only? | decides baseline size | no, until training |

Meanwhile I can proceed without any of these: build the dedup + audit pipeline against
DrBimmer (2,300 images, already in hand), so that when the big downloads land we run E0
immediately instead of writing code.
