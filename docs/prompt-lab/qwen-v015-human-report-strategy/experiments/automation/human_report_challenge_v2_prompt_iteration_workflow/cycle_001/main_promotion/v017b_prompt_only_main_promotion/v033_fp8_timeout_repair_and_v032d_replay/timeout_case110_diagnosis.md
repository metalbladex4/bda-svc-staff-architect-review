# v033 Case 110 Timeout Diagnosis

Generated: `2026-05-09T01:30:05Z`

Case 110 image: `/home/williambenitez1/Capstone/z_reference_docs/Data_set_Storage/human_reports/images_with_reports/110.jpg`

- Original dimensions: `312x208`.
- Image SHA-256: `268e86116da6e63c87e6142602132824c06a6dffe7dfa625c2302bfc7cb49bbd`.
- v032 failure mode: `APITimeoutError('Request timed out.')` before raw response capture with the upstream OpenAI client timeout at 60 seconds.
- v033 repair: experiment-only request timeout raised to `180` seconds, with up to `2` retries and `5` seconds cooldown. Product runtime was not changed.

## Case 110 Validation

| Prompt | Metrics | Retries | Rendered Hash | Request Hash |
|---|---:|---:|---|---|
| baseline v020c FP8 | `3/4/1/5` | `0` | `0587223980d60833ca82c1458f3c878aebf7c66f2f470a260175dda4d77ae80b` | `9b8ad6cb1ec17263632c72bb02a5f6f1096403ea183f492e6800ef1e19ed8c83` |
| v032d single-case | `3/4/1/5` | `0` | `aeff2baeecf7f47b14114280c26b853d072172f883e5ed495dbdbf609c4af72f` | `7b492bb4feffa72bf9506c5f4d4ec1057334ef28f09be91940bc051be9a83dac` |
| v032d full-run case 110 | `3/4/32` | `0` | `aeff2baeecf7f47b14114280c26b853d072172f883e5ed495dbdbf609c4af72f` | `7b492bb4feffa72bf9506c5f4d4ec1057334ef28f09be91940bc051be9a83dac` |

The repair worked mechanically: case 110 completed under v033. However, in the full run v032d produced `35` predicted targets for case 110, yielding `3/4/32`; this is a quality rejection signal, not a timeout failure.
