# Evaluation plan v0.1

Baseline: transfer-learning image classifier (e.g. ResNet-18); exact implementation, dependency lock, seed, pretrained weights, transform and training budget recorded after repository audit. Compare a practical localization-plus-policy model; compare multi-view pooling only where legitimate grouping exists. Match data and compute budgets and pre-register comparisons. API assistance is not evidence of a trained damage model; audit what the existing implementation really does.

Labels: current intended reference is adjudicated expert visual triage. Do not call these actual driveability labels. If adequate independent inspection records become available, maintain a separate outcome endpoint and document timing and tests.

Primary visual error = count(reference visual do-not-drive AND prediction low visible concern) / count(reference visual do-not-drive). Always report numerator and denominator; undefined if denominator is zero. With inspection-backed outcomes, separately report confirmed-unsafe assigned low concern / all confirmed-unsafe. Also report serious references deferred to inspection vs directly detected so deferral cannot hide hazard-detection failures.

Report 3x3 confusion matrix, per-class precision/recall/F1 with support, overall referral fraction, referral fractions by reference class and source, and fraction of low-concern predictions with a serious reference. Include an all-inspection and simple baseline comparator. A system that defers every case has zero low-concern misses but no useful low-concern coverage; it is not automatically successful.

Plot serious-to-low-concern error versus referral rate and useful low-concern coverage over validation-selected policy thresholds. State the exact uncertainty score/coverage gate. Lock an operating point and numerical safety/usefulness criteria after the pilot, before final test access. Never tune on the test set. Treat inability to find a useful operating point as a valid result.

Use vehicle/incident-level bootstrap confidence intervals for grouped cases. If only independent image units can be established, report image-level intervals and dependence limitations. Include denominators, especially rare hazards; zero observed misses is not proof of zero risk. No fabricated rates or guarantees.

Predefined slices: lighting, blur, limited angles, front/rear/side glass, tires/wheels, suspected liquids, source and known vehicle groups. Review false low-concern cases and inspect explanation faithfulness against actual visible evidence. Run ablations for quality gates, policy rules, localization and multi-view when feasible. Maintain a blind final test and a separate independent-source test where rights and grouping permit.

Results table columns: experiment_id, git_commit, data_manifest_hash, guide_version, model/weights, seed, transforms, hyperparameters, hardware, threshold_selection, class_support, confusion_matrix, primary_numerator/denominator, referral_rate, confidence_intervals, runtime, failure_notes. All experiments remain NOT RUN.
