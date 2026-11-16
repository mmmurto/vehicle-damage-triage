# Five-minute speaker script

8 timed slides, 300 seconds total. Three source appendices are backup only. English is provisional pending language confirmation. Replace working title and presenter details after confirmation. Rehearse; timing varies with speaking pace. This is a proposal defence, not a live trained-system demo.

## Slide 1 — Vehicle Damage Assessment from Images (35s)

Good morning. My proposed dissertation investigates vehicle damage assessment from photographs for preliminary driveability triage. The aim is not to certify a vehicle as safe. It is to identify visible evidence, recommend a next step, and recognize when the images are insufficient. This is a proposal-stage presentation: the dataset audit, training and evaluation still need to be completed. The official dissertation title will be confirmed with my supervisor.

## Slide 2 — The problem: appearance is not function (35s)

A damaged vehicle may have a superficial paint scratch, an obvious tire hazard, or hidden damage that a photograph cannot resolve. A simple damaged-versus-undamaged classifier cannot distinguish these situations reliably. Even an apparently normal car may have mechanical faults. My research therefore separates visual observations from recommended actions and from verified inspection outcomes. The key motivation is to avoid false reassurance while still providing useful preliminary guidance.

## Slide 3 — Three outputs, each with evidence (45s)

The system has three outputs. Low visible concern means the submitted views support only a limited cosmetic assessment; the output explicitly says roadworthiness was not verified. Do not drive is reserved for clear serious visible evidence, such as a shredded tire or displaced wheel. Inspection required covers missing context, unclear photographs or unresolved concerns such as possible leakage. Glass must be assessed by location, extent and effect on visibility, not just a broken-glass label. Every output explains the visible reason and next step.

## Slide 4 — Data: substantial candidates, not secured totals (45s)

The collection target is more than twenty thousand usable real images, with fifty thousand a stretch goal if access and useful coverage allow. Our prior VehiDE audit reports thirteen thousand nine hundred forty-five files and thirty-six thousand eighty-one regions across seven released classes. I reviewed, but did not repeat, that audit. CarDD and a nineteen-thousand-image Roboflow candidate could add coverage, subject to rights and overlap checks. These numbers cannot simply be added because sources may overlap. More importantly, no reviewed source has yet been verified to contain linked functional roadworthiness outcomes. Without those outcomes, the research will evaluate expert visual triage, not actual driveability.

## Slide 5 — Pilot first, then scale (40s)

The repository already contains a thirty-six-image pilot sample with labels still open. I propose extending it toward sixty cases with hazard and borderline examples. Two reviewers will record observations and actions independently, with qualified automotive adjudication. We will study disagreement and missing viewpoints before expanding the guide. Duplicate and near-duplicate images must be removed or grouped across sources. Images from the same vehicle or incident must stay in the same split where identity is available. Where grouping is unknown, that limitation will be reported rather than assuming independence.

## Slide 6 — Build a baseline, then test one improvement (35s)

The baseline will be a reproducible transfer-learning image classifier. The practical improvement will identify visible damage and combine it with an explicit conservative action policy. If several photographs can be linked to one vehicle, I will test multi-view aggregation against the image-level baseline. The interface must send photographs to an image-capable component. It will return the category, evidence and next step, optionally read aloud. The current repository provides data-audit scripts and research documentation, not a trained triage model.

## Slide 7 — Evaluation: reduce false reassurance (40s)

The primary visual error is an expert do-not-drive case assigned low visible concern. I will report its count and rate using all expert do-not-drive reference cases as the denominator. If inspection-backed outcomes become available, a separate confirmed-unsafe error will be reported. Evaluation also includes per-class precision and recall, confusion matrices, uncertainty and inspection referral rate. Referring every case cannot count as useful success, so the trade-off must be shown. Thresholds are selected on validation data, with numerical targets fixed after the pilot and before final testing.

## Slide 8 — Plan and expected contribution (25s)

The next steps are to confirm the approved title and university requirements, extend the reviewed repository, and secure suitable data permissions. Then I will run the pilot, train the baseline and improvement, and evaluate on held-out data. The expected contribution is an auditable visual-triage system and an honest analysis of its limitations, documented in the planned seventy-page dissertation. No experimental results are claimed today. Thank you.

## Likely examiner questions

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
