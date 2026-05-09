#!/usr/bin/env python3
"""v042 experiment-only FP8 postprocessed-scoring prompt-refinement operator."""

from __future__ import annotations

import argparse
import contextlib
import csv
import datetime as dt
import hashlib
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.request
from copy import deepcopy
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import yaml


WORKTREE_ROOT = Path("/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement")
CAPSTONE_ROOT = Path("/home/williambenitez1/Capstone")
PACKAGE_ROOT = WORKTREE_ROOT / (
    "docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/"
    "human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/"
    "v017b_prompt_only_main_promotion/v042_fp8_postprocessed_scoring_autonomous"
)
PARENT_ROOT = PACKAGE_ROOT.parent
V034_PACKAGE = PARENT_ROOT / "v034_fp8_vllm_precision_recovery_autonomous"
V038_SCRIPT = PARENT_ROOT / "v038_fp8_same_wreck_duplicate_suppression_simulation/scripts/run_v038_duplicate_suppression_simulation.py"
V041_SCRIPT = PARENT_ROOT / "v041_fp8_prediction_only_duplicate_suppression/scripts/run_v041_prediction_only_duplicate_suppression.py"
BASELINE_OVERLAY = V034_PACKAGE / "overlays/v034a_fp8_broad_context_scene_box_guard.yaml"
V020C_OVERLAY = (
    PARENT_ROOT / "v020_v019c_goal_driven_self_improvement_cycle/overlays/v020c_v019c_extra_box_audit.yaml"
)
V034_FULL_RUN_ROOT = (
    V034_PACKAGE
    / "runs/v034a_fp8_broad_context_scene_box_guard/full_all_current/"
    "human_report_challenge_v2_all_current_117_no101_2026-05-09_023225Z"
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
SENTINEL_MANIFEST = PACKAGE_ROOT / "validation_manifests/v042_fp8_sentinel_with_100_110_no101.yaml"
BDA_EVAL_ROOT = WORKTREE_ROOT / "bda_eval"
INSTRUMENTED_RUNNER = PARENT_ROOT / "v037_fp8_same_wreck_duplicate_guard_autonomous/scripts/instrumented_bda_runner.py"

BACKEND = {
    "label": "vllm_qwen3vl_8b_fp8",
    "base_url": "http://localhost:8000/v1",
    "api_key": "EMPTY",
    "model": "Qwen/Qwen3-VL-8B-Instruct-FP8",
}
REQUEST_TIMEOUT_SECONDS = 180
MAX_RETRIES = 2
RETRY_COOLDOWN_SECONDS = 5

OLD_V020C = {"matches": 186, "false_negatives": 33, "false_positives": 25, "combined_errors": 58}
FP8_BASELINE = {"matches": 180, "false_negatives": 39, "false_positives": 32, "combined_errors": 71}
RAW_V034A = {"matches": 181, "false_negatives": 38, "false_positives": 25, "combined_errors": 63}
COMPOSITE_V034A_P1753 = {"matches": 181, "false_negatives": 38, "false_positives": 24, "combined_errors": 62}
V040_HYBRID_ORACLE = {"matches": 181, "false_negatives": 38, "false_positives": 22, "combined_errors": 60}

SENTINEL_CASES = [12, 14, 16, 42, 66, 67, 77, 84, 88, 90, 97, 100, 103, 110, 155, 166, 172]
WATCH_CASES = ["66", "67", "84", "88", "97", "100", "110", "155", "166"]


def import_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {name} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


v038 = import_module(V038_SCRIPT, "v042_v038_helpers")
v041 = import_module(V041_SCRIPT, "v042_v041_helpers")


@dataclass(frozen=True)
class RuleP1753:
    rule_id: str = "p1753"
    containment_threshold: float = 0.8
    iou_threshold: float = 0.0
    area_ratio_threshold: float = 0.03
    center_inside_required: bool = True
    same_label_required: bool = True
    cross_label_allowed: bool = False
    cross_area_ratio_threshold: float | None = None
    cross_containment_threshold: float | None = None
    cross_removed_not_only_type_required: bool = True
    larger_image_area_max_ratio: float | None = None
    keep_largest_only: bool = True
    never_suppress_if_smaller_contains_prediction: bool = True


P1753 = RuleP1753()


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


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def sha256_file(path: Path) -> str | None:
    if not path.exists():
        return None
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def metrics_string(metrics: dict[str, Any] | None) -> str:
    if not metrics:
        return "n/a"
    return f"{metrics.get('matches')}/{metrics.get('false_negatives')}/{metrics.get('false_positives')}/{metrics.get('combined_errors')}"


def case_metric(eval_payload: dict[str, Any], case_number: str) -> str:
    for image in eval_payload.get("images", []):
        if v038.case_num(image.get("image_filename", "")) == str(case_number):
            return f"{image.get('match_count')}/{image.get('false_negative_count')}/{image.get('false_positive_count')}"
    return "n/a"


def case_metrics(eval_payload: dict[str, Any] | None) -> dict[str, str]:
    if not eval_payload:
        return {case: "n/a" for case in WATCH_CASES}
    metrics = v038.case_metrics(eval_payload)
    return {case: metrics.get(case, "n/a") for case in WATCH_CASES}


def normalize_totals(eval_payload: dict[str, Any] | None) -> dict[str, Any]:
    if not eval_payload:
        return {"matches": None, "false_negatives": None, "false_positives": None, "combined_errors": None, "image_count": None}
    totals = eval_payload["totals"]
    return {
        "matches": totals["matches"],
        "false_negatives": totals["false_negatives"],
        "false_positives": totals["false_positives"],
        "combined_errors": totals["combined_errors"],
        "image_count": totals["image_count"],
    }


def fetch_models() -> dict[str, Any]:
    try:
        with urllib.request.urlopen(BACKEND["base_url"] + "/models", timeout=5) as response:
            payload = json.loads(response.read().decode("utf-8"))
        return {
            "ok": True,
            "payload": payload,
            "model_present": any(item.get("id") == BACKEND["model"] for item in payload.get("data", [])),
        }
    except Exception as exc:
        return {"ok": False, "error": repr(exc), "model_present": False}


def load_manifest_cases(manifest: Path) -> list[dict[str, Any]]:
    payload = read_yaml(manifest)
    return list(payload["cases"])


def load_reference_reports(manifest: Path) -> tuple[dict[str, dict[str, Any]], list[str], list[dict[str, Any]]]:
    cases = load_manifest_cases(manifest)
    references: dict[str, dict[str, Any]] = {}
    image_order: list[str] = []
    for case in cases:
        path = Path(case["reference_report"])
        if not path.is_absolute():
            path = (manifest.parent / path).resolve()
        key, data = v038.discovery.get_report(path)
        references[key] = data
        image_order.append(key)
    return references, image_order, cases


def load_predicted_reports(predicted_dir: Path) -> dict[str, dict[str, Any]]:
    reports: dict[str, dict[str, Any]] = {}
    for path in sorted(predicted_dir.glob("*.json")):
        result = v038.discovery.get_report(path)
        if result:
            key, data = result
            reports[key] = data
    return reports


def evaluate_reports(
    references: dict[str, dict[str, Any]],
    predictions: dict[str, dict[str, Any]],
    image_order: list[str],
) -> dict[str, Any]:
    os.environ.pop("OLLAMA_API_KEY", None)
    with contextlib.redirect_stdout(io.StringIO()):
        return v038.evaluate_reports(references, predictions, image_order)


def image_dimensions(cases: list[dict[str, Any]]) -> dict[str, tuple[int, int]]:
    return v041.image_dimensions(cases)


def apply_p1753_to_reports(
    references: dict[str, dict[str, Any]],
    predictions: dict[str, dict[str, Any]],
    image_order: list[str],
    cases: list[dict[str, Any]],
) -> dict[str, Any]:
    dims = image_dimensions(cases)
    pairs_by_image = {
        image_filename: v041.pair_features_prediction_only(predictions[image_filename], dims.get(image_filename))
        for image_filename in image_order
        if image_filename in predictions
    }
    rule = v041.PredictionOnlyRule(**asdict(P1753))
    postprocessed, removals = v041.apply_rule(predictions, pairs_by_image, rule)
    raw_eval = evaluate_reports(references, predictions, image_order)
    post_eval = evaluate_reports(references, postprocessed, image_order)
    annotated = v041.annotate_removals(removals, raw_eval, post_eval)
    return {
        "rule": {**asdict(P1753), "oracle_fields_used": []},
        "raw_eval": raw_eval,
        "post_eval": post_eval,
        "postprocessed_reports": postprocessed,
        "removals": annotated,
        "removed_predictions": len(annotated),
        "removed_true_positives": sum(1 for row in annotated if row["removed_true_positive"]),
        "removed_false_positives": sum(1 for row in annotated if row["removed_false_positive"]),
    }


def write_postprocessed_reports(output_dir: Path, reports: dict[str, dict[str, Any]]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for image_filename, report in reports.items():
        case = v038.case_num(image_filename)
        path = output_dir / f"{case}_p1753.json"
        path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def create_sentinel_manifest() -> None:
    wanted = {f"human-report-{n}" for n in SENTINEL_CASES}
    all_current = read_yaml(ALL_CURRENT_MANIFEST)
    cases = [case for case in all_current["cases"] if case["case_id"] in wanted]
    found = {case["case_id"] for case in cases}
    missing = sorted(wanted - found)
    if missing:
        raise RuntimeError(f"Missing sentinel cases: {missing}")
    write_yaml(
        SENTINEL_MANIFEST,
        {
            "pack_id": "v042_fp8_sentinel_with_100_110_no101",
            "eval_mode": all_current.get("eval_mode", "object_detection"),
            "images_dir": all_current.get("images_dir"),
            "cases": cases,
        },
    )


def extract_prompt_from_overlay(path: Path) -> str:
    return read_yaml(path)["overrides"]["prompts"]["detect_objects"]


def create_baseline_overlay_copy() -> Path:
    payload = read_yaml(BASELINE_OVERLAY)
    payload["candidate_id"] = "v042_baseline_exact_v034a_replay"
    payload["title"] = "v042 baseline exact v034a replay"
    payload["overlay_id"] = "qwen-1.2-v042_baseline_exact_v034a_replay"
    payload["overlay_type"] = "fp8_postprocessed_scoring_baseline"
    payload["description"] = "Exact FP8 v034a replay for v042 postprocessed-scoring preflight."
    payload["intended_changes"] = []
    out = PACKAGE_ROOT / "overlays/v042_baseline_exact_v034a_replay.yaml"
    write_yaml(out, payload)
    return out


def create_v042a_overlay() -> Path:
    baseline = read_yaml(BASELINE_OVERLAY)
    prompt = baseline["overrides"]["prompts"]["detect_objects"]
    needle = (
        "GOOD FINAL BOX\n"
        "- one connected target body, wreck body, or exterior building structure\n"
    )
    addition = (
        "GOOD FINAL BOX\n"
        "- one connected target body, wreck body, or exterior building structure\n"
        "- low-contrast or smoke-softened target bodies are valid when one connected body outline remains visible after context is ignored\n"
    )
    if "low-contrast or smoke-softened target bodies" not in prompt:
        prompt = prompt.replace(needle, addition)
    candidate = deepcopy(baseline)
    candidate["candidate_id"] = "v042a_fp8_case84_low_contrast_recall_probe"
    candidate["title"] = "v042a fp8 case84 low-contrast recall probe"
    candidate["overlay_id"] = "qwen-1.2-v042a_fp8_case84_low_contrast_recall_probe"
    candidate["overlay_type"] = "fp8_postprocessed_scoring_candidate"
    candidate["description"] = (
        "Narrow recall probe for low-contrast/smoke-softened visible target bodies, scored raw and through p1753."
    )
    candidate["generated_from"] = ["v034a_fp8_broad_context_scene_box_guard", "v041_p1753_postprocessed_scoring"]
    candidate["intended_changes"] = [
        "Add one compact GOOD FINAL BOX recall cue for low-contrast or smoke-softened target bodies whose connected body outline remains visible after context is ignored.",
        "Preserve the v020c extra-box audit.",
        "Preserve the v034a broad-context/scene-box guard.",
        "Do not add same-wreck duplicate wording or dense-fragment wording.",
    ]
    candidate["overrides"]["prompts"]["detect_objects"] = prompt
    candidate["overrides"]["runtime"] = {"notes": "Applied only inside upstream/main scratch config; no product adoption."}
    out = PACKAGE_ROOT / "overlays/v042a_fp8_case84_low_contrast_recall_probe.yaml"
    write_yaml(out, candidate)
    return out


def create_scratch(candidate_id: str) -> Path:
    scratch = Path("/tmp") / f"bda_v042_{candidate_id}_{stamp()}"
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


def run_case_probe(candidate: dict[str, Any], manifest: Path, stage: str) -> dict[str, Any]:
    candidate_id = candidate["candidate_id"]
    run_root = PACKAGE_ROOT / "runs" / candidate_id / stage / f"{manifest.stem}_{stamp()}"
    predicted_dir = run_root / "predicted"
    traces_dir = run_root / "traces"
    logs_dir = run_root / "logs"
    for directory in [predicted_dir, traces_dir, logs_dir]:
        directory.mkdir(parents=True, exist_ok=True)

    overlay_path = Path(candidate["overlay_path"])
    prompt = extract_prompt_from_overlay(overlay_path)
    scratch = create_scratch(candidate_id)
    scratch_config_path = patch_scratch_config(scratch, prompt)
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

    command_records: list[dict[str, Any]] = []
    retry_records: list[dict[str, Any]] = []
    completed_cases: list[str] = []
    failed_cases: list[dict[str, Any]] = []
    runtime_invalid = False
    raw_eval = None
    post_payload = None

    try:
        for case in load_manifest_cases(manifest):
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

        references, image_order, cases = load_reference_reports(manifest)
        predictions = load_predicted_reports(predicted_dir)
        missing = sorted(set(image_order) - set(predictions))
        if missing:
            raise RuntimeError(f"Missing predictions for {missing}")
        post_payload = apply_p1753_to_reports(references, predictions, image_order, cases)
        raw_eval = post_payload["raw_eval"]
        post_output_dir = PACKAGE_ROOT / "postprocessed_outputs" / candidate_id / stage / run_root.name
        write_postprocessed_reports(post_output_dir, post_payload["postprocessed_reports"])
        write_json(run_root / "raw_eval_summary.json", raw_eval)
        write_json(run_root / "postprocessed_eval_summary.json", post_payload["post_eval"])
        write_csv(run_root / "p1753_removed_prediction_audit.csv", post_payload["removals"])
        write_json(
            run_root / "p1753_postprocess_summary.json",
            {
                "rule": post_payload["rule"],
                "raw_metrics": normalize_totals(raw_eval),
                "postprocessed_metrics": normalize_totals(post_payload["post_eval"]),
                "removed_predictions": post_payload["removed_predictions"],
                "removed_true_positives": post_payload["removed_true_positives"],
                "removed_false_positives": post_payload["removed_false_positives"],
                "postprocessed_output_dir": str(post_output_dir),
            },
        )
    except Exception as exc:
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
    detection_request = {}
    rendered = {}
    for trace in traces:
        rendered = rendered or trace.get("rendered_prompt") or {}
        for item in trace.get("request_response_traces", []):
            if item.get("call_kind") == "detection":
                detection_request = item
                break
        if detection_request:
            break

    record = {
        "candidate_id": candidate_id,
        "stage": stage,
        "backend": BACKEND,
        "manifest": str(manifest),
        "run_root": str(run_root),
        "predicted_dir": str(predicted_dir),
        "scratch_config_sha256": sha256_file(scratch_config_path),
        "request_timeout_seconds": REQUEST_TIMEOUT_SECONDS,
        "max_retries": MAX_RETRIES,
        "retry_cooldown_seconds": RETRY_COOLDOWN_SECONDS,
        "retry_records": retry_records,
        "completed_cases": completed_cases,
        "failed_cases": failed_cases,
        "runtime_invalid": runtime_invalid,
        "raw_metrics": normalize_totals(raw_eval),
        "postprocessed_metrics": normalize_totals(post_payload["post_eval"] if post_payload else None),
        "raw_case_metrics": case_metrics(raw_eval),
        "postprocessed_case_metrics": case_metrics(post_payload["post_eval"] if post_payload else None),
        "postprocess_removed_predictions": post_payload["removed_predictions"] if post_payload else None,
        "postprocess_removed_true_positives": post_payload["removed_true_positives"] if post_payload else None,
        "postprocess_removed_false_positives": post_payload["removed_false_positives"] if post_payload else None,
        "rendered_prompt_hash": rendered.get("rendered_prompt_sha256") or "unavailable",
        "request_shape_hash": detection_request.get("request_shape_hash") or "unavailable",
        "raw_response_hash": detection_request.get("raw_response_sha256") or "unavailable",
        "response_trace_captured": bool(detection_request),
        "trace_files": [str(path) for path in sorted(traces_dir.glob("*.json"))],
        "command_records": command_records,
    }
    write_json(run_root / "v042_run_summary.json", record)
    return record


def run_office_guard(candidate: dict[str, Any], label: str) -> dict[str, Any]:
    record = run_case_probe(candidate, OFFICE_NEGATIVE_MANIFEST, f"office_negative_guard_{label}")
    raw = record.get("raw_metrics", {})
    post = record.get("postprocessed_metrics", {})
    return {
        "run_record": record,
        "pass": (
            not record.get("runtime_invalid")
            and raw.get("false_positives") == 0
            and post.get("false_positives") == 0
            and record.get("postprocess_removed_true_positives") == 0
        ),
    }


def parse_metric(metric: str) -> tuple[int, int, int] | None:
    if metric == "n/a":
        return None
    parts = metric.split("/")
    if len(parts) != 3:
        return None
    return int(parts[0]), int(parts[1]), int(parts[2])


def micro_pass(record: dict[str, Any], office_ok: bool) -> tuple[bool, str]:
    if record.get("runtime_invalid"):
        return False, "runtime_invalid"
    if record.get("postprocess_removed_true_positives") != 0:
        return False, "p1753_removed_true_positive"
    cases = record["postprocessed_case_metrics"]
    c66 = parse_metric(cases["66"])
    c67 = parse_metric(cases["67"])
    c84 = parse_metric(cases["84"])
    c110 = parse_metric(cases["110"])
    c166 = parse_metric(cases["166"])
    if not c66 or c66[2] > 5:
        return False, "case66_fp_regression_gate_failed"
    if not c67 or c67[0] < 8 or c67[1] > 3:
        return False, "case67_gate_failed"
    if not c84 or c84[1] > 5:
        return False, "case84_recall_regression_gate_failed"
    if not c110 or c110[2] >= 10:
        return False, "case110_fp_explosion_gate_failed"
    if not c166 or c166[1] > 0:
        return False, "case166_gate_failed"
    if not office_ok:
        return False, "office_negative_failed"
    return True, "micro_pack_passed"


def status_for_record(record: dict[str, Any], office_ok: bool, stage: str) -> str:
    if record.get("runtime_invalid"):
        return "runtime_invalid"
    if record.get("postprocess_removed_true_positives") != 0:
        return "rejected"
    if not office_ok:
        return "rejected"
    post_errors = record["postprocessed_metrics"]["combined_errors"]
    raw_errors = record["raw_metrics"]["combined_errors"]
    if post_errors <= 1:
        return "target_met"
    if post_errors <= OLD_V020C["combined_errors"]:
        return "beat_old_v020c_reference"
    if post_errors < COMPOSITE_V034A_P1753["combined_errors"]:
        return "new_composite_working_best"
    if raw_errors < RAW_V034A["combined_errors"]:
        return "new_raw_working_best"
    return "learning_evidence" if stage == "full_all_current" else "learning_evidence"


def print_candidate_block(record: dict[str, Any], stage: str, status: str, lesson: str, next_axis: str, office_ok: bool) -> None:
    raw = record.get("raw_metrics", {})
    post = record.get("postprocessed_metrics", {})
    print("=== V042 CANDIDATE COMPLETE ===", flush=True)
    print(f"candidate: {record.get('candidate_id')}", flush=True)
    print("backend: vllm_qwen3vl_8b_fp8", flush=True)
    print(f"stage: {stage}", flush=True)
    print(f"raw_metrics: {metrics_string(raw)}", flush=True)
    print(f"postprocessed_metrics: {metrics_string(post)}", flush=True)
    print(
        f"vs_composite_62_delta: {post.get('combined_errors') - COMPOSITE_V034A_P1753['combined_errors'] if post.get('combined_errors') is not None else 'n/a'}",
        flush=True,
    )
    print(
        f"vs_raw_v034a_63_delta: {raw.get('combined_errors') - RAW_V034A['combined_errors'] if raw.get('combined_errors') is not None else 'n/a'}",
        flush=True,
    )
    print(
        f"vs_old_v020c_58_delta: {post.get('combined_errors') - OLD_V020C['combined_errors'] if post.get('combined_errors') is not None else 'n/a'}",
        flush=True,
    )
    raw_cases = record.get("raw_case_metrics", {})
    post_cases = record.get("postprocessed_case_metrics", {})
    for case in ["66", "67", "84", "100", "110", "155", "166"]:
        print(f"case_{case}_raw_post: {raw_cases.get(case, 'n/a')} -> {post_cases.get(case, 'n/a')}", flush=True)
    print(f"office_negative: {'pass' if office_ok else 'fail'}", flush=True)
    print(f"postprocess_removed_predictions: {record.get('postprocess_removed_predictions', 'n/a')}", flush=True)
    print(f"postprocess_removed_true_positives: {record.get('postprocess_removed_true_positives', 'n/a')}", flush=True)
    print(f"status: {status}", flush=True)
    print(f"main_lesson: {lesson}", flush=True)
    print(f"next_axis: {next_axis}", flush=True)
    print("===============================", flush=True)


def print_status(phase: str, record: dict[str, Any] | None, decision: str, lesson: str, next_action: str) -> None:
    print("=== V042 STATUS ===", flush=True)
    print(f"phase: {phase}", flush=True)
    print("backend: vllm_qwen3vl_8b_fp8", flush=True)
    if record:
        print(f"raw_metrics: {metrics_string(record.get('raw_metrics'))}", flush=True)
        print(f"postprocessed_metrics: {metrics_string(record.get('postprocessed_metrics'))}", flush=True)
        print(f"postprocess_removed_predictions: {record.get('postprocess_removed_predictions', 'n/a')}", flush=True)
        print(f"postprocess_removed_true_positives: {record.get('postprocess_removed_true_positives', 'n/a')}", flush=True)
    else:
        print("raw_metrics: n/a", flush=True)
        print("postprocessed_metrics: n/a", flush=True)
        print("postprocess_removed_predictions: n/a", flush=True)
        print("postprocess_removed_true_positives: n/a", flush=True)
    print(f"decision: {decision}", flush=True)
    print(f"main_lesson: {lesson}", flush=True)
    print(f"next_action: {next_action}", flush=True)
    print("===================", flush=True)


def reproduce_p1753() -> dict[str, Any]:
    references, image_order, cases = load_reference_reports(ALL_CURRENT_MANIFEST)
    predictions = load_predicted_reports(V034_FULL_RUN_ROOT / "predicted")
    payload = apply_p1753_to_reports(references, predictions, image_order, cases)
    out_dir = PACKAGE_ROOT / "postprocessed_outputs/v034a_frozen_p1753_reproduction"
    write_postprocessed_reports(out_dir, payload["postprocessed_reports"])
    write_csv(PACKAGE_ROOT / "p1753_reproduction_removed_prediction_audit.csv", payload["removals"])
    write_json(
        PACKAGE_ROOT / "p1753_reproduction.json",
        {
            "generated_at": utc_now(),
            "rule": payload["rule"],
            "raw_metrics": normalize_totals(payload["raw_eval"]),
            "postprocessed_metrics": normalize_totals(payload["post_eval"]),
            "removed_predictions": payload["removed_predictions"],
            "removed_true_positives": payload["removed_true_positives"],
            "removed_false_positives": payload["removed_false_positives"],
            "removed_cases": sorted({row["case_id"] for row in payload["removals"]}),
            "postprocessed_output_dir": str(out_dir),
        },
    )
    return {
        "raw_metrics": normalize_totals(payload["raw_eval"]),
        "postprocessed_metrics": normalize_totals(payload["post_eval"]),
        "raw_case_metrics": case_metrics(payload["raw_eval"]),
        "postprocessed_case_metrics": case_metrics(payload["post_eval"]),
        "postprocess_removed_predictions": payload["removed_predictions"],
        "postprocess_removed_true_positives": payload["removed_true_positives"],
        "postprocess_removed_false_positives": payload["removed_false_positives"],
        "removals": payload["removals"],
    }


def p1753_reproduction_ok(record: dict[str, Any]) -> bool:
    return (
        record["raw_metrics"] == {**RAW_V034A, "image_count": 117}
        and record["postprocessed_metrics"] == {**COMPOSITE_V034A_P1753, "image_count": 117}
        and record["postprocess_removed_predictions"] == 1
        and record["postprocess_removed_true_positives"] == 0
        and {row["case_id"] for row in record.get("removals", [])} == {"88"}
    )


def write_scaffold(preflight: dict[str, Any] | None = None) -> None:
    for directory in ["overlays", "diagnoses", "runs", "scripts", "postprocessed_outputs", "validation_manifests"]:
        (PACKAGE_ROOT / directory).mkdir(parents=True, exist_ok=True)
    for name in ["research_notes.md", "visual_review_notes.md"]:
        path = PACKAGE_ROOT / name
        if not path.exists():
            path.write_text(f"# v042 {path.stem.replace('_', ' ').title()}\n\nNo external web research used; local artifacts were sufficient.\n", encoding="utf-8")
    write_json(
        PACKAGE_ROOT / "source_manifest.json",
        {
            "generated_at": utc_now(),
            "package": "v042_fp8_postprocessed_scoring_autonomous",
            "source_artifacts": [
                str(PARENT_ROOT / "v041_fp8_prediction_only_duplicate_suppression/final_recommendation.md"),
                str(PARENT_ROOT / "v041_fp8_prediction_only_duplicate_suppression/best_prediction_only_rule.md"),
                str(PARENT_ROOT / "v041_fp8_prediction_only_duplicate_suppression/removed_prediction_audit.csv"),
                str(PARENT_ROOT / "v040_fp8_experiment_only_duplicate_postprocessing/final_recommendation.md"),
                str(PARENT_ROOT / "v039_fp8_containment_first_duplicate_suppression/final_recommendation.md"),
                str(V034_PACKAGE / "final_recommendation.md"),
                "z_reference_docs/GPT-Pro_collab/bda_svc_qwen_prompt_engineering_deep_research_bundle.md",
                "z_reference_docs/GPT-Pro_collab/CODEX_QWEN_PROMPT_ENGINEERING_DIRECTION_2026-05-06.md",
            ],
            "graphify_recall": {
                "attempted": True,
                "status": "blocked",
                "error": "ModuleNotFoundError: No module named 'networkx'",
            },
            "hard_boundaries": {
                "no_promotion": True,
                "no_product_truth_mutation": True,
                "no_runtime_code_mutation": True,
                "no_eval_ground_truth_mutation": True,
                "no_v024o_scored_evidence": True,
                "no_graphify_or_mem0_update": True,
            },
        },
    )
    write_json(
        PACKAGE_ROOT / "model_line_manifest.json",
        {
            "generated_at": utc_now(),
            "model_line": "qwen3-vl-8b-instruct-fp8-vllm",
            "backend": BACKEND,
            "raw_prompt_working_best": {"candidate": "v034a_fp8_broad_context_scene_box_guard", **RAW_V034A},
            "composite_working_best": {"candidate": "v034a_fp8_broad_context_scene_box_guard+p1753", **COMPOSITE_V034A_P1753},
            "old_product_reference": OLD_V020C,
            "not_product_replacement": True,
        },
    )
    rule = {**asdict(P1753), "oracle_fields_used": []}
    write_json(PACKAGE_ROOT / "postprocessing_rule_spec.json", {"generated_at": utc_now(), "rule": rule})
    (PACKAGE_ROOT / "postprocessing_rule_spec.md").write_text(
        "# p1753 Postprocessing Rule Spec\n\n"
        "Experiment-only deployable prediction-only duplicate suppression rule.\n\n"
        "- containment >= 0.8\n"
        "- IoU >= 0.0\n"
        "- area ratio <= 0.03\n"
        "- center-inside required\n"
        "- same-label required\n"
        "- cross-label disabled\n"
        "- keep-largest-only enabled\n"
        "- never suppress if the smaller prediction contains another prediction\n"
        "- no reference/eval/oracle fields used at inference time\n",
        encoding="utf-8",
    )
    write_json(
        PACKAGE_ROOT / "postprocessing_wrapper.json",
        {
            "generated_at": utc_now(),
            "script": str(PACKAGE_ROOT / "scripts/run_v042_postprocessed_scoring.py"),
            "wrapper_behavior": [
                "load prediction reports",
                "apply p1753 geometry suppression",
                "write postprocessed reports under postprocessed_outputs",
                "score raw and postprocessed reports with bda_eval matching helpers",
                "audit removals after scoring for TP/FP effect",
            ],
            "product_runtime_modified": False,
        },
    )
    (PACKAGE_ROOT / "postprocessing_wrapper.md").write_text(
        "# v042 Postprocessing Wrapper\n\n"
        "The wrapper is experiment-only. It applies `p1753` to saved prediction JSON files, writes postprocessed copies, "
        "and scores raw plus postprocessed outputs. The rule itself uses only prediction geometry and target type labels; "
        "ground truth is used only after suppression for evaluation/audit.\n",
        encoding="utf-8",
    )
    write_json(
        PACKAGE_ROOT / "backend_preflight.json",
        preflight
        or {
            "generated_at": utc_now(),
            "backend": BACKEND,
            "status": "not_yet_run",
            "timeout_policy": {
                "per_request_timeout_seconds": REQUEST_TIMEOUT_SECONDS,
                "max_retries": MAX_RETRIES,
                "cooldown_seconds": RETRY_COOLDOWN_SECONDS,
            },
        },
    )
    (PACKAGE_ROOT / "README.md").write_text(
        "# v042 FP8 Postprocessed-Scoring Autonomous\n\n"
        "Experiment-only FP8 vLLM prompt-refinement tranche using deployable prediction-only postprocessor `p1753` as a scoring layer.\n\n"
        "- Raw prompt working best: `v034a = 181 / 38 / 25 / 63`.\n"
        "- Composite working best: `v034a + p1753 = 181 / 38 / 24 / 62`.\n"
        "- Old/product reference remains non-FP8 `v020c = 186 / 33 / 25 / 58`.\n\n"
        "No product runtime, doctrine, assessment prompt, eval truth, or source-truth files are modified by this tranche.\n",
        encoding="utf-8",
    )


def write_closeout(records: dict[str, Any], final_status: str, next_axis: str) -> None:
    candidate_records = [records[key] for key in ["p1753_reproduction", "baseline_sentinel", "candidate_micro", "candidate_full"] if key in records]
    rows = [
        {
            "candidate_id": "old_product_v020c_reference",
            "stage": "prior_non_fp8_all_current",
            "raw_metrics": OLD_V020C,
            "postprocessed_metrics": None,
            "status": "product_reference_not_replaced",
        },
        {
            "candidate_id": "v034a_fp8_broad_context_scene_box_guard",
            "stage": "v034_full_all_current_raw",
            "raw_metrics": RAW_V034A,
            "postprocessed_metrics": None,
            "case_66_raw_post": "8/0/5 -> n/a",
            "case_67_raw_post": "10/1/3 -> n/a",
            "case_84_raw_post": "8/5/0 -> n/a",
            "case_100_raw_post": "n/a -> n/a",
            "case_110_raw_post": "3/4/1 -> n/a",
            "case_155_raw_post": "2/0/1 -> n/a",
            "case_166_raw_post": "1/0/0 -> n/a",
            "status": "raw_fp8_prompt_working_best",
        },
        {
            "candidate_id": "v034a_fp8_broad_context_scene_box_guard+p1753",
            "stage": "v041_reproduced_postprocessed",
            "raw_metrics": RAW_V034A,
            "postprocessed_metrics": COMPOSITE_V034A_P1753,
            "status": "composite_working_best",
        },
    ]
    for record in candidate_records:
        rows.append(
            {
                "candidate_id": record.get("candidate_id", "p1753_reproduction"),
                "stage": record.get("stage", "offline_reproduction"),
                "raw_metrics": record.get("raw_metrics"),
                "postprocessed_metrics": record.get("postprocessed_metrics"),
                "case_66_raw_post": f"{record.get('raw_case_metrics', {}).get('66', 'n/a')} -> {record.get('postprocessed_case_metrics', {}).get('66', 'n/a')}",
                "case_67_raw_post": f"{record.get('raw_case_metrics', {}).get('67', 'n/a')} -> {record.get('postprocessed_case_metrics', {}).get('67', 'n/a')}",
                "case_84_raw_post": f"{record.get('raw_case_metrics', {}).get('84', 'n/a')} -> {record.get('postprocessed_case_metrics', {}).get('84', 'n/a')}",
                "case_100_raw_post": f"{record.get('raw_case_metrics', {}).get('100', 'n/a')} -> {record.get('postprocessed_case_metrics', {}).get('100', 'n/a')}",
                "case_110_raw_post": f"{record.get('raw_case_metrics', {}).get('110', 'n/a')} -> {record.get('postprocessed_case_metrics', {}).get('110', 'n/a')}",
                "case_155_raw_post": f"{record.get('raw_case_metrics', {}).get('155', 'n/a')} -> {record.get('postprocessed_case_metrics', {}).get('155', 'n/a')}",
                "case_166_raw_post": f"{record.get('raw_case_metrics', {}).get('166', 'n/a')} -> {record.get('postprocessed_case_metrics', {}).get('166', 'n/a')}",
                "removed_predictions": record.get("postprocess_removed_predictions"),
                "removed_true_positives": record.get("postprocess_removed_true_positives"),
                "status": records.get(f"{record.get('candidate_id')}_status", "complete"),
            }
        )

    write_json(PACKAGE_ROOT / "comparison_matrix.json", {"generated_at": utc_now(), "rows": rows})
    (PACKAGE_ROOT / "comparison_matrix.md").write_text(
        "# v042 Comparison Matrix\n\n"
        "| Candidate | Stage | Raw | Postprocessed | Case 66 | Case 67 | Case 84 | Case 100 | Case 110 | Case 155 | Case 166 | Removed | Removed TPs | Status |\n"
        "|---|---|---|---|---|---|---|---|---|---|---|---:|---:|---|\n"
        + "\n".join(
            "| `{candidate_id}` | {stage} | `{raw}` | `{post}` | `{c66}` | `{c67}` | `{c84}` | `{c100}` | `{c110}` | `{c155}` | `{c166}` | {removed} | {removed_tp} | {status} |".format(
                candidate_id=row["candidate_id"],
                stage=row["stage"],
                raw=metrics_string(row.get("raw_metrics")),
                post=metrics_string(row.get("postprocessed_metrics")),
                c66=row.get("case_66_raw_post", "n/a"),
                c67=row.get("case_67_raw_post", "n/a"),
                c84=row.get("case_84_raw_post", "n/a"),
                c100=row.get("case_100_raw_post", "n/a"),
                c110=row.get("case_110_raw_post", "n/a"),
                c155=row.get("case_155_raw_post", "n/a"),
                c166=row.get("case_166_raw_post", "n/a"),
                removed=row.get("removed_predictions", "n/a"),
                removed_tp=row.get("removed_true_positives", "n/a"),
                status=row.get("status", "n/a"),
            )
            for row in rows
        )
        + "\n",
        encoding="utf-8",
    )
    write_json(PACKAGE_ROOT / "candidate_registry.json", {"generated_at": utc_now(), "candidates": rows})
    (PACKAGE_ROOT / "live_metrics_log.md").write_text(
        "# v042 Live Metrics Log\n\n"
        + "\n".join(
            f"- `{row['candidate_id']}` `{row['stage']}` raw `{metrics_string(row.get('raw_metrics'))}` post `{metrics_string(row.get('postprocessed_metrics'))}` status `{row.get('status', 'n/a')}`"
            for row in rows
        )
        + "\n",
        encoding="utf-8",
    )
    best_raw = "v034a_fp8_broad_context_scene_box_guard"
    best_post = "v034a_fp8_broad_context_scene_box_guard+p1753"
    best_post_metrics = COMPOSITE_V034A_P1753
    best_raw_metrics = RAW_V034A
    for record in candidate_records:
        raw = record.get("raw_metrics") or {}
        post = record.get("postprocessed_metrics") or {}
        if raw.get("combined_errors") is not None and raw["combined_errors"] < best_raw_metrics["combined_errors"]:
            best_raw = record.get("candidate_id", best_raw)
            best_raw_metrics = raw
        if (
            post.get("combined_errors") is not None
            and post["combined_errors"] < best_post_metrics["combined_errors"]
            and record.get("postprocess_removed_true_positives") == 0
        ):
            best_post = record.get("candidate_id", best_post)
            best_post_metrics = post
    beat_composite = best_post_metrics["combined_errors"] < COMPOSITE_V034A_P1753["combined_errors"]
    beat_old = best_post_metrics["combined_errors"] <= OLD_V020C["combined_errors"]
    target = best_post_metrics["combined_errors"] <= 1
    final_payload = {
        "generated_at": utc_now(),
        "status": final_status,
        "best_raw_fp8_candidate": best_raw,
        "best_raw_metrics": best_raw_metrics,
        "best_postprocessed_fp8_candidate": best_post,
        "best_postprocessed_metrics": best_post_metrics,
        "beat_composite_62": beat_composite,
        "reached_or_beat_old_v020c_58": beat_old,
        "target_le_1_reached": target,
        "p1753_behavior": {
            "rule_id": "p1753",
            "v034a_removed_predictions": records.get("p1753_reproduction", {}).get("postprocess_removed_predictions"),
            "v034a_removed_true_positives": records.get("p1753_reproduction", {}).get("postprocess_removed_true_positives"),
            "v034a_removed_cases": sorted({row["case_id"] for row in records.get("p1753_reproduction", {}).get("removals", [])}),
        },
        "postprocessed_scoring_should_continue": final_status not in {"p1753_reproduction_failed", "runtime_invalid"},
        "blocked_until_backend_repair": final_status == "backend_unavailable",
        "hard_boundaries_preserved": True,
        "next_axis": next_axis,
    }
    write_json(PACKAGE_ROOT / "final_recommendation.json", final_payload)
    (PACKAGE_ROOT / "final_recommendation.md").write_text(
        "# v042 Final Recommendation\n\n"
        f"Generated: `{utc_now()}`\n\n"
        f"Status: `{final_status}`.\n\n"
        f"Best raw FP8 candidate: `{best_raw}` at `{metrics_string(best_raw_metrics)}`.\n\n"
        f"Best postprocessed FP8 candidate: `{best_post}` at `{metrics_string(best_post_metrics)}`.\n\n"
        f"Beat composite 62 errors: `{beat_composite}`.\n"
        f"Reached or beat old 58-error reference: `{beat_old}`.\n"
        f"Reached <=1 target: `{target}`.\n\n"
        "p1753 behavior: prediction-only same-label containment-first suppression; on frozen v034a it removes one case-88 FP and zero TPs.\n\n"
        f"Next axis: {next_axis}\n\n"
        "FP8 remains a separate model line. This is experiment-only scoring evidence, not product runtime or promotion.\n",
        encoding="utf-8",
    )
    (PACKAGE_ROOT / "lessons_learned.md").write_text(
        "# v042 Lessons Learned\n\n"
        "- p1753 is deployable prediction-only geometry and must reproduce v041 before any prompt candidate is trusted.\n"
        "- Composite scoring can hide raw prompt regressions, so every candidate keeps raw and postprocessed metrics side by side.\n"
        "- The next prompt gain should target residual FNs or FPs that p1753 does not touch; duplicate wording from v037 remains avoided.\n"
        "- Case 67 and case 84 remain the main dense/recall safety gates.\n",
        encoding="utf-8",
    )
    (PACKAGE_ROOT / "strategy_state.md").write_text(
        "# v042 Strategy State\n\n"
        f"- Raw prompt working best: `{best_raw}` at `{metrics_string(best_raw_metrics)}`.\n"
        f"- Composite working best: `{best_post}` at `{metrics_string(best_post_metrics)}`.\n"
        f"- Final status: `{final_status}`.\n"
        f"- Next axis: {next_axis}\n",
        encoding="utf-8",
    )
    (PACKAGE_ROOT / "recovery_log.md").write_text(
        "# v042 Recovery Log\n\n"
        "- Re-grounded in v041/v040/v039/v034 local artifacts.\n"
        "- Graphify recall was attempted but blocked by missing local `networkx`; source artifacts were used directly.\n"
        "- Created p1753 experiment-only wrapper and reproduction gate.\n"
        "- Preserved no-promotion and no-product-mutation boundaries.\n",
        encoding="utf-8",
    )
    write_json(PACKAGE_ROOT / "recovery_log.json", {"generated_at": utc_now(), "records": sorted(records.keys()), "final_status": final_status})
    diagnosis = PACKAGE_ROOT / "diagnoses/v042a_fp8_case84_low_contrast_recall_probe_diagnosis.md"
    candidate = records.get("candidate_full") or records.get("candidate_micro")
    diagnosis.write_text(
        "# v042a Diagnosis\n\n"
        "What did this candidate test? A narrow low-contrast/smoke-softened visible-body recall cue scored raw and through p1753.\n\n"
        "What changed from current working best? One GOOD FINAL BOX line was added. The v020c extra-box audit and v034a broad-context guard were preserved.\n\n"
        f"Candidate result available: `{bool(candidate)}`.\n\n"
        f"Raw metrics: `{metrics_string(candidate.get('raw_metrics') if candidate else None)}`.\n\n"
        f"Postprocessed metrics: `{metrics_string(candidate.get('postprocessed_metrics') if candidate else None)}`.\n\n"
        f"Next hypothesis: {next_axis}\n",
        encoding="utf-8",
    )


def validate_generated_files() -> dict[str, Any]:
    json_files = sorted(PACKAGE_ROOT.glob("**/*.json"))
    csv_files = sorted(PACKAGE_ROOT.glob("**/*.csv"))
    yaml_files = sorted(PACKAGE_ROOT.glob("**/*.yaml")) + sorted(PACKAGE_ROOT.glob("**/*.yml"))
    errors: list[str] = []
    for path in json_files:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"json:{path}:{exc!r}")
    for path in csv_files:
        try:
            with path.open("r", encoding="utf-8", newline="") as handle:
                list(csv.reader(handle))
        except Exception as exc:
            errors.append(f"csv:{path}:{exc!r}")
    for path in yaml_files:
        try:
            yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"yaml:{path}:{exc!r}")
    result = {
        "generated_at": utc_now(),
        "json_files": len(json_files),
        "csv_files": len(csv_files),
        "yaml_files": len(yaml_files),
        "errors": errors,
        "ok": not errors,
        "baseline_confirmations": {
            "old_v020c": OLD_V020C,
            "raw_v034a": RAW_V034A,
            "p1753_on_v034a": COMPOSITE_V034A_P1753,
            "v040_hybrid_oracle_non_deployable": V040_HYBRID_ORACLE,
            "v024o_unscored": True,
        },
    }
    write_json(PACKAGE_ROOT / "validation_report.json", result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", action="store_true", help="Run scaffold, p1753 reproduction, backend preflight, and v042a if gates pass.")
    args = parser.parse_args()
    if not args.run:
        parser.print_help()
        return 0

    PACKAGE_ROOT.mkdir(parents=True, exist_ok=True)
    write_scaffold()
    create_sentinel_manifest()
    baseline_overlay = create_baseline_overlay_copy()
    candidate_overlay = create_v042a_overlay()

    records: dict[str, Any] = {}
    p1753_record = reproduce_p1753()
    p1753_record["candidate_id"] = "v034a_fp8_broad_context_scene_box_guard+p1753"
    p1753_record["stage"] = "frozen_v034a_reproduction"
    records["p1753_reproduction"] = p1753_record
    repro_ok = p1753_reproduction_ok(p1753_record)
    print_status(
        "p1753_reproduction",
        p1753_record,
        "pass" if repro_ok else "fail",
        "p1753 reproduction must match v041 before prompt autonomy is trusted.",
        "Proceed to backend preflight." if repro_ok else "Stop and diagnose p1753 wrapper drift.",
    )
    if not repro_ok:
        write_closeout(records, "p1753_reproduction_failed", "Diagnose p1753 wrapper drift against v041 before any prompt candidate.")
        validate_generated_files()
        return 1

    models = fetch_models()
    preflight = {
        "generated_at": utc_now(),
        "backend": BACKEND,
        "models": models,
        "status": "pass" if models["ok"] and models["model_present"] else "fail",
        "timeout_policy": {
            "per_request_timeout_seconds": REQUEST_TIMEOUT_SECONDS,
            "max_retries": MAX_RETRIES,
            "cooldown_seconds": RETRY_COOLDOWN_SECONDS,
        },
        "p1753_reproduction": {
            "status": "pass",
            "raw_metrics": p1753_record["raw_metrics"],
            "postprocessed_metrics": p1753_record["postprocessed_metrics"],
        },
    }
    write_scaffold(preflight)
    print_status(
        "backend_preflight",
        None,
        preflight["status"],
        "Backend must expose the official FP8 model before live prompt candidates can run.",
        "Run v034a sentinel replay." if preflight["status"] == "pass" else "Stop and leave exact backend repair requirement.",
    )
    if preflight["status"] != "pass":
        write_closeout(records, "backend_unavailable", "Restart or repair the vLLM FP8 endpoint at http://localhost:8000/v1 before v042 autonomy can continue.")
        validate_generated_files()
        return 0

    baseline = {"candidate_id": "v042_baseline_exact_v034a_replay", "overlay_path": str(baseline_overlay), "intended_changes": []}
    candidate = {
        "candidate_id": "v042a_fp8_case84_low_contrast_recall_probe",
        "overlay_path": str(candidate_overlay),
        "intended_changes": read_yaml(candidate_overlay).get("intended_changes", []),
    }

    records["baseline_sentinel"] = run_case_probe(baseline, SENTINEL_MANIFEST, "micro_pack_only")
    baseline_office = run_office_guard(baseline, "baseline")
    records["baseline_office"] = baseline_office["run_record"]
    records["v042_baseline_exact_v034a_replay_status"] = "baseline_replay"
    if records["baseline_sentinel"].get("runtime_invalid") or not baseline_office["pass"]:
        print_status(
            "baseline_sentinel",
            records["baseline_sentinel"],
            "fail",
            "The v034a backend replay is unstable or office-negative failed.",
            "Stop prompt mutation and repair backend/runtime stability.",
        )
        write_closeout(records, "baseline_replay_failed", "Repair backend/runtime stability before authoring another v042 candidate.")
        validate_generated_files()
        return 0
    print_status(
        "baseline_sentinel",
        records["baseline_sentinel"],
        "pass",
        "v034a sentinel replay completed on the FP8 backend with p1753 paired scoring.",
        "Run v042a micro-pack.",
    )

    records["candidate_micro"] = run_case_probe(candidate, SENTINEL_MANIFEST, "micro_pack_only")
    candidate_office = run_office_guard(candidate, "v042a")
    records["candidate_micro_office"] = candidate_office["run_record"]
    micro_ok, micro_reason = micro_pass(records["candidate_micro"], candidate_office["pass"])
    if not micro_ok:
        status = "runtime_invalid" if micro_reason == "runtime_invalid" else "rejected"
        records["v042a_fp8_case84_low_contrast_recall_probe_status"] = status
        print_candidate_block(
            records["candidate_micro"],
            "micro_pack_only",
            status,
            f"v042a failed the postprocessed micro gate: {micro_reason}.",
            "Diagnose the exact raw/post deltas before any next prompt axis.",
            candidate_office["pass"],
        )
        write_closeout(records, status, "Use v042a raw/post micro deltas to decide whether case-84 recall wording is too broad or whether a different residual-FP axis is safer.")
        validate_generated_files()
        return 0

    print_candidate_block(
        records["candidate_micro"],
        "micro_pack_only",
        "learning_evidence",
        "v042a passed the postprocessed micro gate; full all-current is required.",
        "Run full all-current/no101 with raw and p1753 postprocessed scoring.",
        candidate_office["pass"],
    )

    records["candidate_full"] = run_case_probe(candidate, ALL_CURRENT_MANIFEST, "full_all_current")
    candidate_full_office = run_office_guard(candidate, "v042a_full")
    records["candidate_full_office"] = candidate_full_office["run_record"]
    status = status_for_record(records["candidate_full"], candidate_full_office["pass"], "full_all_current")
    records["v042a_fp8_case84_low_contrast_recall_probe_status"] = status
    next_axis = (
        "If v042a beats composite 62, continue from it with exact remaining deltas; "
        "otherwise pivot to residual FP pressure without dense-fragment or same-wreck duplicate wording."
    )
    print_candidate_block(
        records["candidate_full"],
        "full_all_current",
        status,
        "v042a completed full all-current with paired raw/postprocessed scoring.",
        next_axis,
        candidate_full_office["pass"],
    )
    write_closeout(records, status, next_axis)
    validate_generated_files()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
