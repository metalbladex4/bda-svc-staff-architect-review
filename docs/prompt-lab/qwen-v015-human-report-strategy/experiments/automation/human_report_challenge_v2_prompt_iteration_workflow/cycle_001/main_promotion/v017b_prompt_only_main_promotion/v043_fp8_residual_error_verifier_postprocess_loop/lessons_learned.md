# v043 Lessons Learned

- The residual inventory confirms p1753 leaves both dense missed targets and FP clusters; geometry-only suppression is high-risk around cases 66/67/84/110.
- Prediction-only postprocessing must reject any rule that removes TPs, drops matches, increases FNs, or worsens dense/control cases.
- Crop/verifier review is the next useful lever before prompt wording resumes.
- The first useful post-p1753 improvement came from a tiny dense military-equipment prediction filter, not another duplicate-containment rule.
- `pp0157` is promising because it removes four case-66 FPs while preserving matches/FNs, but its future-data safety depends on visual review of dense military-equipment clusters.
- Prompt wording should remain paused until residual visual evidence identifies a lever that is not the v035/v037 dense-fragment or same-wreck wording family.
