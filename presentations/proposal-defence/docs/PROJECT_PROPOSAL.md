# One-page project proposal — provisional

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
