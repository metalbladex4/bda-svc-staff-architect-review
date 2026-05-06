# Reference Truth Audit

Scope: narrow reference-shape audit only. Source references are
not changed in this wave.

| Case | Duplicate reference boxes | Large group target | Audit finding |
| --- | --- | --- | --- |
| 101 | 1 | yes | Reference-shape caveats present; do not mutate source truth in this wave, but require manual review before interpreting 101 as pure prompt failure. |
| 12 | 0 | no | No reference-shape anomaly found in this narrow audit. |
| 28 | 0 | no | No reference-shape anomaly found in this narrow audit. |
| 155 | 0 | no | No reference-shape anomaly found in this narrow audit. |

## Overall Finding

Case 101 is mixed: v015a has real prompt-output problems, but the reference set also has duplicate target geometry and a large group reference target. Cases 12 and 28 are cleaner precision regressions. Case 155 remains protected.
