"""Draw BDA bounding boxes and review artifacts from two sets of reports."""

from pathlib import Path

import config
import models
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = Path(__file__).resolve().parent / "fonts" / "DejaVuSans.ttf"


def _load_font(size: int) -> ImageFont.FreeTypeFont:
    """Load the bundled TrueType font."""
    return ImageFont.truetype(str(FONT_PATH), size)


def _valid_targets(report: models.BDAReport) -> list[models.BDATarget]:
    """Return targets with non-zero bounding boxes."""
    return [
        target
        for target in report.targets
        if (target.box.xmin, target.box.ymin, target.box.xmax, target.box.ymax)
        != (0, 0, 0, 0)
    ]


def _image_path(img_filename: str) -> Path | None:
    """Return the source image path if available."""
    if config.IMAGES_DIR is None:
        print("[*] Image folder not initialized. Skipping bbox artifacts.")
        return None

    img_path = config.IMAGES_DIR / img_filename
    if not img_path.exists():
        print(f"[*] Image `{img_path}` not found. Skipping bbox artifacts.")
        return None

    return img_path


def _output_folder(folder_name: str) -> Path:
    """Create and return an output folder under the eval output root."""
    assert config.OUTPUT_DIR is not None, "[*] Output folder not initialized."
    output_folder = config.OUTPUT_DIR / folder_name
    output_folder.mkdir(parents=True, exist_ok=True)
    return output_folder


def draw_bbox(
    draw_obj: ImageDraw.ImageDraw,
    obj_bbox: models.BoundingBox,
    rect_color: str,
    label_text: str,
    font: ImageFont.FreeTypeFont,
) -> None:
    """Draw a single bounding box rectangle and corresponding label.

    Args:
        draw_obj: ImageDraw object
        obj_bbox: BoundingBox object
        rect_color: Desired color of the bounding box rectangle
        label_text: Desired label text for the rectangle
        font: TTF font object
    """
    bbox_rect = [
        (obj_bbox.xmin, obj_bbox.ymin),
        (obj_bbox.xmax, obj_bbox.ymax),
    ]

    if bbox_rect == [(0, 0), (0, 0)]:
        return

    if label_text:
        left, top, right, bottom = draw_obj.textbbox(
            (obj_bbox.xmin, obj_bbox.ymin), label_text, font=font
        )
        bbox_label_rect = [left, top, right, bottom + 5]
        draw_obj.rectangle(bbox_label_rect, fill="white")
        draw_obj.text((left, top), label_text, fill="black", font=font)

    draw_obj.rectangle(bbox_rect, outline=rect_color, width=3)


def _draw_report_overlay(
    base_img: Image.Image,
    report: models.BDAReport,
    rect_color: str,
    label_text: str,
) -> Image.Image:
    """Return a copy of an image with one report's boxes drawn on it."""
    overlay = base_img.copy()
    draw_obj = ImageDraw.Draw(overlay)
    font = _load_font(18)

    for target in report.targets:
        draw_bbox(
            draw_obj=draw_obj,
            obj_bbox=target.box,
            rect_color=rect_color,
            label_text=label_text,
            font=font,
        )

    return overlay


def _combined_bbox(report: models.BDAReport) -> models.BoundingBox | None:
    """Return the union bbox for all valid targets in a report."""
    targets = _valid_targets(report)
    if not targets:
        return None

    xmin = min(target.box.xmin for target in targets)
    ymin = min(target.box.ymin for target in targets)
    xmax = max(target.box.xmax for target in targets)
    ymax = max(target.box.ymax for target in targets)
    return models.BoundingBox(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)


def _crop_box(
    bbox: models.BoundingBox,
    img_width: int,
    img_height: int,
) -> tuple[int, int, int, int]:
    """Expand a bbox using the configured crop buffer ratio and clamp to image."""
    width = max(1, bbox.xmax - bbox.xmin)
    height = max(1, bbox.ymax - bbox.ymin)
    pad_x = int(round(width * config.CROP_BUFFER_RATIO))
    pad_y = int(round(height * config.CROP_BUFFER_RATIO))

    xmin = max(0, bbox.xmin - pad_x)
    ymin = max(0, bbox.ymin - pad_y)
    xmax = min(img_width, bbox.xmax + pad_x)
    ymax = min(img_height, bbox.ymax + pad_y)
    return xmin, ymin, xmax, ymax


def _placeholder_panel(size: tuple[int, int], message: str) -> Image.Image:
    """Create a small placeholder panel when a crop cannot be made."""
    panel = Image.new("RGB", size, color="white")
    draw_obj = ImageDraw.Draw(panel)
    draw_obj.rectangle(
        [(0, 0), (size[0] - 1, size[1] - 1)],
        outline="#999999",
        width=2,
    )
    font = _load_font(16)
    left, top, right, bottom = draw_obj.textbbox((0, 0), message, font=font)
    x = max(8, (size[0] - (right - left)) // 2)
    y = max(8, (size[1] - (bottom - top)) // 2)
    draw_obj.text((x, y), message, fill="#444444", font=font)
    return panel


def _build_report_crop(
    base_img: Image.Image,
    report: models.BDAReport,
) -> Image.Image:
    """Build a crop from the union of valid report boxes."""
    bbox = _combined_bbox(report)
    if bbox is None:
        return _placeholder_panel((160, 90), "No valid bbox")

    crop_rect = _crop_box(bbox, *base_img.size)
    return base_img.crop(crop_rect)


def _save_image(
    image: Image.Image,
    folder_name: str,
    prefix: str,
    img_filename: str,
) -> Path:
    """Save an image under the eval output tree."""
    output_folder = _output_folder(folder_name)
    output_path = output_folder / f"{prefix}_{img_filename}"
    image.save(output_path)
    return output_path


def _thumbnail_copy(image: Image.Image, max_size: tuple[int, int]) -> Image.Image:
    """Return a copy of an image shrunk to fit within max_size."""
    thumb = image.copy()
    thumb.thumbnail(max_size)
    return thumb


def _sheet_titles() -> tuple[str, str]:
    """Return user-facing labels for reference and predicted panels."""
    reference = config.REFERENCE_LABEL or (
        config.REFERENCE_DIR.name if config.REFERENCE_DIR else "Reference"
    )
    predicted = config.PREDICTED_LABEL or (
        config.PREDICTED_DIR.name if config.PREDICTED_DIR else "Predicted"
    )
    return reference, predicted


def _save_review_sheet(
    img_filename: str,
    ref_overlay: Image.Image,
    pred_overlay: Image.Image,
    ref_crop: Image.Image,
    pred_crop: Image.Image,
    write_root_sheet: bool,
) -> None:
    """Save a side-by-side review sheet for prompt-lab style visual review."""
    ref_label, pred_label = _sheet_titles()
    title_font = _load_font(16)
    padding = 12
    title_height = 24

    left_width = max(ref_overlay.width, pred_overlay.width)
    right_max = (left_width, max(ref_overlay.height, pred_overlay.height))
    ref_crop_panel = _thumbnail_copy(ref_crop, right_max)
    pred_crop_panel = _thumbnail_copy(pred_crop, right_max)
    right_width = max(ref_crop_panel.width, pred_crop_panel.width)

    row1_height = title_height + max(ref_overlay.height, ref_crop_panel.height)
    row2_height = title_height + max(pred_overlay.height, pred_crop_panel.height)
    sheet_width = padding * 3 + left_width + right_width
    sheet_height = padding * 3 + row1_height + row2_height

    sheet = Image.new("RGB", (sheet_width, sheet_height), color="white")
    draw_obj = ImageDraw.Draw(sheet)

    positions = [
        (
            f"{ref_label} Overlay",
            ref_overlay,
            padding,
            padding,
        ),
        (
            f"{ref_label} Crop",
            ref_crop_panel,
            padding * 2 + left_width,
            padding,
        ),
        (
            f"{pred_label} Overlay",
            pred_overlay,
            padding,
            padding * 2 + row1_height,
        ),
        (
            f"{pred_label} Crop",
            pred_crop_panel,
            padding * 2 + left_width,
            padding * 2 + row1_height,
        ),
    ]

    for title, image, x, y in positions:
        draw_obj.text((x, y), title, fill="black", font=title_font)
        sheet.paste(image, (x, y + title_height))

    review_folder = _output_folder("images_bbox_review")
    review_path = review_folder / f"bbox_review_{Path(img_filename).stem}.jpg"
    sheet.save(review_path)

    if write_root_sheet:
        assert config.OUTPUT_DIR is not None, "[*] Output folder not initialized."
        sheet.save(config.OUTPUT_DIR / "bbox_review_sheet.jpg")


def draw_bboxes(
    img_filename: str,
    R_report: models.BDAReport,
    P_report: models.BDAReport,
    write_root_review_sheet: bool = False,
) -> None:
    """Draw bbox artifacts for both reports and save a review sheet.

    Args:
        img_filename: Image filename (as set in BDA report)
        R_report: Reference BDAReport
        P_report: Predicted BDAReport
        write_root_review_sheet: Save `bbox_review_sheet.jpg` in output root.
    """
    img_path = _image_path(R_report.metadata.image_filename)
    if img_path is None:
        return

    with Image.open(img_path) as image:
        base_img = image.convert("RGB")

    combined = _draw_report_overlay(base_img, R_report, "green", "human")
    combined = _draw_report_overlay(combined, P_report, "red", "model")
    ref_overlay = _draw_report_overlay(base_img, R_report, "green", "")
    pred_overlay = _draw_report_overlay(base_img, P_report, "red", "")
    ref_crop = _build_report_crop(base_img, R_report)
    pred_crop = _build_report_crop(base_img, P_report)

    _save_image(combined, "images_bbox_both", "bbox", img_filename)
    _save_image(ref_overlay, "images_bbox_reference", "bbox", img_filename)
    _save_image(pred_overlay, "images_bbox_predicted", "bbox", img_filename)
    _save_image(ref_crop, "images_crop_reference", "crop", img_filename)
    _save_image(pred_crop, "images_crop_predicted", "crop", img_filename)
    _save_review_sheet(
        img_filename=img_filename,
        ref_overlay=ref_overlay,
        pred_overlay=pred_overlay,
        ref_crop=ref_crop,
        pred_crop=pred_crop,
        write_root_sheet=write_root_review_sheet,
    )
