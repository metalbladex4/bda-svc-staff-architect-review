#!/usr/bin/env python3
"""Run the v022 literal-99 Qwen prompt refinement cycle.

This harness keeps execution on fetched upstream/main code, replacing only
prompts.detect_objects in a scratch worktree for each candidate.
"""

from __future__ import annotations

import argparse
import datetime as dt
import difflib
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
WORKFLOW_ROOT = (
    WORKTREE_ROOT
    / "docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/"
    "human_report_challenge_v2_prompt_iteration_workflow"
)
PACKAGE_ROOT = Path(__file__).resolve().parents[1]
SCRATCH_PARENT = Path("/home/williambenitez1/Capstone_worktrees")
PROMOTION_ROOT = PACKAGE_ROOT.parent

ALL_CURRENT_MANIFEST = (
    WORKFLOW_ROOT
    / "cycle_001/pre_adoption/v017b_group_box_rejection/validation_manifests/"
    "human_report_challenge_v2_all_current_117_no101.yaml"
)
OFFICE_NEGATIVE_MANIFEST = (
    WORKFLOW_ROOT / "validation_manifests/legacy_abstention_guard_office_negative.yaml"
)
V020C_OVERLAY = (
    PROMOTION_ROOT
    / "v020_v019c_goal_driven_self_improvement_cycle/overlays/"
    "v020c_v019c_extra_box_audit.yaml"
)

PREFERRED_BACKEND = {
    "backend_id": "upstream_openai_compat_preferred_8000",
    "openai_base_url": "http://localhost:8000/v1",
    "model": "Qwen/Qwen3-VL-8B-Instruct",
    "openai_api_key": "EMPTY",
    "server_kind": "preferred_upstream_openai_compatible_endpoint",
}
FALLBACK_BACKEND = {
    "backend_id": "ollama_openai_compat_fallback_11434",
    "openai_base_url": "http://localhost:11434/v1",
    "model": "qwen3-vl:8b-instruct",
    "openai_api_key": "no-auth",
    "server_kind": "fallback_ollama_openai_compatible_endpoint",
}

REQUIRED_PLACEHOLDERS = ("{categories}", "{detection_guidance}", "{bbox_format}", "{bbox_scale}")
DENSE_CASES = ("66", "67", "84", "97")
POSITIVE_CONTROLS = ("155", "166")
UPSTREAM_BASELINE = {"match_count": 181, "false_negative_count": 38, "false_positive_count": 36}
LITERAL_99_TARGET_MAX_ERRORS = 1


def _utc() -> str:
    return dt.datetime.now(dt.UTC).isoformat()


def _sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


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


def _run(
    cmd: list[str],
    *,
    cwd: Path,
    env: dict[str, str] | None = None,
    timeout: float | None = None,
) -> dict[str, Any]:
    start = time.time()
    try:
        completed = subprocess.run(
            cmd,
            cwd=cwd,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
        )
        return {
            "cmd": cmd,
            "cwd": str(cwd),
            "returncode": completed.returncode,
            "stdout_tail": (completed.stdout or "")[-4000:],
            "stderr_tail": (completed.stderr or "")[-4000:],
            "elapsed_seconds": round(time.time() - start, 3),
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "cmd": cmd,
            "cwd": str(cwd),
            "returncode": 124,
            "stdout_tail": (exc.stdout or "")[-4000:] if isinstance(exc.stdout, str) else "",
            "stderr_tail": (exc.stderr or "")[-4000:] if isinstance(exc.stderr, str) else "",
            "elapsed_seconds": round(time.time() - start, 3),
            "timeout": timeout,
        }


def _git_show(ref: str, path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{ref}:{path}"], cwd=CAPSTONE_ROOT)


def _git_ref(ref: str) -> str:
    return subprocess.check_output(["git", "rev-parse", ref], cwd=CAPSTONE_ROOT, text=True).strip()


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


def _extract_prompt_from_overlay(path: Path) -> str:
    payload = _read_yaml(path)
    try:
        prompt = payload["overrides"]["prompts"]["detect_objects"]
    except KeyError as exc:
        raise ValueError(f"{path}: missing overrides.prompts.detect_objects") from exc
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError(f"{path}: empty detect_objects prompt")
    return prompt


def _prompt_sources() -> dict[str, dict[str, Any]]:
    sources: dict[str, dict[str, Any]] = {
        "v020c_anchor_replay": {
            "title": "v020c anchor replay",
            "source": str(V020C_OVERLAY),
            "prompt": _extract_prompt_from_overlay(V020C_OVERLAY),
        }
    }
    for overlay in sorted((PACKAGE_ROOT / "overlays").glob("*.yaml")):
        payload = _read_yaml(overlay)
        prompt_id = str(payload.get("candidate_id") or overlay.stem)
        sources[prompt_id] = {
            "title": str(payload.get("title") or prompt_id),
            "source": str(overlay),
            "prompt": _extract_prompt_from_overlay(overlay),
        }
    return sources


def _validate_prompt(prompt_id: str, prompt: str) -> dict[str, bool]:
    placeholders = {token: token in prompt for token in REQUIRED_PLACEHOLDERS}
    missing = [token for token, present in placeholders.items() if not present]
    if missing:
        raise ValueError(f"{prompt_id}: missing placeholders {missing}")
    lowered = prompt.lower()
    forbidden = ["human report text", "case 101", "case 155", "case 166"]
    hits = [term for term in forbidden if term in lowered]
    if hits:
        raise ValueError(f"{prompt_id}: prompt includes forbidden text {hits}")
    return placeholders


def _check_endpoint(base_url: str, model: str, timeout: float = 5.0) -> dict[str, Any]:
    url = f"{base_url.rstrip('/')}/models"
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except Exception as exc:  # noqa: BLE001 - preserve exact endpoint failure
        return {"url": url, "status": "unavailable", "error": repr(exc), "model": model}
    ids = [item.get("id") for item in payload.get("data", []) if isinstance(item, dict)]
    return {
        "url": url,
        "status": "available" if model in ids else "model_missing",
        "model": model,
        "model_ids": ids,
    }


def _append_recovery(event: dict[str, Any]) -> None:
    path = PACKAGE_ROOT / "recovery_log.json"
    payload = _read_json(path) if path.exists() else {"events": []}
    payload["events"].append({"generated_utc": _utc(), **event})
    _write_json(path, payload)
    lines = ["# Recovery Log", ""]
    for item in payload["events"]:
        lines.append(f"- `{item['generated_utc']}` `{item.get('type', 'event')}`: {item.get('message', '')}")
    (PACKAGE_ROOT / "recovery_log.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _select_backend() -> dict[str, Any]:
    attempts: list[dict[str, Any]] = []
    first = _check_endpoint(PREFERRED_BACKEND["openai_base_url"], PREFERRED_BACKEND["model"])
    attempts.append({"backend": PREFERRED_BACKEND, "check": first})
    if first["status"] == "available":
        return {"selected": PREFERRED_BACKEND, "attempts": attempts, "fallback_used": False}
    time.sleep(2)
    retry = _check_endpoint(PREFERRED_BACKEND["openai_base_url"], PREFERRED_BACKEND["model"])
    attempts.append({"backend": PREFERRED_BACKEND, "check": retry, "recovery_attempt": "preferred_endpoint_retry"})
    if retry["status"] == "available":
        return {"selected": PREFERRED_BACKEND, "attempts": attempts, "fallback_used": False}
    fallback = _check_endpoint(FALLBACK_BACKEND["openai_base_url"], FALLBACK_BACKEND["model"])
    attempts.append({"backend": FALLBACK_BACKEND, "check": fallback, "recovery_attempt": "authorized_fallback"})
    if fallback["status"] != "available":
        _append_recovery(
            {
                "type": "endpoint_unavailable",
                "message": "Preferred and fallback OpenAI-compatible Qwen endpoints unavailable.",
                "attempts": attempts,
            }
        )
        raise RuntimeError("No Qwen OpenAI-compatible endpoint is available")
    _append_recovery(
        {
            "type": "backend_fallback",
            "message": "Preferred localhost:8000/v1 unavailable after retry; using authorized Ollama OpenAI-compatible fallback.",
            "attempts": attempts,
        }
    )
    return {"selected": FALLBACK_BACKEND, "attempts": attempts, "fallback_used": True}


def _validate_manifests() -> dict[str, Any]:
    all_cases = _manifest_cases(ALL_CURRENT_MANIFEST)
    office_cases = _manifest_cases(OFFICE_NEGATIVE_MANIFEST)
    all_ids = [str(case["case_id"]) for case in all_cases]
    office_ids = [str(case["case_id"]) for case in office_cases]
    result = {
        "all_current_manifest": str(ALL_CURRENT_MANIFEST),
        "all_current_count": len(all_cases),
        "all_current_has_101": any(case_id.endswith("101") for case_id in all_ids),
        "all_current_has_155": any(case_id.endswith("155") for case_id in all_ids),
        "all_current_has_166": any(case_id.endswith("166") for case_id in all_ids),
        "office_negative_manifest": str(OFFICE_NEGATIVE_MANIFEST),
        "office_negative_count": len(office_cases),
        "office_negative_ids": office_ids,
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


def _doctrine_report() -> dict[str, Any]:
    local_path = CAPSTONE_ROOT / "src/bda_svc/pipeline/doctrine.yaml"
    local = local_path.read_bytes()
    upstream = _git_show("upstream/main", "src/bda_svc/pipeline/doctrine.yaml")
    same = local == upstream
    diff = "".join(
        difflib.unified_diff(
            local.decode("utf-8").splitlines(keepends=True),
            upstream.decode("utf-8").splitlines(keepends=True),
            fromfile=str(local_path),
            tofile="upstream/main:src/bda_svc/pipeline/doctrine.yaml",
        )
    )
    report = {
        "generated_utc": _utc(),
        "same": same,
        "local_path": str(local_path),
        "local_sha256": _sha_bytes(local),
        "upstream_ref": "upstream/main:src/bda_svc/pipeline/doctrine.yaml",
        "upstream_sha256": _sha_bytes(upstream),
        "doctrine_variant": "shared" if same else "upstream_main_only_for_v022",
        "diff": diff,
    }
    _write_json(PACKAGE_ROOT / "doctrine_diff_report.json", report)
    md = "# Doctrine Diff Report\n\n"
    md += f"Generated: `{report['generated_utc']}`\n\n"
    md += f"- identical: `{same}`\n"
    md += f"- local SHA-256: `{report['local_sha256']}`\n"
    md += f"- upstream SHA-256: `{report['upstream_sha256']}`\n\n"
    md += "```diff\n" + (diff if diff else "# no differences\n") + "```\n"
    (PACKAGE_ROOT / "doctrine_diff_report.md").write_text(md, encoding="utf-8")
    return report


def _create_scratch(row_id: str, upstream_commit: str) -> Path:
    stamp = dt.datetime.now(dt.UTC).strftime("%Y%m%d_%H%M%SZ")
    scratch = SCRATCH_PARENT / f"_scratch_v022_{row_id}_{stamp}"
    result = _run(["git", "worktree", "add", "--detach", str(scratch), "upstream/main"], cwd=CAPSTONE_ROOT)
    if result["returncode"] != 0:
        raise RuntimeError(result["stderr_tail"])
    head = _run(["git", "rev-parse", "HEAD"], cwd=scratch)
    if head["returncode"] != 0 or head["stdout_tail"].strip() != upstream_commit:
        raise RuntimeError(f"{scratch}: unexpected upstream commit {head['stdout_tail']}")
    return scratch


def _remove_scratch(scratch: Path) -> dict[str, Any]:
    if not scratch.exists():
        return {"scratch": str(scratch), "status": "already_absent"}
    result = _run(["git", "worktree", "remove", "--force", str(scratch)], cwd=CAPSTONE_ROOT)
    return {"scratch": str(scratch), "status": "removed" if result["returncode"] == 0 else "remove_failed", "command": result}


def _patch_scratch(scratch: Path, prompt: str) -> None:
    config_path = scratch / "src/bda_svc/pipeline/config.yaml"
    config = _read_yaml(config_path)
    config["prompts"]["detect_objects"] = prompt
    _write_yaml(config_path, config)


def _run_manifest(
    *,
    row_id: str,
    manifest_path: Path,
    scratch: Path,
    run_root: Path,
    backend: dict[str, Any],
) -> dict[str, Any]:
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
            "OPENAI_BASE_URL": backend["openai_base_url"],
            "OPENAI_API_KEY": backend["openai_api_key"],
            "BDA_DETECTION_MODEL": backend["model"],
            "BDA_ASSESSMENT_MODEL": backend["model"],
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
            f"[{row_id}] {manifest_path.stem}: {index}/{len(cases)} {image_path.name} rc={entry['returncode']}",
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
        "generated_utc": _utc(),
        "row_id": row_id,
        "manifest_path": str(manifest_path),
        "scratch_worktree": str(scratch),
        "backend": backend,
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
    summary_file = output_root / "upstream_openai_compat_manifest_run_summary.json"
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


def _row_result(
    *,
    row_id: str,
    prompt_id: str,
    prompt_info: dict[str, Any],
    backend: dict[str, Any],
    all_run: dict[str, Any],
    office_run: dict[str, Any],
) -> dict[str, Any]:
    all_summary = all_run["evaluation_summary"]
    office_summary = office_run["evaluation_summary"]
    totals = all_summary["totals"]
    office_totals = office_summary["totals"]
    positive = {case: _case(all_summary, f"{case}.jpg") for case in POSITIVE_CONTROLS}
    dense = {case: _case(all_summary, f"{case}.jpg") for case in DENSE_CASES}
    controls_pass = (
        positive["155"]["match_count"] >= 1
        and positive["166"]["match_count"] >= 1
        and office_totals["negative_scene_abstention_correct_count"] == 1
        and office_totals["negative_scene_false_positive_count"] == 0
    )
    total_errors = totals["false_negative_count"] + totals["false_positive_count"]
    return {
        "row_id": row_id,
        "prompt_id": prompt_id,
        "backend_id": backend["backend_id"],
        "openai_base_url": backend["openai_base_url"],
        "server_kind": backend["server_kind"],
        "model": backend["model"],
        "prompt_sha256": prompt_info["prompt_sha256"],
        "prompt_source": prompt_info["source"],
        "image_count": all_summary["image_count"],
        "match_count": totals["match_count"],
        "false_negative_count": totals["false_negative_count"],
        "false_positive_count": totals["false_positive_count"],
        "total_error_count": total_errors,
        "literal_99_target_met": total_errors <= LITERAL_99_TARGET_MAX_ERRORS,
        "case_155": positive["155"],
        "case_166": positive["166"],
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
        "disqualified": not controls_pass or not all_run["succeeded"] or not office_run["succeeded"],
        "all_current_run_summary": all_run["run_summary_path"],
        "office_negative_run_summary": office_run["run_summary_path"],
        "nonzero_command_count": sum(1 for c in all_run["commands"] + office_run["commands"] if c["returncode"] != 0),
        "missing_outputs": all_run["missing_outputs"] + office_run["missing_outputs"],
        "elapsed_seconds": round(all_run["elapsed_seconds"] + office_run["elapsed_seconds"], 3),
    }


def _load_matrix() -> dict[str, Any]:
    path = PACKAGE_ROOT / "comparison_matrix.json"
    if path.exists():
        return _read_json(path)
    return {
        "matrix_id": "v022_literal99_qwen_recursive_prompt_refinement_cycle",
        "generated_utc": _utc(),
        "results": [],
        "rankings": [],
    }


def _rank_rows(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    eligible = [row for row in results if not row["disqualified"]]
    eligible.sort(key=lambda row: (row["total_error_count"], -row["match_count"], row["prompt_id"]))
    return [
        {
            "rank": index,
            "row_id": row["row_id"],
            "prompt_id": row["prompt_id"],
            "match_count": row["match_count"],
            "false_negative_count": row["false_negative_count"],
            "false_positive_count": row["false_positive_count"],
            "total_error_count": row["total_error_count"],
            "literal_99_target_met": row["literal_99_target_met"],
        }
        for index, row in enumerate(eligible, start=1)
    ]


def _write_matrix(matrix: dict[str, Any]) -> None:
    results = matrix.get("results", [])
    matrix["generated_utc"] = _utc()
    matrix["rankings"] = _rank_rows(results)
    _write_json(PACKAGE_ROOT / "comparison_matrix.json", matrix)
    _write_json(PACKAGE_ROOT / "final_recommendation.json", matrix)
    _write_matrix_md(matrix)
    _write_final_md(matrix)


def _write_matrix_md(matrix: dict[str, Any]) -> None:
    lines = [
        "# v022 Literal-99 Qwen Comparison Matrix",
        "",
        f"Generated: `{matrix['generated_utc']}`",
        "",
        "| Prompt | Matches | FNs | FPs | Total Errors | 155 | 166 | Office | Target | Backend |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |",
    ]
    for row in sorted(matrix.get("results", []), key=lambda r: r["prompt_id"]):
        lines.append(
            "| "
            f"`{row['prompt_id']}` | {row['match_count']} | {row['false_negative_count']} | "
            f"{row['false_positive_count']} | {row['total_error_count']} | "
            f"{row['case_155']['match_count']}/{row['case_155']['false_negative_count']}/{row['case_155']['false_positive_count']} | "
            f"{row['case_166']['match_count']}/{row['case_166']['false_negative_count']}/{row['case_166']['false_positive_count']} | "
            f"{row['office_negative']['negative_scene_abstention_correct_count']}/1 | "
            f"`{row['literal_99_target_met']}` | `{row['backend_id']}` |"
        )
    lines.append("")
    lines.append("## Ranking")
    lines.append("")
    for row in matrix.get("rankings", []):
        lines.append(
            f"{row['rank']}. `{row['prompt_id']}` - {row['match_count']} matches / "
            f"{row['false_negative_count']} FNs / {row['false_positive_count']} FPs "
            f"({row['total_error_count']} total errors)"
        )
    (PACKAGE_ROOT / "comparison_matrix.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_final_md(matrix: dict[str, Any]) -> None:
    rankings = matrix.get("rankings") or []
    top = rankings[0] if rankings else None
    lines = [
        "# v022 Final Recommendation",
        "",
        f"Generated: `{matrix['generated_utc']}`",
        "",
        "## Literal Target",
        "",
        f"- upstream error baseline: `{UPSTREAM_BASELINE['false_negative_count'] + UPSTREAM_BASELINE['false_positive_count']}`",
        f"- literal 99% target: `<= {LITERAL_99_TARGET_MAX_ERRORS}` combined false negatives + false positives",
        "",
    ]
    if top:
        lines.extend(
            [
                "## Current Incumbent",
                "",
                f"- `{top['prompt_id']}`: {top['match_count']} matches / "
                f"{top['false_negative_count']} FNs / {top['false_positive_count']} FPs "
                f"({top['total_error_count']} total errors)",
                f"- literal target met: `{top['literal_99_target_met']}`",
                "",
            ]
        )
    lines.extend(
        [
            "## Boundary",
            "",
            "- This package is prompt-lab evidence only.",
            "- No source truth, doctrine, assessment prompt, runtime code, PR, commit, or push is adopted here.",
            "- Backend labels distinguish preferred upstream OpenAI-compatible service from fallback Ollama OpenAI-compatible service.",
        ]
    )
    (PACKAGE_ROOT / "final_recommendation.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_diagnosis(result: dict[str, Any]) -> None:
    diag = {
        "generated_utc": _utc(),
        "candidate": result["prompt_id"],
        "metrics": {
            "match_count": result["match_count"],
            "false_negative_count": result["false_negative_count"],
            "false_positive_count": result["false_positive_count"],
            "total_error_count": result["total_error_count"],
            "literal_99_target_met": result["literal_99_target_met"],
        },
        "controls_pass": result["controls_pass"],
        "case_155": result["case_155"],
        "case_166": result["case_166"],
        "office_negative": result["office_negative"],
        "dense_cases": result["dense_cases"],
        "backend": {
            "backend_id": result["backend_id"],
            "openai_base_url": result["openai_base_url"],
            "model": result["model"],
            "server_kind": result["server_kind"],
        },
        "run_summaries": {
            "all_current": result["all_current_run_summary"],
            "office_negative": result["office_negative_run_summary"],
        },
    }
    _write_json(PACKAGE_ROOT / "diagnoses" / f"{result['prompt_id']}_diagnosis.json", diag)
    lines = [
        f"# {result['prompt_id']} Diagnosis",
        "",
        f"Generated: `{diag['generated_utc']}`",
        "",
        "## Metrics",
        "",
        f"- matches: `{result['match_count']}`",
        f"- false negatives: `{result['false_negative_count']}`",
        f"- false positives: `{result['false_positive_count']}`",
        f"- total errors: `{result['total_error_count']}`",
        f"- literal 99% target met: `{result['literal_99_target_met']}`",
        "",
        "## Dense Cases",
        "",
        "| Case | Matches | FNs | FPs |",
        "| --- | ---: | ---: | ---: |",
    ]
    for case, payload in result["dense_cases"].items():
        lines.append(f"| `{case}` | {payload['match_count']} | {payload['false_negative_count']} | {payload['false_positive_count']} |")
    lines.extend(
        [
            "",
            "## Controls",
            "",
            f"- case 155: `{result['case_155']}`",
            f"- case 166: `{result['case_166']}`",
            f"- office-negative: `{result['office_negative']}`",
            "",
            "## Next Diagnosis Slot",
            "",
            "Fill after comparing this candidate to the current incumbent before authoring the next prompt.",
        ]
    )
    (PACKAGE_ROOT / "diagnoses" / f"{result['prompt_id']}_diagnosis.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def init_package() -> int:
    (PACKAGE_ROOT / "runs").mkdir(parents=True, exist_ok=True)
    (PACKAGE_ROOT / "logs").mkdir(parents=True, exist_ok=True)
    fetch = _run(["git", "fetch", "upstream", "main"], cwd=CAPSTONE_ROOT)
    upstream_commit = _git_ref("upstream/main")
    upstream_config = _git_show("upstream/main", "src/bda_svc/pipeline/config.yaml")
    upstream_doctrine = _git_show("upstream/main", "src/bda_svc/pipeline/doctrine.yaml")
    doctrine = _doctrine_report()
    manifests = _validate_manifests()
    backend_selection = _select_backend()
    prompts = []
    for prompt_id, info in _prompt_sources().items():
        placeholders = _validate_prompt(prompt_id, info["prompt"])
        prompts.append(
            {
                "prompt_id": prompt_id,
                "title": info["title"],
                "source": info["source"],
                "prompt_sha256": _sha_text(info["prompt"]),
                "prompt_chars": len(info["prompt"]),
                "prompt_lines": len(info["prompt"].splitlines()),
                "placeholders": placeholders,
            }
        )
    backend_preflight = {
        "generated_utc": _utc(),
        "fetch_upstream_main": fetch,
        "upstream_commit": upstream_commit,
        "backend_source": "upstream/main OpenAI-compatible VLMBackend",
        "preferred_backend": PREFERRED_BACKEND,
        "fallback_backend": FALLBACK_BACKEND,
        "selection": backend_selection,
    }
    _write_json(PACKAGE_ROOT / "backend_preflight.json", backend_preflight)
    _write_json(PACKAGE_ROOT / "candidate_registry.json", {"generated_utc": _utc(), "prompts": prompts})
    source_manifest = {
        "generated_utc": _utc(),
        "package": str(PACKAGE_ROOT),
        "matrix_id": "v022_literal99_qwen_recursive_prompt_refinement_cycle",
        "upstream_commit": upstream_commit,
        "upstream_config_sha256": _sha_bytes(upstream_config),
        "upstream_doctrine_sha256": _sha_bytes(upstream_doctrine),
        "manifest_checks": manifests,
        "doctrine": doctrine,
        "literal_99_target": {
            "baseline_false_negatives": UPSTREAM_BASELINE["false_negative_count"],
            "baseline_false_positives": UPSTREAM_BASELINE["false_positive_count"],
            "baseline_total_errors": UPSTREAM_BASELINE["false_negative_count"] + UPSTREAM_BASELINE["false_positive_count"],
            "target_total_errors_max": LITERAL_99_TARGET_MAX_ERRORS,
        },
        "backend_preflight": str(PACKAGE_ROOT / "backend_preflight.json"),
        "candidate_registry": str(PACKAGE_ROOT / "candidate_registry.json"),
        "runtime_boundary": {
            "code_path": "scratch worktrees from upstream/main",
            "prompt_surface": "detect_objects only",
            "qwen_only": True,
            "source_truth_mutation": False,
            "runtime_adoption": False,
            "commit_push_pr": False,
        },
    }
    _write_json(PACKAGE_ROOT / "source_manifest.json", source_manifest)
    readme = f"""# v022 Literal-99 Qwen Recursive Prompt Refinement Cycle

Generated: `{source_manifest['generated_utc']}`

This package runs Qwen-only sequential prompt candidates through fetched
`upstream/main` OpenAI-compatible runtime code. It replaces only
`prompts.detect_objects` in scratch worktrees.

Literal 99% target: reduce the current upstream prompt's 74 total detection
errors to <=1 combined false negatives + false positives on
`human_report_challenge_v2_all_current_117_no101`.

No prompt, doctrine, source truth, runtime code, PR, commit, or push is adopted
by this package.
"""
    (PACKAGE_ROOT / "README.md").write_text(readme, encoding="utf-8")
    if not (PACKAGE_ROOT / "research_notes.md").exists():
        (PACKAGE_ROOT / "research_notes.md").write_text(
            "# v022 Research Notes\n\n"
            "- Qwen3-VL official materials emphasize stronger 2D grounding and OpenAI-compatible serving.\n"
            "- Qwen2.5-VL official grounding examples show concise JSON bbox prompts as the family pattern.\n"
            "- Local v020/v021 evidence is the primary decision source for this cycle.\n",
            encoding="utf-8",
        )
    matrix = _load_matrix()
    matrix["source_manifest"] = str(PACKAGE_ROOT / "source_manifest.json")
    matrix["candidate_registry"] = str(PACKAGE_ROOT / "candidate_registry.json")
    _write_matrix(matrix)
    return 0


def run_candidate(prompt_id: str, *, force: bool = False) -> int:
    if not (PACKAGE_ROOT / "source_manifest.json").exists():
        init_package()
    prompt_sources = _prompt_sources()
    if prompt_id not in prompt_sources:
        raise ValueError(f"unknown prompt id: {prompt_id}")
    matrix = _load_matrix()
    row_id = f"qwen__{prompt_id}"
    if any(row.get("row_id") == row_id for row in matrix.get("results", [])) and not force:
        print(f"[skip] {row_id} already exists; use --force to rerun", flush=True)
        return 0
    backend = _select_backend()["selected"]
    info = dict(prompt_sources[prompt_id])
    prompt = info["prompt"]
    placeholders = _validate_prompt(prompt_id, prompt)
    info["prompt_sha256"] = _sha_text(prompt)
    scratch: Path | None = None
    try:
        upstream_commit = _git_ref("upstream/main")
        scratch = _create_scratch(row_id, upstream_commit)
        _patch_scratch(scratch, prompt)
        run_root = PACKAGE_ROOT / "runs" / prompt_id
        office_run = _run_manifest(
            row_id=row_id,
            manifest_path=OFFICE_NEGATIVE_MANIFEST,
            scratch=scratch,
            run_root=run_root / "office_negative",
            backend=backend,
        )
        all_run = _run_manifest(
            row_id=row_id,
            manifest_path=ALL_CURRENT_MANIFEST,
            scratch=scratch,
            run_root=run_root / "all_current_no101",
            backend=backend,
        )
        if not all_run.get("evaluation_summary") or not office_run.get("evaluation_summary"):
            raise RuntimeError(f"{row_id}: missing evaluation summary; see run summaries")
        result = _row_result(
            row_id=row_id,
            prompt_id=prompt_id,
            prompt_info=info,
            backend=backend,
            all_run=all_run,
            office_run=office_run,
        )
        result["placeholders"] = placeholders
        if force:
            matrix["results"] = [row for row in matrix.get("results", []) if row.get("row_id") != row_id]
        matrix.setdefault("results", []).append(result)
        _write_matrix(matrix)
        _write_diagnosis(result)
        if result["nonzero_command_count"] or result["missing_outputs"] or result["disqualified"]:
            _append_recovery(
                {
                    "type": "candidate_completed_with_warning",
                    "message": f"{row_id} completed but is disqualified or has command/output warnings.",
                    "row_id": row_id,
                }
            )
            return 3
        return 0
    finally:
        if scratch is not None:
            cleanup = _remove_scratch(scratch)
            _write_json(PACKAGE_ROOT / "runs" / prompt_id / "scratch_cleanup.json", cleanup)


def summarize() -> int:
    matrix = _load_matrix()
    _write_matrix(matrix)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init")
    sub.add_parser("summarize")
    run_parser = sub.add_parser("run-candidate")
    run_parser.add_argument("prompt_id")
    run_parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)
    if args.command == "init":
        return init_package()
    if args.command == "summarize":
        return summarize()
    if args.command == "run-candidate":
        return run_candidate(args.prompt_id, force=args.force)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
