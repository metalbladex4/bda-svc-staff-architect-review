# v033 Retry Policy Design

Scope: experiment-only. Product runtime is unchanged.

- Per-case request timeout: `180` seconds.
- Retries per case after first failure: `2`.
- Cooldown between retries: `5` seconds.
- Backend restart between retries: no.
- Partial packs are never scored.
- A full run is valid only if every case completes and eval writes a full summary.
