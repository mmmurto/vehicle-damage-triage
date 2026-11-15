# Dataset Inventory

Verification date: 2026-11-15. Method: metadata and file listings queried directly from the
Hugging Face API (`huggingface.co/api/datasets/...`), the HF datasets-server (`size`,
`statistics`, `rows`), publisher pages, and a visual check of a 36-image contact sheet.

Legend for **Role**: `PRIMARY` = candidate training/evaluation source · `SECONDARY` = extra
volume or specific evidence · `PRETRAIN` = representation learning only, no damage labels ·
`REJECT` = unusable as published · `DERIVED` = re-upload / remix of other sources.

---

## 1. Verified entries

### 1.1 `DrBimmer/comprehensive-car-damage` — the dataset you found

| Field | Verified value |
|---|---|
| URL | https://huggingface.co/datasets/DrBimmer/comprehensive-car-damage |
| Revision checked | `355b0990ec008e15963055e6bb448045a65040a3`, last modified 2025-03-27 |
| **Image count** | **2,300** (not ~2,500). 2,300 rows in the only split, 2,300 image files in the repo |
| Splits | one: `train` only (no official val/test) |
| Label type | 6 mutually exclusive **image-level classes**: `F_Breakage` (500), `F_Crushed` (400), `F_Normal` (500), `R_Breakage` (296+4 png), `R_Crushed` (300), `R_Normal` (300) |
| Annotations | none beyond the class label — **no boxes, no masks, no per-instance severity, no vehicle ID** |
| Resolution | image width 300–2,242 px, median 800, mean 919; most files 800×600 |
| Format | `imagefolder` (jpg/png), 2 columns |
| Licence (declared) | `mit` |
| Access | open, no gating, no auth |
| Formatting caveat | filename prefixes disagree with content: `F_*` images sometimes show rear or side views; the split between "Crushed" and "Breakage" is not defined anywhere |
| Provenance signal | contact-sheet inspection shows used-car/dealer listing photography with **number plates masked by dealer overlays** (e.g. "Encarr"), i.e. scraped marketplace images |

**Why the MIT tag is not sufficient.** The uploader can license the *packaging* of a
collection but cannot grant rights over photographs they did not take and over third-party
plate masks. For a dissertation this matters for (a) redistribution of the images in an
appendix or repository, (b) any claim that the data may be used commercially. Treat the
dataset as *usable for academic analysis with attribution*, *not* as MIT-clean for
redistribution. Record this as a documented limitation.

**Fitness for this project:** can support "is visible damage present, and roughly where"
(image-level). Cannot support "do not drive" as a class, because:
- 0 of 36 sampled images showed tyre, wheel, suspension, fluid-leak or underbody evidence;
- no per-evidence annotations to learn hazard cues from;
- 800×600 compression is marginal for thin cracks, seepage or tread detail;
- no vehicle grouping, so images of the same car may straddle splits;
- label noise is visible at thumbnail scale (see `pilot/04_pilot_report.md`).

**Verdict: SECONDARY** — bootstrap and pilot only. Fine for building the pipeline today;
not the source of a 10,000-image claim.

### 1.2 CarDD — Car Damage Detection dataset (USTC, IEEE TITS 2023)

| Field | Verified value |
|---|---|
| URL | https://cardd-ustc.github.io/ · paper doi 10.1109/TITS.2023.3258480 |
| **Image count** | **4,000** high-resolution images, **>9,000 annotated instances** |
| Label type | 6 categories — dent, scratch, crack, glass shatter, flat tyre, broken lamp; COCO detection **and** instance segmentation; also usable as classification |
| Licence / access | **requires a signed licence form** sent to the authors to obtain the download link; academic, non-commercial terms in the form |
| Verdict | **PRIMARY** (pending: form approval). This is the strongest public source because of instance-level boxes and the `flat tyre` and `glass shatter` classes. |

Note: third-party Hugging Face mirrors exist (e.g. `sashankrudra/CarDD`, 2,817 rows, and
`DrBimmer/car-parts-and-damage-dataset`, MIT-tagged, 0 rows readable). Using a mirror
sidesteps the licence form and breaks the licence chain. **Do not do that**; request the
official release and cite it.

### 1.3 VehiDE — Vehicle Damage Detection dataset

| Field | Verified value |
|---|---|
| Kaggle URL | https://www.kaggle.com/datasets/hendrichscullen/vehide-dataset-automatic-vehicle-damage-detection |
| Paper | *Powering AI-driven car damage identification based on VehiDE dataset*, J. Information and Telecommunication, 2024, doi 10.1080/24751839.2024.2367387 |
| **Image count** | **13,945** high-resolution images, **>32,000 instances**, **8 damage categories** |
| Label type | instance segmentation + detection + classification (paper states all three supported) |
| Licence (declared on Kaggle) | **Apache 2.0** (uploader-set; the paper is open access). Verify against the article before relying on it |
| Image source | insurance/assessment photography — **images come from claims, but labels are damage instances, not claim outcomes** |
| Verdict | **PRIMARY**. Largest verified source; alone it exceeds the 10,000 target. Also the most likely to contain genuine tyre/wheel/structural damage. |
| **Audited 2026-11-15** | 13,945 images and 13,945 annotation entries confirmed; 36,081 polygon regions; **7** classes in the release (paper claims 8); **100% of images contain damage — no undamaged vehicles**; median image width 1,632 px; **shipped train/val split leaks ~80% at minute-level session grouping**. Full details: `docs/07_vehide_audit.md`. |

### 1.4 AutoDamageIQ (`tugberkkalay/autodamageiq-vehicle-damage-dataset`)

| Field | Verified value |
|---|---|
| URL | https://huggingface.co/datasets/tugberkkalay/autodamageiq-vehicle-damage-dataset |
| **Image count** | repo contains **12,094** images (10,000 `images/train` + 2,094 `images/val`); the dataset card claims 13,089 train images, which **does not match the repository** — trust neither number without a local recount |
| Labels | YOLO boxes, 6 classes; card states ~42,419 boxes: scratch 23,967 (56.5%), dent 11,204 (26.4%), crack 3,427 (8.1%), glass_shatter 2,696 (6.4%), lamp_broken 776 (1.8%), **tire_flat 349 (0.8%)** |
| Licence (declared) | CC BY 4.0 |
| Provenance | card states it is a merge of **CarDD + VehiDE + GPT-4o ("human-in-the-loop") pseudo-labels** |
| Verdict | **DERIVED — do not use as an independent test source, and do not count it as new volume.** It re-packages CarDD and VehiDE (both obtainable directly), and part of its annotation is machine-generated, so its licence claim cannot cover the merged content. Useful only as a cross-check of annotation formats. |

### 1.5 Roboflow Universe — `DentDetection/car-damage`

| Field | Verified value |
|---|---|
| URL | https://universe.roboflow.com/dentdetection-ouw7c/car-damage-8qbpa |
| **Image count** | **431** images, 6 dataset versions |
| Classes | 9: car, Body Damage, **Flat Tire**, Flat Tyre, Major Dent, Major Scratch, Minor Dent, Minor Scratch, Paint Peel Off |
| Licence / access | Roboflow Universe default CC BY 4.0 (confirm per version); download requires a Roboflow account/API key |
| Verdict | **SECONDARY**. Small but the only verified source with an explicit flat-tyre class and a minor/major distinction — useful for class-definition sanity checks, not for volume. |

### 1.6 Kaggle — Car Damage Severity (`prajwalbhamere`)

| Field | Verified value |
|---|---|
| URL | https://www.kaggle.com/datasets/prajwalbhamere/car-damage-severity-dataset |
| **Image count** | **1,631 files** |
| Labels | 3 severity classes: minor / moderate / severe, arranged as train/val folders |
| Provenance | "scraped by me from multiple sources" — no licence statement on the card, no per-image source |
| Verdict | **REJECT for the main pipeline** (unknown provenance, no licence), acceptable only as an informal eyeball check of severity wording. Similar-looking Kaggle copies of CarDD exist (`nasimetemadi/car-damage-detection`) and are redundant with 1.2. |

### 1.7 `Naiscorp/car-damage-dataset`

44,794 rows, but the parquet payload is ~5.6 MB and the label vocabulary is a long list of
numeric IDs (`001`, `002`, …). This is a car-*model* catalogue, not a damage taxonomy, and
the image payload is not stored. **REJECT.**

### 1.8 `ikuldeep1/vehicle-damage-fraud-image`

8,079 rows, ~1.06 GB, binary label `0/1` labelled only "fraud"/not. No dataset card, no
licence, no provenance, no definition of fraud. **REJECT.**

### 1.9 Stanford Cars / CompCars — pretraining only

Stanford Cars: 16,185 images, 196 classes (Krause et al., 2013). CompCars: make/model
classification at larger scale. Neither contains damage. Role: **PRETRAIN** for
make/model/part localisation, or as a *negative* (undamaged) pool if you need clean
"normal" images — but class-conditional vehicle appearance then confounds damage detection,
so use with care.

---

## 2. Candidates marked PENDING (not yet verified)

| Candidate | Why it matters | What to check |
|---|---|---|
| `kadireks/cardamagepanel-originals` (HF, 1K–10K, licence `other`) | "panel" damage could add part-level structure | licence text, label schema, overlap with CarDD |
| `DigitalShowroomexperts/car-damage-dataset` (HF, gated, 10K–100K) | volume | request access; check whether labels are damage or car model |
| `useKled/vehicle-damage` (HF, licence `other`) | unknown | card, count |
| Copart / IAAI salvage-auction photography | would add genuinely undriveable vehicles (salvage, rollover, airbag deployment) | **licensing and terms of use almost certainly prohibit scraping — assume not permitted** |
| Insurer/leasing appraisal archives (e.g. the 40,000-report, 342,029-photo leasing dataset described by Jameel et al., ECML 2020) | the only known data with **appraiser-verified damage + repair cost per photo** | not public; a data-access request is a legitimate future-work action, not a bachelor-thesis dependency |
| Police crash databases with images (e.g. crash-injury databases with vehicle images) | would provide true outcome labels ("towed/undriveable") | image availability, ethics, licensing |

---

## 3. Inspection-backed labels: the decisive question

**Result of the search: none found.** No public dataset verified here pairs photographs with
a professional inspection outcome, a repair/condemnation decision, or a "driven afterwards"
record. What exists is:

| Label type | What it supports | What it cannot support |
|---|---|---|
| Damage category per image/instance (CarDD, VehiDE, DrBimmer) | "is visible damage present, where, what type" | whether the vehicle was safe to drive |
| Severity class (Kaggle severity sets, VehiDE severity) | coarse ordering of visual damage | any functional claim |
| Repair cost estimate (proprietary leasing data) | economic severity | driveability |
| Appraiser narrative (not public) | would support triage if released | — |

Therefore the reference standard for this dissertation is **expert-reviewed visual triage
labels**, produced under the rubric in `docs/03_labeling_guide.md`, and the thesis must say
so in RQ1 and in the conclusion. The primary error metric is named accordingly: the
*visual-triage hazard-miss rate*, not "unsafe vehicles assigned low concern" in the
inspection sense.

Two consequences worth writing into the methodology:
1. The study measures **agreement with expert visual judgement**, so it inherits the
   annotators' uncertainty. Inter-annotator agreement is therefore a first-class result, not
   an appendix detail.
2. A negative result ("photographs are insufficient to separate these categories reliably")
   is a scientifically useful outcome for a triage system. Plan the framing so that this is
   a finding, not a failure.

---

## 4. Volume accounting (what 10,000 means here)

Full ranking, access steps and overlap analysis: **`docs/06_dataset_sourcing_plan.md`**.

| Tier | Sources | Raw images | Status |
|---|---|---|---|
| A — free, no application | VehiDE 13,945 · Zenodo minor dent 2,241 · DrBimmer 2,300 · TartesiaDS 108 | **18,594** | counts verified; needs Kaggle account for VehiDE |
| B — free, account or signed form | CarDD 4,000 · Roboflow 4 sets (~19,000 reported) | **~23,000 reported** | CarDD form + Roboflow account |
| **Union before dedup** | | **~41,000** | |
| **Estimate after dedup + unusable removal** | | **9,000–13,000** | to be measured in E0 |

So the 10,000 target is reachable without paying for data; the binding constraint is
**duplicate overlap** between the Roboflow re-uploads and **hazard coverage** (how many images
actually show a tyre, wheel, fluid or glass finding), not raw volume. Both are measured in E0
before any model is trained.

If access fails entirely, the honest ceiling is 2,300 images plus small secondaries, and the
plan switches to **Plan B**: label the full 2,300 with expert triage at roughly 8 s/image
(≈5 h per annotator pass) and spend the saved effort on multi-view grouping and error
analysis rather than on volume.

### Session-2 additions to this inventory

Added after a second search pass (see `docs/06_dataset_sourcing_plan.md` for the ranked queue):
Zenodo Minor Dent Detection (2,241, CC BY 4.0), Roboflow Curacel AI (6.8k, 23 classes),
Roboflow Automobile Damage Detection (6,957, 14 classes), Roboflow Car Damaged Severity
Detection (3.1k, incl. `flat-tire` and `detachment`), Roboflow CSP650 severity (1,692,
minor/moderate/severe), TartesiaDS (108, insurer use case, free for academic research),
Kled (5,000 consented photo sets, commercial licence), VinAssessment (536M auction images,
commercial), Copart/IAAI metadata (taxonomy only), SYNDCAR (245, synthetic).

**Unique vehicles vs unique images.** Vehicle identity is available in *none* of the public
sources (no VIN, no registration, no incident ID). It must be *inferred*: perceptual hash +
embedding clustering to remove duplicates, and (where EXIF or filenames suggest a sequence)
same-scene grouping. Report both counts: images and inferred vehicle clusters, and state the
inference method and its error rate. Where grouping cannot be established, evaluate at image
level and say so.
