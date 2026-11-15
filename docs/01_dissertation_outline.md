# Dissertation Outline with Provisional Page Allocations

Two variants are given because the page limit is still unconfirmed. **All numbers are
provisional** and must be re-cut once `docs/05_open_questions.md` item 1 is answered.

Assumptions (state them in the methods chapter):
- ~300 words per full page of body text; a full-page figure or table counts as one page.
- Page counts include figures, tables, references and front matter; the title page is excluded.
- The 40-page variant **merges chapters 4 and 5** into one "Method" chapter; the 70-page
  variant keeps them separate.

---

## A. Chapter plan (both variants sum to their limit exactly)

| # | Chapter | 40 pp | 70 pp | What it must contain | Evidence artefacts |
|---|---|---|---|---|---|
| 0 | Title page, abstract, contents, abbreviations | 3 | 4 | Abstract ≤ 300 words: aim, data, method, headline result, limitation | — |
| 1 | Introduction | 3 | 4 | The photographic-triage problem; cosmetic damage ≠ driveability; aim; RQ1–RQ3; contributions; scope limits | Fig: three categories on real images |
| 2 | Background and literature review | 5 | 10 | (a) damage-detection datasets and models; (b) severity and repair-cost estimation; (c) glass and driver-visibility criteria; (d) tyre/wheel/fluid hazard evidence; (e) multi-view and set classification; (f) abstention, selective prediction, calibration; (g) limits of image evidence in safety-critical settings | Table: prior datasets vs this work; table: prior models and reported metrics; search-protocol figure (70 pp only) |
| 3 | Dataset construction and labeling methodology | 6 | 12 | Source verification (count, licence, permitted use); dedup + near-dup; vehicle/incident grouping; split rules incl. independent source; rubric rationale; pilot and agreement; class balance; synthetic vs independent images | Fig: dataset funnel (found → verified → usable → labelled); Table: per-source inventory; Table: class balance; Table: agreement (κ, per class); Fig: label distribution |
| 4 | System design | — | 8 | Task formalisation (3 classes + abstain); baseline architecture; damage-evidence heads; multi-view aggregation; coverage check; temperature scaling; output templates and spoken summary | Fig: architecture; Fig: inference flow with abstention; Table: hyperparameters |
| 4–5 | **Method (merged: design + protocol)** — 40 pp only | 5 | — | One chapter: architecture, thresholds, metrics, protocol, reproducibility | Fig: architecture (compact); Table: metric definitions; Table: pre-registered targets |
| 5 | Experimental setup and evaluation protocol | — | 5 | Metrics and why; hazard-miss definition and naming; routing fraction; bootstrap CIs; pre-registered targets; compute and reproducibility; ethics | Table: metric definitions; Table: pre-registered targets (filled before the test run) |
| 6 | Results | 6 | 8 | Headline table; confusion matrices; per-class P/R; hazard-miss count and rate; routing-vs-miss curve; single- vs multi-view; independent-source test | Main results table; 4–6 figures; every cell `[PLACEHOLDER]` until run |
| 7 | Discussion | 4 | 6 | What the numbers mean for triage; where and why it fails; label noise vs model error; "not visibly hazardous" ≠ "safe"; comparison with the literature | Fig: failure gallery |
| 8 | Limitations and threats to validity | 2 | 3 | No inspection-backed ground truth; provenance and licence risk; resolution; viewpoint bias; annotator expertise; single-market vehicle mix; no functional checks | Table: threat → direction of bias → mitigation |
| 9 | Conclusion and future work | 1 | 3 | Answer RQ1–RQ3 explicitly; contributions; what an inspection-linked follow-up would require | — |
| 10 | References | 2 | 3 | One consistent style; every dataset and model cited | — |
| 11 | Appendices | 3 | 4 | Full labeling guide; source verification log; hyperparameters; extra figures; ethics/consent statement; demo screenshots | — |
| | **Total** | **40** | **70** | | |

### What the 40-page cut removes
Chapter 2 is compressed to 5 pages (damage detection, severity estimation, abstention — drop
the repair-cost and pretraining subsections, keep them as citations). Chapter 4 and 5 merge
into one 5-page Method chapter. The independent-source experiment and the routing-vs-miss
curve move to the appendix. Chapter 6 becomes the headline table plus confusion matrices.
Chapter 7 drops the failure gallery to three examples.

### What the 70-page expansion adds
- **Chapter 2**: a documented search protocol (databases, query strings, inclusion criteria)
  with a PRISMA-style flow figure, +4 pages, and a dedicated subsection on abstention and
  selective prediction in safety-critical vision, +1 page.
- **Chapter 3**: per-source audit (+3 pages: duplicate rates, label-noise checks at full
  resolution, resolution histograms, per-source hazard coverage).
- **Chapter 4**: a second baseline family (+2 pages: frozen-backbone linear probe vs full
  fine-tune), and the multi-view aggregation ablations (+1 page).
- **Chapter 6/7**: a coded error taxonomy from a sampled failure review (+2 pages) and a
  label-noise study where a stratified sample is re-annotated at full resolution (+2 pages).

### Experiments register (status column to be maintained, not written from memory)
| ID | Experiment | Purpose | Status |
|---|---|---|---|
| E0 | Source verification + dedup audit | establish usable N, duplicate rate | partially done (`docs/02_dataset_inventory.md`) |
| E1 | Labeling pilot: 2 annotators + adjudication | agreement, rubric revision | sample built; labels open |
| E2 | Single-image baseline (transfer learning) | RQ1 | not started |
| E3 | Damage-evidence multi-head variant | RQ3 | not started |
| E4 | Multi-view aggregation + coverage/abstain | RQ2, hazard-miss | not started |
| E5 | Threshold + calibration study on validation | routing-vs-miss trade-off | not started |
| E6 | Independent-source generalisation test | external validity | blocked: needs a second source |
| E7 | Learning curves vs training-set size | is 10k needed; where does it saturate | not started |
| E8 | Error analysis by evidence type (glass / tyre / fluid / lighting / angle) | RQ3 | not started |

Every results cell in chapter 6 stays `[PLACEHOLDER]` until the experiment has actually run.

---

## B. Word budget (sanity check)

| Variant | Body pages | Body words @300/page | Figures & tables | Realistic part-time writing |
|---|---|---|---|---|
| 40 pages | ≈ 33 | ≈ 9,900 | 8–10 | 6–8 weeks |
| 70 pages | ≈ 60 | ≈ 18,000 | 16–20 | 12–14 weeks |

If your programme excludes figures, tables, references and appendices from the limit, the
40-page variant rises to roughly 12,500 body words; treat the 40 column as the floor and the
70 column as the ceiling, and confirm which definition your handbook uses before allocating.
