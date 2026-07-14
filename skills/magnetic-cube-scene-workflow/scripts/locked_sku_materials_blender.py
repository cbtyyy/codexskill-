from __future__ import annotations

import os
from pathlib import Path

import bpy


SKILL_ROOT = Path(__file__).resolve().parents[1]
FACE_DIR = Path(os.environ.get(
    "MAGNETIC_LOCKED_FACE_DIR",
    str(SKILL_ROOT / "assets/locked_factory_faces_v1"),
))
FIGURE_HEAD_SKUS = {101, 102, 109, 129, 134, 182}


def make_image_material(name: str, image_path: Path) -> bpy.types.Material:
    material = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    nodes.clear()

    output = nodes.new("ShaderNodeOutputMaterial")
    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    emission = nodes.new("ShaderNodeEmission")
    mix = nodes.new("ShaderNodeMixShader")
    texture = nodes.new("ShaderNodeTexImage")
    texture.image = bpy.data.images.load(str(image_path), check_existing=True)
    texture.interpolation = "Linear"

    bsdf.inputs["Roughness"].default_value = 0.40
    if "Specular IOR Level" in bsdf.inputs:
        bsdf.inputs["Specular IOR Level"].default_value = 0.13
    if "Coat Weight" in bsdf.inputs:
        bsdf.inputs["Coat Weight"].default_value = 0.018
    emission.inputs["Strength"].default_value = 0.33
    # Mostly physically lit plastic with a restrained color-preserving fill.
    # This keeps the scene three-dimensional without gray side-face drift.
    mix.inputs[0].default_value = 0.16

    links.new(texture.outputs["Color"], bsdf.inputs["Base Color"])
    links.new(texture.outputs["Color"], emission.inputs["Color"])
    links.new(bsdf.outputs["BSDF"], mix.inputs[1])
    links.new(emission.outputs["Emission"], mix.inputs[2])
    links.new(mix.outputs["Shader"], output.inputs["Surface"])
    return material


def install_sku_materials(builder, sku_ids: tuple[int, ...]) -> None:
    missing = []
    for sku in sku_ids:
        logical = f"sku_{sku:03d}"
        keys = {}
        for face_name in ("top", "side", "front"):
            path = FACE_DIR / f"sku_{sku:03d}_{face_name}.png"
            if not path.exists():
                missing.append(str(path))
                continue
            key = f"{logical}_{face_name}"
            builder.MATERIALS[key] = make_image_material(key, path)
            keys[face_name] = key
        if len(keys) == 3:
            # The production camera looks from -Y with a slight +X turn.
            # Put the complete buyer-facing print on -Y and the profile on +X.
            builder.MATERIAL_SPEC[logical] = (keys["top"], keys["front"], keys["side"])
            if sku in FIGURE_HEAD_SKUS:
                builder.FIGURE_MATERIALS.add(logical)
    if missing:
        raise FileNotFoundError("Missing locked factory faces:\n" + "\n".join(missing))
