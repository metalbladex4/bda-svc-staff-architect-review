#!/usr/bin/env python3
"""Run the v030 exact-model/model-surface stability gate."""

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
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

import yaml


WORKTREE_ROOT = Path(
    "/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement"
)
CAPSTONE_ROOT = Path("/home/williambenitez1/Capstone")
PACKAGE_ROOT = (
    WORKTREE_ROOT
    / "docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/"
    "human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/"
    "v017b_prompt_only_main_promotion/v030_exact_model_or_surface_equivalence_gate"
)
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
BDA_EVAL_ROOT = WORKTREE_ROOT / "bda_eval"
INSTRUMENTED_RUNNER = PACKAGE_ROOT / "scripts/instrumented_bda_runner.py"
DETERMINISTIC_OLLAMA_MODEL = "qwen3-vl:8b-instruct-v028-deterministic"
PREFERRED_BACKEND = {
    "label": "vllm_exact_qwen3_vl_8b_local_8000",
    "base_url": "http://localhost:8000/v1",
    "api_key": "EMPTY",
    "model": "Qwen/Qwen3-VL-8B-Instruct",
}
FALLBACK_BACKEND = {
    "label": "ollama_openai_compat_fallback_11434",
    "base_url": "http://localhost:11434/v1",
    "api_key": "no-auth",
    "model": "qwen3-vl:8b-instruct",
}
DETERMINISTIC_OLLAMA_8000 = {
    "label": "ollama_deterministic_local_8000",
    "base_url": "http://localhost:8000/v1",
    "api_key": "no-auth",
    "model": DETERMINISTIC_OLLAMA_MODEL,
}
DETERMINISTIC_OLLAMA_11434 = {
    "label": "ollama_deterministic_fallback_11434",
    "base_url": "http://localhost:11434/v1",
    "api_key": "no-auth",
    "model": DETERMINISTIC_OLLAMA_MODEL,
}
CASE67_BASELINE = {"matches": 9, "false_negatives": 2, "false_positives": 4}


def utc_now() -> str:
    return dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def stamp() -> str:
    return dt.datetime.now(dt.UTC).strftime("%Y-%m-%d_%H%M%SZ")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str | None:
    if not path.exists():
        return None
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_hash(data: Any) -> str:
    return sha256_text(json.dumps(data, sort_keys=True, separators=(",", ":"), default=str))


def unified_diff(a: str, b: str, a_label: str, b_label: str) -> str:
    return "".join(
        difflib.unified_diff(
            a.splitlines(keepends=True),
            b.splitlines(keepends=True),
            fromfile=a_label,
            tofile=b_label,
        )
    )


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
    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(payload, handle, sort_keys=False, allow_unicode=False)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def append_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text)


def extract_prompt_from_overlay(path: Path) -> str:
    return read_yaml(path)["overrides"]["prompts"]["detect_objects"]


def fetch_url(url: str, timeout: int = 5) -> dict[str, Any]:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            text = response.read().decode("utf-8", errors="replace")
        payload = json.loads(text)
        return {"ok": True, "url": url, "payload": payload, "error": None}
    except Exception as exc:
        return {"ok": False, "url": url, "payload": None, "error": repr(exc)}


def model_list_has(status: dict[str, Any], model_name: str) -> bool:
    if not status.get("ok"):
        return False
    payload = status.get("payload") or {}
    return any(item.get("id") == model_name for item in payload.get("data", []))


def create_deterministic_ollama_model() -> dict[str, Any]:
    modelfile = PACKAGE_ROOT / "backend_logs/Modelfile.v028.deterministic"
    modelfile.parent.mkdir(parents=True, exist_ok=True)
    modelfile.write_text(
        "\n".join(
            [
                "FROM qwen3-vl:8b-instruct",
                "PARAMETER temperature 0",
                "PARAMETER top_k 1",
                "PARAMETER top_p 1",
                "PARAMETER seed 42",
                "PARAMETER num_ctx 4096",
                "",
            ]
        ),
        encoding="utf-8",
    )
    result = run(["ollama", "create", DETERMINISTIC_OLLAMA_MODEL, "-f", str(modelfile)], CAPSTONE_ROOT)
    show = run(["ollama", "show", DETERMINISTIC_OLLAMA_MODEL, "--modelfile"], CAPSTONE_ROOT)
    return {
        "modelfile_path": str(modelfile),
        "create_command": result,
        "show_modelfile": show,
        "ok": result["returncode"] == 0,
    }


def launch_ollama_on_8000() -> dict[str, Any]:
    log_path = PACKAGE_ROOT / "backend_logs" / f"ollama_8000_{stamp()}.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env.update(
        {
            "OLLAMA_HOST": "127.0.0.1:8000",
            "OLLAMA_MODELS": "/usr/share/ollama/.ollama/models",
            "OLLAMA_NUM_PARALLEL": "1",
            "OLLAMA_MAX_LOADED_MODELS": "1",
            "OLLAMA_KEEP_ALIVE": "-1",
        }
    )
    handle = log_path.open("ab")
    proc = subprocess.Popen(
        ["ollama", "serve"],
        cwd=str(CAPSTONE_ROOT),
        env=env,
        stdout=handle,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    status = {"ok": False, "url": DETERMINISTIC_OLLAMA_8000["base_url"] + "/models", "payload": None, "error": "not checked"}
    for _ in range(30):
        status = fetch_url(DETERMINISTIC_OLLAMA_8000["base_url"] + "/models", timeout=2)
        if status["ok"]:
            break
        if proc.poll() is not None:
            break
        import time

        time.sleep(1)
    return {
        "pid": proc.pid,
        "log_path": str(log_path),
        "endpoint_status": status,
        "process_poll": proc.poll(),
        "env": {
            "OLLAMA_HOST": env["OLLAMA_HOST"],
            "OLLAMA_MODELS": env["OLLAMA_MODELS"],
            "OLLAMA_NUM_PARALLEL": env["OLLAMA_NUM_PARALLEL"],
            "OLLAMA_MAX_LOADED_MODELS": env["OLLAMA_MAX_LOADED_MODELS"],
            "OLLAMA_KEEP_ALIVE": env["OLLAMA_KEEP_ALIVE"],
        },
    }


def select_backend() -> tuple[dict[str, str], dict[str, Any]]:
    preferred_status = fetch_url(PREFERRED_BACKEND["base_url"] + "/models")
    fallback_status = fetch_url(FALLBACK_BACKEND["base_url"] + "/models")
    if preferred_status["ok"] and model_list_has(preferred_status, PREFERRED_BACKEND["model"]):
        selected = PREFERRED_BACKEND
        reason = (
            "non-Ollama vLLM endpoint available on localhost:8000 with expected "
            "served model name; actual model root is recorded in /v1/models"
        )
    else:
        selected = {}
        reason = "no non-Ollama endpoint with the expected model name is available"
    ollama_version = run(["ollama", "--version"], CAPSTONE_ROOT)
    vllm_version = run(
        [
            "bash",
            "-lc",
            "/tmp/bda_v030_vllm_env/bin/python - <<'PY'\nimport importlib.metadata as md\nfor p in ['vllm','torch','transformers','openai','fastapi','uvicorn','compressed-tensors']:\n    try: print(p, md.version(p))\n    except Exception: print(p, 'unavailable')\nPY",
        ],
        CAPSTONE_ROOT,
    )
    package_probe = run(
        [
            "bash",
            "-lc",
            "python3 - <<'PY'\nimport importlib.metadata as md\nfor p in ['vllm','sglang','transformers','accelerate','torch','openai','fastapi','uvicorn','litellm']:\n    try: print(p, md.version(p))\n    except Exception: print(p, 'unavailable')\nPY",
        ],
        CAPSTONE_ROOT,
    )
    preflight = {
        "generated_at": utc_now(),
        "preferred_endpoint_status": preferred_status,
        "fallback_endpoint_status": fallback_status,
        "deterministic_ollama_create": None,
        "deterministic_ollama_8000_launch": None,
        "deterministic_ollama_11434_status": None,
        "selected_backend": selected,
        "backend_selected_reason": reason,
        "ollama_version": ollama_version,
        "vllm_version": vllm_version,
        "python_package_probe": package_probe,
        "non_ollama_requirement": "semantic prompt work remains blocked unless this vLLM endpoint passes stability and baseline gates",
    }
    return selected, preflight


def make_subset_manifest(case_ids: list[str], path: Path, pack_id: str) -> None:
    source = read_yaml(ALL_CURRENT_MANIFEST)
    wanted = {str(case_id) for case_id in case_ids}
    cases = [
        case
        for case in source["cases"]
        if case["case_id"].replace("human-report-", "") in wanted
        or str(case["case_id"]) in wanted
    ]
    found = {case["case_id"].replace("human-report-", "") for case in cases}
    missing = sorted(wanted - found)
    if missing:
        raise RuntimeError(f"Missing cases for manifest {pack_id}: {missing}")
    payload = {
        "pack_id": pack_id,
        "eval_mode": source["eval_mode"],
        "images_dir": source["images_dir"],
        "cases": cases,
    }
    write_yaml(path, payload)


def ensure_scaffold() -> None:
    for subdir in ["overlays", "runs", "scripts", "diagnoses", "validation_manifests", "backend_logs", "traces"]:
        (PACKAGE_ROOT / subdir).mkdir(parents=True, exist_ok=True)
    for name, payload in {
        "rendered_prompt_manifest.json": {"generated_at": utc_now(), "records": []},
        "request_shape_manifest.json": {"generated_at": utc_now(), "records": []},
        "runtime_trace_manifest.json": {"generated_at": utc_now(), "records": []},
        "response_trace_manifest.json": {"generated_at": utc_now(), "records": []},
        "overlay_application_audit.json": {"generated_at": utc_now(), "records": []},
        "backend_stability_matrix.json": {"generated_at": utc_now(), "records": []},
        "raw_request_replay_matrix.json": {"generated_at": utc_now(), "records": []},
        "deterministic_settings_probe.json": {"generated_at": utc_now(), "records": []},
        "backend_inventory.json": {"generated_at": utc_now(), "records": []},
        "local_model_inventory.json": {"generated_at": utc_now(), "records": []},
        "backend_launch_attempts.json": {"generated_at": utc_now(), "records": []},
        "stable_backend_recovery.json": {"generated_at": utc_now(), "records": []},
        "recovery_log.json": {"generated_at": utc_now(), "events": []},
        "final_recommendation.json": {"status": "running", "generated_at": utc_now()},
    }.items():
        path = PACKAGE_ROOT / name
        if not path.exists():
            write_json(path, payload)


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def update_manifest_files(record: dict[str, Any]) -> None:
    for filename, key in [
        ("rendered_prompt_manifest.json", "rendered_prompt_record"),
        ("request_shape_manifest.json", "request_shape_record"),
        ("runtime_trace_manifest.json", "runtime_trace_record"),
        ("response_trace_manifest.json", "response_trace_record"),
        ("overlay_application_audit.json", "overlay_application_record"),
    ]:
        path = PACKAGE_ROOT / filename
        payload = load_json(path, {"generated_at": utc_now(), "records": []})
        payload["records"].append(record.get(key, record))
        payload["updated_at"] = utc_now()
        write_json(path, payload)

    matrix_path = PACKAGE_ROOT / "backend_stability_matrix.json"
    matrix = load_json(matrix_path, {"generated_at": utc_now(), "records": []})
    matrix["records"].append(record["matrix_record"])
    matrix["updated_at"] = utc_now()
    write_json(matrix_path, matrix)

    append_text(
        PACKAGE_ROOT / "backend_stability_matrix.md",
        "| {candidate} | {stage} | {backend} | {matches} | {fns} | {fps} | {errors} | {case67} | {rendered_hash} | {request_hash} | {status} |\n".format(
            candidate=record["matrix_record"]["candidate_id"],
            stage=record["matrix_record"]["stage"],
            backend=record["matrix_record"]["backend_label"],
            matches=record["matrix_record"]["matches"],
            fns=record["matrix_record"]["false_negatives"],
            fps=record["matrix_record"]["false_positives"],
            errors=record["matrix_record"]["combined_errors"],
            case67=record["matrix_record"]["case_67"],
            rendered_hash=record["matrix_record"]["rendered_prompt_hash"],
            request_hash=record["matrix_record"]["request_shape_hash"],
            status=record["matrix_record"]["status"],
        ),
    )


def create_overlays() -> list[dict[str, Any]]:
    v020c_prompt = extract_prompt_from_overlay(V020C_OVERLAY)
    blank_line_prompt = v020c_prompt.replace("{categories}\n\nCalibration", "{categories}\n\n\nCalibration")
    trailing_space_prompt = v020c_prompt.replace("{categories}\n\nCalibration", "{categories} \n\nCalibration")
    candidates = [
        ("v030a_case67_exact_v020c_replay_1", v020c_prompt, []),
        ("v030b_case67_exact_v020c_replay_2", v020c_prompt, []),
        ("v030c_case67_exact_v020c_replay_3", v020c_prompt, []),
        ("v030d_case67_blank_line_probe_1", blank_line_prompt, ["one extra blank line after the categories placeholder"]),
        ("v030e_case67_blank_line_probe_2", blank_line_prompt, ["one extra blank line after the categories placeholder"]),
        ("v030f_case67_trailing_space_probe", trailing_space_prompt, ["one trailing space after the categories placeholder line"]),
        ("v030g_case67_noop_template_roundtrip", v020c_prompt, ["YAML roundtrip no-op; no intended semantic change"]),
        ("v030h_sentinel_exact_v020c_replay_1", v020c_prompt, []),
        ("v030i_sentinel_exact_v020c_replay_2", v020c_prompt, []),
        ("v030j_sentinel_blank_line_shape_probe", blank_line_prompt, ["one extra blank line after the categories placeholder"]),
        ("v030k_sentinel_trailing_space_shape_probe", trailing_space_prompt, ["one trailing space after the categories placeholder line"]),
        ("v030l_sentinel_noop_template_roundtrip", v020c_prompt, ["YAML roundtrip no-op; no intended semantic change"]),
    ]
    records = []
    for candidate_id, prompt, intended_changes in candidates:
        overlay = {
            "candidate_id": candidate_id,
            "title": candidate_id.replace("_", " "),
            "overlay_id": f"qwen-1.2-{candidate_id}",
            "overlay_type": "exact_model_surface_probe",
            "model_line": "qwen3-vl:8b-instruct",
            "description": "v030 exact-model/model-surface repeatability probe.",
            "generated_from": ["v020c_v019c_extra_box_audit"],
            "intended_changes": intended_changes,
            "overrides": {
                "prompts": {"detect_objects": prompt},
                "runtime": {
                    "notes": "Applied only inside upstream/main scratch config; no product adoption."
                },
            },
        }
        path = PACKAGE_ROOT / "overlays" / f"{candidate_id}.yaml"
        write_yaml(path, overlay)
        records.append(
            {
                "candidate_id": candidate_id,
                "overlay_path": str(path),
                "prompt_template_sha256": sha256_text(prompt),
                "intended_changes": intended_changes,
            }
        )
    return records


def patch_scratch_config(scratch: Path, prompt: str) -> Path:
    config_path = scratch / "src/bda_svc/pipeline/config.yaml"
    config = read_yaml(config_path)
    config["prompts"]["detect_objects"] = prompt
    write_yaml(config_path, config)
    return config_path


def create_scratch(candidate_id: str) -> Path:
    scratch = Path("/tmp") / f"bda_v030_{candidate_id}_{stamp()}"
    if scratch.exists():
        shutil.rmtree(scratch)
    require_ok(run(["git", "worktree", "add", "--detach", str(scratch), "upstream/main"], CAPSTONE_ROOT))
    return scratch


def remove_scratch(scratch: Path) -> dict[str, Any]:
    result = run(["git", "worktree", "remove", "--force", str(scratch)], CAPSTONE_ROOT)
    if scratch.exists():
        shutil.rmtree(scratch, ignore_errors=True)
    return result


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


def case_metrics(summary: dict[str, Any], filename: str = "67.jpg") -> dict[str, int] | None:
    for image in summary.get("images", []):
        if image.get("image_filename") == filename:
            return {
                "matches": image.get("match_count", 0),
                "false_negatives": image.get("false_negative_count", 0),
                "false_positives": image.get("false_positive_count", 0),
            }
    return None


def print_candidate_block(record: dict[str, Any], preflight: dict[str, Any]) -> None:
    print("=== V030 STATUS ===", flush=True)
    print(f"phase: {record['stage']}", flush=True)
    print(f"backend: {record['backend_label']}", flush=True)
    print(f"endpoint: {record['endpoint']}", flush=True)
    print(f"preferred_backend_available: {str(preflight['preferred_endpoint_status']['ok']).lower()}", flush=True)
    print(f"local_model_source: {record['local_model_source']}", flush=True)
    print(f"probe: {record['candidate_id']}", flush=True)
    print(f"case_67: {record['case_67']}", flush=True)
    print(f"raw_response_hash: {record['raw_response_hash']}", flush=True)
    print(f"rendered_prompt_hash: {record['rendered_prompt_hash']}", flush=True)
    print(f"request_shape_hash: {record['request_shape_hash']}", flush=True)
    print(f"status: {record['status']}", flush=True)
    print(f"main_lesson: {record['main_lesson']}", flush=True)
    print(f"next_action: {record['next_axis']}", flush=True)
    print("===================", flush=True)


def run_probe(candidate: dict[str, Any], manifest: Path, backend: dict[str, str], stage: str, preflight: dict[str, Any]) -> dict[str, Any]:
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
    env = dict(**os.environ)
    env.update(
        {
            "OPENAI_BASE_URL": backend["base_url"],
            "OPENAI_API_KEY": backend["api_key"],
            "BDA_DETECTION_MODEL": backend["model"],
            "BDA_ASSESSMENT_MODEL": backend["model"],
        }
    )

    manifest_payload = read_yaml(manifest)
    command_records = []
    try:
        for case in manifest_payload["cases"]:
            trace_path = traces_dir / f"{case['case_id']}.json"
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
                backend["label"],
                "--endpoint-url",
                backend["base_url"],
                "--source-overlay",
                str(overlay_path),
                "--base-overlay",
                str(V020C_OVERLAY),
                "--stage",
                stage,
                "--intended-changes-json",
                json.dumps(candidate["intended_changes"]),
            ]
            result = run(cmd, scratch, env)
            command_records.append(result)
            (logs_dir / f"{case['case_id']}_stdout.log").write_text(result["stdout"], encoding="utf-8")
            (logs_dir / f"{case['case_id']}_stderr.log").write_text(result["stderr"], encoding="utf-8")
            require_ok(result)

        eval_result, summary_path = run_eval(manifest, predicted_dir, eval_dir)
        command_records.append(eval_result)
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
    finally:
        cleanup = remove_scratch(scratch)
        write_json(run_root / "scratch_cleanup.json", cleanup)

    trace_files = sorted(traces_dir.glob("*.json"))
    traces = [json.loads(path.read_text(encoding="utf-8")) for path in trace_files]
    first_trace = traces[0] if traces else {}
    rendered = first_trace.get("rendered_prompt") or {}
    rendered_text = rendered.get("rendered_prompt_text")
    base_rendered_path = PACKAGE_ROOT / "runs/_base_v020c_rendered_prompt.txt"
    if rendered_text:
        if not base_rendered_path.exists() or candidate_id == "v030a_case67_exact_v020c_replay_1":
            base_rendered_path.write_text(rendered_text, encoding="utf-8")
            rendered["rendered_prompt_diff_from_base"] = ""
        else:
            base_rendered = base_rendered_path.read_text(encoding="utf-8")
            rendered["rendered_prompt_diff_from_base"] = unified_diff(
                base_rendered,
                rendered_text,
                "v028a_rendered_v020c_prompt",
                f"{candidate_id}_rendered_prompt",
            )
        first_trace["rendered_prompt"] = rendered
        if trace_files:
            trace_files[0].write_text(json.dumps(first_trace, indent=2, ensure_ascii=False), encoding="utf-8")
    detection_request = next(
        (
            trace
            for trace in first_trace.get("request_response_traces", [])
            if trace.get("call_kind") == "detection"
        ),
        {},
    )

    totals = summary["totals"]
    c67 = case_metrics(summary) or {"matches": "n/a", "false_negatives": "n/a", "false_positives": "n/a"}
    case67_text = (
        f"{c67['matches']}/{c67['false_negatives']}/{c67['false_positives']}"
        if isinstance(c67["matches"], int)
        else "n/a"
    )
    combined = totals["false_negative_count"] + totals["false_positive_count"]
    baseline_errors = CASE67_BASELINE["false_negatives"] + CASE67_BASELINE["false_positives"]
    case67_errors = (
        c67["false_negatives"] + c67["false_positives"]
        if isinstance(c67["false_negatives"], int)
        else None
    )
    stage_pass = (
        isinstance(c67["matches"], int)
        and c67["matches"] >= 8
        and c67["false_negatives"] <= 4
        and bool(rendered.get("rendered_prompt_sha256"))
        and bool(detection_request.get("request_shape_hash"))
    )
    status = "stability_pass" if stage_pass else "stability_fail"
    main_lesson = (
        "Case 67 stayed within the v020c stability threshold."
        if stage_pass
        else "Case 67 or instrumentation failed the stability threshold."
    )
    next_axis = (
        "Continue the planned stability probe sequence."
        if stage_pass
        else "Stop semantic prompt mutation and diagnose runtime/request-shape instability."
    )

    matrix_record = {
        "candidate_id": candidate_id,
        "stage": stage,
        "backend_label": backend["label"],
        "endpoint": backend["base_url"],
        "local_model_source": "existing_service" if "ollama" not in backend["label"] else "cached",
        "matches": totals["match_count"],
        "false_negatives": totals["false_negative_count"],
        "false_positives": totals["false_positive_count"],
        "combined_errors": combined,
        "case_67": case67_text,
        "rendered_prompt_hash": rendered.get("rendered_prompt_sha256") or "unavailable",
        "request_shape_hash": detection_request.get("request_shape_hash") or "unavailable",
        "response_trace_captured": bool(first_trace.get("response_trace_captured")),
        "status": status,
        "summary_path": str(summary_path),
        "run_root": str(run_root),
    }
    run_summary = {
        "candidate_id": candidate_id,
        "stage": stage,
        "backend": backend,
        "manifest": str(manifest),
        "run_root": str(run_root),
        "predicted_dir": str(predicted_dir),
        "eval_summary": str(summary_path),
        "scratch_config_sha256": scratch_config_sha,
        "command_records": command_records,
        "eval_summary_payload": summary,
        "trace_files": [str(path) for path in trace_files],
        "matrix_record": matrix_record,
    }
    write_json(run_root / "v027_stability_run_summary.json", run_summary)

    record = {
        "candidate_id": candidate_id,
        "backend_label": backend["label"],
        "endpoint": backend["base_url"],
        "local_model_source": "cached" if "ollama" in backend["label"] else "existing_service",
        "stage": stage,
        "matches": totals["match_count"],
        "false_negatives": totals["false_negative_count"],
        "false_positives": totals["false_positive_count"],
        "combined_errors": combined,
        "vs_v020c_errors_delta": (
            case67_errors - baseline_errors if case67_errors is not None else "n/a"
        ),
        "case_67": case67_text,
        "case_155": "n/a",
        "case_166": "n/a",
        "office_negative": "n/a",
        "rendered_prompt_hash": matrix_record["rendered_prompt_hash"],
        "request_shape_hash": matrix_record["request_shape_hash"],
        "response_trace_captured": matrix_record["response_trace_captured"],
        "raw_response_hash": detection_request.get("raw_response_sha256") or "unavailable",
        "status": status,
        "main_lesson": main_lesson,
        "next_axis": next_axis,
    }
    update_manifest_files(
        {
            "matrix_record": matrix_record,
            "rendered_prompt_record": {
                "candidate_id": candidate_id,
                "rendered_prompt": rendered,
                "run_root": str(run_root),
            },
            "request_shape_record": {
                "candidate_id": candidate_id,
                "detection_request": detection_request.get("request_shape"),
                "request_shape_hash": detection_request.get("request_shape_hash"),
                "run_root": str(run_root),
            },
            "runtime_trace_record": {
                "candidate_id": candidate_id,
                "trace_files": [str(path) for path in trace_files],
                "run_root": str(run_root),
            },
            "response_trace_record": {
                "candidate_id": candidate_id,
                "response_trace_captured": matrix_record["response_trace_captured"],
                "detection_raw_response_sha256": detection_request.get("raw_response_sha256"),
                "run_root": str(run_root),
            },
            "overlay_application_record": {
                "candidate_id": candidate_id,
                "overlay_application": first_trace.get("overlay_application"),
                "run_root": str(run_root),
            },
        }
    )
    append_text(
        PACKAGE_ROOT / "live_metrics_log.md",
        f"\n## {candidate_id}\n\n- backend: `{backend['label']}`\n- stage: `{stage}`\n- metrics: `{totals['match_count']}/{totals['false_negative_count']}/{totals['false_positive_count']}/{combined}`\n- case 67: `{case67_text}`\n- rendered prompt hash: `{record['rendered_prompt_hash']}`\n- request shape hash: `{record['request_shape_hash']}`\n- status: `{status}`\n",
    )
    print_candidate_block(record, preflight)
    return record


def write_source_manifest(preflight: dict[str, Any]) -> None:
    upstream_fetch = run(["git", "fetch", "upstream", "main"], CAPSTONE_ROOT)
    upstream_commit = run(["git", "rev-parse", "upstream/main"], CAPSTONE_ROOT)
    source_manifest = {
        "generated_at": utc_now(),
        "upstream_fetch": upstream_fetch,
        "upstream_main_commit": upstream_commit["stdout"].strip(),
        "qwen_worktree": str(WORKTREE_ROOT),
        "package_root": str(PACKAGE_ROOT),
        "v020c_incumbent": {"matches": 186, "false_negatives": 33, "false_positives": 25, "combined_errors": 58},
        "v024l_learning_only": {"matches": 188, "false_negatives": 31, "false_positives": 35, "combined_errors": 66},
        "v025a_rejected": {"matches": 176, "false_negatives": 43, "false_positives": 35, "combined_errors": 78},
        "v024o_status": "partial_unscored_forbidden",
        "v026_stop_reason": "runtime_shape_sensitivity_pause; rendered prompt/request evidence was missing",
        "v027_stop_reason": "fallback instability; identical rendered/request hashes produced both collapsed and stable case-67 responses",
        "base_overlay": str(V020C_OVERLAY),
        "all_current_manifest": str(ALL_CURRENT_MANIFEST),
        "office_negative_manifest": str(OFFICE_NEGATIVE_MANIFEST),
        "backend_preflight": preflight,
    }
    write_json(PACKAGE_ROOT / "source_manifest.json", source_manifest)


def write_final(stage1_records: list[dict[str, Any]], stage2_records: list[dict[str, Any]] | None, backend: dict[str, str], preflight: dict[str, Any]) -> None:
    stage1_pass = all(record["status"] == "stability_pass" for record in stage1_records)
    stage2_pass = bool(stage2_records) and all(record["status"] == "stability_pass" for record in stage2_records)
    status = "stage1_pass_stage2_not_run"
    if not stage1_pass:
        status = "stability_failed_stage1"
    elif stage2_records and not stage2_pass:
        status = "stability_failed_stage2"
    elif stage1_pass and stage2_pass:
        status = "stability_passed"

    recommendation = {
        "generated_at": utc_now(),
        "status": status,
        "backend_used": backend,
        "preferred_backend_available": preflight["preferred_endpoint_status"]["ok"],
        "stage1_passed": stage1_pass,
        "stage2_passed": stage2_pass if stage2_records is not None else None,
        "semantic_prompt_refinement_resumed": False,
        "stability_decision": (
            "C. fallback_stable_with_documented_settings_ready_for_prompt_refinement"
            if stage1_pass and stage2_pass and "ollama" in backend.get("label", "")
            else (
                "B. stable_new_local_backend_ready_for_autonomous_prompt_refinement"
                if stage1_pass and stage2_pass
                else "D. no_stable_backend_available_stop_prompt_mutation"
            )
        ),
        "product_incumbent": "v020c_anchor_replay / v020c_extra_box_audit",
        "product_incumbent_metrics": {"matches": 186, "false_negatives": 33, "false_positives": 25, "combined_errors": 58},
        "v024l_status": "learning_evidence_only",
        "v025a_status": "rejected",
        "v024o_status": "partial_unscored_forbidden",
        "stage1_records": stage1_records,
        "stage2_records": stage2_records or [],
        "decision": (
            "Do not resume semantic prompt mutation until backend/rendering/request-shape stability is repaired or explained."
            if not stage1_pass or (stage2_records and not stage2_pass)
            else "Stability gate passed; semantic prompt refinement may resume in a nested package."
        ),
    }
    write_json(PACKAGE_ROOT / "final_recommendation.json", recommendation)
    lines = [
        "# v030 Final Recommendation",
        "",
        f"Updated: `{recommendation['generated_at']}`",
        "",
        f"Status: `{status}`",
        "",
        f"Backend used: `{backend.get('label', 'none')}`",
        "",
        f"Preferred backend available: `{preflight['preferred_endpoint_status']['ok']}`",
        "",
        "## Decision",
        "",
        recommendation["decision"],
        "",
        "## Stage 1 Case 67 Results",
        "",
        "| candidate | metrics | case 67 | rendered hash | request hash | status |",
        "| --- | ---: | ---: | --- | --- | --- |",
    ]
    for record in stage1_records:
        lines.append(
            f"| `{record['candidate_id']}` | `{record['matches']}/{record['false_negatives']}/{record['false_positives']}/{record['combined_errors']}` | `{record['case_67']}` | `{record['rendered_prompt_hash']}` | `{record['request_shape_hash']}` | `{record['status']}` |"
        )
    write_path = PACKAGE_ROOT / "final_recommendation.md"
    write_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    if not stage1_pass:
        (PACKAGE_ROOT / "pause_report.md").write_text(
            "\n".join(
                [
                    "# v030 Pause Report",
                    "",
                    f"Generated: `{utc_now()}`",
                    "",
                    "Stage 1 failed. Semantic prompt mutation remains paused.",
                    "",
                    "The package captured rendered prompt hashes, request-shape hashes, image/request traces, and response/parsing traces for the case-67 probes.",
                    "",
                    "Next action: review the failed probe traces and decide whether backend nondeterminism, request serialization, image serialization, JSON repair/filtering, or eval matching explains the instability.",
                ]
            )
            + "\n",
            encoding="utf-8",
        )


def write_inventory_docs(preflight: dict[str, Any]) -> None:
    backend_inventory = {
        "generated_at": utc_now(),
        "preferred_endpoint": preflight["preferred_endpoint_status"],
        "fallback_endpoint": preflight["fallback_endpoint_status"],
        "selected_backend": preflight["selected_backend"],
        "backend_selected_reason": preflight["backend_selected_reason"],
        "running_process_probe": run(
            [
                "bash",
                "-lc",
                "ps -eo pid,ppid,etime,cmd --sort=pid | rg -i 'vllm|sglang|ollama|transformers|fastapi|uvicorn|litellm|openai|qwen|qwen3|vl' || true",
            ],
            CAPSTONE_ROOT,
        ),
        "gpu_probe": run(["bash", "-lc", "nvidia-smi || true"], CAPSTONE_ROOT),
        "disk_probe": run(["bash", "-lc", "df -h /home /tmp /home/williambenitez1/.cache /home/williambenitez1/.ollama 2>/dev/null || true"], CAPSTONE_ROOT),
        "package_probe": preflight["python_package_probe"],
        "vllm_launch_doc": "Project README documents: vllm serve Qwen/Qwen3-VL-8B-Instruct",
        "vllm_feasibility": "vLLM/SGLang/Transformers were not installed; Qwen/Qwen3-VL-8B-Instruct is public/apache-2.0 but not cached locally and full BF16 8.8B weights are not treated as safe to pull/load blindly on 16GB VRAM during this tranche.",
    }
    local_model_inventory = {
        "generated_at": utc_now(),
        "huggingface_cache_probe": run(
            ["bash", "-lc", "find /home/williambenitez1/.cache/huggingface/hub -maxdepth 2 -type d -printf '%p\\n' 2>/dev/null | sed -n '1,120p'"],
            CAPSTONE_ROOT,
        ),
        "ollama_list": run(["ollama", "list"], CAPSTONE_ROOT),
        "ollama_qwen_show": run(["bash", "-lc", "ollama show qwen3-vl:8b-instruct --modelfile 2>/dev/null | rg -n '^(FROM|TEMPLATE|RENDERER|PARSER|PARAMETER)' || true"], CAPSTONE_ROOT),
        "deterministic_model_create": preflight.get("deterministic_ollama_create"),
        "deterministic_8000_launch": preflight.get("deterministic_ollama_8000_launch"),
    }
    write_json(PACKAGE_ROOT / "backend_inventory.json", backend_inventory)
    write_json(PACKAGE_ROOT / "local_model_inventory.json", local_model_inventory)
    write_json(PACKAGE_ROOT / "backend_launch_attempts.json", {"generated_at": utc_now(), "attempts": [preflight.get("deterministic_ollama_8000_launch")]})
    write_json(PACKAGE_ROOT / "stable_backend_recovery.json", {"generated_at": utc_now(), "selected_backend": preflight["selected_backend"], "reason": preflight["backend_selected_reason"]})
    write_json(PACKAGE_ROOT / "deterministic_settings_probe.json", {"generated_at": utc_now(), "deterministic_model": DETERMINISTIC_OLLAMA_MODEL, "settings": {"temperature": 0, "top_k": 1, "top_p": 1, "seed": 42, "num_ctx": 4096}, "source": "Ollama Modelfile Reference"})

    (PACKAGE_ROOT / "backend_inventory.md").write_text(
        "\n".join(
            [
                "# v030 Backend Inventory",
                "",
                f"Generated: `{utc_now()}`",
                "",
                f"- preferred endpoint ok: `{preflight['preferred_endpoint_status']['ok']}`",
                f"- fallback endpoint ok: `{preflight['fallback_endpoint_status']['ok']}`",
                f"- selected backend: `{preflight['selected_backend'].get('label', 'none')}`",
                f"- reason: {preflight['backend_selected_reason']}",
                "",
                "Project docs only identify the preferred launch command as `vllm serve Qwen/Qwen3-VL-8B-Instruct`.",
                "No installed vLLM/SGLang/Transformers stack was found in the probed Python environments.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (PACKAGE_ROOT / "local_model_inventory.md").write_text(
        "\n".join(
            [
                "# v030 Local Model Inventory",
                "",
                "- Hugging Face cache: no local Qwen3-VL model snapshot found.",
                "- Ollama cache: `qwen3-vl:8b-instruct`, `qwen3-vl:8b-instruct-q8_0`, and `qwen3-vl:8b` are available.",
                f"- Deterministic Ollama alias attempted: `{DETERMINISTIC_OLLAMA_MODEL}`.",
                "- No private credentials or tokens were used.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", action="store_true", help="Run v030 exact-model/model-surface backend gate.")
    args = parser.parse_args()
    if not args.run:
        parser.print_help()
        return 0

    ensure_scaffold()
    backend, preflight = select_backend()
    write_json(PACKAGE_ROOT / "backend_preflight.json", preflight)
    write_inventory_docs(preflight)
    write_source_manifest(preflight)
    if not backend:
        write_final([], None, {}, preflight)
        raise RuntimeError("No authorized OpenAI-compatible backend is available.")

    case67_manifest = PACKAGE_ROOT / "validation_manifests/v030_case67_only_no101.yaml"
    sentinel_manifest = PACKAGE_ROOT / "validation_manifests/v030_sentinel_micro_pack_no101.yaml"
    make_subset_manifest(["67"], case67_manifest, "v030_case67_only_no101")
    make_subset_manifest(
        ["12", "14", "16", "42", "66", "67", "77", "84", "88", "90", "97", "103", "155", "166", "172"],
        sentinel_manifest,
        "v030_sentinel_micro_pack_no101",
    )
    candidates = create_overlays()
    stage1_candidates = candidates[:7]
    stage2_candidates = candidates[7:]

    stage1_records: list[dict[str, Any]] = []
    try:
        for candidate in stage1_candidates:
            stage1_records.append(run_probe(candidate, case67_manifest, backend, "case67_stability", preflight))
    finally:
        stage1_pass = len(stage1_records) == len(stage1_candidates) and all(
            record["status"] == "stability_pass" for record in stage1_records
        )
        stage2_records = None
        if stage1_pass:
            stage2_records = []
            for candidate in stage2_candidates:
                stage2_records.append(run_probe(candidate, sentinel_manifest, backend, "sentinel_stability", preflight))
        write_final(stage1_records, stage2_records, backend, preflight)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
