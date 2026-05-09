# Lessons Learned

- pp045b sparse upper-right rule did not hit real military-equipment targets in visual review.
- pp045c building-context rule removed intact/background buildings, not damaged targets.
- Remaining residual FPs can be suppressed geometrically in frozen scoring, but the pp046a cleanup rule needs visual review because it touches dense-tail, right-edge building, and mid-context cases.
