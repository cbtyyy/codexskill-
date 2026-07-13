# Local Workflow

## Important Paths

- Blender: `C:/Program Files/Blender Foundation/Blender 5.1/blender.exe`
- Work dir: `C:/Users/Administrator/Documents/Codex/2026-07-05/new-chat/work`
- Competitor references: `D:/Users/Administrator/Desktop/磁力方块场景/`
- Theme Excel: `D:/Users/Administrator/Desktop/海外热度IP节日磁力方块场景主题表.xlsx`
- Default output root: `D:/Users/Administrator/Desktop/生成的场景图/`

Main scripts:

- `scripts/compose_approved_catalog_sheet.py`
- `scripts/compose_approved_color_box.py`
- `work/blender_magnetic_cube_batch.py`
- `work/generate_excel_theme_scenes_blender.py`
- `work/generate_core_element_5_outputs.py`
- `work/make_product_sheets_with_parts.py`
- `work/render_part_icons_blender.py`
- `work/render_color_boxes_blender.py`
- `work/analyze_competitor_cube_samples.py`

## Current Rendering Policy

Use model-based rendering with:

- `MAGNETIC_CORE_ELEMENT_MODE=1`
- When PCS is not specified, also set `MAGNETIC_AESTHETIC_PCS=1` and use
  `MAGNETIC_AESTHETIC_PLANNING_PCS=150`. The planning value is only a soft
  size guide; skip generic filling and publish the final modeled count if it is
  within 100-200 PCS.
- Do not set `MAGNETIC_FLAT_DETAIL_RENDER=1` for main scene rendering. Main scenes need real lit plastic material, ambient occlusion, and contact shadows.
- Render parts-detail icons with `render_part_icons_blender.py` after the main scene render. The parts panel must prefer these real Blender icons over flat exported face textures so the scene and details share the same material, lighting, and post-processing.
- Render parts icons with `MAGNETIC_ICON_LIGHTING_SPAN` equal to the scene metadata `scene_span`.
- Use the fixed 320px camera crop `(67,66,253,254)` and the canonical `orange_brick` alpha silhouette for every one-cube icon. Never alpha-crop each material independently. Validate normalized visible bounds; largest and smallest icon extents may differ by no more than 3 pixels.

This keeps the cube geometry deterministic and reduces lighting mismatch between scene and parts-detail icons.

Current tone target in scripts:

- Catalog background is now a very light warm gray around `(247,247,245)` for the current optimized preview. Keep the detail panel background the same as the sheet background.
- Base texture exposure around `0.96`.
- Saturation around `1.44`.
- Contrast around `1.14`.
- Product post-processing exposure around `1.75` for the current lit render.
- Product color factor around `1.30`.
- Product contrast factor around `1.16`.
- Product sharpness around `1.18`.
- Gamma around `0.68` and midtone lift around `0.02`.
- Highlight guard around `0.35` so white/snow remains white without clipping seams.
- Scene and Blender detail icons use the same post chain. Keep scene-only brightness/color/contrast/gamma at `1.0`; do not use an extreme second scene lift.
- Keep `MAGNETIC_SCENE_WHITE_MATCH_STRENGTH=0.0` while scene and icons share the same lighting pipeline. Do not recolor only the scene whites.
- Competitor-calibrated luma curve: pivot `113`, target `118`, shadow slope `2.55`, midtone slope `2.70`, highlight knee `143`, highlight slope `0.45`, chroma factor `1.06`. Apply this one curve to the scene, Blender detail icons, and the scene pasted onto the color box.
- Current Christmas calibration benchmark: competitor colored-scene median luma/saturation `114.01 / 0.692`; generated sheet approximately `115.95 / 0.688`. Keep deviations within about 3 luma points and 0.02 saturation.

Current controlled saturation presets for the same modeled scene:

- A light reduction: `MAGNETIC_PRODUCT_COLOR=1.50`, `MAGNETIC_SCENE_COLOR=1.55`, `MAGNETIC_SCENE_BRIGHTNESS=1.11`.
- B medium reduction: `MAGNETIC_PRODUCT_COLOR=1.30`, `MAGNETIC_SCENE_COLOR=1.55`, `MAGNETIC_SCENE_BRIGHTNESS=1.11`.
- C restrained: `MAGNETIC_PRODUCT_COLOR=1.12`, `MAGNETIC_SCENE_COLOR=1.80`, `MAGNETIC_SCENE_BRIGHTNESS=1.11`.
- These are calibrated presets, not generic filters. Re-run tone validation for each theme because the proportion of white, green, brick, and character blocks changes the measured median.
- The accepted Christmas sample starts from A but requires
  `MAGNETIC_SCENE_COLOR=1.65` and `MAGNETIC_SCENE_BRIGHTNESS=1.12` to match its
  parts-detail icons. Treat these as theme calibration values, not a new global
  preset.
- Keep `MAGNETIC_SCENE_WHITE_TARGET=239,238,234` and
  `MAGNETIC_SCENE_WHITE_MATCH_STRENGTH=0.86` for the accepted neutral-white
  snow baseline. The correction applies only to low-chroma highlights and
  leaves gray seams and stone untouched.

Current 3D depth target in scripts:

- Camera position uses a near-frontal three-quarter view around `(span*0.32, -span*1.50, span*0.50)`.
- Keep object shadows enabled and use EEVEE ambient occlusion around distance `2.25`, factor `0.38`.
- Keep front fill lower than the key light so side faces retain shading and the scene does not look flat.
- Use only a short pale grounding shadow below the lowest cubes, roughly one cube height or less. Do not use a whole-scene alpha cast shadow on catalog sheets.
- Do not compare the aggregate scene median directly with the aggregate detail-panel median: the scene is count-weighted while the panel shows each material once. Enforce one shared render/post chain and compare corresponding material cubes visually or with per-material samples.
- For neutral white product pixels, also require scene/detail median luminance
  difference `<=4` and per-channel median difference `<=7`.
- Validate the scene's visible alpha bounds against reserved rectangles for the color box, parts panel, right-side PCS/size block, and parameter table. Generation must fail instead of outputting an overlapping sheet.
- Frame raw Blender renders from camera-space projected cube bounds and use a large safety factor (currently `1.62`). Require at least 12 transparent pixels on every raw-render edge before sheet composition; this prevents foreground feet or tall rear blocks from being permanently cropped.
- Product midtone lift should stay around `0.20`; higher values make the scene brighter but flatter.
- Use depth-relief postprocessing in core-element mode: move a small number of front flat ground cubes into rear/tower/roof/tree/gate columns while preserving exact PCS.

The exact values can be tuned, but the main scene, color-box scene, and detail icons must have similar apparent brightness and saturation. Use the detail icons as the visual reference and keep colored scene pixels near the competitor brightness range rather than preserving a darker render value.

Current Christmas template:

- Use `brick_snow_cap` for building roof/corner snow so the sides still read as brick. Use `snow_cap` only for ground snow or clear snow props. Do not use `white_panel` for Christmas snow caps.
- Use a narrower L-shaped brick house/corner wall, not a full-width red wall.
- For an unspecified-PCS Christmas composition, start from a compact planning grid but keep only the necessary footprint. The current audited sample is 119 PCS: 113 cubes in one connected scene plus three complete two-cube figures. It uses an open cottage facade, forward snow awning, short chimney, two trees and a low terrace; no stepped-gable filler.
- Add one large visible-trunk Christmas tree and one smaller side tree. Tree canopy texture should be foliage plus garland, not gift-ribbon stripes.
- Use `snow_dirt` for warm snow-covered ground sides and `fireplace` when the core element is a chimney/house.
- Use `roof_snow` for red roof blocks with snow on top, and `xmas_tree_snow` for upper tree-canopy blocks. This gives the scene a cleaner competitor-style snow layer without turning the whole object white.
- Put house entry details on the visible facade: grouped door, paired windows, wreath/roof detail. Do not place the entry on the foreground snow path, or it creates a gray blocking wall.
- Keep blue/ice accents sparse; red gifts, wreaths, windows, and figures carry the theme.
- The current aesthetic-review Christmas cottage is a compact open-room composition around 125 PCS: warm brick back wall, short right return, chimney, wood interior, low snow terrace, one tall tree, one smaller tree, grouped gifts, Santa, snowman and penguin. Do not restore the former wide facade or long front snow strip.
- Christmas foliage uses the dedicated `xmas_tree_top` top material and dimmed foliage sides. A white top is reserved for explicit `xmas_tree_snow` pieces; never blanket every tree cube with the generic snow top.

Current natural material baseline:

- Current clean color chain avoids the former aggressive gray-haze curve: product exposure `1.88`, color `1.19`, contrast `1.08`, gamma `0.78`, sharpness `1.20`, no midtone lift, and `PRODUCT_TONE_CURVE=0`. Apply the same chain to scene, detail icons and package-scene source.

- `print_wood` uses warm brown continuous grain, visible darker wavy strokes, knots, and mild highlights. It should remain readable at catalog scale.
- `print_orange_brick` uses warm orange-red bricks, clear warm off-white mortar, a slight shadow edge, and per-brick variation. Avoid pure white grid lines, but do not make mortar so soft that the brick pattern disappears.
- `print_roof` and `roof_snow` use natural red roof texture with tile shadowing before snow is applied.
- Snow-on-brick and snow-on-roof transitions use one thin neutral-gray boundary line so white snow stays white while still separating from the material below.
- White top faces use a wider neutral perimeter seam that remains about 1-2 pixels at final catalog scale. Their current material baseline is roughness `0.36`, specular `0.07`, and coat weight `0.008`; do not use the glossy colored-face settings on snow tops because they create a broad white haze against the sheet background.
- Every material used on an upward cube face must be rendered through its generated `__top` material instance. Top instances omit the texture-baked broad white catchlight, receive only an `1.06` chroma grade plus a `+2` value lift, and use roughness `0.30`, specular `0.09`, coat weight `0.012`, and non-white emission strength `0.02`. This is a global rule for brick, wood, grass, gifts, figures, foliage, and all future materials.
- Build scene models before material initialization, collect their actual cube material names, and call `create_materials(used_materials)`. Keep the no-argument form only for full-library icon/export jobs. This avoids regenerating unused top-face variants and reduces a one-scene review render from roughly eight minutes to about one minute.
- Side-specific materials ending in `_side_dim` must not receive the baked broad catchlight used on front artwork. Use clean side ink density (`0.88` for Christmas foliage, `0.84` for the other current side families), roughness `0.32`, specular `0.08`, and coat weight `0.01`. This preserves real face direction without turning green/orange side faces pastel-white.
- Explicit white calibration starts at luma `196`, maps that point to `234`, uses slope `0.55`, caps at `251`, and retains `0.25` of neutral chroma. Apply the same map to the main scene, parts icons, and color-box scene so white highlights stay clean while printed snow and face shading retain visible internal contrast.
- After scene geometry and material cleanup, call `apply_semantic_snow_top_design`. Ice worlds mix white-blue drift and sparse crystal tops; snow rescue uses blue direction marks; Christmas uses drift tops with a higher crystal ratio. Only visible top cubes are replaced, so PCS and side materials remain unchanged.
- `gift_red` uses a vivid but slightly warmer red with subtle print variation, not neon flat red.
- `xmas_tree_icon` uses natural green branch texture plus garland; keep it readable as foliage rather than a green package block.
- Dedicated theme print materials currently available: `castle_window`, `castle_door`, `mine_entrance`, `race_car_red`, `race_car_blue`, and `ice_palace_window`. Keep them registered in both `blender_magnetic_cube_batch.py` and `make_product_sheets_with_parts.py` so scene and parts-detail icons match.
- Premium Christmas materials also include `xmas_window`, `xmas_lantern`, `xmas_tree_ribbon`, and `xmas_bell_print`. `wreath_print`, `xmas_window`, and `xmas_lantern` must keep brick/wood top and side faces instead of repeating the front artwork on every face.
- Current optimized 5-scene preview uses output subdir `核心元素5张完善版` and the output script accepts `MAGNETIC_OUTPUT_SUBDIR`, `MAGNETIC_PREVIEW_LABEL`, and `MAGNETIC_SHEET_BG` so test batches do not overwrite unrelated outputs.
- Current optimized preview uses output subdir `核心元素3张优化测试` and the output script accepts `MAGNETIC_OUTPUT_SUBDIR`, `MAGNETIC_PREVIEW_LABEL`, and `MAGNETIC_SHEET_BG` so test batches do not overwrite unrelated outputs.

## Analyze Competitor Cubes

Run this before changing shared Christmas materials:

```powershell
python 'C:\Users\Administrator\Documents\Codex\2026-07-05\new-chat\work\analyze_competitor_cube_samples.py'
```

It writes `work/competitor_cube_samples.png` and
`work/competitor_cube_material_report.json` from isolated detail-row cubes.

## Generate an Aesthetic-Count Preview

When the user gives a theme but no PCS:

```powershell
$env:MAGNETIC_CORE_ELEMENT_MODE='1'
$env:MAGNETIC_AESTHETIC_PCS='1'
$env:MAGNETIC_AESTHETIC_PLANNING_PCS='150'
& 'C:\Program Files\Blender Foundation\Blender 5.1\blender.exe' -b --python 'C:\Users\Administrator\Documents\Codex\2026-07-05\new-chat\work\generate_excel_theme_scenes_blender.py'
```

The metadata, badge, detail counts and packaging calculations must use the
actual model count returned by Blender.

Run the production geometry gate before rendering parts or packaging:

```powershell
$env:MAGNETIC_MIN_VISIBLE_SAMPLES='12'
& 'C:\Program Files\Blender Foundation\Blender 5.1\blender.exe' -b --python 'C:\Users\Administrator\Documents\Codex\2026-07-05\new-chat\work\audit_scene_geometry_blender.py'
```

The gate must report one connected main component, only one-/two-cube figure components, zero hidden/enclosed/low-visibility cubes, zero duplicates, and zero size errors.

## Generate 5 Test Scenes

PowerShell:

```powershell
$env:MAGNETIC_THEME_JSON='C:\Users\Administrator\Documents\Codex\2026-07-05\new-chat\work\excel_theme_rows_5_texture_test.json'
$env:MAGNETIC_CORE_ELEMENT_MODE='1'
Remove-Item Env:\MAGNETIC_FLAT_DETAIL_RENDER -ErrorAction SilentlyContinue
& 'C:\Program Files\Blender Foundation\Blender 5.1\blender.exe' -b --python 'C:\Users\Administrator\Documents\Codex\2026-07-05\new-chat\work\generate_excel_theme_scenes_blender.py'
& 'C:\Program Files\Blender Foundation\Blender 5.1\blender.exe' -b --python 'C:\Users\Administrator\Documents\Codex\2026-07-05\new-chat\work\render_part_icons_blender.py'
& 'C:\Program Files\Blender Foundation\Blender 5.1\blender.exe' -b --python 'C:\Users\Administrator\Documents\Codex\2026-07-05\new-chat\work\export_scene_textures_blender.py'
python 'C:\Users\Administrator\Documents\Codex\2026-07-05\new-chat\work\generate_core_element_5_outputs.py' --stage textures
& 'C:\Program Files\Blender Foundation\Blender 5.1\blender.exe' -b --python 'C:\Users\Administrator\Documents\Codex\2026-07-05\new-chat\work\render_color_boxes_blender.py'
python 'C:\Users\Administrator\Documents\Codex\2026-07-05\new-chat\work\generate_core_element_5_outputs.py' --stage outputs
```

## Theme Screening

Use screening before larger batches:

```powershell
$env:MAGNETIC_THEME_JSON='C:\Users\Administrator\Documents\Codex\2026-07-05\new-chat\work\excel_theme_rows_5_texture_test.json'
$env:MAGNETIC_SCREEN_THEMES='1'
& 'C:\Program Files\Blender Foundation\Blender 5.1\blender.exe' -b --python 'C:\Users\Administrator\Documents\Codex\2026-07-05\new-chat\work\generate_excel_theme_scenes_blender.py'
```

The script writes `work/theme_screening_report.json`. Themes marked `skip` are not rendered. Themes marked `keep_with_template_review`, such as the current race track template, should be generated only for small tests until the template is accepted by the user.

## Batch Generation

For 20/50-scene batches, first create or update the theme JSON from the Excel source. Keep only themes with strong buildable core elements. Then set `MAGNETIC_THEME_JSON` to that JSON before running Blender.

When clearing folders, only delete inside the intended output directory under `D:/Users/Administrator/Desktop/生成的场景图/`.

Current catalog-only batch mode:

```powershell
$env:MAGNETIC_THEME_JSON='C:\Users\Administrator\Documents\Codex\2026-07-05\new-chat\work\excel_theme_rows_10_easy.json'
$env:MAGNETIC_CORE_ELEMENT_MODE='1'
Remove-Item Env:\MAGNETIC_FLAT_DETAIL_RENDER -ErrorAction SilentlyContinue
& 'C:\Program Files\Blender Foundation\Blender 5.1\blender.exe' -b --python 'C:\Users\Administrator\Documents\Codex\2026-07-05\new-chat\work\generate_excel_theme_scenes_blender.py'
& 'C:\Program Files\Blender Foundation\Blender 5.1\blender.exe' -b --python 'C:\Users\Administrator\Documents\Codex\2026-07-05\new-chat\work\render_part_icons_blender.py'
& 'C:\Program Files\Blender Foundation\Blender 5.1\blender.exe' -b --python 'C:\Users\Administrator\Documents\Codex\2026-07-05\new-chat\work\export_scene_textures_blender.py'
$env:MAGNETIC_OUTPUT_SUBDIR='10个好实现主题资料图'
$env:MAGNETIC_PREVIEW_LABEL='10张'
$env:MAGNETIC_SHEET_BG='247,247,245'
$env:MAGNETIC_SHEETS_ONLY='1'
$env:MAGNETIC_OUTPUT_AT_ROOT='1'
python 'C:\Users\Administrator\Documents\Codex\2026-07-05\new-chat\work\generate_core_element_5_outputs.py' --stage textures
& 'C:\Program Files\Blender Foundation\Blender 5.1\blender.exe' -b --python 'C:\Users\Administrator\Documents\Codex\2026-07-05\new-chat\work\render_color_boxes_blender.py'
python 'C:\Users\Administrator\Documents\Codex\2026-07-05\new-chat\work\generate_core_element_5_outputs.py' --stage outputs
```

The current preferred 10-theme production pool is stored in `work/excel_theme_rows_10_easy.json`. It excludes survival base, race track, and complex castle until their dedicated libraries are strong enough.

When `MAGNETIC_OUTPUT_AT_ROOT=1` and `MAGNETIC_SHEETS_ONLY=1` are both set, the desktop output root is cleared and should contain only the `资料图` folder. The catalog scene is fitted into a fixed safe area so it does not run under the color box, parts panel, PCS/size icon, or bottom parameter table.

## PowerShell Chinese Path Caution

PowerShell output may display Chinese paths as mojibake. Prefer constructing paths inside Python with Unicode escapes or use `Path('D:/Users/Administrator/Desktop') / '<unicode string>'` in scripts. Do not assume a displayed mojibake path means the file was saved incorrectly.

## Quick Quality Metrics

Use PIL to compare colored scene pixels against competitor references:

- Filter product pixels roughly with saturation `>0.16` and luminance between `30` and `248`.
- Track mean, median, p25, p75 luminance and median saturation.
- If scene median is below `136`, it will likely feel dark.
- If p75 is far below competitor while median is OK, it lacks glossy highlights.

## Christmas And Halloween Particle-First Pair

The paired holiday workflow lives in:

`C:\Users\Administrator\Documents\Codex\2026-07-05\new-chat\work\holiday_particle_first_v1`

It locks a `0.32 x span` orthographic lateral camera offset and a slightly
lower `0.44 x span` camera height, and produces two 150 PCS scenes. Run the
full pipeline in this order:

```powershell
python 'C:\Users\Administrator\Documents\Codex\2026-07-05\new-chat\work\holiday_particle_first_v1\draw_holiday_particles.py'
& 'C:\Program Files\Blender Foundation\Blender 5.1\blender.exe' -b --python 'C:\Users\Administrator\Documents\Codex\2026-07-05\new-chat\work\holiday_particle_first_v1\render_holiday_assets_blender.py'
& 'C:\Program Files\Blender Foundation\Blender 5.1\blender.exe' -b --python 'C:\Users\Administrator\Documents\Codex\2026-07-05\new-chat\work\holiday_particle_first_v1\audit_holiday_scenes_blender.py'
python 'C:\Users\Administrator\Documents\Codex\2026-07-05\new-chat\work\holiday_particle_first_v1\compose_holiday_outputs.py' --stage prebox
& 'C:\Program Files\Blender Foundation\Blender 5.1\blender.exe' -b --python 'C:\Users\Administrator\Documents\Codex\2026-07-05\new-chat\work\render_color_boxes_blender.py'
python 'C:\Users\Administrator\Documents\Codex\2026-07-05\new-chat\work\holiday_particle_first_v1\compose_holiday_outputs.py' --stage final
```

Do not replace the holiday face library with the older generic Christmas or
Halloween materials. Scene, detail icons, and package front must all reuse the
locked six-face files from `holiday_particle_first_v1/faces`.
