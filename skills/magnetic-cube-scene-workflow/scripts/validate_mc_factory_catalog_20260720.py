from __future__ import annotations

import hashlib
import json
import struct
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
ROOT = SKILL_ROOT / "assets" / "mc_factory_catalog_20260720"
MANIFEST = ROOT / "manifest.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        signature = handle.read(24)
    if signature[:8] != b"\x89PNG\r\n\x1a\n" or signature[12:16] != b"IHDR":
        raise RuntimeError(f"invalid PNG header: {path}")
    return struct.unpack(">II", signature[16:24])


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    errors = []
    if manifest.get("library_id") != "mc_factory_catalog_20260720":
        errors.append("unexpected library_id")
    expected = {
        "particle_svg_count": 196,
        "scene_particle_count": 192,
        "face_svg_count": 576,
        "face_png_count": 576,
        "embedded_raster_svg_count": 0,
    }
    for key, value in expected.items():
        if manifest.get(key) != value:
            errors.append(f"{key}: expected {value}, got {manifest.get(key)}")
    for record in manifest.get("files", []):
        path = ROOT / record["path"]
        if not path.exists():
            errors.append(f"missing {record['path']}")
            continue
        if path.stat().st_size != record["size"]:
            errors.append(f"size mismatch {record['path']}")
        elif sha256(path) != record["sha256"]:
            errors.append(f"hash mismatch {record['path']}")
    for identifier in manifest.get("scene_particle_ids", []):
        for face in ("top", "front", "right"):
            if not (ROOT / "face_svg" / identifier / f"{face}.svg").exists():
                errors.append(f"missing SVG face {identifier}/{face}")
            if not (ROOT / "face_png" / identifier / f"{face}.png").exists():
                errors.append(f"missing PNG face {identifier}/{face}")

    particles = {record["id"]: record for record in manifest.get("particles", [])}
    if set(particles) != set(manifest.get("scene_particle_ids", [])):
        errors.append("particle dimension records do not match scene_particle_ids")
    rectangular_ids = {
        identifier
        for identifier, record in particles.items()
        if record.get("shape") == "rectangular_prism"
    }
    expected_rectangular_ids = {"073", "095", "096", "097", "098"}
    if rectangular_ids != expected_rectangular_ids:
        errors.append(
            f"rectangular IDs: expected {sorted(expected_rectangular_ids)}, "
            f"got {sorted(rectangular_ids)}"
        )
    for identifier, record in particles.items():
        is_rectangular = identifier in expected_rectangular_ids
        expected_size = [4, 2, 2] if is_rectangular else [2, 2, 2]
        expected_units = [2, 1, 1] if is_rectangular else [1, 1, 1]
        if record.get("physical_size_cm") != expected_size:
            errors.append(f"physical size mismatch {identifier}")
        if record.get("geometry_units") != expected_units:
            errors.append(f"geometry units mismatch {identifier}")
        if record.get("pcs_per_object") != 1:
            errors.append(f"PCS rule mismatch {identifier}")
        if is_rectangular:
            if record.get("default_orientation") != "horizontal_x":
                errors.append(f"default orientation mismatch {identifier}")
            if record.get("allowed_rotations") != [
                "horizontal_x",
                "horizontal_y",
                "upright_z",
            ]:
                errors.append(f"allowed rotations mismatch {identifier}")

    expected_face_sizes = {
        "073": {"top": (4096, 2048), "front": (4096, 2048), "right": (2048, 2048)},
        "095": {"top": (2048, 2048), "front": (2048, 4096), "right": (2048, 4096)},
        "096": {"top": (2048, 2048), "front": (2048, 4096), "right": (2048, 4096)},
        "097": {"top": (2048, 2048), "front": (2048, 4096), "right": (2048, 4096)},
        "098": {"top": (2048, 2048), "front": (2048, 4096), "right": (2048, 4096)},
    }
    for identifier in expected_rectangular_ids:
        for face, expected_size in expected_face_sizes[identifier].items():
            path = ROOT / "face_png" / identifier / f"{face}.png"
            if path.exists() and png_size(path) != expected_size:
                errors.append(
                    f"face aspect mismatch {identifier}/{face}: "
                    f"expected {expected_size}, got {png_size(path)}"
                )
    report = {
        "passed": not errors,
        "checked_files": len(manifest.get("files", [])),
        "scene_particle_count": manifest.get("scene_particle_count"),
        "rectangular_particle_count": len(rectangular_ids),
        "errors": errors,
    }
    print(json.dumps(report, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
