# Sweep Summary

## Conclusion

The frozen `v006 + v008 + v004` stack is the strongest cross-image candidate
in the current branch-aware line so far.

## Why

It fixes the two main failures exposed by the earlier `v000` vs `v004` sweep:

- `operational_tank4` is back to `NO DAMAGE` / `CONFIRMED`
- `destroyed_building4` is back to two separate building targets

And it does that while:

- preserving the tank pressure-case improvement signal
- keeping the negative office scene clean
- staying acceptable on another destroyed tank and an intact building

## Remaining Caution

The main residual issue is no longer detection recall. It is calibration:

- on `destroyed_building4`, the frozen stack labels both buildings as
  `DESTROYED`
- the fresh baseline had split them between `SEVERE DAMAGE` and `DESTROYED`

So the stack now looks much safer cross-image than the earlier `v004` sweep
candidate, but building-severity calibration is still worth monitoring.

## Working Recommendation

Treat the frozen stack as the current best branch-aware promotion candidate:

- `detect_objects` from `v006`
- `assess_damage` from `v008`
- `summarize_scene` from `v004`

Next move should be process-oriented, not another prompt draft by default:

1. stage this frozen stack as the current winner in the branch-aware lab
2. preserve the feature-branch `bda_eval` changes cleanly
3. decide whether to prepare promotion into tracked config work on the branch
   or pause here with the candidate stack documented
