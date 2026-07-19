from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


IDS = ("002", "006", "020", "026", "036", "076", "097", "107", "116", "155")
FACES = ("top", "front", "right")
SKILL_ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    source_root = SKILL_ROOT / "assets" / "structured_factory_redraw_v1"
    dual_root = SKILL_ROOT / "assets" / "dual_factory_library"
    exact_root = SKILL_ROOT / "assets" / "exact_factory_catalog_v3"
    manifest = json.loads((dual_root / "table2_manifest.json").read_text(encoding="utf-8"))
    records = {record["id"]: record for record in manifest["records"]}

    source_pngs = 0
    source_svgs = 0
    runtime_faces = 0
    for particle_id in IDS:
        record = records[particle_id]
        if record.get("structured_redraw", {}).get("profile") != "source_faithful_semantic_vector_v1":
            raise RuntimeError(f"Missing structured-redraw profile: {particle_id}")
        for face in FACES:
            png = source_root / particle_id / f"{particle_id}_{face}.png"
            svg = source_root / particle_id / f"{particle_id}_{face}.svg"
            if not png.is_file() or not svg.is_file():
                raise RuntimeError(f"Missing vector source: {particle_id} {face}")
            svg_text = svg.read_text(encoding="utf-8").lower()
            if "<image" in svg_text or "data:image" in svg_text:
                raise RuntimeError(f"Embedded raster found in SVG: {particle_id} {face}")
            with Image.open(png) as image:
                if image.size != (2048, 2048):
                    raise RuntimeError(f"Source PNG must be 2048 x 2048: {particle_id} {face}")
            runtime = dual_root / record["files"][face]["path"]
            with Image.open(runtime) as image:
                if image.size != (512, 512) or image.mode != "RGB":
                    raise RuntimeError(f"Invalid runtime face: {particle_id} {face}")
            if sha256(runtime) != record["files"][face]["sha256"]:
                raise RuntimeError(f"Runtime hash mismatch: {particle_id} {face}")
            source_pngs += 1
            source_svgs += 1
            runtime_faces += 1

        icon = exact_root / "icons" / f"{particle_id}.png"
        with Image.open(icon) as image:
            if image.size != (512, 512) or image.mode != "RGB":
                raise RuntimeError(f"Invalid exact catalog icon: {particle_id}")

    print(json.dumps({
        "status": "pass",
        "profile": "source_faithful_semantic_vector_v1",
        "particles": len(IDS),
        "source_pngs": source_pngs,
        "source_svgs": source_svgs,
        "runtime_faces": runtime_faces,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
