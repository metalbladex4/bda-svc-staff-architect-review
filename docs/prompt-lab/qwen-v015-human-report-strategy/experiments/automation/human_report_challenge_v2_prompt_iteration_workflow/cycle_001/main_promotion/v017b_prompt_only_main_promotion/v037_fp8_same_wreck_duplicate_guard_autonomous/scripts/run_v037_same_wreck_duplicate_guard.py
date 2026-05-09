#!/usr/bin/env python3
"""v037 FP8 vLLM same-wreck duplicate guard prompt-refinement operator."""

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


WORKTREE_ROOT = Path("/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement")
CAPSTONE_ROOT = Path("/home/williambenitez1/Capstone")
PACKAGE_ROOT = WORKTREE_ROOT / (
    "docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/"
    "human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/"
    "v017b_prompt_only_main_promotion/v037_fp8_same_wreck_duplicate_guard_autonomous"
)
V032_PACKAGE = PACKAGE_ROOT.parent / "v032_qwen3vl_fp8_vllm_model_line_prompt_refinement"
V033_PACKAGE = PACKAGE_ROOT.parent / "v033_fp8_timeout_repair_and_v032d_replay"
V034_PACKAGE = PACKAGE_ROOT.parent / "v034_fp8_vllm_precision_recovery_autonomous"
BASELINE_OVERLAY = V034_PACKAGE / "overlays/v034a_fp8_broad_context_scene_box_guard.yaml"
V020C_OVERLAY = (
    WORKTREE_ROOT
    / "docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/"
    "human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/"
    "v017b_prompt_only_main_promotion/v020_v019c_goal_driven_self_improvement_cycle/"
    "overlays/v020c_v019c_extra_box_audit.yaml"
)
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
SENTINEL_MANIFEST = PACKAGE_ROOT / "validation_manifests/v037_fp8_sentinel_with_110_no101.yaml"
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
FP8_BASELINE_ERRORS = 71
V034A_ERRORS = 63
OLD_V020C_ERRORS = 58


def utc_now() -> str:
    return dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def stamp() -> str:
    return dt.datetime.now(dt.UTC).strftime("%Y-%m-%d_%H%M%SZ")


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
    return {"cmd": cmd, "cwd": str(cwd) if cwd else None, "returncode": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr}


def require_ok(result: dict[str, Any]) -> None:
    if result["returncode"] != 0:
        raise RuntimeError("Command failed: " + " ".join(result["cmd"]) + f"\nstdout:\n{result['stdout']}\nstderr:\n{result['stderr']}")


def read_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def write_yaml(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str | None:
    if not path.exists():
        return None
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def extract_prompt_from_overlay(path: Path) -> str:
    return read_yaml(path)["overrides"]["prompts"]["detect_objects"]


def fetch_models() -> dict[str, Any]:
    try:
        with urllib.request.urlopen(BACKEND["base_url"] + "/models", timeout=5) as response:
            payload = json.loads(response.read().decode("utf-8"))
        return {"ok": True, "payload": payload, "model_present": any(item.get("id") == BACKEND["model"] for item in payload.get("data", []))}
    except Exception as exc:
        return {"ok": False, "error": repr(exc), "model_present": False}


def create_sentinel_manifest() -> None:
    wanted = {f"human-report-{n}" for n in [12, 14, 16, 42, 66, 67, 77, 84, 88, 90, 97, 103, 110, 155, 166, 172]}
    all_current = read_yaml(ALL_CURRENT_MANIFEST)
    cases = [case for case in all_current["cases"] if case["case_id"] in wanted]
    found = {case["case_id"] for case in cases}
    missing = sorted(wanted - found)
    if missing:
        raise RuntimeError(f"Missing sentinel cases: {missing}")
    write_yaml(
        SENTINEL_MANIFEST,
        {
            "pack_id": "v037_fp8_sentinel_with_110_no101",
            "eval_mode": all_current.get("eval_mode", "object_detection"),
            "images_dir": all_current.get("images_dir"),
            "cases": cases,
        },
    )


def create_candidate_overlay() -> Path:
    baseline = read_yaml(BASELINE_OVERLAY)
    prompt = baseline["overrides"]["prompts"]["detect_objects"]
    needle = (
        "- broad context or scene boxes whose strongest support is a row, blast area, road, debris field, "
        "smoke plume, or multiple uncertain fragments rather than one visible target body\n"
    )
    addition = (
        "- smaller duplicate box nested inside or heavily overlapping the same visible wreck/body already covered by a tighter whole-body box\n"
    )
    if addition.strip() in prompt:
        candidate_prompt = prompt
    else:
        candidate_prompt = prompt.replace(needle, needle + addition)
    candidate = dict(baseline)
    candidate["candidate_id"] = "v037a_fp8_same_wreck_duplicate_local_guard"
    candidate["title"] = "v037a fp8 same-wreck duplicate local guard"
    candidate["overlay_id"] = "qwen-1.2-v037a_fp8_same_wreck_duplicate_local_guard"
    candidate["overlay_type"] = "fp8_vllm_same_wreck_duplicate_guard"
    candidate["description"] = "Narrow case-155-style same-wreck duplicate/local-context guard while preserving v034a and the v020c extra-box audit."
    candidate["generated_from"] = ["v034a_fp8_broad_context_scene_box_guard"]
    candidate["intended_changes"] = [
        "Add one compact BAD FINAL BOX guard for smaller duplicate boxes nested inside or heavily overlapping the same visible wreck/body already covered by a tighter whole-body box.",
        "Preserve the v034a broad-context/scene-box guard.",
        "Preserve the v020c extra-box audit without weakening or removing it.",
        "Avoid adding dense-scene, partial-fragment, uncertain-fragment, isolated-mark, body-center, or exterior-boundary language.",
    ]
    candidate["overrides"]["prompts"]["detect_objects"] = candidate_prompt
    candidate["overrides"]["runtime"] = {"notes": "Applied only inside upstream/main scratch config; no product adoption."}
    out = PACKAGE_ROOT / "overlays/v037a_fp8_same_wreck_duplicate_local_guard.yaml"
    write_yaml(out, candidate)
    return out


def create_baseline_overlay_copy() -> Path:
    payload = read_yaml(BASELINE_OVERLAY)
    payload["candidate_id"] = "v037_baseline_exact_v034a_replay"
    payload["title"] = "v037 baseline exact v034a replay"
    payload["overlay_id"] = "qwen-1.2-v037_baseline_exact_v034a_replay"
    payload["overlay_type"] = "fp8_vllm_gap_closure"
    payload["description"] = "Exact FP8 v034a working-best replay for v037 sentinel verification."
    payload["intended_changes"] = []
    out = PACKAGE_ROOT / "overlays/v037_baseline_exact_v034a_replay.yaml"
    write_yaml(out, payload)
    return out


def create_scratch(candidate_id: str) -> Path:
    scratch = Path("/tmp") / f"bda_v037_{candidate_id}_{stamp()}"
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


def run_eval(manifest: Path, predicted: Path, output: Path) -> tuple[dict[str, Any], Path]:
    output.mkdir(parents=True, exist_ok=True)
    result = run(["uv", "run", "python", "main.py", "--manifest", str(manifest), "--predicted", str(predicted), "--output", str(output)], BDA_EVAL_ROOT)
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
                    json.dumps(candidate.get("intended_changes", [])),
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
                retry_records.append({"case_id": case_id, "attempt": attempt, "returncode": result["returncode"], "elapsed_seconds": elapsed, "trace_path": str(trace_path), "trace_exception": trace_exception})
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
        write_json(run_root / "runtime_failure.json", {"exception": repr(exc), "failed_cases": failed_cases})
    finally:
        write_json(run_root / "scratch_cleanup.json", remove_scratch(scratch))

    traces = []
    for path in sorted(traces_dir.glob("*.json")):
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
    combined = totals.get("false_negative_count", 0) + totals.get("false_positive_count", 0) if summary else None
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
            "66": case_metric(summary, "66") if summary else "n/a",
            "67": case_metric(summary, "67") if summary else "n/a",
            "84": case_metric(summary, "84") if summary else "n/a",
            "97": case_metric(summary, "97") if summary else "n/a",
            "110": case_metric(summary, "110") if summary else "n/a",
            "155": case_metric(summary, "155") if summary else "n/a",
            "166": case_metric(summary, "166") if summary else "n/a",
            "14": case_metric(summary, "14") if summary else "n/a",
            "42": case_metric(summary, "42") if summary else "n/a",
            "172": case_metric(summary, "172") if summary else "n/a",
        },
        "rendered_prompt_hash": rendered.get("rendered_prompt_sha256") or "unavailable",
        "request_shape_hash": detection_request.get("request_shape_hash") or "unavailable",
        "raw_response_hash": detection_request.get("raw_response_sha256") or "unavailable",
        "response_trace_captured": bool(detection_request),
        "command_records": command_records,
        "trace_files": [str(path) for path in sorted(traces_dir.glob("*.json"))],
    }
    write_json(run_root / "v037_run_summary.json", record)
    return record


def parse_metric(metric: str) -> tuple[int, int, int] | None:
    if metric == "n/a":
        return None
    parts = metric.split("/")
    if len(parts) != 3:
        return None
    return int(parts[0]), int(parts[1]), int(parts[2])


def office_pass(record: dict[str, Any]) -> bool:
    m = record.get("metrics", {})
    return bool(not record.get("runtime_invalid") and m.get("false_positives") == 0)


def micro_pass(record: dict[str, Any], office_ok: bool) -> tuple[bool, str]:
    if record.get("runtime_invalid"):
        return False, "runtime_invalid"
    cases = record["case_metrics"]
    c67 = parse_metric(cases["67"])
    c66 = parse_metric(cases["66"])
    c110 = parse_metric(cases["110"])
    c84 = parse_metric(cases["84"])
    c166 = parse_metric(cases["166"])
    if not c66 or c66[2] > 5:
        return False, "case66_fp_regression_gate_failed"
    if not c67 or c67[0] < 8 or c67[1] > 3:
        return False, "case67_gate_failed"
    if not c110 or c110[2] >= 10:
        return False, "case110_fp_explosion_gate_failed"
    if not c84 or c84[1] > 5:
        return False, "case84_recall_regression_gate_failed"
    if not c166 or c166[1] > 0:
        return False, "case166_gate_failed"
    if not office_ok:
        return False, "office_negative_failed"
    return True, "micro_pack_passed"


def candidate_status(record: dict[str, Any], office_ok: bool) -> str:
    if record.get("runtime_invalid"):
        return "runtime_invalid"
    errors = record["metrics"]["combined_errors"]
    if not office_ok:
        return "rejected"
    if errors <= 1:
        return "target_met"
    if errors <= OLD_V020C_ERRORS:
        return "beat_old_v020c_reference"
    if errors < V034A_ERRORS:
        return "new_fp8_working_best"
    return "learning_evidence" if errors <= V034A_ERRORS else "rejected"


def print_candidate_block(record: dict[str, Any], stage: str, status: str, lesson: str, next_axis: str, office_ok: bool) -> None:
    m = record.get("metrics", {})
    cases = record.get("case_metrics", {})
    errors = m.get("combined_errors")
    print("=== V037 CANDIDATE COMPLETE ===", flush=True)
    print(f"candidate: {record.get('candidate_id')}", flush=True)
    print("backend: vllm_qwen3vl_8b_fp8", flush=True)
    print(f"stage: {stage}", flush=True)
    print(f"matches: {m.get('matches', 'n/a')}", flush=True)
    print(f"false_negatives: {m.get('false_negatives', 'n/a')}", flush=True)
    print(f"false_positives: {m.get('false_positives', 'n/a')}", flush=True)
    print(f"combined_errors: {errors if errors is not None else 'n/a'}", flush=True)
    print(f"vs_v034a_delta: {errors - V034A_ERRORS if errors is not None else 'n/a'}", flush=True)
    print(f"vs_fp8_baseline_delta: {errors - FP8_BASELINE_ERRORS if errors is not None else 'n/a'}", flush=True)
    print(f"vs_old_v020c_58_delta: {errors - OLD_V020C_ERRORS if errors is not None else 'n/a'}", flush=True)
    print(f"case_66: {cases.get('66', 'n/a')}", flush=True)
    print(f"case_67: {cases.get('67', 'n/a')}", flush=True)
    print(f"case_84: {cases.get('84', 'n/a')}", flush=True)
    print(f"case_110: {cases.get('110', 'n/a')}", flush=True)
    print(f"case_155: {cases.get('155', 'n/a')}", flush=True)
    print(f"case_166: {cases.get('166', 'n/a')}", flush=True)
    print(f"office_negative: {'pass' if office_ok else 'fail'}", flush=True)
    print(f"status: {status}", flush=True)
    print(f"main_lesson: {lesson}", flush=True)
    print(f"next_axis: {next_axis}", flush=True)
    print("===============================", flush=True)


def write_scaffold(preflight: dict[str, Any]) -> None:
    for name in ["overlays", "diagnoses", "runs", "scripts", "research_notes.md", "visual_review_notes.md"]:
        path = PACKAGE_ROOT / name
        if path.suffix:
            path.write_text(f"# v037 {path.stem.replace('_', ' ').title()}\n\n", encoding="utf-8")
        else:
            path.mkdir(parents=True, exist_ok=True)
    write_json(PACKAGE_ROOT / "backend_preflight.json", preflight)
    write_json(
        PACKAGE_ROOT / "source_manifest.json",
        {
            "generated_at": utc_now(),
            "package": "v037_fp8_same_wreck_duplicate_guard_autonomous",
            "source_artifacts": [
                "V036_FP8_CASE155_DENSE_SYNTHESIS_REVIEW_POINTER.md in review repo",
                str(PACKAGE_ROOT.parent / "v036_fp8_case155_dense_synthesis/final_recommendation.md"),
                str(PACKAGE_ROOT.parent / "v036_fp8_case155_dense_synthesis/prompt_axis_decision.md"),
                str(PACKAGE_ROOT.parent / "v036_fp8_case155_dense_synthesis/case155_fp_synthesis.md"),
                str(PACKAGE_ROOT.parent / "v036_fp8_case155_dense_synthesis/dense_case_regression_synthesis.md"),
                "V034_FP8_PRECISION_RECOVERY_REVIEW_POINTER.md if present locally",
                str(V034_PACKAGE / "final_recommendation.md"),
                str(V034_PACKAGE / "diagnoses/v034a_fp8_broad_context_scene_box_guard_diagnosis.md"),
                str(V034_PACKAGE / "comparison_matrix.md"),
                "V033_FP8_TIMEOUT_REPAIR_REVIEW_POINTER.md if present locally",
                str(V033_PACKAGE / "final_recommendation.md"),
                str(V033_PACKAGE / "diagnoses/v033_v032d_clean_replay_diagnosis.md"),
                str(V032_PACKAGE / "final_recommendation.md"),
                "V032_FP8_MODEL_LINE_PROMPT_REFINEMENT_POINTER.md if present locally",
                "V031_QWEN3VL_FP8_SURFACE_REVIEW_POINTER.md if present locally",
            ],
            "old_product_v020c": {"matches": 186, "false_negatives": 33, "false_positives": 25, "combined_errors": 58},
            "fp8_baseline": {"matches": 180, "false_negatives": 39, "false_positives": 32, "combined_errors": 71},
            "v034a_working_best": {"matches": 181, "false_negatives": 38, "false_positives": 25, "combined_errors": 63},
            "v032d_clean_full": {"matches": 185, "false_negatives": 34, "false_positives": 57, "combined_errors": 91, "status": "rejected"},
            "v024l_status": "learning_evidence_only",
            "v025a_status": "rejected",
            "v024o_status": "partial_unscored_forbidden",
            "v035a_micro": {"matches": 41, "false_negatives": 15, "false_positives": 19, "combined_errors": 34, "status": "rejected"},
            "v036_decision": "Axis B: local case-155 same-wreck duplicate guard; do not use broad dense/fragment wording.",
            "hard_boundaries": {"no_promotion": True, "no_product_truth_mutation": True, "no_v024o": True, "no_v032d_as_base": True, "no_v035a_as_base": True},
        },
    )
    write_json(
        PACKAGE_ROOT / "model_line_manifest.json",
        {
            "model_line": "qwen3-vl-8b-instruct-fp8-vllm",
            "backend": BACKEND,
            "working_best_start": "v034a_fp8_broad_context_scene_box_guard",
            "working_best_metrics": {"matches": 181, "false_negatives": 38, "false_positives": 25, "combined_errors": 63},
            "not_product_replacement": True,
        },
    )
    (PACKAGE_ROOT / "README.md").write_text(
        "# v037 FP8 vLLM Same-Wreck Duplicate Guard Autonomous\n\n"
        "Separate-model-line FP8 vLLM prompt-refinement tranche. The working best starts as "
        "`v034a_fp8_broad_context_scene_box_guard = 181 / 38 / 25 / 63`. "
        "`v037a` tests v036's narrow same-wreck duplicate/local-context axis from v034a. "
        "`v032d` and `v035a` are rejected learning evidence only and are not used as base prompts.\n",
        encoding="utf-8",
    )


def write_closeout(records: dict[str, Any], final_status: str, next_axis: str) -> None:
    rows: list[dict[str, Any]] = [
        {"candidate_id": "v020c_old_product_reference", "stage": "prior_all_current", "metrics": {"matches": 186, "false_negatives": 33, "false_positives": 25, "combined_errors": 58}, "status": "product_reference"},
        {"candidate_id": "v020c_fp8_vllm_baseline", "stage": "v031_all_current", "metrics": {"matches": 180, "false_negatives": 39, "false_positives": 32, "combined_errors": 71}, "status": "fp8_working_baseline"},
        {"candidate_id": "v032d_fp8_v019c_anchor_replay", "stage": "v033_clean_full", "metrics": {"matches": 185, "false_negatives": 34, "false_positives": 57, "combined_errors": 91}, "case_67": "8/3/2", "case_110": "3/4/32", "case_155": "2/0/0", "case_166": "1/0/0", "office_negative": "pass", "status": "rejected"},
        {"candidate_id": "v034a_fp8_broad_context_scene_box_guard", "stage": "v034_full_all_current", "metrics": {"matches": 181, "false_negatives": 38, "false_positives": 25, "combined_errors": 63}, "case_66": "8/0/5", "case_67": "10/1/3", "case_84": "8/5/0", "case_110": "3/4/1", "case_155": "2/0/1", "case_166": "1/0/0", "office_negative": "pass", "status": "fp8_working_best"},
    ]
    for key in ["baseline_sentinel", "candidate_micro", "candidate_full"]:
        record = records.get(key)
        if not record:
            continue
        rows.append(
            {
                "candidate_id": record["candidate_id"],
                "stage": record["stage"],
                "metrics": record["metrics"],
                "case_67": record["case_metrics"].get("67"),
                "case_66": record["case_metrics"].get("66"),
                "case_84": record["case_metrics"].get("84"),
                "case_110": record["case_metrics"].get("110"),
                "case_155": record["case_metrics"].get("155"),
                "case_166": record["case_metrics"].get("166"),
                "office_negative": records.get(f"{key}_office_status", "n/a"),
                "status": records.get(f"{key}_status", "complete"),
            }
        )
    write_json(PACKAGE_ROOT / "comparison_matrix.json", {"generated_at": utc_now(), "rows": rows})
    (PACKAGE_ROOT / "comparison_matrix.md").write_text(
        "# v037 Comparison Matrix\n\n"
        "| Candidate | Stage | Matches | FNs | FPs | Errors | Case 66 | Case 67 | Case 84 | Case 110 | Case 155 | Case 166 | Office | Status |\n"
        "|---|---|---:|---:|---:|---:|---|---|---|---|---|---|---|---|\n"
        + "\n".join(
            f"| `{row['candidate_id']}` | {row['stage']} | {row['metrics']['matches']} | {row['metrics']['false_negatives']} | {row['metrics']['false_positives']} | {row['metrics']['combined_errors']} | `{row.get('case_66', 'n/a')}` | `{row.get('case_67', 'n/a')}` | `{row.get('case_84', 'n/a')}` | `{row.get('case_110', 'n/a')}` | `{row.get('case_155', 'n/a')}` | `{row.get('case_166', 'n/a')}` | {row.get('office_negative', 'n/a')} | {row['status']} |"
            for row in rows
        )
        + "\n",
        encoding="utf-8",
    )
    write_json(PACKAGE_ROOT / "candidate_registry.json", {"generated_at": utc_now(), "candidates": rows})
    final_record = records.get("candidate_full") or records.get("candidate_micro")
    best_candidate = "v034a_fp8_broad_context_scene_box_guard"
    beat_v034a = False
    beat_baseline = True
    beat_old = False
    target_met = False
    if final_record and not final_record.get("runtime_invalid"):
        errors = final_record["metrics"]["combined_errors"]
        if errors < V034A_ERRORS and records.get("candidate_full_status") in {"new_fp8_working_best", "beat_old_v020c_reference", "target_met"}:
            best_candidate = final_record["candidate_id"]
            beat_v034a = True
            beat_baseline = True
            beat_old = errors <= OLD_V020C_ERRORS
            target_met = errors <= 1
    write_json(
        PACKAGE_ROOT / "final_recommendation.json",
        {
            "generated_at": utc_now(),
            "status": final_status,
            "best_fp8_candidate": best_candidate,
            "beat_v034a_63": beat_v034a,
            "beat_fp8_baseline_71": beat_baseline,
            "reached_or_beat_old_v020c_58": beat_old,
            "target_le_1_reached": target_met,
            "fp8_should_continue_as_separate_model_line": True,
            "hard_boundaries_preserved": True,
            "next_axis": next_axis,
        },
    )
    (PACKAGE_ROOT / "final_recommendation.md").write_text(
        "# v037 Final Recommendation\n\n"
        f"Generated: `{utc_now()}`\n\n"
        f"Status: `{final_status}`.\n\n"
        f"Best FP8 candidate: `{best_candidate}`.\n\n"
        f"Beat v034a 63 errors: `{beat_v034a}`.\n"
        f"Beat FP8 baseline 71 errors: `{beat_baseline}`.\n"
        f"Reached or beat old 58-error reference: `{beat_old}`.\n"
        f"Reached <=1 target: `{target_met}`.\n\n"
        f"Next axis: {next_axis}\n\n"
        "FP8 should remain a separate model line, not a product replacement. Hard boundaries were preserved.\n",
        encoding="utf-8",
    )
    (PACKAGE_ROOT / "lessons_learned.md").write_text(
        "# v037 Lessons Learned\n\n"
        "- v032d confirms that removing the v020c audit is unsafe on FP8 despite selected control gains.\n"
        "- v036 isolated the case-155 gain as a same-wreck nested duplicate issue, not a broad dense-fragment issue.\n"
        "- Case 110 must remain in the FP8 micro-pack because it exposes broad FP reopening quickly.\n"
        "- Precision candidates must preserve v034a broad-context guard and v020c audit discipline.\n"
        "- Case 84 recall cannot be allowed to slip further without a large compensating full-pack gain.\n",
        encoding="utf-8",
    )
    (PACKAGE_ROOT / "strategy_state.md").write_text(
        "# v037 Strategy State\n\n"
        f"- Current FP8 working best: `{best_candidate}`.\n"
        f"- Final status: `{final_status}`.\n"
        f"- Next axis: {next_axis}\n",
        encoding="utf-8",
    )
    (PACKAGE_ROOT / "live_metrics_log.md").write_text(
        "# v037 Live Metrics Log\n\n"
        + "\n".join(
            f"- `{row['candidate_id']}` `{row['stage']}`: `{row['metrics']['matches']}/{row['metrics']['false_negatives']}/{row['metrics']['false_positives']}/{row['metrics']['combined_errors']}` status `{row['status']}`"
            for row in rows
        )
        + "\n",
        encoding="utf-8",
    )
    (PACKAGE_ROOT / "recovery_log.md").write_text(
        "# v037 Recovery Log\n\n"
        "- Re-grounded in v036/v035/v034/v033 evidence.\n"
        "- Used v033 timeout/retry policy for FP8 vLLM.\n"
        "- Created sentinel manifest including case 110.\n"
        "- Authored one compact same-wreck duplicate candidate from v034a, not from v032d or v035a.\n",
        encoding="utf-8",
    )
    write_json(PACKAGE_ROOT / "recovery_log.json", {"generated_at": utc_now(), "records": sorted(records.keys())})
    diag = PACKAGE_ROOT / "diagnoses/v037a_fp8_same_wreck_duplicate_local_guard_diagnosis.md"
    candidate_micro = records.get("candidate_micro")
    candidate_full = records.get("candidate_full")
    diag.write_text(
        "# v037a Diagnosis\n\n"
        "What did this candidate test? A compact same-wreck duplicate/local-context guard for the case-155-style nested box identified in v036.\n\n"
        "What changed from v034a? One BAD FINAL BOX line was added after the v034a broad-context/scene-box guard. The v034a guard, v020c audit, and final balance were preserved.\n\n"
        f"Micro-pack result: `{candidate_micro['metrics'] if candidate_micro else 'n/a'}`.\n\n"
        f"Full result: `{candidate_full['metrics'] if candidate_full else 'not run'}`.\n\n"
        "Known failure focus: case 155 same-wreck duplicate FP, case 66/67 dense-row safety, case 84 recall, case 110 broad FP explosion, and controls 166/office-negative.\n\n"
        f"Next hypothesis: {next_axis}\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args()
    if not args.run:
        parser.print_help()
        return 0

    PACKAGE_ROOT.mkdir(parents=True, exist_ok=True)
    create_sentinel_manifest()
    baseline_overlay = create_baseline_overlay_copy()
    candidate_overlay = create_candidate_overlay()
    preflight = {"generated_at": utc_now(), "backend": BACKEND, "models": fetch_models(), "timeout_policy": {"per_case_timeout_seconds": REQUEST_TIMEOUT_SECONDS, "max_retries": MAX_RETRIES, "cooldown_seconds": RETRY_COOLDOWN_SECONDS}}
    write_scaffold(preflight)
    if not preflight["models"]["ok"] or not preflight["models"]["model_present"]:
        raise RuntimeError("vLLM FP8 backend is not available.")

    records: dict[str, Any] = {}
    baseline = {"candidate_id": "v037_baseline_exact_v034a_replay", "overlay_path": str(baseline_overlay), "intended_changes": []}
    candidate = {
        "candidate_id": "v037a_fp8_same_wreck_duplicate_local_guard",
        "overlay_path": str(candidate_overlay),
        "intended_changes": read_yaml(candidate_overlay).get("intended_changes", []),
    }

    records["baseline_sentinel"] = run_probe(baseline, SENTINEL_MANIFEST, "micro_pack_only")
    records["baseline_sentinel_office"] = run_probe(baseline, OFFICE_NEGATIVE_MANIFEST, "office_negative_guard")
    records["baseline_sentinel_office_status"] = "pass" if office_pass(records["baseline_sentinel_office"]) else "fail"
    records["baseline_sentinel_status"] = "baseline_replay"

    records["candidate_micro"] = run_probe(candidate, SENTINEL_MANIFEST, "micro_pack_only")
    records["candidate_micro_office"] = run_probe(candidate, OFFICE_NEGATIVE_MANIFEST, "office_negative_guard")
    candidate_office_ok = office_pass(records["candidate_micro_office"])
    records["candidate_micro_office_status"] = "pass" if candidate_office_ok else "fail"
    micro_ok, micro_reason = micro_pass(records["candidate_micro"], candidate_office_ok)
    if not micro_ok:
        status = "runtime_invalid" if micro_reason == "runtime_invalid" else "rejected"
        records["candidate_micro_status"] = status
        print_candidate_block(
            records["candidate_micro"],
            "micro_pack_only",
            status,
            f"v037a failed the FP8 micro gate: {micro_reason}.",
            "Pivot to the exact failing case deltas before another semantic prompt.",
            candidate_office_ok,
        )
        write_closeout(records, status, "Use the v037a failure deltas to decide whether to refine same-wreck overlap wording or pivot away from prompt-only duplicate suppression.")
        return 0

    records["candidate_micro_status"] = "micro_pass"
    print_candidate_block(
        records["candidate_micro"],
        "micro_pack_only",
        "learning_evidence",
        "v037a passed the FP8 micro gate; full all-current is now required.",
        "Run full all-current/no101 before deciding whether it beats v034a.",
        candidate_office_ok,
    )

    records["candidate_full"] = run_probe(candidate, ALL_CURRENT_MANIFEST, "full_all_current")
    records["candidate_full_office"] = run_probe(candidate, OFFICE_NEGATIVE_MANIFEST, "office_negative_guard")
    full_office_ok = office_pass(records["candidate_full_office"])
    records["candidate_full_office_status"] = "pass" if full_office_ok else "fail"
    status = candidate_status(records["candidate_full"], full_office_ok)
    records["candidate_full_status"] = status
    lesson = "v037a completed full all-current on FP8 vLLM."
    next_axis = "If v037a beats 63, continue from it; otherwise use full-run deltas to refine only the same-wreck duplicate axis or pivot to case-84 recall."
    print_candidate_block(records["candidate_full"], "full_all_current", status, lesson, next_axis, full_office_ok)
    write_closeout(records, status, next_axis)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
