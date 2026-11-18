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

---

## 2026-11-15 — Session 3: Kaggle access, VehiDE downloaded, audit (E0 part 1)

**Goal:** get the credential working and pull the volume backbone, then measure what it
actually contains before writing any model code.

**Done**
- Kaggle token (new inline format) tested: username `mmurto`, both basic-auth and bearer
  work (HTTP 200). The Kaggle CLI is unusable on this machine (the `python` on PATH is the
  Microsoft Store stub), so downloads go through the REST API with curl. Credentials live in
  `C:\Users\mmirz\.kaggle\kaggle.json`, outside the repo, never committed.
- Downloaded VehiDE: 2.25 GB, zip integrity verified, 24 s to extract, 13,947 files.
- Wrote `scripts/audit_vehide.mjs` (VIA-format audit: counts, class distribution, missing
  files, resolution sample) and `scripts/vehide_group_analysis.mjs` (session-group derivation
  from filenames + split-leakage measurement).
- Wrote `docs/07_vehide_audit.md`.

**Verified facts about VehiDE**
- 11,621 train + 2,324 val = **13,945 images**, matching the paper. 0 missing, 0 orphan
  annotations, **100% of images carry at least one damage region**.
- **36,081 polygon regions across 7 classes** (paper says 8 — discrepancy logged):
  `tray_son` scratch 14,647 · `mop_lom` dent 5,681 · `rach` tear 5,509 ·
  `mat_bo_phan` missing part 2,818 · `be_den` broken lamp 2,782 · `thung` puncture 2,423 ·
  `vo_kinh` broken glass 2,221. Class names are Vietnamese and unaccented; translation is a
  working interpretation pending confirmation.
- Median image width 1,632 px (vs 800 for DrBimmer) — good enough for panel and glass detail.
- **No tyre, wheel, suspension or fluid class.** The hazard evidence the "do not drive"
  category depends on is absent.

**The headline result**
Filenames encode capture timestamps, so grouping by timestamp approximates same-vehicle
sessions. Against the shipped train/val split: **79.8% of validation images share a session
group with training images at minute granularity, 97.7% at hour granularity.** The published
split is effectively random at image level, so published VehiDE metrics are optimistic.
Decision: build our own grouped split and report the shipped-split number only as a
leakage-effect comparison.

**Consequences**
- Volume target met from one source; remaining datasets now serve diversity, undamaged
  negatives (VehiDE has none) and hazard coverage, not image count.
- Triage labels cannot be mapped from VehiDE's 7 classes; they need expert labeling plus
  rule-based evidence flags.
- "Do not drive" still depends on Roboflow's `flat-tire`/`detachment` set and CarDD
  `tire_flat`. If hazard coverage stays near zero, the thesis falls back to the binary
  hazard + coverage formulation and says so in chapter 8.

**Next**
- Perceptual-hash dedup within VehiDE and across DrBimmer (E0 part 2).
- Tyre/wheel visibility census on 500 sampled images (decides whether the rubric's coverage
  rule is realistic).
- Grouped split builder with the vehicle-session key.

---

## 2026-11-16 — Session 4: five-minute proposal defence and continuation review

**Priority requested:** prepare the first proposal defence before expanding implementation. Current targets: a 70-page dissertation; >20,000 usable real unique images, 50,000+ as a conditional stretch goal.

**Done**
- Read both supplied images and both example Word documents. The Word documents are another student's GNN examples, not the approved vehicle-damage title. Teacher screenshot requests a five-minute proposal defence.
- After the user enabled public repository access, cloned and reviewed base `3482f30`, including the previous VehiDE audit, pilot, guide, inventory and scripts. Preserved earlier work.
- Prepared `presentations/proposal-defence/`: eight timed English proposal slides (300 seconds allocated, embedded notes), three backup source appendices, speech/Q&A, compact editable proposal, 70/40-page budgets, supplemental dataset inventory, source ledger, pilot extension and evaluation protocol.
- Reopened generated PPTX/DOCX to check structure; all slide shape bounds checked programmatically. No PowerPoint visual rendering or Word pagination check was available; rehearse and inspect before presenting.
- Additional leads include a 19,100-image Roboflow version (rights/provenance pending) and AI-Hub's reported 632,694-image accident collection (Korean-national application restriction; estimate records are not roadworthiness labels). No source counts were added into a fictitious unique total.
- Added `docs/08_continuation_review.md`: qualifies the previous timestamp-group overlap interpretation and identifies unresolved fluid/glass, annotation validity and upstream rights issues.
- Added the generation script for reproducibility. No raw photos or credentials are included in this session's new files.

**Not done / limitations**
- Prior archive counts were reviewed, not re-run. No new vehicle-photo archives downloaded; no completed expert pilot labels or agreement, no trained model, no model performance experiments.
- Existing 36-image sample remains the starting point; 60 cases is a proposed extension.
- Official title, presenter details, presentation language/date, handbook and live-demo expectation remain pending.

**Publication**
- Prepared on branch `docs/proposal-defence-2026-11-16`; remote push success must be checked against the command result and remote commit ID, not assumed from this log.

**Next**
Confirm presentation details, inspect/rehearse slides, reproduce the archive audit when the existing raw-data location is supplied, validate cross-source dedup and incident grouping, secure rights and recruit qualified review before scaling labels.

### Session 4 follow-up — visual redesign and Word rehearsal script

User requested a less basic PPTX, the speaking script in Word, and clarification on what the Chinese examples require. Added `Vehicle_Damage_Proposal_Designed_v2.pptx` (8 core slides + 2 source backups) and `Five_Minute_Defence_Script_v2.docx`. Slides now use original editable vector illustration, category cards, numerical data dashboard, pipeline diagram and evidence/inspection trade-off illustration (not invented experimental curves). Word contains slide-by-slide speech, timing, stage cues and examiner answers. Reopened Office files and checked slide shape bounds; no PowerPoint visual rendering or exact Word pagination check was performed. Original drafts retained.

Clarification: presentation explicitly required; Chinese task sheet and proposal report described as examples of files to prepare, so written submissions may also be expected. Exact first-session requirements must be confirmed; research inventories were requested in the broader project brief, not mandated by the examples. No training/data-collection action undertaken in this follow-up. Two final user-facing deliverables only.

### Follow-up — simpler English (v3)

The user found the slide and script language too difficult. Replaced academic wording with short, everyday explanations in both the slide text and full speaking script. Kept the designed slide layout and the three category names, with simple definitions. The new Word script has slide-by-slide speech, timing, reminders and simple question answers. Eight main slides, two backup source slides, 300-second target and approximately 690 spoken words; real timing requires rehearsal. Kept safety limits, prior-count attribution and unfinished-work statements. No data/model results changed. Reopened both Office files and checked slide bounds; visual rendering and exact Word pagination remain unchecked. Recommended files are `Car_Damage_Presentation_Simple_English_v3.pptx` and `Five_Minute_Script_Simple_English_v3.docx`. Older versions retained.

### Urgent follow-up — proposal-first defence pack (v4)

The user reported a friend's proposal defence experience: talks stopped at five minutes, panel emphasis on the printed proposal, and recommendation to print the proposal. Two new attachments were inspected: they are example workflow designs, not official proposal forms. Their clinical-trial content was not copied. The user requested a detailed workflow, completed proposal and help understanding likely questions. The response uses honest, explainable detail, not deliberate complexity to obstruct examination.

Prepared `presentations/tomorrow-defence/`:
- Eight-page proposal PDF and editable Word version with the sample Chinese opening-report section sequence. Identity and official title remain unverified; clear blanks are left for completion before printing. English language and unofficial form status are explicit.
- Two original workflows: research/data-to-final-test process, and one-car photo-to-action decision process. High-resolution PNG, editable SVG, full-page vector PDF and embedded proposal figures. Clear visible hazards precede incomplete-view routing; unusable input means inspection/retake, never low concern.
- Seven-slide main talk with two question-only detailed-diagram backups. Matching script: 519 words, 255 seconds allocated (4:15) with a 45-second buffer. Actual timing requires rehearsal.
- Plain-English guide explaining completed vs planned work, dataset numbers, workflow stages, 30 likely examiner questions and a pre-defence checklist.

Rechecked primary references. Completed VehiDE authors and final issue details in `docs/references.bib`: 2025, volume 9(1), pp. 24–43; first online publication June 2024. Preserved the old citation key. Added no invented performance results, unique-car counts, official identity or deadline. Prior VehiDE archive numbers were reviewed, not reproduced. Expert pilot action labels and model training/testing remain unfinished.

Verification: reopened Office outputs; checked PowerPoint bounds, main/backup slide counts and speech allocation; generated the print PDF from shared content and verified eight pages; rendered all PDF pages and inspected proposal layouts and workflow artwork. Actual Office rendering and exact Word pagination remain unchecked. Source script and provenance/read-me are included for reproduction. No restricted car photos or credentials were added. All new outputs are documented on the existing defence branch; push success is checked separately against the remote commit.

### Real-photo presentation update (v5)

User requested real car images, a roof-down convertible versus severely roof-damaged SUV, and quick photo-led examples. Searched public sources, checked source-file license templates/photographers and visually inspected downloaded images. Selected a roof-down 2022 BMW M4 Competition (Calreyn88, CC BY-SA 4.0), Honda CR-V rollover with visible roof deformation/windshield damage (Ryanandlenny, CC BY 3.0), visibly flat tire (Tiia Monto, CC BY-SA 4.0), and front-area scrapes/damage (Uiliam Nörnberg, Pexels License). The bumper-detail crop and full front photo share one source; this is explicitly disclosed. No whole-car low-concern or confirmed driveability label is assigned from a cosmetic-looking crop. Source pages, authors, licenses, resizing/cropping and image hashes recorded in the v5 folder. Photos are presentation illustrations, NOT acquired VehiDE/DrBimmer records or additions to training/test totals. No generated or fabricated accident photographs were used.

Added two quick main photo slides to the v4 deck, a question-only design-aware challenge slide and two photo-credit backups. Nine main slides, five backups. Rewrote matching simple-English speech to target 250 seconds (4:10), 428 spoken words; actual timing still requires rehearsal. Original Word/PDF proposal remains unchanged. Provided a new matching Word script and a reproducible slide-update script; older presentation preserved.

Special-case rationale is carefully bounded: teach/test factory convertible design separately from crash deformation. Include damaged convertibles and undamaged SUVs/fixed roofs, multiple models and settings, and disjoint car groups. Do not claim all convertibles are undamaged, an open roof proves roadworthiness, two curated images show model accuracy, or the idea establishes novel research without review. No model was trained or evaluated in this update.

Reopened PPTX/DOCX, verified slide counts, main speech budget, shape bounds, and inspected embedded source imagery. Actual PowerPoint visual rendering remains unchecked. Published on the existing defence branch; verify push against remote commit.
