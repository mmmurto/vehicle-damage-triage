# Labeling Guide (v1.0 — draft for pilot)

Purpose: produce labels that keep three things **separate**, because they answer different
questions and must never be collapsed:

| Record | Question answered | Who can supply it | Used for |
|---|---|---|---|
| **A. Observation** | What is visibly there? | Any trained annotator, from the image | inputs, error analysis, evidence explanations |
| **B. Action (triage)** | What should happen next, given only these photos? | Trained annotator applying this rubric | the target label |
| **C. Outcome** | What was actually true after hands-on inspection? | A qualified inspector / linked record | external validation — **usually empty in this project** |

If C is empty, the thesis evaluates B. State that in the research question and in the
conclusions. Never fill C from the image.

---

## 1. Scope

In scope: passenger cars (M1), ordinary photographs, daylight or ordinary artificial light.
Out of scope: commercial vehicles, motorcycles, close-up microscopy of paint, thermal/depth
imagery, video, OBD or diagnostic data, and any judgement of whether the vehicle actually
*is* roadworthy.

Hard rules (apply to every label, every annotator):

1. **Never infer function from appearance.** Not "the steering looks fine", not "the engine
   seems undamaged", not "the brakes are probably OK", not "the airbags did not deploy so it
   is fine". Functionality is unobservable in a photograph.
2. **Never upgrade to "low concern" on the basis of absence of evidence.** Missing views are
   *unknown*, not *undamaged*.
3. **Absence of visible hazard is not evidence of safety.** The category name is
   "low **visible** concern" precisely because it is bounded by what the photos show.
4. Only visible findings may be cited as a reason. "Probably a bent subframe" is not a
   finding; "the front-left wheel sits visibly inboard of the arch line and the tyre is
   deflated" is.

---

## 2. Annotation unit

Two levels, both recorded:

- **Image level**: one photograph, one set of observations.
- **Case level**: one vehicle in one incident, consisting of 1–n photographs. The triage
  label (B) is assigned at **case level**; the observation record (A) is per image.

Where vehicle identity cannot be established (true for every public dataset checked so far),
a case = a manually grouped set of images judged to show the same vehicle (same plate,
same damage pattern, same background sequence). Grouping confidence is recorded:
`confirmed` / `probable` / `image_only`. Any evaluation run on `image_only` cases is reported
as image-level.

---

## 3. Record A — observation fields

```
schema_version            1.0
image_id                  <source>/<path>
case_id                   <assigned or NULL>
views_present             [front, front_left, left, rear_left, rear, rear_right,
                           right, front_right, wheel_closeup, interior, underbody]
lighting                  good | adequate | poor | night | backlit | glare
sharpness                 sharp | soft | motion_blur | out_of_focus
occlusion                 none | partial_panel | heavy
resolution_ok             true | false        # false if detail < ~1 cm/pixel at the damage
damage_instances[]        {type, part, extent, severity_ord, confidence}
damage_types              [scratch, dent, crack, paint_chip, panel_misalignment,
                           glass_damage, lamp_damage, tyre_damage, wheel_damage,
                           fluid_leak, structural_deformation, fire, none_visible]
glass[]                   see §4
tyre_wheel[]              see §5
fluid[]                   see §6
other_hazard_flags[]      [airbag_deployed, door_cannot_latch, hood_unlatched,
                           exhaust_detached, underbody_contact, load_shift,
                           missing_component, registration_plate_absent]
annotator_id, timestamp, seconds_spent, confidence (1-3), notes
```

Severity ordinal for body damage: `1 cosmetic` (paint/clear-coat only, no deformation),
`2 minor` (shallow dent/scratch, panel intact, no gap change), `3 moderate` (clear
deformation, panel gap or fit affected), `4 severe` (panel torn/pierced, structure visibly
deformed, component displaced).

Formal definitions (use these words, not intuition):
- **scratch**: linear loss of paint/clear-coat; no depth change to the panel surface.
- **dent**: localised plastic/permanent deformation without material removal.
- **crack**: fracture line in a rigid body panel or lamp lens.
- **panel misalignment**: an observable change in a panel gap or flushness relative to the
  opposite side or to the manufacturer's line.
- **structural deformation**: visible buckling, creasing or displacement of a load-bearing
  member or aperture (pillar, sill, apron, roof rail, door aperture distortion).

---

## 4. Glass rubric (location × severity × driver visibility)

A single label "broken glass" is not usable for triage. Record all four attributes.

**Location** (one per instance):
`windshield_zoneA` (swept area, 290 mm wide, centred on the steering wheel) ·
`windshield_swept_other` · `windshield_unswept` · `side_front_driver` ·
`side_front_passenger` · `side_rear` · `rear_window` · `roof_glass` · `mirror_glass` ·
`lamp_lens` (handled under lamp, not glass).

**Damage form**: `chip` · `bullseye` · `star_break` · `crack_line` · `crazing` ·
`laminated_delamination` · `tempered_fragmented` (granulated, held by tint film or fallen
out) · `missing_pane`.

**Measured size**: longest visible dimension in mm, estimated from a reference (plate width
520 mm, wheel diameter ≈ 600–700 mm, wiper blade length ≈ 500–650 mm). Record
`size_confidence`: `measured_reference` / `estimated` / `unmeasurable`.

**Driver-view impact**: `none` · `partial` (view intruded but road view usable) ·
`obstructed` (driver cannot see a required field of view) · `not_applicable` (not a
driver-side pane).

**Calibration anchor.** The UK MOT inspection manual, section 3.2, fails a windscreen for
damage in Zone A exceeding 10 mm in diameter, or damage elsewhere in the swept area
exceeding 40 mm, and only where the driver's view of the road is significantly affected
(GOV.UK, *MOT inspection manual: cars and passenger vehicles — 3. Visibility*). This is used
here as a **documented, cited threshold for the rubric**, not as a legal claim about the
annotated vehicle's jurisdiction. Record the source of the threshold in the thesis and note
that other jurisdictions differ.

Mapping to triage:
| Glass finding | Triage |
|---|---|
| chip/star/crack in `windshield_zoneA` > 10 mm, or any swept-area damage > 40 mm | **inspection required** (visibility-critical; not automatically "do not drive") |
| `tempered_fragmented` or `missing_pane` on a driver-side or windscreen pane | **do not drive** (driver view compromised; the pane also contributes to occupant retention) |
| crack line extending across the driver's sight line, or glass displaced into the cabin | **do not drive** |
| damage outside the swept area, or a small chip with no crack and no view intrusion | may support **low visible concern** if all other coverage conditions hold |
| size unmeasurable or the pane is not visible in any photo | **inspection required** |

---

## 5. Tyre and wheel rubric

Record per corner (`front_left`, `front_right`, `rear_left`, `rear_right`,
`spare_or_unknown`) and per attribute:

- **visible**: `yes_clear` / `yes_partial` / `no`
- **inflation**: `normal` / `visibly_soft` / `flat_on_rim` / `unknown`
- **tread damage**: `none_visible` / `worn` / `cord_or_wire_exposed` / `tread_separation` /
  `shredded` / `sidewall_bulge` / `sidewall_cut`
- **wheel damage**: `none_visible` / `kerb_rash` / `bent_lip` / `cracked` / `missing_spokes`
- **position**: `normal` / `visibly_displaced` (out of the arch line, tilted camber, or
  clearly not coaxial) / `contact_with_body` / `unseated_from_rim`
- **fasteners**: `all_present` / `missing_visible` / `unknown`
- **arch clearance**: `ok` / `tyre_contacting_liner_or_body` / `unknown`

Mapping to triage:
| Finding | Triage |
|---|---|
| `shredded`, `tread_separation`, `cord_or_wire_exposed` with visible deflation | **do not drive** |
| `flat_on_rim` / `unseated_from_rim` / `missing_visible` fasteners | **do not drive** |
| wheel `visibly_displaced`, `contact_with_body`, or tyre contacting the liner | **do not drive** |
| `visibly_soft` tyre without other findings | **inspection required** |
| wheel not visible in any photograph, or only partially visible with damage nearby | **inspection required** |

---

## 6. Fluid rubric

- **substance**: `clear_water` / `green_or_orange_coolant` / `brown_black_oil` /
  `red_transmission` / `amber_brake_or_ps` / `fuel_smell_reported` / `unknown_colour`
- **pattern**: `dry_stain` / `fresh_wet_pool` / `active_drip` / `spray_or_mist` /
  `trail_behind_vehicle`
- **location**: `under_engine` / `under_transmission` / `under_fuel_tank` / `at_wheel` /
  `at_brake_caliper` / `at_radiator` / `unknown`
- **quantity**: `drops` / `palm_sized` / `larger_than_palm` / `unbounded`
- **attribution**: `from_this_vehicle` / `pre_existing_or_other_vehicle` / `unclear`

Mapping to triage:
| Finding | Triage |
|---|---|
| `active_drip` or `spray_or_mist` of any non-water substance, especially fuel or brake fluid | **do not drive** |
| `fresh_wet_pool` larger than a palm attributable to this vehicle | **do not drive** |
| `fresh_wet_pool` small or attribution unclear | **inspection required** |
| `dry_stain` only, with no other finding | may support **low visible concern** |

Water condensate from the air-conditioning is the common false positive: record
`likely_ac_condensate` only when the pool is clear, under the cabin area, and the ambient
conditions are consistent; if in doubt, escalate.

---

## 7. Decision rule (apply in order)

```
STEP 1  Is any "do not drive" finding from §4-§6 present and clearly visible?
        -> DO NOT DRIVE, citing the specific finding(s).
STEP 2  Does the image set meet the coverage conditions for a limited assessment?
        Required: >= 4 views (front, rear, left, right), all four wheels visible,
        adequate lighting, sharpness adequate, resolution adequate at the damage,
        no safety-critical area obscured.
        -> If NOT met: INSPECTION REQUIRED (state which condition failed).
STEP 3  Is any safety-critical question unresolved despite adequate coverage?
        e.g. wet patch of unclear origin, damage adjacent to a wheel with the wheel
        itself not visible, glass damage whose size cannot be measured, visible
        deformation near a suspension or steering mounting point without visible
        displacement.
        -> If yes: INSPECTION REQUIRED (name the unresolved question).
STEP 4  Otherwise: LOW VISIBLE CONCERN, only if the visible damage is cosmetic
        (severity 1-2 per §3) and every safety-critical area has been seen.
        Output must include the disclaimer sentence.
```

Tie-break rules: when two annotators disagree between adjacent categories, prefer the more
conservative category (escalate upward). When a finding is visible but its severity is
ambiguous, escalate. Never escalate to "do not drive" on a guess.

---

## 8. Output templates (system output, not dataset labels)

**Low visible concern**
> "Minor cosmetic damage is visible: [e.g. a shallow scratch on the rear-left door]. The
> submitted views show no tyre, wheel, glass or fluid findings. Roadworthiness was not
> verified."

**Do not drive**
> "Do not drive. Visible evidence: [e.g. the front-left tyre is shredded and the wheel sits
> visibly out of line with the arch]. This requires professional assessment before the
> vehicle is moved under its own power."

**Inspection required**
> "Inspection required. The photographs do not show [e.g. the right-side wheels / the source
> of the wet patch under the engine], and [finding] cannot be resolved from the images.
> Arrange a hands-on inspection before driving."

**Spoken summary** (≤ 2 sentences, TTS): *"[Category]. [Visible reason]. [Next step]."*
Example: "Do not drive. The front-left tyre is shredded and the wheel is visibly displaced.
Have the vehicle assessed by a professional before driving it."

---

## 9. Procedure, agreement and quality control

1. **Pilot**: 36 images (already sampled, `pilot/pilot_sample_manifest.csv`), 2 annotators,
   independent, no discussion; then adjudication meeting.
2. Report **Cohen's κ** (2 annotators) or **Krippendorff's α** (3+) for the 3-class label,
   plus per-class agreement; report raw percentage agreement too, and the confusion between
   adjacent categories. Target before scaling: κ ≥ 0.6 (substantial). If κ < 0.6, fix the
   rubric, not the data.
3. Adjudication: disagreements are resolved by a third reviewer with mechanical/assessment
   experience, and every adjudicated case is logged with its reason in
   `pilot/adjudications.csv`.
4. **Scale-up**: fixed batch size per session (≤ 60 images), forced break, randomised order,
   ≥ 10% of items re-shown later for intra-annotator consistency.
5. Record `seconds_spent`; a sudden drop is a fatigue signal.
6. All labels carry `confidence` 1–3. Confidence 1 items get a second opinion by default.
7. Never label from the assigned class name or filename. The labeling tool must hide the
   source folder. (The pilot manifest deliberately keeps the source class in a separate
   column to make this checkable — do not sort or filter by it while labeling.)

---

## 10. Borderline cases and how to log them

| Situation | Action |
|---|---|
| Damage is visible but the photo is too low-resolution to grade | label `resolution_ok = false`, escalate to inspection, note the reason |
| Same vehicle appears twice in the batch | same `case_id`; label once at case level, note duplicates for dedup |
| Plate masked by dealer overlay | record as `occlusion = partial_panel`; the mask itself is not damage |
| Vehicle on a recovery truck or in a salvage yard | record `context`; such images often correlate with genuine undriveability — useful for error analysis but not evidence itself |
| Pre-existing rust or unrepaired old damage | record `damage_age = old`; do not let it drive the triage label alone |
| Snow, rain, dirt, or wet ground that mimics fluid | record, do not label as fluid without pattern evidence |
| Aftermarket add-ons (body kits, spoilers) | not damage |

---

## 11. What changes after the pilot

This is v1.0. Expected revisions: the coverage list in STEP 2 (it may be too strict or too
loose in practice), the fluid attribution rule (hardest in practice), and the glass size
measurement method (needs a reference object in frame). Version every change, date it, and
report the rubric version used for each experiment in the thesis.
