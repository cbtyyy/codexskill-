# Approved Magnetic Cube Catalog Template

Use this as the default for future magnetic-cube scene/SKU image requests.

## Canvas And Zones

- Canvas: `1600 x 1500 px`, RGB PNG.
- Sky/scene zone: `y=0..1029`.
- Grass/dirt divider: `y=1030..1139`.
- Parts-detail zone: `y=1140..1499` (360 px, about 24% of canvas).
- Keep all scene geometry and separate figure cubes above the divider.

## Header

- Top-left: `MAGNETIC CUBE`, dark charcoal, large bold text.
- Top-right line 1: Chinese scene name, right-aligned.
- Top-right line 2: actual modeled `N PCS`, orange, larger than the scene name.
- Do not add a lower-left PCS badge.

## Scene

- Use the final Blender render with transparent background.
- Center one recognizable scene; maximize it within the scene zone without clipping.
- Every cube, including figure heads, is one identical `20 mm` unit cube rendered in the same Blender scene and orthographic camera. Never paste figures at a fixed pixel size.
- Keep integer grid coordinates, one-unit edge length, zero duplicates, and line-to-line connections.
- Show exactly one connected main scene. Only complete one-/two-cube figures may be detached.
- Use the approved near-frontal three-quarter camera; no extreme side angle.
- Preserve factory color/pattern. For approved factory SKUs, load the exact file
  from `assets/locked_factory_faces_v1/` and its manifest. Never paste the whole
  Excel/factory thumbnail, its perspective cube, gray shadow, or background.
- When the user asks to show the approved universal color box, reserve the lower-right package area and pass `assets/approved-universal-color-box-cutout.png` to `scripts/compose_approved_catalog_sheet.py --color-box`. Do not redraw or re-cut the package.

## Particle Variety

- Use `12-15` distinct Excel SKU types per sheet; target `12-14`.
- Figures count as SKU types.
- Add a material only when it has a scene role (ground, water, wall, roof, trunk, foliage, window, light, chest, furnace, gift, character, etc.). Never add random filler to meet the minimum.
- Keep total PCS aesthetic-first and publish the actual modeled count.

## Divider

- Grass band: `y=1030..1074`, varied green pixels.
- Dirt band: `y=1075..1139`, varied brown pixels.
- This is a page divider only. It must not overlap scene cubes or detail cells.

## Parts Detail

- Background: pale warm yellow.
- Heading: `颗粒明细`. Do not append `EXCEL编号 × 数量`.
- Grid: `6 columns x 2 rows` for 12 types. For 13-15 types, use `8+5`, `7+7`, or `8+7` while preserving readable icon size; never exceed two rows.
- Each detail icon is the same canonical clean 3D cube silhouette, not independently cropped.
- Excel number sits at the cell's upper-left.
- `×quantity` sits centered directly below the cube, never at the cell's left edge.
- Sum of all detail quantities must equal displayed PCS exactly.

## Color And Pattern QA

- Use one tone profile for scene and detail icons.
- Scene cubes and detail icons must resolve to the same locked face paths and
  pass `scripts/validate_locked_factory_faces.py` before composition.
- Keep color vivid but not neon; no gray side overlay or milky highlight veil.
- Check faces with strong geometry: character eyes/mouth, chest bands, gift ribbons, bookshelves, furnaces, doors, glass grids, and wood planks.
- Horizontal artwork must remain horizontal after face rectification.
- Remove all source thumbnail haze, projection shadows, and bottom-right alpha residue.

## Required Validation

- Output is `1600 x 1500`.
- Distinct SKU types are within `12-15`.
- Detail sum equals PCS.
- Figures use the same Blender unit size as all scene cubes.
- No duplicate/fractional coordinates.
- No scene/detail overlap.
- Optional color-box preview stays above the divider and does not overlap the main scene, scene name, PCS, or size icon.
- All quantity labels are centered beneath their cube.
