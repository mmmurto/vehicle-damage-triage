# Project Proposal (one page)

**Working title:** Vehicle Damage Assessment from Images for Driveability Triage

**Project name:** VehiTriage *(placeholder — confirm or replace)*

**Candidate:** [name] · **Supervisor:** [name] · **Programme:** BSc [...] · **Date:** [date]

## Problem

After a collision, the first decision a driver, insurer, recovery operator or rental clerk
faces is not "how much will the repair cost" but "may this vehicle be moved under its own
power". Photographs are the cheapest evidence available at that moment, and they are now
routinely collected by phone. Existing car-damage datasets and models answer a different
question: they localise and classify cosmetic damage (dent, scratch, crack, glass shatter,
flat tyre, broken lamp) for insurance estimating. They do not decide whether a visible
condition is a reason not to drive, and they cannot see steering, braking or engine
function at all.

## Aim

Determine how reliably a computer-vision model can distinguish *visible cosmetic damage*
from *visible conditions that warrant taking a vehicle out of service*, and how reliably it
can recognise when a case must be escalated to a hands-on inspection.

## Research questions

- **RQ1** How well can an image model separate the three triage categories from visible
  evidence alone, and how often is a case that an expert judges unsafe assigned
  "low visible concern"?
- **RQ2** Does combining several photographs of the same vehicle, with an explicit coverage
  and evidence check, reduce that hazard-miss rate compared with a single-image baseline?
- **RQ3** Which evidence types drive errors — glass damage, tyre and wheel damage, suspected
  fluid leakage, poor lighting, limited viewing angles — and what does that imply for the
  achievable reliability of photographic triage?

## Method

1. **Data.** Verify and combine public damage-image sources, target ~10,000 usable images,
   remove duplicates and near-duplicates, group by vehicle/incident where identity is
   available, and hold out an independent source for a generalisation test.
2. **Labels.** Define a three-class triage rubric in which the visible observation, the
   recommended action and any verified inspection outcome are stored as separate fields.
   Run a pilot, measure inter-annotator agreement, then scale. Actual roadworthiness is
   **not** measurable from these sources; the reference standard is expert visual triage,
   and this limitation is carried into the research question and the conclusions.
3. **Models.** A reproducible single-image baseline (transfer-learned CNN or ViT, damage-type
   heads plus a triage head) and one practical improvement: a multi-view model that pools
   per-photo evidence, adds a coverage/completeness feature and can abstain to
   "inspection required".
4. **Evaluation.** Thresholds fixed on validation data, evaluated once on a held-out test
   set. Primary metric: the **hazard-miss rate** — the share of expert-labelled unsafe cases
   assigned "low visible concern" — reported with counts, confidence intervals and a named
   reference standard. Secondary: per-class precision/recall, confusion matrix, inspection
   routing fraction, and the routing-versus-miss trade-off curve, so the model cannot look
   good by deferring everything. Calibration and error analysis by evidence type.

## Deliverables

A documented dataset and labeling schema; a reproducible training/evaluation pipeline; an
error analysis of unsafe-case misses; and a written discussion of what photographic triage
can and cannot establish. The system outputs the category, the visible reason and the next
step, with a short spoken summary for each result.

## Scope limits

No claim of roadworthiness. No inference of steering, brake or engine function from
appearance. Single vehicle class (passenger cars), daylight-to-ordinary-lighting photographs,
no thermal or depth sensors, no diagnostic data.
