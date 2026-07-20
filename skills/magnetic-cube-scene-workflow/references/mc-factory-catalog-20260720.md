# MC Factory Catalog 20260720

Use this catalog when the user says latest MC factory catalog, `MC零件对照表`,
or asks to rebuild an existing scene with the latest factory IDs.

## Authority

- `assets/mc_factory_catalog_20260720/factory_catalog.xlsx` is the ID authority.
- The catalog contains 196 unique visible particle IDs.
- `particle_svg/<id>.svg` contains one scalable catalog cube per visible ID.
- 192 scene-eligible IDs have `top`, `front`, and `right` assets under
  `face_svg/<id>/` and matching Blender runtime files under `face_png/<id>/`.
- The production camera must reveal only top, front, and right. Hidden faces may
  alias these assets only to close the mesh.

## Physical Dimensions

- The workbook size field is authoritative and must be read before geometry is
  created.
- `2x2x2 cm` means one `1x1x1` grid cube and one PCS.
- `4x2x2 cm` means one horizontal `2x1x1` rectangular prism and one PCS. It is
  a single molded particle, not two cubes; it must have no center seam.
- IDs `073`, `095`, `096`, `097`, and `098` are the current `4x2x2 cm`
  particles. Their canonical physical geometry is horizontal. A semantic use
  such as a door may rotate the same prism to `1x1x2`, but may not rescale it.
- Use `scripts/mc_particle_geometry_blender.py` to resolve dimensions, apply
  an allowed orientation, build one mesh per particle, and audit occupied grid
  cells before rendering.

## Identity Rules

- Use keys in the form `mc:<id>` in new scene code.
- Never assign artwork by file order, drawing order, similarity, or old catalog
  numbering. Resolve the Excel cell ID first.
- When migrating the old FK-15 scene, the old detail entry `166` used the
  artwork now owned by MC ID `167`. Preserve the artwork and relabel it `167`.
- Do not merge two IDs merely because their patterns look similar.

## Rendering

1. Run `scripts/validate_mc_factory_catalog_20260720.py`.
2. Install materials with `scripts/mc_factory_catalog_materials_blender.py`.
3. Feed each texture directly into a strength-1 emission shader, Standard view
   transform, exposure 0, gamma 1, and no scene-level color adjustment.
4. Keep `2x2x2 cm` particles exactly one grid unit. Keep `4x2x2 cm` particles
   exactly two grid units along their oriented long axis. Use near-zero bevel,
   no gap, no internal seam, and one object per PCS.
5. Render detail icons with the same camera, shader, and face files as the scene.

## Parts Panels

- Group identical MC IDs into one detail cell.
- Put the MC ID above the cube and `×quantity` below it.
- Sum all quantities and require exact equality with the displayed PCS.
- Character and creature-head particles remain isolated one-cube foreground
  components and may not be embedded in structures.
