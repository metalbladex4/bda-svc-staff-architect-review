"""Main application entry point for automated BDA evaluation."""
# pylint: disable=invalid-name

import cli
import discovery
import export

import models


def partition_keys(left: dict, right: dict) -> tuple[set, set, set]:
    """Compares two dictionaries and returns their common and distinct keys as sets.

    Args:
        left: First dictionary to be compared
        right: Second dictionary to be compared

    Returns:
        Tuple with common keys, keys only in left, and keys only in right
    """
    keys_left = set(left.keys())
    keys_right = set(right.keys())

    return keys_left & keys_right, keys_left - keys_right, keys_right - keys_left


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

    # Discover reports
    R_multi_images, P_multi_images = discovery.get_reports(
        args.reference, args.predicted
    )

    # Check if reference reports have corresponding predicted reports
    common_keys, missing_pred, missing_ref = partition_keys(
        R_multi_images, P_multi_images
    )

    # Basic sanity checks
    if missing_pred:
        print(f"\nMissing Predictions: {missing_pred}\n")

    if missing_ref:
        print(f"\nMissing References: {missing_ref}\n")

    # Assess image objects for every pair of reference and predicted reports
    packages = []

    for key in common_keys:
        # NOTE: matches = [(ref_1_object_1, pred_1_object_3), ...]
        R_report, P_report, match_results = compare_image_objects(
            R_multi_images[key], P_multi_images[key]
        )

        if match_results:
            matches, false_negatives, false_positives = match_results

            package = export.package_bda_report(
                # R_report,
                P_report,
                matches,
                false_negatives,
                false_positives,
            )

            packages.extend(package)

    result = export.save_csv(packages, args.output)

    if result:
        print(f"\n[*] Successfully created evaluation report '{result}'.\n")
    else:
        print("\n[*] Error generating evaluation report.")


if __name__ == "__main__":
    main()
