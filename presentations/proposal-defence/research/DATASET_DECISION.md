# Data acquisition decision — provisional

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
