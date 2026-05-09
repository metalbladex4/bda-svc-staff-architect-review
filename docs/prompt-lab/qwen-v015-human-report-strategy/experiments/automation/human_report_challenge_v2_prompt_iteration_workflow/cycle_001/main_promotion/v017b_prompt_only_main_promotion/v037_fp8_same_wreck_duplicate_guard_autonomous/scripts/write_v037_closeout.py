#!/usr/bin/env python3
"""Write the v037 closeout package from recorded run summaries."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def utc_now() -> str:
    return dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def stamp() -> str:
    return dt.datetime.now(dt.UTC).strftime("%Y%m%dT%H%M%SZ")


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def first_summary(pattern: str) -> dict:
    paths = sorted(ROOT.glob(pattern))
    if not paths:
        raise FileNotFoundError(pattern)
    return read_json(paths[0])


def metric_str(row: dict) -> str:
    m = row["metrics"]
    if m.get("combined_errors") is None:
        return "n/a"
    return f"{m.get('matches')}/{m.get('false_negatives')}/{m.get('false_positives')}/{m.get('combined_errors')}"


def md_num(value: object) -> object:
    return "n/a" if value is None else value


def make_row(
    candidate_id: str,
    stage: str,
    metrics: dict,
    status: str,
    case_metrics: dict | None = None,
    office: str = "n/a",
    note: str = "",
    hashes: dict | None = None,
) -> dict:
    return {
        "candidate_id": candidate_id,
        "stage": stage,
        "metrics": metrics,
        "case_66": (case_metrics or {}).get("66", "n/a"),
        "case_67": (case_metrics or {}).get("67", "n/a"),
        "case_84": (case_metrics or {}).get("84", "n/a"),
        "case_97": (case_metrics or {}).get("97", "n/a"),
        "case_110": (case_metrics or {}).get("110", "n/a"),
        "case_155": (case_metrics or {}).get("155", "n/a"),
        "case_166": (case_metrics or {}).get("166", "n/a"),
        "office_negative": office,
        "status": status,
        "note": note,
        "hashes": hashes or {},
    }


def hashes(record: dict) -> dict:
    return {
        "rendered_prompt_hash": record.get("rendered_prompt_hash"),
        "request_shape_hash": record.get("request_shape_hash"),
        "raw_response_hash": record.get("raw_response_hash"),
        "response_trace_captured": record.get("response_trace_captured"),
    }


def continuation(path: str) -> dict:
    return read_json(ROOT / path)["candidate_micro"]


def office_status(path: str) -> str:
    payload = read_json(ROOT / path)
    return payload.get("candidate_micro_office_status") or "n/a"


def main() -> int:
    generated_at = utc_now()
    baseline = first_summary("runs/v037_baseline_exact_v034a_replay/micro_pack_only/*/v037_run_summary.json")
    v037a = first_summary("runs/v037a_fp8_same_wreck_duplicate_local_guard/micro_pack_only/*/v037_run_summary.json")
    v037b = continuation("runs/v037b_continuation_summary.json")
    v037c = continuation("runs/v037c_continuation_summary.json")
    v037d = continuation("runs/v037d_continuation_summary.json")

    rows = [
        make_row(
            "v020c_old_product_reference",
            "prior_all_current",
            {"matches": 186, "false_negatives": 33, "false_positives": 25, "combined_errors": 58, "image_count": 117},
            "old_product_reference_not_fp8_replacement",
            note="Prior non-FP8 product-reference evidence only.",
        ),
        make_row(
            "v020c_fp8_vllm_baseline",
            "v031_full_all_current",
            {"matches": 180, "false_negatives": 39, "false_positives": 32, "combined_errors": 71, "image_count": 117},
            "fp8_baseline",
        ),
        make_row(
            "v032d_fp8_v019c_anchor_replay",
            "v033_clean_full",
            {"matches": 185, "false_negatives": 34, "false_positives": 57, "combined_errors": 91, "image_count": 117},
            "rejected",
            {"67": "8/3/2", "110": "3/4/32", "155": "2/0/0", "166": "1/0/0"},
            "pass",
            "Fixed case 155 but exploded FPs, especially case 110.",
        ),
        make_row(
            "v034a_fp8_broad_context_scene_box_guard",
            "v034_full_all_current",
            {"matches": 181, "false_negatives": 38, "false_positives": 25, "combined_errors": 63, "image_count": 117},
            "fp8_working_best",
            {"66": "8/0/5", "67": "10/1/3", "84": "8/5/0", "97": "1/0/1", "110": "3/4/1", "155": "2/0/1", "166": "1/0/0"},
            "pass",
        ),
        make_row(
            baseline["candidate_id"],
            "v037_baseline_micro",
            baseline["metrics"],
            "baseline_replay",
            baseline["case_metrics"],
            "pass",
            "Exact v034a replay before v037 prompt mutations.",
            hashes(baseline),
        ),
        make_row(
            v037a["candidate_id"],
            "micro_pack_only",
            v037a["metrics"],
            "rejected",
            v037a["case_metrics"],
            "pass",
            "Case 155 improved to 2/0/0 but case 110 exploded to 16 FPs and case 66 worsened.",
            hashes(v037a),
        ),
        make_row(
            v037b["candidate_id"],
            "micro_pack_only",
            v037b["metrics"],
            "runtime_invalid",
            v037b["case_metrics"],
            office_status("runs/v037b_continuation_summary.json"),
            "Case 110 hit the 4096-token context cap after three attempts.",
            hashes(v037b),
        ),
        make_row(
            v037c["candidate_id"],
            "micro_pack_only",
            v037c["metrics"],
            "rejected",
            v037c["case_metrics"],
            office_status("runs/v037c_continuation_summary.json"),
            "Shortened same-wreck wording avoided runtime failure but did not improve case 155 and worsened case 66.",
            hashes(v037c),
        ),
        make_row(
            v037d["candidate_id"],
            "micro_pack_only",
            v037d["metrics"],
            "rejected",
            v037d["case_metrics"],
            office_status("runs/v037d_continuation_summary.json"),
            "Low-contrast recall cue fixed case 155 but did not improve case 84 and worsened dense precision.",
            hashes(v037d),
        ),
    ]

    write_json(ROOT / "comparison_matrix.json", {"generated_at": generated_at, "rows": rows})
    matrix_lines = [
        "# v037 Comparison Matrix",
        "",
        "| Candidate | Stage | Metrics | Case 66 | Case 67 | Case 84 | Case 97 | Case 110 | Case 155 | Case 166 | Office | Status | Note |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for row in rows:
        matrix_lines.append(
            f"| `{row['candidate_id']}` | {row['stage']} | `{metric_str(row)}` | `{row['case_66']}` | `{row['case_67']}` | `{row['case_84']}` | `{row['case_97']}` | `{row['case_110']}` | `{row['case_155']}` | `{row['case_166']}` | {row['office_negative']} | {row['status']} | {row['note']} |"
        )
    (ROOT / "comparison_matrix.md").write_text("\n".join(matrix_lines) + "\n", encoding="utf-8")

    write_json(ROOT / "candidate_registry.json", {"generated_at": generated_at, "candidates": rows})
    live_lines = ["# v037 Live Metrics Log", ""]
    for row in rows:
        live_lines.append(f"- `{row['candidate_id']}` `{row['stage']}`: `{metric_str(row)}` status `{row['status']}`.")
    (ROOT / "live_metrics_log.md").write_text("\n".join(live_lines) + "\n", encoding="utf-8")

    lessons = [
        "# v037 Lessons Learned",
        "",
        "- v034a remains the FP8 working best at `181 / 38 / 25 / 63`.",
        "- v037a isolated the case-155 same-wreck duplicate (`2/0/0`) but reopened broad FPs, especially case 110 (`2/5/16`).",
        "- v037b proved the vLLM FP8 4096-token context cap is still a practical prompt-length constraint; case 110 reached 4097 input tokens.",
        "- v037c showed that an ultra-short same-wreck duplicate cue can avoid runtime failure, but it did not improve case 155 and still worsened case 66.",
        "- v037d showed a tiny recall cue can improve case 155, but it did not recover case 84 and worsened cases 66/67.",
        "- The same-wreck duplicate benefit is real but appears better tested through post-processing or visual/eval simulation than another prompt clause.",
        "- Do not reuse v037a/v037d wording families unless a non-prompt simulation proves the dense-row risk can be separated.",
    ]
    (ROOT / "lessons_learned.md").write_text("\n".join(lessons) + "\n", encoding="utf-8")

    strategy = [
        "# v037 Strategy State",
        "",
        "- Current FP8 working best: `v034a_fp8_broad_context_scene_box_guard`.",
        "- Working-best metrics: `181 / 38 / 25 / 63`.",
        "- v037 did not produce a new FP8 working best.",
        "- Same-wreck duplicate prompt clauses are paused after repeated dense-case regressions and one context-cap failure.",
        "- Next planned axis: inspect post-processing duplicate suppression or visual/eval simulation for same-wreck nested duplicates before authoring more prompt wording.",
        "- FP8 remains a separate model line and is not a product replacement.",
    ]
    (ROOT / "strategy_state.md").write_text("\n".join(strategy) + "\n", encoding="utf-8")

    recovery = [
        "# v037 Recovery Log",
        "",
        "- Re-grounded in v036 synthesis, v035/v034 closeouts, and v033 timeout policy.",
        "- Recovered and used the vLLM FP8 backend on `http://localhost:8000/v1`.",
        "- Applied the v033 experiment-only retry policy: 180-second request timeout, max 2 retries, 5-second cooldown.",
        "- Replayed exact v034a sentinel before candidate work.",
        "- Ran v037a, v037b, v037c, and v037d one at a time.",
        "- Stopped semantic prompt iteration after repeated micro-gate failures rather than scoring partial or unsafe evidence.",
    ]
    (ROOT / "recovery_log.md").write_text("\n".join(recovery) + "\n", encoding="utf-8")
    write_json(
        ROOT / "recovery_log.json",
        {
            "generated_at": generated_at,
            "backend": "vllm_qwen3vl_8b_fp8",
            "timeout_policy": {"per_request_seconds": 180, "max_retries": 2, "cooldown_seconds": 5},
            "events": recovery[2:],
            "hard_boundaries_preserved": True,
        },
    )

    final_payload = {
        "generated_at": generated_at,
        "status": "stopped_no_new_fp8_working_best",
        "best_fp8_candidate": "v034a_fp8_broad_context_scene_box_guard",
        "best_fp8_metrics": {"matches": 181, "false_negatives": 38, "false_positives": 25, "combined_errors": 63},
        "beat_v034a_63": False,
        "beat_fp8_baseline_71": True,
        "reached_or_beat_old_v020c_58": False,
        "target_le_1_reached": False,
        "case_66_67_84_97_summary": {
            "v034a": {"66": "8/0/5", "67": "10/1/3", "84": "8/5/0", "97": "1/0/1"},
            "v037a": {k: v037a["case_metrics"][k] for k in ["66", "67", "84", "97"]},
            "v037c": {k: v037c["case_metrics"][k] for k in ["66", "67", "84", "97"]},
            "v037d": {k: v037d["case_metrics"][k] for k in ["66", "67", "84", "97"]},
        },
        "case_110_summary": {
            "v034a": "3/4/1",
            "v037a": v037a["case_metrics"]["110"],
            "v037b": "runtime_invalid_context_cap_4097_input_tokens",
            "v037c": v037c["case_metrics"]["110"],
            "v037d": v037d["case_metrics"]["110"],
        },
        "controls_summary": {
            "v034a": {"155": "2/0/1", "166": "1/0/0", "office": "pass"},
            "v037a": {"155": v037a["case_metrics"]["155"], "166": v037a["case_metrics"]["166"], "office": "pass"},
            "v037c": {"155": v037c["case_metrics"]["155"], "166": v037c["case_metrics"]["166"], "office": office_status("runs/v037c_continuation_summary.json")},
            "v037d": {"155": v037d["case_metrics"]["155"], "166": v037d["case_metrics"]["166"], "office": office_status("runs/v037d_continuation_summary.json")},
        },
        "fp8_should_continue_as_separate_model_line": True,
        "recommended_next_axis": "Non-prompt visual/eval simulation of same-wreck duplicate suppression before further prompt wording.",
        "hard_boundaries_preserved": True,
    }
    write_json(ROOT / "final_recommendation.json", final_payload)
    final_md = [
        "# v037 Final Recommendation",
        "",
        f"Generated: `{generated_at}`",
        "",
        "Status: `stopped_no_new_fp8_working_best`.",
        "",
        "Best FP8 candidate remains `v034a_fp8_broad_context_scene_box_guard = 181 / 38 / 25 / 63`.",
        "",
        "No v037 candidate beat v034a's 63 combined errors. No v037 candidate reached or beat the old 58-error reference, and the <=1 target was not reached.",
        "",
        "Candidate outcomes:",
        "- `v037a_fp8_same_wreck_duplicate_local_guard`: rejected at micro-pack, `41 / 15 / 30 / 45`; case 155 improved to `2/0/0`, but case 110 exploded to `2/5/16` and case 66 worsened to `8/0/6`.",
        "- `v037b_fp8_same_wreck_inside_box_guard`: runtime invalid; case 110 exceeded the 4096-token context cap at 4097 input tokens on all three attempts.",
        "- `v037c_fp8_same_wreck_inner_duplicate_guard`: rejected at micro-pack, `43 / 13 / 17 / 30`; case 110 stayed controlled, but case 155 stayed `2/0/1` and case 66 worsened to `8/0/6`.",
        "- `v037d_fp8_low_contrast_body_recall_cue`: rejected at micro-pack, `42 / 14 / 18 / 32`; case 155 improved to `2/0/0`, but case 84 did not improve and dense precision regressed (`66 = 8/0/7`, `67 = 8/3/6`).",
        "",
        "Recommendation: keep FP8 as a separate model line, but pause further prompt clauses from this family. The next safe move is a non-prompt visual/eval simulation of same-wreck duplicate suppression, then only return to prompt wording if that simulation proves the case-155 duplicate class can be separated from dense valid rows.",
        "",
        "Hard boundaries were preserved: no promotion, no product config/doctrine/assessment/runtime/eval-ground-truth mutation, no v024o scored evidence, no FP8 product-replacement claim, and no secrets copied.",
    ]
    (ROOT / "final_recommendation.md").write_text("\n".join(final_md) + "\n", encoding="utf-8")

    diagnoses = {
        "v037b_fp8_same_wreck_inside_box_guard_diagnosis.md": [
            "# v037b Diagnosis",
            "",
            "What did this candidate test? A narrower containment-only same-wreck duplicate guard after v037a's broader wording reopened FPs.",
            "",
            "What changed from current FP8 working best? One BAD FINAL BOX line was added from v034a: `second smaller box entirely inside another box for the same connected wreck/body`.",
            "",
            "Result: runtime invalid. Case 110 failed all three attempts with a vLLM BadRequestError because the request reached 4097 input tokens against a 4096-token context cap.",
            "",
            "Lesson: the FP8 vLLM surface remains mechanically stable, but prompt-length margin is thin on case 110. Longer clauses are risky even before semantic quality is evaluated.",
        ],
        "v037c_fp8_same_wreck_inner_duplicate_guard_diagnosis.md": [
            "# v037c Diagnosis",
            "",
            "What did this candidate test? An ultra-short same-wreck duplicate cue intended to avoid v037b's context overflow.",
            "",
            "What changed from current FP8 working best? One BAD FINAL BOX line was added from v034a: `inner duplicate of the same wreck/body`.",
            "",
            f"Micro-pack result: `{metric_str(rows[7])}`.",
            "",
            "What improved? Runtime recovered and case 110 stayed controlled at `3/4/1`.",
            "",
            "What regressed? Case 66 worsened to `8/0/6`, causing micro-gate failure. Case 155 stayed at `2/0/1`, so the intended local duplicate benefit did not appear.",
            "",
            "Lesson: very short same-wreck wording is runtime-safe but not enough to isolate the case-155 duplicate class.",
        ],
        "v037d_fp8_low_contrast_body_recall_cue_diagnosis.md": [
            "# v037d Diagnosis",
            "",
            "What did this candidate test? A tiny case-84-oriented recall cue after same-wreck duplicate clauses failed.",
            "",
            "What changed from current FP8 working best? One GOOD FINAL BOX line was added from v034a: `separable low-contrast damaged body`.",
            "",
            f"Micro-pack result: `{metric_str(rows[8])}`.",
            "",
            "What improved? Case 155 improved to `2/0/0`, and case 110 stayed controlled at `3/4/1`.",
            "",
            "What regressed? Case 84 did not improve (`8/5/0`), case 66 worsened to `8/0/7`, and case 67 worsened to `8/3/6`.",
            "",
            "Lesson: compact recall wording can still push FP8 toward dense-row over-inclusion without recovering the intended recall pocket.",
        ],
    }
    for filename, lines in diagnoses.items():
        (ROOT / "diagnoses" / filename).write_text("\n".join(lines) + "\n", encoding="utf-8")

    pause = [
        "# v037 Pause Report",
        "",
        f"Generated: `{generated_at}`",
        "",
        "Reason: semantic prompt iteration paused after repeated micro-gate failures in the v037 prompt family.",
        "",
        "Last completed candidate: `v037d_fp8_low_contrast_body_recall_cue`.",
        "",
        "Current FP8 working best: `v034a_fp8_broad_context_scene_box_guard = 181 / 38 / 25 / 63`.",
        "",
        "Next planned axis: non-prompt visual/eval simulation of same-wreck duplicate suppression, especially the case-155 nested duplicate class, before any further prompt wording.",
        "",
        "Resume command for evidence review:",
        "",
        "```bash",
        "cd /home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement",
        "python3 docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v037_fp8_same_wreck_duplicate_guard_autonomous/scripts/write_v037_closeout.py",
        "```",
    ]
    (ROOT / f"pause_report_{stamp()}.md").write_text("\n".join(pause) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
