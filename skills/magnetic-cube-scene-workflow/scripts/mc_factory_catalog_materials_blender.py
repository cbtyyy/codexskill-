from __future__ import annotations

from pathlib import Path

import bpy


SKILL_ROOT = Path(__file__).resolve().parents[1]
LIBRARY_ROOT = SKILL_ROOT / "assets" / "mc_factory_catalog_20260720"
FACE_NAMES = ("top", "front", "right")


def safe_name(key: str) -> str:
    return key.replace(":", "_").replace("/", "_").replace("\\", "_")


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


def install_particle_materials(builder, particle_keys: list[str] | tuple[str, ...]) -> dict[str, str]:
    installed = {}
    for key in particle_keys:
        namespace, identifier = key.split(":", 1)
        if namespace != "mc":
            raise RuntimeError(f"Expected mc:<id>, got {key}")
        logical = safe_name(key)
        materials = {}
        for face in FACE_NAMES:
            path = LIBRARY_ROOT / "face_png" / identifier / f"{face}.png"
            if not path.exists():
                raise FileNotFoundError(path)
            material_key = f"{logical}_{face}"
            builder.MATERIALS[material_key] = make_image_material(material_key, path)
            materials[face] = material_key
        builder.MATERIAL_SPEC[logical] = {
            "top": materials["top"],
            "front": materials["front"],
            "right": materials["right"],
            "back": materials["front"],
            "left": materials["right"],
            "bottom": materials["top"],
        }
        installed[key] = logical
    return installed
