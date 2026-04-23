"""Input data retrieval."""

import sys
from pathlib import Path

from bda_svc import constants

VALID_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp")


def get_input_folder(cmdline_path: str | None) -> Path:
    """Retrieve input path and perform validation.

    Args:
        cmdline_path: Optional path from command-line arguments.

    Returns:
        Validated input folder path.

    Raises:
        SystemExit: If the selected input path does not exist.
    """
    # Get command-line path argument (if provided)
    input_folder = Path(cmdline_path or constants.DEFAULT_INPUT_PATH)

    # TODO: implement better logging
    print(f"[*] Input source set to {input_folder.resolve()}")

    # TODO: Create robot endpoint to avoid manually specifying path

    # Perform path validation
    if not input_folder.exists():
        # Print to STDERR with exit code 1
        sys.exit(f"\nThe input path {input_folder} does not exist. Exiting.\n")

    return input_folder


def get_input_paths(input_folder: Path) -> list[Path]:
    """Retrieve paths to all input image files.

    Args:
        input_folder: Input folder path (or a single file path).

    Returns:
        List of valid image file paths.

    Raises:
        SystemExit: If no valid input images are found.
    """
    files: list[Path] = []

    # Return early if input_folder is actually a file
    if input_folder.is_file():
        if input_folder.suffix.lower() in VALID_EXTENSIONS:
            return [input_folder]

        # Invalid extension
        sys.exit(
            f"\nThe input path {input_folder} "
            f"does not contain valid input data. Exiting.\n"
        )

    # Perform recursive file search
    files = [
        path
        for path in input_folder.rglob("*")
        if path.is_file() and path.suffix.lower() in VALID_EXTENSIONS
    ]

    if not files:
        sys.exit(
            f"\nThe input path {input_folder} "
            f"does not contain valid input data. Exiting.\n"
        )

    files.sort()
    return files
