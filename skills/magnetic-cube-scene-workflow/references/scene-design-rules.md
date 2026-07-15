# Scene Design Rules

## Current Dual-Table Camera Exception

The processed Table 1 + Table 2 catalog has only three source-backed visible
faces. For these scenes, lock the orthographic camera near
`center + (span*0.22, -span*1.82, span*0.64)` so only top/front/right appear.
Do not rotate the camera to reveal a runtime-aliased hidden face.

## Competitor Benchmark

Competitor scenes work because they have:

- A readable silhouette: tree, house, castle, ice tower, race gate, bridge, village, or character.
- A small-world composition: foreground figures, middle subject, rear height, side decorations.
- Purposeful printed blocks: doors, windows, roof, leaves, snowflakes, gifts, flags, tires, water, stone, faces.
- Bright printed-plastic finish with visible seams.
- Theme-specific figures, not generic repeated people.

## Single-Cube Benchmarking

Before tuning a material family, crop isolated cubes from the competitor's
parts-detail row whenever available. Record and compare:

- Neutral-white interior color and the single perimeter seam.
- Printed motif scale at one-cube size; brick, wood and foliage must remain
  readable after catalog downscaling.
- Front/top/side continuity. Semantic art stays on the intended front face;
  material texture wraps naturally onto the other faces.
- Highlight size and direction. Reject broad gray-white haze across an entire
  top face.
- Texture density. Reject dense pixel noise, tiny brick grids and unidentifiable
  green/red lines even when the full scene looks acceptable.

Use `work/analyze_competitor_cube_samples.py` to generate the isolated reference
sheet and material report for the current Christmas benchmark.

## Theme Planning

### Particle-First Theme Gate

For every new IP or theme family, finish the particle library before scene modeling:

- Approve a six-face sheet showing `left`, `front`, `right`, `back`, `top`, and
  `bottom` for each particle, followed by a single-cube 3D audit render.
- Approve a unit-cube 3D sheet confirming identical geometry, correct face direction, print scale, seam visibility, and color.
- Store the accepted material keys in a manifest. The scene, detail panel, and color box must all resolve their artwork from that same manifest.
- Do not create a one-off texture while placing scene cubes. Missing semantics mean the library is incomplete, so return to the particle stage.
- Use natural non-pixel textures for terrain, water, wood, foliage, stone, or roofing when they improve realism; reserve graphic or pixel treatment for iconic blocks, symbols, props, and character art.

Use the Excel column `可搭建核心元素` as the source of buildable objects. Do not combine too many theme ideas into one scene.

Element count by PCS:

- `<120`: one main element, optional tiny figure/decor.
- `120-169`: one main element plus one support element.
- `170+`: one main element plus one or two support elements.

Reject or postpone themes where no strong buildable core exists.

When the user does not specify PCS, do not select a target first. Use a soft
100-200 PCS planning range, complete only aesthetically necessary geometry, and
use the final modeled count in the badge, detail totals and packaging formulas.

## Buildability Screening

Before batch generation, score each theme:

- `keep`: clear silhouette, dedicated template, and clear print vocabulary.
- `keep_with_template_review`: usable theme, but only after a specific template is tuned.
- `skip`: no strong buildable core, likely to become a long strip/flat wall/random color block, or no dedicated texture family exists yet.

Hard capability gate for production batches:

- Clear subject silhouette: the buyer can identify the theme without reading the scene name.
- Dedicated texture library: the theme has semantic printed blocks and character/prop faces, not only generic material colors.
- Mature model template: the theme has a tested foreground/middle/back composition and known support elements.

Only themes that satisfy all three gates should enter automatic batch generation. If any one gate is missing, mark the theme as `skip` until that library/template is built.

Current screening status:

- Race track: skip production batches until a fully accepted road/gate/car template exists. Current versions can still read as generic colored blocks.
- Survival base: skip production batches until the house/mine/tree vocabulary is upgraded enough to read without the title.
- Princess/complex castle: skip production batches unless the gate/tower silhouette is clearly readable in a small preview.
- Prefer the current high-success theme pool for batches: ice world, ice castle, snow rescue, Christmas house/tree/workshop, pumpkin snow house, mushroom/pipe game scene, and island hut.

Use `MAGNETIC_SCREEN_THEMES=1` to generate a `theme_screening_report.json` and skip low-score themes in scripted batches.

For preview batches that should contain catalog sheets only, use `MAGNETIC_SHEETS_ONLY=1`. The output root should contain only the `资料图` folder; no `场景图` folder should remain.

## Composition Formula

Use this scene layout:

- Foreground: 1-3 themed figures or small props.
- Middle: the primary recognizable object.
- Back: tallest layer or vertical icon.
- Left/right: small support elements, trees, sign, gifts, podium, bridge, or tower.
- Depth rule: avoid spending too many PCS on a flat foreground platform. If the scene feels flat, move 5-10 low foreground cubes into the back subject, towers, roof, tree canopy, gate pillars, or bridge columns while keeping the exact PCS.

Avoid:

- One long horizontal strip.
- A single flat platform with dots.
- A scene where the front, middle, and back all have similar height.
- A wall of windows.
- Random blocks that only make sense when reading the title.
- Too many different elements from one Excel row.

## Theme Archetypes

- Survival base: small house, door, mine opening, tree, stone path, ore/pickaxe blocks.
- Race track: race gate, visible road, flags, tires, flames, podium, low stands; avoid making it look like a garage wall.
- Princess/castle: central gate, double towers, pink walls, roof/gold accents, garden/flower blocks, princess/knight figures.
- Ice/Frozen: ice tower, ice bridge, snow blocks, snowflake/crystal prints, snowman/penguin figures.
- Christmas: small house or tree, gifts, snow path, wreath, Santa/snowman/penguin; avoid only red/green random blocks.

## Current Production Template Library

Use these material/template modules before generic PCS filling:

- Survival base: compact house + mine entrance. Use `mine_entrance`, `mine_pickaxe`, `ore_blue`, `ore_gold`, `door`, `window`, natural `wood`, grass/dirt sides, and one tree. Avoid long bands of identical windows.
- Race track: road/gate + car props. Use `race_car_red`, `race_car_blue`, `race_flag`, `hazard`, `flame_print`, and controlled `space_dark` only for ground road. Do not stack large black walls.
- Princess castle: main gate + towers. Use `castle_window`, `castle_door`, `pink_brick`, `gold`, and `flower_print`. Keep the main silhouette vertical enough; avoid a single horizontal pink wall.
- Ice palace: central ice tower + bridge. Use `ice_palace_window`, `ice_crystal`, `ice_crown`, `snowflake_print`, `ice`, and `snow_stone`. Snow should stay white with seams, not gray.
- Christmas town: brick/snow house + tree + gifts. Use `brick_snow_cap`, `roof_snow`, `xmas_tree_icon`, `xmas_tree_snow`, `wreath_print`, `gift_red`, `gift_blue`, and `fireplace`. Avoid blue ice dominance and avoid plain white/grid blocks as roof decoration.

When PCS is 120-169, use one primary element plus one support element. When PCS is 170+, use one primary element plus two support elements only if they improve recognizability. If a support element weakens the subject, replace filler cubes with theme print blocks instead.

## Texture Rules

- Increase theme-print blocks when a scene reads as generic materials.
- Prefer themes with clear visual vocabulary for previews and batches: Christmas house/tree, ice tower/bridge, race gate/track, castle gate/towers, survival house/mine. Skip abstract themes until a dedicated texture/icon family exists.
- Keep materials semantically useful: grass for ground, brick for walls, window for house/castle, snow/ice for winter, gifts for Christmas.
- Do not use high-frequency material noise. Competitor-style cubes use clean printed patterns, not dense random pixels.
- Grass, leaf, dirt, stone, water, and ice should use smooth base color plus controlled print texture, not dense random pixels.
- Material blocks must feel like printed product cubes, not flat computer colors. Wood should use warm continuous grain and knots; red brick should use warm orange-red brick with softened mortar; roof/gift reds should be vivid but not neon; leaf/tree blocks should use natural green branch texture instead of uniform green.
- Diagnose "not vivid" with per-material local contrast before increasing global saturation. Strengthen dark branch strokes, brick edge shadows, and wood grain highlights independently; keep ice, water, blue brick, and blue gifts in a bright cyan-blue range instead of a deep saturated blue.
- For all future themes, tune the reusable material family first before changing theme composition. A weak material library will make every theme look artificial even when the model is correct.
- Current grass benchmark: natural medium green top with two scales of grass
  blades, visible tuft/leaf clusters and sparse tiny flowers; warm brown soil
  sides with mixed-size pebbles, short roots, and an irregular narrow grass
  fringe. The accents must survive catalog downscaling without becoming dense
  pixel noise. Avoid flat cartoon green and neon yellow-green unless the
  reference explicitly asks for it.
- Natural material readability benchmark: wood grain, brick mortar, roof seams, and snow/material boundaries must stay visible after the catalog sheet is scaled down. Wood should use darker wavy main strokes plus knots; red/orange brick should use warm off-white mortar with a slight shadow edge; snow caps need one thin neutral-gray transition line. Do not solve readability by turning white snow gray or cyan.
- Large contiguous snow roofs or ground surfaces must not use blank-white tops. Use mostly `snow_drift_top`, sparse `snow_crystal_top`, and theme-specific `snow_rescue_top` where appropriate. Keep the base white, use pale blue for the print, and vary the pattern family so the result does not become another repeated grid.
- Christmas benchmark: use one large readable hero shape, usually an L-shaped warm brick house/corner wall or a tall Christmas tree. Add a second smaller tree, gifts, windows, wreaths, snow caps, Santa/snowman/penguin figures, and a narrow foreground snow path.
- Christmas hard rules: no long straight brick wall as the main subject, no big flat snow platform, no white grid-panel blocks, no blue ice dominating the theme, and no green gift-tower shape when the intent is a tree.
- Premium Christmas print hierarchy: warm brick is the dominant architectural family; windows, door, fireplace, wreath, and lantern are localized building blocks; natural foliage is the dominant tree family; ribbon and bell prints are sparse tree accents; gifts stay near the entrance and never provide structural height.
- Do not put the same semantic artwork on every face. A wreath/window/lantern cube uses building material on top and sides and the semantic print only on the intended front face. Tree foliage may wrap around multiple faces.
- On Christmas buildings, prefer snow-top building cubes such as snow-on-brick or snow-on-roof. Plain white snow cubes are only for ground snow, snow piles, snowmen, or clearly snowy props.
- Treat color, texture, and structure as one decision. Do not brighten a weak scene to hide poor structure; first move filler PCS into the hero house/tree, then tune print brightness/saturation.
- For Christmas PCS filling, avoid stacking the foreground into a snow/dirt mountain. Keep the front low, and spend extra PCS on rear wall height, chimney/roof, tree canopy, entrance gifts, doors, windows, wreaths, and figures.
- Christmas tree cubes should read as foliage: deep green base, subtle branch texture, red/gold garlands or ornaments, and separate visible wood trunk blocks. They must not look like green gift boxes or random green material blocks.
- Christmas foliage tops remain green by default. Use white tops only on explicitly snowy foliage variants; a whole canopy of generic white tops creates the rejected milky-layer effect.
- Gifts are low story props only. Never stack gifts to consume PCS or use them
  as structural height; move surplus pieces into the hero silhouette, foliage,
  roof return, fireplace, windows or other semantic structure.
- Cube gaps should be narrow: keep bevels and printed edge lines subtle so connected magnetic cubes read as tightly attached.
- Current model bevel target is `PRODUCT_BEVEL = 0.006`, which keeps seams visible without making the scene look disconnected.
- For a user-approved strict line-to-line product view, override the generic
  bevel with `PRODUCT_BEVEL = 0.0015`, keep `CUBE_SIZE = 1.0`, disable local
  contact shadows, and add a 2-3 px hue-matched perimeter inside every 256 px
  face texture. This makes the shared grid line visible without opening a gap.
- Current 3D readability benchmark: use a stronger three-quarter camera, moderate top-down angle, visible side faces, natural directional face shading, and controlled front fill. Do not lift all shadows equally, or the model will look flat even when the geometry is correct.
- Do not add tight contact shadows or dark ambient-occlusion bands between connected cubes. They make the seams look wider and the product dirty. Preserve depth with one thin neutral-gray seam, a small controlled face-value shift that keeps the original ink hue, and one short pale grounding shadow immediately below the lowest cubes. Never add a gray side overlay, broad white face highlight, or alpha-shaped shadow behind the whole scene.
- Use plastic highlight/catchlight, but keep seams and do not wash out white blocks.
- Generate a separate top-face material for every reusable print family. Never reuse the front texture's baked broad catchlight on an upward face; preserve the material hue with a small top-only chroma/brightness compensation and retain directional shader shading for depth.
- Parts-detail blocks should use the same texture family as the scene. Treat the detail icons as the color reference: after scene lighting and sheet compositing, colored front faces in the main scene and color-box scene should have the same apparent brightness, saturation, and contrast as the corresponding detail icon. Preserve directional shading on side faces instead of flattening the whole model.
- Two-table factory-catalog exception: the Excel-derived source face is the
  color reference, not the lit detail icon. Use the locked source-color shader
  so scene and detail both preserve that face. Keep depth through geometry,
  perspective, seams, and printed outlines rather than diffuse darkening.
- Theme-specific printed blocks should carry the theme from a distance: race scenes need flags, tires, hazard stripes and flame blocks; ice scenes need snowflakes, crystal/crown blocks and blue ice bridges; Christmas scenes need tree garlands, gifts, wreaths, brick house walls, snow caps and themed figures. Do not let generic material cubes dominate the subject.

## Figures

- Characters may be one cube or two cubes.
- Two-cube figures are body + head only; do not add a third head-top cube.
- Face must be centered on its cube.
- Character cubes must be role designs, not just a front sticker. The front, visible side, and top faces should continue the same hair/hat/clothing design, similar to competitor character blocks.
- The visible side face must continue the role design through hat/hair, ear/beard, scarf, sleeve/arm, pants, shoes, wing, or belly. Do not draw eyes, nose, or mouth on the side; keeping facial features only on the front prevents the side from reading as a duplicated second face.
- A side panel must never reuse the front-face composition. For penguins, use a dark side head, wing, and narrow belly continuation without the centered white face patch. For Santa and snowmen, wrap hat/brim, beard/scarf, and clothing around the side without another face.
- Do not use one-cube human templates that read as a detached head. Until a theme has an approved full-character one-cube print, use complete two-cube body+head roles. On side textures, draw one coherent profile and one visible arm; never mirror two profiles across the side face or add a front-shirt center seam to the side.
- Figure style must match theme:
  - Race: driver/mechanic.
  - Castle: princess/knight/royal character.
  - Ice: snowman/penguin/winter child.
  - Christmas: Santa/snowman/penguin.
  - Mine/base: miner/worker/monster.
- Use a dedicated cast for every mature scene template. In a five-scene preview batch, do not reuse the same lead role across scenes when a theme-specific role exists.
- A licensed or named character cannot be represented by a generic color-coded
  person. Lock the real product's recognition anchors before rendering: head
  silhouette, hat/crown/helmet mark, eye and nose proportions, hair or
  moustache shape, glove/hand treatment, costume cut, and role-specific body.
  Validate these anchors against the supplied physical-product reference at
  single-cube size before placing the figure in a scene.
- Late texture/polish passes must not reintroduce duplicate character blocks. Run final cast cleanup after all theme accents; rescue scenes may contain only one dog unless the design explicitly requires more.
- A one-cube animal is a complete character block, not a face sticker. Its front must show a centered readable face and costume, while top and side faces continue ears, fur, clothing, tail, wing, or equipment without duplicating the front face.
- Figures can stand outside the scene when that improves alignment and readability.
- Keep a theme's hero entrance and primary facade clear. For Christmas house scenes, spread figures across the left and right foreground inside the structure's overall width; do not cluster them in front of the central door, and do not push them so far outside that the scene is scaled down to fit.
- In the production camera, every primary door, window, face, badge, and symbol must remain a complete readable print. A projecting return wall may show depth, but it must not mask half of an adjacent front-face print; relocate the print to a fully visible grid cell when perspective creates a false misalignment.
- For the approved product angle, use an orthographic camera with lateral offset `0.32 x scene span`, depth offset `-1.50 x span`, and height offset `0.50 x span`. Keep this locked across the scene, details, and package unless the user explicitly selects another angle.
- Foreground figures must not overlap each other in the rendered camera view. Keep roughly three cube widths between neighboring figures for the current three-quarter camera, then inspect the raw render before composing the sheet.
- Two-table factory-catalog exception: a source SKU that is itself a one-cube
  head, face character, or creature head must remain one complete detached
  cube. It may be shown as a foreground character/prop, but it must never be
  inserted into a wall, roof, ground, tree canopy, or other connected structure.
  Audit by material key after all remapping; visual intent alone is not enough.

## Designer-Grade Particle Art Gate

- Design the particle before building the scene. A material or character is not approved until its left, front, right, back, top, and bottom faces are shown together with a rendered cube preview.
- Treat the six faces as one three-dimensional object, not six unrelated stickers and not one front sticker repeated on every side.
- Assign a job to every face. Front carries the strongest recognition cue; left and right continue silhouette/material; back contains a believable rear treatment; top explains hair, hat, grain, foliage, lid, roof, or surface; bottom uses a plausible underside rather than a generic colored dot.
- Character particles need distinct silhouette anchors as well as distinct eyes and mouths. Use role-specific ear, hair, hat, wing, tail, horn, beard, scarf, sleeve, footwear, and rear-view cues. Never use a generic side circle as a substitute for a designed arm or profile.
- Animal and fantasy characters should follow the supplied designer-sheet logic: centered front identity, asymmetrical left/right body continuation when appropriate, rear tail/marking, explicit top anatomy, and a restrained underside.
- Natural materials need multi-scale texture: one readable large form, medium clusters or grain, and sparse fine detail. Avoid flat color fields, uniform procedural dots, and evenly repeated symbols.
- Organic textures should have controlled irregularity and embedded value depth. Leaves, grass, stone, soil, wood, ore, crystal, water, and lava must look like different materials even in grayscale.
- Functional blocks use semantic hierarchy. A door, window, fireplace, chest, workbench, bed, bookcase, or lantern has one or two hero faces; other faces return to the underlying wood, brick, metal, cloth, or stone structure.
- Use one coherent illustration language per collection: consistent outline weight, edge softness, highlight direction, shadow depth, and palette. Do not mix flat vector icons, pixel noise, painterly textures, and photographic grain indiscriminately.
- Premium color is not maximum saturation. Preserve dark anchors, midtone richness, small controlled highlights, and clear material separation. Avoid broad gray overlays on top/side faces and avoid large pure-color areas without internal structure.
- At catalog size, each particle must pass three tests: recognizable material/role, visible cube edges, and no face that looks unfinished or merely filled with a placeholder color.
- Scene generation is blocked when a required hero particle fails the six-face sheet. Fix the particle library first; do not hide weak particles inside a larger model.
- Do not apply one generic grain/noise pass to every face. Natural materials may use restrained, material-specific microtexture; characters, gifts, symbols, doors, windows, and other illustrated/function blocks stay clean unless their design explicitly requires texture.
- Reject placeholder anatomy and placeholder sides: generic circles for arms, one repeated face on several sides, a colored dot on every top, or a single stripe used as the entire rear treatment are not production-ready.
- For holiday characters, lock distinct facial grammars and six-face cues per role. Santa, snowman, gingerbread, witch, ghost, and pumpkin roles must differ in eye shape, mouth construction, headwear/hair, side silhouette, back treatment, top treatment, and body construction.

## Aesthetic-First PCS Rule

- When PCS is unspecified, `80-200 PCS` is a feasibility range, not a target.
- PCS is an output of the approved scene, not a quota that the model must fill. Stop adding cubes when the hero silhouette, supporting structure, character story, and foreground rhythm are complete.
- Never consume a requested range by extending the base, building a gift row, stacking generic walls, repeating decorations, or adding hidden support cubes without visible semantic value.
- After the scene passes visual review, count the actual cubes and propagate that exact number to the badge, parts detail, package, dimensions, weights, and carton calculations.
- Different themes in the same batch may have different PCS. Visual quality and theme readability take precedence over matching counts.
- Select support-element count from visual need: normally one primary silhouette plus one support element below 120 PCS, one or two supports at 120-159 PCS, and up to three supports at 160-200 PCS only when each support improves recognition or story. These are soft limits; delete a support that weakens the composition.
- Do not start batch production from a requested theme list. First complete and approve one full sample through particle sheet, geometry audit, raw scene, detail panel, and package-scene color matching.

## Anti-Template Layout Gate

- A new theme must not reuse another theme's full scene skeleton and merely swap colors or face prints. Change the hero silhouette, secondary structure, height rhythm, open space, and foreground contour together.
- Do not default to a centered rectangular building with one decoration on each side and three figures in a straight foreground row. That arrangement is allowed only when the subject itself requires a formal lineup.
- Give each mature theme a dedicated structural template. Christmas may use an asymmetric cottage plus a hero tree; Halloween may use a tall manor/tower plus a lower graveyard; other themes need their own readable subject silhouette.
- Figure placement is selected from the scene story and camera visibility, not fixed slots. Prefer a mixed arrangement: at least one figure integrated near the hero structure, one figure near a secondary element or in the midground, and an optional foreground figure used only when it does not shrink or obscure the scene.
- Vary character depth, lateral position, and relationship to the subject between themes. Do not reuse the same left/center/right coordinates across a batch.
- Before publishing two or more scenes, compare their black silhouettes and figure-position maps. If they still look interchangeable without textures, rebuild one scene before rendering catalog sheets.
- Compare every new scene against the recent approved templates with textures hidden. Reject it when the same base contour, hero position, height peak, open-space map, or figure map can be recognized as a recolored previous scene.
- Every mature theme must have all three assets before batch use: a clear hero silhouette, a dedicated six-face particle family, and a tested structural model template. Screen out the theme when any one is missing and a strong result cannot be built without generic filler.

## Cross-Theme Buyer Acceptance Gate

- Hide all titles and PCS labels. A buyer must identify the scene category and its main action or location within one glance. Color alone does not count as identification.
- The largest visual mass must be the theme hero. Secondary elements must frame or explain it rather than compete with it.
- Characters must perform theme-specific jobs and occupy camera-visible story positions. Do not reuse a generic cast, expression set, or fixed foreground lineup across themes.
- Check the final production camera for complete hero silhouette, complete faces, readable doors/windows/symbols, and no overlap from detail panels, box art, badges, or dimension lines.
- Tune color by material family, not by one global saturation multiplier. Match the scene and package-scene front faces to the detail icons while preserving natural directional side shading; never accept a gray side film or milky top film.
- Publish only after geometry and presentation both pass: identical cube size, integer-grid alignment, one connected scene component unless a separate figure is intentional, no duplicates, no enclosed invisible filler, exact parts sum, and no visually unexplained cubes.

## User-View Quality

Ask: if the scene name is hidden, can a buyer still tell what it is?

If no, improve in this order:

1. Strengthen the main silhouette.
2. Replace generic material blocks with semantic printed blocks.
3. Add or move theme-specific figures.
4. Adjust height/width rhythm.
5. Only then adjust brightness or saturation.

## Christmas Quality Gate

Before accepting a Christmas scene, compare it against the competitor Christmas reference:

- One glance should read as Christmas without the title.
- The largest silhouette should be a house/corner wall or a tree, not a horizontal strip.
- Tree cubes must show a visible trunk and stepped leaf canopy.
- Brick blocks should form a house/wall body with windows/door/wreath, not a repeating red texture band.
- Snow caps should be plain white/snow texture with subtle seams, never panel/grid squares.
- Snow-ground top faces must not contain random blue/green dots or dark grain; after catalog downscaling these read as stains. Keep the neutral-white face clean and use the thin perimeter seam for cube separation.
- Pure-white snow or floor top faces use one thin cool light-gray connection line only. The exposed fold where a white top turns into the vertical side gets a separate slightly stronger single edge; do not simulate that fold by thickening every internal connection and do not add parallel inner frames. On the accepted Christmas snow-ground side, remove the former grass/drip fringe and use one continuous 5 px neutral-gray line at the snow-cap/soil transition; it must remain solid after catalog and package downscaling.
- When a complete cutout is placed on a white catalog or package background, protect the scene at the composition stage: create a 1-1.5 px neutral-gray outside-only alpha contour, enlarge the hero scene within validated no-overlap bounds, and add one short pale grounding shadow. Do not keep increasing the texture seam to solve package downscaling.
- White grid seams use one-sided ownership: for the approved camera/UV orientation, draw only the camera-facing bottom border and left border on each white top texture so every shared cube boundary is rendered once. Keep the accepted vertical seam at 5 px in the 256 px source texture. Because the camera-facing horizontal seam loses more coverage during texture filtering and final downscaling, inset it by about 9 px and render it at 9 px with a slightly darker neutral gray. Validate both line families on the final 2400x1650 catalog and package image, not only on the source texture or raw render. The cutout contour supplies the remaining exposed silhouette. Never draw a full inset rectangle on every adjacent white cube, because that creates a double line.
- Foreground figures and gifts should sit near the house entrance or path so the scene feels inhabited.
- Do not force a stepped gable or broad roof only to consume PCS. The approved compact Christmas template uses an open facade, shallow forward snow awning, short chimney, two stepped trees, and a low snow path. Publish the aesthetic result even when it lands near 119 PCS instead of the planning cap.
- Remove every counted wall-foot or terrace cube that the approved camera cannot clearly show. Reallocate only to a meaningful visible element; if no such element is needed, lower the actual PCS.
