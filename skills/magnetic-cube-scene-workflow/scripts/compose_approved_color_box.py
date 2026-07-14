from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont


SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MASTER = SKILL_ROOT / "assets" / "approved-color-box-master.png"
DEFAULT_FRONT_QUAD = ((129, 84), (1087, 69), (1087, 690), (129, 738))
PANEL_SIZE = (1920, 1260)
IMPACT_FONT = Path("C:/Windows/Fonts/impact.ttf")
ARIAL_BOLD_FONT = Path("C:/Windows/Fonts/arialbd.ttf")


def parse_points(value: str, count: int) -> tuple[tuple[int, int], ...]:
    points = []
    for item in value.split(";"):
        coordinates = item.split(",")
        if len(coordinates) != 2:
            raise argparse.ArgumentTypeError(f"Invalid point: {item}")
        points.append((int(coordinates[0]), int(coordinates[1])))
    if len(points) != count:
        raise argparse.ArgumentTypeError(f"Expected {count} points, got {len(points)}")
    return tuple(points)


def parse_box(value: str) -> tuple[int, int, int, int]:
    coordinates = tuple(int(item) for item in value.split(","))
    if len(coordinates) != 4:
        raise argparse.ArgumentTypeError("Crop boxes use left,top,right,bottom")
    return coordinates


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compose the approved magnetic-cube front panel onto the locked 3D box master."
    )
    parser.add_argument("--scene", type=Path, required=True, help="Transparent Blender scene PNG.")
    parser.add_argument("--output", type=Path, required=True, help="White-background output PNG.")
    parser.add_argument("--cutout-output", type=Path, help="Optional transparent output PNG.")
    parser.add_argument("--master", type=Path, default=DEFAULT_MASTER)
    parser.add_argument(
        "--front-quad",
        type=lambda value: parse_points(value, 4),
        default=DEFAULT_FRONT_QUAD,
        help="Clockwise front corners: x,y;x,y;x,y;x,y.",
    )
    parser.add_argument("--title-crop", type=parse_box, default=(175, 112, 518, 292))
    parser.add_argument("--age-crop", type=parse_box, default=(998, 236, 1072, 314))
    parser.add_argument("--no-age", action="store_true", help="Do not place the 3+ badge.")
    return parser.parse_args()


def crop_alpha(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    bounds = rgba.getchannel("A").getbbox()
    return rgba.crop(bounds) if bounds else rgba


def extract_dark_art(master: Image.Image, box: tuple[int, int, int, int]) -> Image.Image:
    crop = master.crop(box).convert("RGBA")
    source = crop.convert("RGB").load()
    mask = Image.new("L", crop.size, 0)
    target = mask.load()
    for y in range(crop.height):
        for x in range(crop.width):
            red, green, blue = source[x, y]
            if red < 65 and green < 80 and blue < 105:
                target[x, y] = 255
    mask = mask.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(0.35))
    crop.putalpha(mask)
    return crop_alpha(crop)


def extract_age_badge(master: Image.Image, box: tuple[int, int, int, int]) -> Image.Image:
    crop = master.crop(box).convert("RGBA")
    source = crop.convert("RGB").load()
    mask = Image.new("L", crop.size, 0)
    target = mask.load()
    for y in range(crop.height):
        for x in range(crop.width):
            red, green, blue = source[x, y]
            orange = red > 170 and green > 85 and blue < 135 and red > green + 35 and red > blue + 75
            white = red > 215 and green > 215 and blue > 195
            if orange or white:
                target[x, y] = 255
    mask = mask.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(0.35))
    crop.putalpha(mask)
    return crop_alpha(crop)


def shifted_mask(mask: Image.Image, x: int, y: int) -> Image.Image:
    shifted = Image.new("L", mask.size, 0)
    shifted.paste(mask, (x, y))
    return shifted


def metallic_text_line(text: str, font_size: int) -> Image.Image:
    font = ImageFont.truetype(str(IMPACT_FONT), font_size)
    left, top, right, bottom = font.getbbox(text)
    padding = 34
    extrusion = 20
    size = (right - left + padding * 2 + extrusion, bottom - top + padding * 2 + extrusion)
    origin = (padding - left, padding - top)
    face_mask = Image.new("L", size, 0)
    ImageDraw.Draw(face_mask).text(origin, text, font=font, fill=255)

    result = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(result)
    for depth in range(extrusion, 0, -2):
        draw.text(
            (origin[0] + depth, origin[1] + depth),
            text,
            font=font,
            fill=(47, 51, 52, 255),
            stroke_width=13,
            stroke_fill=(16, 20, 24, 255),
        )
    draw.text(
        origin,
        text,
        font=font,
        fill=(150, 154, 154, 255),
        stroke_width=13,
        stroke_fill=(18, 23, 28, 255),
    )

    gradient = Image.new("RGBA", size, (0, 0, 0, 0))
    gradient_draw = ImageDraw.Draw(gradient)
    face_top = max(0, top + origin[1])
    face_bottom = min(size[1] - 1, bottom + origin[1])
    for y in range(face_top, face_bottom + 1):
        ratio = (y - face_top) / max(1, face_bottom - face_top)
        if ratio < 0.28:
            local = ratio / 0.28
            start, end = (232, 235, 231), (181, 186, 185)
        else:
            local = (ratio - 0.28) / 0.72
            start, end = (181, 186, 185), (103, 108, 110)
        value = tuple(round(start[index] * (1 - local) + end[index] * local) for index in range(3))
        gradient_draw.line((0, y, size[0], y), fill=(*value, 255))
    result.alpha_composite(Image.composite(gradient, Image.new("RGBA", size), face_mask))

    top_edge = ImageChops.subtract(face_mask, shifted_mask(face_mask, 0, 4))
    highlight = Image.new("RGBA", size, (244, 246, 240, 0))
    highlight.putalpha(top_edge.point(lambda value: round(value * 0.78)))
    result.alpha_composite(highlight)
    return crop_alpha(result)


def make_metallic_title() -> Image.Image:
    first = metallic_text_line("MAGNETIC", 164)
    second = metallic_text_line("CUBE", 184)
    width = max(first.width, second.width)
    group = Image.new("RGBA", (width, first.height + second.height - 22), (0, 0, 0, 0))
    group.alpha_composite(first, (0, 0))
    group.alpha_composite(second, (8, first.height - 22))
    group.thumbnail((650, 330), Image.Resampling.LANCZOS)
    return group


def make_age_badge() -> Image.Image:
    size = (168, 136)
    badge = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(badge)
    draw.rounded_rectangle((4, 4, 163, 131), radius=19, fill=(255, 255, 248, 255))
    draw.rounded_rectangle((14, 14, 153, 121), radius=14, fill=(246, 164, 17, 255))
    font = ImageFont.truetype(str(ARIAL_BOLD_FONT), 78)
    text = "3+"
    box = draw.textbbox((0, 0), text, font=font, stroke_width=1)
    x = (size[0] - (box[2] - box[0])) // 2 - box[0]
    y = (size[1] - (box[3] - box[1])) // 2 - box[1] - 2
    draw.text(
        (x, y),
        text,
        font=font,
        fill=(255, 255, 255, 255),
        stroke_width=1,
        stroke_fill=(255, 255, 255, 255),
    )
    return badge


def make_panel_sky(size: tuple[int, int]) -> Image.Image:
    width, height = size
    sky = Image.new("RGBA", size)
    draw = ImageDraw.Draw(sky)
    anchors = (
        (70, (174, 230, 249, 255)),
        (600, (211, 241, 250, 255)),
        (1160, (239, 249, 249, 255)),
    )
    for y in range(height):
        if y <= anchors[1][0]:
            y0, color0 = anchors[0]
            y1, color1 = anchors[1]
        else:
            y0, color0 = anchors[1]
            y1, color1 = anchors[2]
        ratio = min(1.0, max(0.0, (y - y0) / max(1, y1 - y0)))
        color = tuple(round(color0[index] * (1 - ratio) + color1[index] * ratio) for index in range(4))
        draw.line((0, y, width, y), fill=color)
    return sky


def draw_integrated_frame(panel: Image.Image) -> None:
    width, height = panel.size
    cell = 64
    palette = (
        (67, 151, 28, 255),
        (79, 166, 30, 255),
        (96, 181, 34, 255),
        (119, 193, 37, 255),
        (158, 207, 31, 255),
        (222, 222, 24, 255),
    )
    draw = ImageDraw.Draw(panel)
    columns = (width + cell - 1) // cell
    rows = (height + cell - 1) // cell
    frame_cells: set[tuple[int, int]] = set()

    for row in range(rows):
        for column in range(columns):
            if row < 2 or row >= rows - 2 or column < 2 or column >= columns - 2:
                frame_cells.add((column, row))

    for row, end_column in ((2, 10), (3, 10), (4, 9), (5, 8)):
        for column in range(2, end_column + 1):
            frame_cells.add((column, row))

    top_tabs = ((11, 12, 1), (15, 16, 2), (20, 22, 1), (25, 26, 1))
    bottom_tabs = ((4, 6, 1), (9, 10, 2), (14, 16, 1), (20, 22, 1), (25, 27, 2))
    left_tabs = ((7, 8, 1), (10, 12, 2), (15, 17, 1))
    right_tabs = ((4, 5, 1), (8, 10, 2), (13, 15, 1))
    for start, end, depth in top_tabs:
        for column in range(start, end + 1):
            for offset in range(depth):
                frame_cells.add((column, 2 + offset))
    for start, end, depth in bottom_tabs:
        for column in range(start, end + 1):
            for offset in range(depth):
                frame_cells.add((column, rows - 3 - offset))
    for start, end, depth in left_tabs:
        for row in range(start, end + 1):
            for offset in range(depth):
                frame_cells.add((2 + offset, row))
    for start, end, depth in right_tabs:
        for row in range(start, end + 1):
            for offset in range(depth):
                frame_cells.add((columns - 3 - offset, row))

    for column, row in sorted(frame_cells, key=lambda item: (item[1], item[0])):
        edge_distance = min(column, row, columns - 1 - column, rows - 1 - row)
        value = (column * 13 + row * 19 + column * row * 5) % 29
        if edge_distance >= 2:
            palette_index = 3 if value < 17 else 4
        elif value < 12:
            palette_index = 1
        elif value < 21:
            palette_index = 2
        elif value < 27:
            palette_index = 3
        else:
            palette_index = 5
        x0 = column * cell
        y0 = row * cell
        draw.rectangle(
            (x0, y0, min(x0 + cell, width), min(y0 + cell, height)),
            fill=palette[palette_index],
        )


def build_panel(
    master: Image.Image,
    scene_path: Path,
    title_crop: tuple[int, int, int, int],
    age_crop: tuple[int, int, int, int],
    include_age: bool,
) -> Image.Image:
    width, height = PANEL_SIZE
    panel = make_panel_sky(PANEL_SIZE)
    draw_integrated_frame(panel)

    title = make_metallic_title()
    panel.alpha_composite(title, (145, 118))

    scene = crop_alpha(Image.open(scene_path))
    alpha = scene.getchannel("A")
    color = ImageEnhance.Color(scene.convert("RGB")).enhance(1.18)
    color = ImageEnhance.Contrast(color).enhance(1.035)
    color = ImageEnhance.Brightness(color).enhance(1.025)
    scene = color.convert("RGBA")
    scene.putalpha(alpha)
    scene.thumbnail((1370, 920), Image.Resampling.LANCZOS)
    scene = scene.filter(ImageFilter.GaussianBlur(0.24))
    scene_x = 420 + (1370 - scene.width) // 2
    scene_y = 145 + (920 - scene.height) // 2

    shadow = Image.new("RGBA", PANEL_SIZE, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.ellipse(
        (
            scene_x + round(scene.width * 0.16),
            scene_y + round(scene.height * 0.70),
            scene_x + round(scene.width * 0.90),
            scene_y + round(scene.height * 0.91),
        ),
        fill=(47, 87, 91, 32),
    )
    panel.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(24)))
    panel.alpha_composite(scene, (scene_x, scene_y))

    if include_age:
        age_badge = make_age_badge()
        panel.alpha_composite(age_badge, (1518, 207))

    lighting = Image.new("RGBA", PANEL_SIZE, (0, 0, 0, 0))
    lighting_draw = ImageDraw.Draw(lighting)
    for x in range(width):
        opacity = max(0, round((x / width - 0.72) * 22))
        if opacity:
            lighting_draw.line((x, 0, x, height), fill=(0, 28, 12, opacity))
    return Image.alpha_composite(panel, lighting).filter(ImageFilter.GaussianBlur(0.35))


def perspective_coefficients(
    destination: tuple[tuple[float, float], ...],
    source: tuple[tuple[float, float], ...],
) -> tuple[float, ...]:
    matrix = []
    values = []
    for (x, y), (u, v) in zip(destination, source):
        matrix.append((x, y, 1, 0, 0, 0, -u * x, -u * y))
        values.append(u)
        matrix.append((0, 0, 0, x, y, 1, -v * x, -v * y))
        values.append(v)
    result = np.linalg.solve(np.asarray(matrix, dtype=float), np.asarray(values, dtype=float))
    return tuple(float(value) for value in result)


def edge_connected_white_cutout(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    rgb = rgba.convert("RGB")
    candidate = Image.new("L", rgb.size, 0)
    candidate_pixels = candidate.load()
    source_pixels = rgb.load()
    for y in range(rgb.height):
        for x in range(rgb.width):
            red, green, blue = source_pixels[x, y]
            if min(red, green, blue) >= 225 and max(red, green, blue) - min(red, green, blue) <= 20:
                candidate_pixels[x, y] = 255
    ImageDraw.floodfill(candidate, (0, 0), 128, thresh=0)
    connected = candidate.point(lambda value: 255 if value == 128 else 0)
    connected = connected.filter(ImageFilter.GaussianBlur(0.8))
    rgba.putalpha(connected.point(lambda value: 255 - value))
    return rgba


def main() -> None:
    args = parse_args()
    if not args.master.exists():
        raise FileNotFoundError(args.master)
    if not args.scene.exists():
        raise FileNotFoundError(args.scene)
    master = Image.open(args.master).convert("RGBA")
    if args.master.resolve() == DEFAULT_MASTER.resolve() and master.size != (1138, 771):
        raise RuntimeError(f"Approved master must be 1138x771, got {master.size}")

    panel = build_panel(master, args.scene, args.title_crop, args.age_crop, not args.no_age)
    panel_width, panel_height = panel.size
    source_quad = (
        (0.0, 0.0),
        (panel_width - 1.0, 0.0),
        (panel_width - 1.0, panel_height - 1.0),
        (0.0, panel_height - 1.0),
    )
    coefficients = perspective_coefficients(args.front_quad, source_quad)
    warped = panel.transform(
        master.size,
        Image.Transform.PERSPECTIVE,
        coefficients,
        resample=Image.Resampling.BICUBIC,
        fillcolor=(0, 0, 0, 0),
    )
    master.alpha_composite(warped)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    master.convert("RGB").save(args.output)
    if args.cutout_output:
        args.cutout_output.parent.mkdir(parents=True, exist_ok=True)
        edge_connected_white_cutout(master).save(args.cutout_output)
    print(args.output)
    if args.cutout_output:
        print(args.cutout_output)


if __name__ == "__main__":
    main()
