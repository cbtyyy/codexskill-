from __future__ import annotations

import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


# Base procedural drawing rules imported by build_locked_factory_faces.py.
# Factory overview crops are used only by that builder's visual contact sheet.
BASE_DIR = Path(__file__).resolve().parent
SOURCE_DIR = BASE_DIR / "xlsx_cubes"
OUTPUT_DIR = BASE_DIR / "redrawn_faces"
CONTACT_PATH = BASE_DIR / "redrawn_texture_comparison.png"
USED_SKUS = (
    6, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 23, 26, 27, 33,
    45, 48, 57, 59, 60, 66, 67, 73, 74, 75, 76, 78, 79, 80, 83,
    86, 87, 101, 102, 109, 129, 134, 151, 153, 154, 157, 161, 184,
)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "msyhbd.ttc" if bold else "msyh.ttc"
    return ImageFont.truetype(f"C:/Windows/Fonts/{name}", size)


def shade(color: tuple[int, int, int], factor: float) -> tuple[int, int, int]:
    return tuple(max(0, min(255, round(channel * factor))) for channel in color)


def canvas(color: tuple[int, int, int]) -> Image.Image:
    return Image.new("RGB", (16, 16), color)


def noise_texture(base, variants, seed: int, density: int = 38, patch: int = 2) -> Image.Image:
    image = canvas(base)
    draw = ImageDraw.Draw(image)
    rng = random.Random(seed)
    for _ in range(density):
        x = rng.randrange(16)
        y = rng.randrange(16)
        size = 1 if rng.random() < 0.72 else patch
        draw.rectangle((x, y, min(15, x + size - 1), min(15, y + size - 1)), fill=rng.choice(variants))
    return image


def stone_texture(seed: int, base=(122, 124, 125)) -> Image.Image:
    image = noise_texture(base, [shade(base, 0.78), shade(base, 0.9), shade(base, 1.15)], seed, 30, 2)
    draw = ImageDraw.Draw(image)
    for y, x0, length in ((3, 1, 6), (7, 8, 6), (11, 2, 7), (14, 10, 4)):
        draw.line((x0, y, min(15, x0 + length), y), fill=shade(base, 0.72))
    return image


def ore_texture(sku: int, accent: tuple[int, int, int]) -> Image.Image:
    image = stone_texture(sku)
    draw = ImageDraw.Draw(image)
    clusters = [((2, 3), (4, 4)), ((10, 2), (12, 4)), ((6, 8), (8, 10)), ((12, 11), (14, 13)), ((2, 12), (3, 14))]
    for index, ((x0, y0), (x1, y1)) in enumerate(clusters):
        color = shade(accent, 0.78 + (index % 3) * 0.14)
        draw.rectangle((x0, y0, x1, y1), fill=color)
        if index % 2 == 0:
            draw.point((x1, y0), fill=shade(accent, 1.18))
    return image


def cobble(seed: int, base=(112, 116, 116)) -> Image.Image:
    image = canvas(base)
    draw = ImageDraw.Draw(image)
    rows = [(0, [(0, 5), (6, 10), (11, 15)]), (5, [(0, 3), (4, 9), (10, 15)]), (10, [(0, 6), (7, 12), (13, 15)])]
    rng = random.Random(seed)
    for y, spans in rows:
        for x0, x1 in spans:
            draw.rectangle((x0, y, x1, min(15, y + 4)), fill=rng.choice([shade(base, 0.85), base, shade(base, 1.12)]))
            draw.line((x0, y, x1, y), fill=shade(base, 0.55))
            draw.line((x1, y, x1, min(15, y + 4)), fill=shade(base, 0.62))
    return image


def planks(base=(168, 126, 73), vertical: bool = False) -> Image.Image:
    image = canvas(base)
    draw = ImageDraw.Draw(image)
    if vertical:
        for x in (0, 4, 8, 12):
            draw.rectangle((x, 0, min(15, x + 3), 15), fill=shade(base, 0.9 if x % 8 else 1.08))
            draw.line((x, 0, x, 15), fill=shade(base, 0.58))
        draw.rectangle((6, 5, 7, 7), fill=shade(base, 0.62))
    else:
        for y in (0, 4, 8, 12):
            draw.rectangle((0, y, 15, min(15, y + 3)), fill=shade(base, 0.92 if y % 8 else 1.07))
            draw.line((0, y, 15, y), fill=shade(base, 0.58))
        draw.rectangle((3, 6, 6, 7), fill=shade(base, 0.65))
        draw.rectangle((11, 13, 13, 14), fill=shade(base, 0.7))
    return image


def bricks(base=(53, 52, 59), mortar=(25, 25, 30)) -> Image.Image:
    image = canvas(base)
    draw = ImageDraw.Draw(image)
    for y in (0, 4, 8, 12):
        draw.line((0, y, 15, y), fill=mortar)
        offset = 0 if (y // 4) % 2 == 0 else 4
        for x in range(offset, 16, 8):
            draw.line((x, y, x, min(15, y + 3)), fill=mortar)
    return image


def water(base=(44, 96, 220)) -> Image.Image:
    image = noise_texture(base, [shade(base, 0.84), shade(base, 1.14), (72, 142, 238)], 600, 22, 2)
    draw = ImageDraw.Draw(image)
    for y, x0 in ((3, 1), (7, 7), (11, 2), (14, 9)):
        draw.line((x0, y, min(15, x0 + 5), y), fill=(92, 164, 246))
    return image


def obsidian() -> Image.Image:
    base = (27, 24, 37)
    image = noise_texture(base, [(45, 28, 68), (66, 35, 92), (33, 30, 48)], 2300, 26, 1)
    ImageDraw.Draw(image).line((2, 13, 8, 11), fill=(76, 45, 106))
    return image


def glowstone() -> Image.Image:
    return noise_texture((196, 154, 86), [(248, 226, 139), (151, 103, 57), (232, 192, 111), (113, 76, 48)], 1800, 58, 2)


def log_face(top: bool = False) -> Image.Image:
    if top:
        image = canvas((184, 148, 91))
        draw = ImageDraw.Draw(image)
        for inset, color in ((1, (104, 73, 44)), (4, (146, 103, 58)), (7, (91, 63, 38))):
            draw.rectangle((inset, inset, 15 - inset, 15 - inset), outline=color)
        return image
    image = noise_texture((111, 82, 53), [(76, 55, 37), (142, 105, 65), (93, 67, 43)], 2600, 30, 1)
    draw = ImageDraw.Draw(image)
    for x in (2, 7, 12):
        draw.line((x, 0, x - 1, 15), fill=(72, 52, 36))
    return image


def leaves(flowers: bool = False) -> Image.Image:
    image = noise_texture((64, 132, 55), [(42, 103, 42), (92, 165, 69), (121, 180, 78)], 2700 + int(flowers), 54, 2)
    if flowers:
        draw = ImageDraw.Draw(image)
        for x, y in ((3, 4), (11, 3), (7, 10), (13, 13)):
            draw.rectangle((x, y, x + 1, y + 1), fill=(245, 241, 231))
            draw.point((x + 1, y + 1), fill=(242, 155, 175))
    return image


def cherry() -> Image.Image:
    image = noise_texture((243, 211, 224), [(255, 237, 244), (231, 165, 190), (214, 124, 158), (236, 190, 207)], 1540, 52, 2)
    draw = ImageDraw.Draw(image)
    for x, y in ((3, 4), (11, 2), (7, 9), (13, 12), (2, 13)):
        draw.rectangle((x, y, x + 1, y + 1), fill=(255, 247, 249))
        draw.point((x + 1, y + 1), fill=(208, 112, 147))
    return image


def magma(bright: bool = False) -> Image.Image:
    if bright:
        image = noise_texture((228, 51, 24), [(255, 118, 19), (255, 210, 50), (194, 28, 24)], 8700, 58, 2)
        draw = ImageDraw.Draw(image)
        for pts in (((1, 4), (7, 3)), ((8, 8), (14, 7)), ((2, 13), (8, 11))):
            draw.line(pts, fill=(255, 225, 67), width=2)
        return image
    return noise_texture((92, 43, 31), [(175, 66, 31), (225, 104, 35), (56, 34, 32), (248, 144, 45)], 8600, 54, 2)


def furnace() -> Image.Image:
    image = cobble(5900, (115, 118, 118))
    draw = ImageDraw.Draw(image)
    draw.rectangle((2, 3, 13, 10), fill=(65, 67, 67), outline=(180, 181, 178))
    draw.rectangle((4, 5, 11, 9), fill=(28, 29, 29))
    draw.rectangle((3, 11, 12, 15), fill=(95, 49, 30))
    draw.rectangle((5, 12, 10, 15), fill=(242, 81, 20))
    draw.rectangle((7, 11, 9, 15), fill=(255, 210, 42))
    return image


def crafting(top: bool = False) -> Image.Image:
    image = planks((150, 105, 62))
    draw = ImageDraw.Draw(image)
    if top:
        draw.rectangle((2, 2, 13, 13), fill=(173, 111, 68), outline=(61, 45, 32))
        for x in (5, 9):
            draw.line((x, 2, x, 13), fill=(78, 53, 35))
        for y in (5, 9):
            draw.line((2, y, 13, y), fill=(78, 53, 35))
    else:
        draw.rectangle((2, 2, 13, 13), outline=(57, 42, 29), width=2)
        draw.line((4, 11, 11, 4), fill=(205, 202, 184), width=2)
        draw.rectangle((9, 3, 12, 5), fill=(62, 65, 64))
    return image


def loom() -> Image.Image:
    image = planks((151, 112, 73), vertical=True)
    draw = ImageDraw.Draw(image)
    for x, color in ((3, (223, 190, 124)), (6, (187, 154, 98)), (9, (229, 199, 136)), (12, (171, 137, 86))):
        draw.rectangle((x, 2, x + 1, 12), fill=color)
    draw.rectangle((1, 13, 14, 15), fill=(89, 58, 36))
    return image


def enchant(top: bool = False) -> Image.Image:
    image = obsidian()
    draw = ImageDraw.Draw(image)
    if top:
        draw.rectangle((2, 2, 13, 13), fill=(130, 45, 48))
        draw.rectangle((0, 0, 3, 3), fill=(70, 220, 209))
        draw.rectangle((12, 0, 15, 3), fill=(70, 220, 209))
        draw.rectangle((4, 4, 11, 10), fill=(235, 225, 199), outline=(83, 65, 48))
        draw.line((8, 4, 8, 10), fill=(103, 71, 58))
    else:
        draw.rectangle((1, 0, 4, 3), fill=(65, 202, 195))
        draw.rectangle((11, 0, 14, 3), fill=(65, 202, 195))
        draw.rectangle((4, 1, 11, 3), fill=(139, 45, 49))
    return image


def bed(top: bool = False) -> Image.Image:
    if top:
        image = canvas((184, 45, 47))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, 15, 4), fill=(238, 237, 228))
        draw.line((0, 5, 15, 5), fill=(112, 31, 34))
        return image
    image = planks((151, 111, 69))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 15, 6), fill=(171, 40, 43))
    draw.line((0, 6, 15, 6), fill=(86, 31, 30))
    return image


def note_block() -> Image.Image:
    image = noise_texture((112, 70, 51), [(83, 49, 39), (142, 91, 62)], 7400, 28, 1)
    draw = ImageDraw.Draw(image)
    draw.rectangle((2, 2, 13, 13), fill=(89, 54, 43), outline=(49, 35, 30))
    for y in range(4, 13, 2):
        for x in range(4, 13, 2):
            draw.point((x, y), fill=(44, 36, 32))
    return image


def bookshelf() -> Image.Image:
    image = planks((159, 119, 72))
    draw = ImageDraw.Draw(image)
    draw.rectangle((1, 2, 14, 7), fill=(60, 50, 38))
    draw.rectangle((1, 9, 14, 14), fill=(60, 50, 38))
    colors = [(166, 49, 49), (40, 104, 154), (197, 156, 48), (57, 131, 73)]
    for row in (2, 9):
        for index, x in enumerate((2, 5, 8, 11)):
            draw.rectangle((x, row, x + 2, row + 4), fill=colors[(index + row) % len(colors)])
    return image


def chest(top: bool = False) -> Image.Image:
    image = planks((159, 104, 52))
    draw = ImageDraw.Draw(image)
    if top:
        draw.rectangle((1, 1, 14, 14), outline=(65, 45, 31), width=2)
    else:
        draw.line((0, 7, 15, 7), fill=(55, 40, 29), width=2)
        draw.rectangle((7, 6, 9, 10), fill=(208, 202, 151), outline=(68, 63, 49))
        draw.rectangle((0, 0, 15, 15), outline=(59, 43, 31))
    return image


def gift(top: bool = False) -> Image.Image:
    image = canvas((177, 41, 44))
    draw = ImageDraw.Draw(image)
    draw.rectangle((6, 0, 9, 15), fill=(239, 191, 62))
    draw.rectangle((0, 6, 15, 9), fill=(239, 191, 62))
    if top:
        draw.rectangle((3, 2, 6, 5), outline=(255, 220, 100))
        draw.rectangle((9, 2, 12, 5), outline=(255, 220, 100))
    return image


def hive(dark: bool = False) -> Image.Image:
    base = (154, 111, 66) if dark else (202, 159, 73)
    image = planks(base)
    draw = ImageDraw.Draw(image)
    draw.rectangle((4, 6, 11, 9), fill=(72, 54, 35))
    if not dark:
        draw.rectangle((6, 7, 9, 8), fill=(242, 192, 54))
    return image


def cake(top: bool = False) -> Image.Image:
    image = canvas((169, 92, 52))
    draw = ImageDraw.Draw(image)
    if top:
        draw.rectangle((0, 0, 15, 15), fill=(244, 240, 225))
        for x, y in ((3, 3), (11, 2), (7, 7), (13, 11), (4, 12)):
            draw.rectangle((x, y, x + 1, y + 1), fill=(226, 42, 48))
    else:
        draw.rectangle((0, 0, 15, 5), fill=(244, 240, 225))
        draw.line((0, 5, 15, 5), fill=(206, 196, 181))
        for x in (3, 9, 13):
            draw.rectangle((x, 2, x + 1, 3), fill=(226, 42, 48))
    return image


def character_face(kind: str) -> tuple[Image.Image, Image.Image, Image.Image]:
    if kind == "steve":
        skin, hair, eye = (152, 104, 77), (52, 42, 38), (70, 72, 158)
        top = canvas(hair)
        face = canvas(skin)
        d = ImageDraw.Draw(face)
        d.rectangle((0, 0, 15, 3), fill=hair)
        d.rectangle((2, 4, 4, 6), fill=(245, 242, 226)); d.rectangle((11, 4, 13, 6), fill=(245, 242, 226))
        d.rectangle((3, 5, 4, 6), fill=eye); d.rectangle((11, 5, 12, 6), fill=eye)
        d.rectangle((6, 8, 9, 10), fill=(119, 75, 59)); d.rectangle((4, 12, 11, 13), fill=(71, 42, 34))
        profile = canvas(hair); pd = ImageDraw.Draw(profile); pd.rectangle((0, 5, 9, 15), fill=skin); pd.rectangle((8, 7, 12, 11), fill=shade(skin, 0.85))
        return top, face, profile
    if kind == "alex":
        skin, hair = (236, 177, 133), (202, 103, 55)
        top = canvas(hair); face = canvas(skin); d = ImageDraw.Draw(face)
        d.rectangle((0, 0, 15, 3), fill=hair); d.rectangle((0, 3, 2, 15), fill=hair); d.rectangle((13, 3, 15, 15), fill=hair)
        for x in (4, 11): d.rectangle((x, 5, x + 1, 6), fill=(48, 110, 81))
        d.rectangle((6, 9, 9, 10), fill=(194, 121, 94)); d.rectangle((5, 12, 10, 12), fill=(136, 66, 53))
        profile = canvas(hair); ImageDraw.Draw(profile).rectangle((0, 5, 8, 15), fill=skin)
        return top, face, profile
    if kind == "creeper":
        base = (81, 175, 67); top = noise_texture(base, [(57, 138, 54), (113, 199, 83)], 109, 26, 2)
        face = top.copy(); d = ImageDraw.Draw(face); dark = (24, 54, 29)
        d.rectangle((3, 4, 6, 7), fill=dark); d.rectangle((10, 4, 13, 7), fill=dark)
        d.rectangle((6, 8, 10, 11), fill=dark); d.rectangle((4, 10, 6, 14), fill=dark); d.rectangle((10, 10, 12, 14), fill=dark)
        return top, face, top.copy()
    if kind == "zombie":
        base = (74, 126, 68); top = noise_texture(base, [(62, 107, 60), (91, 144, 79)], 129, 20, 2)
        face = top.copy(); d = ImageDraw.Draw(face); d.rectangle((3, 5, 5, 6), fill=(35, 43, 31)); d.rectangle((10, 5, 12, 6), fill=(35, 43, 31)); d.rectangle((5, 11, 11, 12), fill=(51, 58, 46))
        return top, face, top.copy()
    top = canvas((27, 27, 29)); face = top.copy(); d = ImageDraw.Draw(face)
    d.rectangle((2, 6, 6, 7), fill=(198, 58, 233)); d.rectangle((10, 6, 14, 7), fill=(198, 58, 233))
    return top, face, top.copy()


def farm_soil(top: bool = False) -> Image.Image:
    if top:
        image = noise_texture((95, 70, 45), [(72, 50, 34), (124, 88, 51)], 151, 28, 1)
        draw = ImageDraw.Draw(image)
        for x in (2, 6, 10, 14):
            draw.line((x, 0, x, 15), fill=(60, 46, 34))
        for x, y in ((3, 3), (8, 9), (12, 4)):
            draw.rectangle((x, y, x + 1, y + 2), fill=(76, 170, 64))
        return image
    return noise_texture((111, 76, 49), [(85, 56, 39), (139, 94, 58)], 152, 28, 2)


def make_faces(sku: int) -> dict[str, Image.Image]:
    if sku == 6: return {name: water() for name in ("top", "side", "front")}
    if sku == 9: return {name: noise_texture((77, 78, 78), [(45, 47, 48), (109, 111, 111), (133, 134, 131)], 900 + i, 48, 2) for i, name in enumerate(("top", "side", "front"))}
    ores = {10: (48, 48, 49), 11: (203, 155, 116), 13: (244, 181, 44), 14: (48, 75, 207), 15: (232, 45, 41), 16: (50, 218, 221), 17: (45, 208, 87)}
    if sku in ores: return {name: ore_texture(sku + i, ores[sku]) for i, name in enumerate(("top", "side", "front"))}
    if sku == 18: return {name: glowstone() for name in ("top", "side", "front")}
    if sku == 19: return {name: stone_texture(1900 + i) for i, name in enumerate(("top", "side", "front"))}
    if sku == 20: return {name: cobble(2000 + i) for i, name in enumerate(("top", "side", "front"))}
    if sku == 23: return {name: obsidian() for name in ("top", "side", "front")}
    if sku == 26: return {"top": log_face(True), "side": log_face(), "front": log_face()}
    if sku == 27: return {name: leaves() for name in ("top", "side", "front")}
    if sku == 33: return {"top": planks(), "side": planks(), "front": planks()}
    if sku == 45: return {name: bricks() for name in ("top", "side", "front")}
    if sku == 48: return {name: noise_texture((33, 34, 36), [(25, 26, 28), (43, 44, 46)], 4800 + i, 14, 1) for i, name in enumerate(("top", "side", "front"))}
    if sku == 57: return {name: noise_texture((137, 87, 181), [(105, 60, 151), (178, 125, 214), (211, 171, 231)], 5700 + i, 44, 2) for i, name in enumerate(("top", "side", "front"))}
    if sku == 59: return {"top": cobble(5901), "side": furnace(), "front": cobble(5902)}
    if sku == 60: return {"top": crafting(True), "side": crafting(), "front": crafting()}
    if sku == 66: return {name: loom() for name in ("top", "side", "front")}
    if sku == 67: return {"top": enchant(True), "side": enchant(), "front": enchant()}
    if sku == 73: return {"top": bed(True), "side": bed(), "front": bed()}
    if sku == 74: return {name: note_block() for name in ("top", "side", "front")}
    if sku == 75: return {"top": planks(), "side": bookshelf(), "front": bookshelf()}
    if sku == 76: return {"top": chest(True), "side": chest(), "front": chest()}
    if sku == 78: return {"top": gift(True), "side": gift(), "front": gift()}
    if sku == 79: return {name: hive(False) for name in ("top", "side", "front")}
    if sku == 80: return {name: hive(True) for name in ("top", "side", "front")}
    if sku == 83: return {"top": cake(True), "side": cake(), "front": cake()}
    if sku == 86: return {name: magma(False) for name in ("top", "side", "front")}
    if sku == 87: return {name: magma(True) for name in ("top", "side", "front")}
    if sku in {101, 102, 109, 129, 134}:
        kind = {101: "steve", 102: "alex", 109: "creeper", 129: "zombie", 134: "enderman"}[sku]
        top, face, profile = character_face(kind)
        return {"top": top, "side": face, "front": profile}
    if sku == 151: return {"top": farm_soil(True), "side": farm_soil(), "front": farm_soil()}
    if sku == 153: return {name: noise_texture((224, 153, 184), [(241, 181, 207), (203, 129, 164)], 1530 + i, 20, 2) for i, name in enumerate(("top", "side", "front"))}
    if sku == 154: return {name: cherry() for name in ("top", "side", "front")}
    if sku == 157: return {name: leaves(True) for name in ("top", "side", "front")}
    if sku == 161: return {name: water((74, 157, 207)) for name in ("top", "side", "front")}
    if sku == 184: return {name: bricks((54, 145, 193), (34, 94, 137)) for name in ("top", "side", "front")}
    raise KeyError(sku)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    previews = []
    for sku in USED_SKUS:
        faces = make_faces(sku)
        for name, image in faces.items():
            image.resize((256, 256), Image.Resampling.NEAREST).save(OUTPUT_DIR / f"sku_{sku:03d}_{name}.png")
        previews.append((sku, faces))

    tile_w, tile_h = 720, 190
    columns = 2
    rows = (len(previews) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * tile_w, rows * tile_h), (247, 247, 245))
    draw = ImageDraw.Draw(sheet)
    for index, (sku, faces) in enumerate(previews):
        x = (index % columns) * tile_w
        y = (index // columns) * tile_h
        source = Image.open(SOURCE_DIR / f"sku_{sku:03d}.png").convert("RGBA")
        source.thumbnail((150, 150), Image.Resampling.LANCZOS)
        sheet.paste(source.convert("RGB"), (x + 12, y + 28), source.getchannel("A"))
        draw.text((x + 12, y + 4), f"SKU {sku:03d}  Excel原图", font=font(16, True), fill=(35, 38, 41))
        for face_index, name in enumerate(("top", "side", "front")):
            preview = faces[name].resize((150, 150), Image.Resampling.NEAREST)
            px = x + 190 + face_index * 170
            sheet.paste(preview, (px, y + 28))
            draw.text((px, y + 4), f"重画{name}", font=font(16, True), fill=(35, 38, 41))
    sheet.save(CONTACT_PATH, quality=96)
    print(CONTACT_PATH)


if __name__ == "__main__":
    raise SystemExit("Run build_locked_factory_faces.py to rebuild the approved library.")
