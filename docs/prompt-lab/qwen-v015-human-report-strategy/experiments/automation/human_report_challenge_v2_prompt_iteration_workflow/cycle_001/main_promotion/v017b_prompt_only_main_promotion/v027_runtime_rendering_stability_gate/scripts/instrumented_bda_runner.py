#!/usr/bin/env python3
"""Scratch-only instrumented BDA runner for v027 stability probes.

This script is executed from an isolated upstream/main scratch worktree. It
monkeypatches only the in-process detection/rendering and OpenAI-compatible
request call path so v027 can retain prompt rendering, request-shape, image
serialization, response, JSON repair, validation, and filtering evidence.
"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import difflib
import hashlib
import importlib.metadata as importlib_metadata
import io
import json
import os
import platform
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import yaml
from PIL import Image


TRACE_CONTEXT: dict[str, Any] = {"call_traces": [], "active_call_kind": None}


def _utc_now() -> str:
    return dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_text(text: str) -> str:
    return _sha256_bytes(text.encode("utf-8"))


def _file_sha256(path: Path) -> str | None:
    if not path.exists():
        return None
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _canonical_json(data: Any) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), default=str)


def _canonical_hash(data: Any) -> str:
    return _sha256_text(_canonical_json(data))


def _read_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def _extract_detect_prompt(path: Path) -> str:
    payload = _read_yaml(path)
    if "overrides" in payload:
        return payload["overrides"]["prompts"]["detect_objects"]
    return payload["prompts"]["detect_objects"]


def _unified_diff(a: str, b: str, a_label: str, b_label: str) -> str:
    return "".join(
        difflib.unified_diff(
            a.splitlines(keepends=True),
            b.splitlines(keepends=True),
            fromfile=a_label,
            tofile=b_label,
        )
    )


def _run(cmd: list[str], cwd: Path | None = None) -> dict[str, Any]:
    try:
        proc = subprocess.run(
            cmd,
            cwd=cwd,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return {
            "cmd": cmd,
            "cwd": str(cwd) if cwd else None,
            "returncode": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
        }
    except Exception as exc:  # pragma: no cover - defensive trace capture
        return {
            "cmd": cmd,
            "cwd": str(cwd) if cwd else None,
            "returncode": None,
            "error": repr(exc),
        }


def _png_bytes(image: Image.Image) -> bytes:
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    return buf.getvalue()


def _version(package: str) -> str | None:
    try:
        return importlib_metadata.version(package)
    except Exception:
        return None


def _make_instrumented_generate() -> Any:
    def instrumented_generate(
        self: Any,
        image: Image.Image | list[Image.Image],
        prompt: str,
        system_prompt: str | None = None,
        format_schema: dict | None = None,
        temperature: float | None = None,
    ) -> str:
        messages: list[dict[str, Any]] = []
        role_sequence: list[str] = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
            role_sequence.append("system")

        image_list = image if isinstance(image, list) else [image]
        user_content: list[dict[str, Any]] = [{"type": "text", "text": prompt}]
        image_trace: list[dict[str, Any]] = []

        for idx, img in enumerate(image_list):
            png = _png_bytes(img)
            b64 = base64.b64encode(png).decode("utf-8")
            image_trace.append(
                {
                    "index": idx,
                    "size": list(img.size),
                    "mode": img.mode,
                    "resized_png_byte_sha256": _sha256_bytes(png),
                    "base64_image_payload_sha256": _sha256_text(b64),
                    "png_byte_length": len(png),
                }
            )
            user_content.append(
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{b64}"},
                }
            )

        messages.append({"role": "user", "content": user_content})
        role_sequence.append("user")

        request_kwargs: dict[str, Any] = {"model": self.model, "messages": messages}
        response_format = None
        if format_schema is not None:
            response_format = {
                "type": "json_schema",
                "json_schema": {"name": "response", "schema": format_schema},
            }
            request_kwargs["response_format"] = response_format
        if temperature is not None:
            request_kwargs["temperature"] = temperature

        content_sequence = ["text"] + ["image_url" for _ in image_trace]
        sanitized_request = {
            "model": self.model,
            "message_role_sequence": role_sequence,
            "number_of_messages": len(messages),
            "system_prompt_text_hash": _sha256_text(system_prompt or ""),
            "system_prompt_byte_length": len((system_prompt or "").encode("utf-8")),
            "user_prompt_hash": _sha256_text(prompt),
            "user_prompt_byte_length": len(prompt.encode("utf-8")),
            "user_content_item_sequence": content_sequence,
            "text_first": content_sequence[0] == "text",
            "image_second": len(content_sequence) > 1 and content_sequence[1] == "image_url",
            "number_of_images_attached": len(image_trace),
            "response_format_type": response_format["type"] if response_format else None,
            "json_schema_hash": _canonical_hash(format_schema) if format_schema else None,
            "temperature": temperature,
            "max_tokens": None,
            "stop": None,
            "timeout": "OpenAI client timeout=60 from upstream VLMBackend",
            "images": image_trace,
        }
        request_shape_hash = _canonical_hash(sanitized_request)
        trace_entry: dict[str, Any] = {
            "call_index": len(TRACE_CONTEXT["call_traces"]),
            "call_kind": TRACE_CONTEXT.get("active_call_kind") or "non_detection",
            "model": self.model,
            "request_shape": sanitized_request,
            "request_shape_hash": request_shape_hash,
            "raw_request_payload_hash_sanitized": request_shape_hash,
            "raw_response_text": None,
            "raw_response_sha256": None,
            "exception": None,
        }

        try:
            response = self.client.chat.completions.create(**request_kwargs)
            text = response.choices[0].message.content or ""
            trace_entry["raw_response_text"] = text
            trace_entry["raw_response_sha256"] = _sha256_text(text)
            return text
        except Exception as exc:
            trace_entry["exception"] = repr(exc)
            raise
        finally:
            TRACE_CONTEXT["call_traces"].append(trace_entry)

    return instrumented_generate


def _make_instrumented_vlm_detections(model_mod: Any, interfaces_mod: Any) -> Any:
    def instrumented_vlm_detections(self: Any, image: Image.Image) -> list[Any]:
        from json_repair import repair_json
        from pydantic import ValidationError

        prompt = self.detect_objects_prompt_template

        categories = ", ".join(self.categories)
        detection_guidance = model_mod.format_detection_doctrine(self.categories)
        if self.detection_bbox_convention.startswith("xyxy"):
            bbox_format = "[xmin, ymin, xmax, ymax]"
        elif self.detection_bbox_convention.startswith("yxyx"):
            bbox_format = "[ymin, xmin, ymax, xmax]"
        else:
            raise ValueError("Unsupported bounding box convention in config.")

        if self.detection_bbox_convention.endswith("_1"):
            bbox_scale = "normalized coordinates from 0.0 to 1.0"
        elif self.detection_bbox_convention.endswith("_1000"):
            bbox_scale = "normalized coordinates from 0 to 1000"
        elif self.detection_bbox_convention.endswith("_pixels"):
            bbox_scale = "raw pixel coordinates relative to the image"
        else:
            raise ValueError("Unsupported bounding box scale in config.")

        placeholder_blocks = {
            "categories": categories,
            "detection_guidance": detection_guidance,
            "bbox_format": bbox_format,
            "bbox_scale": bbox_scale,
        }
        rendered = prompt
        for key, value in placeholder_blocks.items():
            rendered = rendered.replace("{" + key + "}", value)

        unresolved = sorted(set(re.findall(r"\{[a-zA-Z0-9_]+\}", rendered)))
        schema_words_preserved = all(
            phrase in rendered
            for phrase in [
                "Return valid JSON only.",
                "top-level detections field",
                '"target_type": string',
                '"bbox": [xmin, ymin, xmax, ymax]',
            ]
        )

        vlm_image = model_mod.resize_for_vlm(image, self.detection_max_image_size)
        rendered_trace = {
            "rendered_prompt_text": rendered,
            "rendered_prompt_sha256": _sha256_text(rendered),
            "rendered_prompt_byte_length": len(rendered.encode("utf-8")),
            "rendered_prompt_line_count": len(rendered.splitlines()),
            "placeholder_substitution_hashes": {
                key: _sha256_text(value) for key, value in placeholder_blocks.items()
            },
            "unresolved_placeholders": unresolved,
            "json_schema_instruction_preserved": schema_words_preserved,
            "runtime_prompt_mentions_case_ids": bool(
                re.search(r"\bcase\s*\d+\b|human-report-\d+", rendered, re.IGNORECASE)
            ),
            "bbox_convention": self.detection_bbox_convention,
            "max_image_size": self.detection_max_image_size,
            "resized_vlm_image_size": list(vlm_image.size),
        }
        TRACE_CONTEXT["rendered_detection_prompt"] = rendered_trace

        TRACE_CONTEXT["active_call_kind"] = "detection"
        try:
            response = self.detection_vlm.generate(
                image=vlm_image,
                prompt=rendered,
                system_prompt=self.system_prompt,
                format_schema=interfaces_mod.DetectionResponse.model_json_schema(),
                temperature=self.detection_temperature,
            )
        finally:
            TRACE_CONTEXT["active_call_kind"] = None

        parse_trace: dict[str, Any] = {
            "raw_response_text": response,
            "raw_response_sha256": _sha256_text(response),
            "repaired_json_text": None,
            "repaired_json_sha256": None,
            "pydantic_validation_success": False,
            "validation_error": None,
            "raw_detections_count": None,
            "accepted_after_target_type_validation_count": 0,
            "rejected_detections": [],
            "final_detections_count": 0,
            "final_detection_bbox_list": [],
            "failure_stage": None,
        }

        try:
            repaired = repair_json(response)
            parse_trace["repaired_json_text"] = repaired
            parse_trace["repaired_json_sha256"] = _sha256_text(repaired)
            payload = interfaces_mod.DetectionResponse.model_validate_json(repaired)
            parse_trace["pydantic_validation_success"] = True
        except ValidationError as exc:
            parse_trace["validation_error"] = str(exc)
            parse_trace["failure_stage"] = "schema_validation"
            TRACE_CONTEXT["detection_parse_trace"] = parse_trace
            if TRACE_CONTEXT["call_traces"]:
                TRACE_CONTEXT["call_traces"][-1]["detection_parse_trace"] = parse_trace
            return []

        parse_trace["raw_detections_count"] = len(payload.detections)
        detections = []
        accepted_after_type = 0

        for index, item in enumerate(payload.detections):
            target_type = item.target_type.strip().lower()
            raw_item = {"index": index, "target_type": item.target_type, "bbox": item.bbox}
            if target_type not in self.categories:
                parse_trace["rejected_detections"].append(
                    {**raw_item, "reason": "unknown_target_type"}
                )
                continue

            accepted_after_type += 1
            pixel_box = model_mod.bbox_to_pixels(
                image,
                vlm_image,
                item.bbox,
                bbox_convention=self.detection_bbox_convention,
            )
            if pixel_box is None:
                parse_trace["rejected_detections"].append(
                    {**raw_item, "reason": "invalid_bbox_or_conversion_failed"}
                )
                continue

            detections.append(interfaces_mod.Detection(label=target_type, bbox=pixel_box))

        parse_trace["accepted_after_target_type_validation_count"] = accepted_after_type
        parse_trace["final_detections_count"] = len(detections)
        parse_trace["final_detection_bbox_list"] = [
            {"label": det.label, "bbox": list(det.bbox)} for det in detections
        ]
        parse_trace["failure_stage"] = "none"
        TRACE_CONTEXT["detection_parse_trace"] = parse_trace
        if TRACE_CONTEXT["call_traces"]:
            TRACE_CONTEXT["call_traces"][-1]["detection_parse_trace"] = parse_trace
        return detections

    return instrumented_vlm_detections


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scratch-root", required=True)
    parser.add_argument("--image", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--trace-output", required=True)
    parser.add_argument("--candidate-id", required=True)
    parser.add_argument("--backend-label", required=True)
    parser.add_argument("--endpoint-url", required=True)
    parser.add_argument("--source-overlay", required=True)
    parser.add_argument("--base-overlay", required=True)
    parser.add_argument("--stage", required=True)
    parser.add_argument("--intended-changes-json", default="[]")
    args = parser.parse_args()

    scratch_root = Path(args.scratch_root).resolve()
    sys.path.insert(0, str(scratch_root / "src"))

    image_path = Path(args.image).resolve()
    output_dir = Path(args.output).resolve()
    trace_output = Path(args.trace_output).resolve()
    source_overlay = Path(args.source_overlay).resolve()
    base_overlay = Path(args.base_overlay).resolve()
    config_path = scratch_root / "src/bda_svc/pipeline/config.yaml"
    doctrine_path = scratch_root / "src/bda_svc/pipeline/doctrine.yaml"

    trace_output.parent.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    base_template = _extract_detect_prompt(base_overlay)
    overlay_template = _extract_detect_prompt(source_overlay)
    scratch_config = _read_yaml(config_path)
    scratch_detect = scratch_config["prompts"]["detect_objects"]

    with Image.open(image_path).convert("RGB") as original_image:
        original_size = list(original_image.size)
    original_image_sha = _file_sha256(image_path)

    trace: dict[str, Any] = {
        "generated_at": _utc_now(),
        "candidate_id": args.candidate_id,
        "stage": args.stage,
        "backend_label": args.backend_label,
        "endpoint_url": args.endpoint_url,
        "model_name_env": os.environ.get("BDA_DETECTION_MODEL"),
        "server_kind": "openai_compatible",
        "scratch_root": str(scratch_root),
        "git": {
            "branch": _run(["git", "rev-parse", "--abbrev-ref", "HEAD"], scratch_root),
            "commit": _run(["git", "rev-parse", "HEAD"], scratch_root),
            "status_short": _run(["git", "status", "--short"], scratch_root),
        },
        "runtime_versions": {
            "python": platform.python_version(),
            "openai": _version("openai"),
            "pillow": _version("Pillow"),
            "pydantic": _version("pydantic"),
        },
        "source_files": {
            "source_overlay_path": str(source_overlay),
            "base_overlay_path": str(base_overlay),
            "scratch_config_path": str(config_path),
            "doctrine_path": str(doctrine_path),
            "source_overlay_sha256": _file_sha256(source_overlay),
            "base_overlay_sha256": _file_sha256(base_overlay),
            "scratch_config_sha256": _file_sha256(config_path),
            "doctrine_sha256": _file_sha256(doctrine_path),
        },
        "overlay_application": {
            "overlay_template_sha256": _sha256_text(overlay_template),
            "base_v020c_overlay_template_sha256": _sha256_text(base_template),
            "overlay_template_diff_from_base": _unified_diff(
                base_template,
                overlay_template,
                "v020c_detect_objects_template",
                f"{args.candidate_id}_detect_objects_template",
            ),
            "scratch_detect_objects_sha256": _sha256_text(scratch_detect),
            "scratch_detect_vs_intended_overlay_diff": _unified_diff(
                overlay_template,
                scratch_detect,
                f"{args.candidate_id}_intended_overlay",
                "scratch_config_detect_objects",
            ),
            "overlay_actually_applied": scratch_detect == overlay_template,
            "candidate_unintended_no_op": scratch_detect == base_template,
            "intended_semantic_changes": json.loads(args.intended_changes_json),
            "rendered_template_changes": "captured after placeholder substitution",
        },
        "image_source": {
            "original_image_path": str(image_path),
            "original_image_sha256": original_image_sha,
            "original_image_size": original_size,
        },
        "analysis": {},
        "exception": None,
    }

    try:
        import bda_svc.export as export_mod
        import bda_svc.pipeline.interfaces as interfaces_mod
        import bda_svc.pipeline.model as model_mod

        interfaces_mod.VLMBackend.generate = _make_instrumented_generate()
        model_mod.BDAPipeline._vlm_detections = _make_instrumented_vlm_detections(
            model_mod,
            interfaces_mod,
        )

        pipe = model_mod.BDAPipeline()
        model_name = (
            f"detection={pipe.detection_vlm.model};assessment={pipe.assessment_vlm.model}"
        )
        start = time.perf_counter()
        result = pipe.analyze(image_path)
        inference_time = time.perf_counter() - start
        report_path = export_mod.save_json(result, image_path, output_dir, model_name, inference_time)
        trace["analysis"] = {
            "final_report_path": str(report_path),
            "model_name": model_name,
            "inference_time_seconds": inference_time,
            "physical_damage_count": len(result.get("physical_damage", {})),
        }
    except Exception as exc:
        trace["exception"] = repr(exc)
        trace["analysis"]["failed"] = True
    finally:
        rendered_trace = TRACE_CONTEXT.get("rendered_detection_prompt")
        if rendered_trace and rendered_trace.get("rendered_prompt_text"):
            trace["rendered_prompt"] = rendered_trace
            trace["rendered_prompt"]["rendered_prompt_diff_from_base"] = None
        else:
            trace["rendered_prompt"] = rendered_trace
        trace["detection_parse_trace"] = TRACE_CONTEXT.get("detection_parse_trace")
        trace["request_response_traces"] = TRACE_CONTEXT["call_traces"]
        trace["response_trace_captured"] = bool(TRACE_CONTEXT["call_traces"])
        trace_output.write_text(json.dumps(trace, indent=2, ensure_ascii=False), encoding="utf-8")

    return 1 if trace["exception"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
