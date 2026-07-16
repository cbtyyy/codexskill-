from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter


SKILL_ROOT = Path(__file__).resolve().parents[1]
LIBRARY_ROOT = Path(
    os.environ.get(
        "MAGNETIC_DUAL_LIBRARY_ROOT",
        str(SKILL_ROOT / "assets" / "dual_factory_library"),
    )
)
SOURCE_VERSIONS = {
    "table1": "table1_three_visible_faces_v3",
    "table2": "table2_three_visible_faces_v3",
}
TARGET_VERSIONS = {
    "table1": "table1_three_visible_faces_v4",
    "table2": "table2_three_visible_faces_v4",
}
SOURCE_PROFILE_NAME = "fine_print_v3"
TARGET_PROFILE = {
    "name": "fine_print_v4_balanced_smooth",
    "source_profile": SOURCE_PROFILE_NAME,
    "unsharp_radius": 0.9,
    "unsharp_percent": 145,
    "unsharp_threshold": 1,
    "contrast_factor": 1.09,
    "saturation_factor": 1.018,
    "soften_radius": 0.9,
    "soften_blend": 0.3,
    "texture_interpolation": "Linear",
    "geometry_policy": "Preserve source artwork, line positions, and face registration exactly.",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def apply_profile(source: Image.Image) -> Image.Image:
    image = source.convert("RGB")
    image = image.filter(
        ImageFilter.UnsharpMask(
            radius=TARGET_PROFILE["unsharp_radius"],
            percent=TARGET_PROFILE["unsharp_percent"],
            threshold=TARGET_PROFILE["unsharp_threshold"],
        )
    )
    image = ImageEnhance.Contrast(image).enhance(TARGET_PROFILE["contrast_factor"])
    image = ImageEnhance.Color(image).enhance(TARGET_PROFILE["saturation_factor"])
    softened = image.filter(
        ImageFilter.GaussianBlur(radius=TARGET_PROFILE["soften_radius"])
    )
    return Image.blend(image, softened, TARGET_PROFILE["soften_blend"])


def atomic_save(image: Image.Image, path: Path) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    # Standard lossless compression is materially faster for the 1,455-face
    # library and produces identical decoded RGB pixels to optimize=True.
    image.save(temporary, format="PNG", compress_level=6)
    temporary.replace(path)


def upgrade_manifest(library_id: str) -> tuple[int, int]:
    manifest_path = LIBRARY_ROOT / f"{library_id}_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if (
        manifest.get("version") == TARGET_VERSIONS[library_id]
        and manifest.get("texture_profile") == TARGET_PROFILE
    ):
        return 0, sum(bool(record.get("scene_eligible")) for record in manifest["records"])
    if manifest.get("version") != SOURCE_VERSIONS[library_id]:
        raise RuntimeError(f"Unexpected source version: {manifest_path}")
    if manifest.get("texture_profile", {}).get("name") != SOURCE_PROFILE_NAME:
        raise RuntimeError(f"Unexpected source texture profile: {manifest_path}")

    unique_paths: dict[str, Path] = {}
    for record in manifest["records"]:
        if not record.get("scene_eligible"):
            continue
        for file_info in record["files"].values():
            relative = file_info["path"]
            unique_paths[relative] = LIBRARY_ROOT / relative

    for path in unique_paths.values():
        with Image.open(path) as source:
            output = apply_profile(source)
        if output.size != (512, 512) or output.mode != "RGB":
            raise RuntimeError(f"Invalid processed face: {path}")
        atomic_save(output, path)

    hashes = {relative: sha256(path) for relative, path in unique_paths.items()}
    for record in manifest["records"]:
        if not record.get("scene_eligible"):
            continue
        for file_info in record["files"].values():
            file_info["sha256"] = hashes[file_info["path"]]

    manifest["version"] = TARGET_VERSIONS[library_id]
    manifest["texture_profile"] = TARGET_PROFILE
    manifest["render_policy"] = (
        manifest["render_policy"].rstrip(".")
        + "; apply the approved balanced-clear pass and lightly blend internal high-frequency blocks."
    )
    temporary = manifest_path.with_suffix(".json.tmp")
    temporary.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    temporary.replace(manifest_path)
    return len(unique_paths), sum(
        bool(record.get("scene_eligible")) for record in manifest["records"]
    )


def main() -> None:
    if not LIBRARY_ROOT.exists():
        raise FileNotFoundError(LIBRARY_ROOT)
    result = {}
    for library_id in ("table1", "table2"):
        faces, records = upgrade_manifest(library_id)
        result[library_id] = {"processed_faces": faces, "eligible_records": records}
    print(
        json.dumps(
            {"status": "pass", "root": str(LIBRARY_ROOT), "result": result},
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
