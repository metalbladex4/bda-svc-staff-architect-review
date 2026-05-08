# v029 Backend Compatibility Smoke

- `/v1/models`: passed.
- Minimal text-only chat completion: passed.
- bda-svc detection request with one image: passed.
- bda-svc assessment request with two images: failed at image limit `1`, passed after relaunch with image limit `2`.
- `response_format` JSON/schema path: supported during instrumented bda-svc runs.
