from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = SKILL_ROOT / "references" / "dual-factory-role-registry.json"
LIBRARY_ROOT = SKILL_ROOT / "assets" / "dual_factory_library"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_registry() -> tuple[dict[str, dict], set[str], dict]:
    registry = load_json(REGISTRY_PATH)
    complete = {record["key"]: record for record in registry["complete_roles"]}
    components = {record["key"]: record for record in registry["role_components"]}
    if len(complete) != len(registry["complete_roles"]):
        raise RuntimeError("Duplicate complete-role key")
    if len(components) != len(registry["role_components"]):
        raise RuntimeError("Duplicate role-component key")
    overlap = sorted(set(complete) & set(components))
    if overlap:
        raise RuntimeError(f"Role/component overlap: {overlap}")

    manifest_records = {}
    for library_id in ("table1", "table2"):
        manifest = load_json(LIBRARY_ROOT / f"{library_id}_manifest.json")
        manifest_records.update({record["key"]: record for record in manifest["records"]})
    missing = sorted((set(complete) | set(components)) - set(manifest_records))
    if missing:
        raise RuntimeError(f"Registry keys missing from manifests: {missing}")
    ineligible = sorted(
        key
        for key in set(complete) | set(components)
        if not manifest_records[key].get("scene_eligible")
    )
    if ineligible:
        raise RuntimeError(f"Registry keys are not scene eligible: {ineligible}")
    return complete, set(components), registry


def validate_metadata(
    paths: list[Path], complete: dict[str, dict], components: set[str], allow_repeats: bool
) -> dict:
    role_usage = Counter()
    category_usage = Counter()
    scenes = []
    for path in paths:
        for scene in load_json(path):
            parts = {part["key"]: part for part in scene["parts"]}
            invalid_components = sorted(set(parts) & components)
            if invalid_components:
                raise RuntimeError(
                    f"{scene['name_cn']}: body-only role components used {invalid_components}"
                )
            roles = sorted(set(parts) & set(complete))
            if not 1 <= len(roles) <= 3:
                raise RuntimeError(f"{scene['name_cn']}: invalid role count {len(roles)}")
            for key in roles:
                if parts[key]["quantity"] != 1:
                    raise RuntimeError(
                        f"{scene['name_cn']}: role {key} quantity is {parts[key]['quantity']}"
                    )
            audit_roles = sorted(scene["geometry_audit"]["figure_keys"])
            if roles != audit_roles:
                raise RuntimeError(
                    f"{scene['name_cn']}: parts/audit role mismatch {roles} != {audit_roles}"
                )
            if scene["geometry_audit"]["embedded_figure_count"] != 0:
                raise RuntimeError(f"{scene['name_cn']}: embedded role particle")
            if any(size != 1 for size in scene["geometry_audit"]["figure_component_sizes"]):
                raise RuntimeError(f"{scene['name_cn']}: non-unit role component")
            for key in roles:
                role_usage[key] += 1
                category_usage[complete[key]["category"]] += 1
            scenes.append(
                {
                    "name_cn": scene["name_cn"],
                    "roles": [
                        {"key": key, **complete[key]}
                        for key in roles
                    ],
                }
            )
    repeated = {key: count for key, count in role_usage.items() if count > 1}
    if repeated and not allow_repeats:
        raise RuntimeError(f"Repeated role keys across batch: {repeated}")
    if len(scenes) >= 5:
        missing_categories = {"person", "animal", "monster"} - set(category_usage)
        if missing_categories:
            raise RuntimeError(
                f"Multi-scene batch lacks role categories: {sorted(missing_categories)}"
            )
    return {
        "scene_count": len(scenes),
        "unique_role_count": len(role_usage),
        "repeated_roles": repeated,
        "category_usage": dict(sorted(category_usage.items())),
        "scenes": scenes,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("metadata", nargs="*", type=Path)
    parser.add_argument("--allow-repeated-roles", action="store_true")
    args = parser.parse_args()
    complete, components, registry = validate_registry()
    report = {
        "registry_version": registry["version"],
        "complete_role_count": len(complete),
        "role_component_count": len(components),
        "registry_valid": True,
    }
    if args.metadata:
        report["batch"] = validate_metadata(
            args.metadata, complete, components, args.allow_repeated_roles
        )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
