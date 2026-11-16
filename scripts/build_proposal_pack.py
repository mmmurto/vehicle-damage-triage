from pathlib import Path
import csv, json, zipfile
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from docx import Document
from docx.shared import Inches as DI, Pt as DP

ROOT=Path.cwd(); OUT=ROOT/'defence-pack-final'; OUT.mkdir(exist_ok=True)
def save_text(name,text):
 p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.strip()+'\n',encoding='utf-8')

sources=[
('S1','CarDD official project','https://cardd-ustc.github.io/','4,000 images; over 9,000 instances; six visual damage categories.'),
('S2','CarDD original license','https://cardd-ustc.github.io/docs/CarDD_license.pdf','Prior consent for research; no third-party redistribution without authorization; cite original paper.'),
('S3','VehiDE research team','https://cvis.hcmute.edu.vn/Research/Details/4','13,945 images; over 32,000 instances; eight categories reported.'),
('S4','VehiDE Kaggle distribution','https://www.kaggle.com/datasets/hendrichscullen/vehide-dataset-automatic-vehicle-damage-detection','Count corroborated; exact upstream rights and local archive counts pending.'),
('S5','Roboflow car_damages_19k v1','https://universe.roboflow.com/tarpit-patel-uyibg/car_damages_19k/dataset/1','Search-index listing: 19,100 total, no augmentation; direct fetch met security verification. License and provenance pending.'),
('S6','AI-Hub vehicle damage dataset 581','https://aihub.or.kr/aihubdata/data/view.do?dataSetSn=581','Reports 632,694 images and 125,007 estimate records; application restricted to Korean nationals; version 1.1 dated 2023-02-01.'),
('S7','JijoJS/car-damage-new1','https://huggingface.co/datasets/JijoJS/car-damage-new1','Card: 2,427 images (2,187/120/120); dent/scratch; COCO; CC BY 4.0; no augmentation reported.'),
('S8','DrBimmer/comprehensive-car-damage','https://huggingface.co/datasets/DrBimmer/comprehensive-car-damage','Card/viewer: 2,300 rows; front/rear normal, crushed, breakage. Rights pending; normal does not mean roadworthy.'),
('S9','AutoDamageIQ merged dataset','https://huggingface.co/datasets/tugberkkalay/autodamageiq-vehicle-damage-dataset','13,089 training + 2,094 validation images; CarDD + VehiDE + GPT-4o-labeled HITL. Not an independent source.'),
('S10','CompCars official project','https://mmlab.ie.cuhk.edu.hk/datasets/comp_cars/index.html','136,726 whole-car web images; 27,618 part images; 50,000 surveillance images. Auxiliary recognition, not verified safe controls.'),
('S11','CompCars release agreement','http://mmlab.ie.cuhk.edu.hk/datasets/comp_cars/agreement.pdf','Non-commercial research by signed agreement; restrictions on redistribution and publication.'),
('S12','xanoutas/vehicle-damage-detection','https://huggingface.co/datasets/xanoutas/vehicle-damage-detection','Viewer: 495 rows, 15 classes; provenance/license pending.'),
('R1','Prior VehiDE archive audit at 3482f30','https://github.com/mmmurto/vehicle-damage-triage/blob/3482f30/docs/07_vehide_audit.md','Prior project audit: 13,945 files, 36,081 regions, seven released classes; reviewed, not re-run here. Timestamp overlap is not verified vehicle leakage.'),
('R2','Existing 36-image pilot at 3482f30','https://github.com/mmmurto/vehicle-damage-triage/blob/3482f30/pilot/04_pilot_report.md','36-image sample and contact sheet exist; expert labels and agreement remain open.')]
save_text('research/SOURCES.md','# Source evidence ledger\n\nVerification session: 2026-11-16 workspace date. This is a documentation audit, NOT a downloaded-image audit. Freeze actual access timestamps and dataset revisions before use.\n\n'+'\n\n'.join(f'## {s[0]} — {s[1]}\nURL: {s[2]}\nObserved: {s[3]}' for s in sources)+'\n\n## References ready to verify/style\n- Wang, X., Li, W., and Wu, Z. (2023). CarDD: A New Dataset for Vision-Based Car Damage Detection. IEEE Transactions on Intelligent Transportation Systems, 24(7), 7202–7214. DOI: 10.1109/TITS.2023.3258480.\n- VehiDE Dataset: New dataset for Automatic vehicle damage detection in Car insurance (2023). DOI: 10.1109/KSE59128.2023.10299490. Author list must be retrieved before final bibliography.\n\nNo web source has been verified to provide linked, functional roadworthiness outcomes. An insurance expert annotating damage is not the same as an inspection confirming driveability.')
rows=[
['CarDD','S1;S2',4000,'publisher-reported images','unknown', 'dent;scratch;crack;glass shatter;tire flat;lamp broken','boxes;instance masks;COCO','not verified','custom prior-consent research license','permission required; no unauthorized redistribution','high priority; request access','original license overrides mirror claims'],
['VehiDE','S3;S4;R1',13945,'prior project archive audit at 3482f30; not re-run here','unknown','seven released classes in prior audit; paper says eight','VIA polygons;36081 regions in prior audit','not verified','Apache 2.0 listing in prior audit; upstream rights unresolved','original rights audit still required','existing volume backbone; dedup pending','timestamp overlap is proxy not vehicle identity; no tire/wheel/fluid class'],
['Roboflow car_damages_19k v1','S5',19100,'indexed version total; not archive-audited','unknown','damage segmentation; exact classes pending','instance segmentation','not verified','pending','security-check page; verify rights and origins','candidate only','no augmentation reported; overlap with other sources unknown'],
['AI-Hub vehicle damage 581','S6',632694,'portal-reported accident images','unknown; 125007 estimate records are not vehicle count','parts;damage type;extent','JSON;segmentation;estimate information','estimates present; roadworthiness outcomes not verified','portal terms pending','applications restricted to Korean nationals on page','restricted-access lead; not secured','do not bypass eligibility; repair cost is not a safety label'],
['JijoJS/car-damage-new1','S7',2427,'card split sum','unknown','dent;scratch','COCO boxes','not verified','CC BY 4.0 stated by card','attribution; upstream provenance still to check','possible small cosmetic source','may or may not be user remembered dataset'],
['DrBimmer/comprehensive-car-damage','S8;R2',2300,'prior project audit and current card/viewer','unknown','front/rear normal;crushed;breakage','image classes','not verified','pending','do not use until terms established','candidate mixed-condition source','existing 36-image sample, expert labels open; MIT uploader tag reported in repository, upstream rights unresolved; normal not safe'],
['AutoDamageIQ merged','S9',15183,'card split sum','unknown','six CarDD-like categories','YOLO boxes;includes GPT-4o labeling','not verified','CC BY 4.0 metadata claim; upstream restrictions unresolved','contains CarDD; original license still applies','audit only; NOT independent collection','prior repository audit reports only 12094 image files vs card 15183; recount needed; do not sum with originals; AI labels not expert ground truth'],
['CompCars auxiliary','S10;S11',136726,'whole-car web subset; other subsets separate','unknown','vehicle models;viewpoints;parts, not damage outcomes','boxes;attributes;viewpoints','not verified','custom signed non-commercial research agreement','redistribution/publication restricted','auxiliary pretraining only if approved','do not count as damaged-photo target or automatically safe'],
['xanoutas/vehicle-damage-detection','S12',495,'viewer rows','unknown','15 visual classes','image classes','not verified','pending','check provenance and rights','small candidate','not 2500 images'],
['User original Hugging Face dataset','pending','','unidentified','unknown','pending','pending','pending','pending','exact URL needed','blocked on user','do not assume identity']]
with (OUT/'research/dataset_inventory.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.writer(f); w.writerow(['dataset','source_ids','reported_count','count_basis','unique_vehicles','damage_coverage','label_types','inspection_backing','license_status','restrictions','decision','cautions']);w.writerows(rows)
save_text('research/DATASET_DECISION.md','''# Data acquisition decision — provisional

## What can be claimed today
- Candidate sizes have been checked against publisher pages, cards or indexed version pages, not downloaded archives.
- No additional vehicle photos were acquired in this session. Prior project audit at 3482f30 reports 13,945 VehiDE images and 36,081 regions [R1], reviewed but not re-run here. Existing pilot: 36 sampled DrBimmer images, labels open [R2]. Final unique-image/vehicle totals remain unverified.
- CarDD + VehiDE have a nominal sum of 17,945 published images, BEFORE overlap checks and permissions. This is not an acquired total.
- The 19,100-image Roboflow candidate could help exceed 20,000, but its license, provenance, passenger-car suitability and independence are unresolved. Do not sum all rows in the inventory.
- More than 50,000 usable real damaged-vehicle images is a stretch acquisition goal, not an achieved milestone. AI-Hub is numerically large but access is restricted; CompCars cannot be used to inflate the damaged-image target.
- No reviewed source has verified functional roadworthiness outcomes linked to photos. Seek a qualified workshop partner and consented inspection records; meanwhile evaluate expert visual triage.

## Acquisition gates
1. Identify exact user HF URL and repository revision. Save original card, terms, version/revision, contact and permission evidence.
2. For every source, verify training, dissertation illustration, derivative-model publication and redistribution permissions separately. Do not assume a mirror's license supersedes its source.
3. Audit actual decoded images; count corrupt files, non-passenger vehicles, duplicates, synthetic images and augmented derivatives separately.
4. Match exact file hashes plus decoded-pixel hashes; generate perceptual-hash and embedding candidates and visually review near duplicates. Group transformed copies and known vehicle/incident IDs across sources BEFORE splitting.
5. Maintain original source-level sets and counts. Where identity is unknown, disclose possible leakage rather than calling all images independent vehicles.
6. Select an independent source test if feasible; group remaining vehicles/incidents 70/15/15 as a provisional split. Freeze manifests before training. No synthetic or augmented photos in the final test.
7. Start with a licensed pilot. Expand only after agreement review; prioritize wheel/tire, glass, leakage uncertainty, low-quality and missing-angle cases rather than raw volume.
8. Plot grouped learning curves at feasible sample sizes, with fixed evaluation sets. Choose expansion by measured gains and case coverage.

## Inspection-backed evidence checklist
Ask providers whether records include photo-to-case linkage, inspection date relative to photo, assessor qualification, checks performed (tires/wheels, visibility, brakes, steering and other relevant functions), explicit out-of-service decision and reasons, and any repairs between photo and inspection. Estimates, total-loss status and visual severity alone are insufficient. Record unknown/partial outcomes without converting them into confirmed safe labels.

## GitHub
Do not commit source image archives, API keys, personal records, unredacted plate/face data or unapproved screenshots. Commit provenance manifests, rights decisions, labeling guides, code, configurations, aggregate metrics, experiment logs and permitted derived artifacts. The repository became publicly readable, was cloned at 3482f30 and reviewed. Publication is tracked separately; local generation is not proof of a successful push.
''')
proposal='''# One-page project proposal — provisional

**Working title:** Vehicle Damage Assessment from Images for Driveability Triage  
**Approved title / student / supervisor:** To be confirmed.  
**Status:** Proposal stage; no training or performance results claimed.

## Problem and aim
Vehicle photographs can reveal cosmetic damage and serious visible hazards, but cannot establish mechanical roadworthiness. This project will investigate an evidence-based computer vision system for preliminary passenger-vehicle triage. Each output will contain a visible finding, a recommended action and a clear limitation statement.

## Research questions
RQ1: How reliably can a baseline distinguish expert-reviewed low visible concern, do not drive and inspection required cases? RQ2: Does visible-damage localization and, where available, multi-view aggregation reduce serious visual cases assigned low concern compared with an image-only baseline? RQ3: How does inspection referral trade off against missed serious damage across sources and difficult conditions? Actual driveability will be evaluated only if adequately linked inspection-backed outcomes become available.

## Data and labeling
Target more than 20,000 usable unique real images; 50,000+ is a conditional stretch goal. Prior project audit reports 13,945 VehiDE files and 36,081 regions [R1], not recounted here. CarDD (4,000) and Roboflow (19,100 listed) remain candidates with rights/overlap checks [S1–S5]. Extend the existing 36-image unlabeled pilot [R2] toward 60 cases with independent reviewers and qualified adjudication. Separate visible observation, action and verified inspection outcome. Track image quality, viewpoints, glass location/visibility, tires/wheels and uncertain leakage. No inspection-backed outcome dataset has yet been verified.

## Proposed method and evaluation
Build on the reviewed GitHub scaffold and audit scripts. Train a reproducible transfer-learning image classifier as baseline; compare a damage-localization model plus conservative decision policy, and multi-view pooling when case grouping exists. Deduplicate across sources and keep vehicles/incidents within one split. Use validation-only threshold selection, a frozen held-out test and, if feasible, an independent-source test. Primary error: expert do-not-drive cases predicted low visible concern, divided by all expert do-not-drive reference cases; rename and evaluate against confirmed unsafe outcomes only when inspection-backed labels exist. Report counts, confidence intervals, per-class precision/recall, confusion matrix, inspection-referral rate and risk–coverage trade-offs. Fix numerical targets after the pilot and before final testing.

## Deliverables and sequence
Five-minute proposal defence → rights/provenance audit and pilot → baseline → practical improvement → frozen evaluation and error analysis → reproducible demo and 70-page dissertation draft. The prototype accepts image-capable input and returns category, evidence and next step, with optional spoken summary. Experiments and dates remain pending; approval, deadline, title and handbook must be confirmed. Contribution: a transparent evaluation of visual triage—not a certificate that a vehicle is safe to drive.
'''
save_text('docs/PROJECT_PROPOSAL.md',proposal)
save_text('docs/DISSERTATION_OUTLINE.md','''# Dissertation outline — page budgets

User target: 70 pages. University rules on what counts have NOT been confirmed. The 40-page version is retained as a fallback only. Allocations below include front matter, references and appendices; change the budget once the handbook is available.

| Section | 70-page budget | 40-page fallback | Content |
|---|---:|---:|---|
| Front matter incl. abstract | 4 | 3 | Cover/declarations/abstract/contents; exact mandatory items pending |
| 1 Introduction | 6 | 4 | Motivation, scope, three RQs, contributions, safety boundary |
| 2 Literature review | 10 | 5 | Damage recognition, visual triage, uncertainty, multi-view, selective prediction; verified citations only |
| 3 Dataset and labeling methodology | 11 | 6 | Rights, source provenance, uniqueness, grouping, pilot, expert agreement and label validity |
| 4 Model and system design | 10 | 6 | Baseline, localization/policy improvement, optional multi-view, image interface and speech |
| 5 Evaluation methodology | 7 | 4 | Frozen splits, target-setting, metrics, thresholds, CIs, source tests and ablations |
| 6 Results | 7 | 3 | PLACEHOLDERS until experiments run; learning curves, confusion matrices, risk–coverage |
| 7 Discussion and limitations | 6 | 3 | Error cases, appearance vs function, grouping limits, label uncertainty, ethics |
| 8 Conclusion | 2 | 1 | Answer RQs only from actual evidence, practical limits, future work |
| References | 4 | 3 | Citation style pending; complete author/DOI verification |
| Appendices | 3 | 2 | Label guide excerpts, configurations, interface outputs and reproducibility links |
| **Total** | **70** | **40** | |

The 70-page budget has 59 pages across Chapters 1–8. If 70 means main-body pages only, reallocate after confirmation rather than padding. Full manifests and experiment details belong in GitHub/permitted supplementary files, with compact report excerpts. Do not copy the sample student's GNN title, identity, dates or research content.

## Results placeholders
- Dataset usable unique image / vehicle / incident counts: NOT YET AUDITED.
- Expert agreement and adjudication statistics: NOT YET RUN.
- Baseline and improvement metrics: NOT YET RUN.
- Thresholds and numerical targets: TO BE LOCKED after pilot, before final testing.
- Independent-source generalization and learning curves: NOT YET RUN.
''')
save_text('labeling/PILOT_GUIDE.md','''# Labeling pilot v0.1 — ready-to-run protocol, NOT completed labels

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
''')
headers=['case_id','image_ids','source_id','source_revision','rights_record','vehicle_id_if_known','incident_id_if_known','reviewer_id','reviewer_qualification','guide_version','visible_observation','component_location','supporting_image_ids','quality_flags','views_present','coverage_sufficient','glass_location','glass_extent','driver_visibility_effect','unresolved_safety_issue','visual_action','reason','next_step','inspection_record_id','inspection_date','inspection_tests','verified_outcome','adjudicated_action','adjudicator','split_group']
with (OUT/'labeling/pilot_annotations_template.csv').open('w',newline='',encoding='utf-8-sig') as f: csv.writer(f).writerow(headers)
save_text('docs/EVALUATION_PLAN.md','''# Evaluation plan v0.1

Baseline: transfer-learning image classifier (e.g. ResNet-18); exact implementation, dependency lock, seed, pretrained weights, transform and training budget recorded after repository audit. Compare a practical localization-plus-policy model; compare multi-view pooling only where legitimate grouping exists. Match data and compute budgets and pre-register comparisons. API assistance is not evidence of a trained damage model; audit what the existing implementation really does.

Labels: current intended reference is adjudicated expert visual triage. Do not call these actual driveability labels. If adequate independent inspection records become available, maintain a separate outcome endpoint and document timing and tests.

Primary visual error = count(reference visual do-not-drive AND prediction low visible concern) / count(reference visual do-not-drive). Always report numerator and denominator; undefined if denominator is zero. With inspection-backed outcomes, separately report confirmed-unsafe assigned low concern / all confirmed-unsafe. Also report serious references deferred to inspection vs directly detected so deferral cannot hide hazard-detection failures.

Report 3x3 confusion matrix, per-class precision/recall/F1 with support, overall referral fraction, referral fractions by reference class and source, and fraction of low-concern predictions with a serious reference. Include an all-inspection and simple baseline comparator. A system that defers every case has zero low-concern misses but no useful low-concern coverage; it is not automatically successful.

Plot serious-to-low-concern error versus referral rate and useful low-concern coverage over validation-selected policy thresholds. State the exact uncertainty score/coverage gate. Lock an operating point and numerical safety/usefulness criteria after the pilot, before final test access. Never tune on the test set. Treat inability to find a useful operating point as a valid result.

Use vehicle/incident-level bootstrap confidence intervals for grouped cases. If only independent image units can be established, report image-level intervals and dependence limitations. Include denominators, especially rare hazards; zero observed misses is not proof of zero risk. No fabricated rates or guarantees.

Predefined slices: lighting, blur, limited angles, front/rear/side glass, tires/wheels, suspected liquids, source and known vehicle groups. Review false low-concern cases and inspect explanation faithfulness against actual visible evidence. Run ablations for quality gates, policy rules, localization and multi-view when feasible. Maintain a blind final test and a separate independent-source test where rights and grouping permit.

Results table columns: experiment_id, git_commit, data_manifest_hash, guide_version, model/weights, seed, transforms, hyperparameters, hardware, threshold_selection, class_support, confusion_matrix, primary_numerator/denominator, referral_rate, confidence_intervals, runtime, failure_notes. All experiments remain NOT RUN.
''')

slides=[
('Vehicle Damage Assessment\nfrom Images','For preliminary driveability triage',[
'Proposal defence • Working title; official title pending',
'Visible evidence → explained action → professional follow-up',
'Photographs do not verify roadworthiness.'],35,
'''Good morning. My proposed dissertation investigates vehicle damage assessment from photographs for preliminary driveability triage. The aim is not to certify a vehicle as safe. It is to identify visible evidence, recommend a next step, and recognize when the images are insufficient. This is a proposal-stage presentation: the dataset audit, training and evaluation still need to be completed. The official dissertation title will be confirmed with my supervisor.''',''),
('The problem: appearance is not function','Why a three-way decision matters',[
'A superficial scratch and a displaced wheel need different actions.',
'Missing views and uncertain findings must remain unresolved.',
'Never infer working brakes, steering or engine from appearance.'],35,
'''A damaged vehicle may have a superficial paint scratch, an obvious tire hazard, or hidden damage that a photograph cannot resolve. A simple damaged-versus-undamaged classifier cannot distinguish these situations reliably. Even an apparently normal car may have mechanical faults. My research therefore separates visual observations from recommended actions and from verified inspection outcomes. The key motivation is to avoid false reassurance while still providing useful preliminary guidance.''',''),
('Three outputs, each with evidence','Category + visible reason + next step',[
'LOW VISIBLE CONCERN — cosmetic findings with sufficient visual coverage; roadworthiness not verified.',
'DO NOT DRIVE — clear serious visible hazard; name it and seek professional assessment before driving.',
'INSPECTION REQUIRED — incomplete views or unresolved safety-critical concern; explain what needs checking.'],45,
'''The system has three outputs. Low visible concern means the submitted views support only a limited cosmetic assessment; the output explicitly says roadworthiness was not verified. Do not drive is reserved for clear serious visible evidence, such as a shredded tire or displaced wheel. Inspection required covers missing context, unclear photographs or unresolved concerns such as possible leakage. Glass must be assessed by location, extent and effect on visibility, not just a broken-glass label. Every output explains the visible reason and next step.''',''),
('Data: substantial candidates, not secured totals','20,000+ usable real images targeted • 50,000+ stretch goal',[
'CarDD: 4,000 images; six visual damage classes. [S1–S2]',
'Prior VehiDE audit: 13,945 files; 36,081 regions; seven released classes. [R1]',
'Roboflow candidate: 19,100 listed; rights and overlap pending. [S5]',
'Final deduplicated total and inspection-backed outcomes remain unverified.'],45,
'''The collection target is more than twenty thousand usable real images, with fifty thousand a stretch goal if access and useful coverage allow. Our prior VehiDE audit reports thirteen thousand nine hundred forty-five files and thirty-six thousand eighty-one regions across seven released classes. I reviewed, but did not repeat, that audit. CarDD and a nineteen-thousand-image Roboflow candidate could add coverage, subject to rights and overlap checks. These numbers cannot simply be added because sources may overlap. More importantly, no reviewed source has yet been verified to contain linked functional roadworthiness outcomes. Without those outcomes, the research will evaluate expert visual triage, not actual driveability.''','R1: prior audit, not re-run here. S1–S5: candidate counts. No additive unique total.'),
('Pilot first, then scale','Separate observation, action and inspection outcome',[
'Existing pilot: 36 sampled images, labels open; extend toward 60 cases. [R2]',
'Include cosmetic, serious and ambiguous cases; review glass, tires and missing views.',
'Deduplicate across sources; group vehicles/incidents before splitting.',
'Hold out an independent source where possible; synthetic/augmented data stay out of final tests.'],40,
'''The repository already contains a thirty-six-image pilot sample with labels still open. I propose extending it toward sixty cases with hazard and borderline examples. Two reviewers will record observations and actions independently, with qualified automotive adjudication. We will study disagreement and missing viewpoints before expanding the guide. Duplicate and near-duplicate images must be removed or grouped across sources. Images from the same vehicle or incident must stay in the same split where identity is available. Where grouping is unknown, that limitation will be reported rather than assuming independence.''','Sample exists; expert labels remain open. Timestamp groups are proxies, not vehicle IDs.'),
('Build a baseline, then test one improvement','Proposed system — builds on existing data-audit scaffold',[
'Image-capable input → quality/coverage assessment → visual model.',
'Baseline: transfer-learning image classifier.',
'Improvement: damage localization + conservative evidence policy; multi-view pooling if grouping exists.',
'Output: category, finding, next step; optional short spoken summary.'],35,
'''The baseline will be a reproducible transfer-learning image classifier. The practical improvement will identify visible damage and combine it with an explicit conservative action policy. If several photographs can be linked to one vehicle, I will test multi-view aggregation against the image-level baseline. The interface must send photographs to an image-capable component. It will return the category, evidence and next step, optionally read aloud. The current repository provides data-audit scripts and research documentation, not a trained triage model.''','No trained-model or working-demo claim is made.'),
('Evaluation: reduce false reassurance','Safety error AND useful coverage must be reported',[
'Primary visual error: expert do-not-drive cases assigned low concern / all expert do-not-drive cases.',
'Report error counts, per-class precision/recall, confusion matrix and uncertainty.',
'Plot missed-serious-case vs inspection-referral trade-off; all-inspection is a comparator, not success.',
'Select thresholds on validation data; freeze targets before final test.'],40,
'''The primary visual error is an expert do-not-drive case assigned low visible concern. I will report its count and rate using all expert do-not-drive reference cases as the denominator. If inspection-backed outcomes become available, a separate confirmed-unsafe error will be reported. Evaluation also includes per-class precision and recall, confusion matrices, uncertainty and inspection referral rate. Referring every case cannot count as useful success, so the trade-off must be shown. Thresholds are selected on validation data, with numerical targets fixed after the pilot and before final testing.''','No numerical model performance results exist for this proposal.'),
('Plan and expected contribution','A defensible visual-triage study, not a roadworthiness certificate',[
'1  Confirm title, deadline and handbook; build on reviewed GitHub work.',
'2  Secure data rights; run pilot; freeze labels and splits.',
'3  Train baseline; compare improvement; analyze held-out errors.',
'4  Document reproducible findings and limitations in the 70-page report.'],25,
'''The next steps are to confirm the approved title and university requirements, extend the reviewed repository, and secure suitable data permissions. Then I will run the pilot, train the baseline and improvement, and evaluate on held-out data. The expected contribution is an auditable visual-triage system and an honest analysis of its limitations, documented in the planned seventy-page dissertation. No experimental results are claimed today. Thank you.''','Relative sequence only; calendar dates await the confirmed deadline.')]
# Total allocated time: 300 seconds.
prs=Presentation();prs.slide_width=Inches(13.333);prs.slide_height=Inches(7.5)
NAVY='101B2C';WHITE='F3F6FA';MUTED='AFC0D2';TEAL='49D5C6';AMBER='FFCD74'
def textbox(sl,x,y,w,h,text,size=24,color=WHITE,bold=False):
 box=sl.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)); tf=box.text_frame;tf.word_wrap=True
 for i,line in enumerate(text.split('\n')):
  p=tf.paragraphs[0] if i==0 else tf.add_paragraph();p.text=line;p.font.name='Aptos';p.font.size=Pt(size);p.font.bold=bold;p.font.color.rgb=RGBColor.from_string(color);p.space_after=Pt(10)
 return box
for i,(title,sub,bullets,seconds,notes,foot) in enumerate(slides):
 sl=prs.slides.add_slide(prs.slide_layouts[6]);sl.background.fill.solid();sl.background.fill.fore_color.rgb=RGBColor.from_string(NAVY)
 textbox(sl,.6,.28,12,.35,'RESEARCH PROPOSAL  /  VEHICLE DAMAGE TRIAGE',12,TEAL,True)
 textbox(sl,.6,.95,12,1.35 if i==0 else .8,title,36 if i==0 else 32,WHITE,True)
 textbox(sl,.62,2.32 if i==0 else 1.85,12,.55,sub,20,TEAL)
 y=3.25 if i==0 else 2.65
 for b in bullets:
  textbox(sl,.72,y,.25,.3,'•',22,TEAL,True)
  textbox(sl,1.05,y,11.4,.77 if len(b)>120 else .66,b,22 if i!=2 else 21)
  y+=.85
 textbox(sl,.62,6.72,11.7,.35,foot or 'Proposal-stage work • Photographs cannot establish mechanical roadworthiness.',11,MUTED)
 textbox(sl,12.1,7.1,.7,.25,f'{i+1:02}',12,TEAL)
 sl.notes_slide.notes_text_frame.text=f'Target: {seconds} seconds\n\n{notes}\n\n'+foot
# appendix not in 5-minute talk
for group in (sources[:6], sources[6:12], sources[12:]):
 sl=prs.slides.add_slide(prs.slide_layouts[6]);sl.background.fill.solid();sl.background.fill.fore_color.rgb=RGBColor.from_string(NAVY)
 textbox(sl,.6,.5,12,.6,'Source appendix — not part of the timed talk',28,WHITE,True)
 y=1.4
 for sid,name,url,claim in group:
  textbox(sl,.65,y,12,.32,f'{sid}  {name}',17,TEAL,True);textbox(sl,.65,y+.33,12,.5,url,13,MUTED);y+=.88
 sl.notes_slide.notes_text_frame.text='Backup source slide only. See research/SOURCES.md for exact claims, rights and pending checks. Do not add dataset totals.'
with (OUT/'vehicle_damage_proposal_defence.pptx').open('xb') as f:prs.save(f)
script='# Five-minute speaker script\n\n8 timed slides, 300 seconds total. Three source appendices are backup only. English is provisional pending language confirmation. Replace working title and presenter details after confirmation. Rehearse; timing varies with speaking pace. This is a proposal defence, not a live trained-system demo.\n\n'
for i,(title,sub,bullets,seconds,notes,foot) in enumerate(slides):script+=f'## Slide {i+1} — {title.replace(chr(10)," ")} ({seconds}s)\n\n{notes}\n\n'
script+='''## Likely examiner questions

**Can you really decide if a car can be driven?** No. The intended endpoint is expert visual triage. Actual driveability requires adequate linked inspection evidence and functional checks beyond photos.

**How many images do you have now?** The prior project audit reports 13,945 VehiDE files and 36,081 regions, reviewed rather than repeated here. A 36-image DrBimmer pilot sample exists with labels open. Final cross-source deduplicated usable totals and unique-vehicle counts remain unverified.

**Why target 20,000 or 50,000?** It is an acquisition goal, not a scientific guarantee. Learning curves and failure-case coverage will determine whether more data helps. Rights, case diversity and label quality matter more than raw count.

**What is new?** A practical comparison of a reproducible image baseline with evidence-based action policy and optional multi-view aggregation, emphasizing false reassurance and deferral trade-offs. Novelty claims require the literature review, not assertions of a new algorithm today.

**What if every case goes to inspection?** Report referral rate and useful low-concern coverage alongside missed serious cases, and compare with an all-inspection policy.

**Where are the results?** Not run yet. This defence presents a proposed method, verified candidate information, and a planned evaluation.

**What about broken glass?** Record location, severity, driver visibility and uncertainty. The generic class alone does not determine action.

**Why not use repair estimates as safety labels?** They measure repair/claim information, not necessarily steering, brakes or confirmed roadworthiness.

## Before presenting
- Confirm the official title, presenter name, supervisor and presentation language.
- Confirm whether the teacher expects proposal slides only or also a live software demonstration.
- Replace relative milestones with approved dates; never copy the sample GNN student's schedule.
- Rehearse the eight-slide core in five minutes. Keep source slides for questions.
'''
save_text('five_minute_script_and_questions.md',script)
# Compact editable one-page proposal; page count depends on installed Word fonts/printer.
doc=Document();sec=doc.sections[0];sec.top_margin=DI(.55);sec.bottom_margin=DI(.55);sec.left_margin=DI(.65);sec.right_margin=DI(.65)
normal=doc.styles['Normal'];normal.font.name='Calibri';normal.font.size=DP(9);normal.paragraph_format.space_after=DP(4)
for line in proposal.strip().splitlines():
 if not line.strip():continue
 if line.startswith('# '):doc.add_heading(line[2:],0)
 elif line.startswith('## '):doc.add_heading(line[3:],2)
 else:doc.add_paragraph(line.replace('**','').replace('  ',''))
with (OUT/'docs/one_page_project_proposal.docx').open('xb') as f:doc.save(f)
save_text('README.md','''# Vehicle damage visual-triage — proposal defence pack

## Start here
- `vehicle_damage_proposal_defence.pptx`: eight timed English proposal slides + three backup source slides; speaker notes embedded. Official title and language pending confirmation.
- `five_minute_script_and_questions.md`: timed talk and examiner answers.
- `docs/one_page_project_proposal.docx` / `PROJECT_PROPOSAL.md`: provisional proposal. DOCX is compactly formatted for one page; pagination requires a Word/LibreOffice visual check.
- `docs/DISSERTATION_OUTLINE.md`: 70-page target and 40-page fallback.
- `research/`: inventory, source ledger and acquisition gates.
- `labeling/`: 60-case pilot protocol and EMPTY annotation template; no actual vehicle photos labeled.
- `docs/EVALUATION_PLAN.md`: planned endpoints and reproducibility requirements.

## Status / honesty boundary
No additional archive downloaded here. Existing repository at 3482f30 was cloned and reviewed: prior VehiDE audit reports 13,945 files, 36,081 regions and seven released classes; a 36-image pilot sample exists with labels open. Counts were not re-run here. Final deduplicated totals, unique vehicles, linked roadworthiness outcomes, expert agreement and trained-model results remain unverified. Timestamp overlap is not confirmed same-vehicle leakage. See session publication log for push status.

## University documents
The task sheet and opening-report documents are examples for another student, about GNN spatial-network decoding. Use their structural sections (background/significance; related work; contents/problems; methods; schedule; references), not their identity, research claims, dates or title. The WeChat screenshot explicitly requests a five-minute proposal debate; the embedded schedule/title is too small to identify reliably. The other image is a dataset comparison table, not an approved title.

## GitHub integration once access is available
1. Authenticate through normal GitHub/browser or approved CLI flow; never paste secrets into chat.
2. Inspect existing repository, branch, history, licensing and secret exposure before making changes.
3. Add these documents under appropriate existing directories without replacing prior work blindly.
4. Use small descriptive commits for data audit, labeling guide, baseline, evaluation and report changes; record commit IDs in experiment logs.
5. Push only to the user-approved repository/branch. Do not upload restricted photos or private inspection records. Review permissions before public release.

## Pending user input
Exact approved title; presentation language and date; whether a live demo is expected; student/supervisor details; original Hugging Face URL; GitHub access; university handbook and page-count/citation rules; available hardware; qualified assessor access.
''')
save_text('docs/WORK_LOG.md','''# Work log

## Session 1 — proposal defence preparation
- Read the supplied dataset comparison image and teacher-message screenshot.
- Converted and read both example Word documents; identified unrelated GNN sample content.
- Initially saw 404; after user update, cloned public repository at 3482f30 and reviewed research documents and audit scripts. Prior audit reports 13,945 VehiDE images and 36,081 regions; 36-image pilot labels remain open.
- Researched candidate datasets; separated images from annotations, documented original CarDD restrictions, large-source access limits and merged-source overlap.
- Prepared proposal-stage slides, speech, proposal, page plan, inventory and a planned pilot/evaluation protocol.
- Did NOT download additional data, recruit experts, complete expert labels, train a model or run model evaluation. Publication status is recorded separately after generation.
- Next decision: confirm approved title/language/deadline and extend existing rights, dedup and pilot work. Then audit the exact HF dataset and run a licensed pilot before scaling.
''')
# Reopen final Office files and validate structural properties.
check=Presentation(OUT/'vehicle_damage_proposal_defence.pptx');assert len(check.slides)==11
assert sum(s[3] for s in slides)==300
assert all(len(s.notes_slide.notes_text_frame.text)>50 for s in check.slides)
assert len(Document(OUT/'docs/one_page_project_proposal.docx').paragraphs)>10
for sl in check.slides:
 for sh in sl.shapes:
  assert sh.left>=0 and sh.top>=0 and sh.left+sh.width<=check.slide_width+10000 and sh.top+sh.height<=check.slide_height+10000
with zipfile.ZipFile(ROOT/'vehicle_damage_defence_pack_final.zip','x',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(OUT.rglob('*')):
  if p.is_file():z.write(p,Path('defence-pack')/p.relative_to(OUT))
print(json.dumps({'slides':len(check.slides),'timed_slides':8,'allocated_seconds':300,'spoken_words':sum(len(s[4].split()) for s in slides),'files':len([p for p in OUT.rglob('*') if p.is_file()]),'output':str(OUT)},indent=2))
