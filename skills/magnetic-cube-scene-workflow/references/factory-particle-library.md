# Factory Particle Library V2

This is the approved runtime texture source for factory magnetic-cube scenes.

## Authoritative Files

- Face textures: `assets/locked_factory_faces_v2/`
- Portable Excel SKU metadata, file paths, and SHA-256 hashes:
  `references/locked-factory-faces-v2.json`
- Factory-to-redraw review sheet: `assets/locked-factory-face-contact-sheet-v2.png`
- Rebuild entry point: `scripts/build_locked_factory_faces.py`
- Blender material loader: `scripts/locked_sku_materials_blender.py`
- Integrity check: `scripts/validate_locked_factory_faces.py`

The approved V2 set contains `64` Excel-confirmed SKU IDs and `192` RGB face
textures. Each SKU has one `512 x 512` `top`, `side`, and `front` file. The
manifest preserves the Excel name/size where those cells are populated; IDs
`166`, `176`, `180`, `181`, `182`, `184`, and `185` are explicitly marked
`id_only` because the supplied workbook leaves their name/size cells blank.

## Source And Mapping Policy

- Use Excel cells as the formal SKU number and name source.
- Use the factory SKU overview as the visual pattern and color reference.
- Never map Excel embedded images by drawing order. The workbook contains
  duplicate drawings, attachments, and missing anchors, so drawing order is not
  a reliable SKU key.
- Factory overview crops may appear only in the review contact sheet. They must
  never be loaded as Blender materials.
- Runtime faces are procedurally redrawn square artwork. Natural materials use
  a conservative multiscale print finish: 70% crisp base geometry, 30% softened
  transition, plus a finer 64-cell grain. Exact character and prop geometry does
  not receive the natural finish. The faces are not
  perspective crops, thumbnail cutouts, competitor pixels, or AI-generated
  texture guesses.
- The raw Excel workbook and raw factory overview are private source materials.
  They are intentionally not bundled in the public Skill repository.

## Runtime Rules

- If a requested SKU exists in V2, use its locked files without redrawing or
  color substitution.
- Scene cubes, parts-detail cubes, and color-box scenes must load the same file
  paths from the manifest.
- Figure SKUs `101`, `102`, `109`, `129`, `134`, and `182` are single unit cubes.
  They must use the same geometry and scale as every structural cube.
- Put the complete buyer-facing figure artwork toward the production camera.
- Do not use old `sku_faces`, `traced_faces`, `redrawn_faces`, or direct Excel
  image extraction after the V2 library is available. V1 is retained only as a
  rollback reference and is not the default runtime source.

## Rebuild

Set the two private source paths, then rebuild and validate:

```powershell
$env:MAGNETIC_FACTORY_XLSX='D:\path\to\磁力颗粒编号.xlsx'
$env:MAGNETIC_FACTORY_SKU_SHEET='D:\path\to\磁力颗粒SKU大图.png'
python scripts/build_locked_factory_faces.py
python scripts/validate_locked_factory_faces.py
```

The rebuild deletes stale face PNGs, redraws the full locked set, writes
relative paths and hashes to the manifest, and creates the review contact sheet.

## Adding A SKU

1. Confirm the formal ID from the Excel cell, not an embedded-image index.
2. Inspect its factory pattern and colors on the SKU overview.
3. Add explicit top, side, and front drawing rules.
4. Rebuild the library and review the contact sheet at full size.
5. Render the unit cube from the production camera and verify orientation.
6. Run the integrity validator and commit the new PNGs with the updated manifest.

Do not commit a new SKU if any face is skewed, stretched, cropped from a 3D
thumbnail, contaminated by a shadow/background, or inconsistent with its detail
icon.
