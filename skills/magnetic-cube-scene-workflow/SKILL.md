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
  finish the scene first, keep the result within 80-200 PCS, then display the
  actual modeled count; never add filler only to reach a preset number.
- For an unspecified-PCS batch of six or more scenes, cover all three count
  bands: `80-119`, `120-159`, and `160-200`. High-PCS scenes must earn their
  count through a more complete hero and meaningful support structures, not a
  longer base, thicker hidden walls, or repeated decoration.
- The buyer must understand the scene without reading the scene name.
- Use the competitor folder as the quality benchmark: `D:/Users/Administrator/Desktop/磁力方块场景/`.
- For factory SKU work, read `references/factory-particle-library.md` and use
  `assets/locked_factory_faces_v2/` as the authoritative runtime texture source.
  Use Excel cells for formal IDs and the factory overview for pattern/color
  review. Never map workbook images by drawing order or load a perspective
  thumbnail crop as a cube material.
- For the current two-table factory catalog, read
  `references/dual-factory-particle-libraries.md` and use
  `assets/dual_factory_library/` as the authoritative source. Keep every key
  namespaced as `table1:<source-id>` or `table2:<source-id>`; never merge two
  particles because their numbers or artwork look the same.
- The current two-table catalog is a fixed-camera three-visible-face library.
  Store only `top`, `front`, and `right` source-backed textures. The
  production camera must not reveal left/back/bottom. Runtime aliases may close
  the mesh, but they are not factory artwork and must never be exported as such.
- Mixed-library scenes are allowed. Every parts-detail cell must show the
  source-aware label from the manifest, such as `表1-026` or `表2-026`, with
  `×quantity` centered below the cube. A bare `026` is invalid in a mixed scene.
- Keep the scene, parts-detail icons, and color-box scene visually consistent.
- Keep side-face ink close to the approved front-face color. Create depth with
  balanced diffuse lighting and a thin edge shadow, never a gray side overlay
  or a broad white specular film.
- Current two-table factory exception: source-table color accuracy takes
  priority over diffuse shading. Use the locked source-color shader that routes
  the texture through emission at strength `1.0`, exposure `0`, with no added
  diffuse/specular layer. This is a color-preserving print shader, not a glow
  effect. Perspective, three visible faces, seams, and the printed perimeter
  provide depth without darkening the factory artwork.
- Place buyer-facing characters where their complete front artwork is visible
  from the production camera. Side/top character artwork must remain distinct,
  but it must not replace or hide the primary face in the catalog view.
- For any character-led scene, read `references/character-story-and-template-rules.md`.
  Lock each role's expression, costume, six-face continuation, story function,
  and camera-facing placement before modeling. A repeated dot-eye/curve-mouth
  face or a duplicated front texture on the side is a rejection condition.
- A new theme must use a theme-specific model template. Reusing the same wall,
  stair, platform, or tower skeleton with different colors is prohibited. Only
  low-level cube helpers and generic support components may be shared across
  themes; the hero silhouette, circulation path, props, and elevation rhythm
  must be designed for that theme.
- Before a multi-scene batch, assign each model a structural signature and run
  `scripts/validate_scene_batch_diversity.py`. A batch of five or more scenes
  must use at least four archetypes; one template ID may appear at most twice.
  Consecutive scenes and two variants of one template must differ on at least
  three of footprint, primary mass, major void, height rhythm, and foreground
  path.
- In the current two-table factory catalog, every source particle classified as
  a person, head, face character, or creature head is an isolated one-cube
  foreground component. Never use one as a wall, roof, floor, tree, bridge, or
  other structural cube. Reject the scene when a figure particle is face-
  adjacent to the main component or when its connected-component size is not 1.
  Keep each registered figure key to one cube per scene unless the user
  explicitly approves duplicates.
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
2. Read [references/dual-factory-particle-libraries.md](references/dual-factory-particle-libraries.md) for two-table work, or [references/factory-particle-library.md](references/factory-particle-library.md) for the legacy locked set, and validate the selected manifest before rendering.
3. Use [assets/approved-catalog-template.png](assets/approved-catalog-template.png) as the visual acceptance target.
4. Compose with `scripts/compose_approved_catalog_sheet.py`; do not restart background/layout exploration unless the user explicitly asks.
5. Treat packaging as a separate optional workflow. Do not produce color boxes when the request is only for scene/SKU images.
6. Reject delivery if the sheet has fewer than 12 or more than 15 SKU types, a figure is larger than a scene cube, any `×quantity` label is not centered below its cube, or the detail panel exceeds the approved bottom area.

## Approved Color Box

For color-box creation or catalog insertion:

1. Read [references/approved-color-box.md](references/approved-color-box.md).
2. Reuse [assets/approved-universal-color-box-cutout.png](assets/approved-universal-color-box-cutout.png) when the approved universal box only needs to be placed into a catalog.
3. Use [assets/approved-universal-color-box.png](assets/approved-universal-color-box.png) and [assets/approved-catalog-with-color-box.png](assets/approved-catalog-with-color-box.png) as visual acceptance targets.
4. For a changed front scene, compose the whole flat front print first and run `scripts/compose_approved_color_box.py`; never patch the 3D box face with separate background or border fragments.
5. Reject delivery if front artwork crosses a fold line, a white hairline or double edge appears, the blue/green boundary reads as pasted layers, or the catalog thumbnail has a white halo.

## Workflow

1. Clarify the task type:
   - For scene generation or optimization, read `references/scene-design-rules.md`.
   - For scenes containing people, animals, vehicles, occupations, or a buyer-
     visible story, also read `references/character-story-and-template-rules.md`.
   - For pirate or engineering themes, also read `references/pirate-engineer-templates.md` and start from the approved particle-first structural templates instead of recoloring another scene.
   - For local rendering commands and script locations, read `references/local-workflow.md`.
   - For color box composition, read `references/approved-color-box.md`.
   - For carton, weight, quantity, and package-size calculations, read `references/packaging-formulas.md`.
2. Choose themes from the Excel table or user-specified topic. Prefer themes with clear buildable core elements.
   - In two-table work, select particles by the manifest `key`, not by a bare
     numeric ID. The same source number may legally exist in both tables.
   - Use `scripts/dual_library_materials_blender.py` to install the selected
     namespaced six-face materials into the scene builder.
3. For a new theme family, use the particle-first gate before scene modeling:
   - Reuse an existing face from `assets/locked_factory_faces_v2/` whenever its SKU is listed in the approved manifest.
   - List every required structural, semantic, prop, and character particle.
   - For a new full-view theme family, draw and lock separate `left`, `front`,
     `right`, `back`, `top`, and `bottom` artwork. The current dual-table
     fixed-camera catalog is the explicit exception and uses only source-backed
     top/front/right.
   - Render every particle as one identical 3D cube and review the unit-cube contact sheet.
   - Save the approved set as a versioned particle manifest with relative paths and SHA-256 hashes. Scene code may reference only manifest materials.
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
   - 80-119 PCS: 1 core element.
   - 120-169 PCS: 2 core elements.
   - 170+ PCS: 2-3 core elements.
   - Aesthetic clarity beats using every listed element.
7. If PCS is unspecified, use aesthetic-count mode (`MAGNETIC_AESTHETIC_PCS=1`)
   with a soft planning cap. Complete the silhouette, support element and props,
   skip generic target filling, then use the actual 80-200 PCS result.
8. Build a model-based scene around one primary silhouette. Add support elements only when they improve recognizability.
9. For each theme, apply its dedicated archetype template before filling PCS.
   Run the hidden-title recognition test and the cross-theme silhouette test:
   the theme and role relationship must remain readable without the title, and
   the model must not reduce to another theme's skeleton after recoloring.
   Fillers must stay subordinate to the main silhouette. Save the batch PCS and
   structural signatures, then run `validate_scene_batch_diversity.py` before
   rendering.
10. Render and compose catalog sheets. Parts details and color-box scenes must reuse the exact locked particle textures and final scene render.
11. Run `work/audit_scene_geometry_blender.py` before catalog composition. Reject any duplicate, enclosed, hidden, low-visibility, wrong-size, or unexpected non-figure component.
12. Compare against competitor references before stopping. If it looks like colored material blocks instead of a recognizable scene, revise the model/texture plan.
13. When color direction is not approved, render the same geometry in controlled saturation variants. Do not change the model, materials, PCS, or layout between variants, and validate scene/detail/package tone separately for each variant.
14. For the two-table factory catalog, render the main scene and every detail
    icon with the same source-color material profile, exposure `0`, Standard
    color management, fixed camera direction, and no cast shadows. The texture
    must feed a strength-`1.0` emission shader directly; never mix it on top of
    diffuse shading or apply per-scene gamma, saturation, brightness, or a
    white-overlay fix.

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
- Catalog sheet size defaults to the approved `1600x1500` template unless the user chooses another resolution.
- Include PCS badge, Chinese scene name, 20mm cube icon on catalog sheets.
- Use `0.79 IN` on color boxes for foreign-facing size labeling.

## Validation Checklist

Before final response, check:

- Exact PCS count.
- When PCS was not specified, every result is within `80-200 PCS`; batches of
  six or more cover the low, middle, and high count bands.
- `scripts/validate_locked_factory_faces.py` passes with `64` SKUs, `192`
  `512x512` RGB files, and no SHA-256 mismatch before factory-library rendering.
- `scripts/validate_color_box_cutout.py` passes before inserting the approved
  package. Resize RGBA package assets in premultiplied-alpha mode so transparent
  white RGB or studio-floor shadow cannot bleed onto the blue catalog.
- Sum of all parts-detail quantities equals PCS.
- Every mixed-library detail label begins with `表1-` or `表2-` and resolves to
  exactly one manifest record. Never infer the source from color or artwork.
- Same cube size, no big/small cube.
- No cube misalignment.
- Grid audit reports zero fractional coordinates, one identical cube edge
  length, and exact one-unit center spacing for every adjacent pair.
- Exactly one connected main component; only complete one- or two-cube figures may be separate.
- For the current two-table factory catalog, all person/head/face-character
  particles are separate one-cube components. Their component sizes must all
  equal 1, the embedded-figure count must equal 0, and the duplicate-figure
  count must equal 0.
- Geometry audit reports zero enclosed cubes, zero camera-hidden cubes, zero low-visibility cubes, and zero cube-size errors. Use at least 12 visible face samples per cube for the production camera.
- White blocks do not merge into the background or each other.
- Top and side faces have no milky veil: side ink remains saturated, white tops remain neutral white, and their thin gray perimeter survives final downscaling.
- Unit renders retain the locked print color: top/right colored ink must not be
  clipped or covered by a gray/white lighting layer. For the dual-table catalog,
  validate the three source-backed visible faces only.
- Reject a technically valid scene if it still reads as a repeated block pile. The hero silhouette, interior/foreground story, texture rhythm, and figure placement must pass a buyer-view aesthetic review before batch generation.
- Parts-detail icons do not overlap counts.
- All one-cube detail icons use one fixed orthographic crop and one canonical alpha silhouette; never crop each material independently.
- Parts-detail colors match scene colors.
- Main-scene colored faces, parts-detail icons, and the color-box scene use one
  locked tone profile; reject visible side-face desaturation or gray drift.
- Pixel-compare detached one-cube figure/head particles against their exact
  detail icons after alpha-crop normalization. Median RGB and luminance error
  must each stay within `4/255`. This verifies the shared scene/detail renderer;
  reject any scene-only color adjustment even when aggregate averages look close.
- Project the top/front/right polygons of every detail icon and compare their
  color statistics against the corresponding authoritative source face files.
  Across the current batch, require median luminance error at most `1/255`, 95th
  percentile at most `3.5/255`, maximum at most `7/255`, and 95th-percentile
  saturation error at most `0.02`.
- Every featured character shows its complete front face without scene overlap.
- Every featured character has a role-specific expression and costume. Side,
  back, and top faces continue the headgear, hair, ears, sleeves, and clothing;
  none duplicates the front face.
- Character placement follows the story and is staggered across foreground,
  midground, and the hero structure. Reject a straight repeated front-row
  lineup or any placement that hides the face from the production camera.
- Theme templates pass the cross-theme silhouette test. Police, pirate,
  Christmas, engineering, farm, and other themes may not share one recolored
  wall/platform/stair skeleton.
- `scripts/validate_scene_batch_diversity.py` passes for multi-scene batches;
  no duplicate structural signature, overused template, or single-band PCS
  batch is accepted.
- Different PCS labels refer to genuinely different modeled geometry and exact
  counts. Never relabel one render as several PCS variants.
- Main-scene white/snow matches the detail icon's neutral white; do not accept
  cool gray or blue-cyan snow. Preserve only one thin neutral-gray seam.
- Color-box scene matches catalog scene brightness.
- Approved universal color-box insertion reuses the locked transparent asset; it is not regenerated per catalog.
- Color-box front is one complete perspective-mapped panel with no fold-line overrun, white hairline, double edge, or local patch seam.
- Color box dimensions and carton table follow the formula reference.
- At least one strong silhouette communicates the theme.

Report any remaining weak theme honestly instead of saying it is fine.
