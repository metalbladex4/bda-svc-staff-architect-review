# SGLang Install Or Environment Report

SGLang was installed into the isolated environment `/tmp/bda_v031_sglang_env`. No system-wide destructive install was performed.

Important recovery steps:

- `libnuma.so.1` was missing, so `libnuma1` was downloaded and extracted into the isolated env path instead of installed system-wide.
- PyTorch/CuDNN required `nvidia-cudnn-cu12==9.16.0.29`, installed inside the isolated env.
- CUDA graph capture failed because `nvcc`/CUDA toolkit was unavailable, so the successful launch used `--disable-cuda-graph`.

SGLang then launched official FP8 successfully, but failed the behavior gate: all case-67 probes were `0/11/1`.
