# Dual Factory Particle Libraries

Use this reference when a scene may combine particles from `表格1.xlsx` and
`表格2.xlsx`.

## Authoritative Files

- Portable asset root: `assets/dual_factory_library/`
- Table 1 workbook: `assets/dual_factory_library/workbooks/表格1.xlsx`
- Table 2 workbook: `assets/dual_factory_library/workbooks/表格2.xlsx`
- Table 1 manifest: `assets/dual_factory_library/table1_manifest.json`
- Table 2 manifest: `assets/dual_factory_library/table2_manifest.json`
- Blender loader: `scripts/dual_library_materials_blender.py`
- Validator: `scripts/validate_dual_factory_library.py`

The processed workbooks contain only `编号`, `图片`, and `尺寸`. They do not
contain a product-name field.

Workbook body cells and embedded particle thumbnails share the same pale-yellow
background `#FFF5D4`. Thumbnail generation replaces only the studio background
outside the modeled particle silhouette; white/snow/glass artwork inside the
particle must remain white. Reject a workbook if an embedded image has a white
rectangular panel or a white halo around the cube.

## Identity Rules

- Preserve every source ID-to-image relationship exactly as recorded in its
  source workbook.
- Never renumber, deduplicate, or merge repeated artwork.
- Runtime identity is namespaced: `table1:<source-id>` or
  `table2:<source-id>`.
- The buyer-facing detail label is `表1-<source-id>` or `表2-<source-id>`.
- A bare number is not sufficient in a mixed-library scene. For example,
  `table1:026` and `table2:026` are different particles and must display as
  `表1-026` and `表2-026`.
- Scene metadata must store the manifest `key`, `detail_label`, and quantity
  for every used particle.

## Source Preservation

- Table 1 contains cross-net artwork. The top, front, and right source panels
  are registered per image object, rectified to locked square files, and
  installed on one standard unit cube. Do not assume every net uses a 46 px
  panel; derive the panel size and origin from that image's connected cut line.
- Table 2 contains perspective cube drawings. All source drawing objects,
  including overlapping or repeated drawings, remain embedded in the processed
  workbook in source order.
- Table 2 runtime textures are the perspective-rectified top, front, and right
  faces only. Broad studio-light gradients may be reduced, but print lines,
  palette, and source image identity must not be redrawn or invented.
- When a Table 2 record contains multiple source drawings, the topmost visible
  source drawing is the runtime primary. The workbook still preserves every
  drawing object associated with that record.
- Missing-source records remain in the workbook and manifest but must not be
  used in a scene.

## Fine Print Texture Profile

- The locked runtime profile is `fine_print_v3` for both tables.
- Preserve source artwork, face registration, line positions, and every
  ID-to-image relationship. This profile is a restrained print finish, not a
  redraw or content-generation pass.
- Reduce coarse resampling blocks with a `1.0 px` Gaussian deblock source mixed
  at `0.28`; then raise color saturation by a factor of `1.055`.
- Apply the same profile to all top/front/right runtime faces and source cube
  thumbnails. Do not apply another scene-only sharpening, blur, saturation, or
  brightness adjustment after Blender rendering.
- Validation must require `table1_three_visible_faces_v3`,
  `table2_three_visible_faces_v3`, and the exact profile parameters above.

## Scene And Detail Use

1. Validate the library before rendering:

   ```powershell
   python scripts/validate_dual_factory_library.py
   ```

2. Load selected materials by namespaced keys:

   ```python
   from dual_library_materials_blender import install_particle_materials

   installed = install_particle_materials(
       builder,
       ("table1:026", "table2:026", "table1:101"),
   )
   ```

3. Use the returned logical material names for scene cubes and Blender detail
   icons. Both must reuse the same three locked visible-face paths.
4. Pass `detail_label` to the catalog metadata. The approved composer prints it
   at the upper-left of each detail cell and prints `×quantity` below the cube.

### Figure Isolation

- Current audited one-cube figure/head registry used by the factory scene batch:
  `table1:030`, `table1:151`, `table1:162`, `table1:168`, `table2:129`,
  `table2:134`, and `table2:181`.
- These keys are display particles, not structural materials. Each must be a
  detached foreground component with connected-component size exactly `1`.
- Never place a registered figure/head key in a wall, roof, floor, tree canopy,
  bridge, or other main component. The final geometry audit must report
  `embedded_figure_count: 0`.
- Reclassify materials after every legacy numeric-ID remap. If a mapped key is
  now a figure but the legacy model used that number structurally, replace all
  structural occurrences with an existing theme-appropriate material and add
  exactly one detached figure cube. Do not move a structural occurrence and
  leave a hole in the model.
- Require `duplicate_figure_count: 0`; each registered figure key may occur at
  most once per scene unless the user explicitly approves duplicates.
- Before using a new face/character-like SKU, inspect its three source faces and
  add it to the scene's explicit figure registry. Do not infer figure status
  from coordinates or from whether the legacy model happened to detach it.

## Fixed Camera And Tone

- Use an orthographic near-front camera around
  `center + (span*0.22, -span*1.82, span*0.64)`.
- Only top/front/right may appear. If left/back/bottom becomes visible, reject
  the render instead of fabricating another face.
- Use `CUBE_SIZE = 1.0`, integer coordinates, and a bevel no larger than
  `0.001` for line-to-line magnetic-cube scenes.
- Use the locked source-color material: image texture directly into an Emission
  shader at strength `1.0`, Standard color management, exposure `0`. Do not add
  diffuse, specular, coat, tint, or another emission layer. This preserves the
  Excel-derived face color exactly while perspective, seams, and face outlines
  preserve the cube form.
- Use Standard color management with no high-contrast look. Keep broad white
  reflections off the print; intentional white source pixels are allowed.
- Render one-cube detail icons from the same model and three textures. Keep one
  fixed camera crop and lower icon light energy so white particles retain line
  detail instead of clipping.
- Main scenes and detail icons must use the same source-color shader, exposure,
  color management, and camera direction. Disable cast shadows in this factory
  color-lock profile. Do not apply a scene-only gamma, brightness, saturation,
  diffuse-lighting, additive-emission, or white-overlay pass.

## Delivery Gate

- All selected keys are unique and exist in exactly one manifest.
- Every selected record has `scene_eligible: true`.
- Every referenced face file exists and matches its manifest SHA-256.
- Every scene-eligible record contains exactly `top`, `front`, and `right`.
- Scene, detail icon, and package render use the same material key.
- Mixed-library details contain no bare IDs.
- Repeated source artwork remains separate when its source IDs differ.
- Every registered figure/head key has component size `1`; embedded figure count
  is zero.
- Alpha-normalized pixel comparison of every detached figure/head cube against
  its exact detail icon has median RGB and luminance error at most `4/255`.
- Render metadata confirms `scene_color_adjustment: false`, gamma `1.0`, shared
  source-color emission enabled, exposure `0`, and cast shadows disabled.
- For all selected top/front/right faces, compare icon face polygons against the
  authoritative source files. Require median luminance error `<=1/255`, P95
  `<=3.5/255`, maximum `<=7/255`, P95 channel-median error `<=4/255`, and P95
  saturation error `<=0.02`.
