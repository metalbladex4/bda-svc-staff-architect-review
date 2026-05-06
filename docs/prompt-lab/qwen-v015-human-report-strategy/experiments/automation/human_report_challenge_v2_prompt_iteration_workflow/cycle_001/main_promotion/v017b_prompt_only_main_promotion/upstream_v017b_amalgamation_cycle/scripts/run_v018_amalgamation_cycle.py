#!/usr/bin/env python3
"""Run v018 upstream/v017b amalgamation candidates through upstream code."""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


CAPSTONE_ROOT = Path("/home/williambenitez1/Capstone")
WORKTREE_ROOT = Path(
    "/home/williambenitez1/Capstone_worktrees/"
    "1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement"
)
PACKAGE_ROOT = Path(__file__).resolve().parents[1]
PREV_COMPARISON_ROOT = PACKAGE_ROOT.parent / "upstream_main_baseline_comparison"
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
SCRATCH_PARENT = Path("/home/williambenitez1/Capstone_worktrees")
OPENAI_BASE_URL = "http://localhost:11434/v1"
OPENAI_API_KEY = "no-auth"
MODEL = "qwen3-vl:8b-instruct"
UPSTREAM_COMMIT = "f462ef4516b63ca1a2cd2434e75692f65d0e94cb"


@dataclass(frozen=True)
class Candidate:
    """One v018 prompt candidate."""

    candidate_id: str
    title: str
    axis: str
    prompt: str


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected JSON object.")
    return payload


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _read_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle) or {}
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected YAML mapping.")
    return payload


def _write_yaml(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=False), encoding="utf-8")


def _run(
    cmd: list[str],
    *,
    cwd: Path,
    env: dict[str, str] | None = None,
    capture: bool = True,
) -> dict[str, Any]:
    completed = subprocess.run(
        cmd,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
        check=False,
    )
    return {
        "cmd": cmd,
        "cwd": str(cwd),
        "returncode": completed.returncode,
        "stdout_tail": (completed.stdout or "")[-4000:],
        "stderr_tail": (completed.stderr or "")[-4000:],
    }


def _resolve(raw: str | Path, base: Path) -> Path:
    path = Path(raw)
    if not path.is_absolute():
        path = (base / path).resolve()
    return path


def _manifest_cases(manifest_path: Path) -> list[dict[str, Any]]:
    payload = _read_yaml(manifest_path)
    cases = payload.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError(f"{manifest_path}: missing cases.")
    return cases


def _latest_summary(eval_dir: Path) -> Path | None:
    summaries = sorted(eval_dir.glob("evaluation_*_summary.json"))
    return summaries[-1] if summaries else None


def _prompt_hash(prompt: str) -> str:
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()


def _upstream_prompt() -> str:
    result = _run(
        ["git", "show", "upstream/main:src/bda_svc/pipeline/config.yaml"],
        cwd=CAPSTONE_ROOT,
    )
    if result["returncode"] != 0:
        raise RuntimeError(result["stderr_tail"])
    return _read_yaml_from_text(result["stdout_tail"] if False else subprocess.check_output(
        ["git", "show", "upstream/main:src/bda_svc/pipeline/config.yaml"],
        cwd=CAPSTONE_ROOT,
        text=True,
    ))["prompts"]["detect_objects"]


def _read_yaml_from_text(text: str) -> dict[str, Any]:
    payload = yaml.safe_load(text) or {}
    if not isinstance(payload, dict):
        raise ValueError("expected YAML mapping.")
    return payload


def _v017b_prompt() -> str:
    overlay = _read_yaml(
        WORKTREE_ROOT
        / "docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/"
        "human_report_challenge_v2_prompt_iteration_workflow/cycle_001/candidates/"
        "v017b/overlay.yaml"
    )
    return overlay["overrides"]["prompts"]["detect_objects"]


def _required_placeholders(prompt: str) -> dict[str, bool]:
    return {
        token: token in prompt
        for token in ("{categories}", "{detection_guidance}", "{bbox_format}", "{bbox_scale}")
    }


def _validate_prompt(candidate: Candidate) -> None:
    placeholders = _required_placeholders(candidate.prompt)
    missing = [token for token, present in placeholders.items() if not present]
    if missing:
        raise ValueError(f"{candidate.candidate_id}: missing placeholders {missing}")
    forbidden = ["human-report-101", "case 101", "case 155", "case 166", "case 67"]
    lowered = candidate.prompt.lower()
    hits = [term for term in forbidden if term in lowered]
    if hits:
        raise ValueError(f"{candidate.candidate_id}: prompt includes case-specific text {hits}")


def _candidate_prompts() -> list[Candidate]:
    """Return the five v018 candidate prompts."""
    v018a = """Perform a VISUAL-ONLY object detection.

TASK
Detect targets whose doctrinal target_type is one of:
{categories}

GOAL
Find all visible valid targets, then output one tight box per target. Favor
recall for clearly visible targets, but do not create broad area boxes or
unsupported context boxes.

RULES
- First identify all valid targets using the target-type specific detection
  guidance below.
- Include secondary, distant, foreground, background, and off-center targets
  when their own visible body or exterior structure can be boxed.
- Then produce exactly one bounding box per valid target.
- The number of detections must match the number of accepted targets.
- Each box must cover one distinct target body or one exterior building
  structure, not a row, group, smoke region, debris field, road, shadow, or
  broad scene area.
- Do not use object_not_found for a positive-looking target scene. If no valid
  target is visible, return an empty detections list.
- Do not infer equipment from smoke, flames, dust, tracks, repeated marks, or
  ambiguous fragments.
- Do not split one continuous building or one connected wreck body into
  duplicate boxes.

TARGET-TYPE SPECIFIC DETECTION GUIDANCE
{detection_guidance}

FINAL BOX CHECK
Before final JSON, reject any box that mainly contains context, spans multiple
possible targets, or could be tightened substantially without cutting off the
accepted target body.

BOUNDING BOX FORMAT
- Format: {bbox_format}
- Coordinate scale: {bbox_scale}

OUTPUT
Return valid JSON only.
Return a JSON object with a top-level detections field.
If no valid targets are visible, return {"detections": []}.

OUTPUT SCHEMA
{
  "detections": [
    {
      "target_type": string,
      "bbox": {bbox_format}
    }
  ]
}
"""

    v018b = """Perform a VISUAL-ONLY object detection.

TASK
Detect targets whose doctrinal target_type is one of:
{categories}

OUTPUT CONTRACT
Return valid JSON only. If no valid target is visible, return:
{"detections": []}

SILENT METHOD
1. Scan the whole image for visible target candidates.
2. Keep only candidates with a distinct visible target body, wreck body, or
   exterior building structure.
3. Output one tight box for each kept candidate.

RECALL RULES
- Do not stop after the largest, closest, most central, or most damaged target.
- Include small or distant targets when their own body or exterior structure
  remains separable and tight-boxable.
- Burned or destroyed equipment counts when a connected hull, chassis, vehicle
  mass, wreck body, or outline remains visible.

REJECTION RULES
- Reject rows, convoys, clusters, group regions, and scene regions.
- Reject smoke, flame, dust, debris, shadow, road, rail bed, terrain, repeated
  marks, background texture, and adjacent context.
- Reject uncertain targets whose individual body cannot be isolated.
- Reject duplicate partial boxes for the same body or building.
- In crowded rows, output only bodies that are visually separable from
  neighbors; if bodies are not clear, omit that region.
- For buildings, detect distinct exterior structures only; do not split one
  continuous building or box interior rooms, furniture, facade texture, smoke,
  flame, or debris as a building.

TARGET-TYPE SPECIFIC DETECTION GUIDANCE
{detection_guidance}

BOX AUDIT
For every proposed detection, ask silently:
- Is this one target body or exterior structure?
- Is most of the box occupied by that target rather than context?
- Does the box avoid spanning a row, group, or multiple possible targets?
- Can it be tightened without cutting off the accepted target?
If any answer fails, remove the detection instead of using a broad proxy box.

BOUNDING BOX FORMAT
- Format: {bbox_format}
- Coordinate scale: {bbox_scale}

OUTPUT SCHEMA
{
  "detections": [
    {
      "target_type": string,
      "bbox": {bbox_format}
    }
  ]
}
"""

    v018c = """Perform a VISUAL-ONLY object detection.

TASK
Detect targets whose doctrinal target_type is one of:
{categories}

RECALL-FIRST PASS
First, find all visible targets using the target-type specific detection
guidance below. Look across the full image, including foreground, background,
edges, distant areas, and off-center areas. A target can be valid even when
small, partially damaged, burned, or distant, if its own visible body or
exterior structure can be separated from the scene.

PRECISION AUDIT PASS
After recall, audit each proposed target before final JSON:
- Keep it only if the box is tight around one target body, one wreck body, or
  one exterior building structure.
- Remove it if the box is a row, group, cluster, broad scene region, smoke,
  flame, dust, debris, shadow, road, terrain, repeated mark, or adjacent
  context.
- Remove it if the target body cannot be isolated from neighbors.
- Remove duplicate boxes that describe the same target or a subsection of one
  continuous building.
- Never replace a rejected target with a larger proxy box.

TARGET-TYPE SPECIFIC DETECTION GUIDANCE
{detection_guidance}

COUNT DISCIPLINE
- Produce exactly one detection per accepted target.
- Do not invent targets to match an expected count.
- Do not infer a finer subtype; use only the doctrinal target_type category.
- If no valid target remains after the audit, return {"detections": []}.

BOUNDING BOX FORMAT
- Format: {bbox_format}
- Coordinate scale: {bbox_scale}

OUTPUT
Return valid JSON only.
Return a JSON object with a top-level detections field.

OUTPUT SCHEMA
{
  "detections": [
    {
      "target_type": string,
      "bbox": {bbox_format}
    }
  ]
}
"""

    v018d = """Perform a VISUAL-ONLY object detection.

TASK
Detect targets whose doctrinal target_type is one of:
{categories}

WORKFLOW: CANDIDATE EVIDENCE BUDGET
Think silently. Do not output notes. Spend your attention in this order:

1. Candidate sweep
Find possible targets across the whole image. Do not stop at central or obvious
targets. Notice damaged, burned, distant, edge, foreground, and background
objects.

2. Evidence budget
Each final target needs at least one body-support cue:
- connected vehicle or equipment body, hull, chassis, wreck mass, or outline
- distinct exterior building body or collapsed exterior structural remain
- visible target edges or body mass that can be separated from context

The following cues may guide search but cannot justify a final detection by
themselves:
- smoke, flame, dust, soot, blast marks, debris, road, rail bed, shadow,
  repeated dots, row alignment, terrain change, or background texture

3. Budget pruning
If a proposed target uses mostly context cues and weak body support, remove it.
If a proposed box is mostly empty/context area, remove it. If multiple boxes
describe the same connected body or one continuous building, keep only the
tightest single body box.

4. Final boxing
Output one tight box per remaining target. The box must describe the visible
connected target body or exterior structure, not the search cue that helped
find it.

TARGET-TYPE SPECIFIC DETECTION GUIDANCE
{detection_guidance}

DENSE OR ROW-LIKE AREAS
Rows and formations are allowed search regions but not targets. Output only
separable bodies with body-support cues. Do not place evenly spaced placeholder
boxes along dust, smoke, tracks, or a row line. If separate bodies are not
visible enough to box tightly, omit those positions.

NEGATIVE AND UNCERTAIN SCENES
If no valid target has body-support evidence, return {"detections": []}. Do
not output object_not_found as a detection target_type.

BOUNDING BOX FORMAT
- Format: {bbox_format}
- Coordinate scale: {bbox_scale}

OUTPUT
Return valid JSON only.
Return a JSON object with a top-level detections field.

OUTPUT SCHEMA
{
  "detections": [
    {
      "target_type": string,
      "bbox": {bbox_format}
    }
  ]
}
"""

    v018e = """Perform a VISUAL-ONLY object detection.

TASK
Detect targets whose doctrinal target_type is one of:
{categories}

USE CONTRASTIVE BOXING RULES
Good final boxes:
- wrap one connected equipment body, wreck body, or exterior building structure
- are tight enough that most of the box is occupied by the target
- can stand alone if nearby smoke, dust, terrain, roads, shadows, and
  neighboring bodies are ignored
- include small or distant targets when their body center and edges remain
  visible enough to localize

Bad final boxes:
- cover a row, convoy, cluster, formation, broad damaged area, or scene region
- mainly cover smoke, flame, dust, debris, blast effects, shadow, road, rail
  bed, terrain, repeated marks, or background texture
- split one connected target body or one continuous building into fragments
- use evenly spaced placeholders where bodies are not individually visible
- box adjacent context because it is near a real target

DETECTION PROCESS
1. Find obvious targets first.
2. Re-scan for secondary, distant, edge, foreground, and background targets.
3. In row-like or dense scenes, anchor each possible box on visible body
   center, ground contact, hull/chassis/wreck mass, or exterior structure, not
   on the top edge of smoke, dust, or row alignment.
4. Remove any candidate that is not a good final box.
5. Output one box per accepted target.

TARGET-TYPE SPECIFIC DETECTION GUIDANCE
{detection_guidance}

BUILDINGS
Detect distinct exterior building bodies only. Do not box interior rooms,
furniture, facade texture, smoke, flame, debris, or one attached subsection as
a separate building. Do not split a continuous building.

MILITARY EQUIPMENT
Detect distinct equipment bodies and wreck bodies only. Burned equipment can
count when a connected body, chassis, hull, vehicle mass, or wreck outline is
visible. Do not infer equipment from tracks, dust, smoke, repeated marks, or
ambiguous fragments.

OUTPUT DISCIPLINE
- Return only doctrinal target_type values.
- Do not infer finer subtypes.
- If no valid target is visible, return {"detections": []}.

BOUNDING BOX FORMAT
- Format: {bbox_format}
- Coordinate scale: {bbox_scale}

OUTPUT
Return valid JSON only.
Return a JSON object with a top-level detections field.

OUTPUT SCHEMA
{
  "detections": [
    {
      "target_type": string,
      "bbox": {bbox_format}
    }
  ]
}
"""

    return [
        Candidate(
            "v018a_upstream_plus_control_guard",
            "Upstream Plus Control Guard",
            "Upstream skeleton plus minimal v017b controls for broad/group boxes, object_not_found, and positive targets.",
            v018a,
        ),
        Candidate(
            "v018b_compressed_v017b",
            "Compressed v017b",
            "v017b behavior compressed into shorter wording to reduce instruction overload.",
            v018b,
        ),
        Candidate(
            "v018c_upstream_first_precision_audit",
            "Upstream First Precision Audit",
            "Upstream recall-first behavior followed by a compact v017b-style single-target audit.",
            v018c,
        ),
        Candidate(
            "v018d_evidence_budget_pruner",
            "Evidence Budget Pruner",
            "Creative candidate using body-support evidence budget and pruning.",
            v018d,
        ),
        Candidate(
            "v018e_contrastive_body_anchor",
            "Contrastive Body Anchor",
            "Creative candidate using good-box/bad-box contrast and dense-row body anchoring.",
            v018e,
        ),
    ]


def _create_overlays(candidates: list[Candidate]) -> dict[str, Any]:
    registry: dict[str, Any] = {
        "generated_utc": dt.datetime.now(dt.UTC).isoformat(),
        "cycle_id": "v018_upstream_v017b_amalgamation_cycle",
        "runtime_path": "upstream_main_code_ollama_openai_compat",
        "candidates": [],
    }
    for candidate in candidates:
        _validate_prompt(candidate)
        overlay = {
            "overlay_id": f"qwen-1.2-{candidate.candidate_id}",
            "overlay_type": "experiment",
            "model_line": MODEL,
            "description": candidate.axis,
            "overrides": {
                "prompts": {
                    "detect_objects": candidate.prompt,
                },
                "runtime": {
                    "notes": "Prompt text is applied by scratch upstream config replacement; no runtime adoption.",
                },
            },
        }
        path = OVERLAY_DIR / f"{candidate.candidate_id}.yaml"
        _write_yaml(path, overlay)
        registry["candidates"].append(
            {
                "candidate_id": candidate.candidate_id,
                "title": candidate.title,
                "axis": candidate.axis,
                "overlay_path": str(path),
                "prompt_sha256": _prompt_hash(candidate.prompt),
                "prompt_chars": len(candidate.prompt),
                "prompt_lines": len(candidate.prompt.splitlines()),
                "prompt_bullets": sum(
                    1 for line in candidate.prompt.splitlines() if line.strip().startswith("-")
                ),
                "placeholders": _required_placeholders(candidate.prompt),
            }
        )
    _write_json(PACKAGE_ROOT / "candidate_registry.json", registry)
    return registry


def _write_diagnosis(registry: dict[str, Any]) -> None:
    comparison = _read_json(PREV_COMPARISON_ROOT / "upstream_main_baseline_comparison.json")
    upstream_prompt = _upstream_prompt()
    v017b_prompt = _v017b_prompt()
    diagnosis = {
        "generated_utc": dt.datetime.now(dt.UTC).isoformat(),
        "question": "Why is upstream/main doing well, and what should v018 combine?",
        "source_rows": {
            "upstream_prompt_controlled": {
                "match_count": comparison["prompt_controlled_baseline"]["match_count"],
                "false_negative_count": comparison["prompt_controlled_baseline"]["false_negative_count"],
                "false_positive_count": comparison["prompt_controlled_baseline"]["false_positive_count"],
                "case_155": comparison["prompt_controlled_baseline"]["case_155"],
            },
            "v017b_local_qwen": {
                "match_count": comparison["v017b_reference"]["match_count"],
                "false_negative_count": comparison["v017b_reference"]["false_negative_count"],
                "false_positive_count_raw": comparison["v017b_reference"]["false_positive_count_raw"],
                "false_positive_count_effective_extra_target": comparison["v017b_reference"]["false_positive_count_effective_extra_target"],
                "case_155": comparison["v017b_reference"]["case_155"],
            },
            "v017b_upstream_code_compat": comparison[
                "practical_upstream_code_ollama_compat_attempt"
            ]["all_current_result"],
        },
        "prompt_shape": {
            "upstream": {
                "chars": len(upstream_prompt),
                "lines": len(upstream_prompt.splitlines()),
                "bullets": sum(1 for line in upstream_prompt.splitlines() if line.strip().startswith("-")),
            },
            "v017b": {
                "chars": len(v017b_prompt),
                "lines": len(v017b_prompt.splitlines()),
                "bullets": sum(1 for line in v017b_prompt.splitlines() if line.strip().startswith("-")),
            },
        },
        "hypothesis": [
            "Upstream's short prompt leaves the model freer to enumerate ordinary visible targets.",
            "v017b's repeated filters improve corrected positive-control and FP behavior but can under-count clean multi-object scenes.",
            "The best amalgamation should keep upstream's simple task flow while adding only the highest-yield v017b controls.",
        ],
        "candidate_registry": str(PACKAGE_ROOT / "candidate_registry.json"),
        "candidate_count": len(registry["candidates"]),
    }
    _write_json(PACKAGE_ROOT / "upstream_v017b_prompt_diagnosis.json", diagnosis)

    md = f"""# Upstream/v017b Prompt Diagnosis

Generated: `{diagnosis['generated_utc']}`

## Why Upstream Is Doing Well

The current upstream prompt is short and permissive. It has `{diagnosis['prompt_shape']['upstream']['chars']}`
characters, `{diagnosis['prompt_shape']['upstream']['lines']}` lines, and `{diagnosis['prompt_shape']['upstream']['bullets']}`
bullets. On the same all-current/no101 pack, the prompt-controlled upstream row
scored `{diagnosis['source_rows']['upstream_prompt_controlled']['match_count']}`
matches, `{diagnosis['source_rows']['upstream_prompt_controlled']['false_negative_count']}`
FNs, and `{diagnosis['source_rows']['upstream_prompt_controlled']['false_positive_count']}`
FPs, but failed corrected positive-control `155`.

The accepted v017b prompt is much more defensive. It has
`{diagnosis['prompt_shape']['v017b']['chars']}` characters,
`{diagnosis['prompt_shape']['v017b']['lines']}` lines, and
`{diagnosis['prompt_shape']['v017b']['bullets']}` bullets. It improved corrected
positive-control and false-positive behavior in the local reference row, but it
lost raw recall relative to the upstream prompt-controlled row.

## Working Hypothesis

- Upstream's brevity improves ordinary visible-target enumeration.
- v017b's repeated single-body filters suppress context boxes and fix `155`, but
  can make the model under-count clean multi-object scenes.
- v018 should keep upstream's simple recall path while importing only the
  highest-yield v017b controls.

## Candidate Set

Five candidates were authored:

"""
    for row in registry["candidates"]:
        md += (
            f"- `{row['candidate_id']}`: {row['axis']} "
            f"({row['prompt_chars']} chars, {row['prompt_bullets']} bullets)\n"
        )
    md += """
## Boundaries

This diagnosis is experiment evidence only. It does not change doctrine, source
truth, runtime config, GitHub PR state, Graphify, or Mem0.
"""
    (PACKAGE_ROOT / "upstream_v017b_prompt_diagnosis.md").write_text(md, encoding="utf-8")


def _validate_manifests() -> dict[str, Any]:
    all_cases = _manifest_cases(ALL_CURRENT_MANIFEST)
    office_cases = _manifest_cases(OFFICE_NEGATIVE_MANIFEST)
    ids = [case["case_id"] for case in all_cases]
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


def _check_endpoint() -> dict[str, Any]:
    url = f"{OPENAI_BASE_URL}/models"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except Exception as exc:  # pragma: no cover - diagnostic path
        return {"url": url, "status": "unavailable", "error": repr(exc)}
    ids = [item.get("id") for item in payload.get("data", []) if isinstance(item, dict)]
    return {
        "url": url,
        "status": "available" if MODEL in ids else "model_missing",
        "model_ids": ids,
    }


def _patch_scratch_config(scratch: Path, prompt: str) -> None:
    config_path = scratch / "src/bda_svc/pipeline/config.yaml"
    config = _read_yaml(config_path)
    config["prompts"]["detect_objects"] = prompt
    _write_yaml(config_path, config)


def _run_manifest(
    *,
    candidate_id: str,
    manifest_path: Path,
    scratch: Path,
    run_root: Path,
) -> dict[str, Any]:
    manifest_cases = _manifest_cases(manifest_path)
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

    command_log: list[dict[str, Any]] = []
    missing_outputs: list[str] = []
    start = time.time()
    total = len(manifest_cases)
    for index, case in enumerate(manifest_cases, start=1):
        image_path = _resolve(case["image_path"], manifest_path.parent)
        before = set(predicted_dir.glob(f"{image_path.stem}_*.json"))
        cmd = ["uv", "run", "bda-svc", "-i", str(image_path), "-o", str(predicted_dir)]
        entry = _run(cmd, cwd=scratch, env=env)
        command_log.append(entry)
        after = set(predicted_dir.glob(f"{image_path.stem}_*.json"))
        print(
            f"[{candidate_id}] {manifest_path.stem}: {index}/{total} "
            f"{image_path.name} rc={entry['returncode']}",
            flush=True,
        )
        if entry["returncode"] != 0:
            break
        if not (after - before):
            missing_outputs.append(image_path.name)
            break

    if command_log and all(item["returncode"] == 0 for item in command_log) and not missing_outputs:
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
        command_log.append(_run(eval_cmd, cwd=WORKTREE_ROOT / "bda_eval", env=env))

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
        "commands": command_log,
        "elapsed_seconds": round(time.time() - start, 3),
        "succeeded": (
            bool(command_log)
            and all(item["returncode"] == 0 for item in command_log)
            and not missing_outputs
            and summary_path is not None
        ),
    }
    summary_file = output_root / "upstream_code_manifest_run_summary.json"
    _write_json(summary_file, payload)
    return payload | {"run_summary_path": str(summary_file)}


def _create_scratch(candidate_id: str) -> Path:
    stamp = dt.datetime.now(dt.UTC).strftime("%Y%m%d_%H%M%SZ")
    scratch = SCRATCH_PARENT / f"_scratch_v018_{candidate_id}_{stamp}"
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


def _candidate_result(candidate: Candidate, all_run: dict[str, Any], office_run: dict[str, Any]) -> dict[str, Any]:
    all_summary = all_run["evaluation_summary"]
    office_summary = office_run["evaluation_summary"]
    totals = _totals(all_run)
    office_totals = office_summary["totals"]
    case_155 = _case(all_summary, "155.jpg")
    case_166 = _case(all_summary, "166.jpg")
    dense = {case: _case(all_summary, f"{case}.jpg") for case in ("66", "67", "84", "97")}
    controls_pass = (
        case_155["match_count"] >= 1
        and case_166["match_count"] >= 1
        and office_totals["negative_scene_abstention_correct_count"] == 1
        and office_totals["negative_scene_false_positive_count"] == 0
    )
    outright_winner = (
        totals["match_count"] > 169
        and totals["false_negative_count"] < 50
        and totals["false_positive_count"] <= 22
        and controls_pass
    )
    disqualified = not controls_pass or not all_run["succeeded"] or not office_run["succeeded"]
    return {
        "candidate_id": candidate.candidate_id,
        "title": candidate.title,
        "axis": candidate.axis,
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
        "outright_winner": outright_winner,
        "all_current_run_summary": all_run["run_summary_path"],
        "office_negative_run_summary": office_run["run_summary_path"],
        "nonzero_command_count": sum(1 for c in all_run["commands"] + office_run["commands"] if c["returncode"] != 0),
        "missing_outputs": all_run["missing_outputs"] + office_run["missing_outputs"],
    }


def _rank_results(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    def key(item: dict[str, Any]) -> tuple[Any, ...]:
        return (
            0 if item["disqualified"] else 1,
            1 if item["controls_pass"] else 0,
            item["match_count"],
            -item["false_negative_count"],
            -item["false_positive_count"],
            item["dense_cases"]["67"]["match_count"],
            -item["dense_cases"]["67"]["false_positive_count"],
        )

    return sorted(results, key=key, reverse=True)


def _write_reports(results: list[dict[str, Any]], recovery_events: list[dict[str, Any]]) -> None:
    comparison = _read_json(PREV_COMPARISON_ROOT / "upstream_main_baseline_comparison.json")
    ranking = _rank_results(results)
    outright = [item for item in ranking if item["outright_winner"]]
    best = ranking[0] if ranking else None
    final_verdict = (
        "outright_winner_found"
        if outright
        else "no_outright_winner_rank_best_pareto_candidate"
        if best and not best["disqualified"]
        else "no_candidate_recommended"
    )
    matrix = {
        "generated_utc": dt.datetime.now(dt.UTC).isoformat(),
        "cycle_id": "v018_upstream_v017b_amalgamation_cycle",
        "baselines": {
            "upstream_prompt_controlled": {
                "match_count": 169,
                "false_negative_count": 50,
                "false_positive_count": 24,
                "case_155_passed": False,
            },
            "v017b_local_qwen": {
                "match_count": 165,
                "false_negative_count": 54,
                "false_positive_count_raw": 22,
                "false_positive_count_effective_extra_target": 21,
                "case_155_passed": True,
            },
            "v017b_upstream_code_compat": {
                "match_count": 166,
                "false_negative_count": 53,
                "false_positive_count": 26,
                "case_155_passed": True,
            },
        },
        "results": results,
        "ranking": [item["candidate_id"] for item in ranking],
        "final_verdict": final_verdict,
        "recommended_candidate": best["candidate_id"] if best and not best["disqualified"] else None,
        "recovery_events": recovery_events,
        "source_comparison": str(PREV_COMPARISON_ROOT / "upstream_main_baseline_comparison.json"),
    }
    _write_json(PACKAGE_ROOT / "comparison_matrix.json", matrix)
    _write_json(PACKAGE_ROOT / "final_recommendation.json", matrix)
    _write_json(PACKAGE_ROOT / "recovery_log.json", {"generated_utc": matrix["generated_utc"], "events": recovery_events})

    md = f"""# v018 Upstream/v017b Amalgamation Cycle

Generated: `{matrix['generated_utc']}`

## Baselines

| Row | Matches | FNs | FPs | `155` |
| --- | ---: | ---: | ---: | --- |
| upstream prompt-controlled | 169 | 50 | 24 | fail |
| v017b local Qwen | 165 | 54 | 22 raw / 21 effective | pass |
| v017b upstream-code compat | 166 | 53 | 26 | pass |

## Candidate Results

| Rank | Candidate | Matches | FNs | FPs | `155` | `166` | Office | Verdict |
| ---: | --- | ---: | ---: | ---: | --- | --- | --- | --- |
"""
    for idx, item in enumerate(ranking, start=1):
        md += (
            f"| {idx} | `{item['candidate_id']}` | {item['match_count']} | "
            f"{item['false_negative_count']} | {item['false_positive_count']} | "
            f"{item['case_155']['match_count']}m/{item['case_155']['false_negative_count']}fn/{item['case_155']['false_positive_count']}fp | "
            f"{item['case_166']['match_count']}m/{item['case_166']['false_negative_count']}fn/{item['case_166']['false_positive_count']}fp | "
            f"{'pass' if item['office_negative']['negative_scene_abstention_correct_count'] == 1 else 'fail'} | "
            f"{'outright winner' if item['outright_winner'] else 'disqualified' if item['disqualified'] else 'near/pareto'} |\n"
        )
    md += "\n## Dense Case Snapshot\n\n"
    md += "| Candidate | 66 | 67 | 84 | 97 |\n| --- | --- | --- | --- | --- |\n"
    for item in ranking:
        dense = item["dense_cases"]
        md += (
            f"| `{item['candidate_id']}` | "
            f"{dense['66']['match_count']}/{dense['66']['false_negative_count']}/{dense['66']['false_positive_count']} | "
            f"{dense['67']['match_count']}/{dense['67']['false_negative_count']}/{dense['67']['false_positive_count']} | "
            f"{dense['84']['match_count']}/{dense['84']['false_negative_count']}/{dense['84']['false_positive_count']} | "
            f"{dense['97']['match_count']}/{dense['97']['false_negative_count']}/{dense['97']['false_positive_count']} |\n"
        )
    md += f"""
## Recommendation

Verdict: `{final_verdict}`.

Recommended candidate: `{matrix['recommended_candidate']}`.

Decision rule reminder: an outright winner must beat upstream raw recall
(`>169` matches and `<50` FNs), stay at or below the v017b raw FP ceiling
(`<=22`), and pass `155`, `166`, and office-negative.

## Boundaries

No source reports, references, doctrine, runtime config adoption, commit, push,
Graphify refresh, or Mem0 write happened in this wave.
"""
    (PACKAGE_ROOT / "comparison_matrix.md").write_text(md, encoding="utf-8")
    (PACKAGE_ROOT / "final_recommendation.md").write_text(md, encoding="utf-8")


def _write_source_manifest(manifest_checks: dict[str, Any], endpoint: dict[str, Any]) -> None:
    payload = {
        "generated_utc": dt.datetime.now(dt.UTC).isoformat(),
        "cycle_id": "v018_upstream_v017b_amalgamation_cycle",
        "purpose": "Test five detect prompt amalgamations of upstream/main and v017b.",
        "upstream_commit": UPSTREAM_COMMIT,
        "runtime_path": "current upstream/main code with Ollama OpenAI-compatible endpoint",
        "openai_base_url": OPENAI_BASE_URL,
        "model": MODEL,
        "manifest_checks": manifest_checks,
        "endpoint_check": endpoint,
        "previous_comparison_package": str(PREV_COMPARISON_ROOT),
        "boundaries": {
            "commit_or_push": False,
            "graphify_refresh": False,
            "mem0_write": False,
            "runtime_adoption": False,
            "source_truth_mutation": False,
            "doctrine_edit": False,
        },
    }
    _write_json(PACKAGE_ROOT / "source_manifest.json", payload)


def main() -> int:
    PACKAGE_ROOT.mkdir(parents=True, exist_ok=True)
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    endpoint = _check_endpoint()
    manifest_checks = _validate_manifests()
    _write_source_manifest(manifest_checks, endpoint)
    if endpoint["status"] != "available":
        _write_json(PACKAGE_ROOT / "recovery_log.json", {"events": [{"type": "endpoint_blocker", "endpoint": endpoint}]})
        print(f"Endpoint unavailable: {endpoint}", file=sys.stderr)
        return 2

    candidates = _candidate_prompts()
    registry = _create_overlays(candidates)
    _write_diagnosis(registry)

    results: list[dict[str, Any]] = []
    recovery_events: list[dict[str, Any]] = []
    for candidate in candidates:
        scratch: Path | None = None
        try:
            print(f"\n=== Running {candidate.candidate_id} ===", flush=True)
            scratch = _create_scratch(candidate.candidate_id)
            _patch_scratch_config(scratch, candidate.prompt)
            run_root = RUNS_DIR / candidate.candidate_id
            office_run = _run_manifest(
                candidate_id=candidate.candidate_id,
                manifest_path=OFFICE_NEGATIVE_MANIFEST,
                scratch=scratch,
                run_root=run_root / "office_negative",
            )
            all_run = _run_manifest(
                candidate_id=candidate.candidate_id,
                manifest_path=ALL_CURRENT_MANIFEST,
                scratch=scratch,
                run_root=run_root / "all_current_no101",
            )
            results.append(_candidate_result(candidate, all_run, office_run))
        except Exception as exc:  # pragma: no cover - operational recovery log
            recovery_events.append(
                {
                    "candidate_id": candidate.candidate_id,
                    "type": "candidate_run_exception",
                    "error": repr(exc),
                    "recovered": False,
                }
            )
        finally:
            if scratch is not None:
                recovery_events.append(
                    {
                        "candidate_id": candidate.candidate_id,
                        "type": "scratch_cleanup",
                        **_remove_scratch(scratch),
                    }
                )
    _write_reports(results, recovery_events)
    print(PACKAGE_ROOT / "comparison_matrix.json")
    print(PACKAGE_ROOT / "final_recommendation.md")
    return 0 if len(results) == len(candidates) else 1


if __name__ == "__main__":
    raise SystemExit(main())
