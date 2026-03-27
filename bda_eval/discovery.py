"""Input data retrieval."""
# pylint: disable=invalid-name

import json
import sys
from pathlib import Path


def get_folder(folder_path: str) -> Path:
    """Retrieve folder path and perform validation.

    Args:
        folder_path: Folder path (string).

    Returns:
        Validated input folder path.

    Raises:
        SystemExit: If the selected path does not exist.
    """
    folder = Path(folder_path)

    # NOTE: implement better logging
    # print(f"[*] Input source set to {folder.resolve()}")

    # Perform path validation
    if not folder.is_dir():
        # Print to STDERR with exit code 1
        sys.exit(f"\nThe path {folder.resolve()} does not exist. Exiting.\n")

    return folder


def get_report_paths(
    ref_folder: str, pred_folder: str
) -> tuple[list[Path], list[Path]]:
    """Retrieve paths to all BDA reports.

    Args:
        ref_folder: Folder path (str) of reference BDA reports.
        pred_folder: Folder path (str) of predicted BDA reports.

    Returns:
        Tuple with reference and predicted report file paths.

    Raises:
        SystemExit: If no valid input images are found.
    """
    # Validate folder paths
    ref_folder_path = get_folder(ref_folder)
    pred_folder_path = get_folder(pred_folder)

    # Perform file search
    ref_paths = list(ref_folder_path.glob("*.json"))
    pred_paths = list(pred_folder_path.glob("*.json"))

    # Check if either folder is empty
    for paths, folder in [(ref_paths, ref_folder_path), (pred_paths, pred_folder_path)]:
        if not paths:
            sys.exit(f"\nNo report data found in {folder.resolve()}. Exiting.\n")

    return ref_paths, pred_paths


def get_report(report_path: Path) -> tuple[str, dict] | None:
    """Parse a BDA report file.

    Args:
        report_path: Path to BDA report

    Returns:
        Tuple with `match_key` and JSON data
    """
    match_key = "image_filename"

    try:
        with open(report_path, encoding="utf-8") as file:
            json_obj = json.load(file)
    except json.JSONDecodeError:
        print(f"\nUnable to load JSON data from {report_path}. Skipping.")
        return None

    # Attempt to set new key `match_key` with value of JSON data
    try:
        match_value = json_obj["metadata"][match_key]
    except KeyError:
        print(f"\nNo such key '{match_key}'. Skipping {report_path}")
        return None

    return (match_value, json_obj)


def get_reports(ref_folder: str, pred_folder: str) -> tuple[dict, dict]:
    """Locate and parse BDA report files.

    Args:
        ref_folder: Folder path (str) of reference BDA reports.
        pred_folder: Folder path (str) of predicted BDA reports.

    Returns:
        Tuple with dictionary of reference JSON data and dictionary of predicted JSON data.
    """
    R_dict_json = {}
    P_dict_json = {}

    # Locate all report files
    R_paths, P_paths = get_report_paths(ref_folder, pred_folder)

    # Parse report files
    for ref_path in R_paths:
        result = get_report(ref_path)

        if result:
            key, data = result

            if key not in R_dict_json:
                R_dict_json[key] = data
            else:
                print(f"\nDuplicate key '{key}'. Skipping {ref_path}")

    for pred_path in P_paths:
        result = get_report(pred_path)

        if result:
            key, data = result

            if key not in P_dict_json:
                P_dict_json[key] = data
            else:
                print(f"\nDuplicate key '{key}'. Skipping {pred_path}")

    return R_dict_json, P_dict_json
