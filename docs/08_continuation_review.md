# Continuation review — proposal defence preparation

Reviewed base: `3482f30` (prior Session 3). This review does not replace the original audit or claim it was reproduced.

## Confirmed repository contents
- Research scaffold, proposal, 40/70-page outline, inventory, labeling guide and sourcing plan.
- Prior VehiDE audit reports **13,945 image files, 36,081 regions, seven released classes**. Counts are recorded prior results; the raw archive was not available inside this checkout and was not re-audited during this session.
- Existing DrBimmer pilot: **36 sampled images**, manifest/contact sheet; expert action labels and agreement results remain open.
- No training or inference implementation for a learned triage model is present in the reviewed tracked files. Existing scripts support dataset verification/audit and pilot sampling.

## Qualifications to earlier claims
1. **Timestamp overlap is not verified vehicle leakage.** The earlier 79.8% figure is 1,707 / 2,139 parsed validation filenames sharing a minute-level timestamp group with training. It is not a count or rate of confirmed same-vehicle overlap. Minute boundaries can split one incident, and multiple vehicles/cameras can share a timestamp. Validate candidate groups using photographs/metadata and measure false merges/splits before treating them as incident IDs. No demonstrated model-performance inflation can be claimed without a controlled experiment.
2. **Annotated damage does not establish absence of intact vehicles or safe controls.** The prior audit establishes that every annotation entry contains at least one region. It does not inspect all image content or certify any vehicle's condition. An absent tire/wheel/fluid class does not mean the imagery contains none of those findings.
3. **Ungroupable files are not automatically safe for training.** They can still overlap a test vehicle; quarantine or cross-source near-duplicate/incident review is needed before including them. A different website is not automatically an independent source.
4. **Low concern is not an undamaged label.** Cosmetic damage can belong to low visible concern if coverage is adequate; an undamaged-looking cropped photo can require inspection. Do not map source damage classes or severity directly into triage classes.
5. **Licenses need upstream provenance.** Uploader MIT/Apache/CC tags do not prove rights to third-party photographs or supersede CarDD's permission and redistribution restrictions. Do not republish photos or contact sheets merely because the repository is public.
6. **Fluid identity is generally unresolved from color/position.** A photograph of a wet patch does not verify coolant, fuel, brake fluid or harmless condensate. Use visual appearance/uncertainty fields; uncertain liquid normally requires inspection, not a hidden-function claim.
7. **Glass measurements and action mapping need revision/review.** Generic assumed plate/wheel sizes and perspective do not establish millimeter accuracy. Add `not_assessable` for driver visibility; do not equate a missing side pane with proven driver-view obstruction. Any legal calibration anchor must be checked against its exact current jurisdictional source, separately from the visual policy.
8. **Agreement must be measured before adjudication.** Consensus labels cannot be used to inflate independent-review agreement. Interpret kappa with raw agreement, class counts and disagreements; a single kappa cutoff is not sufficient evidence of label validity.
9. **Page and collection targets updated by the user.** Plan for a 70-page report (counting rules pending), more than 20,000 usable real unique images, and 50,000+ as a conditional stretch goal. Earlier 5k–10k plans are historical, not the current target. Do not fabricate an expected unique yield before deduplication.

## New deliverables
`presentations/proposal-defence/` contains the English provisional five-minute presentation, embedded notes, speech/Q&A, one-page proposal, 70/40 page budgets, supplemental dataset inventory, sources, an extension protocol for the existing pilot, and evaluation plan. Existing files were preserved rather than silently replaced. The existing 36-image pilot remains the starting point; 60 cases is a proposed extension, not completed work.

## Immediate next actions
Confirm approved title, presenter details, language, date and whether a live demo is required. Reproduce the archive audit from the locally stored dataset when its location is supplied. Validate dedup/grouping, audit licenses, and add serious-hazard examples before completing expert labeling. Numerical model targets must be locked after pilot review and before final testing.
