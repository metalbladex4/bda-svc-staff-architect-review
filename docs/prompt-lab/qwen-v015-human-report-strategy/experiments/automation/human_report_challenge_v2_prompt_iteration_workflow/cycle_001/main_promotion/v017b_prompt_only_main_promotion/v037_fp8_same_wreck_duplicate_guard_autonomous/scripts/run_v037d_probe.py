#!/usr/bin/env python3
"""Run v037d as a tiny case-84-oriented recall probe from v034a."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
CORE_PATH = HERE / "run_v037_same_wreck_duplicate_guard.py"
spec = importlib.util.spec_from_file_location("v037_core", CORE_PATH)
core = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(core)


def create_v037d_overlay() -> Path:
    baseline = core.read_yaml(core.BASELINE_OVERLAY)
    prompt = baseline["overrides"]["prompts"]["detect_objects"]
    needle = "- one connected target body, wreck body, or exterior building structure\n"
    addition = "- separable low-contrast damaged body\n"
    if addition.strip() in prompt:
        candidate_prompt = prompt
    else:
        candidate_prompt = prompt.replace(needle, needle + addition)
    candidate = dict(baseline)
    candidate["candidate_id"] = "v037d_fp8_low_contrast_body_recall_cue"
    candidate["title"] = "v037d fp8 low-contrast body recall cue"
    candidate["overlay_id"] = "qwen-1.2-v037d_fp8_low_contrast_body_recall_cue"
    candidate["overlay_type"] = "fp8_vllm_case84_recall_probe"
    candidate["description"] = "Tiny recall cue from v034a after same-wreck duplicate prompt clauses failed micro-gates."
    candidate["generated_from"] = [
        "v034a_fp8_broad_context_scene_box_guard",
        "v037_same_wreck_duplicate_axis_failed",
    ]
    candidate["intended_changes"] = [
        "Add one short GOOD FINAL BOX cue for a separable low-contrast damaged body.",
        "Target case-84-style FNs without adding broad recall language.",
        "Preserve the v034a broad-context/scene-box guard.",
        "Preserve the v020c extra-box audit without weakening or removing it.",
    ]
    candidate["overrides"]["prompts"]["detect_objects"] = candidate_prompt
    candidate["overrides"]["runtime"] = {"notes": "Applied only inside upstream/main scratch config; no product adoption."}
    out = core.PACKAGE_ROOT / "overlays/v037d_fp8_low_contrast_body_recall_cue.yaml"
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
        "continuation_from": "v037_same_wreck_axis_failed",
    }
    core.write_json(core.PACKAGE_ROOT / "backend_preflight_v037d.json", preflight)
    if not preflight["models"]["ok"] or not preflight["models"]["model_present"]:
        raise RuntimeError("vLLM FP8 backend is not available.")

    overlay = create_v037d_overlay()
    candidate = {
        "candidate_id": "v037d_fp8_low_contrast_body_recall_cue",
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
        status = "runtime_invalid" if micro_reason == "runtime_invalid" else "rejected"
        core.print_candidate_block(
            micro,
            "micro_pack_only",
            status,
            f"v037d failed the FP8 micro gate: {micro_reason}.",
            "Stop v037 and plan visual/post-processing work before more prompt clauses.",
            office_ok,
        )
        core.write_json(core.PACKAGE_ROOT / "runs/v037d_continuation_summary.json", records)
        return 0

    core.print_candidate_block(
        micro,
        "micro_pack_only",
        "learning_evidence",
        "v037d passed the FP8 micro gate; full all-current is required.",
        "Run full all-current/no101 for v037d.",
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
        "v037d completed full all-current on FP8 vLLM.",
        "Continue from v037d if it beats 63; otherwise stop and inspect remaining deltas visually.",
        full_office_ok,
    )
    core.write_json(core.PACKAGE_ROOT / "runs/v037d_continuation_summary.json", records)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
