---
name: magnetic-cube-scene-workflow
description: Generate and refine production-ready magnetic cube product scenes, approved-format catalog/SKU images, parts-detail panels, and optional packaging specifications. Use when the user asks for magnetic cube scene pictures, “这种图片”, SKU资料图, multi-theme generation from Excel, same-size aligned cube modeling, PCS-accurate parts lists, competitor-style optimization, or color-box/carton work. Default scene-image requests to the approved blue catalog template with 12-15 particle types unless the user explicitly requests another layout.
---

# Magnetic Cube Scene Workflow

Use this skill to produce wholesale-ready magnetic cube scene assets. The output must feel like a real SKU sheet, not a generic AI image.

## Non-Negotiables

- Model first. Do not rely on image generation for cube geometry.
- Every cube must be identical size, square/cubic, grid-aligned, and line-to-line connected when part of the scene.
- In strict magnetic-cube renders, every modeled coordinate must be an integer
  grid point, cube edge length must equal exactly one grid unit, and adjacent
  faces must share the same plane. Use only a near-zero bevel and a thin
  hue-matched printed perimeter; never use a visible gap or contact-shadow band
  to simulate the seam.
- Cube count must match the displayed PCS exactly. If PCS is not specified,
  finish the scene first, keep the result within 100-200 PCS, then display the
  actual modeled count; never add filler only to reach a preset number.
- The buyer must understand the scene without reading the scene name.
- Use the competitor folder as the quality benchmark: `D:/Users/Administrator/Desktop/磁力方块场景/`.
- Keep the scene, parts-detail icons, and color-box scene visually consistent.
- Keep side-face ink close to the approved front-face color. Create depth with
  balanced diffuse lighting and a thin edge shadow, never a gray side overlay
  or a broad white specular film.
- Place buyer-facing characters where their complete front artwork is visible
  from the production camera. Side/top character artwork must remain distinct,
  but it must not replace or hide the primary face in the catalog view.
- Avoid long flat strips, large empty planes, random material blocks, misaligned characters, and repeated generic figures.
- Apply a premium-toy design gate: repeated decoration cannot be used as PCS filler. Every visible print block must have a role such as wall, window, door, fireplace, foliage, tree ornament, gift, lamp, or character.
- Keep white/snow blocks white, but preserve seams with thin gray edges.
- Do not add tight internal contact shadows between connected cubes. Use natural face shading, one thin neutral-gray seam, and only a short pale grounding shadow below the complete scene.
- Do not build a large visible plane from blank-white top faces. Keep pure white for figures and isolated snow pieces; distribute theme-appropriate pale-blue drift, crystal, or functional direction prints across contiguous snow roofs and ground.
- Do not assign a generic white top to every themed cube. Top materials must follow semantics: foliage stays foliage, wood stays wood, brick stays brick; only actual snow ground, snow caps, and snowy roof pieces use white tops.
- For holiday/Christmas scenes, prioritize a recognizable small-world scene over material variety: strong tree or house silhouette first, decorations second.

## Approved Catalog Default

For scene pictures, SKU images, catalog sheets, “这种图片”, or requests to generate another theme in the same style:

1. Read [references/approved-catalog-template.md](references/approved-catalog-template.md).
2. Use [assets/approved-catalog-template.png](assets/approved-catalog-template.png) as the visual acceptance target.
3. Compose with `scripts/compose_approved_catalog_sheet.py`; do not restart background/layout exploration unless the user explicitly asks.
4. Treat packaging as a separate optional workflow. Do not produce color boxes when the request is only for scene/SKU images.
5. Reject delivery if the sheet has fewer than 12 or more than 15 SKU types, a figure is larger than a scene cube, any `×quantity` label is not centered below its cube, or the detail panel exceeds the approved bottom area.

## Workflow

1. Clarify the task type:
   - For scene generation or optimization, read `references/scene-design-rules.md`.
   - For local rendering commands and script locations, read `references/local-workflow.md`.
   - For color box, carton, weight, and quantity calculations, read `references/packaging-formulas.md`.
2. Choose themes from the Excel table or user-specified topic. Prefer themes with clear buildable core elements.
3. For a new theme family, use the particle-first gate before scene modeling:
   - List every required structural, semantic, prop, and character particle.
   - Draw and lock separate `left`, `front`, `right`, `back`, `top`, and
     `bottom` artwork for each particle. New theme families must not reuse one
     generic side texture for all lateral faces.
   - Render every particle as one identical 3D cube and review the unit-cube contact sheet.
   - Save the approved set as a versioned particle manifest. Scene code may reference only manifest materials.
   - If modeling reveals a missing particle, return to the particle library, add and re-audit it; never draw an improvised texture inside the scene stage.
   - Mix natural, clean graphic, and illustrated particles according to the theme. Do not force the entire set into pixel art.
4. Before changing a reusable material family, isolate competitor detail cubes
   for that material. Compare neutral white, hue, print scale, line width,
   texture density, face continuity, and highlight behavior. Never judge only
   from the full scene.
5. Screen theme buildability before rendering:
   - Keep strong themes with a clear object vocabulary and a ready template.
   - Mark borderline themes as `keep_with_template_review`; optimize their template before batch generation.
   - Skip themes that have no readable silhouette, no dedicated print vocabulary, or tend to become flat walls/long strips.
   - Use `MAGNETIC_SCREEN_THEMES=1` for scripted screening reports.
6. Select core elements by PCS and visual clarity:
   - Under 120 PCS: 1 core element.
   - 120-169 PCS: 2 core elements.
   - 170+ PCS: 2-3 core elements.
   - Aesthetic clarity beats using every listed element.
7. If PCS is unspecified, use aesthetic-count mode (`MAGNETIC_AESTHETIC_PCS=1`)
   with a soft planning cap. Complete the silhouette, support element and props,
   skip generic target filling, then use the actual 100-200 PCS result.
8. Build a model-based scene around one primary silhouette. Add support elements only when they improve recognizability.
9. For each theme, apply the archetype template before filling PCS. Fillers must stay subordinate to the main silhouette.
10. Render and compose catalog sheets. Parts details and color-box scenes must reuse the exact locked particle textures and final scene render.
11. Run `work/audit_scene_geometry_blender.py` before catalog composition. Reject any duplicate, enclosed, hidden, low-visibility, wrong-size, or unexpected non-figure component.
12. Compare against competitor references before stopping. If it looks like colored material blocks instead of a recognizable scene, revise the model/texture plan.
13. When color direction is not approved, render the same geometry in controlled saturation variants. Do not change the model, materials, PCS, or layout between variants, and validate scene/detail/package tone separately for each variant.

## Visual Target

Aim for the competitor median brightness range, not raw overexposure:

- Colored scene pixel median brightness target: about 140-146.
- Keep saturation vivid but not neon.
- Use printed-plastic gloss: local catchlights and clean highlights, not a washed-out white overlay.
- Never bake a broad white gloss film into top or side textures. Keep the oil-bright catchlight on the buyer-facing print, while top/side faces use low-specular directional shading and a crisp printed perimeter.
- Prefer clear theme prints: windows, doors, snowflakes, gifts, leaves, brick, flags, tires, character faces.
- Use print hierarchy: one dominant material family, two or three semantic print families, and only sparse accent blocks. Avoid evenly alternating colors or repeating the same ribbon/wreath print across unrelated surfaces.
- A good scene should still be understandable if the Chinese scene name and PCS badge are hidden.

## Output Rules

- Put generated files on the desktop under `D:/Users/Administrator/Desktop/生成的场景图/` unless the user specifies otherwise.
- For batches, separate scene-only images and catalog sheets into subfolders.
- Use Chinese scene names on catalog sheets; use English-style clean packaging copy on color boxes.
- Catalog sheet size defaults to `2400x1650` unless the user chooses another resolution.
- Include PCS badge, Chinese scene name, 20mm cube icon on catalog sheets.
- Use `0.79 IN` on color boxes for foreign-facing size labeling.

## Validation Checklist

Before final response, check:

- Exact PCS count.
- Sum of all parts-detail quantities equals PCS.
- Same cube size, no big/small cube.
- No cube misalignment.
- Grid audit reports zero fractional coordinates, one identical cube edge
  length, and exact one-unit center spacing for every adjacent pair.
- Exactly one connected main component; only complete one- or two-cube figures may be separate.
- Geometry audit reports zero enclosed cubes, zero camera-hidden cubes, zero low-visibility cubes, and zero cube-size errors. Use at least 12 visible face samples per cube for the production camera.
- White blocks do not merge into the background or each other.
- Top and side faces have no milky veil: side ink remains saturated, white tops remain neutral white, and their thin gray perimeter survives final downscaling.
- Six-face unit renders retain the locked print color: top/right colored ink
  must not be clipped or covered by a gray/white lighting layer.
- Reject a technically valid scene if it still reads as a repeated block pile. The hero silhouette, interior/foreground story, texture rhythm, and figure placement must pass a buyer-view aesthetic review before batch generation.
- Parts-detail icons do not overlap counts.
- All one-cube detail icons use one fixed orthographic crop and one canonical alpha silhouette; never crop each material independently.
- Parts-detail colors match scene colors.
- Main-scene colored faces, parts-detail icons, and the color-box scene use one
  locked tone profile; reject visible side-face desaturation or gray drift.
- Every featured character shows its complete front face without scene overlap.
- Main-scene white/snow matches the detail icon's neutral white; do not accept
  cool gray or blue-cyan snow. Preserve only one thin neutral-gray seam.
- Color-box scene matches catalog scene brightness.
- Color box dimensions and carton table follow the formula reference.
- At least one strong silhouette communicates the theme.

Report any remaining weak theme honestly instead of saying it is fine.
