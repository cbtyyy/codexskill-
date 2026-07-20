from __future__ import annotations

import json
from collections import Counter
from functools import lru_cache
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = SKILL_ROOT / "assets" / "mc_factory_catalog_20260720" / "manifest.json"
ORIENTATIONS = {
    "horizontal_x": lambda units: tuple(units),
    "horizontal_y": lambda units: (units[1], units[0], units[2]),
    "upright_z": lambda units: (units[2], units[1], units[0]),
    "unit": lambda units: tuple(units),
}


def _particle_id(material: str) -> str | None:
    for prefix in ("mc:", "mc_"):
        if material.startswith(prefix):
            return material[len(prefix) :]
    return None


@lru_cache(maxsize=1)
def load_particle_dimensions() -> dict[str, dict]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return {record["id"]: record for record in manifest["particles"]}


def particle_extent(
    cube,
    orientation_by_particle: dict[str, str] | None = None,
) -> tuple[int, int, int]:
    identifier = _particle_id(cube.mat)
    if identifier is None:
        return (1, 1, 1)
    record = load_particle_dimensions().get(identifier)
    if record is None:
        raise RuntimeError(f"Unknown MC particle ID: {identifier}")
    orientation_by_particle = orientation_by_particle or {}
    orientation = (
        getattr(cube, "orientation", None)
        or orientation_by_particle.get(cube.mat)
        or orientation_by_particle.get(f"mc:{identifier}")
        or orientation_by_particle.get(f"mc_{identifier}")
        or record["default_orientation"]
    )
    if orientation not in record["allowed_rotations"]:
        raise RuntimeError(
            f"MC {identifier} does not allow orientation {orientation}; "
            f"allowed={record['allowed_rotations']}"
        )
    extent = ORIENTATIONS[orientation](record["geometry_units"])
    if sorted(extent) != sorted(record["geometry_units"]):
        raise RuntimeError(f"MC {identifier}: orientation changed physical proportions")
    return extent


def occupied_cells(cube, orientation_by_particle: dict[str, str] | None = None):
    width, depth, height = particle_extent(cube, orientation_by_particle)
    for dx in range(width):
        for dy in range(depth):
            for dz in range(height):
                yield (cube.x + dx, cube.y + dy, cube.z + dz)


def physical_occupancy_audit(
    model,
    orientation_by_particle: dict[str, str] | None = None,
) -> dict:
    counts = Counter(
        cell
        for cube in model.cubes
        for cell in occupied_cells(cube, orientation_by_particle)
    )
    overlaps = sorted(cell for cell, count in counts.items() if count > 1)
    non_unit = []
    for cube in model.cubes:
        extent = particle_extent(cube, orientation_by_particle)
        if extent != (1, 1, 1):
            non_unit.append(
                {
                    "material": cube.mat,
                    "position": [cube.x, cube.y, cube.z],
                    "extent": list(extent),
                    "pcs": 1,
                }
            )
    return {
        "particle_object_count": len(model.cubes),
        "occupied_grid_cell_count": len(counts),
        "physical_overlap_count": len(overlaps),
        "physical_overlaps": [list(cell) for cell in overlaps],
        "non_unit_particles": non_unit,
        "one_object_one_pcs": True,
    }


def validate_physical_occupancy(
    model,
    orientation_by_particle: dict[str, str] | None = None,
) -> dict:
    audit = physical_occupancy_audit(model, orientation_by_particle)
    if audit["physical_overlap_count"]:
        raise RuntimeError(
            f"{model.name}: dimensional particles overlap at "
            f"{audit['physical_overlaps']}"
        )
    return audit


def install_dimension_aware_geometry(
    builder,
    orientation_by_particle: dict[str, str] | None = None,
) -> None:
    import bpy

    original = builder.add_cube_object

    def add_particle_object(cube) -> None:
        extent = particle_extent(cube, orientation_by_particle)
        if extent == (1, 1, 1):
            original(cube)
            return

        width, depth, height = extent
        pad = (1 - builder.CUBE_SIZE) / 2
        x0, y0, z0 = cube.x + pad, cube.y + pad, cube.z + pad
        x1 = cube.x + width - pad
        y1 = cube.y + depth - pad
        z1 = cube.z + height - pad
        verts = [
            (x0, y0, z0),
            (x1, y0, z0),
            (x1, y1, z0),
            (x0, y1, z0),
            (x0, y0, z1),
            (x1, y0, z1),
            (x1, y1, z1),
            (x0, y1, z1),
        ]
        faces = [
            (0, 3, 2, 1),
            (4, 5, 6, 7),
            (0, 1, 5, 4),
            (1, 2, 6, 5),
            (2, 3, 7, 6),
            (3, 0, 4, 7),
        ]
        face_order = ("bottom", "top", "front", "right", "back", "left")
        material_names = [builder.MATERIAL_SPEC[cube.mat][name] for name in face_order]
        unique_names = list(dict.fromkeys(material_names))

        mesh = bpy.data.meshes.new(
            f"mesh_{cube.mat}_{cube.x}_{cube.y}_{cube.z}"
        )
        mesh.from_pydata(verts, [], faces)
        mesh.update()
        for name in unique_names:
            mesh.materials.append(builder.MATERIALS[name])
        for polygon, name in zip(mesh.polygons, material_names):
            polygon.material_index = unique_names.index(name)

        uv_layer = mesh.uv_layers.new(name="uv")
        uv_face = [(0, 0), (1, 0), (1, 1), (0, 1)]
        for polygon in mesh.polygons:
            for loop_index, uv in zip(polygon.loop_indices, uv_face):
                uv_layer.data[loop_index].uv = uv

        obj = bpy.data.objects.new(
            f"particle_{cube.mat}_{cube.x}_{cube.y}_{cube.z}", mesh
        )
        bpy.context.collection.objects.link(obj)
        bevel = obj.modifiers.new("small_real_product_edge", "BEVEL")
        bevel.width = builder.PRODUCT_BEVEL
        bevel.segments = 2
        obj.modifiers.new("weighted_normals", "WEIGHTED_NORMAL")

    builder.add_cube_object = add_particle_object
