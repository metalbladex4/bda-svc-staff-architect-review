# v038 Simulation Plan

The simulation reads frozen `v034a` predictions, removes duplicate-like boxes in memory, and recomputes the same `bda_eval` detection-study matching logic. It does not call the VLM and does not edit runtime or eval truth.
