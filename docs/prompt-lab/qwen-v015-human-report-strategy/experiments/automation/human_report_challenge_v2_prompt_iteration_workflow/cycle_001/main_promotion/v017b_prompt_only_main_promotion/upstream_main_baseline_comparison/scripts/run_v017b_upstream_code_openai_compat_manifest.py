#!/usr/bin/env python3
"""Run upstream/main bda-svc code against a v2 manifest and score the outputs."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
from pathlib import Path
from typing import Any

import yaml


def _read_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle) or {}
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected YAML mapping.")
    return payload


def _resolve(raw: str | Path, base: Path) -> Path:
    path = Path(raw)
    if not path.is_absolute():
        path = (base / path).resolve()
    return path


def _manifest_images(manifest_path: Path) -> list[Path]:
    payload = _read_yaml(manifest_path)
    cases = payload.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError(f"{manifest_path}: missing cases.")

    images: list[Path] = []
    for case in cases:
        if not isinstance(case, dict):
            raise ValueError(f"{manifest_path}: case must be a mapping.")
        image_path = case.get("image_path")
        if not isinstance(image_path, str) or not image_path.strip():
            raise ValueError(f"{manifest_path}: case missing image_path.")
        images.append(_resolve(image_path, manifest_path.parent))
    return images


def _run_command(cmd: list[str], *, cwd: Path, env: dict[str, str]) -> dict[str, Any]:
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
        "stdout_tail": completed.stdout[-4000:],
        "stderr_tail": completed.stderr[-4000:],
    }


def _latest_summary(eval_dir: Path) -> Path | None:
    summaries = sorted(eval_dir.glob("evaluation_*_summary.json"))
    return summaries[-1] if summaries else None


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected JSON object.")
    return payload


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--upstream-worktree", type=Path, required=True)
    parser.add_argument("--eval-worktree", type=Path, required=True)
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--label", required=True)
    parser.add_argument("--openai-base-url", required=True)
    parser.add_argument("--openai-api-key", default="no-auth")
    parser.add_argument("--model", default="qwen3-vl:8b-instruct")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    manifest_path = args.manifest.resolve()
    upstream_worktree = args.upstream_worktree.resolve()
    eval_worktree = args.eval_worktree.resolve()
    timestamp = dt.datetime.now(dt.UTC).strftime("%Y-%m-%d_%H%M%SZ")
    output_root = args.run_root.resolve() / f"{manifest_path.stem}_{timestamp}"
    predicted_dir = output_root / "predicted"
    eval_dir = output_root / "eval"
    predicted_dir.mkdir(parents=True, exist_ok=True)
    eval_dir.mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    env.update(
        {
            "OPENAI_BASE_URL": args.openai_base_url,
            "OPENAI_API_KEY": args.openai_api_key,
            "BDA_DETECTION_MODEL": args.model,
            "BDA_ASSESSMENT_MODEL": args.model,
        }
    )

    commands: list[dict[str, Any]] = []
    missing_outputs: list[str] = []

    for image_path in _manifest_images(manifest_path):
        cmd = [
            "uv",
            "run",
            "bda-svc",
            "-i",
            str(image_path),
            "-o",
            str(predicted_dir),
        ]
        before = set(predicted_dir.glob(f"{image_path.stem}_*.json"))
        entry = _run_command(cmd, cwd=upstream_worktree, env=env)
        commands.append(entry)
        after = set(predicted_dir.glob(f"{image_path.stem}_*.json"))
        if entry["returncode"] != 0:
            break
        if not (after - before):
            missing_outputs.append(image_path.name)
            break

    if (
        commands
        and all(entry["returncode"] == 0 for entry in commands)
        and not missing_outputs
    ):
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
        commands.append(_run_command(eval_cmd, cwd=eval_worktree / "bda_eval", env=env))

    summary_path = _latest_summary(eval_dir)
    summary_payload = _load_json(summary_path) if summary_path else None
    payload = {
        "generated_utc": dt.datetime.now(dt.UTC).isoformat(),
        "label": args.label,
        "manifest_path": str(manifest_path),
        "upstream_worktree": str(upstream_worktree),
        "eval_worktree": str(eval_worktree),
        "openai_base_url": args.openai_base_url,
        "model": args.model,
        "predicted_dir": str(predicted_dir),
        "eval_dir": str(eval_dir),
        "summary_path": str(summary_path) if summary_path else None,
        "evaluation_summary": summary_payload,
        "missing_outputs": missing_outputs,
        "commands": commands,
        "succeeded": (
            bool(commands)
            and all(entry["returncode"] == 0 for entry in commands)
            and not missing_outputs
            and summary_path is not None
        ),
    }
    run_summary_path = output_root / "upstream_code_manifest_run_summary.json"
    run_summary_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(run_summary_path)
    return 0 if payload["succeeded"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
