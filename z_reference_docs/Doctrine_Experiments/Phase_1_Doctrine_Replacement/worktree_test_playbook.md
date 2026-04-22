# Worktree Test Playbook

This is the local execution playbook for the doctrine replacement experiment.

## Testbeds

### Qwen doctrine branch

- branch: `feat/qwen3-vl-8b-instruct/doctrine-bda-alignment`
- worktree:
  `/home/williambenitez1/Capstone_worktrees/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment`

### Gemma doctrine branch

- branch: `feat/gemma4-e4b/doctrine-bda-alignment`
- worktree:
  `/home/williambenitez1/Capstone_worktrees/3.2_feat__gemma4-e4b__doctrine-bda-alignment`
- host override:
  `OLLAMA_HOST=http://127.0.0.1:11435`

## Round-One Static Checks

Run these first in each doctrine worktree:

```bash
uv run pytest tests/unit/test_yamls.py tests/unit/test_utilities.py
```

Purpose:

- confirm that the candidate doctrine still satisfies the runtime schema
- confirm that doctrine formatting helpers still behave normally

## Doctrine-Sensitive Guard Set

Use this six-case set first:

1. `destroyed_building4`
2. `operational_building7`
3. `tank_pressure`
4. `operational_tank4`
5. `destroyed_tank15`
6. `office_negative`

Interpretation:

- buildings test severity framing and section-versus-whole-building logic
- tanks test that equipment behavior is preserved
- office negative tests that doctrine wording does not widen detection

## Runtime Execution Pattern

### Qwen

Use the doctrine branch worktree and save outputs under the new doctrine lab
root:

```bash
uv run bda-svc --input <image-or-folder> --output <run-output-dir>
```

### Gemma

Use the Gemma doctrine branch worktree and the local Gemma host:

```bash
OLLAMA_HOST=http://127.0.0.1:11435 uv run bda-svc --input <image-or-folder> --output <run-output-dir>
```

## Evaluation Pattern

Compare:

- parent active feature branch outputs using current doctrine
- doctrine branch outputs using candidate doctrine

Use `bda_eval` exactly as in the active prompt-lab workflow:

```bash
uv run python bda_eval/main.py -r <reference-report-dir> -p <predicted-report-dir> -i <image-dir> -o <eval-output-dir>
```

Review:

- output JSONs
- bbox overlays
- crops
- `bbox_review_sheet.jpg`
- evaluation CSVs

## Go / No-Go Rule

Only continue to full inherited comparison runs if the guard set shows:

- no contract break
- no obvious reopening of equipment or negative-control failures
- either improved building-severity behavior or a cleaner doctrinal tradeoff
