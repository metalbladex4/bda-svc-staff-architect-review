"""Simple script to fix human-generated BDAs."""

import argparse
import datetime
import json
import re
import sys
import uuid
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


def get_report_paths(ref_folder: str) -> list[Path]:
    """Retrieve paths to all BDA reports.

    Args:
        ref_folder: Folder path (str) of reference BDA reports.

    Returns:
        List of reference report file paths.

    Raises:
        SystemExit: If no valid input images are found.
    """
    # Validate folder path
    ref_folder_path = get_folder(ref_folder)

    # Perform file search
    ref_paths = list(ref_folder_path.glob("*"))

    # Check if the folder is empty
    for paths in ref_paths:
        if not paths:
            sys.exit(
                f"\nNo report data found in {ref_folder_path.resolve()}. Exiting.\n"
            )

    return ref_paths


def get_report(report_path: Path) -> list | None:
    """Parse a BDA report file.

    Args:
        report_path: Path to BDA report

    Returns:
        Tuple with `match_key` and JSON data
    """
    objects = {}
    regex_pattern = re.compile(r"(?<=})[\s\\n]+(?={)")

    with open(report_path, encoding="utf-8") as file:
        try:
            # Load less strictly to prevent issues (ex. newlines in values)
            objects = [json.load(file, strict=False)]
        except json.JSONDecodeError:
            try:
                file.seek(0)

                # Split by empty line
                objects = [json.loads(s) for s in re.split(regex_pattern, file.read())]
            except json.JSONDecodeError:
                print(f"\nUnable to load JSON data from {report_path}. Skipping.")
                return None

    return objects


def fix_json(report_path: Path, objects: list) -> dict | None:
    """Generates schema-compliant JSON from dict.

    Args:
        report_path: Path of report.
        objects: List of detected objects.

    Returns:
        Compliant BDA report as dictionary
    """
    template = {
        "metadata": {
            "model_name": "",
            "image_id": str(uuid.uuid4()),
            "image_filename": "",
            "date_created": datetime.datetime.now(datetime.UTC).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            ),
            "location": {"crs": "", "coordinates": ""},
            "report_type": "PDA",
            "analyst": "",
        },
        "physical_damage": {},
        "summary": "",
    }

    target_types = [
        "bridges",
        "buildings",
        "bunkers",
        "dams_and_locks",
        "distillation_towers",
        "electronic_data_and_information_technology_systems",
        "ground_force_personnel_military_units",
        "ground_force_personnel_individuals",
        "military_equipment",
        "petroleum_oil_lubricants_storage_tanks",
        "power_plant_turbines_and_generators",
        "rail_lines_and_rail_yards",
        "roads",
        "runways_and_taxiways",
        "satellite_dishes",
        "ships",
        "steel_towers",
        "transformers",
        "tunnel_entrances_or_portals",
        "tunnel_facility_air_vents",
        "object_not_found",
    ]

    try:
        template["metadata"]["image_filename"] = f"{report_path.stem}.jpg"

        for i, obj in enumerate(objects):
            target_type = obj["t"].replace(" ", "_")

            if target_type not in target_types:
                target_type += "s"

                if target_type not in target_types:
                    print("Unable to parse 'obj'. Skipping")
                    continue

            template["physical_damage"][f"target_{i}"] = {
                "target_type": target_type,
                "damage_category": obj["d"].upper(),
                "confidence_level": obj["c"].upper(),
                "brief_supporting_logic": obj["l"].replace("\n", " ").replace("\t", ""),
                "bounding_box": {
                    "xmin": obj["bounding_box"]["xmin"],
                    "ymin": obj["bounding_box"]["ymin"],
                    "xmax": obj["bounding_box"]["xmax"],
                    "ymax": obj["bounding_box"]["ymax"],
                },
            }

        return template
    except KeyError:
        print(f"\nUnable to fix report {report_path} (KeyError). Skipping.")
        return None


def convert_reports(ref_folder: str, output_path: Path) -> bool:
    """Locate, parse, fix and save BDA report files.

    Args:
        ref_folder: Folder path (str) of reference BDA reports.
        output_path: Folder path output reports.

    Returns:
        Tuple with dictionary of reference JSON data and dictionary of predicted JSON data.
    """
    # Locate all report files
    R_paths = get_report_paths(ref_folder)

    if R_paths:
        # Parse report files
        for report_path in R_paths:
            objects = get_report(report_path)

            if objects:
                report_fixed = fix_json(report_path, objects)

                with open(
                    f"{output_path}/{report_path.stem}.json", "w", encoding="utf-8"
                ) as file:
                    json.dump(report_fixed, file, indent=4)

                print(f"Writing {report_path}")

        return True
    else:
        print("\n[*] No reports to process. Exiting.")
        return False


def main(args):
    """Main entrypoint."""
    output_path = Path(args.output)
    output_path.mkdir(parents=True, exist_ok=True)

    convert_reports(args.reports, output_path)


if __name__ == "__main__":
    tojson_desc = "Generates valid reports from minimal reports."

    parser = argparse.ArgumentParser(description=tojson_desc)

    parser.add_argument(
        "-r",
        "--reports",
        type=str,
        required=True,
        help=("Path to reference report folder."),
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help=("Path to output folder."),
    )

    args = parser.parse_args()

    main(args)
