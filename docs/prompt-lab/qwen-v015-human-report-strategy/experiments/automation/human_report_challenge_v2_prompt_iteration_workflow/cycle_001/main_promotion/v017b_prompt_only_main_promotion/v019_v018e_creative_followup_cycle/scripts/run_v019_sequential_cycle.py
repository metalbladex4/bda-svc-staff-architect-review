#!/usr/bin/env python3
"""Run the sequential v019 v018e follow-up prompt cycle."""

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
V018_ROOT = PACKAGE_ROOT.parent / "upstream_v017b_amalgamation_cycle"
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

HISTORICAL_BASELINES = {
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
    "v018d_recall_ceiling": {
        "match_count": 180,
        "false_negative_count": 39,
        "false_positive_count": 39,
        "case_155_passed": True,
    },
    "v018e_historical_anchor": {
        "match_count": 173,
        "false_negative_count": 46,
        "false_positive_count": 29,
        "case_155_passed": True,
    },
}


@dataclass(frozen=True)
class Candidate:
    candidate_id: str
    title: str
    axis: str
    prompt: str
    generated_from: list[str]


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


def _resolve(raw: str | Path, base: Path) -> Path:
    path = Path(raw)
    if not path.is_absolute():
        path = (base / path).resolve()
    return path


def _manifest_cases(manifest_path: Path) -> list[dict[str, Any]]:
    payload = _read_yaml(manifest_path)
    cases = payload.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError(f"{manifest_path}: missing cases")
    return cases


def _latest_summary(eval_dir: Path) -> Path | None:
    summaries = sorted(eval_dir.glob("evaluation_*_summary.json"))
    return summaries[-1] if summaries else None


def _prompt_hash(prompt: str) -> str:
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()


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
    lowered = candidate.prompt.lower()
    forbidden = ["human-report", "case 101", "case 155", "case 166", "case 67"]
    hits = [term for term in forbidden if term in lowered]
    if hits:
        raise ValueError(f"{candidate.candidate_id}: prompt includes forbidden case text {hits}")


def _load_v018e_prompt() -> str:
    overlay = _read_yaml(V018_ROOT / "overlays/v018e_contrastive_body_anchor.yaml")
    return overlay["overrides"]["prompts"]["detect_objects"]


def _base_output_contract() -> str:
    return """TARGET-TYPE SPECIFIC DETECTION GUIDANCE
{detection_guidance}

BOUNDING BOX FORMAT
- Format: {bbox_format}
- Coordinate scale: {bbox_scale}

OUTPUT
Return valid JSON only.
Return a JSON object with a top-level detections field.
If no valid target is visible, return {"detections": []}.

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


def _lesson_text(results: list[dict[str, Any]]) -> str:
    if not results:
        return (
            "Calibration: start from v018e. Preserve positive-control safety and "
            "office abstention while reducing context-only false positives."
        )
    last = results[-1]
    parts: list[str] = []
    if last["false_positive_count"] >= 29:
        parts.append("tighten the final veto against context-heavy boxes")
    if last["match_count"] <= 173:
        parts.append("avoid becoming fail-closed; keep a full-image recall sweep")
    if last["match_count"] > 173 and last["false_positive_count"] >= 29:
        parts.append("preserve the recall gain but add a sharper precision filter")
    dense = last["dense_cases"]
    if dense["67"]["false_positive_count"] >= 8 or dense["67"]["false_negative_count"] >= 7:
        parts.append("dense formations still need a separable-body test, not placeholder spacing")
    if dense["84"]["false_negative_count"] >= 5:
        parts.append("large multi-target scenes still need a second pass for missed bodies")
    if not parts:
        parts.append("preserve the prior candidate's balance and compress the rules")
    return "Calibration from prior run: " + "; ".join(parts) + "."


def _candidate_v019a(results: list[dict[str, Any]]) -> Candidate:
    prompt = f"""Perform a VISUAL-ONLY object detection.

TASK
Detect targets whose doctrinal target_type is one of:
{{categories}}

{_lesson_text(results)}

FP SIEVE METHOD
1. Scan the whole image for possible military equipment, wreck bodies, and
   distinct exterior building structures.
2. For each possible target, require a visible target body: connected hull,
   chassis, wreck mass, structural exterior, body center, or clear body edge.
3. Reject a candidate when the box is mostly smoke, flame, dust, shadow, road,
   debris, terrain, background texture, repeated marks, or adjacent context.
4. Reject broad row, convoy, cluster, formation, and scene-region boxes.
5. Keep one tight box per accepted target.

FINAL BOX SIEVE
Before output, silently ask for every box:
- Would this still be a target box if nearby smoke, dust, road, debris, and
  shadows were ignored?
- Is most of the box occupied by one target body or one exterior structure?
- Can the box be tightened without cutting off the accepted target?
If any answer is no, remove the detection.

{_base_output_contract()}"""
    return Candidate(
        "v019a_fp_sieve",
        "FP Sieve",
        "v018e with a stricter final context/occupancy veto.",
        prompt,
        ["v018e_historical_anchor"],
    )


def _candidate_v019b(results: list[dict[str, Any]]) -> Candidate:
    prompt = f"""Perform a VISUAL-ONLY object detection.

TASK
Detect targets whose doctrinal target_type is one of:
{{categories}}

{_lesson_text(results)}

BUDGETED RECALL FUSE
Think silently. Do not output notes.

1. Recall sweep: search center, edges, foreground, background, small targets,
   distant targets, damaged equipment, burned wrecks, and exterior structures.
2. Evidence budget: each final target needs at least two visible support cues
   when the scene is crowded, or one strong body cue when the target is obvious.
   Support cues include body center, hull/chassis, connected wreck mass, clear
   exterior structure, target edge, ground contact, or separable body outline.
3. Context is search evidence only. Smoke, dust, shadows, roads, row alignment,
   tracks, debris, blast marks, repeated dots, and terrain change cannot justify
   a final detection without body support.
4. Precision fuse: if a candidate was found by context, shrink it to the body.
   If it cannot be shrunk to a body, remove it.

DENSE SCENES
Rows and formations are search regions, not targets. Output only individually
separable bodies. Do not place evenly spaced boxes where individual bodies are
not visible.

{_base_output_contract()}"""
    return Candidate(
        "v019b_budgeted_recall_fuse",
        "Budgeted Recall Fuse",
        "v018e plus a capped version of v018d's evidence-budget recall behavior.",
        prompt,
        [results[-1]["candidate_id"] if results else "v018e_historical_anchor"],
    )


def _candidate_v019c(results: list[dict[str, Any]]) -> Candidate:
    prompt = f"""Perform a VISUAL-ONLY object detection.

TASK
Detect targets whose doctrinal target_type is one of:
{{categories}}

{_lesson_text(results)}

CONTEXT SHADOW REVERSAL
Use context to search, then mentally remove context to decide.

1. Find possible targets across the full image.
2. For each candidate, imagine removing smoke, dust, flame, shadow, road,
   debris, row alignment, blast texture, tracks, and terrain marks.
3. Keep the candidate only if a target body, wreck body, or exterior structure
   remains visible enough to draw a tight box after those context cues are
   removed.
4. If the candidate disappears when context is ignored, reject it.
5. If a broad box contains several possible targets, split only when distinct
   bodies are visible; otherwise reject the broad box.

GOOD FINAL BOX
- one connected target body, wreck body, or exterior building structure
- tight enough that the target occupies most of the box
- not a proxy for damage effects, row position, nearby roads, or debris

BAD FINAL BOX
- context-only cue
- group, row, convoy, cluster, or scene region
- duplicate fragment of one connected body
- interior/facade/debris subsection of one continuous building

{_base_output_contract()}"""
    return Candidate(
        "v019c_context_shadow_reversal",
        "Context Shadow Reversal",
        "Reject candidates that vanish when context-only cues are mentally removed.",
        prompt,
        [results[-1]["candidate_id"]],
    )


def _candidate_v019d(results: list[dict[str, Any]]) -> Candidate:
    prompt = f"""Perform a VISUAL-ONLY object detection.

TASK
Detect targets whose doctrinal target_type is one of:
{{categories}}

{_lesson_text(results)}

TRIAGE LADDER DETECTOR
Think silently in three bins, but output only final JSON.

BIN 1: CERTAIN
Targets with a clear connected body, wreck mass, or exterior structure. Keep
these unless the box spans multiple targets or mostly context.

BIN 2: SUPPORTED
Small, distant, damaged, or partially obscured targets with enough body edge,
body center, chassis, structure, or ground contact to localize tightly. Keep
only when the box can be drawn around the body, not around the clue.

BIN 3: REJECT
Smoke, flame, dust, debris, shadow, roads, tracks, rail beds, row alignment,
repeated marks, texture, broad damage zones, placeholder spacing, and any
candidate whose body cannot be isolated.

FINAL SELECTION
Output BIN 1 plus only BIN 2 candidates that survive the reject test. Never
promote BIN 3 to a broad proxy box. Merge duplicates that describe one connected
body or one continuous building.

{_base_output_contract()}"""
    return Candidate(
        "v019d_triage_ladder_detector",
        "Triage Ladder Detector",
        "Silent certain/supported/reject triage before final detections.",
        prompt,
        [results[-1]["candidate_id"]],
    )


def _candidate_v019e(results: list[dict[str, Any]]) -> Candidate:
    prompt = f"""Perform a VISUAL-ONLY object detection.

TASK
Detect targets whose doctrinal target_type is one of:
{{categories}}

{_lesson_text(results)}

CARTOGRAPHER GRID SWEEP
Think silently. Treat the image as a map with overlapping zones: center, four
corners, four edges, foreground, midground, and background. Do not output this
map.

1. Sweep each zone for visible target bodies or exterior structures.
2. In each zone, mark only candidates with their own body support.
3. Merge duplicate candidates that refer to the same connected body across
   neighboring zones.
4. Apply the body-anchor veto: if a candidate is mostly context, damage effect,
   row alignment, or scene texture, remove it.
5. Output one tight box per surviving target.

SPATIAL DISCIPLINE
- A target near an image edge is valid only when its own body is visible enough
  to localize.
- A target in a row is valid only when its body separates from neighbors.
- A large structure is one target when it is one continuous exterior building.
- A broad area is never a substitute for uncertain individual targets.

{_base_output_contract()}"""
    return Candidate(
        "v019e_cartographer_grid_sweep",
        "Cartographer Grid Sweep",
        "Silent spatial sweep inspired by visual grounding research, then merge/veto.",
        prompt,
        [results[-1]["candidate_id"]],
    )


def _candidate_v019f(results: list[dict[str, Any]]) -> Candidate:
    prompt = f"""Perform a VISUAL-ONLY object detection.

TASK
Detect targets whose doctrinal target_type is one of:
{{categories}}

{_lesson_text(results)}

ADVERSARIAL BOX JURY
Think silently with three internal roles. Do not output the roles or notes.

RECALL SCOUT
Find every plausible target body across the whole image: obvious, small,
distant, edge, foreground, background, burned, damaged, and partially obscured
targets.

FALSE-POSITIVE PROSECUTOR
Attack each proposed box. Reject it if the evidence is mainly smoke, dust,
flame, debris, shadow, road, rail bed, track, row alignment, repeated mark,
terrain texture, broad damage area, adjacent context, or placeholder spacing.
Reject it if the box covers a group, row, convoy, cluster, or scene region.

BOX JUDGE
Keep only boxes that survive both sides:
- one visible connected target body, wreck body, or exterior building structure
- tight enough that the target occupies most of the box
- separable from neighbors
- not a duplicate or fragment of the same connected body

JURY RULE
When recall scout and prosecutor disagree, choose the smaller body-supported
box if a body is visible. If no body-supported tight box exists, omit the
candidate. Never output a broad compromise box.

{_base_output_contract()}"""
    return Candidate(
        "v019f_adversarial_box_jury",
        "Adversarial Box Jury",
        "Recall scout, FP prosecutor, and box judge synthesize the final boxes.",
        prompt,
        [results[-1]["candidate_id"]],
    )


def _candidate_v019g(results: list[dict[str, Any]]) -> Candidate:
    prompt = f"""Perform a VISUAL-ONLY object detection.

TASK
Detect targets whose doctrinal target_type is one of:
{{categories}}

{_lesson_text(results)}

PROSECUTOR-HEAVY JURY
Use the adversarial jury from the prior candidate, but give the false-positive
prosecutor veto power over any box that cannot prove target-body occupancy.
Keep recall open during search, then make final selection conservative.

FINAL VETOES
- box mostly context: reject
- row/cluster/formation/scene region: reject
- body not separable from neighbors: reject
- connected target split into fragments: merge or reject
- broad compromise box: reject

Only output targets that remain after this veto and still have a tight
body-supported box.

{_base_output_contract()}"""
    return Candidate(
        "v019g_prosecutor_heavy",
        "Prosecutor Heavy",
        "Conditional v019f follow-up with stronger FP veto.",
        prompt,
        [results[-1]["candidate_id"]],
    )


def _candidate_v019h(results: list[dict[str, Any]]) -> Candidate:
    prompt = f"""Perform a VISUAL-ONLY object detection.

TASK
Detect targets whose doctrinal target_type is one of:
{{categories}}

{_lesson_text(results)}

SCOUT WITH FP LEASH
Search like a recall scout, but every final target must carry a leash: a visible
body anchor that the box cannot move away from.

LEASH TEST
For each candidate, identify the visual anchor silently:
body center, hull, chassis, wreck mass, body edge, exterior wall/roof mass, or
ground-contact outline. Draw the box around that anchor and target body only.
If the anchor is smoke, road, shadow, debris, row spacing, or terrain texture,
reject the candidate.

Output all body-anchored candidates after duplicate merge and context veto.

{_base_output_contract()}"""
    return Candidate(
        "v019h_scout_with_fp_leash",
        "Scout With FP Leash",
        "Conditional v019f follow-up that restores recall while forcing anchors.",
        prompt,
        [results[-1]["candidate_id"]],
    )


def _candidate_v019i(results: list[dict[str, Any]]) -> Candidate:
    prompt = f"""Perform a VISUAL-ONLY object detection.

TASK
Detect targets whose doctrinal target_type is one of:
{{categories}}

{_lesson_text(results)}

COMPRESSED BOX-JUDGE RUBRIC
Scan the full image. Keep a detection only when all four checks pass:

1. BODY: one connected equipment body, wreck body, or exterior building body is
   visible.
2. BOUNDARY: the box can be tight around that body without becoming a broad
   scene, row, cluster, or context box.
3. SEPARATION: the body is separable from neighboring targets and background
   effects.
4. CLEANUP: smoke, dust, road, debris, shadow, texture, and row alignment helped
   search but do not occupy most of the final box.

If a candidate fails any check, omit it. If multiple boxes describe one body,
keep the tightest one.

{_base_output_contract()}"""
    return Candidate(
        "v019i_judge_rubric_compression",
        "Judge Rubric Compression",
        "Conditional v019f follow-up that compresses the jury into four checks.",
        prompt,
        [results[-1]["candidate_id"]],
    )


BASE_SEQUENCE = [
    _candidate_v019a,
    _candidate_v019b,
    _candidate_v019c,
    _candidate_v019d,
    _candidate_v019e,
    _candidate_v019f,
]
EXTRA_SEQUENCE = [_candidate_v019g, _candidate_v019h, _candidate_v019i]


def _create_overlay(candidate: Candidate) -> dict[str, Any]:
    _validate_prompt(candidate)
    overlay = {
        "overlay_id": f"qwen-1.2-{candidate.candidate_id}",
        "overlay_type": "experiment",
        "model_line": MODEL,
        "description": candidate.axis,
        "generated_from": candidate.generated_from,
        "overrides": {
            "prompts": {"detect_objects": candidate.prompt},
            "runtime": {
                "notes": "Prompt text is applied by scratch upstream config replacement; no runtime adoption.",
            },
        },
    }
    path = OVERLAY_DIR / f"{candidate.candidate_id}.yaml"
    _write_yaml(path, overlay)
    return {
        "candidate_id": candidate.candidate_id,
        "title": candidate.title,
        "axis": candidate.axis,
        "generated_from": candidate.generated_from,
        "overlay_path": str(path),
        "prompt_sha256": _prompt_hash(candidate.prompt),
        "prompt_chars": len(candidate.prompt),
        "prompt_lines": len(candidate.prompt.splitlines()),
        "prompt_bullets": sum(1 for line in candidate.prompt.splitlines() if line.strip().startswith("-")),
        "placeholders": _required_placeholders(candidate.prompt),
    }


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


def _check_endpoint() -> dict[str, Any]:
    url = f"{OPENAI_BASE_URL}/models"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        return {"url": url, "status": "unavailable", "error": repr(exc)}
    ids = [item.get("id") for item in payload.get("data", []) if isinstance(item, dict)]
    return {"url": url, "status": "available" if MODEL in ids else "model_missing", "model_ids": ids}


def _create_scratch(candidate_id: str) -> Path:
    stamp = dt.datetime.now(dt.UTC).strftime("%Y%m%d_%H%M%SZ")
    scratch = SCRATCH_PARENT / f"_scratch_v019_{candidate_id}_{stamp}"
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


def _run_manifest(
    *,
    candidate_id: str,
    manifest_path: Path,
    scratch: Path,
    run_root: Path,
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
        after = set(predicted_dir.glob(f"{image_path.stem}_*.json"))
        print(
            f"[{candidate_id}] {manifest_path.stem}: {index}/{len(cases)} "
            f"{image_path.name} rc={entry['returncode']}",
            flush=True,
        )
        if entry["returncode"] != 0:
            break
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
        "succeeded": (
            bool(commands)
            and all(item["returncode"] == 0 for item in commands)
            and not missing_outputs
            and summary_path is not None
        ),
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


def _candidate_result(
    candidate: Candidate,
    all_run: dict[str, Any],
    office_run: dict[str, Any],
    *,
    anchor: dict[str, Any],
) -> dict[str, Any]:
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
    disqualified = not controls_pass or not all_run["succeeded"] or not office_run["succeeded"]
    adoption_grade = (
        totals["match_count"] > 173
        and totals["false_negative_count"] < 46
        and totals["false_positive_count"] <= 22
        and controls_pass
    )
    strong_next_primary = (
        totals["match_count"] > anchor["match_count"]
        and totals["false_negative_count"] < anchor["false_negative_count"]
        and totals["false_positive_count"] < anchor["false_positive_count"]
        and controls_pass
    )
    return {
        "candidate_id": candidate.candidate_id,
        "title": candidate.title,
        "axis": candidate.axis,
        "generated_from": candidate.generated_from,
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
        "adoption_grade": adoption_grade,
        "strong_next_primary": strong_next_primary,
        "learning_only": controls_pass and not adoption_grade and not strong_next_primary,
        "delta_vs_anchor": {
            "match_count": totals["match_count"] - anchor["match_count"],
            "false_negative_count": totals["false_negative_count"] - anchor["false_negative_count"],
            "false_positive_count": totals["false_positive_count"] - anchor["false_positive_count"],
        },
        "all_current_run_summary": all_run["run_summary_path"],
        "office_negative_run_summary": office_run["run_summary_path"],
        "nonzero_command_count": sum(1 for c in all_run["commands"] + office_run["commands"] if c["returncode"] != 0),
        "missing_outputs": all_run["missing_outputs"] + office_run["missing_outputs"],
    }


def _diagnosis(result: dict[str, Any], prior_results: list[dict[str, Any]], anchor: dict[str, Any]) -> dict[str, Any]:
    preserve: list[str] = []
    avoid: list[str] = []
    if result["controls_pass"]:
        preserve.append("kept 155, 166, and office-negative safe")
    else:
        avoid.append("control failure disqualifies the candidate")
    if result["match_count"] > anchor["match_count"]:
        preserve.append("improved recall over the v018e anchor")
    else:
        avoid.append("did not improve recall over the v018e anchor")
    if result["false_positive_count"] < anchor["false_positive_count"]:
        preserve.append("reduced false positives versus v018e")
    else:
        avoid.append("false positives still at or above the v018e pressure point")
    if result["dense_cases"]["67"]["match_count"] <= 3:
        avoid.append("dense formation recall remains weak")
    if result["dense_cases"]["66"]["false_positive_count"] >= 5:
        avoid.append("dense/row false positives remain concentrated")
    if result["dense_cases"]["84"]["false_negative_count"] <= 4:
        preserve.append("improved larger multi-target scene recall")

    if result["adoption_grade"]:
        verdict = "adoption_grade"
    elif result["strong_next_primary"]:
        verdict = "strong_next_primary"
    elif result["disqualified"]:
        verdict = "disqualified"
    else:
        verdict = "learning_only"

    next_axis = "compress the strongest surviving behavior"
    if result["false_positive_count"] >= anchor["false_positive_count"]:
        next_axis = "tighten final veto without losing full-image sweep"
    elif result["match_count"] <= anchor["match_count"]:
        next_axis = "restore recall while preserving the FP reduction"
    elif result["strong_next_primary"]:
        next_axis = "preserve this balance and test a more creative variant"

    return {
        "generated_utc": dt.datetime.now(dt.UTC).isoformat(),
        "candidate_id": result["candidate_id"],
        "verdict": verdict,
        "metrics": {
            "match_count": result["match_count"],
            "false_negative_count": result["false_negative_count"],
            "false_positive_count": result["false_positive_count"],
            "delta_vs_anchor": result["delta_vs_anchor"],
        },
        "controls": {
            "case_155": result["case_155"],
            "case_166": result["case_166"],
            "office_negative": result["office_negative"],
        },
        "dense_cases": result["dense_cases"],
        "preserve": preserve,
        "avoid": avoid,
        "next_axis": next_axis,
        "prior_candidate_count": len(prior_results),
    }


def _write_diagnosis(result: dict[str, Any], diagnosis: dict[str, Any]) -> None:
    json_path = DIAG_DIR / f"{result['candidate_id']}_diagnosis.json"
    md_path = DIAG_DIR / f"{result['candidate_id']}_diagnosis.md"
    _write_json(json_path, diagnosis)
    md = f"""# {result['candidate_id']} Diagnosis

Generated: `{diagnosis['generated_utc']}`

Verdict: `{diagnosis['verdict']}`

## Metrics

| Candidate | Matches | FNs | FPs | Delta vs v018e |
| --- | ---: | ---: | ---: | --- |
| `{result['candidate_id']}` | {result['match_count']} | {result['false_negative_count']} | {result['false_positive_count']} | {result['delta_vs_anchor']['match_count']} / {result['delta_vs_anchor']['false_negative_count']} / {result['delta_vs_anchor']['false_positive_count']} |

## Preserve

"""
    for item in diagnosis["preserve"]:
        md += f"- {item}\n"
    md += "\n## Avoid\n\n"
    for item in diagnosis["avoid"]:
        md += f"- {item}\n"
    md += f"\n## Next Axis\n\n{diagnosis['next_axis']}\n"
    md_path.write_text(md, encoding="utf-8")


def _rank_key(item: dict[str, Any]) -> tuple[Any, ...]:
    return (
        0 if item["disqualified"] else 1,
        1 if item["adoption_grade"] else 0,
        1 if item["strong_next_primary"] else 0,
        item["match_count"],
        -item["false_negative_count"],
        -item["false_positive_count"],
        item["dense_cases"]["67"]["match_count"],
        -item["dense_cases"]["67"]["false_positive_count"],
    )


def _rank_results(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(results, key=_rank_key, reverse=True)


def _run_candidate_once(candidate: Candidate, anchor: dict[str, Any]) -> dict[str, Any]:
    scratch: Path | None = None
    try:
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
        return _candidate_result(candidate, all_run, office_run, anchor=anchor)
    finally:
        if scratch is not None:
            cleanup = _remove_scratch(scratch)
            _write_json(RUNS_DIR / candidate.candidate_id / "scratch_cleanup.json", cleanup)


def _run_candidate_with_retry(
    candidate: Candidate,
    anchor: dict[str, Any],
    recovery_events: list[dict[str, Any]],
) -> dict[str, Any]:
    for attempt in (1, 2):
        try:
            print(f"\n=== Running {candidate.candidate_id} attempt {attempt} ===", flush=True)
            result = _run_candidate_once(candidate, anchor)
            if result["nonzero_command_count"] == 0 and not result["missing_outputs"]:
                if attempt > 1:
                    recovery_events.append(
                        {
                            "candidate_id": candidate.candidate_id,
                            "type": "runner_retry_recovered",
                            "attempt": attempt,
                        }
                    )
                return result
            recovery_events.append(
                {
                    "candidate_id": candidate.candidate_id,
                    "type": "runner_untrusted_attempt",
                    "attempt": attempt,
                    "nonzero_command_count": result["nonzero_command_count"],
                    "missing_outputs": result["missing_outputs"],
                }
            )
        except Exception as exc:
            recovery_events.append(
                {
                    "candidate_id": candidate.candidate_id,
                    "type": "candidate_exception",
                    "attempt": attempt,
                    "error": repr(exc),
                }
            )
        if attempt == 2:
            raise RuntimeError(f"{candidate.candidate_id}: repeated untrustworthy runner failure")
    raise AssertionError("unreachable")


def _anchor_stable(anchor: dict[str, Any]) -> bool:
    hist = HISTORICAL_BASELINES["v018e_historical_anchor"]
    return (
        abs(anchor["match_count"] - hist["match_count"]) <= 2
        and abs(anchor["false_negative_count"] - hist["false_negative_count"]) <= 2
        and abs(anchor["false_positive_count"] - hist["false_positive_count"]) <= 2
        and anchor["controls_pass"]
    )


def _write_registry(rows: list[dict[str, Any]]) -> None:
    payload = {
        "generated_utc": dt.datetime.now(dt.UTC).isoformat(),
        "cycle_id": "v019_v018e_creative_followup_cycle",
        "runtime_path": "upstream_main_code_ollama_openai_compat",
        "candidates": rows,
    }
    _write_json(PACKAGE_ROOT / "candidate_registry.json", payload)


def _write_source_manifest(manifest_checks: dict[str, Any], endpoint: dict[str, Any]) -> None:
    payload = {
        "generated_utc": dt.datetime.now(dt.UTC).isoformat(),
        "cycle_id": "v019_v018e_creative_followup_cycle",
        "purpose": "Sequential follow-up from v018e with adaptive prompt authoring.",
        "upstream_commit": UPSTREAM_COMMIT,
        "runtime_path": "current upstream/main code with Ollama OpenAI-compatible endpoint",
        "openai_base_url": OPENAI_BASE_URL,
        "model": MODEL,
        "manifest_checks": manifest_checks,
        "endpoint_check": endpoint,
        "source_artifacts": {
            "v018_final_recommendation": str(V018_ROOT / "final_recommendation.md"),
            "v018_comparison_matrix": str(V018_ROOT / "comparison_matrix.json"),
            "v018e_overlay": str(V018_ROOT / "overlays/v018e_contrastive_body_anchor.yaml"),
            "research_notes": str(PACKAGE_ROOT / "research_notes.md"),
        },
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


def _write_final_reports(
    *,
    anchor: dict[str, Any],
    anchor_attempts: list[dict[str, Any]],
    results: list[dict[str, Any]],
    registry_rows: list[dict[str, Any]],
    diagnoses: list[dict[str, Any]],
    recovery_events: list[dict[str, Any]],
    extra_triggered: bool,
) -> None:
    ranking = _rank_results(results)
    adoption = [item for item in ranking if item["adoption_grade"]]
    strong = [item for item in ranking if item["strong_next_primary"]]
    if adoption:
        verdict = "adoption_grade_winner_found"
        recommended = adoption[0]["candidate_id"]
    elif strong:
        verdict = "strong_next_primary_found"
        recommended = strong[0]["candidate_id"]
    elif ranking and not ranking[0]["disqualified"]:
        verdict = "learning_only_best_candidate"
        recommended = ranking[0]["candidate_id"]
    else:
        verdict = "no_candidate_recommended"
        recommended = None
    matrix = {
        "generated_utc": dt.datetime.now(dt.UTC).isoformat(),
        "cycle_id": "v019_v018e_creative_followup_cycle",
        "baselines": HISTORICAL_BASELINES,
        "fresh_v018e_anchor": anchor,
        "fresh_v018e_anchor_attempts": anchor_attempts,
        "results": results,
        "ranking": [item["candidate_id"] for item in ranking],
        "diagnoses": diagnoses,
        "candidate_registry": registry_rows,
        "extra_v019g_i_triggered": extra_triggered,
        "final_verdict": verdict,
        "recommended_candidate": recommended,
        "recovery_events": recovery_events,
    }
    _write_json(PACKAGE_ROOT / "comparison_matrix.json", matrix)
    _write_json(PACKAGE_ROOT / "final_recommendation.json", matrix)
    _write_json(PACKAGE_ROOT / "recovery_log.json", {"generated_utc": matrix["generated_utc"], "events": recovery_events})

    md = f"""# v019 v018e Creative Follow-Up Cycle

Generated: `{matrix['generated_utc']}`

## Fresh Anchor

| Anchor | Matches | FNs | FPs | Controls |
| --- | ---: | ---: | ---: | --- |
| `v018e_anchor_replay` | {anchor['match_count']} | {anchor['false_negative_count']} | {anchor['false_positive_count']} | {'pass' if anchor['controls_pass'] else 'fail'} |

## Candidate Results

| Rank | Candidate | Matches | FNs | FPs | `155` | `166` | Office | Verdict |
| ---: | --- | ---: | ---: | ---: | --- | --- | --- | --- |
"""
    for index, item in enumerate(ranking, start=1):
        if item["adoption_grade"]:
            row_verdict = "adoption-grade"
        elif item["strong_next_primary"]:
            row_verdict = "strong next-primary"
        elif item["disqualified"]:
            row_verdict = "disqualified"
        else:
            row_verdict = "learning-only"
        md += (
            f"| {index} | `{item['candidate_id']}` | {item['match_count']} | "
            f"{item['false_negative_count']} | {item['false_positive_count']} | "
            f"{item['case_155']['match_count']}m/{item['case_155']['false_negative_count']}fn/{item['case_155']['false_positive_count']}fp | "
            f"{item['case_166']['match_count']}m/{item['case_166']['false_negative_count']}fn/{item['case_166']['false_positive_count']}fp | "
            f"{'pass' if item['office_negative']['negative_scene_abstention_correct_count'] == 1 else 'fail'} | "
            f"{row_verdict} |\n"
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

Verdict: `{verdict}`.

Recommended candidate: `{recommended}`.

Conditional `v019g-i` triggered: `{extra_triggered}`.

Decision rule reminder:

- adoption-grade: `>173` matches, `<46` FNs, `<=22` raw FPs, controls pass
- strong next-primary: beats fresh `v018e` recall and reduces FPs below fresh
  `v018e`, controls pass
- learning-only: useful evidence but not adoption-ready

## Boundaries

No source reports, references, doctrine, runtime config adoption, commit, push,
Graphify refresh, or Mem0 write happened in this wave.
"""
    (PACKAGE_ROOT / "comparison_matrix.md").write_text(md, encoding="utf-8")
    (PACKAGE_ROOT / "final_recommendation.md").write_text(md, encoding="utf-8")


def _compile_python() -> None:
    result = _run(["python3", "-m", "py_compile", str(Path(__file__).resolve())], cwd=WORKTREE_ROOT)
    if result["returncode"] != 0:
        raise RuntimeError(result["stderr_tail"])


def _run_anchor(recovery_events: list[dict[str, Any]]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    prompt = _load_v018e_prompt()
    candidate = Candidate(
        "v018e_anchor_replay",
        "v018e Anchor Replay",
        "Fresh replay of v018e_contrastive_body_anchor.",
        prompt,
        ["v018e_contrastive_body_anchor"],
    )
    attempts: list[dict[str, Any]] = []
    for attempt in (1, 2):
        result = _run_candidate_with_retry(candidate, HISTORICAL_BASELINES["v018e_historical_anchor"], recovery_events)
        attempts.append(result)
        if _anchor_stable(result):
            return result, attempts
        recovery_events.append(
            {
                "candidate_id": "v018e_anchor_replay",
                "type": "anchor_drift",
                "attempt": attempt,
                "metrics": {
                    "match_count": result["match_count"],
                    "false_negative_count": result["false_negative_count"],
                    "false_positive_count": result["false_positive_count"],
                    "controls_pass": result["controls_pass"],
                },
            }
        )
    _write_json(PACKAGE_ROOT / "anchor_replay_drift.json", {"attempts": attempts})
    raise RuntimeError("v018e anchor replay drifted materially twice; stop before v019 scoring")


def main() -> int:
    PACKAGE_ROOT.mkdir(parents=True, exist_ok=True)
    OVERLAY_DIR.mkdir(parents=True, exist_ok=True)
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    DIAG_DIR.mkdir(parents=True, exist_ok=True)
    _compile_python()
    endpoint = _check_endpoint()
    manifest_checks = _validate_manifests()
    _write_source_manifest(manifest_checks, endpoint)
    recovery_events: list[dict[str, Any]] = []
    if endpoint["status"] != "available":
        recovery_events.append({"type": "endpoint_blocker", "endpoint": endpoint})
        _write_json(PACKAGE_ROOT / "recovery_log.json", {"events": recovery_events})
        print(f"Endpoint unavailable: {endpoint}", file=sys.stderr)
        return 2

    anchor, anchor_attempts = _run_anchor(recovery_events)
    results: list[dict[str, Any]] = []
    diagnoses: list[dict[str, Any]] = []
    registry_rows: list[dict[str, Any]] = [
        _create_overlay(
            Candidate(
                "v018e_anchor_replay",
                "v018e Anchor Replay",
                "Fresh replay of v018e_contrastive_body_anchor.",
                _load_v018e_prompt(),
                ["v018e_contrastive_body_anchor"],
            )
        )
    ]

    for generator in BASE_SEQUENCE:
        candidate = generator(results)
        registry_rows.append(_create_overlay(candidate))
        _write_registry(registry_rows)
        result = _run_candidate_with_retry(candidate, anchor, recovery_events)
        diagnosis = _diagnosis(result, results, anchor)
        _write_diagnosis(result, diagnosis)
        results.append(result)
        diagnoses.append(diagnosis)

    ranked_base = _rank_results(results)
    extra_triggered = (
        bool(ranked_base)
        and ranked_base[0]["candidate_id"] == "v019f_adversarial_box_jury"
        and (
            ranked_base[0]["adoption_grade"]
            or ranked_base[0]["strong_next_primary"]
        )
    )
    if extra_triggered:
        for generator in EXTRA_SEQUENCE:
            candidate = generator(results)
            registry_rows.append(_create_overlay(candidate))
            _write_registry(registry_rows)
            result = _run_candidate_with_retry(candidate, anchor, recovery_events)
            diagnosis = _diagnosis(result, results, anchor)
            _write_diagnosis(result, diagnosis)
            results.append(result)
            diagnoses.append(diagnosis)

    _write_registry(registry_rows)
    _write_final_reports(
        anchor=anchor,
        anchor_attempts=anchor_attempts,
        results=results,
        registry_rows=registry_rows,
        diagnoses=diagnoses,
        recovery_events=recovery_events,
        extra_triggered=extra_triggered,
    )
    print(PACKAGE_ROOT / "comparison_matrix.json")
    print(PACKAGE_ROOT / "final_recommendation.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
