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


def print_scene_reports(scene_reports: list[models.SceneReport]):
    """Prints scene reports in tabular form to STDOUT.

    Args:
        scene_reports: List of SceneReport objects
    """
    len_col_0 = 30
    row_sep_eq = f"+{'=' * (len_col_0 + 4)}+{'=' * 8}+{'=' * 7}+{'=' * 7}+"
    row_sep_dash = f"+{'-' * (len_col_0 + 4)}+{'-' * 8}+{'-' * 7}+{'-' * 7}+"

    print(f"\n\n+{'=' * (len(row_sep_eq) - 2)}+")
    print(f"|{'SCORES (PER IMAGE)':^{len(row_sep_eq) - 2}}|")
    print(row_sep_eq)
    print(f"|  {'IMAGE':^{len_col_0}}  | ASSESS | LOGIC | TOTAL |")
    print(row_sep_eq)

    for scene_report in scene_reports:
        assess_str = (
            f"{scene_report.assess:.3f}" if scene_report.assess is not None else " N/A "
        )
        logic_str = (
            f"{scene_report.logic:.3f}" if scene_report.logic is not None else " N/A "
        )
        total_str = (
            f"{scene_report.total:.3f}" if scene_report.total is not None else " N/A "
        )

        print(
            f"| {scene_report.image[:len_col_0]:>{len_col_0 + 2}} "
            f"|  {assess_str} "
            f"| {logic_str} "
            f"| {total_str} |"
        )
        print(row_sep_dash)


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
    scene_reports = []

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
        else:
            matches = []
            false_negatives = []
            false_positives = P_report.targets

        # Calculate scores for the entire image
        scene_reports.append(
            models.SceneReport(
                P_report.metadata.model_name,
                key,
                matches,
                len(R_report.targets),
                len(false_negatives),
                len(false_positives),
                float(P_report.metadata.inference_time),
            )
        )

        # Generate reference and model bounding boxes for current image
        bboxes.draw_bboxes(R_report=R_report, P_report=P_report)

    # Print scores per image
    # print_scene_reports(scene_reports)

    # Print overall model scores
    model_report = models.ModelReport(scene_reports)
    model_report.print_summary()

    # Copy report folders into our destination output folder
    output_path_ref = config.OUTPUT_DIR / config.REFERENCE_DIR.name
    output_path_pred = config.OUTPUT_DIR / config.PREDICTED_DIR.name
    shutil.copytree(config.REFERENCE_DIR, output_path_ref, dirs_exist_ok=True)
    shutil.copytree(config.PREDICTED_DIR, output_path_pred, dirs_exist_ok=True)

    # Try to create and write the CSVs
    result_targets = export.save_csv("eval_targets", packages)

    if result_targets:
        print(f"\n[*] Successfully created per-target report '{result_targets}'.")
    else:
        print("\n[*] Error generating evaluation report.")

    result_model = export.save_csv(
        "eval_model", [model_report.to_dict()], export.CSV_HEADERS_MODEL
    )

    if result_model:
        print(f"[*] Successfully created model report '{result_model}'.\n")
    else:
        print("\n[*] Error generating evaluation report.")


if __name__ == "__main__":
    main()
