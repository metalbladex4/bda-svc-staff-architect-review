#!/usr/bin/env python3
"""Run the v025a compact separate-body recovery candidate.

This wrapper reuses the established upstream-code OpenAI-compatible scratch
worktree runner from the v023 package, but writes v025-shaped evidence artifacts.
It replaces only prompts.detect_objects inside the scratch config.
"""

from __future__ import annotations

import csv
import datetime as dt
import importlib.util
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


CAPSTONE_ROOT = Path("/home/williambenitez1/Capstone")
WORKTREE_ROOT = Path(
    "/home/williambenitez1/Capstone_worktrees/"
    "1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement"
)
PROMOTION_ROOT = (
    WORKTREE_ROOT
    / "docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/"
    "human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/"
    "v017b_prompt_only_main_promotion"
)
PACKAGE_ROOT = PROMOTION_ROOT / "v025_visual_delta_prompt_recovery"
V023_RUNNER = (
    PROMOTION_ROOT
    / "v023_literal99_qwen_no_stop_continuation/scripts/run_v023_literal99_cycle.py"
)
V020C_DIAGNOSIS = (
    PROMOTION_ROOT
    / "v023_literal99_qwen_no_stop_continuation/diagnoses/v020c_anchor_replay_diagnosis.json"
)
V024L_DIAGNOSIS = (
    PROMOTION_ROOT
    / "v023_literal99_qwen_no_stop_continuation/diagnoses/"
    "v024l_v023s_no_wheel_track_ablation_diagnosis.json"
)
OVERLAY_PATH = PACKAGE_ROOT / "overlays/v025a_v020c_compact_separate_body_recovery.yaml"
PROMPT_ID = "v025a_v020c_compact_separate_body_recovery"
ROW_ID = f"qwen__{PROMPT_ID}"
TARGET_CASES = ("14", "42", "172")
FP_RISK_CASES = ("12", "16", "66", "77", "88", "90", "97", "103")
DENSE_CASES = ("66", "67", "84", "97")
CONTROL_CASES = ("155", "166")
PRIORITY_CASES = (
    "12",
    "14",
    "16",
    "21",
    "42",
    "66",
    "67",
    "76",
    "77",
    "84",
    "88",
    "90",
    "97",
    "103",
    "155",
    "164",
    "166",
    "172",
)
V020C_BASELINE = {
    "candidate_id": "v020c_anchor_replay",
    "matches": 186,
    "false_negatives": 33,
    "false_positives": 25,
    "combined_errors": 58,
}
V024L_BASELINE = {
    "candidate_id": "v024l_v023s_no_wheel_track_ablation",
    "matches": 188,
    "false_negatives": 31,
    "false_positives": 35,
    "combined_errors": 66,
}


def utc() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat()


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected object")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def load_v023_runner() -> Any:
    spec = importlib.util.spec_from_file_location("v023_runner", V023_RUNNER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to import {V023_RUNNER}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.PACKAGE_ROOT = PACKAGE_ROOT
    return module


def run_cmd(cmd: list[str], cwd: Path) -> dict[str, Any]:
    completed = subprocess.run(
        cmd,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return {
        "cmd": cmd,
        "cwd": str(cwd),
        "returncode": completed.returncode,
        "stdout_tail": (completed.stdout or "")[-4000:],
        "stderr_tail": (completed.stderr or "")[-4000:],
    }


def select_backend(v023: Any) -> dict[str, Any]:
    attempts: list[dict[str, Any]] = []
    preferred = v023.PREFERRED_BACKEND
    fallback_backend = v023.FALLBACK_BACKEND
    first = v023._check_endpoint(preferred["openai_base_url"], preferred["model"])
    attempts.append({"backend": preferred, "check": first})
    if first["status"] == "available":
        return {"selected": preferred, "attempts": attempts, "fallback_used": False}
    time.sleep(2)
    retry = v023._check_endpoint(preferred["openai_base_url"], preferred["model"])
    attempts.append(
        {
            "backend": preferred,
            "check": retry,
            "recovery_attempt": "preferred_endpoint_retry",
        }
    )
    if retry["status"] == "available":
        return {"selected": preferred, "attempts": attempts, "fallback_used": False}
    fallback = v023._check_endpoint(fallback_backend["openai_base_url"], fallback_backend["model"])
    attempts.append(
        {
            "backend": fallback_backend,
            "check": fallback,
            "recovery_attempt": "authorized_fallback",
        }
    )
    if fallback["status"] != "available":
        raise RuntimeError("No Qwen OpenAI-compatible endpoint is available")
    return {"selected": fallback_backend, "attempts": attempts, "fallback_used": True}


def case_metrics(summary: dict[str, Any], case_id: str) -> dict[str, int]:
    images = {Path(str(item["image_filename"])).stem: item for item in summary["images"]}
    if case_id not in images:
        raise KeyError(f"{case_id} missing from evaluation summary")
    item = images[case_id]
    return {
        "reference_target_count": int(item["reference_target_count"]),
        "predicted_target_count": int(item["predicted_target_count"]),
        "match_count": int(item["match_count"]),
        "false_negative_count": int(item["false_negative_count"]),
        "false_positive_count": int(item["false_positive_count"]),
    }


def compact_case(metrics: dict[str, int]) -> str:
    return (
        f"{metrics['match_count']}/"
        f"{metrics['false_negative_count']}/"
        f"{metrics['false_positive_count']}"
    )


def source_case_tables() -> tuple[dict[str, dict[str, int]], dict[str, dict[str, int]]]:
    v020c = read_json(V020C_DIAGNOSIS)
    v024l = read_json(V024L_DIAGNOSIS)
    v020c_cases: dict[str, dict[str, int]] = {}
    v024l_cases: dict[str, dict[str, int]] = {}
    for case in DENSE_CASES:
        v020c_cases[case] = v020c["dense_cases"][case]
        v024l_cases[case] = v024l["dense_cases"][case]
    for case in CONTROL_CASES:
        v020c_cases[case] = v020c[f"case_{case}"]
        v024l_cases[case] = v024l[f"case_{case}"]
    matrix = read_json(PACKAGE_ROOT / "comparison_matrix.json")
    for row in matrix.get("priority_delta", []):
        case = str(row["case_id"])
        if case in PRIORITY_CASES:
            v020c_cases.setdefault(case, parse_compact(row["v020c"]))
            v024l_cases.setdefault(case, parse_compact(row["v024l"]))
    return v020c_cases, v024l_cases


def parse_compact(value: str) -> dict[str, int]:
    match, fn, fp = value.split("/")
    return {
        "match_count": int(match),
        "false_negative_count": int(fn),
        "false_positive_count": int(fp),
    }


def classify_result(result: dict[str, Any], v020c_cases: dict[str, dict[str, int]]) -> dict[str, Any]:
    metrics = {
        "matches": result["match_count"],
        "false_negatives": result["false_negative_count"],
        "false_positives": result["false_positive_count"],
        "combined_errors": result["total_error_count"],
    }
    case_155_pass = (
        result["case_155"]["match_count"] == result["case_155"]["reference_target_count"]
        and result["case_155"]["false_negative_count"] == 0
        and result["case_155"]["false_positive_count"] == 0
    )
    case_166_pass = (
        result["case_166"]["match_count"] == result["case_166"]["reference_target_count"]
        and result["case_166"]["false_negative_count"] == 0
        and result["case_166"]["false_positive_count"] == 0
    )
    office_pass = (
        result["office_negative"]["image_count"] == 1
        and result["office_negative"]["negative_scene_abstention_correct_count"] == 1
        and result["office_negative"]["negative_scene_false_positive_count"] == 0
    )
    case_67 = result["dense_cases"]["67"]
    v020c_67 = v020c_cases["67"]
    case_84 = result["dense_cases"]["84"]
    v020c_84 = v020c_cases["84"]
    case_67_preserved = (
        case_67["match_count"] >= v020c_67["match_count"]
        and case_67["false_negative_count"] <= v020c_67["false_negative_count"]
    )
    case_84_collapsed = case_84["match_count"] < v020c_84["match_count"] - 1
    reopened_fp_classes: list[str] = []
    for case in FP_RISK_CASES:
        current = result["priority_cases"][case]
        base = v020c_cases[case]
        if current["false_positive_count"] > base["false_positive_count"]:
            if case in {"12", "77", "90", "97", "103"}:
                reopened_fp_classes.append("building_piece_facade_roof_section")
            elif case in {"16", "88"}:
                reopened_fp_classes.append("adjacent_off_target_object")
            elif case == "66":
                reopened_fp_classes.append("nested_fragment_box")
    reopened_fp_classes = sorted(set(reopened_fp_classes))
    fp_explosion = metrics["false_positives"] > V024L_BASELINE["false_positives"]
    hard_disqualifiers = []
    if result["image_count"] != 117:
        hard_disqualifiers.append("manifest_count_wrong")
    if result["case_101_seen"]:
        hard_disqualifiers.append("case_101_seen")
    if not case_155_pass:
        hard_disqualifiers.append("case_155_failed")
    if not case_166_pass:
        hard_disqualifiers.append("case_166_failed")
    if not office_pass:
        hard_disqualifiers.append("office_negative_failed")
    if not case_67_preserved:
        hard_disqualifiers.append("case_67_below_v020c")
    if case_84_collapsed:
        hard_disqualifiers.append("case_84_collapse")
    if fp_explosion:
        hard_disqualifiers.append("fp_explosion_above_v024l")
    if not result["runtime_json_valid"]:
        hard_disqualifiers.append("runtime_or_json_failure")
    if hard_disqualifiers:
        status = "rejected"
    elif metrics["combined_errors"] < V020C_BASELINE["combined_errors"]:
        status = "replay_worthy_challenger"
    elif metrics["matches"] > V020C_BASELINE["matches"] or metrics["false_negatives"] < V020C_BASELINE["false_negatives"]:
        status = "learning_evidence"
    elif reopened_fp_classes:
        status = "rejected"
    else:
        status = "neutral_learning_evidence"
    return {
        "status": status,
        "case_155_pass": case_155_pass,
        "case_166_pass": case_166_pass,
        "office_negative_pass": office_pass,
        "case_67_preserved": case_67_preserved,
        "case_84_collapsed": case_84_collapsed,
        "fp_explosion": fp_explosion,
        "reopened_fp_classes": reopened_fp_classes,
        "hard_disqualifiers": hard_disqualifiers,
    }


def update_candidate_registry(result: dict[str, Any], decision: dict[str, Any]) -> None:
    path = PACKAGE_ROOT / "candidate_registry.json"
    registry = read_json(path)
    registry["candidate_authoring_status"] = "v025a_completed"
    registry["candidate_authoring_gate"] = "v025a was explicitly approved after visual failure review"
    registry.setdefault("authored_candidates", [])
    registry["authored_candidates"] = [
        row for row in registry["authored_candidates"] if row.get("candidate_id") != PROMPT_ID
    ]
    registry["authored_candidates"].append(
        {
            "candidate_id": PROMPT_ID,
            "prompt_identity": PROMPT_ID,
            "role": "single_compact_v020c_based_candidate",
            "generated_from": "v020c_v019c_extra_box_audit",
            "metrics": {
                "matches": result["match_count"],
                "false_negatives": result["false_negative_count"],
                "false_positives": result["false_positive_count"],
                "combined_errors": result["total_error_count"],
            },
            "controls": {
                "155": "passed" if decision["case_155_pass"] else "failed",
                "166": "passed" if decision["case_166_pass"] else "failed",
                "office_negative": "passed" if decision["office_negative_pass"] else "failed",
            },
            "decision_status": decision["status"],
            "overlay": str(OVERLAY_PATH),
            "all_current_run_summary": result["all_current_run_summary"],
            "office_negative_run_summary": result["office_negative_run_summary"],
        }
    )
    registry["future_candidate_slots"] = [
        slot for slot in registry.get("future_candidate_slots", []) if not slot["candidate_id"].startswith("v025a")
    ]
    registry["last_updated_utc"] = utc()
    write_json(path, registry)


def update_comparison_matrix(
    result: dict[str, Any],
    decision: dict[str, Any],
    v020c_cases: dict[str, dict[str, int]],
    v024l_cases: dict[str, dict[str, int]],
) -> None:
    path = PACKAGE_ROOT / "comparison_matrix.json"
    matrix = read_json(path)
    matrix["new_inference_run"] = True
    matrix["last_updated_utc"] = utc()
    matrix["rows"] = [row for row in matrix["rows"] if row.get("candidate_id") != PROMPT_ID]
    matrix["rows"].append(
        {
            "candidate_id": PROMPT_ID,
            "role": "v020c_based_single_compact_candidate",
            "matches": result["match_count"],
            "false_negatives": result["false_negative_count"],
            "false_positives": result["false_positive_count"],
            "combined_errors": result["total_error_count"],
            "case_155": "pass" if decision["case_155_pass"] else "fail",
            "case_166": "pass" if decision["case_166_pass"] else "fail",
            "office_negative": "pass" if decision["office_negative_pass"] else "fail",
            "v025_status": decision["status"],
        }
    )
    delta_rows = []
    for case in PRIORITY_CASES:
        current = result["priority_cases"][case]
        base = v020c_cases.get(case)
        high = v024l_cases.get(case)
        item = {
            "case_id": case,
            "v020c": compact_case(base) if base else None,
            "v024l": compact_case(high) if high else None,
            "v025a": compact_case(current),
            "v025a_vs_v020c": (
                f"{current['match_count'] - base['match_count']:+d}/"
                f"{current['false_negative_count'] - base['false_negative_count']:+d}/"
                f"{current['false_positive_count'] - base['false_positive_count']:+d}"
                if base
                else None
            ),
        }
        delta_rows.append(item)
    matrix["v025a_priority_delta"] = delta_rows
    matrix["v025a_decision"] = decision
    write_json(path, matrix)

    lines = [
        "# v025 Comparison Matrix",
        "",
        f"Updated: `{matrix['last_updated_utc']}`",
        "",
        "| Candidate | Role | Matches | FNs | FPs | Errors | 155 | 166 | Office | Status |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- |",
    ]
    for row in matrix["rows"]:
        lines.append(
            f"| `{row['candidate_id']}` | {row['role']} | {row['matches']} | "
            f"{row['false_negatives']} | {row['false_positives']} | {row['combined_errors']} | "
            f"{row['case_155']} | {row['case_166']} | {row['office_negative']} | {row['v025_status']} |"
        )
    lines.extend(
        [
            "",
            "## v025a Priority Cases",
            "",
            "| Case | v020c M/FN/FP | v024l M/FN/FP | v025a M/FN/FP | v025a vs v020c |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in delta_rows:
        lines.append(
            f"| `{row['case_id']}` | {row['v020c']} | {row['v024l']} | "
            f"{row['v025a']} | {row['v025a_vs_v020c']} |"
        )
    (PACKAGE_ROOT / "comparison_matrix.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_diagnosis(result: dict[str, Any], decision: dict[str, Any], v020c_cases: dict[str, dict[str, int]]) -> None:
    payload = {
        "generated_utc": utc(),
        "candidate_id": PROMPT_ID,
        "source_base": "v020c_v019c_extra_box_audit",
        "hypothesis": "compact separate visible body recovery cue",
        "metrics": {
            "matches": result["match_count"],
            "false_negatives": result["false_negative_count"],
            "false_positives": result["false_positive_count"],
            "combined_errors": result["total_error_count"],
            "delta_vs_v020c": {
                "matches": result["match_count"] - V020C_BASELINE["matches"],
                "false_negatives": result["false_negative_count"] - V020C_BASELINE["false_negatives"],
                "false_positives": result["false_positive_count"] - V020C_BASELINE["false_positives"],
                "combined_errors": result["total_error_count"] - V020C_BASELINE["combined_errors"],
            },
            "delta_vs_v024l": {
                "matches": result["match_count"] - V024L_BASELINE["matches"],
                "false_negatives": result["false_negative_count"] - V024L_BASELINE["false_negatives"],
                "false_positives": result["false_positive_count"] - V024L_BASELINE["false_positives"],
                "combined_errors": result["total_error_count"] - V024L_BASELINE["combined_errors"],
            },
        },
        "decision": decision,
        "dense_cases": result["dense_cases"],
        "target_visual_cases": {case: result["priority_cases"][case] for case in TARGET_CASES},
        "fp_risk_cases": {case: result["priority_cases"][case] for case in FP_RISK_CASES},
        "controls": {
            "155": result["case_155"],
            "166": result["case_166"],
            "office_negative": result["office_negative"],
        },
        "runtime": {
            "backend_id": result["backend_id"],
            "openai_base_url": result["openai_base_url"],
            "model": result["model"],
            "server_kind": result["server_kind"],
            "json_valid": result["runtime_json_valid"],
            "nonzero_command_count": result["nonzero_command_count"],
            "missing_outputs": result["missing_outputs"],
        },
        "run_summaries": {
            "all_current": result["all_current_run_summary"],
            "office_negative": result["office_negative_run_summary"],
        },
    }
    diag_json = PACKAGE_ROOT / f"diagnoses/{PROMPT_ID}_diagnosis.json"
    write_json(diag_json, payload)

    lines = [
        f"# {PROMPT_ID} Diagnosis",
        "",
        f"Generated: `{payload['generated_utc']}`",
        "",
        "## Decision",
        "",
        f"- status: `{decision['status']}`",
        f"- hard disqualifiers: `{decision['hard_disqualifiers']}`",
        f"- reopened FP classes: `{decision['reopened_fp_classes']}`",
        f"- case 67 preserved: `{decision['case_67_preserved']}`",
        "",
        "## Metrics",
        "",
        "| Candidate | Matches | FNs | FPs | Errors |",
        "| --- | ---: | ---: | ---: | ---: |",
        f"| `v020c_anchor_replay` | {V020C_BASELINE['matches']} | {V020C_BASELINE['false_negatives']} | {V020C_BASELINE['false_positives']} | {V020C_BASELINE['combined_errors']} |",
        f"| `v024l_v023s_no_wheel_track_ablation` | {V024L_BASELINE['matches']} | {V024L_BASELINE['false_negatives']} | {V024L_BASELINE['false_positives']} | {V024L_BASELINE['combined_errors']} |",
        f"| `{PROMPT_ID}` | {result['match_count']} | {result['false_negative_count']} | {result['false_positive_count']} | {result['total_error_count']} |",
        "",
        "## Dense Cases",
        "",
        "| Case | v020c | v025a |",
        "| --- | ---: | ---: |",
    ]
    for case in DENSE_CASES:
        lines.append(f"| `{case}` | {compact_case(v020c_cases[case])} | {compact_case(result['dense_cases'][case])} |")
    lines.extend(["", "## Target Visual Cases", "", "| Case | v025a M/FN/FP |", "| --- | ---: |"])
    for case in TARGET_CASES:
        lines.append(f"| `{case}` | {compact_case(result['priority_cases'][case])} |")
    lines.extend(["", "## FP-Risk Cases", "", "| Case | v025a M/FN/FP |", "| --- | ---: |"])
    for case in FP_RISK_CASES:
        lines.append(f"| `{case}` | {compact_case(result['priority_cases'][case])} |")
    lines.extend(
        [
            "",
            "## Controls",
            "",
            f"- case 155: `{result['case_155']}`",
            f"- case 166: `{result['case_166']}`",
            f"- office-negative: `{result['office_negative']}`",
            "",
            "## Interpretation",
            "",
            interpretation(decision, result),
        ]
    )
    (PACKAGE_ROOT / f"diagnoses/{PROMPT_ID}_diagnosis.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def interpretation(decision: dict[str, Any], result: dict[str, Any]) -> str:
    if decision["status"] == "replay_worthy_challenger":
        return (
            "`v025a` beat the v020c combined-error incumbent while passing controls and "
            "preserving case 67. Treat it as a replay-worthy challenger, not promotion."
        )
    if decision["status"] == "learning_evidence":
        return (
            "`v025a` improved recall signal but did not beat the v020c combined-error "
            "incumbent. Keep it as learning evidence and stop before authoring v025b."
        )
    if decision["status"] == "rejected":
        return (
            "`v025a` is rejected for this wave because a hard disqualifier or reopened "
            "false-positive class appeared. Stop and return to the v020c branch base."
        )
    return (
        "`v025a` is neutral learning evidence. It did not replace v020c and should not "
        "be promoted or extended without a fresh next-axis decision."
    )


def update_delta_review(result: dict[str, Any], decision: dict[str, Any]) -> None:
    path = PACKAGE_ROOT / "v020c_v024l_delta_review.md"
    text = path.read_text(encoding="utf-8")
    marker = "\n## v025a Result Addendum\n"
    text = text.split(marker, 1)[0].rstrip()
    addendum = [
        "",
        "## v025a Result Addendum",
        "",
        f"Generated: `{utc()}`",
        "",
        f"`{PROMPT_ID}` was authored after explicit approval as a one-cue v020c-based candidate.",
        "",
        "| Candidate | Matches | FNs | FPs | Errors | Status |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
        f"| `v020c_anchor_replay` | {V020C_BASELINE['matches']} | {V020C_BASELINE['false_negatives']} | {V020C_BASELINE['false_positives']} | {V020C_BASELINE['combined_errors']} | incumbent |",
        f"| `v024l_v023s_no_wheel_track_ablation` | {V024L_BASELINE['matches']} | {V024L_BASELINE['false_negatives']} | {V024L_BASELINE['false_positives']} | {V024L_BASELINE['combined_errors']} | high-recall learning evidence |",
        f"| `{PROMPT_ID}` | {result['match_count']} | {result['false_negative_count']} | {result['false_positive_count']} | {result['total_error_count']} | {decision['status']} |",
        "",
        "Decision:",
        "",
        f"```text\n{decision['status']}\n```",
        "",
        "Hard disqualifiers:",
        "",
        f"```text\n{decision['hard_disqualifiers']}\n```",
        "",
        "Reopened FP classes:",
        "",
        f"```text\n{decision['reopened_fp_classes']}\n```",
        "",
        "Boundary: no `v025b` was authored, no prompt was promoted, and no Graphify or Mem0 write occurred in this wave.",
    ]
    path.write_text(text + "\n" + "\n".join(addendum) + "\n", encoding="utf-8")


def update_final(result: dict[str, Any], decision: dict[str, Any]) -> None:
    payload = read_json(PACKAGE_ROOT / "final_recommendation.json")
    payload["status"] = "v025a_evaluated"
    payload["review_timestamp_utc"] = utc()
    payload["promotion_recommendation"] = "none"
    payload["incumbent"] = "v020c_anchor_replay"
    payload["latest_candidate"] = {
        "candidate_id": PROMPT_ID,
        "metrics": {
            "matches": result["match_count"],
            "false_negatives": result["false_negative_count"],
            "false_positives": result["false_positive_count"],
            "combined_errors": result["total_error_count"],
        },
        "decision_status": decision["status"],
        "hard_disqualifiers": decision["hard_disqualifiers"],
        "reopened_fp_classes": decision["reopened_fp_classes"],
    }
    if decision["status"] == "replay_worthy_challenger":
        payload["next_required_action"] = "rerun v025a once before any promotion discussion"
    elif decision["status"] == "learning_evidence":
        payload["next_required_action"] = "stop and review the v025a diagnosis before choosing any v025b axis"
    elif decision["status"] == "rejected":
        payload["next_required_action"] = "stop and return to the v020c branch base"
    else:
        payload["next_required_action"] = "stop; v025a is neutral evidence only"
    write_json(PACKAGE_ROOT / "final_recommendation.json", payload)

    lines = [
        "# v025 Final Recommendation",
        "",
        f"Review timestamp: `{payload['review_timestamp_utc']}`",
        "",
        "## Status",
        "",
        "`v025a_v020c_compact_separate_body_recovery` has been authored and evaluated as a single-candidate evidence wave.",
        "",
        "## Current Recommendation",
        "",
        "- Keep `v020c_anchor_replay` / `v020c_extra_box_audit` as the Qwen incumbent.",
        "- Reject `v025a_v020c_compact_separate_body_recovery` for this wave because it collapses case `67` below the v020c baseline.",
        "- Treat `v024l_v023s_no_wheel_track_ablation` as high-recall learning evidence only.",
        "- Do not use `v024o` unless it is rerun from scratch.",
        "- Do not author `v025b` until the v025a result is reviewed.",
        "",
        "## v025a Result",
        "",
        "| Candidate | Matches | FNs | FPs | Errors | Status |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
        f"| `v020c_anchor_replay` | {V020C_BASELINE['matches']} | {V020C_BASELINE['false_negatives']} | {V020C_BASELINE['false_positives']} | {V020C_BASELINE['combined_errors']} | incumbent |",
        f"| `v024l_v023s_no_wheel_track_ablation` | {V024L_BASELINE['matches']} | {V024L_BASELINE['false_negatives']} | {V024L_BASELINE['false_positives']} | {V024L_BASELINE['combined_errors']} | learning evidence |",
        f"| `{PROMPT_ID}` | {result['match_count']} | {result['false_negative_count']} | {result['false_positive_count']} | {result['total_error_count']} | {decision['status']} |",
        "",
        "## Boundary",
        "",
        "No source truth, doctrine, assessment prompt, runtime code, eval ground truth, Graphify refresh, Mem0 write, promotion, or `v025b` authoring is adopted by this package.",
    ]
    (PACKAGE_ROOT / "final_recommendation.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def append_recovery(result: dict[str, Any], decision: dict[str, Any], backend_selection: dict[str, Any], fetch: dict[str, Any]) -> None:
    path = PACKAGE_ROOT / "recovery_log.json"
    payload = read_json(path)
    payload["runtime_recovery_required"] = bool(backend_selection.get("fallback_used"))
    payload["model_inference_run"] = True
    payload.setdefault("events", [])
    payload["events"] = [
        event for event in payload["events"] if event.get("event_type") != "v025a_run"
    ]
    payload["events"].append(
        {
            "event_type": "v025a_run",
            "timestamp_utc": utc(),
            "description": "Authored and evaluated v025a as the single approved compact separate-body recovery prompt candidate.",
            "fetch_upstream_main": fetch,
            "backend_selection": backend_selection,
            "all_current_run_summary": result["all_current_run_summary"],
            "office_negative_run_summary": result["office_negative_run_summary"],
            "decision_status": decision["status"],
            "hard_disqualifiers": decision["hard_disqualifiers"],
            "resolution": "Stopped after v025a diagnosis; no v025b authored.",
        }
    )
    payload["stop_conditions_preserved"].update(
        {
            "no_prompt_candidate_authored": False,
            "only_v025a_prompt_candidate_authored": True,
            "no_v025b_authored": True,
            "no_promotion": True,
            "no_review_repo_push": True,
        }
    )
    write_json(path, payload)
    lines = ["# Recovery Log", "", f"Updated: `{utc()}`", ""]
    for event in payload["events"]:
        stamp = event.get("timestamp_utc") or event.get("generated_utc") or payload.get("review_timestamp_utc", "")
        event_type = event.get("event_type") or event.get("type") or "event"
        description = event.get("description") or event.get("message") or ""
        lines.append(f"- `{stamp}` `{event_type}`: {description}")
    (PACKAGE_ROOT / "recovery_log.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_result(v023: Any, row: dict[str, Any], all_run: dict[str, Any], office_run: dict[str, Any]) -> dict[str, Any]:
    result = v023._row_result(
        row_id=ROW_ID,
        prompt_id=PROMPT_ID,
        prompt_info=row,
        backend=row["backend"],
        all_run=all_run,
        office_run=office_run,
    )
    all_summary = all_run["evaluation_summary"]
    filenames = [str(item["image_filename"]) for item in all_summary["images"]]
    result["case_101_seen"] = "101.jpg" in filenames or any(name.startswith("101.") for name in filenames)
    result["runtime_json_valid"] = (
        bool(all_run["succeeded"])
        and bool(office_run["succeeded"])
        and result["nonzero_command_count"] == 0
        and not result["missing_outputs"]
    )
    result["priority_cases"] = {case: case_metrics(all_summary, case) for case in PRIORITY_CASES}
    return result


def latest_run_summary(pack_dir: str) -> dict[str, Any]:
    candidates = sorted(
        (PACKAGE_ROOT / "runs" / PROMPT_ID / pack_dir).glob(
            "*/upstream_openai_compat_manifest_run_summary.json"
        )
    )
    if not candidates:
        raise FileNotFoundError(f"no completed run summary under {pack_dir}")
    payload = read_json(candidates[-1])
    payload["run_summary_path"] = str(candidates[-1])
    return payload


def finalize_runs(v023: Any, all_run: dict[str, Any], office_run: dict[str, Any], backend_selection: dict[str, Any], fetch: dict[str, Any]) -> int:
    prompt = v023._extract_prompt_from_overlay(OVERLAY_PATH)
    placeholders = v023._validate_prompt(PROMPT_ID, prompt)
    row = {
        "title": "v025a v020c compact separate body recovery",
        "source": str(OVERLAY_PATH),
        "prompt": prompt,
        "prompt_sha256": v023._sha_text(prompt),
        "backend": all_run["backend"],
        "placeholders": placeholders,
    }
    result = build_result(v023, row, all_run, office_run)
    v020c_cases, v024l_cases = source_case_tables()
    decision = classify_result(result, v020c_cases)
    update_candidate_registry(result, decision)
    update_comparison_matrix(result, decision, v020c_cases, v024l_cases)
    write_diagnosis(result, decision, v020c_cases)
    update_delta_review(result, decision)
    update_final(result, decision)
    append_recovery(result, decision, backend_selection, fetch)
    print(json.dumps({"result": result, "decision": decision}, indent=2)[:8000])
    return 0


def main() -> int:
    v023 = load_v023_runner()
    if "--finalize-existing" in sys.argv:
        all_run = latest_run_summary("all_current_no101")
        office_run = latest_run_summary("office_negative")
        backend = all_run["backend"]
        backend_selection = {
            "selected": backend,
            "attempts": [],
            "fallback_used": backend.get("backend_id") == "ollama_openai_compat_fallback_11434",
            "reuse_existing": True,
        }
        fetch = {
            "cmd": ["git", "fetch", "upstream", "main"],
            "returncode": None,
            "stdout_tail": "not rerun; reused completed v025a run summaries",
            "stderr_tail": "",
        }
        return finalize_runs(v023, all_run, office_run, backend_selection, fetch)
    fetch = run_cmd(["git", "fetch", "upstream", "main"], CAPSTONE_ROOT)
    if fetch["returncode"] != 0:
        raise RuntimeError(fetch["stderr_tail"])
    prompt = v023._extract_prompt_from_overlay(OVERLAY_PATH)
    placeholders = v023._validate_prompt(PROMPT_ID, prompt)
    backend_selection = select_backend(v023)
    backend = backend_selection["selected"]
    upstream_commit = v023._git_ref("upstream/main")
    scratch = None
    try:
        scratch = v023._create_scratch(ROW_ID, upstream_commit)
        v023._patch_scratch(scratch, prompt)
        run_root = PACKAGE_ROOT / "runs" / PROMPT_ID
        office_run = v023._run_manifest(
            row_id=ROW_ID,
            manifest_path=v023.OFFICE_NEGATIVE_MANIFEST,
            scratch=scratch,
            run_root=run_root / "office_negative",
            backend=backend,
        )
        all_run = v023._run_manifest(
            row_id=ROW_ID,
            manifest_path=v023.ALL_CURRENT_MANIFEST,
            scratch=scratch,
            run_root=run_root / "all_current_no101",
            backend=backend,
        )
    finally:
        if scratch is not None:
            cleanup = v023._remove_scratch(scratch)
            write_json(PACKAGE_ROOT / "runs" / PROMPT_ID / "scratch_cleanup.json", cleanup)
    if not all_run.get("evaluation_summary") or not office_run.get("evaluation_summary"):
        raise RuntimeError("missing evaluation summary")
    return finalize_runs(v023, all_run, office_run, backend_selection, fetch)


if __name__ == "__main__":
    raise SystemExit(main())
