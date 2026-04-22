# Runtime Candidate Doctrine `v002`

This revision only changes `buildings.detection_guidance`.

Intent:

- tighten what counts as the selected building body in mixed adjacent-building
  scenes
- reduce false splitting of neighboring intact facades into separate damaged
  building detections
- keep the rest of the doctrine candidate unchanged so the next Qwen rerun
  isolates the effect of building-selection language rather than broader PDA
  wording changes

Operational expectation:

- better target delimitation on `destroyed_building4`-style scenes
- neutral behavior on equipment and office-negative controls
- no schema or runtime-contract change
