from __future__ import annotations

import hashlib
import json
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree

from PIL import Image


EXPECTED_IDS = [f"{value:03d}" for value in range(1, 186)] + [
    "207",
    "273",
    "283",
    "289",
    "484",
    "485",
    "486",
    "A01",
    "A02",
    "A03",
    "270",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate(root: Path) -> dict[str, object]:
    catalog = root / "assets" / "exact_factory_catalog_v3"
    manifest_path = catalog / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    require(manifest["library_id"] == "exact_factory_catalog_v3", "wrong library_id")
    particles = manifest["particles"]
    ids = [record["id"] for record in particles]
    require(ids == EXPECTED_IDS, "particle ID order or membership changed")
    require(len(ids) == len(set(ids)) == 196, "particle IDs must be 196 unique values")
    require(manifest["particle_count"] == 196, "particle_count must be 196")

    for record in particles:
        icon = catalog / record["icon"]
        require(icon.is_file(), f"missing icon: {record['id']}")
        require(sha256(icon) == record["sha256"], f"hash mismatch: {record['id']}")
        with Image.open(icon) as image:
            require(list(image.size) == [record["width"], record["height"]], f"size mismatch: {record['id']}")
            require(image.mode == record["mode"], f"mode mismatch: {record['id']}")
            require(image.size == (512, 512), f"icon must be 512 x 512: {record['id']}")

    workbook = catalog / manifest["workbook"]["path"]
    overview = catalog / manifest["overview"]["path"]
    require(workbook.is_file(), "catalog workbook is missing")
    require(overview.is_file(), "catalog overview is missing")
    require(sha256(workbook) == manifest["workbook"]["sha256"], "workbook hash mismatch")
    require(sha256(overview) == manifest["overview"]["sha256"], "overview hash mismatch")

    with Image.open(overview) as image:
        require(image.size == (2400, 7250), "overview must be 2400 x 7250")

    with zipfile.ZipFile(workbook) as archive:
        media = [name for name in archive.namelist() if name.startswith("xl/media/")]
        anchors = 0
        for name in archive.namelist():
            if not name.startswith("xl/drawings/drawing") or not name.endswith(".xml"):
                continue
            root_node = ElementTree.fromstring(archive.read(name))
            anchors += sum(1 for node in root_node if node.tag.endswith("CellAnchor"))
        require(len(media) == 196, f"workbook must embed 196 images, found {len(media)}")
        require(anchors == 196, f"workbook must anchor 196 images, found {anchors}")

    return {
        "library_id": manifest["library_id"],
        "particles": len(particles),
        "workbook_images": len(media),
        "workbook_anchors": anchors,
        "overview_size": [2400, 7250],
    }


def main() -> int:
    skill_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    print(json.dumps(validate(skill_root), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
