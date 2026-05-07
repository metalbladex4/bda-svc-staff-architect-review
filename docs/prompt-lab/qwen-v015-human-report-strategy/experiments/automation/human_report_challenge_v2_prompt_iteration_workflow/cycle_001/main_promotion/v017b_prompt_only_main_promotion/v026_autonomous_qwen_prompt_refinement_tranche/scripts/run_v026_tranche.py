#!/usr/bin/env python3
"""Run the v026 autonomous Qwen prompt refinement tranche.

This package is evidence-only. It reuses the established upstream/main
OpenAI-compatible scratch-worktree runner from v023, and replaces only
prompts.detect_objects inside scratch configs.
"""

from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml


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
PACKAGE_ROOT = PROMOTION_ROOT / "v026_autonomous_qwen_prompt_refinement_tranche"
V023_RUNNER = PROMOTION_ROOT / "v023_literal99_qwen_no_stop_continuation/scripts/run_v023_literal99_cycle.py"
V020C_OVERLAY = PROMOTION_ROOT / "v020_v019c_goal_driven_self_improvement_cycle/overlays/v020c_v019c_extra_box_audit.yaml"
V025_ROOT = PROMOTION_ROOT / "v025_visual_delta_prompt_recovery"
V020C_DIAGNOSIS = PROMOTION_ROOT / "v023_literal99_qwen_no_stop_continuation/diagnoses/v020c_anchor_replay_diagnosis.json"
V024L_DIAGNOSIS = PROMOTION_ROOT / "v023_literal99_qwen_no_stop_continuation/diagnoses/v024l_v023s_no_wheel_track_ablation_diagnosis.json"
V025A_DIAGNOSIS = V025_ROOT / "diagnoses/v025a_v020c_compact_separate_body_recovery_diagnosis.json"

SENTINEL_NUMBERS = ("12", "14", "16", "42", "66", "67", "77", "84", "88", "90", "97", "103", "155", "166", "172")
TARGET_VISUAL_CASES = ("14", "42", "172")
FP_RISK_CASES = ("12", "16", "66", "77", "88", "90", "97", "103")
DENSE_CASES = ("66", "67", "84", "97")
CONTROL_CASES = ("155", "166")
REQUIRED_PLACEHOLDERS = ("{categories}", "{detection_guidance}", "{bbox_format}", "{bbox_scale}")
V020C_BASELINE = {"matches": 186, "false_negatives": 33, "false_positives": 25, "combined_errors": 58}
V024L_BASELINE = {"matches": 188, "false_negatives": 31, "false_positives": 35, "combined_errors": 66}
V025A_BASELINE = {"matches": 176, "false_negatives": 43, "false_positives": 35, "combined_errors": 78}
TARGET_MAX_ERRORS = 1


def utc() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat()


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected JSON object")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def read_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle) or {}
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected YAML object")
    return payload


def write_yaml(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=False), encoding="utf-8")


def run_cmd(cmd: list[str], cwd: Path) -> dict[str, Any]:
    completed = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    return {
        "cmd": cmd,
        "cwd": str(cwd),
        "returncode": completed.returncode,
        "stdout_tail": (completed.stdout or "")[-4000:],
        "stderr_tail": (completed.stderr or "")[-4000:],
    }


def load_v023() -> Any:
    spec = importlib.util.spec_from_file_location("v023_runner", V023_RUNNER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to import {V023_RUNNER}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.PACKAGE_ROOT = PACKAGE_ROOT
    return module


def prompt_from_overlay(path: Path) -> str:
    payload = read_yaml(path)
    try:
        prompt = payload["overrides"]["prompts"]["detect_objects"]
    except KeyError as exc:
        raise ValueError(f"{path}: missing overrides.prompts.detect_objects") from exc
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError(f"{path}: empty prompt")
    return prompt


def validate_prompt(prompt_id: str, prompt: str) -> dict[str, bool]:
    placeholders = {token: token in prompt for token in REQUIRED_PLACEHOLDERS}
    missing = [token for token, present in placeholders.items() if not present]
    if missing:
        raise ValueError(f"{prompt_id}: missing placeholders {missing}")
    lowered = prompt.lower()
    forbidden = ["case 101", "case 155", "case 166", "human report text"]
    hits = [term for term in forbidden if term in lowered]
    if hits:
        raise ValueError(f"{prompt_id}: forbidden runtime prompt text {hits}")
    if "return valid json only" not in lowered or '"detections"' not in prompt:
        raise ValueError(f"{prompt_id}: JSON-only/schema wording appears missing")
    return placeholders


def case_key(raw_id: Any, image_filename: Any = None) -> str:
    text = str(raw_id)
    if text.startswith("human-report-"):
        return text.rsplit("-", 1)[-1]
    if image_filename:
        return Path(str(image_filename)).stem
    return text


def create_sentinel_manifest(v023: Any) -> Path:
    manifest = read_yaml(v023.ALL_CURRENT_MANIFEST)
    wanted = set(SENTINEL_NUMBERS)
    cases = [case for case in manifest["cases"] if case_key(case.get("case_id"), case.get("image_filename")) in wanted]
    ids = [case_key(case.get("case_id"), case.get("image_filename")) for case in cases]
    missing = sorted(wanted.difference(ids), key=lambda value: int(value))
    if missing:
        raise RuntimeError(f"sentinel manifest missing cases {missing}")
    if "101" in ids:
        raise RuntimeError("case 101 entered sentinel manifest")
    payload = dict(manifest)
    payload["pack_id"] = "v026_sentinel_micro_pack_no101"
    payload["description"] = "v026 micro-pack sentinel for dense/control/FP-risk prompt gates; excludes case 101."
    payload["cases"] = cases
    path = PACKAGE_ROOT / "validation_manifests/v026_sentinel_micro_pack_no101.yaml"
    write_yaml(path, payload)
    return path


def manifest_check(v023: Any, sentinel_path: Path) -> dict[str, Any]:
    def ids(path: Path) -> list[str]:
        payload = read_yaml(path)
        return [case_key(case.get("case_id"), case.get("image_filename")) for case in payload["cases"]]

    all_ids = ids(v023.ALL_CURRENT_MANIFEST)
    sent_ids = ids(sentinel_path)
    office_ids = ids(v023.OFFICE_NEGATIVE_MANIFEST)
    result = {
        "all_current_manifest": str(v023.ALL_CURRENT_MANIFEST),
        "all_current_count": len(all_ids),
        "all_current_has_101": "101" in all_ids,
        "all_current_has_155": "155" in all_ids,
        "all_current_has_166": "166" in all_ids,
        "sentinel_manifest": str(sentinel_path),
        "sentinel_count": len(sent_ids),
        "sentinel_ids": sent_ids,
        "sentinel_has_101": "101" in sent_ids,
        "office_negative_manifest": str(v023.OFFICE_NEGATIVE_MANIFEST),
        "office_negative_count": len(office_ids),
        "office_negative_ids": office_ids,
    }
    if result["all_current_count"] != 117 or result["all_current_has_101"]:
        raise RuntimeError(f"bad all-current manifest check: {result}")
    if not result["all_current_has_155"] or not result["all_current_has_166"]:
        raise RuntimeError(f"missing positive controls: {result}")
    if result["sentinel_count"] != len(SENTINEL_NUMBERS) or result["sentinel_has_101"]:
        raise RuntimeError(f"bad sentinel manifest check: {result}")
    if result["office_negative_count"] != 1:
        raise RuntimeError(f"bad office-negative manifest check: {result}")
    return result


def append_recovery(event: dict[str, Any]) -> None:
    path = PACKAGE_ROOT / "recovery_log.json"
    payload = read_json(path) if path.exists() else {"events": []}
    payload.setdefault("events", []).append({"timestamp_utc": utc(), **event})
    write_json(path, payload)
    lines = ["# v026 Recovery Log", ""]
    for item in payload["events"]:
        stamp = item.get("timestamp_utc") or item.get("generated_utc") or utc()
        lines.append(f"- `{stamp}` `{item.get('event_type', item.get('type', 'event'))}`: {item.get('description', item.get('message', ''))}")
    (PACKAGE_ROOT / "recovery_log.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def select_backend(v023: Any) -> dict[str, Any]:
    attempts: list[dict[str, Any]] = []
    preferred = v023.PREFERRED_BACKEND
    fallback = v023.FALLBACK_BACKEND
    first = v023._check_endpoint(preferred["openai_base_url"], preferred["model"])
    attempts.append({"backend": preferred, "check": first})
    if first["status"] == "available":
        return {"selected": preferred, "attempts": attempts, "fallback_used": False}
    retry = v023._check_endpoint(preferred["openai_base_url"], preferred["model"])
    attempts.append({"backend": preferred, "check": retry, "recovery_attempt": "preferred_endpoint_retry"})
    if retry["status"] == "available":
        return {"selected": preferred, "attempts": attempts, "fallback_used": False}
    fallback_check = v023._check_endpoint(fallback["openai_base_url"], fallback["model"])
    attempts.append({"backend": fallback, "check": fallback_check, "recovery_attempt": "authorized_fallback"})
    if fallback_check["status"] != "available":
        append_recovery(
            {
                "event_type": "backend_unavailable",
                "description": "Preferred and fallback OpenAI-compatible Qwen endpoints unavailable.",
                "attempts": attempts,
            }
        )
        raise RuntimeError("No Qwen OpenAI-compatible endpoint is available")
    return {"selected": fallback, "attempts": attempts, "fallback_used": True}


def init_package() -> None:
    v023 = load_v023()
    for rel in ("overlays", "diagnoses", "runs", "scripts", "validation_manifests"):
        (PACKAGE_ROOT / rel).mkdir(parents=True, exist_ok=True)
    sentinel_path = create_sentinel_manifest(v023)
    fetch = run_cmd(["git", "fetch", "upstream", "main"], CAPSTONE_ROOT)
    if fetch["returncode"] != 0:
        append_recovery({"event_type": "fetch_failed", "description": "git fetch upstream main failed", "command": fetch})
        raise RuntimeError(fetch["stderr_tail"])
    backend_selection = select_backend(v023)
    if backend_selection.get("fallback_used"):
        append_recovery(
            {
                "event_type": "backend_fallback",
                "description": "Preferred localhost:8000/v1 unavailable; using Ollama-backed OpenAI-compatible fallback.",
                "backend_selection": backend_selection,
            }
        )
    manifest_checks = manifest_check(v023, sentinel_path)
    v020c_prompt = prompt_from_overlay(V020C_OVERLAY)
    validate_prompt("v020c_anchor_replay", v020c_prompt)
    source_manifest = {
        "generated_utc": utc(),
        "package_root": str(PACKAGE_ROOT),
        "source_docs": {
            "operating_doctrine": str(CAPSTONE_ROOT / "z_reference_docs/GPT-Pro_collab/CODEX_QWEN_PROMPT_ENGINEERING_DIRECTION_2026-05-06.md"),
            "deep_research_bundle": str(CAPSTONE_ROOT / "z_reference_docs/GPT-Pro_collab/bda_svc_qwen_prompt_engineering_deep_research_bundle.md"),
            "v025_final": str(V025_ROOT / "final_recommendation.md"),
            "v025_prompt_delta_autopsy": str(V025_ROOT / "diagnoses/v025a_prompt_delta_autopsy.md"),
            "v025_case67_autopsy": str(V025_ROOT / "diagnoses/v025a_case67_collapse_autopsy.md"),
            "v025_pointer_local_status": "missing_in_main_checkout_not_blocking",
        },
        "current_state": {
            "product_incumbent": "v020c_anchor_replay / v020c_extra_box_audit",
            "v020c": V020C_BASELINE,
            "v024l_learning_only": V024L_BASELINE,
            "v025a_rejected": V025A_BASELINE,
            "v024o": "partial_unscored_forbidden_as_evidence",
            "literal_target_combined_errors_max": TARGET_MAX_ERRORS,
        },
        "manifest_checks": manifest_checks,
        "backend_preflight": str(PACKAGE_ROOT / "backend_preflight.json"),
        "prompt_surface": "prompts.detect_objects only",
        "no_product_mutation": True,
    }
    backend_preflight = {
        "generated_utc": utc(),
        "fetch_upstream_main": fetch,
        "selection": backend_selection,
        "preferred_backend": v023.PREFERRED_BACKEND,
        "fallback_backend": v023.FALLBACK_BACKEND,
    }
    write_json(PACKAGE_ROOT / "backend_preflight.json", backend_preflight)
    write_json(PACKAGE_ROOT / "source_manifest.json", source_manifest)
    write_json(
        PACKAGE_ROOT / "candidate_registry.json",
        {
            "generated_utc": utc(),
            "working_best": "v020c_anchor_replay",
            "product_incumbent": "v020c_anchor_replay",
            "baseline_rows": {
                "v020c_anchor_replay": V020C_BASELINE,
                "v024l_v023s_no_wheel_track_ablation": V024L_BASELINE,
                "v025a_v020c_compact_separate_body_recovery": V025A_BASELINE,
            },
            "candidates": [],
        },
    )
    write_json(
        PACKAGE_ROOT / "comparison_matrix.json",
        {
            "generated_utc": utc(),
            "product_incumbent": "v020c_anchor_replay",
            "working_best": "v020c_anchor_replay",
            "target_combined_errors_max": TARGET_MAX_ERRORS,
            "rows": [],
            "rankings": [],
        },
    )
    write_json(
        PACKAGE_ROOT / "final_recommendation.json",
        {
            "generated_utc": utc(),
            "status": "initialized",
            "target_met": False,
            "product_incumbent": "v020c_anchor_replay",
            "tranche_working_best": "v020c_anchor_replay",
            "promotion": "none",
        },
    )
    (PACKAGE_ROOT / "README.md").write_text(
        "# v026 Autonomous Qwen Prompt Refinement Tranche\n\n"
        "Local-only prompt-lab evidence package. Product config, doctrine, assessment prompt, runtime code, and eval truth are not modified.\n",
        encoding="utf-8",
    )
    (PACKAGE_ROOT / "research_notes.md").write_text(
        "# v026 Research Notes\n\n"
        "- Local doctrine and v025 visual/autopsy evidence are primary for candidate design.\n"
        "- External research may inform prompt tactics but cannot override local eval evidence.\n",
        encoding="utf-8",
    )
    (PACKAGE_ROOT / "visual_review_notes.md").write_text(
        "# v026 Visual Review Notes\n\n"
        "- v025 static review and v025a autopsies are the starting visual evidence.\n",
        encoding="utf-8",
    )
    (PACKAGE_ROOT / "lessons_learned.md").write_text(
        "# v026 Lessons Learned\n\n"
        "- Start from v020c. Do not branch from v024l or v025a.\n"
        "- Do not place positive split/recovery cues in EXTRA-BOX AUDIT or FINAL BALANCE.\n"
        "- Case 67 is a sentinel for dense-row localization drift.\n",
        encoding="utf-8",
    )
    write_strategy_state("initialized", "v026a_fragment_context_precision_guard")
    write_matrix_md()
    write_final_md()


def write_strategy_state(status: str, next_axis: str) -> None:
    (PACKAGE_ROOT / "strategy_state.md").write_text(
        "# v026 Strategy State\n\n"
        f"Updated: `{utc()}`\n\n"
        "- product incumbent: `v020c_anchor_replay`\n"
        "- tranche working best: `v020c_anchor_replay`\n"
        f"- status: `{status}`\n"
        f"- next candidate axis: `{next_axis}`\n"
        "- current hard lesson: no positive split cue inside EXTRA-BOX AUDIT or FINAL BALANCE.\n",
        encoding="utf-8",
    )


def author_v026a() -> Path:
    prompt = prompt_from_overlay(V020C_OVERLAY)
    added = (
        "Bad final boxes also include boxes whose strongest evidence is only a roof/facade patch, "
        "debris/smoke/terrain, rowline, or cropped vehicle fragment rather than a visible target body "
        "with its own center and exterior boundary."
    )
    anchor = "- extra neighboring box whose distinct body boundary is not visible\n\n      EXTRA-BOX AUDIT"
    if added not in prompt:
        prompt = prompt.replace(anchor, f"- extra neighboring box whose distinct body boundary is not visible\n\n      {added}\n\n      EXTRA-BOX AUDIT")
    candidate_id = "v026a_fragment_context_precision_guard"
    validate_prompt(candidate_id, prompt)
    payload = {
        "candidate_id": candidate_id,
        "title": "v026a fragment/context precision guard",
        "overlay_id": "qwen-1.2-v026a-fragment-context-precision-guard",
        "overlay_type": "experiment",
        "model_line": "qwen3-vl:8b-instruct",
        "description": "Exact v020c plus one negative-only bad-box cue outside audit/final-balance.",
        "generated_from": ["v020c_v019c_extra_box_audit"],
        "hypothesis": "A compact precision guard outside audit can suppress fragment/context boxes without creating v025a-style split salience.",
        "overrides": {
            "prompts": {"detect_objects": prompt},
            "runtime": {"notes": "Applied only inside upstream/main scratch config; no product adoption."},
        },
    }
    path = PACKAGE_ROOT / "overlays/v026a_fragment_context_precision_guard.yaml"
    write_yaml(path, payload)
    return path


def author_v026b() -> Path:
    prompt = prompt_from_overlay(V020C_OVERLAY)
    added = "This audit is removal-only: never create new boxes during the audit; only discard boxes that fail the visible-body test."
    anchor = (
        "Before output, silently inspect every detection that sits near another detection or near a strong context cue. "
        "Remove it unless it has its own visible body center and at least one visible body edge or exterior-structure boundary. "
        "If two boxes describe the same connected body or the same continuous exterior building, keep only the tighter whole-body box."
    )
    if added not in prompt:
        prompt = prompt.replace(anchor, f"{anchor}\n\n      {added}")
    candidate_id = "v026b_audit_removal_only_lock"
    validate_prompt(candidate_id, prompt)
    payload = {
        "candidate_id": candidate_id,
        "title": "v026b audit removal only lock",
        "overlay_id": "qwen-1.2-v026b-audit-removal-only-lock",
        "overlay_type": "experiment",
        "model_line": "qwen3-vl:8b-instruct",
        "description": "Exact v020c plus one negative-only sentence clarifying that the final audit only removes boxes.",
        "generated_from": ["v020c_v019c_extra_box_audit", "v025a_prompt_delta_autopsy"],
        "hypothesis": "Locking the audit as removal-only may reduce extra boxes without creating v025a-style split salience.",
        "overrides": {
            "prompts": {"detect_objects": prompt},
            "runtime": {"notes": "Applied only inside upstream/main scratch config; no product adoption."},
        },
    }
    path = PACKAGE_ROOT / "overlays/v026b_audit_removal_only_lock.yaml"
    write_yaml(path, payload)
    return path


def author_v026c() -> Path:
    prompt = prompt_from_overlay(V020C_OVERLAY)
    added = (
        "- vehicle-like military equipment is anchored on the visible hull/body footprint, "
        "not only a top edge, dust plume, track mark, rowline, or spacing cue"
    )
    anchor = "- not a proxy for damage effects, row position, nearby roads, repeated spacing, or debris\n\n      BAD FINAL BOX"
    if added not in prompt:
        prompt = prompt.replace(
            anchor,
            "- not a proxy for damage effects, row position, nearby roads, repeated spacing, or debris\n"
            f"      {added}\n\n      BAD FINAL BOX",
        )
    candidate_id = "v026c_vehicle_body_anchor_not_rowline"
    validate_prompt(candidate_id, prompt)
    payload = {
        "candidate_id": candidate_id,
        "title": "v026c vehicle body anchor not rowline",
        "overlay_id": "qwen-1.2-v026c-vehicle-body-anchor-not-rowline",
        "overlay_type": "experiment",
        "model_line": "qwen3-vl:8b-instruct",
        "description": "Exact v020c plus one good-box cue anchoring vehicle boxes on visible body footprint instead of rowline/context cues.",
        "generated_from": ["v020c_v019c_extra_box_audit", "v025a_case67_collapse_autopsy"],
        "hypothesis": "A good-box vehicle body anchor may prevent dense-row top-edge/dust localization without changing audit salience.",
        "overrides": {
            "prompts": {"detect_objects": prompt},
            "runtime": {"notes": "Applied only inside upstream/main scratch config; no product adoption."},
        },
    }
    path = PACKAGE_ROOT / "overlays/v026c_vehicle_body_anchor_not_rowline.yaml"
    write_yaml(path, payload)
    return path


def author_v026d() -> Path:
    prompt = prompt_from_overlay(V020C_OVERLAY)
    added = "Detect every visible valid target and output one JSON bbox per distinct visible target body."
    anchor = "Perform a VISUAL-ONLY object detection."
    if added not in prompt:
        prompt = prompt.replace(anchor, f"{anchor}\n      {added}", 1)
    candidate_id = "v026d_qwen_native_grounding_header"
    validate_prompt(candidate_id, prompt)
    payload = {
        "candidate_id": candidate_id,
        "title": "v026d qwen native grounding header",
        "overlay_id": "qwen-1.2-v026d-qwen-native-grounding-header",
        "overlay_type": "experiment",
        "model_line": "qwen3-vl:8b-instruct",
        "description": "Exact v020c plus one compact Qwen-native grounding header at the start of the prompt.",
        "generated_from": ["v020c_v019c_extra_box_audit", "qwen_grounding_style_research"],
        "hypothesis": "A direct JSON bbox grounding header may improve recall while leaving v020c cleanup logic intact.",
        "overrides": {
            "prompts": {"detect_objects": prompt},
            "runtime": {"notes": "Applied only inside upstream/main scratch config; no product adoption."},
        },
    }
    path = PACKAGE_ROOT / "overlays/v026d_qwen_native_grounding_header.yaml"
    write_yaml(path, payload)
    return path


def author_v026e() -> Path:
    prompt = prompt_from_overlay(V020C_OVERLAY)
    added = "- side-by-side target body with its own visible center and boundary, even when smoke, debris, or proximity touches nearby targets"
    anchor = "- one connected target body, wreck body, or exterior building structure\n"
    if added not in prompt:
        prompt = prompt.replace(anchor, f"{anchor}      {added}\n", 1)
    candidate_id = "v026e_low_salience_separate_body_good_box"
    validate_prompt(candidate_id, prompt)
    payload = {
        "candidate_id": candidate_id,
        "title": "v026e low salience separate body good box",
        "overlay_id": "qwen-1.2-v026e-low-salience-separate-body-good-box",
        "overlay_type": "experiment",
        "model_line": "qwen3-vl:8b-instruct",
        "description": "Exact v020c plus one low-salience GOOD FINAL BOX cue for side-by-side visible bodies.",
        "generated_from": ["v020c_v019c_extra_box_audit", "v025a_prompt_delta_autopsy"],
        "hypothesis": "A non-audit, non-imperative good-box cue may recover separate bodies without v025a split salience.",
        "overrides": {
            "prompts": {"detect_objects": prompt},
            "runtime": {"notes": "Applied only inside upstream/main scratch config; no product adoption."},
        },
    }
    path = PACKAGE_ROOT / "overlays/v026e_low_salience_separate_body_good_box.yaml"
    write_yaml(path, payload)
    return path


def author_v026f() -> Path:
    prompt = prompt_from_overlay(V020C_OVERLAY)
    added = "- box where the visible target body occupies only a small part of the proposed box"
    anchor = "- extra neighboring box whose distinct body boundary is not visible\n\n      EXTRA-BOX AUDIT"
    if added not in prompt:
        prompt = prompt.replace(anchor, f"- extra neighboring box whose distinct body boundary is not visible\n      {added}\n\n      EXTRA-BOX AUDIT")
    candidate_id = "v026f_tight_box_occupancy_guard"
    validate_prompt(candidate_id, prompt)
    payload = {
        "candidate_id": candidate_id,
        "title": "v026f tight box occupancy guard",
        "overlay_id": "qwen-1.2-v026f-tight-box-occupancy-guard",
        "overlay_type": "experiment",
        "model_line": "qwen3-vl:8b-instruct",
        "description": "Exact v020c plus one bad-box cue rejecting boxes where the visible target occupies too little of the proposed box.",
        "generated_from": ["v020c_v019c_extra_box_audit"],
        "hypothesis": "A geometry-neutral tight-box restatement may reduce broad/context boxes without split or audit salience.",
        "overrides": {
            "prompts": {"detect_objects": prompt},
            "runtime": {"notes": "Applied only inside upstream/main scratch config; no product adoption."},
        },
    }
    path = PACKAGE_ROOT / "overlays/v026f_tight_box_occupancy_guard.yaml"
    write_yaml(path, payload)
    return path


def author_v026g() -> Path:
    prompt = prompt_from_overlay(V020C_OVERLAY)
    added = "- box where the visible target body occupies only a small part of the proposed box"
    anchor = "- extra neighboring box whose distinct body boundary is not visible\n\nEXTRA-BOX AUDIT"
    if added not in prompt:
        if anchor not in prompt:
            raise RuntimeError("v026g insertion anchor not found")
        prompt = prompt.replace(
            anchor,
            "- extra neighboring box whose distinct body boundary is not visible\n"
            f"{added}\n\n"
            "EXTRA-BOX AUDIT",
        )
    candidate_id = "v026g_actual_tight_occupancy_guard"
    validate_prompt(candidate_id, prompt)
    payload = {
        "candidate_id": candidate_id,
        "title": "v026g actual tight occupancy guard",
        "overlay_id": "qwen-1.2-v026g-actual-tight-occupancy-guard",
        "overlay_type": "experiment",
        "model_line": "qwen3-vl:8b-instruct",
        "description": "Exact v020c plus the intended bad-box cue rejecting boxes where the visible target occupies too little of the proposed box.",
        "generated_from": ["v020c_v019c_extra_box_audit"],
        "hypothesis": "A correctly inserted geometry-neutral tight-box guard may reduce broad/context boxes without split or audit salience.",
        "overrides": {
            "prompts": {"detect_objects": prompt},
            "runtime": {"notes": "Applied only inside upstream/main scratch config; no product adoption."},
        },
    }
    path = PACKAGE_ROOT / "overlays/v026g_actual_tight_occupancy_guard.yaml"
    write_yaml(path, payload)
    return path


def author_v026h() -> Path:
    prompt = prompt_from_overlay(V020C_OVERLAY)
    removed = (
        "\nCalibration from prior runs: broad recall additions raised false positives. "
        "Return to the v019c context-shadow balance and improve only the final cleanup of extra boxes.\n"
    )
    if removed not in prompt:
        raise RuntimeError("v026h calibration paragraph not found")
    prompt = prompt.replace(removed, "\n", 1)
    candidate_id = "v026h_remove_calibration_preamble"
    validate_prompt(candidate_id, prompt)
    payload = {
        "candidate_id": candidate_id,
        "title": "v026h remove calibration preamble",
        "overlay_id": "qwen-1.2-v026h-remove-calibration-preamble",
        "overlay_type": "experiment",
        "model_line": "qwen3-vl:8b-instruct",
        "description": "Exact v020c with only the prompt-lab calibration paragraph removed.",
        "generated_from": ["v020c_v019c_extra_box_audit"],
        "hypothesis": "Removing prompt-lab meta-calibration may simplify the prompt without touching dense-row, audit, or schema wording.",
        "overrides": {
            "prompts": {"detect_objects": prompt},
            "runtime": {"notes": "Applied only inside upstream/main scratch config; no product adoption."},
        },
    }
    path = PACKAGE_ROOT / "overlays/v026h_remove_calibration_preamble.yaml"
    write_yaml(path, payload)
    return path


def author_v026i() -> Path:
    prompt = prompt_from_overlay(V020C_OVERLAY)
    old = (
        "FINAL BALANCE\n"
        "Keep v019c recall behavior: small, damaged, crowded, or partly obscured targets are valid "
        "when their own target body remains visible after context is removed."
    )
    new = (
        "FINAL BALANCE\n"
        "Small, damaged, crowded, or partly obscured targets are valid "
        "when their own target body remains visible after context is removed."
    )
    if old not in prompt:
        raise RuntimeError("v026i final-balance label phrase not found")
    prompt = prompt.replace(old, new, 1)
    candidate_id = "v026i_remove_v019c_label_only"
    validate_prompt(candidate_id, prompt)
    payload = {
        "candidate_id": candidate_id,
        "title": "v026i remove v019c label only",
        "overlay_id": "qwen-1.2-v026i-remove-v019c-label-only",
        "overlay_type": "experiment",
        "model_line": "qwen3-vl:8b-instruct",
        "description": "Exact v020c with only the opaque v019c label removed from FINAL BALANCE while preserving the behavior sentence.",
        "generated_from": ["v020c_v019c_extra_box_audit"],
        "hypothesis": "Removing only version-label wording may simplify prompt format without changing recall, audit, or dense-row semantics.",
        "overrides": {
            "prompts": {"detect_objects": prompt},
            "runtime": {"notes": "Applied only inside upstream/main scratch config; no product adoption."},
        },
    }
    path = PACKAGE_ROOT / "overlays/v026i_remove_v019c_label_only.yaml"
    write_yaml(path, payload)
    return path


def author_v026j() -> Path:
    prompt = prompt_from_overlay(V020C_OVERLAY)
    old = "- tight enough that the target occupies most of the box"
    new = "- tight enough that the visible target body or exterior structure occupies most of the box"
    if old not in prompt:
        raise RuntimeError("v026j tight-box phrase not found")
    prompt = prompt.replace(old, new, 1)
    candidate_id = "v026j_visible_body_occupancy_phrase"
    validate_prompt(candidate_id, prompt)
    payload = {
        "candidate_id": candidate_id,
        "title": "v026j visible body occupancy phrase",
        "overlay_id": "qwen-1.2-v026j-visible-body-occupancy-phrase",
        "overlay_type": "experiment",
        "model_line": "qwen3-vl:8b-instruct",
        "description": "Exact v020c with one existing GOOD FINAL BOX tightness phrase made more visually concrete.",
        "generated_from": ["v020c_v019c_extra_box_audit"],
        "hypothesis": "Rewriting an existing tight-box phrase may reduce context/broad boxes without adding a new rejection bullet or split salience.",
        "overrides": {
            "prompts": {"detect_objects": prompt},
            "runtime": {"notes": "Applied only inside upstream/main scratch config; no product adoption."},
        },
    }
    path = PACKAGE_ROOT / "overlays/v026j_visible_body_occupancy_phrase.yaml"
    write_yaml(path, payload)
    return path


def author_v026k() -> Path:
    prompt = prompt_from_overlay(V020C_OVERLAY)
    old = "- context-only cue"
    new = "- context-only cue or unrelated intact background object"
    if old not in prompt:
        raise RuntimeError("v026k context-only bad-box phrase not found")
    prompt = prompt.replace(old, new, 1)
    candidate_id = "v026k_unrelated_background_object_guard"
    validate_prompt(candidate_id, prompt)
    payload = {
        "candidate_id": candidate_id,
        "title": "v026k unrelated background object guard",
        "overlay_id": "qwen-1.2-v026k-unrelated-background-object-guard",
        "overlay_type": "experiment",
        "model_line": "qwen3-vl:8b-instruct",
        "description": "Exact v020c with the existing context-only bad-box cue narrowed to also reject unrelated intact background objects.",
        "generated_from": ["v020c_v019c_extra_box_audit"],
        "hypothesis": "A tiny rewrite may reduce adjacent off-target background FPs without suppressing valid target-class objects or changing dense split behavior.",
        "overrides": {
            "prompts": {"detect_objects": prompt},
            "runtime": {"notes": "Applied only inside upstream/main scratch config; no product adoption."},
        },
    }
    path = PACKAGE_ROOT / "overlays/v026k_unrelated_background_object_guard.yaml"
    write_yaml(path, payload)
    return path


def author_v026l() -> Path:
    prompt = """Perform a VISUAL-ONLY object detection.

Detect every visible valid target whose doctrinal target_type is one of:
{categories}

Use context to search the whole image, but final boxes must be supported by the target itself.

KEEP
- one tight box per visible target body, wreck body, or exterior building structure
- small, damaged, crowded, or partly obscured targets when their own body remains visible
- separate boxes only when separate visible bodies are clear

REJECT
- smoke, dust, flame, shadow, road, terrain, blast texture, tracks, debris, row alignment, or spacing without a visible target body
- broad group, row, convoy, cluster, or scene-region boxes
- duplicate boxes or fragments of one connected body
- interior/facade/debris subsections of one continuous building
- neighboring boxes whose distinct body boundary is not visible

Before output, silently audit boxes near another detection or strong context cue. Keep the box only if it still has its own visible body center and at least one visible body edge or exterior-structure boundary after context cues are ignored.

TARGET-TYPE SPECIFIC DETECTION GUIDANCE
{detection_guidance}

BOUNDING BOX FORMAT
- Format: {bbox_format}
- Coordinate scale: {bbox_scale}

OUTPUT
Return valid JSON only.
Return a JSON object with a top-level detections field.
If no valid target is visible, return {\"detections\": []}.

OUTPUT SCHEMA
{
  \"detections\": [
    {
      \"target_type\": string,
      \"bbox\": {bbox_format}
    }
  ]
}
"""
    candidate_id = "v026l_compact_context_shadow_schema"
    validate_prompt(candidate_id, prompt)
    payload = {
        "candidate_id": candidate_id,
        "title": "v026l compact context shadow schema",
        "overlay_id": "qwen-1.2-v026l-compact-context-shadow-schema",
        "overlay_type": "experiment",
        "model_line": "qwen3-vl:8b-instruct",
        "description": "A compact v020c-inspired rewrite using Qwen-style JSON grounding wording without branching from v024l.",
        "generated_from": ["v020c_v019c_extra_box_audit"],
        "hypothesis": "A shorter prompt may reach a different Qwen grounding attractor while retaining v020c context-shadow and audit principles.",
        "overrides": {
            "prompts": {"detect_objects": prompt},
            "runtime": {"notes": "Applied only inside upstream/main scratch config; no product adoption."},
        },
    }
    path = PACKAGE_ROOT / "overlays/v026l_compact_context_shadow_schema.yaml"
    write_yaml(path, payload)
    return path


def author_v026m() -> Path:
    prompt = prompt_from_overlay(V020C_OVERLAY)
    guidance_block = "TARGET-TYPE SPECIFIC DETECTION GUIDANCE\n{detection_guidance}\n\n"
    insert_after = "Detect targets whose doctrinal target_type is one of:\n{categories}\n\n"
    if guidance_block not in prompt:
        raise RuntimeError("v026m guidance block not found")
    if insert_after not in prompt:
        raise RuntimeError("v026m categories insertion point not found")
    prompt = prompt.replace(guidance_block, "", 1)
    prompt = prompt.replace(insert_after, insert_after + guidance_block, 1)
    candidate_id = "v026m_target_guidance_before_context"
    validate_prompt(candidate_id, prompt)
    payload = {
        "candidate_id": candidate_id,
        "title": "v026m target guidance before context",
        "overlay_id": "qwen-1.2-v026m-target-guidance-before-context",
        "overlay_type": "experiment",
        "model_line": "qwen3-vl:8b-instruct",
        "description": "Exact v020c wording with target-type guidance moved before context-shadow cleanup.",
        "generated_from": ["v020c_v019c_extra_box_audit"],
        "hypothesis": "Keeping words intact but moving target guidance earlier may improve category anchoring without adding split/rejection salience.",
        "overrides": {
            "prompts": {"detect_objects": prompt},
            "runtime": {"notes": "Applied only inside upstream/main scratch config; no product adoption."},
        },
    }
    path = PACKAGE_ROOT / "overlays/v026m_target_guidance_before_context.yaml"
    write_yaml(path, payload)
    return path


def author_v026n() -> Path:
    prompt = prompt_from_overlay(V020C_OVERLAY)
    anchor = (
        "Calibration from prior runs: broad recall additions raised false positives. "
        "Return to the v019c context-shadow balance and improve only the final cleanup of extra boxes.\n\n"
    )
    added = (
        "Dense-row safety: keep compact visible vehicle bodies in rows; reject row, track, dust, "
        "or fragment boxes only when no own body remains.\n\n"
    )
    if anchor not in prompt:
        raise RuntimeError("v026n calibration anchor not found")
    prompt = prompt.replace(anchor, anchor + added, 1)
    candidate_id = "v026n_dense_row_body_safety_cue"
    validate_prompt(candidate_id, prompt)
    payload = {
        "candidate_id": candidate_id,
        "title": "v026n dense row body safety cue",
        "overlay_id": "qwen-1.2-v026n-dense-row-body-safety-cue",
        "overlay_type": "experiment",
        "model_line": "qwen3-vl:8b-instruct",
        "description": "Exact v020c plus one compact dense-row protective cue after the existing calibration paragraph.",
        "generated_from": ["v020c_v019c_extra_box_audit"],
        "hypothesis": "A protection-first dense-row cue may preserve case 67 while allowing row/track/fragment rejection to apply only when no own body remains.",
        "overrides": {
            "prompts": {"detect_objects": prompt},
            "runtime": {"notes": "Applied only inside upstream/main scratch config; no product adoption."},
        },
    }
    path = PACKAGE_ROOT / "overlays/v026n_dense_row_body_safety_cue.yaml"
    write_yaml(path, payload)
    return path


def author_v026o() -> Path:
    prompt = prompt_from_overlay(V020C_OVERLAY)
    old = "Return valid JSON only.\nReturn a JSON object with a top-level detections field."
    new = (
        "Return valid JSON only.\n"
        "Do not include markdown, prose, comments, confidence scores, or extra keys.\n"
        "Return a JSON object with a top-level detections field."
    )
    if old not in prompt:
        raise RuntimeError("v026o output anchor not found")
    prompt = prompt.replace(old, new, 1)
    candidate_id = "v026o_output_only_no_extra_keys"
    validate_prompt(candidate_id, prompt)
    payload = {
        "candidate_id": candidate_id,
        "title": "v026o output only no extra keys",
        "overlay_id": "qwen-1.2-v026o-output-only-no-extra-keys",
        "overlay_type": "experiment",
        "model_line": "qwen3-vl:8b-instruct",
        "description": "Exact v020c with only an output-format reinforcement before schema instructions.",
        "generated_from": ["v020c_v019c_extra_box_audit"],
        "hypothesis": "A detection-semantic-neutral output cue should preserve dense behavior and reveal whether suffix-only edits are safely ignored.",
        "overrides": {
            "prompts": {"detect_objects": prompt},
            "runtime": {"notes": "Applied only inside upstream/main scratch config; no product adoption."},
        },
    }
    path = PACKAGE_ROOT / "overlays/v026o_output_only_no_extra_keys.yaml"
    write_yaml(path, payload)
    return path


def author_v026p() -> Path:
    prompt = prompt_from_overlay(V020C_OVERLAY)
    old = "1. Find possible targets across the full image."
    new = "1. Find possible targets across the full image, scanning each quadrant before judging any box."
    if old not in prompt:
        raise RuntimeError("v026p context-shadow step 1 not found")
    prompt = prompt.replace(old, new, 1)
    candidate_id = "v026p_quadrant_scan_search_cue"
    validate_prompt(candidate_id, prompt)
    payload = {
        "candidate_id": candidate_id,
        "title": "v026p quadrant scan search cue",
        "overlay_id": "qwen-1.2-v026p-quadrant-scan-search-cue",
        "overlay_type": "experiment",
        "model_line": "qwen3-vl:8b-instruct",
        "description": "Exact v020c with context-shadow step 1 rewritten to scan each quadrant before judging boxes.",
        "generated_from": ["v020c_v019c_extra_box_audit"],
        "hypothesis": "A search-order cue may recover missed small targets without adding cleanup, split, or rejection salience.",
        "overrides": {
            "prompts": {"detect_objects": prompt},
            "runtime": {"notes": "Applied only inside upstream/main scratch config; no product adoption."},
        },
    }
    path = PACKAGE_ROOT / "overlays/v026p_quadrant_scan_search_cue.yaml"
    write_yaml(path, payload)
    return path


def author_v026q() -> Path:
    prompt = prompt_from_overlay(V020C_OVERLAY)
    old = "Detect targets whose doctrinal target_type is one of:\n{categories}\n\nCalibration"
    new = "Detect targets whose doctrinal target_type is one of:\n{categories}\n\n\nCalibration"
    if old not in prompt:
        raise RuntimeError("v026q blank-line anchor not found")
    prompt = prompt.replace(old, new, 1)
    candidate_id = "v026q_blank_line_shape_probe"
    validate_prompt(candidate_id, prompt)
    payload = {
        "candidate_id": candidate_id,
        "title": "v026q blank line shape probe",
        "overlay_id": "qwen-1.2-v026q-blank-line-shape-probe",
        "overlay_type": "experiment",
        "model_line": "qwen3-vl:8b-instruct",
        "description": "Exact v020c with only one extra blank line after the categories block.",
        "generated_from": ["v020c_v019c_extra_box_audit"],
        "hypothesis": "A no-semantics prompt-shape probe can distinguish semantic brittleness from general prompt-byte sensitivity.",
        "overrides": {
            "prompts": {"detect_objects": prompt},
            "runtime": {"notes": "Applied only inside upstream/main scratch config; no product adoption."},
        },
    }
    path = PACKAGE_ROOT / "overlays/v026q_blank_line_shape_probe.yaml"
    write_yaml(path, payload)
    return path


def candidate_intent(prompt_id: str) -> dict[str, str]:
    intents = {
        "v026a_fragment_context_precision_guard": {
            "test": "An attempted v020c-based compact precision guard; post-run inspection found the insertion did not render, so this is an exact-replay/control artifact.",
            "changed": "No effective detect_objects delta rendered in the overlay.",
            "likely": "No prompt phrase; this result is useful as a stability control, not as a precision-guard test.",
        },
        "v026b_audit_removal_only_lock": {
            "test": "A v020c-based audit-region lock that makes the final audit explicitly removal-only.",
            "changed": "One negative-only sentence was added inside EXTRA-BOX AUDIT.",
            "likely": "The audit removal-only sentence, especially if dense rows regress.",
        },
        "v026c_vehicle_body_anchor_not_rowline": {
            "test": "An attempted v020c-based vehicle-body anchor cue; post-run inspection found the insertion did not render, so this is an exact-replay/control artifact.",
            "changed": "No effective detect_objects delta rendered in the overlay.",
            "likely": "No prompt phrase; this result is useful as a stability control, not as a vehicle-anchor test.",
        },
        "v026d_qwen_native_grounding_header": {
            "test": "A v020c-based Qwen-native grounding header that directly asks for one JSON bbox per distinct visible target body.",
            "changed": "One direct grounding sentence was added immediately after the opening visual-only task line.",
            "likely": "The new opening grounding header, especially if recall or FP salience changes.",
        },
        "v026e_low_salience_separate_body_good_box": {
            "test": "A v020c-based low-salience separate-body cue placed in GOOD FINAL BOX rather than audit/final balance.",
            "changed": "One side-by-side visible-body bullet was added to GOOD FINAL BOX.",
            "likely": "The side-by-side visible-body bullet, especially if dense rows start splitting or drifting.",
        },
        "v026f_tight_box_occupancy_guard": {
            "test": "An attempted v020c-based tight-box precision cue; post-run inspection found the insertion did not render, so this is an exact-replay/control artifact.",
            "changed": "No effective detect_objects delta rendered in the overlay.",
            "likely": "No prompt phrase; this result is useful as a stability control, not as an occupancy-guard test.",
        },
        "v026g_actual_tight_occupancy_guard": {
            "test": "A v020c-based tight-box precision cue that rejects boxes where the visible target occupies too little of the proposed box.",
            "changed": "One BAD FINAL BOX bullet was inserted before EXTRA-BOX AUDIT using a verified anchor.",
            "likely": "The target-occupancy bad-box bullet, especially if broad/context boxes change.",
        },
        "v026h_remove_calibration_preamble": {
            "test": "A v020c load-bearing phrase micro-ablation that removes only the prompt-lab calibration paragraph.",
            "changed": "The calibration paragraph after TASK was removed; no detection rules, audit wording, final balance, placeholders, or schema text changed.",
            "likely": "The removed calibration paragraph, especially if recall/precision balance changes without dense collapse.",
        },
        "v026i_remove_v019c_label_only": {
            "test": "A tiny prompt-format simplification that removes only the opaque v019c label from FINAL BALANCE.",
            "changed": "The words 'Keep v019c recall behavior:' were removed while preserving the actual final-balance behavior sentence.",
            "likely": "The removed version-label phrase, especially if dense stability or recall changes.",
        },
        "v026j_visible_body_occupancy_phrase": {
            "test": "A one-phrase rewrite of the existing GOOD FINAL BOX tightness cue.",
            "changed": "'target occupies most of the box' became 'visible target body or exterior structure occupies most of the box'.",
            "likely": "The tightened visible-body occupancy phrase, especially if broad/context boxes or dense rows change.",
        },
        "v026k_unrelated_background_object_guard": {
            "test": "A one-phrase rewrite of the existing context-only BAD FINAL BOX cue for adjacent off-target background objects.",
            "changed": "'context-only cue' became 'context-only cue or unrelated intact background object'.",
            "likely": "The unrelated-intact-background phrase, especially in FP-risk cases 16 and 88 or controls 155/166.",
        },
        "v026l_compact_context_shadow_schema": {
            "test": "A compact v020c-inspired prompt rewrite using Qwen-style JSON grounding form.",
            "changed": "The prompt was compressed while preserving context-shadow search, visible-body support, rejection classes, placeholders, and output schema.",
            "likely": "The compact prompt structure, especially if recall improves or FP classes reopen.",
        },
        "v026m_target_guidance_before_context": {
            "test": "An ordering-only ablation that moves target-type guidance before context-shadow cleanup.",
            "changed": "All v020c wording is preserved, but the target-type guidance block appears immediately after categories.",
            "likely": "The earlier target-guidance position, especially if category anchoring improves or dense context cleanup regresses.",
        },
        "v026n_dense_row_body_safety_cue": {
            "test": "A compact dense-row protection cue placed after the load-bearing calibration paragraph.",
            "changed": "One sentence tells the model to keep compact visible vehicle bodies in rows and reject row/track/dust/fragment boxes only when no own body remains.",
            "likely": "The dense-row safety sentence, especially if case 67 is preserved or fragment FPs change.",
        },
        "v026o_output_only_no_extra_keys": {
            "test": "A suffix/output-only cue that should not change detection semantics.",
            "changed": "One output-format sentence was added before the existing top-level detections instruction.",
            "likely": "The no-extra-keys output sentence, mostly as a stability probe rather than a detection lever.",
        },
        "v026p_quadrant_scan_search_cue": {
            "test": "A search-order cue in context-shadow step 1, aimed at recall without cleanup/split wording.",
            "changed": "Step 1 now asks to scan each quadrant before judging any box.",
            "likely": "The quadrant-scan wording, especially if target cases 14/42/172 improve or dense rows drift.",
        },
        "v026q_blank_line_shape_probe": {
            "test": "A no-semantics prompt-shape probe.",
            "changed": "One blank line was added after the categories block.",
            "likely": "No semantic phrase; use this to judge prompt-shape sensitivity on the fallback backend.",
        },
    }
    return intents.get(
        prompt_id,
        {
            "test": "A v020c-based single prompt change.",
            "changed": "One detect_objects prompt delta from the current working best.",
            "likely": "The newest prompt delta.",
        },
    )


def case_metrics(summary: dict[str, Any], case_id: str) -> dict[str, int]:
    images = {Path(str(item["image_filename"])).stem: item for item in summary["images"]}
    item = images[case_id]
    return {
        "reference_target_count": int(item["reference_target_count"]),
        "predicted_target_count": int(item["predicted_target_count"]),
        "match_count": int(item["match_count"]),
        "false_negative_count": int(item["false_negative_count"]),
        "false_positive_count": int(item["false_positive_count"]),
    }


def compact(metrics: dict[str, int]) -> str:
    return f"{metrics['match_count']}/{metrics['false_negative_count']}/{metrics['false_positive_count']}"


def totals_from_summary(summary: dict[str, Any]) -> dict[str, int]:
    totals = summary["totals"]
    fn = int(totals["false_negative_count"])
    fp = int(totals["false_positive_count"])
    return {
        "matches": int(totals["match_count"]),
        "false_negatives": fn,
        "false_positives": fp,
        "combined_errors": fn + fp,
    }


def load_prompt(prompt_id: str) -> tuple[str, Path]:
    if prompt_id == "v020c_anchor_replay":
        return prompt_from_overlay(V020C_OVERLAY), V020C_OVERLAY
    overlay = PACKAGE_ROOT / f"overlays/{prompt_id}.yaml"
    return prompt_from_overlay(overlay), overlay


def run_manifest_with_prompt(prompt_id: str, manifest_path: Path, pack_dir: str, backend: dict[str, Any]) -> dict[str, Any]:
    v023 = load_v023()
    prompt, source = load_prompt(prompt_id)
    validate_prompt(prompt_id, prompt)
    row_id = f"qwen__{prompt_id}__{pack_dir}"
    upstream_commit = v023._git_ref("upstream/main")
    scratch = None
    try:
        scratch = v023._create_scratch(row_id, upstream_commit)
        v023._patch_scratch(scratch, prompt)
        return v023._run_manifest(
            row_id=row_id,
            manifest_path=manifest_path,
            scratch=scratch,
            run_root=PACKAGE_ROOT / "runs" / prompt_id / pack_dir,
            backend=backend,
        ) | {"prompt_source": str(source)}
    finally:
        if scratch is not None:
            cleanup = v023._remove_scratch(scratch)
            write_json(PACKAGE_ROOT / "runs" / prompt_id / f"scratch_cleanup_{pack_dir}.json", cleanup)


def current_backend() -> dict[str, Any]:
    v023 = load_v023()
    if not (PACKAGE_ROOT / "backend_preflight.json").exists():
        init_package()
    selection = read_json(PACKAGE_ROOT / "backend_preflight.json")["selection"]
    backend = selection["selected"]
    check = v023._check_endpoint(backend["openai_base_url"], backend["model"])
    if check["status"] == "available":
        return backend
    append_recovery({"event_type": "backend_recheck_failed", "description": "Selected backend recheck failed.", "check": check})
    selection = select_backend(v023)
    write_json(PACKAGE_ROOT / "backend_preflight.json", {"generated_utc": utc(), "selection": selection})
    return selection["selected"]


def office_pass(office_run: dict[str, Any]) -> bool:
    if not office_run.get("succeeded"):
        return False
    totals = office_run["evaluation_summary"]["totals"]
    return (
        office_run["evaluation_summary"]["image_count"] == 1
        and int(totals["negative_scene_abstention_correct_count"]) == 1
        and int(totals["negative_scene_false_positive_count"]) == 0
    )


def build_stage_result(prompt_id: str, stage: str, run: dict[str, Any], office_run: dict[str, Any]) -> dict[str, Any]:
    summary = run["evaluation_summary"]
    totals = totals_from_summary(summary)
    cases = {case: case_metrics(summary, case) for case in SENTINEL_NUMBERS if case in {Path(str(i["image_filename"])).stem for i in summary["images"]}}
    result = {
        "candidate_id": prompt_id,
        "stage": stage,
        "backend": run["backend"],
        "image_count": summary["image_count"],
        **totals,
        "case_101_seen": any(Path(str(item["image_filename"])).stem == "101" for item in summary["images"]),
        "cases": cases,
        "dense_cases": {case: cases[case] for case in DENSE_CASES if case in cases},
        "controls": {case: cases[case] for case in CONTROL_CASES if case in cases},
        "target_visual_cases": {case: cases[case] for case in TARGET_VISUAL_CASES if case in cases},
        "fp_risk_cases": {case: cases[case] for case in FP_RISK_CASES if case in cases},
        "office_negative": {
            "image_count": office_run["evaluation_summary"]["image_count"] if office_run.get("evaluation_summary") else None,
            "pass": office_pass(office_run),
            "summary_path": office_run.get("summary_path"),
        },
        "run_summaries": {"stage": run["run_summary_path"], "office_negative": office_run["run_summary_path"]},
        "runtime_json_valid": bool(run.get("succeeded")) and bool(office_run.get("succeeded")),
        "nonzero_command_count": sum(1 for c in run.get("commands", []) + office_run.get("commands", []) if c["returncode"] != 0),
        "missing_outputs": run.get("missing_outputs", []) + office_run.get("missing_outputs", []),
    }
    return result


def ensure_baseline_micro() -> dict[str, Any]:
    path = PACKAGE_ROOT / "diagnoses/v020c_anchor_replay_micro_baseline.json"
    if path.exists():
        return read_json(path)
    v023 = load_v023()
    sentinel_path = PACKAGE_ROOT / "validation_manifests/v026_sentinel_micro_pack_no101.yaml"
    if not sentinel_path.exists():
        init_package()
    backend = current_backend()
    office = run_manifest_with_prompt("v020c_anchor_replay", v023.OFFICE_NEGATIVE_MANIFEST, "office_negative", backend)
    micro = run_manifest_with_prompt("v020c_anchor_replay", sentinel_path, "sentinel_micro", backend)
    result = build_stage_result("v020c_anchor_replay", "micro_pack_only", micro, office)
    write_json(path, result)
    append_metrics_block(result, "baseline_micro", "baseline", "sentinel calibration")
    return result


def micro_decision(result: dict[str, Any], baseline: dict[str, Any]) -> dict[str, Any]:
    hard: list[str] = []
    cases = result["cases"]
    base_cases = baseline["cases"]
    if result["image_count"] != len(SENTINEL_NUMBERS):
        hard.append("sentinel_image_count_wrong")
    if result["case_101_seen"]:
        hard.append("case_101_seen")
    if not result["runtime_json_valid"]:
        hard.append("runtime_or_json_failure")
    for control in CONTROL_CASES:
        item = cases.get(control)
        if not item or item["match_count"] < item["reference_target_count"] or item["false_negative_count"] or item["false_positive_count"]:
            hard.append(f"case_{control}_failed")
    if not result["office_negative"]["pass"]:
        hard.append("office_negative_failed")
    c67 = cases["67"]
    b67 = base_cases["67"]
    if c67["match_count"] < b67["match_count"] or c67["false_negative_count"] > b67["false_negative_count"] + 1 or c67["false_positive_count"] > b67["false_positive_count"] + 3:
        hard.append("case_67_regression")
    c84 = cases["84"]
    b84 = base_cases["84"]
    if c84["match_count"] < b84["match_count"] - 1:
        hard.append("case_84_regression")
    if cases["66"]["false_positive_count"] > base_cases["66"]["false_positive_count"] + 2:
        hard.append("nested_fragment_or_context_fp_reopened")
    if cases["97"]["match_count"] < base_cases["97"]["match_count"]:
        hard.append("case_97_match_loss")
    status = "micro_pass" if not hard else "rejected"
    return {
        "status": status,
        "hard_disqualifiers": hard,
        "run_full_all_current": status == "micro_pass",
    }


def full_decision(result: dict[str, Any]) -> dict[str, Any]:
    hard: list[str] = []
    if result["image_count"] != 117:
        hard.append("all_current_image_count_wrong")
    if result["case_101_seen"]:
        hard.append("case_101_seen")
    if not result["runtime_json_valid"]:
        hard.append("runtime_or_json_failure")
    for control in CONTROL_CASES:
        item = result["controls"].get(control)
        if not item or item["match_count"] < item["reference_target_count"] or item["false_negative_count"] or item["false_positive_count"]:
            hard.append(f"case_{control}_failed")
    if not result["office_negative"]["pass"]:
        hard.append("office_negative_failed")
    c67 = result["dense_cases"]["67"]
    if c67["match_count"] < 9 or c67["false_negative_count"] > 3:
        hard.append("case_67_below_v020c")
    if result["false_positives"] > 35:
        hard.append("fp_explosion_above_v024l")
    if result["combined_errors"] <= TARGET_MAX_ERRORS:
        status = "target_met"
    elif hard:
        status = "rejected"
    elif result["combined_errors"] < V020C_BASELINE["combined_errors"]:
        status = "new_working_best"
    elif result["matches"] > V020C_BASELINE["matches"] or result["false_negatives"] < V020C_BASELINE["false_negatives"]:
        status = "learning_evidence"
    else:
        status = "learning_evidence"
    return {"status": status, "hard_disqualifiers": hard}


def append_metrics_block(result: dict[str, Any], status: str, lesson: str, next_axis: str) -> None:
    c67 = result.get("dense_cases", {}).get("67") or result.get("cases", {}).get("67")
    c155 = result.get("controls", {}).get("155") or result.get("cases", {}).get("155")
    c166 = result.get("controls", {}).get("166") or result.get("cases", {}).get("166")
    block = (
        "=== CANDIDATE COMPLETE ===\n"
        f"candidate: {result['candidate_id']}\n"
        f"backend: {result['backend']['backend_id']}\n"
        f"stage: {result['stage']}\n"
        f"matches: {result.get('matches', 'n/a')}\n"
        f"false_negatives: {result.get('false_negatives', 'n/a')}\n"
        f"false_positives: {result.get('false_positives', 'n/a')}\n"
        f"combined_errors: {result.get('combined_errors', 'n/a')}\n"
        f"vs_v020c_errors_delta: {result.get('combined_errors', 0) - V020C_BASELINE['combined_errors'] if result.get('stage') == 'full_all_current' else 'n/a'}\n"
        f"case_67: {compact(c67) if c67 else 'n/a'}\n"
        f"case_155: {compact(c155) if c155 else 'n/a'}\n"
        f"case_166: {compact(c166) if c166 else 'n/a'}\n"
        f"office_negative: {'pass' if result['office_negative']['pass'] else 'fail'}\n"
        f"status: {status}\n"
        f"main_lesson: {lesson}\n"
        f"next_axis: {next_axis}\n"
        "==========================\n"
    )
    print(block, flush=True)
    with (PACKAGE_ROOT / "live_metrics_log.md").open("a", encoding="utf-8") as handle:
        handle.write(block + "\n")


def update_registry_and_matrix(result: dict[str, Any], decision: dict[str, Any]) -> None:
    registry = read_json(PACKAGE_ROOT / "candidate_registry.json")
    rows = [row for row in registry.get("candidates", []) if not (row["candidate_id"] == result["candidate_id"] and row["stage"] == result["stage"])]
    rows.append(
        {
            "candidate_id": result["candidate_id"],
            "stage": result["stage"],
            "status": decision["status"],
            "metrics": {k: result[k] for k in ("matches", "false_negatives", "false_positives", "combined_errors")},
            "case_67": compact(result.get("dense_cases", {}).get("67") or result["cases"].get("67")),
            "backend_id": result["backend"]["backend_id"],
            "run_summaries": result["run_summaries"],
        }
    )
    registry["candidates"] = rows
    registry["last_updated_utc"] = utc()
    write_json(PACKAGE_ROOT / "candidate_registry.json", registry)
    matrix = read_json(PACKAGE_ROOT / "comparison_matrix.json")
    matrix_rows = [row for row in matrix.get("rows", []) if not (row["candidate_id"] == result["candidate_id"] and row["stage"] == result["stage"])]
    matrix_rows.append(
        {
            "candidate_id": result["candidate_id"],
            "stage": result["stage"],
            "status": decision["status"],
            "matches": result["matches"],
            "false_negatives": result["false_negatives"],
            "false_positives": result["false_positives"],
            "combined_errors": result["combined_errors"],
            "case_67": compact(result.get("dense_cases", {}).get("67") or result["cases"].get("67")),
            "case_155": compact(result.get("controls", {}).get("155") or result["cases"].get("155")),
            "case_166": compact(result.get("controls", {}).get("166") or result["cases"].get("166")),
            "office_negative": "pass" if result["office_negative"]["pass"] else "fail",
            "hard_disqualifiers": decision.get("hard_disqualifiers", []),
            "backend_id": result["backend"]["backend_id"],
        }
    )
    matrix["rows"] = matrix_rows
    matrix["generated_utc"] = utc()
    matrix["rankings"] = sorted(
        [
            row for row in matrix_rows
            if row["stage"] == "full_all_current" and row["status"] not in {"rejected"}
        ],
        key=lambda row: (row["combined_errors"], -row["matches"]),
    )
    write_json(PACKAGE_ROOT / "comparison_matrix.json", matrix)
    write_matrix_md()
    write_final_md()


def write_matrix_md() -> None:
    matrix_path = PACKAGE_ROOT / "comparison_matrix.json"
    matrix = read_json(matrix_path) if matrix_path.exists() else {"rows": []}
    lines = [
        "# v026 Comparison Matrix",
        "",
        f"Updated: `{matrix.get('generated_utc', utc())}`",
        "",
        "| Candidate | Stage | Status | Matches | FNs | FPs | Errors | 67 | 155 | 166 | Office | Backend |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for row in matrix.get("rows", []):
        lines.append(
            f"| `{row['candidate_id']}` | `{row['stage']}` | `{row['status']}` | {row['matches']} | "
            f"{row['false_negatives']} | {row['false_positives']} | {row['combined_errors']} | "
            f"{row['case_67']} | {row['case_155']} | {row['case_166']} | {row['office_negative']} | `{row['backend_id']}` |"
        )
    (PACKAGE_ROOT / "comparison_matrix.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_final_md() -> None:
    matrix = read_json(PACKAGE_ROOT / "comparison_matrix.json") if (PACKAGE_ROOT / "comparison_matrix.json").exists() else {"rows": []}
    full_rows = [row for row in matrix.get("rows", []) if row["stage"] == "full_all_current"]
    best = sorted(full_rows, key=lambda row: (row["combined_errors"], -row["matches"]))[0] if full_rows else None
    payload = read_json(PACKAGE_ROOT / "final_recommendation.json") if (PACKAGE_ROOT / "final_recommendation.json").exists() else {}
    payload.update(
        {
            "generated_utc": utc(),
            "target_met": bool(best and best["combined_errors"] <= TARGET_MAX_ERRORS),
            "product_incumbent": "v020c_anchor_replay",
            "tranche_working_best": best["candidate_id"] if best and best["combined_errors"] < V020C_BASELINE["combined_errors"] else "v020c_anchor_replay",
            "best_full_candidate": best,
            "promotion": "none",
        }
    )
    write_json(PACKAGE_ROOT / "final_recommendation.json", payload)
    lines = [
        "# v026 Final Recommendation",
        "",
        f"Updated: `{payload['generated_utc']}`",
        "",
        "- product incumbent: `v020c_anchor_replay`",
        f"- tranche working best: `{payload['tranche_working_best']}`",
        f"- target met: `{payload['target_met']}`",
        "- promotion: `none`",
        "",
        "This package is prompt-lab evidence only. No product config, doctrine, assessment prompt, runtime code, eval truth, commit, push, or PR is adopted here.",
    ]
    if best:
        lines.extend(
            [
                "",
                "## Best Full Candidate So Far",
                "",
                f"- `{best['candidate_id']}`: {best['matches']} matches / {best['false_negatives']} FNs / {best['false_positives']} FPs / {best['combined_errors']} errors",
            ]
        )
    (PACKAGE_ROOT / "final_recommendation.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_diagnosis(result: dict[str, Any], decision: dict[str, Any], next_axis: str, lesson: str) -> None:
    payload = {
        "generated_utc": utc(),
        "candidate_id": result["candidate_id"],
        "stage": result["stage"],
        "metrics": {k: result[k] for k in ("matches", "false_negatives", "false_positives", "combined_errors")},
        "decision": decision,
        "dense_cases": result.get("dense_cases"),
        "controls": result.get("controls"),
        "target_visual_cases": result.get("target_visual_cases"),
        "fp_risk_cases": result.get("fp_risk_cases"),
        "office_negative": result.get("office_negative"),
        "run_summaries": result.get("run_summaries"),
        "answers": {
            "what_did_this_test": candidate_intent(result["candidate_id"])["test"],
            "what_changed_from_working_best": candidate_intent(result["candidate_id"])["changed"],
            "what_improved": "See metrics and case table.",
            "what_regressed": "See hard_disqualifiers and case deltas.",
            "known_failure_reproduced": "v025a-style dense-row collapse is flagged if case 67 regresses.",
            "new_failure_class": "Classify from FP-risk cases before next candidate.",
            "likely_load_bearing_phrase": candidate_intent(result["candidate_id"])["likely"],
            "lesson_type": "local eval signal until confirmed by all-current.",
            "preserve": "v020c context-shadow and extra-box audit ordering.",
            "avoid": "Positive split language in audit/final-balance.",
            "next_hypothesis": next_axis,
            "why_next_differs": "The next axis is chosen from the observed sentinel/full failure, not from the original v025a hypothesis.",
        },
    }
    path = PACKAGE_ROOT / "diagnoses" / f"{result['candidate_id']}_{result['stage']}_diagnosis.json"
    write_json(path, payload)
    lines = [
        f"# {result['candidate_id']} {result['stage']} Diagnosis",
        "",
        f"Generated: `{payload['generated_utc']}`",
        "",
        f"- status: `{decision['status']}`",
        f"- hard disqualifiers: `{decision.get('hard_disqualifiers', [])}`",
        f"- metrics: `{result['matches']}/{result['false_negatives']}/{result['false_positives']}/{result['combined_errors']}`",
        "",
        "## Dense Cases",
        "",
        "| Case | M/FN/FP |",
        "| --- | ---: |",
    ]
    for case, item in (result.get("dense_cases") or {}).items():
        lines.append(f"| `{case}` | {compact(item)} |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            lesson,
            "",
            "## Next Hypothesis",
            "",
            next_axis,
        ]
    )
    path.with_suffix(".md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    with (PACKAGE_ROOT / "lessons_learned.md").open("a", encoding="utf-8") as handle:
        handle.write(f"\n## {result['candidate_id']} {result['stage']}\n\n- {lesson}\n- Next axis: {next_axis}\n")
    write_strategy_state(decision["status"], next_axis)


def run_candidate(prompt_id: str) -> int:
    if not (PACKAGE_ROOT / "source_manifest.json").exists():
        init_package()
    if prompt_id == "v026a_fragment_context_precision_guard" and not (PACKAGE_ROOT / f"overlays/{prompt_id}.yaml").exists():
        author_v026a()
    if prompt_id == "v026b_audit_removal_only_lock" and not (PACKAGE_ROOT / f"overlays/{prompt_id}.yaml").exists():
        author_v026b()
    if prompt_id == "v026c_vehicle_body_anchor_not_rowline" and not (PACKAGE_ROOT / f"overlays/{prompt_id}.yaml").exists():
        author_v026c()
    if prompt_id == "v026d_qwen_native_grounding_header" and not (PACKAGE_ROOT / f"overlays/{prompt_id}.yaml").exists():
        author_v026d()
    if prompt_id == "v026e_low_salience_separate_body_good_box" and not (PACKAGE_ROOT / f"overlays/{prompt_id}.yaml").exists():
        author_v026e()
    if prompt_id == "v026f_tight_box_occupancy_guard" and not (PACKAGE_ROOT / f"overlays/{prompt_id}.yaml").exists():
        author_v026f()
    if prompt_id == "v026g_actual_tight_occupancy_guard" and not (PACKAGE_ROOT / f"overlays/{prompt_id}.yaml").exists():
        author_v026g()
    if prompt_id == "v026h_remove_calibration_preamble" and not (PACKAGE_ROOT / f"overlays/{prompt_id}.yaml").exists():
        author_v026h()
    if prompt_id == "v026i_remove_v019c_label_only" and not (PACKAGE_ROOT / f"overlays/{prompt_id}.yaml").exists():
        author_v026i()
    if prompt_id == "v026j_visible_body_occupancy_phrase" and not (PACKAGE_ROOT / f"overlays/{prompt_id}.yaml").exists():
        author_v026j()
    if prompt_id == "v026k_unrelated_background_object_guard" and not (PACKAGE_ROOT / f"overlays/{prompt_id}.yaml").exists():
        author_v026k()
    if prompt_id == "v026l_compact_context_shadow_schema" and not (PACKAGE_ROOT / f"overlays/{prompt_id}.yaml").exists():
        author_v026l()
    if prompt_id == "v026m_target_guidance_before_context" and not (PACKAGE_ROOT / f"overlays/{prompt_id}.yaml").exists():
        author_v026m()
    if prompt_id == "v026n_dense_row_body_safety_cue" and not (PACKAGE_ROOT / f"overlays/{prompt_id}.yaml").exists():
        author_v026n()
    if prompt_id == "v026o_output_only_no_extra_keys" and not (PACKAGE_ROOT / f"overlays/{prompt_id}.yaml").exists():
        author_v026o()
    if prompt_id == "v026p_quadrant_scan_search_cue" and not (PACKAGE_ROOT / f"overlays/{prompt_id}.yaml").exists():
        author_v026p()
    if prompt_id == "v026q_blank_line_shape_probe" and not (PACKAGE_ROOT / f"overlays/{prompt_id}.yaml").exists():
        author_v026q()
    v023 = load_v023()
    sentinel = PACKAGE_ROOT / "validation_manifests/v026_sentinel_micro_pack_no101.yaml"
    baseline = ensure_baseline_micro()
    backend = current_backend()
    office = run_manifest_with_prompt(prompt_id, v023.OFFICE_NEGATIVE_MANIFEST, "office_negative", backend)
    micro = run_manifest_with_prompt(prompt_id, sentinel, "sentinel_micro", backend)
    micro_result = build_stage_result(prompt_id, "micro_pack_only", micro, office)
    micro_gate = micro_decision(micro_result, baseline)
    if micro_gate["status"] == "micro_pass":
        lesson = "Micro-pack passed dense/control gate; candidate earned an all-current run."
        next_axis = "Run full all-current for the same candidate."
        append_metrics_block(micro_result, "learning_evidence", lesson, next_axis)
        write_diagnosis(micro_result, micro_gate, next_axis, lesson)
        update_registry_and_matrix(micro_result, {"status": "micro_pass", "hard_disqualifiers": []})
        all_run = run_manifest_with_prompt(prompt_id, v023.ALL_CURRENT_MANIFEST, "all_current_no101", backend)
        full_result = build_stage_result(prompt_id, "full_all_current", all_run, office)
        full_gate = full_decision(full_result)
        if full_gate["status"] == "new_working_best":
            lesson = "Candidate beat v020c combined error while preserving required controls; keep as tranche working best pending replay."
            next_axis = "Replay the challenger once before using it as a base."
        elif full_gate["status"] == "target_met":
            lesson = "Literal target reached; stop without promotion and report."
            next_axis = "Stop for user review."
        elif full_gate["status"] == "rejected":
            lesson = "Full run exposed a hard disqualifier despite micro-pack pass."
            next_axis = "Run a v020c load-bearing phrase micro-ablation, not another positive split cue."
        else:
            lesson = "Full run did not beat v020c; retain as learning evidence."
            next_axis = "Try a smaller v020c load-bearing ordering ablation."
        append_metrics_block(full_result, full_gate["status"], lesson, next_axis)
        write_diagnosis(full_result, full_gate, next_axis, lesson)
        update_registry_and_matrix(full_result, full_gate)
        append_recovery({"event_type": "candidate_full_completed", "description": f"{prompt_id} completed full all-current.", "decision": full_gate})
        return 0 if full_gate["status"] in {"learning_evidence", "new_working_best", "target_met"} else 2
    lesson = "Micro-pack rejected the candidate before all-current, preserving model time and protecting case 67/control gates."
    next_axis = "Use a v020c load-bearing ordering ablation or remove the new guard entirely before another hypothesis."
    append_metrics_block(micro_result, "rejected", lesson, next_axis)
    write_diagnosis(micro_result, micro_gate, next_axis, lesson)
    update_registry_and_matrix(micro_result, micro_gate)
    append_recovery({"event_type": "candidate_micro_rejected", "description": f"{prompt_id} rejected by micro-pack.", "decision": micro_gate})
    return 2


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init")
    sub.add_parser("author-v026a")
    sub.add_parser("author-v026b")
    sub.add_parser("author-v026c")
    sub.add_parser("author-v026d")
    sub.add_parser("author-v026e")
    sub.add_parser("author-v026f")
    sub.add_parser("author-v026g")
    sub.add_parser("author-v026h")
    sub.add_parser("author-v026i")
    sub.add_parser("author-v026j")
    sub.add_parser("author-v026k")
    sub.add_parser("author-v026l")
    sub.add_parser("author-v026m")
    sub.add_parser("author-v026n")
    sub.add_parser("author-v026o")
    sub.add_parser("author-v026p")
    sub.add_parser("author-v026q")
    sub.add_parser("baseline-micro")
    run_parser = sub.add_parser("run-candidate")
    run_parser.add_argument("prompt_id")
    args = parser.parse_args(argv)
    if args.command == "init":
        init_package()
        return 0
    if args.command == "author-v026a":
        if not (PACKAGE_ROOT / "source_manifest.json").exists():
            init_package()
        print(author_v026a())
        return 0
    if args.command == "author-v026b":
        if not (PACKAGE_ROOT / "source_manifest.json").exists():
            init_package()
        print(author_v026b())
        return 0
    if args.command == "author-v026c":
        if not (PACKAGE_ROOT / "source_manifest.json").exists():
            init_package()
        print(author_v026c())
        return 0
    if args.command == "author-v026d":
        if not (PACKAGE_ROOT / "source_manifest.json").exists():
            init_package()
        print(author_v026d())
        return 0
    if args.command == "author-v026e":
        if not (PACKAGE_ROOT / "source_manifest.json").exists():
            init_package()
        print(author_v026e())
        return 0
    if args.command == "author-v026f":
        if not (PACKAGE_ROOT / "source_manifest.json").exists():
            init_package()
        print(author_v026f())
        return 0
    if args.command == "author-v026g":
        if not (PACKAGE_ROOT / "source_manifest.json").exists():
            init_package()
        print(author_v026g())
        return 0
    if args.command == "author-v026h":
        if not (PACKAGE_ROOT / "source_manifest.json").exists():
            init_package()
        print(author_v026h())
        return 0
    if args.command == "author-v026i":
        if not (PACKAGE_ROOT / "source_manifest.json").exists():
            init_package()
        print(author_v026i())
        return 0
    if args.command == "author-v026j":
        if not (PACKAGE_ROOT / "source_manifest.json").exists():
            init_package()
        print(author_v026j())
        return 0
    if args.command == "author-v026k":
        if not (PACKAGE_ROOT / "source_manifest.json").exists():
            init_package()
        print(author_v026k())
        return 0
    if args.command == "author-v026l":
        if not (PACKAGE_ROOT / "source_manifest.json").exists():
            init_package()
        print(author_v026l())
        return 0
    if args.command == "author-v026m":
        if not (PACKAGE_ROOT / "source_manifest.json").exists():
            init_package()
        print(author_v026m())
        return 0
    if args.command == "author-v026n":
        if not (PACKAGE_ROOT / "source_manifest.json").exists():
            init_package()
        print(author_v026n())
        return 0
    if args.command == "author-v026o":
        if not (PACKAGE_ROOT / "source_manifest.json").exists():
            init_package()
        print(author_v026o())
        return 0
    if args.command == "author-v026p":
        if not (PACKAGE_ROOT / "source_manifest.json").exists():
            init_package()
        print(author_v026p())
        return 0
    if args.command == "author-v026q":
        if not (PACKAGE_ROOT / "source_manifest.json").exists():
            init_package()
        print(author_v026q())
        return 0
    if args.command == "baseline-micro":
        if not (PACKAGE_ROOT / "source_manifest.json").exists():
            init_package()
        ensure_baseline_micro()
        return 0
    if args.command == "run-candidate":
        return run_candidate(args.prompt_id)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
