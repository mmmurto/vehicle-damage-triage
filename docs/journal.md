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
