from __future__ import annotations

import argparse
import importlib
import json
import os
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


CANVAS = (1600, 1500)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compose the approved magnetic-cube catalog sheet.")
    parser.add_argument("--work-dir", type=Path, required=True, help="Directory containing compose_competitor_rebuild.py and texture assets.")
    parser.add_argument("--metadata", type=Path, required=True, help="Scene metadata JSON.")
    selector = parser.add_mutually_exclusive_group(required=True)
    selector.add_argument("--order", type=int, help="Scene order in metadata.")
    selector.add_argument("--scene-name", help="Exact Chinese scene name in metadata.")
    parser.add_argument("--output", type=Path, required=True, help="Output PNG path.")
    parser.add_argument("--title", default="MAGNETIC CUBE")
    parser.add_argument(
        "--color-box",
        type=Path,
        help="Optional approved transparent color-box PNG placed at lower right.",
    )
    return parser.parse_args()


def import_pipeline(work_dir: Path):
    work_dir = work_dir.resolve()
    sys.path.insert(0, str(work_dir))
    try:
        pipeline = importlib.import_module("compose_competitor_rebuild")
    except ImportError as exc:
        raise RuntimeError(f"Cannot import catalog helpers from {work_dir}") from exc
    locked_faces = os.environ.get("MAGNETIC_LOCKED_FACE_DIR")
    if locked_faces:
        pipeline.FACE_DIR = Path(locked_faces)
    return pipeline.font, pipeline.make_detail_icon, pipeline.prepare_scene


def sky_background() -> Image.Image:
    height, width = 1030, CANVAS[0]
    yy, xx = np.mgrid[0:height, 0:width]
    t = (yy / (height - 1))[..., None]
    top = np.asarray((150, 210, 240), dtype=np.float32)
    bottom = np.asarray((218, 239, 246), dtype=np.float32)
    rgb = top * (1 - t) + bottom * t
    distance = np.sqrt(((xx - width * 0.52) / 760) ** 2 + ((yy - height * 0.46) / 620) ** 2)
    rgb += 12 * np.clip(1 - distance, 0, 1)[..., None]
    rgba = np.dstack((np.clip(rgb, 0, 255).astype(np.uint8), np.full((height, width), 255, dtype=np.uint8)))
    return Image.fromarray(rgba, "RGBA")


def draw_divider(canvas: Image.Image) -> None:
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 1030, 1600, 1075), fill=(117, 180, 62))
    draw.rectangle((0, 1075, 1600, 1140), fill=(91, 51, 34))
    greens = ((141, 203, 68), (101, 164, 49), (157, 211, 75), (84, 146, 45))
    browns = ((111, 61, 42), (77, 43, 31), (126, 70, 46), (87, 47, 35))
    unit = 46
    for column, x in enumerate(range(0, 1600, unit)):
        height = (column * 17 % 3 + 1) * 15
        draw.rectangle((x, 1030, x + unit, 1030 + height), fill=greens[column % len(greens)])
        if column % 4 == 0:
            draw.rectangle((x + 12, 1065, x + 34, 1088), fill=greens[(column + 2) % len(greens)])
    for row, y in enumerate(range(1085, 1140, 25)):
        for column, x in enumerate(range(-20, 1600, 76)):
            if (row + column) % 3 != 1:
                draw.rectangle((x, y, x + 54, y + 24), fill=browns[(row + column) % len(browns)])


def grid_columns(type_count: int) -> int:
    if type_count == 12:
        return 6
    if type_count == 13:
        return 7
    return 8


def crop_alpha(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    bounds = rgba.getchannel("A").getbbox()
    return rgba.crop(bounds) if bounds else rgba


def alpha_safe_thumbnail(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    premultiplied = crop_alpha(image).convert("RGBa")
    premultiplied.thumbnail(size, Image.Resampling.LANCZOS)
    return premultiplied.convert("RGBA")


def add_color_box(canvas: Image.Image, path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(path)
    color_box = alpha_safe_thumbnail(Image.open(path), (420, 300))
    reserved = (1148, 690, 1578, 1005)
    x = reserved[0] + (reserved[2] - reserved[0] - color_box.width) // 2
    y = reserved[1] + (reserved[3] - reserved[1] - color_box.height) // 2
    if y + color_box.height >= 1030:
        raise RuntimeError("Color box overlaps the catalog divider")
    canvas.alpha_composite(color_box, (x, y))


def add_2cm_icon(canvas: Image.Image, font, make_detail_icon) -> None:
    draw = ImageDraw.Draw(canvas)
    icon = make_detail_icon(2, 132)
    x, y = 1405, 225
    canvas.alpha_composite(icon, (x + (132 - icon.width) // 2, y))
    line_x = x - 24
    top, bottom = y + 8, y + 126
    color = (54, 59, 57, 255)
    draw.line((line_x, top, line_x, bottom), fill=color, width=3)
    draw.line((line_x - 10, top, line_x + 10, top), fill=color, width=3)
    draw.line((line_x - 10, bottom, line_x + 10, bottom), fill=color, width=3)
    draw.text((line_x, y - 22), "2CM", font=font(24, True), fill=(42, 45, 43, 255), anchor="mm")


def add_parts_grid(canvas: Image.Image, item: dict, font, make_detail_icon) -> None:
    details = item["sku_counts"]
    type_count = len(details)
    if not 12 <= type_count <= 15:
        raise RuntimeError(f"Approved template requires 12-15 SKU types, got {type_count}")
    if sum(detail["count"] for detail in details) != item["pcs"]:
        raise RuntimeError("Parts-detail sum does not equal PCS")

    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 1140, 1600, 1500), fill=(255, 246, 205), outline=(77, 58, 39), width=4)
    draw.text((58, 1150), "颗粒明细", font=font(20, True), fill=(42, 45, 48))

    columns = grid_columns(type_count)
    gap_x, gap_y = 12, 8
    usable_width = 1484
    cell_w = (usable_width - (columns - 1) * gap_x) // columns
    cell_h = 142
    start_x, start_y = 58, 1190
    for index, detail in enumerate(details):
        row, column = divmod(index, columns)
        x = start_x + column * (cell_w + gap_x)
        y = start_y + row * (cell_h + gap_y)
        draw.rectangle((x, y, x + cell_w, y + cell_h), fill=(255, 239, 188), outline=(91, 61, 35), width=3)
        draw.text((x + 8, y + 5), f"{detail['sku']:03d}", font=font(17, True), fill=(72, 50, 31))
        icon = make_detail_icon(detail["sku"], 82)
        canvas.alpha_composite(icon, (x + (cell_w - icon.width) // 2, y + 24))
        count = f"×{detail['count']}"
        count_font = font(20, True)
        box = draw.textbbox((0, 0), count, font=count_font)
        count_x = x + (cell_w - (box[2] - box[0])) // 2
        draw.text((count_x, y + cell_h - 29), count, font=count_font, fill=(55, 43, 34))


def select_item(items: list[dict], order: int | None, scene_name: str | None) -> dict:
    for item in items:
        if order is not None and item["order"] == order:
            return item
        if scene_name is not None and item["name_cn"] == scene_name:
            return item
    raise RuntimeError("Requested scene was not found in metadata")


def main() -> None:
    args = parse_args()
    font, make_detail_icon, prepare_scene = import_pipeline(args.work_dir)
    items = json.loads(args.metadata.resolve().read_text(encoding="utf-8"))
    item = select_item(items, args.order, args.scene_name)

    raw_path = Path(item["raw_path"])
    if not raw_path.is_absolute():
        raw_path = args.metadata.resolve().parent / raw_path
    if not raw_path.exists():
        raise FileNotFoundError(raw_path)

    canvas = Image.new("RGBA", CANVAS, (248, 248, 246, 255))
    canvas.alpha_composite(sky_background())
    draw_divider(canvas)

    scene_area_width = 1120 if args.color_box else 1420
    scene = prepare_scene(raw_path, (scene_area_width, 820))
    x = 40 + (scene_area_width - scene.width) // 2 if args.color_box else (CANVAS[0] - scene.width) // 2
    y = 150 + (830 - scene.height) // 2
    if y < 145 or y + scene.height > 1025:
        raise RuntimeError("Scene exceeds approved scene zone")
    canvas.alpha_composite(scene, (x, y))
    if args.color_box:
        add_color_box(canvas, args.color_box.resolve())
    add_2cm_icon(canvas, font, make_detail_icon)

    draw = ImageDraw.Draw(canvas)
    draw.text((64, 38), args.title, font=font(56, True), fill=(42, 48, 51))
    name_box = draw.textbbox((0, 0), item["name_cn"], font=font(44, True))
    draw.text((1528 - (name_box[2] - name_box[0]), 34), item["name_cn"], font=font(44, True), fill=(43, 50, 53))
    pcs_text = f"{item['pcs']} PCS"
    pcs_box = draw.textbbox((0, 0), pcs_text, font=font(50, True))
    draw.text((1528 - (pcs_box[2] - pcs_box[0]), 92), pcs_text, font=font(50, True), fill=(232, 120, 24))
    add_parts_grid(canvas, item, font, make_detail_icon)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(args.output, quality=96)
    print(json.dumps({"output": str(args.output), "scene": item["name_cn"], "pcs": item["pcs"], "sku_types": len(item["sku_counts"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()
