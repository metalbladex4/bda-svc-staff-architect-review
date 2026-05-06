# Integration Design

Status: `design_only`

## Recommended First Implementation

Build an offline guard simulator first. It should read existing predicted JSON
from v015a/v015b/v015c/v015d hinge runs and write new candidate-local outputs:

- `guarded_predicted/`
- `guard_diagnostics.json`
- `before_after_gate_summary.json`
- `case_101_guard_review.md`

This keeps raw predictions intact and avoids changing the runtime detector
before the guard's behavior is measurable.

## Future Runtime Insertion Options

Source inspection points to these future options:

- `src/bda_svc/pipeline/detectors.py`: `VLMPromptDetector.detect()` parses VLM
  JSON and returns pixel-space `Detection` records.
- `src/bda_svc/pipeline/model.py`: `BDAPipeline.detect_objects()` receives raw
  detections, attaches crops, sorts them, and returns detections for assessment.
- `src/bda_svc/pipeline/interfaces.py`: `Detection` is the lightweight object
  shape a guard could consume.

If a runtime guard is later approved, the least invasive hook is likely between
`self.detector_backend.detect(...)` and crop attachment in
`BDAPipeline.detect_objects()`, because that prevents rejected boxes from
entering damage assessment while preserving backend parsing.

## Why Not Runtime First

- v015d showed that suppressing bad shape can collapse recall.
- Case `101` has reference-shape caveats, so automatic suppression must remain
  auditable.
- A runtime hook would change product behavior, not just prompt-lab evidence.
- The safer first proof is before/after scoring on existing predictions.

## Required Audit Behavior

Any future guard must preserve:

- raw model output
- raw evaluation results
- guard decisions with reason codes
- before/after metrics
- manual review notes for case `101`
