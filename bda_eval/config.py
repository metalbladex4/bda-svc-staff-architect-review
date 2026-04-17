"""Collection of common configuration entries."""

from pathlib import Path

IMAGES_DIR: Path | None = None
REFERENCE_DIR: Path | None = None
PREDICTED_DIR: Path | None = None
OUTPUT_DIR: Path | None = None
REFERENCE_LABEL: str | None = None
PREDICTED_LABEL: str | None = None
CROP_BUFFER_RATIO: float = 0.2
