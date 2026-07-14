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

- Table 1 contains cross-net artwork. Its six faces are rectified to locked
  square files and installed on one standard unit cube.
- Table 2 contains perspective cube drawings. All source drawing objects,
  including overlapping or repeated drawings, remain embedded in the processed
  workbook in source order.
- When a Table 2 record contains multiple source drawings, the topmost visible
  source drawing is the runtime primary. The workbook still preserves every
  drawing object associated with that record.
- Missing-source records remain in the workbook and manifest but must not be
  used in a scene.

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
   icons. Both must reuse the same six locked face paths.
4. Pass `detail_label` to the catalog metadata. The approved composer prints it
   at the upper-left of each detail cell and prints `×quantity` below the cube.

## Delivery Gate

- All selected keys are unique and exist in exactly one manifest.
- Every selected record has `scene_eligible: true`.
- Every referenced face file exists and matches its manifest SHA-256.
- Scene, detail icon, and package render use the same material key.
- Mixed-library details contain no bare IDs.
- Repeated source artwork remains separate when its source IDs differ.
