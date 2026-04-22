# Vision Language Models for Battle Damage Assessment

## User Guide

*Working Draft aligned to `origin/main` as of 17 April 2026*

## Drafting Scope Note

This working draft is written for future users of the stable `bda-svc` system on
`origin/main`. It is intentionally operator-first, CLI-focused, and limited to
the merged implementation. It does not describe prompt-lab workflows, local
worktree experiments, or unmerged model-development branches.

# Introduction

The Autonomous Battle Damage Assessment project is a research-focused software
system that analyzes post-strike imagery and produces structured Phase 1
physical damage assessments. In the current stable implementation, the system
operates as a local command-line application named `bda-svc`. It uses locally
served vision-language models (VLMs) through Ollama to detect relevant targets,
assess visible physical damage, and generate a JSON report for each processed
image. In the current stable path on `origin/main`, the system is centered on
doctrinal assessment of `buildings` and `military_equipment` and is intended to
run locally rather than through an external cloud inference service.

This User Guide is intended for future users who need to run the system,
understand what data it expects, and interpret the reports it produces. The
guide is written for operators and technically capable teammates who may not
have built the software themselves, so it focuses on practical usage, system
behavior, and output interpretation rather than internal prompt-engineering or
experimental model-comparison workflows.

# System Overview

## High-Level Architecture

At a high level, the stable system follows a local image-to-report workflow.
The user supplies either a single image or a folder of images to the `bda-svc`
CLI. The application validates the input path, loads the current pipeline
configuration and doctrine, and sends the image data to a locally running
Ollama model server. The pipeline then performs full-scene target detection,
creates buffered crops for each detection, runs per-target physical damage
assessment using both scene context and target crops, and produces a short
scene summary before exporting a structured JSON report to the selected output
directory.

The major components are the CLI entry point, the pipeline orchestration layer,
the doctrine and configuration files, the Ollama-served VLM backend, and the
JSON export layer. In practical terms, the operator interacts only with the CLI
and the input/output folders, while the pipeline manages model calls and report
generation internally. If a reusable architecture figure is needed later, the
best candidate is the Phase 3 model-architecture figure, but it should only be
reused if it still matches the stable `origin/main` implementation.

## Machine Learning Models

The current stable implementation uses locally served vision-language models in
a zero-shot configuration. This means the deployed system relies on pretrained
models and prompt/configuration control rather than custom fine-tuning. On
`origin/main`, the stable configuration currently uses the Ollama model tag
`qwen3-vl:8b-instruct` for both the detection and assessment roles, although
those roles remain logically separate within the pipeline and can be configured
independently in the pipeline configuration.

In the stable system, the detection role identifies doctrinally relevant
targets and produces bounding boxes, while the assessment role evaluates the
visible physical damage for each detected target and contributes to the final
scene-level summary. The key practical capabilities are local inference through
Ollama, structured JSON output, doctrinally guided physical-damage
classification, and timestamped report generation that avoids overwriting prior
results. In the current stable doctrine on `main`, the system is configured to
reason about `buildings` and `military_equipment`.

# Using the System

## Input Data Requirements

The system accepts image files as input. In the current implementation, valid
file extensions are `.png`, `.jpg`, `.jpeg`, and `.bmp`. A user may provide
either a single image file or a directory containing multiple supported images.
If a directory is used, the application recursively searches for valid image
files and processes them in sorted order.

If no input path is provided on the command line, `bda-svc` uses the
environment variable `BDA_INPUT` when it is set; otherwise it defaults to the
local folder `./bda_input`. No separate preprocessing step is required from the
operator beyond supplying accessible image files in a supported format, but the
selected input path must exist and contain valid images. The stable system is
designed for still-image analysis and does not currently present itself as a
video-ingestion or multi-sensor pipeline in normal user operation. If the input
path is invalid or contains no supported image files, the application exits
with an error instead of silently continuing.

## Model Invocation

Before running the system locally, the operator should have a working Python
environment managed with `uv`, a running Ollama service, and the configured
model available in Ollama. In the stable path, a normal local setup is:

```bash
uv sync
ollama serve
ollama pull qwen3-vl:8b-instruct
```

Once the environment is ready, the system can be invoked through the CLI. The
most common commands are:

```bash
uv run bda-svc -h
uv run bda-svc
uv run bda-svc -i /path/to/image.jpg
uv run bda-svc -i /path/to/folder
uv run bda-svc -i /path/to/folder -o /path/to/output
```

The `-i` / `--input` option selects the input image or folder, and the
`-o` / `--output` option selects the output folder. If the Ollama server is not
reachable at the default local endpoint, the operator can point the application
to a different Ollama host by setting `OLLAMA_HOST` before invocation, for
example:

```bash
OLLAMA_HOST=http://<host>:<port> uv run bda-svc -i /path/to/image.jpg
```

The application and the model server are separate runtime pieces: `bda-svc`
provides the CLI and pipeline logic, while Ollama hosts the configured model.
That means the operator should think of a successful run as requiring both the
local Python environment and a reachable Ollama model endpoint.

## Output Interpretation

The system writes one timestamped JSON report per processed image. If no output
path is supplied, reports are written to `./bda_output`. Timestamped filenames
are used so repeated runs do not overwrite previous outputs. Each exported
report contains three top-level sections: `metadata`, `physical_damage`, and
`summary`.

The `metadata` section records contextual information such as the model name,
image filename, creation timestamp, analyst label, report type, and inference
time. The `physical_damage` section contains one entry per assessed target,
typically keyed by a target identifier such as `target_0`. Each target entry
contains a `target_type`, `damage_category`, `confidence_level`,
`brief_supporting_logic`, and `bounding_box`. In the current stable
implementation, the `bounding_box` is represented as a four-value list in the
form `[xmin, ymin, xmax, ymax]`. The `summary` field provides a short
scene-level description that remains consistent with the target-level
assessments.

A simplified example is shown below:

```json
{
  "metadata": {
    "model_name": "detection=qwen3-vl:8b-instruct;assessment=qwen3-vl:8b-instruct",
    "image_filename": "example.jpg",
    "report_type": "PDA",
    "analyst": "bda-svc",
    "inference_time": "12.34"
  },
  "physical_damage": {
    "target_0": {
      "target_type": "military_equipment",
      "damage_category": "DESTROYED",
      "confidence_level": "PROBABLE",
      "brief_supporting_logic": "visible fire and heavy structural damage",
      "bounding_box": [73, 79, 113, 122]
    }
  },
  "summary": "One target assessed and reported as destroyed."
}
```

When interpreting results, operators should treat `damage_category` as the main
statement of visible physical condition, `confidence_level` as the model's
strength of evidence, and `brief_supporting_logic` as the short explanation of
what visual cues supported the assessment. The output is intended to assist
review and downstream integration, not to replace human judgment in ambiguous
cases. If the system finds no relevant targets, it still returns a valid
`physical_damage` entry using `target_type: "object_not_found"`,
`damage_category: "NOT APPLICABLE"`, and a zero bounding box so downstream
consumers still receive a structurally consistent report.

# Deployment and Integration

The final version of this section should stay centered on the stable deployment
paths already documented in the completed Phase 3 deployment procedure. The two
main user-relevant paths are local CLI execution from a repository checkout and
container-compatible execution using the repository Dockerfile. This section
should not describe branch-local experimentation or prompt-lab workflows.

The final write-up should explain prerequisites, local Ollama assumptions, and
how the JSON outputs can be consumed by downstream systems or stored for later
analysis. If integration examples are added, they should focus on stable file
inputs/outputs and the CLI workflow rather than on unmerged APIs or
experimental evaluation tooling.

# Monitoring and Maintenance

The final version of this section should connect the User Guide to the separate
Phase 4 Maintenance and Monitoring Plan while staying understandable for a
future operator. The most relevant operator-facing topics are likely model
availability, configuration changes, dependency updates, rerunning local
validation after changes, and keeping output/report locations organized.

This section should also point readers to the deeper maintenance document
instead of trying to duplicate every long-term operational procedure inside the
User Guide itself. The User Guide should summarize responsibilities and common
maintenance touchpoints, while the maintenance plan should hold the full policy
detail.

# Troubleshooting and Support

The final version of this section should focus on common user-visible issues in
the stable system. The highest-priority troubleshooting topics are likely:

- input path does not exist
- selected folder contains no valid images
- Ollama is not running or the configured model is unavailable
- outputs are not appearing in the expected directory

Support guidance should point users toward the project README, the stable
configuration files, and the project team or maintainer workflow for reporting
issues. If this section remains optional in the final submission, it can still
be prepared as a short practical appendix or support note for your partner.

# Appendices

The appendices are the right place for reusable support material that would
clutter the main operator narrative. The most useful appendix candidates are:

- glossary of BDA and system terms
- sample command list
- sample JSON output fragment
- reference list to prior deliverables and stable repo docs

If space is limited in the submission version, the glossary and command summary
should take priority because they provide the most direct operator value.
