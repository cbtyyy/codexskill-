# Exact Factory Catalog V3

Use `assets/exact_factory_catalog_v3/` as the authoritative catalog identity
and detail-panel reference for the current factory set.

## Contents

- `manifest.json`: ordered ID-to-image mapping, dimensions, and SHA-256 hashes.
- `icons/`: 196 locked catalog icons. Most are exact source-cell crops; the 10
  approved structured-redraw IDs use source-faithful vector-derived icons.
- `workbooks/factory-particle-catalog-v3.xlsx`: factory catalog workbook.
- `overview.png`: full catalog overview.

The order is `001` through `185`, followed by `207`, `273`, `283`, `289`,
`484`, `485`, `486`, `A01`, `A02`, `A03`, and `270`. IDs `A01` through
`A03` are flat accessories; every other entry is a 2 x 2 x 2 cm cube.

## Required Rules

- Preserve every ID-to-image relationship exactly, including repeated-looking
  artwork. Never deduplicate or renumber by appearance.
- Use the V3 icon directly for catalog and parts-detail cells. Do not redraw,
  recolor, reproject, sharpen, blur, or increase saturation after loading it.
- IDs `002`, `006`, `020`, `026`, `036`, `076`, `097`, `107`, `116`, and
  `155` are the approved structured-redraw exception. Their locked source is
  `assets/structured_factory_redraw_v1/`; the catalog icon and workbook image
  are derived from that source. Preserve the original ID relationship and do
  not fall back to the earlier enlarged raster thumbnail.
- These icons are perspective catalog thumbnails, not flat face textures. Do
  not load them as Blender cube materials.
- For modeled scenes, resolve the matching particle identity here, then use the
  verified source-backed top/front/right face assets from the applicable
  runtime library. If no verified face set exists, stop and request source face
  artwork instead of inventing it from the thumbnail.
- Validate the package with
  `scripts/validate_exact_factory_catalog_v3.py` before delivery or release.
