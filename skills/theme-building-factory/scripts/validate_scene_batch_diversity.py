from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


AXES = (
    "footprint",
    "primary_mass",
    "major_void",
    "height_rhythm",
    "foreground_path",
)
REQUIRED_SIGNATURE_FIELDS = ("template_id", "archetype", *AXES)


def load_scenes(path: Path) -> list[dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    scenes = payload.get("scenes") if isinstance(payload, dict) else payload
    if not isinstance(scenes, list) or not scenes:
        raise ValueError("Metadata must be a non-empty list or contain a scenes list")
    return scenes


def band(pcs: int) -> str:
    if 80 <= pcs <= 119:
        return "80-119"
    if 120 <= pcs <= 159:
        return "120-159"
    if 160 <= pcs <= 200:
        return "160-200"
    return "out-of-range"


def axis_difference(left: dict, right: dict) -> int:
    return sum(left[name] != right[name] for name in AXES)


def validate(scenes: list[dict]) -> dict:
    errors: list[str] = []
    signatures: list[dict] = []
    names: list[str] = []
    pcs_values: list[int] = []

    for index, scene in enumerate(scenes, start=1):
        name = str(scene.get("name") or scene.get("name_cn") or f"scene-{index}")
        names.append(name)
        pcs = scene.get("pcs")
        if not isinstance(pcs, int) or isinstance(pcs, bool):
            errors.append(f"{name}: pcs must be an integer")
            pcs = -1
        elif not 80 <= pcs <= 200:
            errors.append(f"{name}: {pcs} PCS is outside 80-200")
        pcs_values.append(pcs)

        signature = scene.get("structure_signature")
        if not isinstance(signature, dict):
            errors.append(f"{name}: missing structure_signature")
            signature = {}
        missing = [field for field in REQUIRED_SIGNATURE_FIELDS if not signature.get(field)]
        if missing:
            errors.append(f"{name}: missing signature fields {', '.join(missing)}")
        signatures.append(signature)

    if errors:
        return {"status": "fail", "scene_count": len(scenes), "errors": errors}

    encoded = [tuple(signature[field] for field in REQUIRED_SIGNATURE_FIELDS) for signature in signatures]
    for signature, count in Counter(encoded).items():
        if count > 1:
            duplicates = [names[i] for i, value in enumerate(encoded) if value == signature]
            errors.append(f"duplicate structural signature: {', '.join(duplicates)}")

    template_counts = Counter(signature["template_id"] for signature in signatures)
    for template_id, count in template_counts.items():
        if count > 2:
            errors.append(f"template {template_id!r} is used {count} times; maximum is 2")

    if len(scenes) >= 5:
        archetypes = {signature["archetype"] for signature in signatures}
        if len(archetypes) < 4:
            errors.append(f"batch has {len(archetypes)} archetypes; at least 4 are required")

    if len(scenes) >= 6 and max(pcs_values) - min(pcs_values) < 24:
        errors.append(
            f"PCS spread is only {max(pcs_values) - min(pcs_values)}; "
            "candidate counts appear artificially clustered"
        )

    for index in range(1, len(scenes)):
        difference = axis_difference(signatures[index - 1], signatures[index])
        if difference < 3:
            errors.append(
                f"{names[index - 1]} -> {names[index]} changes only {difference}/5 geometry axes"
            )

    grouped: dict[str, list[int]] = {}
    for index, signature in enumerate(signatures):
        grouped.setdefault(signature["template_id"], []).append(index)
    for template_id, indexes in grouped.items():
        if len(indexes) == 2:
            left, right = indexes
            difference = axis_difference(signatures[left], signatures[right])
            if difference < 3:
                errors.append(
                    f"template {template_id!r} variants {names[left]} and {names[right]} "
                    f"change only {difference}/5 geometry axes"
                )

    return {
        "status": "pass" if not errors else "fail",
        "scene_count": len(scenes),
        "pcs_range": [min(pcs_values), max(pcs_values)],
        "pcs_bands": dict(sorted(Counter(band(pcs) for pcs in pcs_values).items())),
        "archetype_count": len({signature["archetype"] for signature in signatures}),
        "template_counts": dict(sorted(template_counts.items())),
        "errors": errors,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate magnetic-cube batch PCS and structure diversity")
    parser.add_argument("metadata", type=Path)
    args = parser.parse_args()
    report = validate(load_scenes(args.metadata))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report["status"] != "pass":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
