# Vehicle Damage Assessment from Images for Driveability Triage

Dissertation research workspace. Started 2026-11-15.

## What this is

A computer-vision system that reads photos of a damaged passenger car and outputs one of
three triage categories with the visible evidence and a recommended next step:

1. **Low visible concern** — minor cosmetic damage, coverage adequate; roadworthiness not verified.
2. **Do not drive** — visible hazard (shredded tyre, displaced wheel, etc.); professional assessment first.
3. **Inspection required** — photos incomplete/unclear, or a safety-critical issue is unresolved.

## Proposal defence — current continuation

### Latest presentation — real photos (v5)

Use **[Presentation_Real_Photos_v5.pptx](presentations/real-photo-v5/Presentation_Real_Photos_v5.pptx)** and the **[matched Word speech](presentations/real-photo-v5/Photo_Presentation_Script_v5.docx)**. Nine main slides (including two quick photo-led examples), five question/credit backups, 4:10 speech target. Real photos compare a roof-down BMW M4 with a roof-crushed Honda CR-V, plus surface scrapes, flat tire and incomplete front-impact evidence. [Photo sources, authors, licenses and changes](presentations/real-photo-v5/PHOTO_SOURCES.md) are documented. These are licensed presentation illustrations, NOT additions to the audited training collection or verified inspection labels.

Design-aware evaluation is a planned challenge: include intact and damaged convertibles as well as intact and damaged fixed-roof vehicles. Do not equate roof-down with damage, or convertible design with a safe car. No new trained-model result or proven novelty is claimed. The v4 printable proposal below remains the print document; v5 replaces only the presentation and matched speech.

### Latest printable proposal — proposal first (v4)

Following new peer feedback about the defence, the current recommended files are in **[presentations/tomorrow-defence/](presentations/tomorrow-defence/START_HERE.md)**:
- **[Print proposal PDF — 8 pages](presentations/tomorrow-defence/PRINT_Proposal.pdf)** and [editable Word proposal](presentations/tomorrow-defence/Proposal_Editable.docx).
- **[Presentation v4](presentations/tomorrow-defence/Presentation_Under_5_Minutes_v4.pptx)** — 7 main slides, 2 detailed-workflow backups; script targets 4:15 to leave a buffer.
- **[Simple defence guide and matched script](presentations/tomorrow-defence/READ_Defence_Guide_and_Script.docx)** — dataset facts, workflow explanation and 30 likely questions.
- **[Two detailed workflow diagrams](presentations/tomorrow-defence/Workflow_Diagrams.pdf)** — both also embedded in the proposal.

**Before printing:** fill identity fields and confirm the approved title. The PDF currently has clear blanks. The proposal follows the supplied sample's section order; it is not a verified official university form. Completed research preparation and planned model/expert-review work are clearly separated. Only the proposal is recommended for printing based on the friend's report; confirm the teacher's final instructions.

### Earlier version — simple English (v3)

Use these two files for rehearsal and presenting:
- [Simple-English PowerPoint v3](presentations/proposal-defence/Car_Damage_Presentation_Simple_English_v3.pptx)
- [Matching simple-English Word script v3](presentations/proposal-defence/Five_Minute_Script_Simple_English_v3.docx)

The visual layout is kept, but the slide text and spoken explanation use shorter sentences and everyday words. Eight main slides plus two backup source slides; five-minute target. Older versions below are retained for history, not the recommended speaking version.

The five-minute proposal pack is in [`presentations/proposal-defence/`](presentations/proposal-defence/):
- **[Redesigned PowerPoint v2: 8 timed slides + 2 source appendices](presentations/proposal-defence/Vehicle_Damage_Proposal_Designed_v2.pptx)** — current presentation; original vector artwork, decision cards, data dashboard and pipeline diagram.
- **[Word speaking script v2](presentations/proposal-defence/Five_Minute_Defence_Script_v2.docx)** — matching timing, stage directions and examiner questions.
- [Earlier plain PowerPoint draft](presentations/proposal-defence/vehicle_damage_proposal_defence.pptx) and [earlier Markdown script](presentations/proposal-defence/five_minute_script_and_questions.md) retained for history.

**Requirements clarification:** the teacher screenshot explicitly requests a five-minute presentation and calls the supplied Chinese task sheet (任务书) and opening report (开题报告) examples of files to prepare. Written documents may also be expected; exact first-session submission requirements and deadlines need teacher confirmation. Supporting inventories/protocols are research deliverables from the broader user request, not extra requirements proven by those examples.
- [One-page proposal](presentations/proposal-defence/docs/PROJECT_PROPOSAL.md)
- [70-page outline and 40-page fallback](presentations/proposal-defence/docs/DISSERTATION_OUTLINE.md)
- [Supplemental candidate inventory](presentations/proposal-defence/research/dataset_inventory.csv)

Current user target: **70-page report; >20,000 usable real unique images, with 50,000+ a conditional stretch goal**. University page-count rules and the approved title/language/deadline are pending. Prior VehiDE audit counts are preserved, not re-run; the existing 36-image pilot has open expert labels. The proposed 60-case protocol extends that pilot rather than replacing completed annotations.

**Read [continuation review](docs/08_continuation_review.md) before citing earlier audit claims:** timestamp-group overlap is a leakage warning, not verified same-vehicle leakage or demonstrated performance inflation. Uploader license tags do not resolve upstream photo rights. No actual-driveability or trained-model results are claimed.

## Status of the first assignment

| Deliverable | File | Status |
|---|---|---|
| One-page project proposal | `docs/00_proposal_one_page.md` | draft v1 |
| Dissertation outline, 40- and 70-page variants | `docs/01_dissertation_outline.md` | draft v1 |
| Dataset inventory (verified + pending) | `docs/02_dataset_inventory.md`, `data/dataset_inventory.csv` | verified for 8 candidates |
| Labeling guide (observation / action / outcome) | `docs/03_labeling_guide.md` | draft v1 |
| Labeling pilot | `pilot/04_pilot_report.md`, `pilot/pilot_sample_manifest.csv`, `pilot/pilot_sheet_36_images.png` | sample built, labels open |
| Dataset sourcing plan to reach 5k–10k | `docs/06_dataset_sourcing_plan.md` | verified counts, ranked queue, access steps |
| Decisions needed from you | `docs/05_open_questions.md` | open |
| References | `docs/references.bib` | draft, marked for verification |
| Process log (one entry per session) | `docs/journal.md` | current |

Repository: https://github.com/mmmurto/vehicle-damage-triage (publicly readable at continuation review). Every session's work is
committed and pushed, and `docs/journal.md` mirrors the commit history.

## The single most important finding so far

**No public dataset checked so far contains inspection-backed driveability labels.** Every
candidate is annotated with *visible damage categories* (dent, scratch, crack, glass shatter,
flat tyre, broken lamp) at image or instance level. None links an image to a professional
inspection outcome, a repair/condemnation decision, or a "was it driven afterwards" record.

Consequence: the thesis can rigorously evaluate **agreement with expert visual triage
labels**, not actual roadworthiness. That must be stated in the research question and in
the conclusions. See `docs/02_dataset_inventory.md` section "Inspection-backed labels".

## Directory layout

```
vehtriage/
  docs/           proposal, outline, inventory, labeling guide, open questions, references
  data/           dataset_inventory.csv (machine-readable inventory)
  pilot/          pilot sample manifest + contact sheet + pilot report
  scripts/        small reproducible helpers (sheet builder, dedup, splits)
  _scratch/       throwaway downloads (safe to delete)
```

## Immediate next steps (in order)

1. **You:** confirm approved title, presentation language/date, handbook and whether a live software demo is expected; arrange permissions (including CarDD) and authenticated access as needed. Do not paste tokens/passwords into chat.
2. **Me:** dedup + audit pipeline (E0) against DrBimmer, ready to run the moment the big
   downloads land.
3. Approve the labeling rubric, then label the 36 pilot images in `pilot/pilot_sample_manifest.csv`.
4. Confirm the university's page limit, citation style and deadline (`docs/05_open_questions.md`).
5. Only then start the baseline.
