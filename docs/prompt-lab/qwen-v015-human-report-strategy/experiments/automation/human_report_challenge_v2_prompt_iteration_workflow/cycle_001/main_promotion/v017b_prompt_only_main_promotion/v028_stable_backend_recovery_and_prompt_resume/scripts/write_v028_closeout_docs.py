#!/usr/bin/env python3
"""Write v028 closeout documents from generated stability evidence."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any


PACKAGE_ROOT = Path(__file__).resolve().parents[1]


def utc_now() -> str:
    return dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_json(name: str) -> Any:
    return json.loads((PACKAGE_ROOT / name).read_text(encoding="utf-8"))


def write_json(name: str, payload: Any) -> None:
    (PACKAGE_ROOT / name).write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def write_text(name: str, text: str) -> None:
    (PACKAGE_ROOT / name).write_text(text.rstrip() + "\n", encoding="utf-8")


def table(records: list[dict[str, Any]]) -> str:
    lines = [
        "| probe | case 67 | raw response | rendered prompt | request shape | status |",
        "| --- | ---: | --- | --- | --- | --- |",
    ]
    for record in records:
        lines.append(
            "| `{candidate}` | `{case67}` | `{raw}` | `{rendered}` | `{request}` | `{status}` |".format(
                candidate=record["candidate_id"],
                case67=record["case_67"],
                raw=record.get("raw_response_hash", "see response manifest"),
                rendered=record["rendered_prompt_hash"],
                request=record["request_shape_hash"],
                status=record["status"],
            )
        )
    return "\n".join(lines)


def main() -> int:
    preflight = read_json("backend_preflight.json")
    final = read_json("final_recommendation.json")
    matrix = read_json("backend_stability_matrix.json")
    records = final.get("stage1_records", [])
    original_preferred_available = not bool(preflight.get("deterministic_ollama_create"))
    selected = preflight.get("selected_backend", {})
    updated = utc_now()

    final["updated_at"] = updated
    final["original_preferred_backend_available_before_recovery"] = original_preferred_available
    final["preferred_port_8000_after_recovery"] = {
        "available": bool(preflight["preferred_endpoint_status"]["ok"]),
        "server_kind": "ollama" if selected.get("label") == "ollama_deterministic_local_8000" else "unknown",
        "equivalent_to_original_preferred_vllm_backend": False,
    }
    final["stable_backend_recovered_or_launched"] = False
    final["semantic_prompt_refinement_resumed"] = False
    final["stability_decision"] = "D. no_stable_backend_available_stop_prompt_mutation"
    final["why"] = (
        "A deterministic Ollama-backed local endpoint on port 8000 still failed Stage 1: "
        "exact v020c replay 1 collapsed to 1/10/9 while exact replays 2 and 3 returned 9/2/4; "
        "blank-line and trailing-space probes also collapsed."
    )
    write_json("final_recommendation.json", final)
    write_json(
        "stability_decision.json",
        {
            "generated_at": updated,
            "decision": "D. no_stable_backend_available_stop_prompt_mutation",
            "stable_backend_recovered_or_launched": False,
            "semantic_prompt_refinement_resumed": False,
            "original_preferred_backend_available_before_recovery": original_preferred_available,
            "backend_tested": selected,
            "stage1_passed": False,
            "stage2_run": False,
            "reason": final["why"],
        },
    )

    write_text(
        "final_recommendation.md",
        f"""# v028 Final Recommendation

Updated: `{updated}`

Status: `stability_failed_stage1`

Decision: `D. no_stable_backend_available_stop_prompt_mutation`

## Summary

No stable backend was recovered. The original preferred `localhost:8000/v1`
backend was unavailable before recovery. v028 created a deterministic
Ollama-backed Qwen model alias from cached local model files and launched an
experiment-only Ollama endpoint on `localhost:8000/v1`, but that endpoint still
failed the case-67 stability gate.

Semantic prompt refinement did not resume.

## Backend Tested

- backend label: `{selected.get('label')}`
- endpoint: `{selected.get('base_url')}`
- model: `{selected.get('model')}`
- local model source: `cached Ollama model`
- public/HF model download: `not performed`
- product runtime/config mutation: `none`

## Stage 1 Case 67 Results

{table(records)}

## Interpretation

The deterministic Ollama alias used `temperature 0`, `top_k 1`, `top_p 1`,
`seed 42`, and `num_ctx 4096`. Even with those settings, the first exact
`v020c` replay collapsed while later exact/no-op replays returned the known
stable case-67 behavior. The blank-line and trailing-space probes collapsed
consistently.

This is enough to keep prompt mutation paused. The strongest remaining
hypothesis is a backend/model-serving instability or cold-start/request-shape
sensitivity in the Ollama-backed path, not a trustworthy prompt-quality signal.

## Required Next Fix Before Autonomy

Restore a genuinely stable OpenAI-compatible multimodal backend, preferably a
vLLM/SGLang/Transformers server that supports the bda-svc request shape and can
pass exact replay plus blank-line/trailing-space probes before any semantic
prompt work resumes.
""",
    )

    write_text(
        "stability_decision.md",
        """# v028 Stability Decision

Decision: `D. no_stable_backend_available_stop_prompt_mutation`

The deterministic Ollama-backed recovery endpoint did not pass Stage 1. Do not
resume semantic prompt mutation.
""",
    )

    write_text(
        "backend_launch_attempts.md",
        f"""# v028 Backend Launch Attempts

Generated: `{updated}`

## Original Preferred Backend

- endpoint: `http://localhost:8000/v1`
- status before recovery: `unavailable`
- established project command found: `vllm serve Qwen/Qwen3-VL-8B-Instruct`
- vLLM installed locally: `no`
- Qwen/Qwen3-VL-8B-Instruct HF cache present: `no`

## Deterministic Ollama Recovery

- model alias: `qwen3-vl:8b-instruct-v028-deterministic`
- source model: cached `qwen3-vl:8b-instruct`
- endpoint launched: `http://localhost:8000/v1`
- server kind: `Ollama OpenAI-compatible`
- result: `launched but failed Stage 1 stability`
- cleanup: experiment-only port-8000 Ollama process was stopped after failure.
""",
    )

    write_text(
        "stable_backend_recovery.md",
        """# v028 Stable Backend Recovery

No stable backend was recovered. The only locally feasible recovery path without
new large installs/downloads was an Ollama deterministic model alias. That path
still reproduced the v027 instability pattern on case 67.
""",
    )

    write_text(
        "deterministic_settings_probe.md",
        """# v028 Deterministic Settings Probe

The deterministic Ollama alias was created with:

```text
FROM qwen3-vl:8b-instruct
PARAMETER temperature 0
PARAMETER top_k 1
PARAMETER top_p 1
PARAMETER seed 42
PARAMETER num_ctx 4096
```

Official Ollama Modelfile documentation states that `seed` sets the random
number seed for generation and that temperature/top-k/top-p control sampling.
Local evidence shows these settings were insufficient to make the fallback
Ollama-backed Qwen3-VL path safe for prompt optimization.
""",
    )

    write_json(
        "raw_request_replay_matrix.json",
        {
            "generated_at": updated,
            "records": [
                {
                    "candidate_id": record["candidate_id"],
                    "case_67": record["case_67"],
                    "rendered_prompt_hash": record["rendered_prompt_hash"],
                    "request_shape_hash": record["request_shape_hash"],
                    "raw_response_hash": record.get("raw_response_hash"),
                    "status": record["status"],
                }
                for record in records
            ],
        },
    )
    write_text(
        "raw_request_replay_matrix.md",
        "# v028 Raw Request Replay Matrix\n\n" + table(records),
    )

    write_text(
        "research_notes.md",
        """# v028 Research Notes

## vLLM

- Source: Context7 vLLM docs, multimodal/OpenAI-compatible serving snippets.
- Useful note: vLLM documents `vllm serve <multimodal-model>` and
  OpenAI-compatible multimodal chat requests using user content lists with text
  and `image_url` items. It also documents seed-based deterministic examples.
- Local impact: vLLM would be a better target for the preferred backend, but it
  was not installed and the HF Qwen3-VL model was not cached.

## Hugging Face Model Metadata

- Source: Hugging Face repo details for `Qwen/Qwen3-VL-8B-Instruct`.
- Useful note: the model is public, Apache-2.0, image-text-to-text, and not
  gated/private.
- Local impact: no download was performed because the full model was not cached
  and a blind vLLM/Transformers install plus full-model pull was not judged a
  safe recovery step on the current 16 GB VRAM machine.

## Ollama

- Source: official Ollama Modelfile Reference.
- Useful note: `seed`, `temperature`, `top_k`, and `top_p` are documented
  Modelfile parameters.
- Local impact: v028 tested those deterministic controls directly. They did not
  make the Ollama-backed path pass the stability gate.
""",
    )

    write_text(
        "README.md",
        """# v028 Stable Backend Recovery And Prompt Resume

This package records an evidence-only backend stability recovery tranche. It
does not promote anything and does not author semantic prompt candidates.

Outcome: no stable backend was recovered. Prompt mutation remains paused.
""",
    )

    write_text(
        "diagnoses/v028_stage1_backend_stability_diagnosis.md",
        f"""# v028 Stage 1 Backend Stability Diagnosis

Generated: `{updated}`

The deterministic Ollama-backed local endpoint failed Stage 1. Exact v020c
replay 1 returned `1/10/9`, exact replays 2 and 3 returned `9/2/4`, and the
blank-line/trailing-space probes returned `1/10/9`.

The run captured rendered prompt hashes, request-shape hashes, raw response
hashes, and response/parsing traces. The failure remains a serving/repeatability
blocker rather than prompt-learning evidence.
""",
    )

    write_text(
        "pause_report.md",
        """# v028 Pause Report

Semantic prompt refinement remains paused because no backend passed the
repeatability gate. Resume only after a stable multimodal OpenAI-compatible
backend passes exact replay and no-semantics shape probes.
""",
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
