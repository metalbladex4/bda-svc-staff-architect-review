"""Main application entry point for automated BDA evaluation."""
# pylint: disable=invalid-name

import shutil
from pathlib import Path

import bboxes
import cli
import config
import discovery
import export
import models


def compare_image_objects(
    R: dict, P: dict
) -> tuple[
    models.BDAReport,
    models.BDAReport,
    tuple[list[models.BDAMatch], list[models.BDATarget], list[models.BDATarget]] | None,
]:
    """Compare objects from reference BDA to objects from predicted BDA.

    Args:
        R: Reference report (dictionary)
        P: Predicted report (dictionary)

    Returns:
        Reference/Predicted BDA reports and tuple of matching results
    """
    # Extract detected targets from report and instantiate as BDA objects
    R_report = models.BDAReport.from_dict(R)
    P_report = models.BDAReport.from_dict(P)

    # return P_report.get_bda_matches(R_report)
    return R_report, P_report, P_report.get_bda_matches(R_report)


def main():
    """Load reports, find matching objects and assess VLM performance."""
    args = cli.get_args()

    # Create output folder (if it doesn't exist) and store in config module
    config.OUTPUT_DIR = Path(args.output)
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Verify image folder exists
    config.IMAGES_DIR = Path(args.images)

    # Discover reports
    config.REFERENCE_DIR = Path(args.reference)
    config.PREDICTED_DIR = Path(args.predicted)
    R_multi_images, P_multi_images = discovery.get_reports(
        config.REFERENCE_DIR, config.PREDICTED_DIR
    )

    # Check if reference reports have corresponding predicted reports
    common_keys, missing_pred, missing_ref = discovery.partition_keys(
        R_multi_images, P_multi_images
    )

    # Basic sanity checks
    if missing_pred:
        print(f"[*] Missing Predictions: {missing_pred}")

    if missing_ref:
        print(f"[*] Missing References: {missing_ref}")

    packages = []

    # NOTE: "key" == image filename
    for key in common_keys:
        # Assess image objects for every pair of reference and predicted reports
        # NOTE: matches = [(ref_1_object_1, pred_1_object_3), ...]
        R_report, P_report, match_results = compare_image_objects(
            R_multi_images[key], P_multi_images[key]
        )

        if match_results:
            matches, false_negatives, false_positives = match_results

            # Convert our results into a list of CSV rows
            package = export.package_bda_report(
                # R_report,
                P_report,
                matches,
                false_negatives,
                false_positives,
            )

            packages.extend(package)

        # Generate reference and model bounding boxes for current image
        bboxes.draw_bboxes(img_filename=key, R_report=R_report, P_report=P_report)

    # Copy report folders into our destination output folder
    output_path_ref = config.OUTPUT_DIR / config.REFERENCE_DIR.name
    output_path_pred = config.OUTPUT_DIR / config.PREDICTED_DIR.name
    shutil.copytree(config.REFERENCE_DIR, output_path_ref, dirs_exist_ok=True)
    shutil.copytree(config.PREDICTED_DIR, output_path_pred, dirs_exist_ok=True)

    # Try to create the CSV and save to file
    result = export.save_csv(packages)

    if result:
        print(f"\n[*] Successfully created evaluation report '{result}'.\n")
    else:
        print("\n[*] Error generating evaluation report.")


if __name__ == "__main__":
    main()
