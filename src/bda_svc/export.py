"""Export utilities."""

import datetime
import json
import uuid
from pathlib import Path

from bda_svc import constants


def build_report(
    bda: dict, image_path: str | Path, model_name: str, inference_time: float
) -> dict:
    """Build report IAW JSON schema.

    Args:
        bda: BDA analysis dictionary.
        image_path: Path of the original image.
        model_name: Model name metadata.
        inference_time: Inference time metadata.
    """
    image_path = Path(image_path)

    return {
        "metadata": {
            "model_name": model_name,
            "image_id": str(uuid.uuid4()),
            "image_filename": image_path.name,
            "date_created": datetime.datetime.now(datetime.UTC).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            ),
            "location": {"crs": "", "coordinates": ""},
            "report_type": "PDA",
            "analyst": "bda-svc",
            "inference_time": f"{inference_time:.2f}",
        },
        "physical_damage": bda.get("physical_damage", {}),
        "summary": bda.get("summary", ""),
    }


def save_json(
    bda: dict,
    image_path: str | Path,
    output_path: str | Path | None,
    model_name: str,
    inference_time: float,
) -> None:
    """Save BDA as a JSON file.

    Args:
        bda: BDA analysis dictionary.
        image_path: Path of the original image.
        output_path: Path of output folder. Uses default if None/empty.
        model_name: Model name metadata.
        inference_time: Inference time metadata.
    """
    image_path = Path(image_path)
    output_path = Path(output_path or constants.DEFAULT_OUTPUT_PATH)
    output_path.mkdir(parents=True, exist_ok=True)

    report = build_report(bda, image_path, model_name, inference_time)

    timestamp = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d_%H%M%SZ")
    json_path = output_path / f"{image_path.stem}_{timestamp}.json"

    with json_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)

    print(f"[*] Exported: {json_path}")
