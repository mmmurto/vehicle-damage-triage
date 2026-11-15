# Vehicle Damage Assessment from Images for Driveability Triage

Dissertation research workspace. Started 2026-11-15.

## What this is

A computer-vision system that reads photos of a damaged passenger car and outputs one of
three triage categories with the visible evidence and a recommended next step:

1. **Low visible concern** — minor cosmetic damage, coverage adequate; roadworthiness not verified.
2. **Do not drive** — visible hazard (shredded tyre, displaced wheel, etc.); professional assessment first.
3. **Inspection required** — photos incomplete/unclear, or a safety-critical issue is unresolved.

## Status of the first assignment

| Deliverable | File | Status |
|---|---|---|
| One-page project proposal | `docs/00_proposal_one_page.md` | draft v1 |
| Dissertation outline, 40- and 70-page variants | `docs/01_dissertation_outline.md` | draft v1 |
| Dataset inventory (verified + pending) | `docs/02_dataset_inventory.md`, `data/dataset_inventory.csv` | verified for 8 candidates |
| Labeling guide (observation / action / outcome) | `docs/03_labeling_guide.md` | draft v1 |
| Labeling pilot | `pilot/04_pilot_report.md`, `pilot/pilot_sample_manifest.csv`, `pilot/pilot_sheet_36_images.png` | sample built, labels open |
| Decisions needed from you | `docs/05_open_questions.md` | open |
| References | `docs/references.bib` | draft, marked for verification |

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

1. Confirm the university's page limit, citation style and deadline (`docs/05_open_questions.md`).
2. Approve the labeling rubric, then label the 36 pilot images in `pilot/pilot_sample_manifest.csv`.
3. Request CarDD via its licence form; download VehiDE from Kaggle; check the licence wording.
4. Build the dedup + grouping pipeline before any training split exists.
5. Only then start the baseline.
