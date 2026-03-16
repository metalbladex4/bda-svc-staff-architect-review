"""A collection of model utility functions."""

import json
from pathlib import Path
from typing import Any

import torch
import transformers
import yaml
from json_repair import repair_json
from PIL import Image, ImageDraw
from torchvision.ops import batched_nms

from bda_svc.pipeline.interfaces import Detection

REPO_PATH = Path(__file__).parents[3]
CONFIG_PATH = Path(__file__).parent / "config.yaml"
DOCTRINE_PATH = Path(__file__).parent / "doctrine.yaml"


def test_gpu() -> None:
    """Verify hardware acceleration and library versions."""
    print(f"Transformers Version: {transformers.__version__}")
    print(f"PyTorch Version: {torch.__version__}")

    cuda_available = torch.cuda.is_available()
    if cuda_available:
        print(f"CUDA Version: {torch.version.cuda}")
        print(f"Device: {torch.cuda.get_device_name()}")
    else:
        print("WARNING: CUDA not found.")


def load_yaml(path: Path) -> dict:
    """Load file from YAML.

    Args:
        path: Path to YAML file.

    Returns:
        A dictionary with loaded YAML.
    """
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data


def parse_json(response: str) -> list | dict[str, Any]:
    """Parse VLM output into JSON.

    Args:
        response: Raw VLM response text.

    Returns:
        Parsed JSON object or list.

    Raises:
        ValueError: If response cannot be parsed as JSON.
    """
    try:
        return json.loads(repair_json(response))
    except Exception as exc:
        raise ValueError("Unable to parse output as JSON.") from exc


def format_pda_doctrine(categories: list[str]) -> str:
    """Format PDA doctrine for selected target categories.

    Args:
        categories: A list of doctrinal BDA target categories.

    Returns:
        A doctrinal PDA string in the format:
            - Target Category
            - Physical Damage Definitions
            - Physical Damage Considerations
    """
    doctrine = load_yaml(DOCTRINE_PATH)
    output = []

    for key in categories:
        entry = doctrine.get(key)
        if not isinstance(entry, dict):
            continue
        title = key.replace("_", " ").upper()
        output.append(f"TARGET CATEGORY: {title}")

        for section_key in [
            "physical_damage_definitions",
            "physical_damage_considerations",
        ]:
            section_entry = entry.get(section_key)
            if section_entry is None:
                continue
            section_title = section_key.replace("_", " ").upper()
            output.append(f"{title} {section_title}")
            output.append(str(section_entry).strip())

    return "\n".join(output).strip() if output else "NO TARGET DOCTRINE AVAILABLE."


def bbox_from_1000(
    image: Image.Image, bbox: list[int | float]
) -> tuple[int, int, int, int] | None:
    """Convert a normalized 0-1000 bbox to raw pixel coordinates.

    Args:
        image: Source PIL image used for scaling.
        bbox: Normalized box in 0-1000 format.

    Returns:
        Pixel-space bounding box, or `None` if invalid.
    """
    # Fail safe if invalid
    if len(bbox) != 4:
        return None

    try:
        xmin, ymin, xmax, ymax = [float(value) for value in bbox]
    except (TypeError, ValueError):
        return None

    if not (0 <= xmin <= 1000 and 0 <= ymin <= 1000):
        return None
    if not (0 <= xmax <= 1000 and 0 <= ymax <= 1000):
        return None
    if xmin >= xmax or ymin >= ymax:
        return None

    # Scale pixel coordinates
    xmin_px = min(max(int(round((xmin / 1000) * image.width)), 0), image.width)
    ymin_px = min(max(int(round((ymin / 1000) * image.height)), 0), image.height)
    xmax_px = min(max(int(round((xmax / 1000) * image.width)), 0), image.width)
    ymax_px = min(max(int(round((ymax / 1000) * image.height)), 0), image.height)

    return xmin_px, ymin_px, xmax_px, ymax_px


def crop_with_buffer(
    image: Image.Image,
    box: tuple[int, int, int, int],
    buffer_ratio: float,
) -> Image.Image:
    """Crop a detection box with a small padding buffer.

    Args:
        image: Source image.
        box: Bounding box in integer pixel coordinates.
        buffer_ratio: Fractional padding applied to width and height.

    Returns:
        Cropped image region clamped to the image bounds.
    """
    xmin, ymin, xmax, ymax = box
    width = xmax - xmin
    height = ymax - ymin

    pad_x = int(round(width * buffer_ratio))
    pad_y = int(round(height * buffer_ratio))

    left = max(0, xmin - pad_x)
    top = max(0, ymin - pad_y)
    right = min(image.width, xmax + pad_x)
    bottom = min(image.height, ymax + pad_y)

    return image.crop((left, top, right, bottom))


def draw_box_overlay(image: Image.Image, box: tuple[int, int, int, int]) -> Image.Image:
    """Draw an outline box on a scene image.

    Args:
        image: Source scene image.
        box: Bounding box in integer pixel coordinates.

    Returns:
        Scene image copy with an outlined target box.
    """
    overlay = image.convert("RGB")
    draw = ImageDraw.Draw(overlay)

    xmin, ymin, xmax, ymax = box
    line_width = max(2, int(round(min(image.width, image.height) * 0.003)))
    draw.rectangle(
        (xmin, ymin, xmax, ymax),
        outline=(0, 255, 0),
        width=line_width,
    )

    return overlay


def nms(
    detections: list[Detection],
    iou_threshold: float = 0.50,
) -> list[Detection]:
    """Apply non-maximum suppression to detections.

    If multiple detector phrases map to one category, overlapping boxes
    compete under that shared label.

    Args:
        detections: Detection records to filter.
        iou_threshold: Maximum allowed IoU before suppression.

    Returns:
        Filtered detection list.
    """
    if not detections:
        return []

    label_to_index = {}
    boxes = []
    scores = []
    labels = []

    for detection in detections:
        # Convert string labels to numeric ids
        if detection.label not in label_to_index:
            label_to_index[detection.label] = len(label_to_index)
        # Convert Detection fields into tensor-friendly arrays
        boxes.append([float(value) for value in detection.box])
        scores.append(float(detection.score if detection.score is not None else 0.0))
        labels.append(label_to_index[detection.label])

    # Run NMS independently per label id.
    keep_indices = batched_nms(
        boxes=torch.tensor(boxes, dtype=torch.float32),
        scores=torch.tensor(scores, dtype=torch.float32),
        idxs=torch.tensor(labels, dtype=torch.int64),
        iou_threshold=iou_threshold,
    )
    return [detections[index] for index in keep_indices.tolist()]
