# v050 Final Recommendation

Backend ran: `true`.

Case 40 image resolved: `true`.

Old/product v020c remains the incumbent under prior non-FP8 evidence: `186 / 33 / 25 / 58`.

Locked FP8 composite baseline remains pp045c: `181 / 38 / 11 / 49`.

Diagnostic pp046a remains diagnostic-only and is not locked: `181 / 38 / 0 / 38`.

v024o remains partial/unscored and was not used as scored evidence.

Strategies tested: `A, B, C, D` on the micro-pack.

Micro-pack baseline: `51/25/5/30`.

Micro-pack raw merged: `58/18/48/66`.

Micro-pack postprocessed merged: `58/18/48/66`.

Added detections: `50`; added TPs: `8`; added FPs: `42`.

Full all-current run: `false`.

Decision: `B`.

Next action: Recommend v051 crop-level verifier gating before any full-pack merge.

Hard boundaries were preserved: reference boxes were not used for inference crop generation, pp046a stayed diagnostic-only, and no product/runtime/source-truth files were mutated.
