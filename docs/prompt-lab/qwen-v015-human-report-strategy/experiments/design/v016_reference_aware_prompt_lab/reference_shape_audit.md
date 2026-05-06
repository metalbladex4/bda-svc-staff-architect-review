# Reference Shape Audit

Status: `complete_for_design_only`

This audit separates prompt-relevant failures from reference/evaluation-shape
caveats before any v016 prompt text is authored. It does not mutate source
truth.

## Main Manual Diagnostic: Case 101

Case `101` remains useful, but only as a manual diagnostic. The v015e hinge
run suppressed row-fragment enumeration, but it still produced a broad
group/scene box spanning much of the image:

- predicted bbox: `[75, 13, 1000, 571]`
- row-fragment enumeration: suppressed
- broad group/scene box: present
- case metrics: 1 match, 11 false negatives, 0 false positives

The manual review also records reference-shape caveats:

- `target_1` is a large foreground reference target, which can make oversized
  predictions look numerically better than they look visually.
- `target_7` and `target_8` are duplicate reference boxes at
  `[531, 131, 568, 170]`.

Consequence: `101` should remain in the hinge pack, but v016 should not be
optimized only to improve its aggregate metrics. The correct design target is
to separate dense-target recall, broad-box rejection, and reference-shape
caveats.

## Other Dev Outliers

| Case | Role | Caveat status | Design interpretation |
| --- | --- | --- | --- |
| `66` | dense equipment recall | no source-recorded caveat | Prompt-recall failure unless later visual audit says otherwise. |
| `67` | dense mixed recall/precision | no source-recorded caveat | Misplaced enumeration evidence; prompt needs discovery plus self-filter. |
| `69` | single-target precision | no source-recorded caveat | Unsupported extra prediction. |
| `84` | dense equipment recall | no source-recorded caveat | Strong prompt-recall failure. |
| `86` | wrong-boundary building case | no source-recorded caveat | Target/boundary selection failure. |
| `97` | building precision | no source-recorded caveat | Unsupported extra building/context detections. |
| `100` | multi-building recall | no source-recorded caveat | Missed secondary visible targets. |
| `103` | single-target precision | no source-recorded caveat | Unsupported extra prediction. |
| `147` | mixed-category recall | no source-recorded caveat | Missed supported targets across categories. |

## Protected Controls

Case `155` is the dev protected object-not-found control. It stayed
abstention-safe in v015e and must remain a no-regression gate.

Case `166` is the holdout protected object-not-found control. It was not run in
the v015e dev wave and is included here only as reference-only future guard
awareness. It must not be used for direct prompt tuning until a separately
approved holdout wave.

## Audit Conclusion

Most reviewed dev outliers are prompt-relevant. Case `101` is both
prompt-relevant and reference/eval-shape caveated, so it should guide v016
method design rather than become a single numeric optimization target.
