from __future__ import annotations

import hashlib
import json
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
    report = {
        "passed": not errors,
        "checked_files": len(manifest.get("files", [])),
        "scene_particle_count": manifest.get("scene_particle_count"),
        "errors": errors,
    }
    print(json.dumps(report, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
