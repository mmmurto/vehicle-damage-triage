# Start here — urgent proposal defence

## Use these files, not the earlier versions

1. **PRINT_Proposal.pdf** — eight-page printable proposal. Follows the section order of the supplied Chinese opening-report example. Includes both workflow diagrams and references.
2. **Proposal_Editable.docx** — editable version of the same proposal content. **Fill in name, student number, university/programme, supervisor/date and confirm the working title before submission.** The supplied PDF currently also has identity blanks. If Word is edited, export a new PDF and check it before printing.
3. **Presentation_Under_5_Minutes_v4.pptx** — seven main slides + two question-only detailed-workflow backups. Embedded speech targets 4:15 (519 words), not a full five minutes. Rehearse at your own pace; the time is not guaranteed.
4. **READ_Defence_Guide_and_Script.docx** — plain-English explanation, dataset numbers, 30 question/answer pairs, matching talk and tonight/tomorrow checklist. This is for studying, not the proposal to hand in.
5. **Workflow_Diagrams.pdf** — two full-page diagrams. They are also included in the proposal; extra printing is optional, not established as required.

Editable SVG and high-resolution PNG diagrams are supplied for future changes. `verification.json` records the structural checks.

## What the attachments establish

The two new JPEGs are visual workflow examples, not official proposal forms. Their clinical-trial counts, drugs and process claims are not relevant and were not copied. The earlier Chinese opening report provides the section structure: background/significance, related work, main content/problems, methods/implementation, schedule and references. The supplied task sheet is a different document and is not silently presented as completed here.

The friend's Azerbaijani message reports that the panel stops talks after five minutes and focuses on the printed proposal. This is practical peer advice, not an independently verified university policy. The actual teacher's instructions take priority. No official title, identity, university form, signed approval or calendar deadline has been invented.

## Main workflow logic

Research: rights → file audit/dedup/groups → pilot and independent review → grouped train/validation/test → model comparison → validation settings frozen → final testing/error review.

One-car system: photos → usability → damage findings → clear serious hazard? → enough views and no unresolved concern? → only cosmetic/no visible damage? → output category, reason and next step. Clear hazards take priority over missing views. Unusable photos route to inspection/retake, not low concern.

## Accuracy of progress claims

The previous project audit at `3482f30` reports 13,945 VehiDE files and 36,081 regions in seven released classes. These were reviewed, not re-audited here. A 36-image pilot sample exists with expert labels open. No trained-model results, completed expert agreement, final deduplicated image/car count or linked functional roadworthiness outcome set is claimed. The new acquisition target is >20,000 useful real unique photos; 50,000+ is conditional, not collected.

## Reference check

CarDD original count/license, the ResNet paper, Guo et al. calibration paper and selective-classification paper were checked against original pages. VehiDE author names and the final volume/year were clarified: online June 2024; journal volume 9(1), 2025, pp. 24–43. The prior bibliography's 2024 entry was incomplete; this proposal uses the final issue citation. Sources:
- https://cardd-ustc.github.io/
- https://cardd-ustc.github.io/docs/CarDD_license.pdf
- https://cvis.hcmute.edu.vn/Publications/Details/257
- https://www.tandfonline.com/doi/full/10.1080/24751839.2024.2367387
- https://openaccess.thecvf.com/content_cvpr_2016/html/He_Deep_Residual_Learning_CVPR_2016_paper.html
- https://proceedings.mlr.press/v70/guo17a.html
- https://proceedings.neurips.cc/paper_files/paper/2017/hash/4a8423d5e91fda00bb7e46540e2b0cf1-Abstract.html

## Checks and remaining visual checks

The proposal PDF was generated directly from shared content, reopened, verified as eight pages and rendered for visual inspection. Both diagram PNGs were inspected; their PDF versions preserve vector artwork. Word and PowerPoint files were reopened and structurally checked; slide text sizes were adjusted using font metrics. Exact Word pagination and actual PowerPoint rendering were not verified in Office. Open the deck on the presentation computer before the defence.

Rebuild from the repository root with temporary Python dependencies:

```bash
uv run --with python-docx --with python-pptx --with reportlab --with pillow --with pymupdf --with svglib python scripts/build_tomorrow_defence.py
```

Generation refuses existing Word/PPTX destinations. Use a new output directory for a fresh run; do not overwrite earlier deliverables accidentally. Windows Arial font files are currently used; change the font paths for another operating system.
