"""Command-line functionality."""

import argparse


def get_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed command-line arguments.
    """
    bda_eval_desc = "Evaluate bda-svc reports."

    parser = argparse.ArgumentParser(description=bda_eval_desc)

    parser.add_argument(
        "-r",
        "--reference",
        type=str,
        required=True,
        help=("Path to reference report folder."),
    )

    parser.add_argument(
        "-p",
        "--predicted",
        type=str,
        required=True,
        help=("Path to predicted report folder."),
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help=("Path to output folder."),
    )

    parser.add_argument(
        "-i",
        "--images",
        type=str,
        help=("Path to images folder."),
    )

    return parser.parse_args()
