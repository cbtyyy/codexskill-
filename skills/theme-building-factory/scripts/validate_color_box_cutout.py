from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image


SKILL_ROOT = Path(__file__).resolve().parents[1]
CUTOUT_PATH = SKILL_ROOT / "assets/approved-universal-color-box-cutout.png"


def main() -> None:
    image = Image.open(CUTOUT_PATH).convert("RGBA")
    pixels = np.asarray(image)
    alpha = pixels[:, :, 3]
    rgb = pixels[:, :, :3]
    bbox = image.getchannel("A").getbbox()
    errors: list[str] = []

    if image.size != (1138, 771):
        errors.append(f"unexpected cutout size: {image.size}")
    if bbox is None:
        errors.append("cutout alpha is empty")
    elif not (
        64 <= bbox[0] <= 70
        and 48 <= bbox[1] <= 55
        and 1087 <= bbox[2] <= 1090
        and 739 <= bbox[3] <= 743
    ):
        errors.append(f"cutout alpha bounds include studio residue: {bbox}")

    transparent_rgb = int(((alpha == 0) & (rgb.max(axis=2) > 0)).sum())
    if transparent_rgb:
        errors.append(f"transparent pixels retain RGB: {transparent_rgb}")

    result = {
        "status": "pass" if not errors else "fail",
        "path": CUTOUT_PATH.relative_to(SKILL_ROOT).as_posix(),
        "size": list(image.size),
        "alpha_bbox": list(bbox) if bbox else None,
        "transparent_rgb_pixels": transparent_rgb,
        "errors": errors,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
