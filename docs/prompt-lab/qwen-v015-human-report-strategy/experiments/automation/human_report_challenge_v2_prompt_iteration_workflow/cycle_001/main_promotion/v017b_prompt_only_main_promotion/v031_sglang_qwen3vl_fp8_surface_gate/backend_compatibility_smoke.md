# Backend Compatibility Smoke

Both SGLang and vLLM accepted the OpenAI-compatible bda-svc style request shape with system message, user text plus `image_url`, `response_format=json_schema`, and temperature. SGLang failed behaviorally on case 67. vLLM passed stability and failed acceptance only at the fresh full-baseline gate.
