# Approved Universal Color Box

Use this reference when the user asks for a color box or asks to place the
approved universal box into a catalog/SKU sheet.

## Assets

- `assets/approved-color-box-master.png`: locked 3D box photograph used only as
  the perspective, lid, side-face, lighting, and shadow base.
- `assets/approved-universal-color-box.png`: approved white-background result.
- `assets/approved-universal-color-box-cutout.png`: approved transparent asset
  for catalog insertion.
- `assets/approved-catalog-with-color-box.png`: accepted catalog placement and
  scale reference.

Do not redraw the universal box when the request is only to add it to another
catalog sheet. Reuse the approved transparent asset exactly.

## Front-Face Composition

- Build the complete front print as one flat raster first. The blue background,
  connected green pixel frame, title, `3+`, and modeled scene must share this
  one canvas.
- Never repair the box with separate background rectangles or partial green
  patches. Local patches create visible seams after perspective mapping.
- The blue area is one continuous top-to-bottom gradient. Green blocks are one
  connected perimeter layer; every block extending into blue must connect to
  that perimeter or to the title field.
- Use grouped stepped edge blocks, not isolated single-square teeth or a noisy
  checkerboard.
- Keep `3+` fully inside the blue display area. Do not show a PCS badge on this
  approved universal front.
- Draw `MAGNETIC CUBE` as a two-line silver-gray dimensional block logo: dark
  outer stroke, deep lower-right extrusion, light top highlight, and a
  light-to-dark metallic face. Do not upscale the former flat black title.
- Draw the enlarged `3+` badge from clean vector shapes: white outer border,
  orange rounded square, and centered bold white text. Keep visible blue space
  between the badge and the right green frame.
- Insert the exact locked Blender scene render. Do not regenerate the scene with
  an image model and do not alter cube geometry, spacing, or face artwork.
- Size the SKU scene with alpha-mask collision detection, not one fixed
  rectangular thumbnail box. Search for the largest placement that keeps the
  actual visible pixels clear of the title, PCS/size block, age badge, and STEM
  footer. Tall and wide scenes must therefore receive different placements.
- Reject any package where the scene is merely reduced to avoid overlap while
  unused irregular space remains beside the fixed information blocks.
- The five lower-right STEM swatches are SKU-specific. Select five visually
  significant material families from the actual scene, then sample their final
  front-face textures. Never use the generic fallback palette for a production
  SKU, and do not let raw PCS ranking omit a theme-defining color.
- Apply color, contrast, print softness, and right-side lighting to the complete
  front panel, not to individual fragments.

## Perspective Lock

For the `1138 x 771` approved master, map the flat front panel once to these
clockwise corners:

```text
left-top:     129,84
right-top:   1087,69
right-bottom:1087,690
left-bottom: 129,738
```

The upper corners are the printed front-face fold line, not the lid plane. A
panel mapped above these points creates a white hairline and makes the artwork
look pasted over the lid.

Preserve the original lid, left side, outer box shadow, and white studio
background. Warp only once with bicubic resampling and a transparent fill.

## Catalog Placement

- Prefer `approved-universal-color-box-cutout.png` for the lower-right package
  preview.
- Keep its original aspect ratio and reserve approximately `420 x 300 px` in a
  `1600 x 1500 px` catalog sheet.
- Do not let the package overlap the main scene, Chinese name, PCS, 20 mm cube,
  divider, or parts cells.
- The universal package may use its locked universal scene. A SKU-specific
  package must reuse that SKU's exact final Blender render instead.

## Edge QA

Inspect at 200-400% before delivery:

- No front artwork crosses onto the lid or left side.
- No white hairline, double contour, or exposed old artwork along any fold.
- No rectangular seam between blue and green artwork.
- No detached green blocks inside the blue field.
- No halo around the transparent catalog cutout.
- Run `scripts/validate_color_box_cutout.py`. The cutout must exclude the white
  studio floor/shadow, store zero RGB in fully transparent pixels, and be
  resized in premultiplied-alpha mode before catalog composition.
- The downscaled package remains readable without oversharpened pixel edges.
- The lower-right swatches visibly match colors present in the package scene;
  different themes must not show the same fixed swatch row unless their sampled
  materials are genuinely identical.
