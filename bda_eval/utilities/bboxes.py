"""Draw BDA bounding boxes from two sets of reports."""

import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


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


def get_paths(folder: str) -> list[Path]:
    """Retrieve paths to all BDA reports.

    Args:
        folder: Folder path (str) of BDA reports.

    Returns:
        List of report file paths.

    Raises:
        SystemExit: If no valid input images are found.
    """
    # Validate folder path
    folder_path = get_folder(folder)

    # Perform file search
    paths = list(folder_path.glob("*"))

    # Check if the folder is empty
    for p in paths:
        if not p:
            sys.exit(f"\nNo report data found in {folder_path.resolve()}. Exiting.\n")

    return paths


def draw_bbox(
    draw_obj, obj_label: str, obj_bbox: dict, rect_color: str, label_text: str
):
    """Draw a single bounding box rectangle and corresponding label.

    Args:
        draw_obj: Draw object
        obj_label: The label assigned to the object within the report
        obj_bbox: Dictionary containing {xmin, ymin, xmax, ymax}
        rect_color: Desired color of the bounding box rectangle
        label_text: Desired label text for the rectangle
    """
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    label_fill = "white"
    bbox_width = 3

    # Sanity check if bounding box coming in as a list instead of a dict
    if isinstance(obj_bbox, list):
        obj_bbox = {
            "xmin": obj_bbox[0],
            "ymin": obj_bbox[1],
            "xmax": obj_bbox[2],
            "ymax": obj_bbox[3],
        }

    # Create label bounding box [(xmin, ymin), (xmax, ymax)]
    left, top, right, bottom = draw_obj.textbbox(
        (obj_bbox["xmin"], obj_bbox["ymin"]), label_text, font=font
    )

    bbox_label_rect = [left, top, right, bottom + 5]

    # Create rectangle bounding box [(xmin, ymin), (xmax, ymax)]
    bbox_rect = [
        (obj_bbox["xmin"], obj_bbox["ymin"]),
        (obj_bbox["xmax"], obj_bbox["ymax"]),
    ]

    # Check if object was not actually found within image (as per report)
    if bbox_rect == [(0, 0), (0, 0)]:
        return

    # Draw the label background rectangle
    draw_obj.rectangle(bbox_label_rect, fill=label_fill)

    # Draw the label
    draw_obj.text(bbox_label_rect, label_text, fill="black", font=font)

    # Draw the rectangle bounding box
    draw_obj.rectangle(bbox_rect, outline=rect_color, width=bbox_width)


def draw_bboxes(
    folder_img: Path, paths_ref: list[Path], paths_pred: list[Path], folder_output: Path
):
    """Draw bounding boxes for all objects from both sets of reports.

    Args:
        folder_img: Path to image folder
        paths_ref: List of reference report paths
        paths_pred: List of predicted report paths
        folder_output: Path to output folder
    """
    # for path_img in paths_img:
    #    path_ref = [p for p in paths_ref if f"{path_img.stem}.json" in p.name][0]
    #    path_pred = [p for p in paths_pred if f"{path_img.stem}_" in p.stem][0]
    for path_ref in paths_ref:
        path_pred = [p for p in paths_pred if f"{path_ref.stem}_" in p.stem][0]

        with (
            path_ref.open("r", encoding="utf-8") as file_ref,
            path_pred.open("r", encoding="utf-8") as file_pred,
        ):
            report_ref = json.load(file_ref)
            report_pred = json.load(file_pred)

            # Create a draw object
            img_filename = report_ref["metadata"]["image_filename"]
            path_img = Path(f"{folder_img}/{img_filename}")

            img = Image.open(path_img)
            draw_obj = ImageDraw.Draw(img)

            for obj_label, obj_value in report_ref["physical_damage"].items():
                draw_bbox(
                    draw_obj, obj_label, obj_value["bounding_box"], "green", "human"
                )

            for obj_label, obj_value in report_pred["physical_damage"].items():
                draw_bbox(
                    draw_obj, obj_label, obj_value["bounding_box"], "red", "model"
                )

            img.save(f"{folder_output}/bbox_{img_filename}")

            print(f"Saved 'bbox_{img_filename}'")


def main(args):
    """Main entry point."""
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = Path("images_bbox_both")

    output_path.mkdir(parents=True, exist_ok=True)

    paths_ref = get_paths(args.reference)
    paths_pred = get_paths(args.predicted)

    draw_bboxes(Path(args.images), paths_ref, paths_pred, output_path)

    print("\nDone")


if __name__ == "__main__":
    bboxes_desc = (
        "Draws bounding boxes from reference and predicted reports, per image."
    )

    parser = argparse.ArgumentParser(description=bboxes_desc)

    parser.add_argument(
        "-i",
        "--images",
        type=str,
        required=True,
        help=("Path to images folder."),
    )

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

    args = parser.parse_args()

    main(args)
