#!/usr/bin/env python3
"""Run v037b after v037a failed the FP8 micro gate."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CORE_PATH = HERE / "run_v037_same_wreck_duplicate_guard.py"
spec = importlib.util.spec_from_file_location("v037_core", CORE_PATH)
core = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(core)


def create_v037b_overlay() -> Path:
    baseline = core.read_yaml(core.BASELINE_OVERLAY)
    prompt = baseline["overrides"]["prompts"]["detect_objects"]
    needle = (
        "- broad context or scene boxes whose strongest support is a row, blast area, road, debris field, "
        "smoke plume, or multiple uncertain fragments rather than one visible target body\n"
    )
    addition = "- second smaller box entirely inside another box for the same connected wreck/body\n"
    if addition.strip() in prompt:
        candidate_prompt = prompt
    else:
        candidate_prompt = prompt.replace(needle, needle + addition)
    candidate = dict(baseline)
    candidate["candidate_id"] = "v037b_fp8_same_wreck_inside_box_guard"
    candidate["title"] = "v037b fp8 same-wreck inside-box guard"
    candidate["overlay_id"] = "qwen-1.2-v037b_fp8_same_wreck_inside_box_guard"
    candidate["overlay_type"] = "fp8_vllm_same_wreck_duplicate_guard"
    candidate["description"] = "Narrow containment-only same-wreck duplicate guard after v037a reopened case-110 broad FPs."
    candidate["generated_from"] = ["v034a_fp8_broad_context_scene_box_guard", "v037a_fp8_same_wreck_duplicate_local_guard_failure"]
    candidate["intended_changes"] = [
        "Add one compact BAD FINAL BOX guard for a second smaller box entirely inside another box for the same connected wreck/body.",
        "Remove v037a's broader heavily-overlapping/whole-body wording.",
        "Preserve the v034a broad-context/scene-box guard.",
        "Preserve the v020c extra-box audit without weakening or removing it.",
    ]
    candidate["overrides"]["prompts"]["detect_objects"] = candidate_prompt
    candidate["overrides"]["runtime"] = {"notes": "Applied only inside upstream/main scratch config; no product adoption."}
    out = core.PACKAGE_ROOT / "overlays/v037b_fp8_same_wreck_inside_box_guard.yaml"
    core.write_yaml(out, candidate)
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args()
    if not args.run:
        parser.print_help()
        return 0

    core.create_sentinel_manifest()
    preflight = {
        "generated_at": core.utc_now(),
        "backend": core.BACKEND,
        "models": core.fetch_models(),
        "timeout_policy": {
            "per_case_timeout_seconds": core.REQUEST_TIMEOUT_SECONDS,
            "max_retries": core.MAX_RETRIES,
            "cooldown_seconds": core.RETRY_COOLDOWN_SECONDS,
        },
        "continuation_from": "v037a_micro_rejected",
    }
    core.write_json(core.PACKAGE_ROOT / "backend_preflight_v037b.json", preflight)
    if not preflight["models"]["ok"] or not preflight["models"]["model_present"]:
        raise RuntimeError("vLLM FP8 backend is not available.")

    overlay = create_v037b_overlay()
    candidate = {
        "candidate_id": "v037b_fp8_same_wreck_inside_box_guard",
        "overlay_path": str(overlay),
        "intended_changes": core.read_yaml(overlay).get("intended_changes", []),
    }

    micro = core.run_probe(candidate, core.SENTINEL_MANIFEST, "micro_pack_only")
    office = core.run_probe(candidate, core.OFFICE_NEGATIVE_MANIFEST, "office_negative_guard")
    office_ok = core.office_pass(office)
    micro_ok, micro_reason = core.micro_pass(micro, office_ok)
    records = {
        "candidate_micro": micro,
        "candidate_micro_office": office,
        "candidate_micro_office_status": "pass" if office_ok else "fail",
        "candidate_micro_status": "micro_pass" if micro_ok else "rejected",
    }
    if not micro_ok:
        core.print_candidate_block(
            micro,
            "micro_pack_only",
            "rejected",
            f"v037b failed the FP8 micro gate: {micro_reason}.",
            "Pivot away from prompt-only same-wreck duplicate suppression or inspect post-processing simulation.",
            office_ok,
        )
        core.write_json(core.PACKAGE_ROOT / "runs/v037b_continuation_summary.json", records)
        return 0

    core.print_candidate_block(
        micro,
        "micro_pack_only",
        "learning_evidence",
        "v037b passed the FP8 micro gate; full all-current is required.",
        "Run full all-current/no101 for v037b.",
        office_ok,
    )
    full = core.run_probe(candidate, core.ALL_CURRENT_MANIFEST, "full_all_current")
    full_office = core.run_probe(candidate, core.OFFICE_NEGATIVE_MANIFEST, "office_negative_guard")
    full_office_ok = core.office_pass(full_office)
    status = core.candidate_status(full, full_office_ok)
    records.update(
        {
            "candidate_full": full,
            "candidate_full_office": full_office,
            "candidate_full_office_status": "pass" if full_office_ok else "fail",
            "candidate_full_status": status,
        }
    )
    core.print_candidate_block(
        full,
        "full_all_current",
        status,
        "v037b completed full all-current on FP8 vLLM.",
        "Continue from v037b if it beats 63; otherwise pivot based on full-run deltas.",
        full_office_ok,
    )
    core.write_json(core.PACKAGE_ROOT / "runs/v037b_continuation_summary.json", records)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
