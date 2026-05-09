# v040 r019 vs r020 Tradeoff

- r020: `181/38/22/60`, `3` removals; numeric best, but label-agnostic and includes cross-label case 100.
- r019: `181/38/23/61`, `2` removals; safer same-label footprint.
- hybrid: `181/38/22/60`, `3` removals; same-label OR zero-reference-IoU cross-label.

Decision `C`: hybrid rule beats or matches r020 with safer semantics.
