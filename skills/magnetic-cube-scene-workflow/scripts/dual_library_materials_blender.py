from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import bpy


SKILL_ROOT = Path(__file__).resolve().parents[1]
LIBRARY_ROOT = Path(
    os.environ.get(
        "MAGNETIC_DUAL_LIBRARY_ROOT",
        str(SKILL_ROOT / "assets" / "dual_factory_library"),
    )
)
MANIFEST_PATHS = {
    "table1": LIBRARY_ROOT / "table1_manifest.json",
    "table2": LIBRARY_ROOT / "table2_manifest.json",
}
FACE_NAMES = ("top", "front", "right")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _safe_name(key: str) -> str:
    return key.replace(":", "_").replace("/", "_").replace("\\", "_")


def load_particle_index(validate_hashes: bool = True) -> dict[str, dict]:
    index: dict[str, dict] = {}
    for library_id, manifest_path in MANIFEST_PATHS.items():
        if not manifest_path.exists():
            raise FileNotFoundError(manifest_path)
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("library_id") != library_id:
            raise RuntimeError(f"Unexpected library ID in {manifest_path}")
        for record in manifest["records"]:
            key = record["key"]
            if key in index:
                raise RuntimeError(f"Duplicate namespaced particle key: {key}")
            if record.get("scene_eligible"):
                for face_name in FACE_NAMES:
                    file_info = record["files"][face_name]
                    path = LIBRARY_ROOT / file_info["path"]
                    if not path.exists():
                        raise FileNotFoundError(path)
                    if validate_hashes and _sha256(path) != file_info["sha256"]:
                        raise RuntimeError(f"Face hash mismatch: {key} {face_name}")
            index[key] = record
    return index


def make_image_material(name: str, image_path: Path) -> bpy.types.Material:
    material = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    nodes.clear()

    output = nodes.new("ShaderNodeOutputMaterial")
    emission = nodes.new("ShaderNodeEmission")
    texture = nodes.new("ShaderNodeTexImage")
    texture.image = bpy.data.images.load(str(image_path), check_existing=True)
    texture.interpolation = "Linear"

    emission.inputs["Strength"].default_value = 1.0
    links.new(texture.outputs["Color"], emission.inputs["Color"])
    links.new(emission.outputs["Emission"], output.inputs["Surface"])
    return material


def install_particle_materials(
    builder,
    particle_keys: tuple[str, ...] | list[str],
    *,
    validate_hashes: bool = True,
) -> dict[str, str]:
    index = load_particle_index(validate_hashes=validate_hashes)
    installed: dict[str, str] = {}
    for particle_key in particle_keys:
        if particle_key not in index:
            raise KeyError(f"Unknown particle key: {particle_key}")
        record = index[particle_key]
        if not record.get("scene_eligible"):
            raise RuntimeError(f"Particle has no usable source artwork: {particle_key}")

        logical = _safe_name(particle_key)
        face_materials = {}
        for face_name in FACE_NAMES:
            path = LIBRARY_ROOT / record["files"][face_name]["path"]
            material_key = f"{logical}_{face_name}"
            builder.MATERIALS[material_key] = make_image_material(material_key, path)
            face_materials[face_name] = material_key

        # The production camera can only see top/front/right. Hidden faces use
        # aliases solely to satisfy the closed cube mesh and are not source art.
        builder.MATERIAL_SPEC[logical] = {
            "top": face_materials["top"],
            "front": face_materials["front"],
            "right": face_materials["right"],
            "back": face_materials["front"],
            "left": face_materials["right"],
            "bottom": face_materials["top"],
        }
        installed[particle_key] = logical
    return installed
