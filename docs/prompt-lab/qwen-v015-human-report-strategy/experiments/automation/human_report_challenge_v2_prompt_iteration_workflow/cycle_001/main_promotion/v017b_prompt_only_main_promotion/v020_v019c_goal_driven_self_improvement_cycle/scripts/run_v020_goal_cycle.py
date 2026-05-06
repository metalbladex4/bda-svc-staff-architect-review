#!/usr/bin/env python3
"""Run one step of the v020 v019c goal-driven prompt cycle.

This runner deliberately does not generate multiple candidates. Use:

- init
- run-anchor
- run-candidate v020a --overlay overlays/v020a_*.yaml
"""

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


CAPSTONE_ROOT = Path("/home/williambenitez1/Capstone")
WORKTREE_ROOT = Path(
    "/home/williambenitez1/Capstone_worktrees/"
    "1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement"
)
PACKAGE_ROOT = Path(__file__).resolve().parents[1]
V019_ROOT = PACKAGE_ROOT.parent / "v019_v018e_creative_followup_cycle"
ALL_CURRENT_MANIFEST = (
    PACKAGE_ROOT.parents[2]
    / "pre_adoption/v017b_group_box_rejection/validation_manifests/"
    "human_report_challenge_v2_all_current_117_no101.yaml"
)
OFFICE_NEGATIVE_MANIFEST = (
    PACKAGE_ROOT.parents[3] / "validation_manifests/legacy_abstention_guard_office_negative.yaml"
)
OVERLAY_DIR = PACKAGE_ROOT / "overlays"
RUNS_DIR = PACKAGE_ROOT / "runs"
DIAG_DIR = PACKAGE_ROOT / "diagnoses"
SCRATCH_PARENT = Path("/home/williambenitez1/Capstone_worktrees")
OPENAI_BASE_URL = "http://localhost:11434/v1"
OPENAI_API_KEY = "no-auth"
MODEL = "qwen3-vl:8b-instruct"
UPSTREAM_COMMIT = "f462ef4516b63ca1a2cd2434e75692f65d0e94cb"

V019C_BASELINE = {
    "candidate_id": "v019c_context_shadow_reversal",
    "match_count": 174,
    "false_negative_count": 45,
    "false_positive_count": 28,
    "controls_pass": True,
}
SUCCESS_TARGET = {"false_negative_count": 25, "false_positive_count": 15}
DENSE_CASES = ("66", "67", "84", "97")
REQUIRED_PLACEHOLDERS = ("{categories}", "{detection_guidance}", "{bbox_format}", "{bbox_scale}")


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected JSON object")
    return payload


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _read_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle) or {}
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected YAML mapping")
    return payload


def _write_yaml(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=False), encoding="utf-8")


def _run(cmd: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> dict[str, Any]:
    completed = subprocess.run(
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
        "cwd": str(cwd),
        "returncode": completed.returncode,
        "stdout_tail": (completed.stdout or "")[-4000:],
        "stderr_tail": (completed.stderr or "")[-4000:],
    }


def _manifest_cases(manifest_path: Path) -> list[dict[str, Any]]:
    payload = _read_yaml(manifest_path)
    cases = payload.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError(f"{manifest_path}: missing cases")
    return cases


def _resolve(raw: str | Path, base: Path) -> Path:
    path = Path(raw)
    if not path.is_absolute():
        path = (base / path).resolve()
    return path


def _latest_summary(eval_dir: Path) -> Path | None:
    summaries = sorted(eval_dir.glob("evaluation_*_summary.json"))
    return summaries[-1] if summaries else None


def _prompt_hash(prompt: str) -> str:
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()


def _extract_prompt(overlay_path: Path) -> str:
    overlay = _read_yaml(overlay_path)
    try:
        prompt = overlay["overrides"]["prompts"]["detect_objects"]
    except KeyError as exc:
        raise ValueError(f"{overlay_path}: missing overrides.prompts.detect_objects") from exc
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError(f"{overlay_path}: empty detect prompt")
    return prompt


def _validate_prompt(candidate_id: str, prompt: str) -> dict[str, bool]:
    placeholders = {token: token in prompt for token in REQUIRED_PLACEHOLDERS}
    missing = [token for token, present in placeholders.items() if not present]
    if missing:
        raise ValueError(f"{candidate_id}: missing placeholders {missing}")
    lowered = prompt.lower()
    forbidden = ["human-report", "human report text", "case 101", "case 155", "case 166"]
    hits = [term for term in forbidden if term in lowered]
    if hits:
        raise ValueError(f"{candidate_id}: prompt includes forbidden text {hits}")
    return placeholders


def _check_endpoint() -> dict[str, Any]:
    url = f"{OPENAI_BASE_URL}/models"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        return {"url": url, "status": "unavailable", "error": repr(exc)}
    ids = [item.get("id") for item in payload.get("data", []) if isinstance(item, dict)]
    return {"url": url, "status": "available" if MODEL in ids else "model_missing", "model_ids": ids}


def _validate_manifests() -> dict[str, Any]:
    all_cases = _manifest_cases(ALL_CURRENT_MANIFEST)
    office_cases = _manifest_cases(OFFICE_NEGATIVE_MANIFEST)
    ids = [str(case["case_id"]) for case in all_cases]
    result = {
        "all_current_manifest": str(ALL_CURRENT_MANIFEST),
        "all_current_count": len(all_cases),
        "all_current_has_101": any(case_id.endswith("101") for case_id in ids),
        "all_current_has_155": any(case_id.endswith("155") for case_id in ids),
        "all_current_has_166": any(case_id.endswith("166") for case_id in ids),
        "office_negative_manifest": str(OFFICE_NEGATIVE_MANIFEST),
        "office_negative_count": len(office_cases),
    }
    if result["all_current_count"] != 117:
        raise ValueError(f"Expected 117 all-current cases, got {result['all_current_count']}")
    if result["all_current_has_101"]:
        raise ValueError("case 101 appears in all-current no101 manifest")
    if not result["all_current_has_155"] or not result["all_current_has_166"]:
        raise ValueError("positive controls 155/166 missing")
    if result["office_negative_count"] != 1:
        raise ValueError(f"Expected one office-negative case, got {result['office_negative_count']}")
    return result


def _create_scratch(candidate_id: str) -> Path:
    stamp = dt.datetime.now(dt.UTC).strftime("%Y%m%d_%H%M%SZ")
    scratch = SCRATCH_PARENT / f"_scratch_v020_{candidate_id}_{stamp}"
    result = _run(["git", "worktree", "add", "--detach", str(scratch), "upstream/main"], cwd=CAPSTONE_ROOT)
    if result["returncode"] != 0:
        raise RuntimeError(result["stderr_tail"])
    head = _run(["git", "rev-parse", "HEAD"], cwd=scratch)
    if head["returncode"] != 0 or head["stdout_tail"].strip() != UPSTREAM_COMMIT:
        raise RuntimeError(f"{scratch}: unexpected upstream commit {head['stdout_tail']}")
    return scratch


def _remove_scratch(scratch: Path) -> dict[str, Any]:
    if not scratch.exists():
        return {"scratch": str(scratch), "status": "already_absent"}
    result = _run(["git", "worktree", "remove", "--force", str(scratch)], cwd=CAPSTONE_ROOT)
    return {"scratch": str(scratch), "status": "removed" if result["returncode"] == 0 else "remove_failed", "command": result}


def _patch_scratch_config(scratch: Path, prompt: str) -> None:
    config_path = scratch / "src/bda_svc/pipeline/config.yaml"
    config = _read_yaml(config_path)
    config["prompts"]["detect_objects"] = prompt
    config["detection_vlm"]["model"] = MODEL
    config["assessment_vlm"]["model"] = MODEL
    _write_yaml(config_path, config)


def _run_manifest(candidate_id: str, manifest_path: Path, scratch: Path, run_root: Path) -> dict[str, Any]:
    cases = _manifest_cases(manifest_path)
    timestamp = dt.datetime.now(dt.UTC).strftime("%Y-%m-%d_%H%M%SZ")
    output_root = run_root / f"{manifest_path.stem}_{timestamp}"
    predicted_dir = output_root / "predicted"
    eval_dir = output_root / "eval"
    predicted_dir.mkdir(parents=True, exist_ok=True)
    eval_dir.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.update(
        {
            "OPENAI_BASE_URL": OPENAI_BASE_URL,
            "OPENAI_API_KEY": OPENAI_API_KEY,
            "BDA_DETECTION_MODEL": MODEL,
            "BDA_ASSESSMENT_MODEL": MODEL,
        }
    )
    commands: list[dict[str, Any]] = []
    missing_outputs: list[str] = []
    start = time.time()
    for index, case in enumerate(cases, start=1):
        image_path = _resolve(case["image_path"], manifest_path.parent)
        before = set(predicted_dir.glob(f"{image_path.stem}_*.json"))
        cmd = ["uv", "run", "bda-svc", "-i", str(image_path), "-o", str(predicted_dir)]
        entry = _run(cmd, cwd=scratch, env=env)
        commands.append(entry)
        print(
            f"[{candidate_id}] {manifest_path.stem}: {index}/{len(cases)} {image_path.name} rc={entry['returncode']}",
            flush=True,
        )
        if entry["returncode"] != 0:
            break
        after = set(predicted_dir.glob(f"{image_path.stem}_*.json"))
        if not (after - before):
            missing_outputs.append(image_path.name)
            break
    if commands and all(item["returncode"] == 0 for item in commands) and not missing_outputs:
        eval_cmd = [
            "uv",
            "run",
            "python",
            "main.py",
            "--manifest",
            str(manifest_path),
            "-p",
            str(predicted_dir),
            "-o",
            str(eval_dir),
        ]
        commands.append(_run(eval_cmd, cwd=WORKTREE_ROOT / "bda_eval", env=env))
    summary_path = _latest_summary(eval_dir)
    summary_payload = _read_json(summary_path) if summary_path else None
    payload = {
        "generated_utc": dt.datetime.now(dt.UTC).isoformat(),
        "candidate_id": candidate_id,
        "manifest_path": str(manifest_path),
        "scratch_worktree": str(scratch),
        "openai_base_url": OPENAI_BASE_URL,
        "model": MODEL,
        "predicted_dir": str(predicted_dir),
        "eval_dir": str(eval_dir),
        "summary_path": str(summary_path) if summary_path else None,
        "evaluation_summary": summary_payload,
        "missing_outputs": missing_outputs,
        "commands": commands,
        "elapsed_seconds": round(time.time() - start, 3),
        "succeeded": bool(commands)
        and all(item["returncode"] == 0 for item in commands)
        and not missing_outputs
        and summary_path is not None,
    }
    summary_file = output_root / "upstream_code_manifest_run_summary.json"
    _write_json(summary_file, payload)
    return payload | {"run_summary_path": str(summary_file)}


def _case(summary: dict[str, Any], image_filename: str) -> dict[str, Any]:
    images = {item["image_filename"]: item for item in summary["images"]}
    item = images[image_filename]
    return {
        "reference_target_count": item["reference_target_count"],
        "predicted_target_count": item["predicted_target_count"],
        "match_count": item["match_count"],
        "false_negative_count": item["false_negative_count"],
        "false_positive_count": item["false_positive_count"],
    }


def _totals(run_payload: dict[str, Any]) -> dict[str, Any]:
    summary = run_payload["evaluation_summary"]
    totals = summary["totals"]
    return {
        "image_count": summary["image_count"],
        "match_count": totals["match_count"],
        "false_negative_count": totals["false_negative_count"],
        "false_positive_count": totals["false_positive_count"],
    }


def _candidate_result(candidate_id: str, overlay_path: Path, all_run: dict[str, Any], office_run: dict[str, Any]) -> dict[str, Any]:
    all_summary = all_run["evaluation_summary"]
    office_summary = office_run["evaluation_summary"]
    totals = _totals(all_run)
    office_totals = office_summary["totals"]
    case_155 = _case(all_summary, "155.jpg")
    case_166 = _case(all_summary, "166.jpg")
    dense = {case: _case(all_summary, f"{case}.jpg") for case in DENSE_CASES}
    controls_pass = (
        case_155["match_count"] >= 1
        and case_166["match_count"] >= 1
        and office_totals["negative_scene_abstention_correct_count"] == 1
        and office_totals["negative_scene_false_positive_count"] == 0
    )
    disqualified = not controls_pass or not all_run["succeeded"] or not office_run["succeeded"]
    success_target = (
        controls_pass
        and totals["false_negative_count"] <= SUCCESS_TARGET["false_negative_count"]
        and totals["false_positive_count"] <= SUCCESS_TARGET["false_positive_count"]
    )
    return {
        "candidate_id": candidate_id,
        "overlay_path": str(overlay_path),
        **totals,
        "case_155": case_155,
        "case_166": case_166,
        "dense_cases": dense,
        "office_negative": {
            "image_count": office_summary["image_count"],
            "match_count": office_totals["match_count"],
            "false_negative_count": office_totals["false_negative_count"],
            "false_positive_count": office_totals["false_positive_count"],
            "negative_scene_abstention_correct_count": office_totals["negative_scene_abstention_correct_count"],
            "negative_scene_false_positive_count": office_totals["negative_scene_false_positive_count"],
        },
        "controls_pass": controls_pass,
        "disqualified": disqualified,
        "success_target": success_target,
        "delta_vs_v019c": {
            "match_count": totals["match_count"] - V019C_BASELINE["match_count"],
            "false_negative_count": totals["false_negative_count"] - V019C_BASELINE["false_negative_count"],
            "false_positive_count": totals["false_positive_count"] - V019C_BASELINE["false_positive_count"],
        },
        "all_current_run_summary": all_run["run_summary_path"],
        "office_negative_run_summary": office_run["run_summary_path"],
        "nonzero_command_count": sum(1 for c in all_run["commands"] + office_run["commands"] if c["returncode"] != 0),
        "missing_outputs": all_run["missing_outputs"] + office_run["missing_outputs"],
    }


def _load_matrix() -> dict[str, Any]:
    path = PACKAGE_ROOT / "comparison_matrix.json"
    if path.exists():
        return _read_json(path)
    return {
        "cycle_id": "v020_v019c_goal_driven_self_improvement_cycle",
        "baseline": V019C_BASELINE,
        "success_target": SUCCESS_TARGET,
        "anchor_replay": None,
        "results": [],
        "balanced_incumbent": V019C_BASELINE,
        "recall_ceiling_near_miss": None,
        "events": [],
    }


def _replacement_reason(candidate: dict[str, Any], incumbent: dict[str, Any]) -> str | None:
    if candidate["disqualified"]:
        return None
    if candidate["success_target"]:
        return "success_target"
    if candidate["false_positive_count"] < incumbent["false_positive_count"] and candidate["match_count"] >= incumbent["match_count"]:
        return "reduces_fps_without_losing_matches"
    if candidate["match_count"] > incumbent["match_count"] and candidate["false_positive_count"] <= incumbent["false_positive_count"]:
        return "increases_matches_without_raising_fps"
    if (
        candidate["match_count"] >= incumbent["match_count"]
        and candidate["false_negative_count"] <= incumbent["false_negative_count"]
        and candidate["false_positive_count"] <= incumbent["false_positive_count"]
        and (
            candidate["match_count"] > incumbent["match_count"]
            or candidate["false_negative_count"] < incumbent["false_negative_count"]
            or candidate["false_positive_count"] < incumbent["false_positive_count"]
        )
    ):
        return "dominates_incumbent"
    return None


def _update_matrix(result: dict[str, Any], *, anchor: bool = False) -> dict[str, Any]:
    matrix = _load_matrix()
    if anchor:
        matrix["anchor_replay"] = result
    else:
        matrix["results"].append(result)
        incumbent = matrix["balanced_incumbent"]
        reason = _replacement_reason(result, incumbent)
        if reason:
            updated = dict(result)
            updated["replacement_reason"] = reason
            matrix["balanced_incumbent"] = updated
        if not result["disqualified"]:
            near = matrix.get("recall_ceiling_near_miss")
            if near is None or result["match_count"] > near["match_count"]:
                matrix["recall_ceiling_near_miss"] = result
    matrix["generated_utc"] = dt.datetime.now(dt.UTC).isoformat()
    _write_json(PACKAGE_ROOT / "comparison_matrix.json", matrix)
    _write_json(PACKAGE_ROOT / "final_recommendation.json", matrix)
    return matrix


def _diagnosis(result: dict[str, Any], matrix: dict[str, Any]) -> dict[str, Any]:
    preserve: list[str] = []
    avoid: list[str] = []
    if result["controls_pass"]:
        preserve.append("kept 155, 166, and office-negative safe")
    else:
        avoid.append("control failure disqualifies the candidate")
    if result["match_count"] >= V019C_BASELINE["match_count"]:
        preserve.append("preserved or improved v019c match count")
    else:
        avoid.append("lost matches versus v019c")
    if result["false_positive_count"] <= V019C_BASELINE["false_positive_count"]:
        preserve.append("preserved or reduced v019c false positives")
    else:
        avoid.append("raised false positives versus v019c")
    if result["dense_cases"]["67"]["match_count"] <= 3:
        avoid.append("case 67 dense formation recall remains weak")
    if result["dense_cases"]["66"]["false_positive_count"] >= 5:
        avoid.append("case 66 still carries dense/row false positives")
    if result["dense_cases"]["84"]["false_negative_count"] >= 6:
        avoid.append("case 84 still misses many large-scene targets")
    if result["success_target"]:
        next_axis = "success target reached; prepare closeout"
    elif len(matrix.get("results", [])) and len(matrix["results"]) % 3 == 0:
        next_axis = "pivot with systematic debugging and artifact review before the next candidate"
    elif result["false_positive_count"] > V019C_BASELINE["false_positive_count"]:
        next_axis = "tighten FP veto while preserving full-image recall"
    elif result["match_count"] < V019C_BASELINE["match_count"]:
        next_axis = "restore recall without weakening the v019c context-shadow filter"
    else:
        next_axis = "preserve balanced gains and test one sharper local axis"
    return {
        "generated_utc": dt.datetime.now(dt.UTC).isoformat(),
        "candidate_id": result["candidate_id"],
        "metrics": {
            "match_count": result["match_count"],
            "false_negative_count": result["false_negative_count"],
            "false_positive_count": result["false_positive_count"],
            "delta_vs_v019c": result["delta_vs_v019c"],
        },
        "controls": {
            "case_155": result["case_155"],
            "case_166": result["case_166"],
            "office_negative": result["office_negative"],
        },
        "dense_cases": result["dense_cases"],
        "fp_fn_pattern": {
            "false_negative_count": result["false_negative_count"],
            "false_positive_count": result["false_positive_count"],
            "dense_case_snapshot": result["dense_cases"],
        },
        "preserve": preserve,
        "avoid": avoid,
        "next_axis": next_axis,
    }


def _write_diagnosis(result: dict[str, Any], diagnosis: dict[str, Any]) -> None:
    _write_json(DIAG_DIR / f"{result['candidate_id']}_diagnosis.json", diagnosis)
    md = f"""# {result['candidate_id']} Diagnosis

Generated: `{diagnosis['generated_utc']}`

## Metrics

| Candidate | Matches | FNs | FPs | Delta vs v019c |
| --- | ---: | ---: | ---: | --- |
| `{result['candidate_id']}` | {result['match_count']} | {result['false_negative_count']} | {result['false_positive_count']} | {result['delta_vs_v019c']['match_count']} / {result['delta_vs_v019c']['false_negative_count']} / {result['delta_vs_v019c']['false_positive_count']} |

## Dense Cases

| Case | Matches | FNs | FPs |
| --- | ---: | ---: | ---: |
"""
    for case, item in result["dense_cases"].items():
        md += f"| {case} | {item['match_count']} | {item['false_negative_count']} | {item['false_positive_count']} |\n"
    md += "\n## Controls\n\n"
    md += f"- 155: {result['case_155']}\n"
    md += f"- 166: {result['case_166']}\n"
    md += f"- office-negative: {result['office_negative']}\n"
    md += "\n## FP/FN Pattern\n\n"
    md += f"- false negatives: {result['false_negative_count']}\n"
    md += f"- false positives: {result['false_positive_count']}\n"
    md += "\n## Preserve\n\n"
    for item in diagnosis["preserve"]:
        md += f"- {item}\n"
    md += "\n## Avoid\n\n"
    for item in diagnosis["avoid"]:
        md += f"- {item}\n"
    md += f"\n## Next Axis\n\n{diagnosis['next_axis']}\n"
    (DIAG_DIR / f"{result['candidate_id']}_diagnosis.md").write_text(md, encoding="utf-8")


def _write_source_manifest() -> None:
    endpoint = _check_endpoint()
    manifest_checks = _validate_manifests()
    source = {
        "generated_utc": dt.datetime.now(dt.UTC).isoformat(),
        "cycle_id": "v020_v019c_goal_driven_self_improvement_cycle",
        "purpose": "Goal-driven sequential follow-up from v019c_context_shadow_reversal.",
        "upstream_commit": UPSTREAM_COMMIT,
        "runtime_path": "current upstream/main code with Ollama OpenAI-compatible endpoint",
        "openai_base_url": OPENAI_BASE_URL,
        "model": MODEL,
        "manifest_checks": manifest_checks,
        "endpoint_check": endpoint,
        "source_artifacts": {
            "v019_final_recommendation": str(V019_ROOT / "final_recommendation.md"),
            "v019_comparison_matrix": str(V019_ROOT / "comparison_matrix.json"),
            "v019c_overlay": str(V019_ROOT / "overlays/v019c_context_shadow_reversal.yaml"),
            "v019c_diagnosis": str(V019_ROOT / "diagnoses/v019c_context_shadow_reversal_diagnosis.md"),
        },
        "boundaries": {
            "case_101": False,
            "commit_or_push": False,
            "doctrine_edit": False,
            "runtime_adoption": False,
            "source_truth_mutation": False,
        },
    }
    _write_json(PACKAGE_ROOT / "source_manifest.json", source)


def init_package() -> int:
    OVERLAY_DIR.mkdir(parents=True, exist_ok=True)
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    DIAG_DIR.mkdir(parents=True, exist_ok=True)
    v019c_prompt = _extract_prompt(V019_ROOT / "overlays/v019c_context_shadow_reversal.yaml")
    _validate_prompt("v019c_anchor_replay", v019c_prompt)
    anchor_overlay = {
        "overlay_id": "qwen-1.2-v019c_anchor_replay",
        "overlay_type": "experiment",
        "model_line": MODEL,
        "description": "Fresh replay of v019c_context_shadow_reversal before v020 candidate authoring.",
        "generated_from": ["v019c_context_shadow_reversal"],
        "overrides": {
            "prompts": {"detect_objects": v019c_prompt},
            "runtime": {"notes": "Prompt text is applied by scratch upstream config replacement; no runtime adoption."},
        },
    }
    _write_yaml(OVERLAY_DIR / "v019c_anchor_replay.yaml", anchor_overlay)
    _write_source_manifest()
    matrix = _load_matrix()
    _write_json(PACKAGE_ROOT / "comparison_matrix.json", matrix)
    _write_json(PACKAGE_ROOT / "final_recommendation.json", matrix)
    return 0


def _run_overlay(candidate_id: str, overlay_path: Path, *, anchor: bool = False) -> int:
    prompt = _extract_prompt(overlay_path)
    placeholders = _validate_prompt(candidate_id, prompt)
    scratch: Path | None = None
    try:
        scratch = _create_scratch(candidate_id)
        _patch_scratch_config(scratch, prompt)
        run_root = RUNS_DIR / candidate_id
        office_run = _run_manifest(candidate_id, OFFICE_NEGATIVE_MANIFEST, scratch, run_root / "office_negative")
        all_run = _run_manifest(candidate_id, ALL_CURRENT_MANIFEST, scratch, run_root / "all_current_no101")
        result = _candidate_result(candidate_id, overlay_path, all_run, office_run)
        result["prompt_sha256"] = _prompt_hash(prompt)
        result["placeholders"] = placeholders
        matrix = _update_matrix(result, anchor=anchor)
        diagnosis = _diagnosis(result, matrix)
        _write_diagnosis(result, diagnosis)
        if result["nonzero_command_count"] or result["missing_outputs"] or result["disqualified"]:
            return 3
        return 0
    finally:
        if scratch is not None:
            cleanup = _remove_scratch(scratch)
            _write_json(RUNS_DIR / candidate_id / "scratch_cleanup.json", cleanup)


def run_anchor() -> int:
    overlay_path = OVERLAY_DIR / "v019c_anchor_replay.yaml"
    if not overlay_path.exists():
        init_package()
    return _run_overlay("v019c_anchor_replay", overlay_path, anchor=True)


def run_candidate(candidate_id: str, overlay_path: Path) -> int:
    if not candidate_id.startswith("v020"):
        raise ValueError("candidate_id must increment from v020a, v020b, ...")
    return _run_overlay(candidate_id, overlay_path, anchor=False)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init")
    sub.add_parser("run-anchor")
    run_candidate_parser = sub.add_parser("run-candidate")
    run_candidate_parser.add_argument("candidate_id")
    run_candidate_parser.add_argument("--overlay", required=True)
    args = parser.parse_args(argv)
    if args.command == "init":
        return init_package()
    if args.command == "run-anchor":
        return run_anchor()
    if args.command == "run-candidate":
        return run_candidate(args.candidate_id, Path(args.overlay).resolve())
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
