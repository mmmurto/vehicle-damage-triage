# Photo sources and licensing

These are real licensed presentation illustrations, NOT images acquired from the audited VehiDE/DrBimmer collection. They add zero images to the training or test dataset inventory. Captions are visible-evidence explanations, not expert ground-truth inspection outcomes.

## m4_roof_down.jpg
- Photographer: Calreyn88
- Source: https://commons.wikimedia.org/wiki/File:2022_BMW_M4_Competition_Convertible.jpg
- License: CC BY-SA 4.0 — https://creativecommons.org/licenses/by-sa/4.0/
- Changes: Resized and JPEG re-encoded; aspect ratio retained. Any detail crop explicitly labeled.

## suv_roof_crush.jpg
- Photographer: Ryanandlenny
- Source: https://commons.wikimedia.org/wiki/File:CR-V-Accident.jpg
- License: CC BY 3.0 — https://creativecommons.org/licenses/by/3.0/
- Changes: Resized and JPEG re-encoded; aspect ratio retained. Any detail crop explicitly labeled.

## flat_tire.jpg
- Photographer: Tiia Monto
- Source: https://commons.wikimedia.org/wiki/File:Broken_tire.jpg
- License: CC BY-SA 4.0 — https://creativecommons.org/licenses/by-sa/4.0/
- Changes: Resized and JPEG re-encoded; aspect ratio retained. Any detail crop explicitly labeled.

## front_damage.jpg
- Photographer: Uiliam Nörnberg
- Source: https://www.pexels.com/photo/close-up-of-the-side-of-a-car-with-scratches-on-the-front-fender-24960483/
- License: Pexels License — https://www.pexels.com/license/
- Changes: Resized and JPEG re-encoded; aspect ratio retained. Any detail crop explicitly labeled.

## surface_detail.jpg
- Photographer: Uiliam Nörnberg
- Source: https://www.pexels.com/photo/close-up-of-the-side-of-a-car-with-scratches-on-the-front-fender-24960483/
- License: Pexels License — https://www.pexels.com/license/
- Changes: Detail crop of lower front bumper scrapes; remainder of damaged vehicle deliberately not shown. Derived from front_damage.jpg source, not a separate example.

## Reuse and safeguards
Photographs retain their individual licenses; no photographer or manufacturer endorsement is implied. CC BY-SA image derivatives remain available under CC BY-SA 4.0; this is not a blanket relicensing of other components. Presentation use does not establish machine-learning rights for a future dataset. The left surface-detail and right front-damage panels share one Pexels source and are not independent examples. The surface detail is not assigned a whole-car low-concern category: the full source contains other front-area damage.

## Planned design-aware evaluation
A roof-down convertible must not automatically be labeled roof-damaged. Convertible is not a synonym for undamaged: include damaged convertibles and undamaged fixed-roof cars/SUVs, multiple backgrounds and roof-up/down states. Record design/state separately from damage. Use disjoint vehicles for learning and testing; inspect source shortcuts and roof false alarms/misses. These two comparison pictures do not establish a trained feature, novelty or an error rate.
