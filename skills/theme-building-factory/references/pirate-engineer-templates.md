# Pirate and Engineer Templates

Use these only after the global particle-first, alignment, PCS, figure, color, and catalog rules pass.

## Shared gate

- Draw and review all six faces of every reusable particle before scene modeling.
- Keep `CUBE_SIZE = 1.0`, integer coordinates, and `PRODUCT_BEVEL = 0.0015`.
- Validate duplicate coordinates, cube-size errors, enclosed cubes, connectivity, production-camera visibility, and exact material-count sum before composition.
- Keep semantic artwork on its intended front face. Side and top faces continue the underlying material or character design and never duplicate the front face.
- Use the same raw scene and tone chain for the scene, detail panel, and package image.

## Pirate treasure cove

- Approved hero: compact stepped wooden ship with a tall mast and one readable 3 x 3 sail.
- Use mostly plain stitched canvas and one centered pirate emblem. Never repeat the emblem on every sail cube.
- Supporting story: shallow water rim, small sand cove, palm tree, treasure chest, gold, map, cannon, porthole, captain, sailor, and one parrot.
- Keep captain and sailor fronts unobstructed. Their side and top faces continue hat, hair, beard, sleeves, stripes, and clothing without another face.
- Approved pilot: `135 PCS`. The current structure uses an asymmetric stepped bow, deep hull, raised stern, mast, stepped sail, treasure cove, and staggered figures. Visual quality takes priority over preserving this count in later variants.
- Visual reference: `assets/approved-pirate-catalog-v2.png`.

## Engineer crane station

- Approved hero: tall tower crane with a long horizontal boom, suspended hook/load, and a part-built station below it.
- Supporting structure: concrete frame, steel beam row, localized brick infill, windows, door, scaffold, safety barriers, blueprint, toolbox, signs, and cones.
- Keep the tower crane connected to the base structure. A two-cube foreground figure may be an intentionally separate magnetic character.
- Use engineer and worker roles with distinct helmet, clothing color, face design, side arms, and back harness treatment.
- Approved pilot: `132 PCS`. The current structure uses a right-side tower crane, left-side part-built frame, localized brick infill, suspended load, and staggered workers so it cannot share the pirate silhouette.
- Visual reference: `assets/approved-engineer-catalog-v2.png`.

## Local implementation

Current tested implementation:

`C:/Users/Administrator/Documents/Codex/2026-07-05/new-chat/work/pirate_engineer_particle_first_v1/`

Run in this order:

1. `draw_particles.py`
2. `audit_scenes_blender.py`
3. `render_assets_blender.py`
4. `compose_outputs.py --stage prebox`
5. shared `render_color_boxes_blender.py`
6. `compose_outputs.py --stage final`

Do not batch-expand these templates until the final 2400 x 1650 catalog images have been visually checked for complete scene framing, readable faces, single seams, matching detail colors, and exact PCS totals.
