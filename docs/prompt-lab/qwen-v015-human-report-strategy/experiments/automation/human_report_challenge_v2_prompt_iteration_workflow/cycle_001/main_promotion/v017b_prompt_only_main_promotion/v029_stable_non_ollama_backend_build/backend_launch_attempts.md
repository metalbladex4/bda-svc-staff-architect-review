# v029 Backend Launch Attempts

1. Exact `Qwen/Qwen3-VL-8B-Instruct` with vLLM was not launched because its
   measured safetensor shards total about 17.53 GB, which is above the local
   16 GB VRAM envelope before KV/cache.
2. Public quantized `SherlockID365/Qwen3-VL-8B-Instruct-quantized.w4a16`
   launched under vLLM with served model name `Qwen/Qwen3-VL-8B-Instruct`.
3. Initial launch allowed one image per prompt. Detection worked, but bda-svc
   assessment sent two images and vLLM rejected the request.
4. Relaunch with `--limit-mm-per-prompt.image 2` passed request-shape
   compatibility, Stage 1, Stage 2, all-current baseline, and office-negative.

SGLang and Transformers/FastAPI shim were not attempted because vLLM reached the
non-Ollama serving and stability gates first.
