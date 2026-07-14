from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


SKILL_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = SKILL_ROOT / "references/locked-factory-faces-v1.json"
EXPECTED_FACE_NAMES = {"top", "side", "front"}
EXPECTED_SIZE = (512, 512)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    errors: list[str] = []
    seen_skus: set[str] = set()
    seen_paths: set[Path] = set()

    for entry in manifest.get("skus", []):
        sku = entry.get("sku", "")
        if sku in seen_skus:
            errors.append(f"duplicate SKU: {sku}")
        seen_skus.add(sku)
        metadata_status = entry.get("metadata_status")
        if metadata_status not in {"complete", "id_only"}:
            errors.append(f"SKU {sku}: invalid Excel metadata status")
        if metadata_status == "complete" and (not entry.get("name") or not entry.get("size")):
            errors.append(f"SKU {sku}: incomplete Excel metadata marked complete")

        files = entry.get("files", {})
        if set(files) != EXPECTED_FACE_NAMES:
            errors.append(f"SKU {sku}: faces must be top/side/front")

        for face_name, file_info in files.items():
            relative = Path(file_info["path"])
            path = (SKILL_ROOT / relative).resolve()
            if SKILL_ROOT.resolve() not in path.parents:
                errors.append(f"SKU {sku} {face_name}: path leaves skill root")
                continue
            if path in seen_paths:
                errors.append(f"duplicate file path: {relative.as_posix()}")
            seen_paths.add(path)
            if not path.exists():
                errors.append(f"missing: {relative.as_posix()}")
                continue

            with Image.open(path) as image:
                if image.size != EXPECTED_SIZE:
                    errors.append(f"{relative.as_posix()}: size {image.size}")
                if image.mode != "RGB":
                    errors.append(f"{relative.as_posix()}: mode {image.mode}")

            actual_hash = sha256(path)
            if actual_hash != file_info.get("sha256"):
                errors.append(f"{relative.as_posix()}: SHA-256 mismatch")

    if len(seen_skus) != 64:
        errors.append(f"expected 64 SKUs, found {len(seen_skus)}")
    if len(seen_paths) != 192:
        errors.append(f"expected 192 faces, found {len(seen_paths)}")

    result = {
        "status": "pass" if not errors else "fail",
        "manifest": MANIFEST_PATH.relative_to(SKILL_ROOT).as_posix(),
        "skus": len(seen_skus),
        "faces": len(seen_paths),
        "errors": errors,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
