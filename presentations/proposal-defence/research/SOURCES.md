# Source evidence ledger

Verification session: 2026-11-16 workspace date. This is a documentation audit, NOT a downloaded-image audit. Freeze actual access timestamps and dataset revisions before use.

## S1 — CarDD official project
URL: https://cardd-ustc.github.io/
Observed: 4,000 images; over 9,000 instances; six visual damage categories.

## S2 — CarDD original license
URL: https://cardd-ustc.github.io/docs/CarDD_license.pdf
Observed: Prior consent for research; no third-party redistribution without authorization; cite original paper.

## S3 — VehiDE research team
URL: https://cvis.hcmute.edu.vn/Research/Details/4
Observed: 13,945 images; over 32,000 instances; eight categories reported.

## S4 — VehiDE Kaggle distribution
URL: https://www.kaggle.com/datasets/hendrichscullen/vehide-dataset-automatic-vehicle-damage-detection
Observed: Count corroborated; exact upstream rights and local archive counts pending.

## S5 — Roboflow car_damages_19k v1
URL: https://universe.roboflow.com/tarpit-patel-uyibg/car_damages_19k/dataset/1
Observed: Search-index listing: 19,100 total, no augmentation; direct fetch met security verification. License and provenance pending.

## S6 — AI-Hub vehicle damage dataset 581
URL: https://aihub.or.kr/aihubdata/data/view.do?dataSetSn=581
Observed: Reports 632,694 images and 125,007 estimate records; application restricted to Korean nationals; version 1.1 dated 2023-02-01.

## S7 — JijoJS/car-damage-new1
URL: https://huggingface.co/datasets/JijoJS/car-damage-new1
Observed: Card: 2,427 images (2,187/120/120); dent/scratch; COCO; CC BY 4.0; no augmentation reported.

## S8 — DrBimmer/comprehensive-car-damage
URL: https://huggingface.co/datasets/DrBimmer/comprehensive-car-damage
Observed: Card/viewer: 2,300 rows; front/rear normal, crushed, breakage. Rights pending; normal does not mean roadworthy.

## S9 — AutoDamageIQ merged dataset
URL: https://huggingface.co/datasets/tugberkkalay/autodamageiq-vehicle-damage-dataset
Observed: 13,089 training + 2,094 validation images; CarDD + VehiDE + GPT-4o-labeled HITL. Not an independent source.

## S10 — CompCars official project
URL: https://mmlab.ie.cuhk.edu.hk/datasets/comp_cars/index.html
Observed: 136,726 whole-car web images; 27,618 part images; 50,000 surveillance images. Auxiliary recognition, not verified safe controls.

## S11 — CompCars release agreement
URL: http://mmlab.ie.cuhk.edu.hk/datasets/comp_cars/agreement.pdf
Observed: Non-commercial research by signed agreement; restrictions on redistribution and publication.

## S12 — xanoutas/vehicle-damage-detection
URL: https://huggingface.co/datasets/xanoutas/vehicle-damage-detection
Observed: Viewer: 495 rows, 15 classes; provenance/license pending.

## R1 — Prior VehiDE archive audit at 3482f30
URL: https://github.com/mmmurto/vehicle-damage-triage/blob/3482f30/docs/07_vehide_audit.md
Observed: Prior project audit: 13,945 files, 36,081 regions, seven released classes; reviewed, not re-run here. Timestamp overlap is not verified vehicle leakage.

## R2 — Existing 36-image pilot at 3482f30
URL: https://github.com/mmmurto/vehicle-damage-triage/blob/3482f30/pilot/04_pilot_report.md
Observed: 36-image sample and contact sheet exist; expert labels and agreement remain open.

## References ready to verify/style
- Wang, X., Li, W., and Wu, Z. (2023). CarDD: A New Dataset for Vision-Based Car Damage Detection. IEEE Transactions on Intelligent Transportation Systems, 24(7), 7202–7214. DOI: 10.1109/TITS.2023.3258480.
- VehiDE Dataset: New dataset for Automatic vehicle damage detection in Car insurance (2023). DOI: 10.1109/KSE59128.2023.10299490. Author list must be retrieved before final bibliography.

No web source has been verified to provide linked, functional roadworthiness outcomes. An insurance expert annotating damage is not the same as an inspection confirming driveability.
