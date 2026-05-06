#!/usr/bin/env python3
"""Run the v021 OpenAI-compatible cross-model prompt matrix.

This script keeps inference on the fetched upstream/main runtime code path
while using local prompt-lab/eval artifacts for repeatable comparison.
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
GEMMA_OLLAMA_BIN = Path("/home/williambenitez1/.local/lib/ollama-local/bin/ollama")

ALL_CURRENT_MANIFEST = (
    WORKFLOW_ROOT
    / "cycle_001/pre_adoption/v017b_group_box_rejection/validation_manifests/"
    "human_report_challenge_v2_all_current_117_no101.yaml"
)
OFFICE_NEGATIVE_MANIFEST = (
    WORKFLOW_ROOT / "validation_manifests/legacy_abstention_guard_office_negative.yaml"
)

V009_VERSION = (
    CAPSTONE_ROOT
    / "z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/"
    "1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/versions/"
    "v009_unified_best-stack.yaml"
)
V017B_OVERLAY = WORKFLOW_ROOT / "cycle_001/candidates/v017b/overlay.yaml"
PROMOTION_ROOT = PACKAGE_ROOT.parent
V018E_OVERLAY = (
    PROMOTION_ROOT / "upstream_v017b_amalgamation_cycle/overlays/v018e_contrastive_body_anchor.yaml"
)
V019C_OVERLAY = (
    PROMOTION_ROOT / "v019_v018e_creative_followup_cycle/overlays/v019c_context_shadow_reversal.yaml"
)
V020C_OVERLAY = (
    PROMOTION_ROOT
    / "v020_v019c_goal_driven_self_improvement_cycle/overlays/v020c_v019c_extra_box_audit.yaml"
)

REQUIRED_PLACEHOLDERS = ("{categories}", "{detection_guidance}", "{bbox_format}", "{bbox_scale}")
DENSE_CASES = ("66", "67", "84", "97")
POSITIVE_CONTROLS = ("155", "166")

MODEL_ROWS = {
    "qwen3_vl_8b_instruct": {
        "label": "Qwen3-VL 8B Instruct",
        "openai_base_url": "http://localhost:11434/v1",
        "openai_api_key": "no-auth",
        "model": "qwen3-vl:8b-instruct",
        "server_kind": "ollama_openai_compatible_endpoint",
        "startup": None,
    },
    "gemma4_e4b": {
        "label": "Gemma 4 E4B",
        "openai_base_url": "http://localhost:11435/v1",
        "openai_api_key": "no-auth",
        "model": "gemma4:e4b",
        "server_kind": "ollama_openai_compatible_endpoint",
        "startup": {
            "OLLAMA_HOST": "127.0.0.1:11435",
            "OLLAMA_MODELS": "/home/williambenitez1/.ollama-gemma4-models",
        },
    },
}


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


def _git_text(ref: str, path: str) -> str:
    return _git_show(ref, path).decode("utf-8")


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


def _extract_v009_prompt() -> str:
    payload = _read_yaml(V009_VERSION)
    try:
        prompt = payload["prompt_surfaces"]["detect_objects"]
    except KeyError as exc:
        raise ValueError(f"{V009_VERSION}: missing prompt_surfaces.detect_objects") from exc
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError(f"{V009_VERSION}: empty detect_objects prompt")
    return prompt


def _extract_upstream_prompt() -> str:
    payload = yaml.safe_load(_git_text("upstream/main", "src/bda_svc/pipeline/config.yaml"))
    return payload["prompts"]["detect_objects"]


def _prompt_sources() -> dict[str, dict[str, Any]]:
    return {
        "upstream_main_config_prompt": {
            "title": "Current upstream/main config prompt",
            "source": "upstream/main:src/bda_svc/pipeline/config.yaml",
            "prompt": _extract_upstream_prompt(),
        },
        "v009_unified_best_stack": {
            "title": "v009 unified best stack",
            "source": str(V009_VERSION),
            "prompt": _extract_v009_prompt(),
        },
        "v017b_group_box_rejection": {
            "title": "v017b group box rejection",
            "source": str(V017B_OVERLAY),
            "prompt": _extract_prompt_from_overlay(V017B_OVERLAY),
        },
        "v018e_contrastive_body_anchor": {
            "title": "v018e contrastive body anchor",
            "source": str(V018E_OVERLAY),
            "prompt": _extract_prompt_from_overlay(V018E_OVERLAY),
        },
        "v019c_context_shadow_reversal": {
            "title": "v019c context shadow reversal",
            "source": str(V019C_OVERLAY),
            "prompt": _extract_prompt_from_overlay(V019C_OVERLAY),
        },
        "v020c_extra_box_audit": {
            "title": "v020c extra box audit",
            "source": str(V020C_OVERLAY),
            "prompt": _extract_prompt_from_overlay(V020C_OVERLAY),
        },
    }


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
    except Exception as exc:  # noqa: BLE001 - record exact preflight failure
        return {"url": url, "status": "unavailable", "error": repr(exc), "model": model}
    ids = [item.get("id") for item in payload.get("data", []) if isinstance(item, dict)]
    return {
        "url": url,
        "status": "available" if model in ids else "model_missing",
        "model": model,
        "model_ids": ids,
    }


def _start_gemma_if_needed() -> dict[str, Any]:
    row = MODEL_ROWS["gemma4_e4b"]
    first = _check_endpoint(row["openai_base_url"], row["model"])
    if first["status"] == "available":
        return {
            "needed_start": False,
            "endpoint_check": first,
            "ollama_binary": str(GEMMA_OLLAMA_BIN if GEMMA_OLLAMA_BIN.exists() else Path("ollama")),
        }
    env = os.environ.copy()
    env.update(row["startup"] or {})
    logs_dir = PACKAGE_ROOT / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_path = logs_dir / "gemma_ollama_11435.log"
    handle = log_path.open("ab")
    ollama_binary = str(GEMMA_OLLAMA_BIN if GEMMA_OLLAMA_BIN.exists() else Path("ollama"))
    process = subprocess.Popen(  # noqa: S603 - controlled local command
        [ollama_binary, "serve"],
        cwd=CAPSTONE_ROOT,
        env=env,
        stdout=handle,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    checks: list[dict[str, Any]] = [first]
    final = first
    for _ in range(60):
        time.sleep(1)
        final = _check_endpoint(row["openai_base_url"], row["model"], timeout=2.0)
        checks.append(final)
        if final["status"] == "available":
            break
        if process.poll() is not None:
            break
    return {
        "needed_start": True,
        "pid": process.pid,
        "log_path": str(log_path),
        "ollama_binary": ollama_binary,
        "startup_env_keys": sorted((row["startup"] or {}).keys()),
        "checks": checks,
        "endpoint_check": final,
        "process_returncode": process.poll(),
    }


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
    local_lines = local.decode("utf-8").splitlines(keepends=True)
    upstream_lines = upstream.decode("utf-8").splitlines(keepends=True)
    diff = "".join(
        difflib.unified_diff(
            local_lines,
            upstream_lines,
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
        "local_bytes": len(local),
        "upstream_bytes": len(upstream),
        "doctrine_variants": ["shared"] if same else ["local", "upstream_main"],
        "diff": diff,
    }
    _write_json(PACKAGE_ROOT / "doctrine_diff_report.json", report)
    md = "# Doctrine Diff Report\n\n"
    md += f"Generated: `{report['generated_utc']}`\n\n"
    md += f"- identical: `{same}`\n"
    md += f"- local SHA-256: `{report['local_sha256']}`\n"
    md += f"- upstream SHA-256: `{report['upstream_sha256']}`\n"
    md += f"- active doctrine variants: `{', '.join(report['doctrine_variants'])}`\n\n"
    md += "## Diff\n\n"
    md += "```diff\n" + (diff if diff else "# no differences\n") + "```\n"
    (PACKAGE_ROOT / "doctrine_diff_report.md").write_text(md, encoding="utf-8")
    return report


def _create_scratch(row_id: str, upstream_commit: str) -> Path:
    stamp = dt.datetime.now(dt.UTC).strftime("%Y%m%d_%H%M%SZ")
    scratch = SCRATCH_PARENT / f"_scratch_v021_{row_id}_{stamp}"
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


def _patch_scratch(scratch: Path, prompt: str, doctrine_variant: str) -> None:
    config_path = scratch / "src/bda_svc/pipeline/config.yaml"
    config = _read_yaml(config_path)
    config["prompts"]["detect_objects"] = prompt
    _write_yaml(config_path, config)
    if doctrine_variant == "local":
        shutil.copy2(CAPSTONE_ROOT / "src/bda_svc/pipeline/doctrine.yaml", scratch / "src/bda_svc/pipeline/doctrine.yaml")
    elif doctrine_variant not in {"shared", "upstream_main"}:
        raise ValueError(f"unknown doctrine variant: {doctrine_variant}")


def _run_manifest(
    *,
    row_id: str,
    manifest_path: Path,
    scratch: Path,
    run_root: Path,
    model_row: dict[str, Any],
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
            "OPENAI_BASE_URL": model_row["openai_base_url"],
            "OPENAI_API_KEY": model_row["openai_api_key"],
            "BDA_DETECTION_MODEL": model_row["model"],
            "BDA_ASSESSMENT_MODEL": model_row["model"],
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
        "openai_base_url": model_row["openai_base_url"],
        "server_kind": model_row["server_kind"],
        "model": model_row["model"],
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


def _totals(run_payload: dict[str, Any]) -> dict[str, Any]:
    summary = run_payload["evaluation_summary"]
    totals = summary["totals"]
    return {
        "image_count": summary["image_count"],
        "match_count": totals["match_count"],
        "false_negative_count": totals["false_negative_count"],
        "false_positive_count": totals["false_positive_count"],
    }


def _row_result(
    *,
    row_id: str,
    prompt_id: str,
    model_id: str,
    doctrine_variant: str,
    prompt_info: dict[str, Any],
    model_row: dict[str, Any],
    all_run: dict[str, Any],
    office_run: dict[str, Any],
) -> dict[str, Any]:
    all_summary = all_run["evaluation_summary"]
    office_summary = office_run["evaluation_summary"]
    totals = _totals(all_run)
    office_totals = office_summary["totals"]
    positive = {case: _case(all_summary, f"{case}.jpg") for case in POSITIVE_CONTROLS}
    dense = {case: _case(all_summary, f"{case}.jpg") for case in DENSE_CASES}
    controls_pass = (
        positive["155"]["match_count"] >= 1
        and positive["166"]["match_count"] >= 1
        and office_totals["negative_scene_abstention_correct_count"] == 1
        and office_totals["negative_scene_false_positive_count"] == 0
    )
    disqualified = not controls_pass or not all_run["succeeded"] or not office_run["succeeded"]
    return {
        "row_id": row_id,
        "prompt_id": prompt_id,
        "model_id": model_id,
        "model": model_row["model"],
        "openai_base_url": model_row["openai_base_url"],
        "server_kind": model_row["server_kind"],
        "doctrine_variant": doctrine_variant,
        "prompt_sha256": prompt_info["prompt_sha256"],
        "prompt_source": prompt_info["source"],
        **totals,
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
        "disqualified": disqualified,
        "all_current_run_summary": all_run["run_summary_path"],
        "office_negative_run_summary": office_run["run_summary_path"],
        "nonzero_command_count": sum(1 for c in all_run["commands"] + office_run["commands"] if c["returncode"] != 0),
        "missing_outputs": all_run["missing_outputs"] + office_run["missing_outputs"],
        "elapsed_seconds": round(all_run["elapsed_seconds"] + office_run["elapsed_seconds"], 3),
    }


def _failed_case() -> dict[str, int]:
    return {
        "reference_target_count": 0,
        "predicted_target_count": 0,
        "match_count": 0,
        "false_negative_count": 0,
        "false_positive_count": 0,
    }


def _failed_row_result(
    *,
    row_id: str,
    prompt_id: str,
    model_id: str,
    doctrine_variant: str,
    prompt_info: dict[str, Any],
    model_row: dict[str, Any],
    all_run: dict[str, Any],
    office_run: dict[str, Any],
    reason: str,
) -> dict[str, Any]:
    return {
        "row_id": row_id,
        "prompt_id": prompt_id,
        "model_id": model_id,
        "model": model_row["model"],
        "openai_base_url": model_row["openai_base_url"],
        "server_kind": model_row["server_kind"],
        "doctrine_variant": doctrine_variant,
        "prompt_sha256": prompt_info["prompt_sha256"],
        "prompt_source": prompt_info["source"],
        "image_count": 0,
        "match_count": 0,
        "false_negative_count": 0,
        "false_positive_count": 0,
        "case_155": _failed_case(),
        "case_166": _failed_case(),
        "dense_cases": {case: _failed_case() for case in DENSE_CASES},
        "office_negative": {
            "image_count": 0,
            "match_count": 0,
            "false_negative_count": 0,
            "false_positive_count": 0,
            "negative_scene_abstention_correct_count": 0,
            "negative_scene_false_positive_count": 0,
        },
        "controls_pass": False,
        "disqualified": True,
        "failure_reason": reason,
        "all_current_run_summary": all_run["run_summary_path"],
        "office_negative_run_summary": office_run["run_summary_path"],
        "nonzero_command_count": sum(1 for c in all_run["commands"] + office_run["commands"] if c["returncode"] != 0),
        "missing_outputs": all_run["missing_outputs"] + office_run["missing_outputs"],
        "elapsed_seconds": round(all_run["elapsed_seconds"] + office_run["elapsed_seconds"], 3),
    }


def _load_matrix() -> dict[str, Any]:
    path = PACKAGE_ROOT / "cross_model_comparison_matrix.json"
    if path.exists():
        return _read_json(path)
    return {
        "matrix_id": "v021_openai_compat_cross_model_prompt_matrix",
        "generated_utc": _utc(),
        "results": [],
        "rankings": {},
        "verdict": None,
    }


def _rank_rows(results: list[dict[str, Any]]) -> dict[str, Any]:
    by_model: dict[str, list[dict[str, Any]]] = {}
    for row in results:
        by_model.setdefault(row["model_id"], []).append(row)
    rankings: dict[str, Any] = {}
    for model_id, rows in by_model.items():
        eligible = [row for row in rows if not row["disqualified"]]
        eligible.sort(
            key=lambda row: (
                -row["match_count"],
                row["false_negative_count"],
                row["false_positive_count"],
                row["prompt_id"],
            )
        )
        rankings[model_id] = [
            {
                "rank": index,
                "row_id": row["row_id"],
                "prompt_id": row["prompt_id"],
                "match_count": row["match_count"],
                "false_negative_count": row["false_negative_count"],
                "false_positive_count": row["false_positive_count"],
                "controls_pass": row["controls_pass"],
            }
            for index, row in enumerate(eligible, start=1)
        ]
    eligible_all = [row for row in results if not row["disqualified"]]
    eligible_all.sort(
        key=lambda row: (
            -row["match_count"],
            row["false_negative_count"],
            row["false_positive_count"],
            row["model_id"],
            row["prompt_id"],
        )
    )
    rankings["overall"] = [
        {
            "rank": index,
            "row_id": row["row_id"],
            "model_id": row["model_id"],
            "prompt_id": row["prompt_id"],
            "match_count": row["match_count"],
            "false_negative_count": row["false_negative_count"],
            "false_positive_count": row["false_positive_count"],
            "controls_pass": row["controls_pass"],
        }
        for index, row in enumerate(eligible_all, start=1)
    ]
    return rankings


def _write_matrix(matrix: dict[str, Any]) -> None:
    results = matrix.get("results", [])
    matrix["generated_utc"] = _utc()
    matrix["rankings"] = _rank_rows(results)
    _write_json(PACKAGE_ROOT / "cross_model_comparison_matrix.json", matrix)
    _write_json(PACKAGE_ROOT / "final_recommendation.json", matrix)
    _write_matrix_md(matrix)
    _write_final_md(matrix)


def _write_matrix_md(matrix: dict[str, Any]) -> None:
    lines = [
        "# v021 OpenAI-Compatible Cross-Model Prompt Matrix",
        "",
        f"Generated: `{matrix['generated_utc']}`",
        "",
        "| Model | Prompt | Matches | FNs | FPs | 155 | 166 | Office | Disqualified |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for row in sorted(matrix.get("results", []), key=lambda r: (r["model_id"], r["prompt_id"], r["doctrine_variant"])):
        lines.append(
            "| "
            f"`{row['model_id']}` | `{row['prompt_id']}` | "
            f"{row['match_count']} | {row['false_negative_count']} | {row['false_positive_count']} | "
            f"{row['case_155']['match_count']}/{row['case_155']['false_negative_count']}/{row['case_155']['false_positive_count']} | "
            f"{row['case_166']['match_count']}/{row['case_166']['false_negative_count']}/{row['case_166']['false_positive_count']} | "
            f"{row['office_negative']['negative_scene_abstention_correct_count']}/1 | "
            f"`{row['disqualified']}` |"
        )
    lines.append("")
    lines.append("## Rankings")
    lines.append("")
    for model_id, rows in matrix.get("rankings", {}).items():
        lines.append(f"### {model_id}")
        lines.append("")
        for row in rows:
            lines.append(
                f"{row['rank']}. `{row['row_id']}` - "
                f"{row['match_count']} matches / {row['false_negative_count']} FNs / {row['false_positive_count']} FPs"
            )
        lines.append("")
    (PACKAGE_ROOT / "cross_model_comparison_matrix.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_final_md(matrix: dict[str, Any]) -> None:
    overall = matrix.get("rankings", {}).get("overall", [])
    top = overall[0] if overall else None
    lines = [
        "# v021 Final Recommendation",
        "",
        f"Generated: `{matrix['generated_utc']}`",
        "",
    ]
    if top:
        lines.append(
            "Current top row by primary ranking: "
            f"`{top['row_id']}` at {top['match_count']} matches / "
            f"{top['false_negative_count']} FNs / {top['false_positive_count']} FPs."
        )
        lines.append("")
    lines.extend(
        [
            "## Recommendation Boundary",
            "",
            "- This package is comparison evidence only.",
            "- No prompt, doctrine, runtime config, source truth, PR, commit, or push is adopted here.",
            "- The OpenAI-compatible `OPENAI_BASE_URL` upstream-code path is the comparison default recorded by this wave.",
            "- Ollama-backed `/v1` endpoints are labeled as OpenAI-compatible Ollama endpoints, not pure upstream vLLM/server.",
            "",
            "## Follow-Up",
            "",
            "- Use the matrix winner only as a candidate for review unless a later promotion wave approves adoption.",
            "- Inspect dense cases `66`, `67`, `84`, and `97` before any promotion decision.",
        ]
    )
    (PACKAGE_ROOT / "final_recommendation.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _row_exists(matrix: dict[str, Any], row_id: str) -> bool:
    return any(row.get("row_id") == row_id for row in matrix.get("results", []))


def _append_recovery(event: dict[str, Any]) -> None:
    path = PACKAGE_ROOT / "recovery_log.json"
    payload = _read_json(path) if path.exists() else {"events": []}
    payload["events"].append({"generated_utc": _utc(), **event})
    _write_json(path, payload)
    lines = ["# Recovery Log", ""]
    for item in payload["events"]:
        lines.append(f"- `{item['generated_utc']}` `{item.get('type', 'event')}`: {item.get('message', '')}")
    (PACKAGE_ROOT / "recovery_log.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def init_package() -> int:
    (PACKAGE_ROOT / "runs").mkdir(parents=True, exist_ok=True)
    (PACKAGE_ROOT / "logs").mkdir(parents=True, exist_ok=True)
    fetch = _run(["git", "fetch", "upstream", "main"], cwd=CAPSTONE_ROOT)
    upstream_commit = _git_ref("upstream/main")
    upstream_config = _git_show("upstream/main", "src/bda_svc/pipeline/config.yaml")
    upstream_doctrine = _git_show("upstream/main", "src/bda_svc/pipeline/doctrine.yaml")
    prompt_sources = _prompt_sources()
    registry = []
    for prompt_id, info in prompt_sources.items():
        placeholders = _validate_prompt(prompt_id, info["prompt"])
        registry.append(
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
        info["prompt_sha256"] = _sha_text(info["prompt"])
    doctrine = _doctrine_report()
    manifests = _validate_manifests()
    gemma = _start_gemma_if_needed()
    endpoint_checks = {
        "qwen3_vl_8b_instruct": _check_endpoint(
            MODEL_ROWS["qwen3_vl_8b_instruct"]["openai_base_url"],
            MODEL_ROWS["qwen3_vl_8b_instruct"]["model"],
        ),
        "gemma4_e4b": gemma["endpoint_check"],
    }
    backend_preflight = {
        "generated_utc": _utc(),
        "fetch_upstream_main": fetch,
        "upstream_commit": upstream_commit,
        "backend_source": "upstream/main:src/bda_svc/pipeline/interfaces.py",
        "backend_contract": "OpenAI Chat Completions client controlled by OPENAI_BASE_URL",
        "upstream_config_sha256": _sha_bytes(upstream_config),
        "upstream_doctrine_sha256": _sha_bytes(upstream_doctrine),
        "model_rows": MODEL_ROWS,
        "endpoint_checks": endpoint_checks,
        "gemma_startup": gemma,
    }
    _write_json(PACKAGE_ROOT / "backend_preflight.json", backend_preflight)
    _write_json(PACKAGE_ROOT / "candidate_registry.json", {"generated_utc": _utc(), "prompts": registry, "models": MODEL_ROWS})
    source_manifest = {
        "generated_utc": _utc(),
        "package": str(PACKAGE_ROOT),
        "matrix_id": "v021_openai_compat_cross_model_prompt_matrix",
        "upstream_commit": upstream_commit,
        "upstream_config_sha256": _sha_bytes(upstream_config),
        "upstream_doctrine_sha256": _sha_bytes(upstream_doctrine),
        "manifest_checks": manifests,
        "doctrine": doctrine,
        "backend_preflight": str(PACKAGE_ROOT / "backend_preflight.json"),
        "candidate_registry": str(PACKAGE_ROOT / "candidate_registry.json"),
        "runtime_boundary": {
            "code_path": "scratch worktrees from upstream/main",
            "prompt_surface": "detect_objects only",
            "openai_base_url_required": True,
            "source_truth_mutation": False,
            "runtime_adoption": False,
            "commit_push_pr": False,
        },
    }
    _write_json(PACKAGE_ROOT / "source_manifest.json", source_manifest)
    readme = f"""# v021 OpenAI-Compatible Cross-Model Prompt Matrix

Generated: `{source_manifest['generated_utc']}`

This package reruns six detect prompts through the fetched `upstream/main`
OpenAI-compatible runtime path and compares Qwen against Gemma on the same
`human_report_challenge_v2_all_current_117_no101` and office-negative guards.

No prompt, doctrine, source-truth, runtime config, PR, commit, or push is
adopted by this package.
"""
    (PACKAGE_ROOT / "README.md").write_text(readme, encoding="utf-8")
    matrix = _load_matrix()
    matrix["source_manifest"] = str(PACKAGE_ROOT / "source_manifest.json")
    matrix["candidate_registry"] = str(PACKAGE_ROOT / "candidate_registry.json")
    matrix["doctrine_variants"] = doctrine["doctrine_variants"]
    _write_matrix(matrix)
    if any(check["status"] != "available" for check in endpoint_checks.values()):
        _append_recovery(
            {
                "type": "endpoint_preflight_warning",
                "message": "One or more model endpoints are not available after startup preflight.",
                "endpoint_checks": endpoint_checks,
            }
        )
    return 0


def run_row(prompt_id: str, model_id: str, doctrine_variant: str, *, force: bool = False) -> int:
    prompt_sources = _prompt_sources()
    if prompt_id not in prompt_sources:
        raise ValueError(f"unknown prompt id: {prompt_id}")
    if model_id not in MODEL_ROWS:
        raise ValueError(f"unknown model id: {model_id}")
    doctrine = _read_json(PACKAGE_ROOT / "doctrine_diff_report.json") if (PACKAGE_ROOT / "doctrine_diff_report.json").exists() else _doctrine_report()
    if doctrine_variant not in doctrine["doctrine_variants"]:
        raise ValueError(f"{doctrine_variant} not in active doctrine variants {doctrine['doctrine_variants']}")
    matrix = _load_matrix()
    row_id = f"{model_id}__{prompt_id}__{doctrine_variant}"
    if _row_exists(matrix, row_id) and not force:
        print(f"[skip] {row_id} already exists; use --force to rerun", flush=True)
        return 0
    model_row = MODEL_ROWS[model_id]
    endpoint = _check_endpoint(model_row["openai_base_url"], model_row["model"])
    if endpoint["status"] != "available":
        if model_id == "gemma4_e4b":
            endpoint = _start_gemma_if_needed()["endpoint_check"]
        if endpoint["status"] != "available":
            _append_recovery(
                {
                    "type": "endpoint_unavailable",
                    "message": f"Endpoint unavailable for {row_id}",
                    "endpoint": endpoint,
                }
            )
            return 4
    upstream_commit = _git_ref("upstream/main")
    info = prompt_sources[prompt_id]
    prompt = info["prompt"]
    placeholders = _validate_prompt(prompt_id, prompt)
    info = dict(info)
    info["prompt_sha256"] = _sha_text(prompt)
    info["placeholders"] = placeholders
    scratch: Path | None = None
    try:
        scratch = _create_scratch(row_id, upstream_commit)
        _patch_scratch(scratch, prompt, doctrine_variant)
        run_root = PACKAGE_ROOT / "runs" / model_id / prompt_id / doctrine_variant
        office_run = _run_manifest(
            row_id=row_id,
            manifest_path=OFFICE_NEGATIVE_MANIFEST,
            scratch=scratch,
            run_root=run_root / "office_negative",
            model_row=model_row,
        )
        all_run = _run_manifest(
            row_id=row_id,
            manifest_path=ALL_CURRENT_MANIFEST,
            scratch=scratch,
            run_root=run_root / "all_current_no101",
            model_row=model_row,
        )
        if not all_run.get("evaluation_summary") or not office_run.get("evaluation_summary"):
            result = _failed_row_result(
                row_id=row_id,
                prompt_id=prompt_id,
                model_id=model_id,
                doctrine_variant=doctrine_variant,
                prompt_info=info,
                model_row=model_row,
                all_run=all_run,
                office_run=office_run,
                reason="missing evaluation summary after run; see per-pack run summaries",
            )
        else:
            result = _row_result(
                row_id=row_id,
                prompt_id=prompt_id,
                model_id=model_id,
                doctrine_variant=doctrine_variant,
                prompt_info=info,
                model_row=model_row,
                all_run=all_run,
                office_run=office_run,
            )
        result["placeholders"] = placeholders
        matrix = _load_matrix()
        if force:
            matrix["results"] = [row for row in matrix.get("results", []) if row.get("row_id") != row_id]
        matrix.setdefault("results", []).append(result)
        _write_matrix(matrix)
        if result["nonzero_command_count"] or result["missing_outputs"] or result["disqualified"]:
            _append_recovery(
                {
                    "type": "row_completed_with_warning",
                    "message": f"{row_id} completed but is disqualified or has command/output warnings.",
                    "row_id": row_id,
                }
            )
            return 3
        return 0
    finally:
        if scratch is not None:
            cleanup = _remove_scratch(scratch)
            _write_json(PACKAGE_ROOT / "runs" / model_id / prompt_id / doctrine_variant / "scratch_cleanup.json", cleanup)


def run_all(*, force: bool = False) -> int:
    if not (PACKAGE_ROOT / "source_manifest.json").exists():
        init_package()
    doctrine = _read_json(PACKAGE_ROOT / "doctrine_diff_report.json")
    failures: list[dict[str, Any]] = []
    for doctrine_variant in doctrine["doctrine_variants"]:
        for model_id in MODEL_ROWS:
            for prompt_id in _prompt_sources():
                rc = run_row(prompt_id, model_id, doctrine_variant, force=force)
                if rc != 0:
                    failures.append(
                        {
                            "prompt_id": prompt_id,
                            "model_id": model_id,
                            "doctrine_variant": doctrine_variant,
                            "returncode": rc,
                        }
                    )
    if failures:
        _append_recovery({"type": "run_all_failures", "message": "One or more rows returned nonzero.", "failures": failures})
        return 5
    return 0


def summarize() -> int:
    matrix = _load_matrix()
    _write_matrix(matrix)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init")
    sub.add_parser("summarize")
    run_row_parser = sub.add_parser("run-row")
    run_row_parser.add_argument("prompt_id")
    run_row_parser.add_argument("model_id")
    run_row_parser.add_argument("--doctrine", default="shared")
    run_row_parser.add_argument("--force", action="store_true")
    run_all_parser = sub.add_parser("run-all")
    run_all_parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)
    if args.command == "init":
        return init_package()
    if args.command == "summarize":
        return summarize()
    if args.command == "run-row":
        return run_row(args.prompt_id, args.model_id, args.doctrine, force=args.force)
    if args.command == "run-all":
        return run_all(force=args.force)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
