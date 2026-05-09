# v032 Lessons Learned

- The FP8 vLLM surface is stable enough for micro-pack prompt testing, but it is a separate model line and not a continuation of the old v020c surface.
- Baseline sentinel replay preserved dense case 67 at `10/1/2`, but retained the FP8 case-155 FP regression at `2/0/2`.
- `v032a` proved the importance of rendered-prompt hash checks: an intended prompt edit can silently become a no-op.
- `v032b` showed broad context/fragment precision guards can fix one case-155 FP while worsening dense cases and total micro errors.
- `v032c` showed compact FP8 calibration language can weaken recall without improving controls.
- `v032d` showed the v019c anchor can reduce FPs and fix case 155 on the sentinel, but it weakens case 67/84 recall and its full all-current run timed out.
- Do not advance an FP8 working best from micro evidence alone when full all-current is incomplete.
