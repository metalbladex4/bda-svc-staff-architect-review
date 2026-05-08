#!/usr/bin/env python3
"""Experiment-only OpenAI-compatible shim for local Qwen3-VL Transformers.

This file lives inside the v030 evidence package on purpose. It is not product
runtime. It exists only to test whether the exact public Hugging Face model can
serve the request shape that bda-svc sends to an OpenAI-compatible backend.
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import time
from typing import Any

import torch
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from qwen_vl_utils import process_vision_info
from transformers import AutoModelForImageTextToText, AutoProcessor


MODEL_ID = os.getenv("HF_MODEL_ID", "Qwen/Qwen3-VL-8B-Instruct")
SERVED_MODEL_NAME = os.getenv("HF_SERVED_MODEL_NAME", MODEL_ID)
DTYPE_NAME = os.getenv("HF_DTYPE", "bfloat16")
MAX_NEW_TOKENS = int(os.getenv("HF_MAX_NEW_TOKENS", "512"))
OFFLOAD_DIR = os.getenv(
    "HF_OFFLOAD_DIR",
    "docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/"
    "human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/"
    "v017b_prompt_only_main_promotion/v030_exact_model_or_surface_equivalence_gate/"
    "traces/hf_transformers_offload",
)
INPUT_DEVICE = os.getenv("HF_INPUT_DEVICE", "none")


def _dtype() -> torch.dtype:
    if DTYPE_NAME == "float16":
        return torch.float16
    if DTYPE_NAME == "float32":
        return torch.float32
    return torch.bfloat16


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


app = FastAPI(title="v030 Hugging Face Transformers OpenAI Shim")

processor = None
model = None
model_load_error: str | None = None
model_loaded_at: float | None = None
generation_kwargs = {
    "do_sample": False,
    "max_new_tokens": MAX_NEW_TOKENS,
}


class ChatCompletionRequest(BaseModel):
    model: str
    messages: list[dict[str, Any]]
    temperature: float | None = None
    response_format: dict[str, Any] | None = None
    max_tokens: int | None = None
    stop: Any | None = None


def _load_model() -> None:
    global processor, model, model_load_error, model_loaded_at
    if model is not None:
        return
    try:
        os.makedirs(OFFLOAD_DIR, exist_ok=True)
        processor = AutoProcessor.from_pretrained(MODEL_ID, trust_remote_code=True)
        model = AutoModelForImageTextToText.from_pretrained(
            MODEL_ID,
            torch_dtype=_dtype(),
            device_map="auto",
            max_memory={0: "14GiB", "cpu": "24GiB"} if torch.cuda.is_available() else None,
            offload_folder=OFFLOAD_DIR,
            low_cpu_mem_usage=True,
            trust_remote_code=True,
        )
        model.eval()
        model_loaded_at = time.time()
    except Exception as exc:  # pragma: no cover - this is a launch-time probe.
        model_load_error = repr(exc)
        raise


@app.on_event("startup")
def startup() -> None:
    _load_model()


@app.get("/v1/models")
def models() -> dict[str, Any]:
    return {
        "object": "list",
        "data": [
            {
                "id": SERVED_MODEL_NAME,
                "object": "model",
                "created": int(model_loaded_at or time.time()),
                "owned_by": "local-huggingface-transformers",
            }
        ],
    }


def _normalize_content_item(item: dict[str, Any]) -> dict[str, Any] | None:
    item_type = item.get("type")
    if item_type == "text":
        return {"type": "text", "text": item.get("text", "")}
    if item_type == "image_url":
        image_url = item.get("image_url")
        if isinstance(image_url, dict):
            url = image_url.get("url")
        else:
            url = image_url
        if not isinstance(url, str):
            raise HTTPException(status_code=400, detail="image_url item missing url")
        if url.startswith("data:image") and "base64," in url:
            # Validate base64 without storing it in traces.
            _, encoded = url.split("base64,", 1)
            base64.b64decode(encoded, validate=False)
        return {"type": "image", "image_url": url}
    return None


def _to_hf_messages(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    hf_messages: list[dict[str, Any]] = []
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        if isinstance(content, str):
            hf_content = [{"type": "text", "text": content}]
        elif isinstance(content, list):
            hf_content = []
            for item in content:
                if isinstance(item, dict):
                    normalized = _normalize_content_item(item)
                    if normalized is not None:
                        hf_content.append(normalized)
        else:
            hf_content = [{"type": "text", "text": str(content)}]
        hf_messages.append({"role": role, "content": hf_content})
    return hf_messages


@app.post("/v1/chat/completions")
def chat_completions(request: ChatCompletionRequest) -> dict[str, Any]:
    if model is None or processor is None:
        raise HTTPException(status_code=503, detail=model_load_error or "model not loaded")
    started = time.time()
    hf_messages = _to_hf_messages(request.messages)
    try:
        rendered = processor.apply_chat_template(
            hf_messages,
            tokenize=False,
            add_generation_prompt=True,
        )
        image_inputs, video_inputs = process_vision_info(hf_messages)
        inputs = processor(
            text=[rendered],
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt",
        )
        if INPUT_DEVICE == "cuda" and torch.cuda.is_available():
            inputs = inputs.to("cuda")
        elif INPUT_DEVICE == "cpu":
            inputs = inputs.to("cpu")
        max_new_tokens = request.max_tokens or MAX_NEW_TOKENS
        generated = model.generate(
            **inputs,
            do_sample=False,
            max_new_tokens=max_new_tokens,
        )
        trimmed = [out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated)]
        text = processor.batch_decode(
            trimmed,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False,
        )[0]
    except Exception as exc:
        raise HTTPException(status_code=500, detail=repr(exc)) from exc

    return {
        "id": f"chatcmpl-v030-hf-{int(started)}",
        "object": "chat.completion",
        "created": int(started),
        "model": SERVED_MODEL_NAME,
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": text},
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": int(inputs.input_ids.shape[-1]),
            "completion_tokens": int(trimmed[0].shape[-1]),
            "total_tokens": int(inputs.input_ids.shape[-1] + trimmed[0].shape[-1]),
        },
        "v030_trace": {
            "rendered_chat_template_sha256": _sha256_text(rendered),
            "generation_kwargs": {**generation_kwargs, "max_new_tokens": max_new_tokens},
            "input_device_mode": INPUT_DEVICE,
            "elapsed_seconds": round(time.time() - started, 3),
            "response_format_supplied": request.response_format is not None,
            "temperature_supplied": request.temperature,
        },
    }


def main() -> None:
    host = os.getenv("HF_SHIM_HOST", "127.0.0.1")
    port = int(os.getenv("HF_SHIM_PORT", "8000"))
    print(
        json.dumps(
            {
                "event": "v030_hf_transformers_shim_start",
                "model_id": MODEL_ID,
                "served_model_name": SERVED_MODEL_NAME,
                "dtype": DTYPE_NAME,
                "max_new_tokens": MAX_NEW_TOKENS,
                "input_device_mode": INPUT_DEVICE,
                "offload_dir": OFFLOAD_DIR,
                "host": host,
                "port": port,
            },
            sort_keys=True,
        ),
        flush=True,
    )
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
