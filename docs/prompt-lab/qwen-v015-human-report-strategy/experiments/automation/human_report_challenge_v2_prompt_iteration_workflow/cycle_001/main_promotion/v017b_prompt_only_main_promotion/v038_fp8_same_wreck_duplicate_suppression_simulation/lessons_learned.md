# v038 Lessons Learned

- Offline simulation is strong enough to test duplicate suppression without risking prompt-shape instability.
- A safe rule must prove zero recall loss and preserve dense cases before it can motivate experiment-only post-processing.
- Same-wreck duplicate handling should remain non-promoted evidence until implemented and replayed in a separate experiment-only tranche.
- Best rule `r001` achieved `181/38/25/63`.
