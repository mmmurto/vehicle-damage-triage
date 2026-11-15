# Project Journal

One entry per working session. Newest at the bottom. Every entry is committed with the repo,
so the git history and this log agree. This is the audit trail the methodology chapter will
cite for "how the data was assembled".

---

## 2026-11-15 — Session 1: setup and dataset verification

**Goal:** establish the project skeleton, verify the one dataset the candidate had found,
and find out whether any public dataset contains inspection-backed driveability labels.

**Done**
- Read the candidate's dataset comparison screenshot (Chinese table listing CarDD, Roboflow
  car damage, Kaggle car damage sets, Stanford Cars/CompCars). Transcribed into the inventory
  as candidate leads.
- Verified `DrBimmer/comprehensive-car-damage` against the HF API: revision
  `355b0990`, 2,300 rows, 2,300 image files, one `train` split, 6 classes
  (500/400/500/300/300/300), no boxes, MIT tag, median width 800 px.
- Visual screening of a 36-image contact sheet (6 per class, systematic spread). Found
  dealer-listing photography with third-party plate masks, and no tyre/wheel/fluid/glass
  hazard evidence in the sample.
- Verified CarDD (4,000 images, licence form required) and VehiDE (13,945 images, Kaggle)
  from their official pages/papers. Rejected Naiscorp (car-model catalogue, no image payload),
  ikuldeep1 (undefined binary label, no card), Kaggle severity set (self-scraped, no licence).
  Flagged AutoDamageIQ as a derived CarDD+VehiDE+GPT-4o remix.
- **Key negative result:** no public dataset checked has inspection-backed driveability labels.
  Research question and metric plan adjusted to expert visual triage.
- Wrote: one-page proposal, 40- and 70-page outline with exact page sums, dataset inventory
  (MD + CSV), labeling guide v1.0 (observation / action / outcome records; glass, tyre, wheel,
  fluid rubrics; four-step decision rule), pilot report, open questions, references.bib.
- Built the pilot sample: 36 images, manifest CSV with empty label columns, contact sheet PNG.

**Decisions**
- Reference standard = expert visual triage labels (revisit if an outcome-linked source appears).
- Primary metric = visual-triage hazard-miss rate, reported with counts and CIs.
- Three classes with `inspection_required` as the abstain/default class.
- DrBimmer = secondary/bootstrap source, not the basis of the 10,000-image claim.

**Open / next**
- GitHub repo created (`mmmurto/vehicle-damage-triage`), first push.
- Second search pass for volume: Roboflow Universe (Curacel AI 6.8k, Automobile Damage
  Detection 7k, Car Damaged Severity Detection 3.1k, CSP650 severity 1.7k), Zenodo minor-dent
  (2,241), VehiDE (13,945), CarDD (4,000). Licence verification pending for each.
- Candidate still needs to confirm: page limit, citation style, title, ethics for annotators.

---

## 2026-11-15 — Session 2: GitHub repository, second dataset pass, 10k sourcing plan

**Goal:** as requested — get everything into the candidate's GitHub with every action pushed,
and widen the dataset search from 500–1,000 images to the 5,000–10,000 range with *mixed*
(usable and unusable) damage.

**Done**
- Created repository `mmmurto/vehicle-damage-triage` (private) and pushed session 1
  (`9331ff7`). Credential manager supplied the existing GitHub token; no secret was written
  to disk or to any file in the repo.
- Noted the SSH key on this machine is not registered with the GitHub account
  (`Permission denied (publickey)` on `git@ssh.github.com:443`); HTTPS push works, so HTTPS
  is the transport for now.
- Second search pass, new candidates found and ranked:
  - Zenodo Minor Dent Detection — 2,241 images, YOLOv8 boxes, **CC BY 4.0**, DOI 10.5281/zenodo.16934368.
  - Roboflow Curacel AI `car-damage-detection-5ioys` — 6.8k reported (v1 metadata: 16,326 images), 23 classes.
  - Roboflow Automobile Damage Detection — 6,957 images (v3), 14 part-level classes.
  - Roboflow Car Damaged Severity Detection — 3.1k reported, 18 classes incl. `flat-tire`, `detachment`, `car-part-crack`.
  - Roboflow CSP650 Car Damage Severity Assessment — 1,692 images, `01-minor/02-moderate/03-severe`.
  - TartesiaDS (insurer use case, Appl. Sci. 2024) — 108 images, free for academic research via Google form.
  - Kled `useKled/vehicle-damage` — 5,000+ consented photo sets, whole-vehicle→panel→close-up with questionnaire, but **commercial licence** (sample on request).
  - VinAssessment — 536M+ VIN-linked auction damage images, commercial; Copart/IAAI metadata sets usable only as a label taxonomy (scraping photos violates their terms).
  - SYNDCAR — 245 synthetic images, excluded from test use.
- Wrote `docs/06_dataset_sourcing_plan.md`: tiered acquisition queue, overlap warning
  (the 14/18/23-class Roboflow sets are re-uploads of one image pool — counts must never be
  summed), expected unique yield (9,000–13,000 after dedup), exact download commands, and the
  auction-primary-damage taxonomy to borrow for the rubric.
- Updated the inventory CSV to 24 rows with an explicit `count_status` column
  (verified / reported / unknown) and a `tier` column.

**Findings that change the plan**
- 10,000 images is reachable for free; the binding constraints are duplicate overlap and
  **hazard coverage**, not volume. Measure both in E0 before training.
- Vehicle identity does not exist in any free source → reporting unit is images plus inferred
  duplicate clusters, not unique vehicles. State this in chapter 3.
- The `do not drive` class still has the thinnest evidence. Roboflow's 18-class set
  (flat-tire, detachment) and CSP650 `03-severe` are the best free proxies; auction damage
  classes (rollover, water/flood, burn) are the categories to check coverage against.

**Blocked on the candidate**
- Kaggle API token (for VehiDE, 13,945 images), Roboflow API key (4 sets), CarDD licence form.
- Page limit / citation style / final title still unconfirmed.
