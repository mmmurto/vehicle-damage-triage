# Labeling pilot v0.1 — ready-to-run protocol, NOT completed labels

## Unit and sample
Extend the existing 36-image unlabeled pilot [R2] toward 60 licensed vehicle/incident cases. Aim for 20 initially suspected cosmetic cases, 20 suspected visible-hazard cases and 20 ambiguous/quality/coverage cases. These are sampling strata, not assigned ground truth. Prefer 2–4 views per case (about 120–240 images); do not fabricate grouping when only single images exist. If grouping is unavailable, run a clearly named 60-image pilot and record this limitation. This is a difficulty-enriched pilot, not a deployment-prevalence estimate or a final performance test.

Ensure inclusion of tire/wheel damage, front/rear/side glass, scratches/dents near impact areas, suspected fluid, poor lighting, missing viewpoints and apparently undamaged cars. Categories may overlap. Source mix depends on permissions. Keep pilot/development cases out of the final test, unless a distinct blind protocol is approved before any model development.

## Annotators and workflow
Two independent reviewers label the same cases without seeing model outputs or each other's decisions. Prefer qualified automotive reviewers; otherwise train annotators and require a qualified automotive assessor for adjudication. Do not describe student-only labels as expert review. Randomize order; preserve original votes; record qualifications, time and evidence. Review disagreements, identify missing views and revise this guide before scaling. Re-label changed definitions and retain version history.

## Three separate label layers
1. Visible observation: component/location, damage appearance, severity description, localization if possible, image IDs supporting the observation. Distinguish observed, not visible and uncertain. Avoid hidden-function claims.
2. Recommended visual action: one of the three categories below with evidence and next step. Record coverage sufficiency and unresolved issues separately.
3. Inspection outcome: unknown unless there is a legitimately linked record; include record ID, date, assessor qualification, tests and result/reason. Never fill it using the model or appearance alone.

## Decision guide
**Do not drive:** Credible visible evidence of a serious hazard, for example shredded tire, conspicuously displaced wheel after impact, or severe windshield destruction obstructing the driver's view. Name evidence and recommend professional assessment before driving. A clear hazard is not downgraded merely because other views are missing. Do not infer unseen severity from a generic damage class.

**Inspection required:** No decisive visible hazard but photos are blurry/incomplete, an impact hides safety-critical components, glass severity/location is unresolved, liquid may be leaking, or steering-related effects would require functional checks. State what is unresolved; request targeted views and/or hands-on professional inspection. Uncertain liquid is not proof of brake-fluid leakage.

**Low visible concern:** Submitted views provide sufficient coverage for the limited visual question and show only superficial cosmetic findings, with no visible hazard or unresolved safety-critical issue in the submitted evidence. A close-up scratch alone normally lacks coverage; route it to inspection rather than certifying the whole vehicle. Required wording: “Minor cosmetic damage is visible. Roadworthiness was not verified.” If no damage is visible, describe that accurately instead of inventing cosmetic damage.

## Coverage and glass
Record front/rear/left/right overview availability, impact-context view, affected tire/wheel close-ups and glass context where relevant. Define coverage sufficiency for the specific damage and scope; do not call a standard photo checklist proof of roadworthiness. Record glass position (front windshield/rear/side), damage extent, obstruction relative to driver field of view (visible/not assessable), and uncertainty. Generic “broken glass” is not a deterministic action label. Local legal requirements are outside this visual pilot unless separately documented.

## Disagreement/quality analysis
Tabulate class counts, quality flags and missing views; calculate raw action agreement and nominal Cohen's kappa with uncertainty where feasible. Report per-class disagreement and adjudication count; note prevalence effects. Examine low-concern vs do-not-drive disagreements first. Do not force a fabricated inspection outcome when reviewers disagree. Pilot stop/revise triggers include unclear coverage definitions, repeat glass disagreements, leakage over-interpretation and insufficient qualified review.

## Illustrative vignettes — invented training examples, NOT photo annotations
| Scenario | Action | Rationale / next step |
|---|---|---|
| Adequate overview + shallow door paint scratch; no unresolved impact concern | Low visible concern | Describe cosmetic scratch; roadworthiness not verified |
| Only a close-up scratch with no surrounding context | Inspection required | Inadequate coverage; request overviews and inspection as needed |
| Clearly shredded tire visible | Do not drive | Name tire damage; professional assistance before driving |
| Wheel conspicuously displaced after impact | Do not drive | Name displaced wheel; do not infer steering/brake function |
| Liquid under vehicle, source not identifiable | Inspection required | Suspected leak unresolved; professional assessment |
| Windshield image too distant to assess crack extent or visibility | Inspection required | Need location/extent and driver-view assessment |
| Windshield shattered across driver field of view | Do not drive | Visible severe visibility hazard; professional repair/assessment |
| Small rear-glass defect, cropped context and unclear extent | Inspection required | Location alone insufficient; assess extent and associated hazard |

## Pilot completion sheet
Existing project: 36 sampled DrBimmer images with open labels [R2]. This session proposes a 60-case extension, not completed expert annotations. Additional cases acquired in this session: 0. Qualified reviewers recruited: pending. Agreement: not measured. Adjudicated cases: 0. Targets: not set. No attached user image is a damaged-vehicle photograph; supplied images are reference material and a chat screenshot.
