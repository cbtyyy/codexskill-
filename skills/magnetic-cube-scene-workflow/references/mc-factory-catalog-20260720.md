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
4. Keep every cube exactly one grid unit with near-zero bevel and no gap.
5. Render detail icons with the same camera, shader, and face files as the scene.

## Parts Panels

- Group identical MC IDs into one detail cell.
- Put the MC ID above the cube and `×quantity` below it.
- Sum all quantities and require exact equality with the displayed PCS.
- Character and creature-head particles remain isolated one-cube foreground
  components and may not be embedded in structures.
