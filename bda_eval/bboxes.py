"""Draw BDA bounding boxes from two sets of reports."""

import config
import models
from PIL import Image, ImageDraw, ImageFont


def draw_bbox(
    draw_obj: ImageDraw.ImageDraw,
    obj_label: str,
    obj_bbox: models.BoundingBox,
    rect_color: str,
    label_text: str,
    font: ImageFont.FreeTypeFont,
):
    """Draw a single bounding box rectangle and corresponding label.

    Args:
        draw_obj: ImageDraw object
        obj_label: The label assigned to the object within the report
        obj_bbox: BoundingBox object
        rect_color: Desired color of the bounding box rectangle
        label_text: Desired label text for the rectangle
        font: TTF font object
    """
    # Create rectangle bounding box [(xmin, ymin), (xmax, ymax)]
    bbox_rect = [
        (obj_bbox.xmin, obj_bbox.ymin),
        (obj_bbox.xmax, obj_bbox.ymax),
    ]

    # Check if object was not actually found within image (as per report)
    if bbox_rect == [(0, 0), (0, 0)]:
        return

    label_fill = "white"
    bbox_width = 3

    # Create label bounding box [(xmin, ymin), (xmax, ymax)]
    left, top, right, bottom = draw_obj.textbbox(
        (obj_bbox.xmin, obj_bbox.ymin), label_text, font=font
    )

    bbox_label_rect = [left, top, right, bottom + 5]

    # Draw the label background rectangle
    draw_obj.rectangle(bbox_label_rect, fill=label_fill)

    # Draw the label
    draw_obj.text((left, top), label_text, fill="black", font=font)

    # Draw the rectangle bounding box
    draw_obj.rectangle(bbox_rect, outline=rect_color, width=bbox_width)


def draw_bboxes(
    img_filename: str,
    R_report: models.BDAReport,
    P_report: models.BDAReport,
):
    """Draw bounding boxes for all objects from both sets of reports.

    Args:
        img_filename: Image filename (as set in BDA report)
        R_report: Reference BDAReport
        P_report: Predicted BDAReport
    """
    # Load TrueType font
    font = ImageFont.truetype("./fonts/DejaVuSans.ttf", 18)

    # Create a draw object `draw_obj`
    img_filename = R_report.metadata.image_filename
    assert config.IMAGES_DIR is not None, "[*] Image folder not initialized."
    img_path = config.IMAGES_DIR / img_filename

    if not img_path.exists():
        print(f"[*] Image `{img_path}` not found. Skipping.")
        return

    img = Image.open(img_path)
    draw_obj = ImageDraw.Draw(img)

    # Draw a bounding box for every reference target
    for r_target in R_report.targets:
        draw_bbox(
            draw_obj=draw_obj,
            obj_label=r_target.target_label,
            obj_bbox=r_target.box,
            rect_color="green",
            label_text="human",
            font=font,
        )

    # Draw a bounding box for every predicted target
    for p_target in P_report.targets:
        draw_bbox(
            draw_obj=draw_obj,
            obj_label=p_target.target_label,
            obj_bbox=p_target.box,
            rect_color="red",
            label_text="model",
            font=font,
        )

    assert config.OUTPUT_DIR is not None, "[*] Output folder not initialized."
    output_folder = config.OUTPUT_DIR / "images_bbox_both"
    output_folder.mkdir(parents=True, exist_ok=True)

    img.save(f"{output_folder}/bbox_{img_filename}")
