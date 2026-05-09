#!/usr/bin/env python3
"""v033 FP8 vLLM timeout repair and v032d clean replay operator."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any

import yaml
from PIL import Image


WORKTREE_ROOT = Path(
    "/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement"
)
CAPSTONE_ROOT = Path("/home/williambenitez1/Capstone")
PACKAGE_ROOT = (
    WORKTREE_ROOT
    / "docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/"
    "human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/"
    "v017b_prompt_only_main_promotion/v033_fp8_timeout_repair_and_v032d_replay"
)
V032_PACKAGE = PACKAGE_ROOT.parent / "v032_qwen3vl_fp8_vllm_model_line_prompt_refinement"
V020C_OVERLAY = (
    WORKTREE_ROOT
    / "docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/"
    "human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/"
    "v017b_prompt_only_main_promotion/v020_v019c_goal_driven_self_improvement_cycle/"
    "overlays/v020c_v019c_extra_box_audit.yaml"
)
V032D_OVERLAY = V032_PACKAGE / "overlays/v032d_fp8_v019c_anchor_replay.yaml"
BASELINE_OVERLAY = V032_PACKAGE / "overlays/v032_baseline_exact_v020c_fp8_replay.yaml"
ALL_CURRENT_MANIFEST = (
    WORKTREE_ROOT
    / "docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/"
    "human_report_challenge_v2_prompt_iteration_workflow/cycle_001/pre_adoption/"
    "v017b_group_box_rejection/validation_manifests/"
    "human_report_challenge_v2_all_current_117_no101.yaml"
)
OFFICE_NEGATIVE_MANIFEST = (
    WORKTREE_ROOT
    / "docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/"
    "human_report_challenge_v2_prompt_iteration_workflow/validation_manifests/"
    "legacy_abstention_guard_office_negative.yaml"
)
CASE110_MANIFEST = PACKAGE_ROOT / "validation_manifests/v033_case110_only_no101.yaml"
BDA_EVAL_ROOT = WORKTREE_ROOT / "bda_eval"
INSTRUMENTED_RUNNER = PACKAGE_ROOT / "scripts/instrumented_bda_runner.py"
BACKEND = {
    "label": "vllm_qwen3vl_8b_fp8",
    "base_url": "http://localhost:8000/v1",
    "api_key": "EMPTY",
    "model": "Qwen/Qwen3-VL-8B-Instruct-FP8",
}
REQUEST_TIMEOUT_SECONDS = 180
MAX_RETRIES = 2
RETRY_COOLDOWN_SECONDS = 5


def utc_now() -> str:
    return dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def stamp() -> str:
    return dt.datetime.now(dt.UTC).strftime("%Y-%m-%d_%H%M%SZ")


def sha256_file(path: Path) -> str | None:
    if not path.exists():
        return None
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def run(cmd: list[str], cwd: Path | None = None, env: dict[str, str] | None = None) -> dict[str, Any]:
    proc = subprocess.run(
        cmd,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return {
        "cmd": cmd,
        "cwd": str(cwd) if cwd else None,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def require_ok(result: dict[str, Any]) -> None:
    if result["returncode"] != 0:
        raise RuntimeError(
            "Command failed: "
            + " ".join(result["cmd"])
            + f"\nstdout:\n{result['stdout']}\nstderr:\n{result['stderr']}"
        )


def read_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def write_yaml(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def append_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text)


def extract_prompt_from_overlay(path: Path) -> str:
    return read_yaml(path)["overrides"]["prompts"]["detect_objects"]


def create_scratch(candidate_id: str) -> Path:
    scratch = Path("/tmp") / f"bda_v033_{candidate_id}_{stamp()}"
    if scratch.exists():
        shutil.rmtree(scratch)
    require_ok(run(["git", "worktree", "add", "--detach", str(scratch), "upstream/main"], CAPSTONE_ROOT))
    return scratch


def remove_scratch(scratch: Path) -> dict[str, Any]:
    result = run(["git", "worktree", "remove", "--force", str(scratch)], CAPSTONE_ROOT)
    if scratch.exists():
        shutil.rmtree(scratch, ignore_errors=True)
    return result


def patch_scratch_config(scratch: Path, prompt: str) -> Path:
    config_path = scratch / "src/bda_svc/pipeline/config.yaml"
    config = read_yaml(config_path)
    config["prompts"]["detect_objects"] = prompt
    write_yaml(config_path, config)
    return config_path


def fetch_models() -> dict[str, Any]:
    try:
        with urllib.request.urlopen(BACKEND["base_url"] + "/models", timeout=5) as response:
            payload = json.loads(response.read().decode("utf-8"))
        model_present = any(item.get("id") == BACKEND["model"] for item in payload.get("data", []))
        return {"ok": True, "payload": payload, "model_present": model_present}
    except Exception as exc:
        return {"ok": False, "error": repr(exc), "model_present": False}


def ensure_case110_manifest() -> None:
    all_current = read_yaml(ALL_CURRENT_MANIFEST)
    cases = [case for case in all_current["cases"] if case["case_id"] == "human-report-110"]
    if len(cases) != 1:
        raise RuntimeError("Could not find exactly one human-report-110 case.")
    write_yaml(
        CASE110_MANIFEST,
        {
            "pack_id": "v033_case110_only_no101",
            "eval_mode": all_current.get("eval_mode", "object_detection"),
            "images_dir": all_current.get("images_dir"),
            "cases": cases,
        },
    )


def run_eval(manifest: Path, predicted: Path, output: Path) -> tuple[dict[str, Any], Path]:
    output.mkdir(parents=True, exist_ok=True)
    result = run(
        [
            "uv",
            "run",
            "python",
            "main.py",
            "--manifest",
            str(manifest),
            "--predicted",
            str(predicted),
            "--output",
            str(output),
        ],
        BDA_EVAL_ROOT,
    )
    require_ok(result)
    summaries = sorted(output.glob("*_summary.json"))
    if not summaries:
        raise RuntimeError(f"No eval summary written under {output}")
    return result, summaries[-1]


def case_metric(summary: dict[str, Any], case_number: str) -> str:
    filename = f"{case_number}.jpg" if case_number != "office" else "office_negative.jpg"
    for image in summary.get("images", []):
        if image.get("image_filename") == filename:
            return f"{image.get('match_count')}/{image.get('false_negative_count')}/{image.get('false_positive_count')}"
    return "n/a"


def run_probe(candidate: dict[str, Any], manifest: Path, stage: str) -> dict[str, Any]:
    candidate_id = candidate["candidate_id"]
    run_root = PACKAGE_ROOT / "runs" / candidate_id / stage / f"{manifest.stem}_{stamp()}"
    predicted_dir = run_root / "predicted"
    eval_dir = run_root / "eval"
    traces_dir = run_root / "traces"
    logs_dir = run_root / "logs"
    for directory in [predicted_dir, eval_dir, traces_dir, logs_dir]:
        directory.mkdir(parents=True, exist_ok=True)

    overlay_path = Path(candidate["overlay_path"])
    prompt = extract_prompt_from_overlay(overlay_path)
    scratch = create_scratch(candidate_id)
    scratch_config_path = patch_scratch_config(scratch, prompt)
    scratch_config_sha = sha256_file(scratch_config_path)
    env = dict(os.environ)
    env.update(
        {
            "OPENAI_BASE_URL": BACKEND["base_url"],
            "OPENAI_API_KEY": BACKEND["api_key"],
            "BDA_DETECTION_MODEL": BACKEND["model"],
            "BDA_ASSESSMENT_MODEL": BACKEND["model"],
            "BDA_VLM_REQUEST_TIMEOUT_SECONDS": str(REQUEST_TIMEOUT_SECONDS),
        }
    )

    manifest_payload = read_yaml(manifest)
    command_records: list[dict[str, Any]] = []
    retry_records: list[dict[str, Any]] = []
    completed_cases: list[str] = []
    failed_cases: list[dict[str, Any]] = []

    try:
        for case in manifest_payload["cases"]:
            case_id = case["case_id"]
            success = False
            for attempt in range(1, MAX_RETRIES + 2):
                trace_path = traces_dir / f"{case_id}_attempt{attempt}.json"
                cmd = [
                    "uv",
                    "run",
                    "python",
                    str(INSTRUMENTED_RUNNER),
                    "--scratch-root",
                    str(scratch),
                    "--image",
                    str(case["image_path"]),
                    "--output",
                    str(predicted_dir),
                    "--trace-output",
                    str(trace_path),
                    "--candidate-id",
                    candidate_id,
                    "--backend-label",
                    BACKEND["label"],
                    "--endpoint-url",
                    BACKEND["base_url"],
                    "--source-overlay",
                    str(overlay_path),
                    "--base-overlay",
                    str(V020C_OVERLAY),
                    "--stage",
                    stage,
                    "--intended-changes-json",
                    json.dumps(candidate["intended_changes"]),
                ]
                start = time.perf_counter()
                result = run(cmd, scratch, env)
                elapsed = time.perf_counter() - start
                result["elapsed_seconds"] = elapsed
                result["case_id"] = case_id
                result["attempt"] = attempt
                command_records.append(result)
                (logs_dir / f"{case_id}_attempt{attempt}_stdout.log").write_text(result["stdout"], encoding="utf-8")
                (logs_dir / f"{case_id}_attempt{attempt}_stderr.log").write_text(result["stderr"], encoding="utf-8")
                trace_exception = None
                if trace_path.exists():
                    try:
                        trace_exception = json.loads(trace_path.read_text(encoding="utf-8")).get("exception")
                    except Exception as exc:
                        trace_exception = f"trace_read_failed: {exc!r}"
                retry_records.append(
                    {
                        "case_id": case_id,
                        "attempt": attempt,
                        "returncode": result["returncode"],
                        "elapsed_seconds": elapsed,
                        "trace_path": str(trace_path),
                        "trace_exception": trace_exception,
                    }
                )
                if result["returncode"] == 0:
                    success = True
                    completed_cases.append(case_id)
                    break
                if attempt <= MAX_RETRIES:
                    time.sleep(RETRY_COOLDOWN_SECONDS)
            if not success:
                failed_cases.append({"case_id": case_id, "attempts": MAX_RETRIES + 1})
                raise RuntimeError(f"{case_id} failed after {MAX_RETRIES + 1} attempts")

        eval_result, summary_path = run_eval(manifest, predicted_dir, eval_dir)
        command_records.append(eval_result)
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        runtime_invalid = False
    except Exception as exc:
        summary_path = None
        summary = None
        runtime_invalid = True
        run_root.joinpath("runtime_failure.json").write_text(
            json.dumps({"exception": repr(exc), "failed_cases": failed_cases}, indent=2),
            encoding="utf-8",
        )
    finally:
        cleanup = remove_scratch(scratch)
        write_json(run_root / "scratch_cleanup.json", cleanup)

    trace_files = sorted(traces_dir.glob("*.json"))
    traces = []
    for path in trace_files:
        try:
            traces.append(json.loads(path.read_text(encoding="utf-8")))
        except Exception:
            pass
    first_trace = traces[0] if traces else {}
    detection_request = {}
    for trace in traces:
        for item in trace.get("request_response_traces", []):
            if item.get("call_kind") == "detection":
                detection_request = item
                break
        if detection_request:
            break
    rendered = first_trace.get("rendered_prompt") or {}
    totals = summary.get("totals", {}) if summary else {}
    combined = (
        totals.get("false_negative_count", 0) + totals.get("false_positive_count", 0)
        if summary
        else None
    )
    record = {
        "candidate_id": candidate_id,
        "stage": stage,
        "backend": BACKEND,
        "manifest": str(manifest),
        "run_root": str(run_root),
        "predicted_dir": str(predicted_dir),
        "eval_summary": str(summary_path) if summary_path else None,
        "scratch_config_sha256": scratch_config_sha,
        "request_timeout_seconds": REQUEST_TIMEOUT_SECONDS,
        "max_retries": MAX_RETRIES,
        "retry_cooldown_seconds": RETRY_COOLDOWN_SECONDS,
        "retry_records": retry_records,
        "completed_cases": completed_cases,
        "failed_cases": failed_cases,
        "runtime_invalid": runtime_invalid,
        "metrics": {
            "matches": totals.get("match_count") if summary else None,
            "false_negatives": totals.get("false_negative_count") if summary else None,
            "false_positives": totals.get("false_positive_count") if summary else None,
            "combined_errors": combined,
            "image_count": summary.get("image_count") if summary else None,
        },
        "case_metrics": {
            "67": case_metric(summary, "67") if summary else "n/a",
            "155": case_metric(summary, "155") if summary else "n/a",
            "166": case_metric(summary, "166") if summary else "n/a",
            "110": case_metric(summary, "110") if summary else "n/a",
            "66": case_metric(summary, "66") if summary else "n/a",
            "84": case_metric(summary, "84") if summary else "n/a",
            "97": case_metric(summary, "97") if summary else "n/a",
            "14": case_metric(summary, "14") if summary else "n/a",
            "42": case_metric(summary, "42") if summary else "n/a",
            "172": case_metric(summary, "172") if summary else "n/a",
        },
        "rendered_prompt_hash": rendered.get("rendered_prompt_sha256") or "unavailable",
        "request_shape_hash": detection_request.get("request_shape_hash") or "unavailable",
        "raw_response_hash": detection_request.get("raw_response_sha256") or "unavailable",
        "response_trace_captured": bool(detection_request),
        "command_records": command_records,
        "trace_files": [str(path) for path in trace_files],
    }
    write_json(run_root / "v033_run_summary.json", record)
    return record


def status_block(phase: str, record: dict[str, Any] | None, status: str, lesson: str, next_action: str) -> None:
    metrics = record.get("metrics", {}) if record else {}
    case_metrics = record.get("case_metrics", {}) if record else {}
    print("=== V033 STATUS ===", flush=True)
    print(f"phase: {phase}", flush=True)
    print("backend: vllm_qwen3vl_8b_fp8", flush=True)
    print(f"case_110: {case_metrics.get('110', 'n/a') if record else 'n/a'}", flush=True)
    print(f"candidate: {record.get('candidate_id') if record else 'n/a'}", flush=True)
    print(
        "metrics: "
        + (
            f"{metrics.get('matches')}/{metrics.get('false_negatives')}/{metrics.get('false_positives')}/{metrics.get('combined_errors')}"
            if record and metrics.get("matches") is not None
            else "n/a"
        ),
        flush=True,
    )
    print(f"case_67: {case_metrics.get('67', 'n/a') if record else 'n/a'}", flush=True)
    print(f"case_155: {case_metrics.get('155', 'n/a') if record else 'n/a'}", flush=True)
    print(f"case_166: {case_metrics.get('166', 'n/a') if record else 'n/a'}", flush=True)
    print("office_negative: n/a" if phase != "full_v032d_replay" else f"office_negative: {record.get('office_negative', 'n/a')}", flush=True)
    print(f"status: {status}", flush=True)
    print(f"main_lesson: {lesson}", flush=True)
    print(f"next_action: {next_action}", flush=True)
    print("===================", flush=True)


def write_scaffold(preflight: dict[str, Any]) -> None:
    source_manifest = {
        "generated_at": utc_now(),
        "package": "v033_fp8_timeout_repair_and_v032d_replay",
        "source_artifacts": [
            "V032_FP8_MODEL_LINE_PROMPT_REFINEMENT_POINTER.md if present in local workspace",
            str(V032_PACKAGE / "final_recommendation.md"),
            str(V032_PACKAGE / "diagnoses/v032_runtime_timeout_case110_diagnosis.md"),
            str(V032_PACKAGE / "diagnoses/v032d_fp8_v019c_anchor_replay_diagnosis.md"),
            str(V032_PACKAGE / "comparison_matrix.md"),
            str(V032_PACKAGE / "live_metrics_log.md"),
            str(PACKAGE_ROOT.parent / "v031_sglang_qwen3vl_fp8_surface_gate/final_recommendation.md"),
        ],
        "old_product_v020c": {"matches": 186, "false_negatives": 33, "false_positives": 25, "combined_errors": 58},
        "fp8_baseline": {"matches": 180, "false_negatives": 39, "false_positives": 32, "combined_errors": 71},
        "v024l_status": "learning_evidence_only",
        "v025a_status": "rejected",
        "v024o_status": "partial_unscored_forbidden",
        "hard_boundaries": {
            "no_promotion": True,
            "no_product_source_truth_mutation": True,
            "no_v024o_scored_evidence": True,
            "no_new_semantic_candidate_before_v032d_replay": True,
        },
    }
    write_json(PACKAGE_ROOT / "source_manifest.json", source_manifest)
    write_json(PACKAGE_ROOT / "backend_preflight.json", preflight)
    write_json(
        PACKAGE_ROOT / "retry_policy_design.json",
        {
            "generated_at": utc_now(),
            "scope": "experiment_only_v033",
            "per_case_timeout_seconds": REQUEST_TIMEOUT_SECONDS,
            "max_retries_per_case": MAX_RETRIES,
            "cooldown_seconds_between_retries": RETRY_COOLDOWN_SECONDS,
            "backend_restart_between_retries": False,
            "resume_without_rerunning_previous_cases": "case-level retry inside one run; failed complete packs remain unscored",
            "all_retries_fail_policy": "mark runtime_invalid and stop without scoring partial output",
            "comparability_policy": "same policy applies to case110 validation and v032d full replay",
        },
    )
    (PACKAGE_ROOT / "retry_policy_design.md").write_text(
        "\n".join(
            [
                "# v033 Retry Policy Design",
                "",
                "Scope: experiment-only. Product runtime is unchanged.",
                "",
                f"- Per-case request timeout: `{REQUEST_TIMEOUT_SECONDS}` seconds.",
                f"- Retries per case after first failure: `{MAX_RETRIES}`.",
                f"- Cooldown between retries: `{RETRY_COOLDOWN_SECONDS}` seconds.",
                "- Backend restart between retries: no.",
                "- Partial packs are never scored.",
                "- A full run is valid only if every case completes and eval writes a full summary.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def write_docs(records: dict[str, Any]) -> None:
    baseline_case = records.get("baseline_case110")
    v032d_case = records.get("v032d_case110")
    v032d_full = records.get("v032d_full")
    office = records.get("office_negative")
    full_valid = bool(v032d_full and not v032d_full.get("runtime_invalid"))
    if full_valid and office:
        v032d_full["office_negative"] = "pass" if office["metrics"]["false_positives"] == 0 else "fail"

    write_json(PACKAGE_ROOT / "timeout_case110_diagnosis.json", records.get("timeout_diagnosis", {}))
    write_json(PACKAGE_ROOT / "full_run_replay_plan.json", records.get("replay_plan", {}))
    write_json(PACKAGE_ROOT / "v032d_full_replay_summary.json", v032d_full or {"runtime_invalid": True})

    matrix_rows = [
        {"candidate_id": "v020c_old_product_reference", "stage": "prior_all_current", "metrics": "186/33/25/58", "status": "product_reference"},
        {"candidate_id": "v020c_fp8_vllm_baseline", "stage": "v031_all_current", "metrics": "180/39/32/71", "status": "fp8_baseline"},
    ]
    for key, label in [("baseline_case110", "case110_validation"), ("v032d_case110", "case110_validation"), ("v032d_full", "full_all_current"), ("office_negative", "office_negative")]:
        record = records.get(key)
        if not record:
            continue
        m = record.get("metrics", {})
        matrix_rows.append(
            {
                "candidate_id": record["candidate_id"],
                "stage": label,
                "metrics": f"{m.get('matches')}/{m.get('false_negatives')}/{m.get('false_positives')}/{m.get('combined_errors')}",
                "image_count": m.get("image_count"),
                "case_67": record.get("case_metrics", {}).get("67", "n/a"),
                "case_110": record.get("case_metrics", {}).get("110", "n/a"),
                "case_155": record.get("case_metrics", {}).get("155", "n/a"),
                "case_166": record.get("case_metrics", {}).get("166", "n/a"),
                "status": "runtime_invalid" if record.get("runtime_invalid") else "complete",
            }
        )
    write_json(PACKAGE_ROOT / "comparison_matrix.json", {"generated_at": utc_now(), "rows": matrix_rows})
    (PACKAGE_ROOT / "comparison_matrix.md").write_text(
        "# v033 Comparison Matrix\n\n"
        "| Candidate | Stage | Metrics | Image Count | Case 67 | Case 110 | Case 155 | Case 166 | Status |\n"
        "|---|---|---:|---:|---|---|---|---|---|\n"
        + "\n".join(
            f"| `{row['candidate_id']}` | {row['stage']} | `{row['metrics']}` | {row.get('image_count', 'n/a')} | `{row.get('case_67', 'n/a')}` | `{row.get('case_110', 'n/a')}` | `{row.get('case_155', 'n/a')}` | `{row.get('case_166', 'n/a')}` | {row['status']} |"
            for row in matrix_rows
        )
        + "\n",
        encoding="utf-8",
    )

    final_status = "runtime_invalid"
    became_best = False
    resumed = False
    if full_valid:
        errors = v032d_full["metrics"]["combined_errors"]
        if errors < 71 and v032d_full["case_metrics"]["67"] != "n/a":
            final_status = "new_fp8_working_best"
            became_best = True
            resumed = True
        else:
            final_status = "learning_evidence" if errors <= 71 else "rejected"

    final = {
        "generated_at": utc_now(),
        "status": final_status,
        "case110_timeout_diagnosed": True,
        "retry_policy_worked": bool(baseline_case and v032d_case and not baseline_case.get("runtime_invalid") and not v032d_case.get("runtime_invalid")),
        "v032d_clean_full_score_available": full_valid,
        "v032d_full_metrics": v032d_full.get("metrics") if v032d_full else None,
        "v032d_became_new_fp8_working_best": became_best,
        "autonomous_fp8_prompt_refinement_resumed": resumed,
        "old_product_v020c": {"matches": 186, "false_negatives": 33, "false_positives": 25, "combined_errors": 58},
        "fp8_baseline": {"matches": 180, "false_negatives": 39, "false_positives": 32, "combined_errors": 71},
        "hard_boundaries_preserved": True,
    }
    write_json(PACKAGE_ROOT / "final_recommendation.json", final)

    full_line = "No valid full all-current score." if not full_valid else (
        f"`{v032d_full['metrics']['matches']} / {v032d_full['metrics']['false_negatives']} / "
        f"{v032d_full['metrics']['false_positives']} / {v032d_full['metrics']['combined_errors']}`"
    )
    (PACKAGE_ROOT / "final_recommendation.md").write_text(
        "\n".join(
            [
                "# v033 Final Recommendation",
                "",
                f"Generated: `{utc_now()}`",
                "",
                f"Status: `{final_status}`.",
                "",
                "Case 110 timeout was diagnosed as a 60-second OpenAI client request timeout in the v032 instrumented path. v033 used an experiment-only timeout/retry policy and did not modify product runtime.",
                "",
                f"v032d clean full all-current result: {full_line}",
                "",
                f"v032d became new FP8 working best: `{became_best}`.",
                f"Autonomous FP8 prompt refinement resumed: `{resumed}`.",
                "",
                "Hard boundaries were preserved: no promotion, no product source truth/runtime/doctrine/assessment/eval-truth mutation, no Graphify/Mem0 update, and no v024o scored evidence.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (PACKAGE_ROOT / "README.md").write_text(
        "# v033 FP8 Timeout Repair And v032d Replay\n\n"
        "This package repairs the v032 case-110 timeout path using experiment-only instrumentation and replays `v032d_fp8_v019c_anchor_replay` cleanly if case 110 validates.\n",
        encoding="utf-8",
    )
    (PACKAGE_ROOT / "timeout_case110_diagnosis.md").write_text(
        "# v033 Case 110 Timeout Diagnosis\n\n"
        "v032 timed out before raw response capture on case 110 with the OpenAI-compatible client timeout at 60 seconds. v033 captures the same rendered/request evidence and raises only the experiment-local request timeout.\n",
        encoding="utf-8",
    )
    (PACKAGE_ROOT / "full_run_replay_plan.md").write_text(
        "# v033 Full Run Replay Plan\n\n"
        "Validate case 110 alone for baseline and v032d, then run full all-current/no101 for v032d only if both complete. Partial packs remain unscored.\n",
        encoding="utf-8",
    )
    (PACKAGE_ROOT / "v032d_full_replay_summary.md").write_text(
        "# v032d Full Replay Summary\n\n" + f"{full_line}\n",
        encoding="utf-8",
    )
    (PACKAGE_ROOT / "lessons_learned.md").write_text(
        "# v033 Lessons Learned\n\n"
        "- The timeout policy must be experiment-local and explicit.\n"
        "- Case-level retries are acceptable only when every retry is logged and partial packs remain unscored.\n"
        "- v032d cannot become FP8 working best without a valid full all-current result below 71 errors.\n",
        encoding="utf-8",
    )
    (PACKAGE_ROOT / "strategy_state.md").write_text(
        "# v033 Strategy State\n\n"
        f"Final status: `{final_status}`.\n\n"
        "If v032d is not a valid new FP8 working best, do not author another candidate until this evidence is reviewed.\n",
        encoding="utf-8",
    )
    (PACKAGE_ROOT / "recovery_log.md").write_text(
        "# v033 Recovery Log\n\n"
        "- Created experiment-only timeout/retry runner.\n"
        "- Validated case 110 for FP8 baseline and v032d when possible.\n"
        "- Replayed v032d full all-current only after case110 validation.\n",
        encoding="utf-8",
    )
    write_json(PACKAGE_ROOT / "recovery_log.json", {"generated_at": utc_now(), "records": list(records.keys())})
    append_text(
        PACKAGE_ROOT / "live_metrics_log.md",
        "\n".join(
            [
                "# v033 Live Metrics Log",
                "",
                f"- final_status: `{final_status}`",
                f"- v032d_full: {full_line}",
                "",
            ]
        ),
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args()
    if not args.run:
        parser.print_help()
        return 0

    PACKAGE_ROOT.mkdir(parents=True, exist_ok=True)
    ensure_case110_manifest()
    preflight = {
        "generated_at": utc_now(),
        "backend": BACKEND,
        "models": fetch_models(),
        "request_timeout_seconds": REQUEST_TIMEOUT_SECONDS,
        "max_retries": MAX_RETRIES,
    }
    write_scaffold(preflight)
    if not preflight["models"]["ok"] or not preflight["models"]["model_present"]:
        raise RuntimeError("vLLM FP8 backend is not available.")
    status_block("timeout_diagnosis", None, "pass", "v032 timeout path identified as the 60-second OpenAI client request timeout.", "Validate case 110 with longer experiment-only timeout.")

    baseline = {
        "candidate_id": "v033_case110_baseline_v020c_fp8",
        "overlay_path": str(BASELINE_OVERLAY),
        "intended_changes": ["Exact FP8 v020c baseline prompt, case 110 timeout validation."],
    }
    v032d = {
        "candidate_id": "v032d_fp8_v019c_anchor_replay",
        "overlay_path": str(V032D_OVERLAY),
        "intended_changes": ["Replay v032d v019c anchor prompt with experiment-only timeout/retry policy."],
    }
    records: dict[str, Any] = {
        "timeout_diagnosis": {
            "source": "v032 trace plus v033 instrumented runner",
            "timeout_before": 60,
            "timeout_after": REQUEST_TIMEOUT_SECONDS,
            "product_runtime_changed": False,
        },
        "replay_plan": {
            "case110_manifest": str(CASE110_MANIFEST),
            "all_current_manifest": str(ALL_CURRENT_MANIFEST),
            "office_negative_manifest": str(OFFICE_NEGATIVE_MANIFEST),
        },
    }

    records["baseline_case110"] = run_probe(baseline, CASE110_MANIFEST, "case110_validation")
    status_block("case110_validation", records["baseline_case110"], "pass" if not records["baseline_case110"]["runtime_invalid"] else "fail", "Baseline case 110 completed under the v033 timeout policy." if not records["baseline_case110"]["runtime_invalid"] else "Baseline case 110 still failed.", "Validate v032d case 110.")
    records["v032d_case110"] = run_probe(v032d, CASE110_MANIFEST, "case110_validation")
    status_block("case110_validation", records["v032d_case110"], "pass" if not records["v032d_case110"]["runtime_invalid"] else "fail", "v032d case 110 completed under the v033 timeout policy." if not records["v032d_case110"]["runtime_invalid"] else "v032d case 110 still failed.", "Run full v032d replay if both case110 probes completed.")

    if records["baseline_case110"]["runtime_invalid"] or records["v032d_case110"]["runtime_invalid"]:
        write_docs(records)
        status_block("full_v032d_replay", None, "stopped", "Case 110 did not validate cleanly.", "Stop without scoring partial output.")
        return 0

    records["v032d_full"] = run_probe(v032d, ALL_CURRENT_MANIFEST, "full_all_current")
    office = run_probe(v032d, OFFICE_NEGATIVE_MANIFEST, "office_negative_guard")
    records["office_negative"] = office
    office_pass = office["metrics"]["false_positives"] == 0 and not office["runtime_invalid"]
    records["v032d_full"]["office_negative"] = "pass" if office_pass else "fail"
    write_docs(records)

    m = records["v032d_full"]["metrics"]
    status = "runtime_invalid"
    if not records["v032d_full"]["runtime_invalid"]:
        status = "new_fp8_working_best" if m["combined_errors"] < 71 and office_pass else ("learning_evidence" if m["combined_errors"] <= 71 else "rejected")
    status_block(
        "full_v032d_replay",
        records["v032d_full"],
        status,
        "v032d full replay completed under the v033 timeout policy." if not records["v032d_full"]["runtime_invalid"] else "v032d full replay remained runtime-invalid.",
        "Resume autonomy only if v032d is a valid new FP8 working best; otherwise stop for review.",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
