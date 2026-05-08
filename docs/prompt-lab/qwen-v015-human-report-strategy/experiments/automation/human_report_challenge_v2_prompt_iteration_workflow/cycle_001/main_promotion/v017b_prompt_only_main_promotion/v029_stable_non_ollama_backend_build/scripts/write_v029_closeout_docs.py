#!/usr/bin/env python3
"""Write v029 closeout docs from generated stability/baseline artifacts."""

from __future__ import annotations

import datetime as dt
import glob
import json
from pathlib import Path


WORKTREE_ROOT = Path(
    "/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement"
)
PACKAGE_ROOT = (
    WORKTREE_ROOT
    / "docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/"
    "human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/"
    "v017b_prompt_only_main_promotion/v029_stable_non_ollama_backend_build"
)


def utc_now() -> str:
    return dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def find_one(pattern: str) -> Path | None:
    paths = sorted(glob.glob(str(PACKAGE_ROOT / pattern), recursive=True))
    return Path(paths[-1]) if paths else None


def image_metrics(summary: dict, image_id: int) -> dict | None:
    candidates = {f"{image_id}.jpg", f"{image_id:02d}.jpg", f"{image_id}.png", f"{image_id:02d}.png"}
    for image in summary.get("images", []):
        if image.get("image_filename") in candidates:
            return {
                "image_filename": image.get("image_filename"),
                "matches": image.get("match_count"),
                "false_negatives": image.get("false_negative_count"),
                "false_positives": image.get("false_positive_count"),
                "reference_target_count": image.get("reference_target_count"),
                "predicted_target_count": image.get("predicted_target_count"),
            }
    return None


def compact_stage_records(records: list[dict]) -> list[dict]:
    return [
        {
            "candidate_id": record.get("candidate_id"),
            "stage": record.get("stage"),
            "case_67": record.get("case_67"),
            "raw_response_hash": record.get("raw_response_hash"),
            "rendered_prompt_hash": record.get("rendered_prompt_hash"),
            "request_shape_hash": record.get("request_shape_hash"),
            "status": record.get("status"),
        }
        for record in records
    ]


def main() -> int:
    generated_at = utc_now()
    source_manifest = read_json(PACKAGE_ROOT / "source_manifest.json")
    stability = read_json(PACKAGE_ROOT / "final_recommendation.json")
    matrix = read_json(PACKAGE_ROOT / "backend_stability_matrix.json")
    baseline = read_json(PACKAGE_ROOT / "new_backend_v020c_baseline.json")
    preflight = read_json(PACKAGE_ROOT / "backend_preflight.json")

    all_summary_path = find_one(
        "runs/v020c_vllm_quantized_baseline/full_v020c_baseline/**/eval/*summary*.json"
    )
    office_summary_path = find_one(
        "runs/v020c_vllm_quantized_office_negative/office_negative_guard/**/eval/*summary*.json"
    )
    all_summary = read_json(all_summary_path) if all_summary_path else {}
    office_summary = read_json(office_summary_path) if office_summary_path else {}

    stage_records = matrix.get("records", [])
    stage1 = [record for record in stage_records if record.get("stage") == "case67_stability"]
    stage2 = [record for record in stage_records if record.get("stage") == "sentinel_stability"]
    baseline_record = baseline.get("all_current_record") or {}
    office_record = baseline.get("office_negative_record") or {}

    selected_cases = {
        str(case_id): image_metrics(all_summary, case_id)
        for case_id in [12, 14, 16, 42, 66, 67, 77, 84, 88, 90, 97, 103, 155, 166, 172]
    }

    decision = {
        "generated_at": generated_at,
        "decision": "D. stable_backend_found_but_v020c_baseline_unacceptable_pause",
        "semantic_prompt_refinement_resumed": False,
        "backend": {
            "label": "vllm_quantized_qwen3_vl_8b_local_8000",
            "endpoint": "http://localhost:8000/v1",
            "served_model_name": "Qwen/Qwen3-VL-8B-Instruct",
            "actual_model_root": "SherlockID365/Qwen3-VL-8B-Instruct-quantized.w4a16",
            "server_kind": "vLLM OpenAI-compatible",
            "non_ollama": True,
        },
        "model_source": {
            "target_exact_model": "Qwen/Qwen3-VL-8B-Instruct",
            "exact_model_public_non_gated": True,
            "exact_model_weight_bytes": 17534339512,
            "exact_model_feasibility_note": "17.53 GB of weights exceeds the 16 GB VRAM envelope before KV/cache, so exact BF16 8B was not launched.",
            "served_quantized_model": "SherlockID365/Qwen3-VL-8B-Instruct-quantized.w4a16",
            "served_quantized_public_non_gated": True,
            "served_quantized_weight_bytes": 7224284152,
            "download_or_cache_status": "downloaded_public_hf_into_local_cache_by_vLLM",
        },
        "prior_incumbent": {"matches": 186, "false_negatives": 33, "false_positives": 25, "combined_errors": 58},
        "fresh_v020c_baseline": {
            "matches": baseline_record.get("matches"),
            "false_negatives": baseline_record.get("false_negatives"),
            "false_positives": baseline_record.get("false_positives"),
            "combined_errors": baseline_record.get("combined_errors"),
            "image_count": all_summary.get("image_count"),
            "case_101_present": any(
                image.get("image_filename") in {"101.jpg", "101.png"} for image in all_summary.get("images", [])
            ),
            "selected_cases": selected_cases,
        },
        "office_negative": {
            "record": office_record,
            "image_count": office_summary.get("image_count"),
            "totals": office_summary.get("totals"),
            "passed": (
                office_summary.get("image_count") == 1
                and (office_summary.get("totals") or {}).get("negative_scene_false_positive_count") == 0
                and (office_summary.get("totals") or {}).get("negative_scene_abstention_correct_count") == 1
            ),
        },
        "stability": {
            "stage1_passed": all(record.get("status") == "stability_pass" for record in stage1),
            "stage2_passed": all(record.get("status") == "stability_pass" for record in stage2),
            "stage1_records": compact_stage_records(stage1),
            "stage2_records": compact_stage_records(stage2),
        },
        "baseline_gate": {
            "old_combined_errors": 58,
            "new_combined_errors": baseline_record.get("combined_errors"),
            "delta": None
            if baseline_record.get("combined_errors") is None
            else baseline_record.get("combined_errors") - 58,
            "pause_threshold_delta": 20,
            "passed": False,
        },
        "hard_boundaries": {
            "product_config_modified": False,
            "doctrine_modified": False,
            "assessment_prompt_modified": False,
            "runtime_code_modified_as_product_truth": False,
            "eval_truth_modified": False,
            "semantic_prompt_candidate_authored": False,
            "promotion_performed": False,
            "v024o_used_as_scored_evidence": False,
        },
    }

    write_json(PACKAGE_ROOT / "final_recommendation.json", decision)
    write_json(PACKAGE_ROOT / "backend_feasibility_matrix.json", {
        "generated_at": generated_at,
        "options": [
            {
                "backend": "vLLM",
                "status": "launched",
                "model": "SherlockID365/Qwen3-VL-8B-Instruct-quantized.w4a16",
                "reason": "vLLM installed in isolated /tmp env; exact 8B BF16 not VRAM-feasible; quantized public derivative loaded.",
            },
            {
                "backend": "SGLang",
                "status": "not_attempted_after_vllm_launch",
                "reason": "vLLM achieved non-Ollama compatibility and stability; no need to widen install surface.",
            },
            {
                "backend": "Transformers/FastAPI shim",
                "status": "not_attempted_after_vllm_launch",
                "reason": "vLLM achieved OpenAI-compatible multimodal serving.",
            },
            {
                "backend": "Ollama",
                "status": "comparison_only_blocked_for_prompt_optimization",
                "reason": "v027/v028 showed fallback instability.",
            },
        ],
    })
    write_json(PACKAGE_ROOT / "dependency_inventory.json", {
        "generated_at": generated_at,
        "system_python": {"vllm": "not_installed", "sglang": "not_installed", "transformers": "not_installed"},
        "qwen_worktree_venv": {"vllm": "not_installed", "sglang": "not_installed", "transformers": "not_installed"},
        "isolated_vllm_env": {
            "path": "/tmp/bda_v029_vllm_env",
            "vllm": "0.20.1",
            "torch": "2.11.0",
            "transformers": "5.8.0",
            "openai": "2.36.0",
            "fastapi": "0.136.1",
            "uvicorn": "0.46.0",
        },
        "gpu": {
            "name": "NVIDIA RTX 5000 Ada Generation Laptop GPU",
            "vram_mib": 16376,
            "cuda_reported_by_nvidia_smi": "13.0",
        },
        "disk_available": "about 840 GB on /dev/sdd at inventory time",
    })
    write_json(PACKAGE_ROOT / "model_download_or_cache_report.json", decision["model_source"])
    write_json(PACKAGE_ROOT / "backend_install_log.json", {
        "generated_at": generated_at,
        "install_mode": "isolated /tmp uv venv",
        "environment_path": "/tmp/bda_v029_vllm_env",
        "command": "uv pip install --python /tmp/bda_v029_vllm_env/bin/python vllm",
        "result": "success",
        "product_environment_modified": False,
    })
    write_json(PACKAGE_ROOT / "backend_launch_log.json", {
        "generated_at": generated_at,
        "successful_command": (
            "HF_HUB_DISABLE_TELEMETRY=1 /tmp/bda_v029_vllm_env/bin/python "
            "-m vllm.entrypoints.openai.api_server --host 127.0.0.1 --port 8000 "
            "--model SherlockID365/Qwen3-VL-8B-Instruct-quantized.w4a16 "
            "--served-model-name Qwen/Qwen3-VL-8B-Instruct --trust-remote-code "
            "--dtype auto --max-model-len 4096 --limit-mm-per-prompt.image 2 "
            "--gpu-memory-utilization 0.85 --enforce-eager --seed 42 --generation-config vllm"
        ),
        "initial_limit_1_attempt": "launched but failed bda-svc assessment request shape because assessment sends two images",
        "limit_2_attempt": "successful",
    })
    write_json(PACKAGE_ROOT / "backend_compatibility_smoke.json", {
        "generated_at": generated_at,
        "models_endpoint": preflight.get("preferred_endpoint_status"),
        "text_only_chat": "passed with JSON object smoke",
        "bda_svc_multimodal_request": "passed after --limit-mm-per-prompt.image 2",
        "response_format_json_schema": "supported during instrumented bda-svc runs",
    })
    write_json(PACKAGE_ROOT / "new_backend_v020c_baseline.json", {
        **baseline,
        "selected_case_metrics": selected_cases,
        "all_current_summary_path": str(all_summary_path) if all_summary_path else None,
        "office_negative_summary_path": str(office_summary_path) if office_summary_path else None,
        "decision": decision["decision"],
    })

    feasibility_md = """# v029 Backend Feasibility Matrix

| Backend | Result | Notes |
| --- | --- | --- |
| vLLM | launched | Isolated `/tmp/bda_v029_vllm_env`; served public quantized Qwen3-VL 8B derivative on `localhost:8000/v1`. |
| SGLang | not attempted | vLLM reached compatibility/stability, so no need to widen install surface. |
| Transformers/FastAPI shim | not attempted | vLLM provided OpenAI-compatible multimodal serving. |
| Ollama | comparison only | v027/v028 instability keeps Ollama blocked for prompt optimization. |
"""
    write_text(PACKAGE_ROOT / "backend_feasibility_matrix.md", feasibility_md)
    write_text(PACKAGE_ROOT / "dependency_inventory.md", """# v029 Dependency Inventory

- System and Qwen worktree Python envs did not have `vllm`, `sglang`, `transformers`, `torch`, or `openai` installed.
- Created isolated vLLM env: `/tmp/bda_v029_vllm_env`.
- vLLM env: `vllm 0.20.1`, `torch 2.11.0`, `transformers 5.8.0`, `openai 2.36.0`.
- GPU: NVIDIA RTX 5000 Ada Generation Laptop GPU, 16,376 MiB VRAM.
- Disk: about 840 GB available at inventory time.
""")
    write_text(PACKAGE_ROOT / "model_download_or_cache_report.md", """# v029 Model Download Or Cache Report

- Exact target model: `Qwen/Qwen3-VL-8B-Instruct`.
- HF status: public, non-gated, Apache-2.0.
- Exact target weight shards measured by HEAD requests: about 17.53 GB.
- Local GPU VRAM: 16,376 MiB, so exact BF16 8B was not launched because it exceeds the practical VRAM envelope before KV/cache.
- Served model: `SherlockID365/Qwen3-VL-8B-Instruct-quantized.w4a16`.
- Served model status: public, non-gated, Apache-2.0, base model is Qwen3-VL 8B.
- Served model weight shards measured by HEAD requests: about 7.22 GB.
- vLLM downloaded/used the public quantized model through the local Hugging Face cache. No token or private credential was used.
""")
    write_text(PACKAGE_ROOT / "backend_install_log.md", """# v029 Backend Install Log

Installed vLLM into an isolated temporary environment:

```bash
uv venv /tmp/bda_v029_vllm_env --python 3.12
uv pip install --python /tmp/bda_v029_vllm_env/bin/python vllm
```

The project venv and product source were not modified.
""")
    write_text(PACKAGE_ROOT / "backend_launch_log.md", """# v029 Backend Launch Log

Successful launch:

```bash
HF_HUB_DISABLE_TELEMETRY=1 /tmp/bda_v029_vllm_env/bin/python -m vllm.entrypoints.openai.api_server \
  --host 127.0.0.1 --port 8000 \
  --model SherlockID365/Qwen3-VL-8B-Instruct-quantized.w4a16 \
  --served-model-name Qwen/Qwen3-VL-8B-Instruct \
  --trust-remote-code --dtype auto --max-model-len 4096 \
  --limit-mm-per-prompt.image 2 --gpu-memory-utilization 0.85 \
  --enforce-eager --seed 42 --generation-config vllm
```

The first vLLM launch used `--limit-mm-per-prompt.image 1`; detection worked, but bda-svc assessment sent two images and vLLM returned a request-shape error. Relaunching with image limit `2` fixed the compatibility issue.
""")
    write_text(PACKAGE_ROOT / "backend_compatibility_smoke.md", """# v029 Backend Compatibility Smoke

- `/v1/models`: passed.
- Minimal text-only chat completion: passed.
- bda-svc detection request with one image: passed.
- bda-svc assessment request with two images: failed at image limit `1`, passed after relaunch with image limit `2`.
- `response_format` JSON/schema path: supported during instrumented bda-svc runs.
""")
    write_text(PACKAGE_ROOT / "new_backend_v020c_baseline.md", f"""# v029 New Backend v020c Baseline

Backend: `vllm_quantized_qwen3_vl_8b_local_8000`

Actual model root: `SherlockID365/Qwen3-VL-8B-Instruct-quantized.w4a16`

Served model name: `Qwen/Qwen3-VL-8B-Instruct`

## All-Current

- pack: `human_report_challenge_v2_all_current_117_no101`
- image_count: `{all_summary.get('image_count')}`
- case 101 present: `{decision['fresh_v020c_baseline']['case_101_present']}`
- metrics: `{baseline_record.get('matches')} / {baseline_record.get('false_negatives')} / {baseline_record.get('false_positives')} / {baseline_record.get('combined_errors')}`
- old v020c baseline: `186 / 33 / 25 / 58`
- combined-error delta: `+{baseline_record.get('combined_errors') - 58 if baseline_record.get('combined_errors') is not None else 'n/a'}`

## Controls And Sentinels

- case 67: `{selected_cases['67']['matches']}/{selected_cases['67']['false_negatives']}/{selected_cases['67']['false_positives']}`
- case 155: `{selected_cases['155']['matches']}/{selected_cases['155']['false_negatives']}/{selected_cases['155']['false_positives']}`
- case 166: `{selected_cases['166']['matches']}/{selected_cases['166']['false_negatives']}/{selected_cases['166']['false_positives']}`
- office-negative image_count: `{office_summary.get('image_count')}`
- office-negative passed: `{decision['office_negative']['passed']}`

## Decision

The backend passed stability, but the fresh v020c baseline is too weak for autonomous prompt refinement. The combined error is `91`, which is `+33` over the old v020c baseline and exceeds the user-defined pause threshold of `+20`.
""")
    write_text(PACKAGE_ROOT / "final_recommendation.md", f"""# v029 Final Recommendation

Updated: `{generated_at}`

Decision: `D. stable_backend_found_but_v020c_baseline_unacceptable_pause`

## Summary

v029 successfully launched a non-Ollama local vLLM OpenAI-compatible backend on `localhost:8000/v1` using a public quantized Qwen3-VL 8B derivative. The backend passed the case-67 stability probes and the sentinel stability probes. However, the fresh v020c all-current baseline on this backend was much worse than the old incumbent baseline, so semantic prompt refinement did not resume.

## Backend

- server: `vLLM`
- endpoint: `http://localhost:8000/v1`
- served model name: `Qwen/Qwen3-VL-8B-Instruct`
- actual model root: `SherlockID365/Qwen3-VL-8B-Instruct-quantized.w4a16`
- model source: public HF download/cache, no token or private credential

## Stability

- Stage 1 case-67 stability: passed
- Stage 2 sentinel stability: passed
- case 67 exact replays: `8/3/7`, `8/3/7`, `8/3/7`
- blank-line probes: `9/2/7`, `9/2/8`
- trailing-space probe: `8/3/7`
- no-op roundtrip: `9/2/8`
- sentinel exact replays: `9/2/5`, `9/2/5`
- sentinel blank-line: `9/2/9`
- sentinel trailing-space: `9/2/4`
- sentinel no-op: `9/2/5`

## Fresh v020c Baseline

- old v020c: `186 / 33 / 25 / 58`
- vLLM quantized v020c: `{baseline_record.get('matches')} / {baseline_record.get('false_negatives')} / {baseline_record.get('false_positives')} / {baseline_record.get('combined_errors')}`
- delta: `+{baseline_record.get('combined_errors') - 58 if baseline_record.get('combined_errors') is not None else 'n/a'}` combined errors
- office-negative: passed
- case 155: passed
- case 166: passed

## Recommendation

Do not resume autonomous semantic prompt refinement on this backend. The backend is repeatable enough, but the quantized model baseline is not close enough to the old incumbent behavior to make prompt deltas comparable.

The next fix is either:

- recover a stable non-Ollama backend for the exact `Qwen/Qwen3-VL-8B-Instruct` model on hardware with enough VRAM, or
- test a smaller official Qwen3-VL model as a new model line with its own baseline and expectations, not as a drop-in replacement for the old v020c evidence.

Product v020c remains the incumbent under prior stable evidence. v024l remains learning evidence only, v025a remains rejected, and v024o remains unscored/forbidden.
""")
    write_text(PACKAGE_ROOT / "README.md", """# v029 Stable Non-Ollama Backend Build

Purpose: recover or build a stable non-Ollama Qwen-compatible OpenAI backend, then establish whether v020c remains usable on that backend before any new prompt mutation.

Result: vLLM launched successfully with a public quantized Qwen3-VL 8B derivative and passed stability probes, but the fresh v020c baseline was too weak (`153 / 66 / 25 / 91`) to resume prompt refinement.

No product config, doctrine, assessment prompt, runtime code, eval truth, promotion branch, Graphify memory, Mem0 memory, or semantic prompt candidate was modified.
""")
    write_text(PACKAGE_ROOT / "research_notes.md", """# v029 Research Notes

- vLLM docs show OpenAI-compatible multimodal chat completions with text plus `image_url` content and `response_format` JSON schema support.
  - Source: https://docs.vllm.ai/en/latest/features/multimodal_inputs
  - Source: https://docs.vllm.ai/en/latest/features/structured_outputs
- SGLang docs include Qwen3-VL-8B multimodal launch examples and structured-output examples, but v029 did not attempt SGLang after vLLM launched.
  - Source: https://github.com/sgl-project/sglang
- Hugging Face repo metadata showed `Qwen/Qwen3-VL-8B-Instruct` and `SherlockID365/Qwen3-VL-8B-Instruct-quantized.w4a16` as public, non-gated, Apache-2.0 models.
  - Source: https://hf.co/Qwen/Qwen3-VL-8B-Instruct
  - Source: https://hf.co/SherlockID365/Qwen3-VL-8B-Instruct-quantized.w4a16
""")
    write_text(PACKAGE_ROOT / "recovery_log.md", """# v029 Recovery Log

- Read v028/v027 source evidence and GPT-Pro collaboration directives.
- Inventoried GPU, disk, endpoint status, processes, Python packages, HF cache, and Ollama cache.
- Verified exact Qwen3-VL 8B is public/non-gated but too large for the 16 GB VRAM envelope in BF16.
- Installed vLLM into `/tmp/bda_v029_vllm_env`.
- Launched vLLM with public quantized Qwen3-VL 8B derivative on `localhost:8000/v1`.
- Fixed bda-svc compatibility by allowing two images per prompt.
- Ran case-67 stability, sentinel stability, full v020c all-current baseline, and office-negative guard.
- Stopped semantic prompt refinement because the new backend-specific baseline was `153 / 66 / 25 / 91`.
""")
    write_json(PACKAGE_ROOT / "recovery_log.json", {
        "generated_at": generated_at,
        "events": [
            "inventory_completed",
            "vllm_installed_isolated",
            "quantized_public_model_downloaded_or_cached",
            "vllm_launch_limit1_failed_assessment_two_image_shape",
            "vllm_launch_limit2_passed_request_shape",
            "case67_stability_passed",
            "sentinel_stability_passed",
            "full_v020c_baseline_completed",
            "office_negative_completed",
            "semantic_prompt_refinement_not_resumed_due_baseline_delta",
        ],
    })
    write_text(PACKAGE_ROOT / "backend_stability_matrix.md", "\n".join([
        "# v029 Backend Stability Matrix",
        "",
        "| Candidate | Stage | Case 67 | Status | Rendered Prompt Hash | Request Shape Hash |",
        "| --- | --- | --- | --- | --- | --- |",
        *[
            f"| `{r.get('candidate_id')}` | `{r.get('stage')}` | `{r.get('case_67')}` | `{r.get('status')}` | `{r.get('rendered_prompt_hash')}` | `{r.get('request_shape_hash')}` |"
            for r in stage_records
        ],
        f"| `v020c_vllm_quantized_baseline` | `full_v020c_baseline` | `{baseline_record.get('case_67')}` | `baseline_completed` | `{baseline_record.get('rendered_prompt_hash')}` | `{baseline_record.get('request_shape_hash')}` |",
    ]))
    write_text(PACKAGE_ROOT / "diagnoses/v029_baseline_unacceptable_diagnosis.md", """# v029 Baseline Unacceptable Diagnosis

The vLLM backend stabilized the request surface, but the served quantized model does not reproduce the old v020c all-current baseline closely enough.

- Prior v020c: `186 / 33 / 25 / 58`
- v029 vLLM quantized v020c: `153 / 66 / 25 / 91`
- Delta: `+33` combined errors

This exceeds the user-defined pause threshold of `+20` combined errors. Because the baseline is model/backend-specific, prompt engineering on this backend would optimize a different model behavior profile and should not be treated as a continuation of the old Qwen v020c line.
""")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
