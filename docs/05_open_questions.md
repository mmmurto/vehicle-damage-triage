# Open Questions and Decisions Needed From You

Each item says why it matters and what I assume meanwhile. Work continues on the assumptions
unless you say otherwise.

## Blocking (needed before the outline is final)

**1. Page limit and what counts toward it.**
Is it 40 or 70 pages, and do figures, tables, references, front matter and appendices count?
My assumption: 40 pages including figures, excluding the title page; the 70-page variant is
the upper bound. Source: your programme handbook, not the supervisor's memory.

**2. Citation style and referencing rules.** IEEE, APA 7, Harvard, or a house style? My
assumption: IEEE numeric, since the field (IEEE TITS, CVPR) uses it.

**3. Deadline and any intermediate milestones** (proposal defence, mid-term review,
submission, viva). These set the experiment freeze date: no new experiments after
`deadline − 4 weeks`.

**4. Title.** The picture you sent is a *dataset comparison table* — its top row is a header
("dataset name / scale / task type / access"), not a dissertation title, so I could not
extract the official title from it. Please confirm:
- Working title used in all drafts: **Vehicle Damage Assessment from Images for Driveability
  Triage**
- Project name for code and the app: proposed **VehiTriage** (alternatives: DriveTriage,
  VisualRoadworthiness, TriageCar). Pick one; it appears in the repository name and the demo.

**5. Your programme's handbook and marking rubric.** Send the PDF/section. Chapter weighting
and "originality" criteria decide how much space the dataset contribution gets versus the
model contribution.

## Method-critical

**6. Ethics approval for annotators.** Will you label alone, or recruit 2–3 annotators (a
mechanic, a workshop foreman, an insurance assessor)? Agreement between annotators is a
core result; if you must label alone, say so now, because then RQ1 becomes "expert visual
triage labels produced by a single rater" and the limitation must be written in from the
start. Check whether your institution requires ethics review even for image annotation
by colleagues.

**7. Dataset access.** Can you (a) submit the CarDD licence form — it may need an
institutional signature and a supervisor's endorsement — and (b) download VehiDE from Kaggle
(account + terms acceptance)? Both are needed to reach 10,000 images. If (a) is refused, the
10,000 target is at risk and we switch to Plan B (see `docs/02_dataset_inventory.md` §4).

**8. Any local source of outcome-linked images.** Even 50 images with a known
"was it driven / was it towed / what did the inspector find" outcome would transform the
validity of the thesis, because it would give a small inspection-backed slice alongside the
large expert-visual slice. Do you have access to a workshop, recovery operator, insurer,
leasing company or driving school that could supply anonymised cases with outcomes? If yes,
that becomes a separate small study inside the thesis and a strong discussion point.

**9. Compute.** What is available: a local GPU (which model/VRAM), Colab/Kaggle notebooks, or
university cluster? This decides whether the improvement model is a fine-tuned ConvNeXt-T /
ViT-B or a frozen-backbone linear probe. My assumption until told otherwise: free Colab
(T4, 16 GB), ≤ 6 h per run, so fine-tuning a small backbone at 224–384 px is feasible and
everything else must be an adapter or a linear probe.

**10. Demo scope.** Does the dissertation need a runnable user-facing application, or is a
notebook + CLI enough? The brief mentions spoken output and image input; if a demo is
required, a small local app that takes 1–6 photos, prints category + evidence + next step and
speaks the summary is ~2 days of work once the model exists. Confirm whether that counts
toward the page limit (it should go in an appendix).

## Provisional decisions I have already made

| Decision | Value | Change if… |
|---|---|---|
| Reference standard | expert visual triage labels (no inspection data available publicly) | you find an outcome-linked source (item 8) |
| Primary metric | visual-triage hazard-miss rate (count + rate + CI among expert-labelled hazardous cases) | inspection labels become available |
| Classes | 3, with `inspection_required` as the abstain/default class | pilot κ < 0.4, then collapse to binary hazard + coverage flag |
| Splits | grouped by inferred vehicle/case, plus an independent-source test set | grouping fails, then image-level with the limitation stated |
| Augmentation | allowed in training only, counted separately, never in test | — |
| Model family | transfer-learned CNN/ViT baseline; multi-view + abstention as the improvement | compute limits (item 9) |
| Labeling tool | CSV manifest + contact sheet, then a light local labelling UI if > 1,000 images | — |

## Things I will not do without your confirmation

- Invent any performance number, dataset count, or citation.
- Claim the system determines roadworthiness.
- Redistribute dataset images in a public repository without checking the licence.
