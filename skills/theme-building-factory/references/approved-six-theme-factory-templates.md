# Approved Six-Theme Factory Templates

Use this library for engineering, pirate, Christmas, Halloween, firefighting,
and police requests. These are six separate model families, not one scene with
six palettes.

## Shared production order

1. Draw and approve the theme's complete particle library first.
2. Render every particle as one identical cube and review its visible faces.
3. Build low-detail geometry candidates on integer coordinates with one-unit
   cubes and no simulated gaps.
4. Select the candidate by buyer recognition and scene beauty, then accept its
   natural count within `80-200 PCS`.
5. Apply only the locked particle materials. The scene, parts icons, and color-
   box scene must reuse the same renders and tone chain.
6. Audit duplicate coordinates, size, grid alignment, PCS sum, connected scene
   components, figure completeness, camera framing, reserved layout regions,
   and package calculations before delivery.

Do not start with a requested PCS and pad the scene. PCS follows the approved
silhouette, supporting story, and useful props.

## Approved structural signatures

### Engineering: tower-crane station

- Current approved pilot: `132 PCS`.
- Hero silhouette: tall connected tower crane with a long asymmetric boom and
  one suspended load.
- Secondary mass: open, partially completed station frame with visible bays,
  scaffold, concrete, steel beams, localized brick, and windows.
- Story path: work-yard foreground to frame, crane, hook, and load.
- Characters: engineer and worker occupy separate work functions and show their
  complete front artwork.
- Reject a solid building facade, centered symmetrical crane, or broad empty
  concrete platform.

### Pirate: skull-cave dock

- Current approved pilot: `153 PCS`.
- Hero silhouette: dark skull-like cave mass with a readable entrance and high
  lookout accent.
- Secondary mass: irregular water edge, wooden dock, treasure path, palm/shore
  accent, and small maritime props.
- Story path: water foreground to dock, cave entrance, treasure, and lookout.
- Characters: captain and crew stand at different depth anchors; front faces
  remain visible and side art continues hats, hair, and costume.
- Reject a generic rectangular house, flat ship wall, or long uniform water
  strip.

### Christmas: warm winter cottage

- Current approved pilot: `133 PCS`.
- Hero silhouette: warm brick cottage with chimney and stepped roof mass.
- Secondary mass: one decorated tree, snow platform, gifts, fireplace/door, and
  a few role-specific holiday props.
- Story path: foreground visitor or gingerbread role to gifts, entrance, and
  tree.
- Keep snow white with thin neutral seams; never turn connected snow into one
  blank white slab.
- Reject repeated tree-print filler, a flat wall with gifts in front, or all
  characters lined up on the base edge.

### Halloween: pumpkin manor

- Current approved pilot: `134 PCS`.
- Hero silhouette: tall dark manor with a deep doorway/arch and an asymmetric
  roof or tower rhythm.
- Secondary mass: gate or fence, pumpkins, lanterns, bat/ghost accents, and a
  short foreground path.
- Story path: pumpkin entrance to manor doorway and upper lantern landmark.
- Characters: witch, ghost, and pumpkin role use different expressions and
  depth positions.
- Reject a recolored Christmas cottage, a solid purple rectangle, or repeated
  pumpkins used only as count filler.

### Firefighting: rescue station

- Current approved pilot: `142 PCS`.
- Hero silhouette: alarm tower plus open garage bay; the garage opening must
  remain visible without the title.
- Secondary mass: turning rescue lane, fire engine, ladder/hose/hydrant, and a
  localized emergency corner.
- Story path: lane to vehicle, garage, and fire-response point.
- Characters: chief and firefighter stand near their operational anchors with
  distinct helmets, expressions, and uniforms.
- Reject a closed red wall, construction-site recolor, or repeated flame blocks
  without a readable rescue action.

### Police: garage courtyard

- Current approved pilot: `151 PCS`.
- Hero silhouette: blue precinct mass with an open vehicle courtyard and
  readable garage/entrance opening.
- Secondary mass: turning road, patrol vehicles, traffic lights, barriers, and
  one contrasting brick or white side mass.
- Story path: road entrance through checkpoint/courtyard to garage.
- Characters: officer, commander, and suspect/visitor occupy different story
  positions. Never repeat one generic police face.
- Reject a flat blue wall, a straight row of vehicles, or the same checkpoint
  topology used by every police SKU.

## Batch diversity gate

For a six-theme batch, all six structural signatures must remain different in
plain gray. At least four archetypes are required, and no template may appear
more than twice. Compare footprint, primary mass, major void, height rhythm,
and foreground path; neighboring outputs must differ on at least three.

## Catalog and packaging gate

- The main scene must remain fully inside its safe rectangle and at least
  `12px` away from the color box, right information block, parts panel, and
  parameter table before final upscaling.
- The color-box scene must clear title, PCS/size, age, and STEM regions by its
  alpha mask. Move the scene within the allowed region before shrinking it.
- Detail quantities must sum exactly to PCS and use the same one-cube render as
  the scene material.
- Run `scripts/calculate_airplane_carton.py` for every SKU. Current locked
  weights are `2.5g` per cube and `70g` per color box; carton quantity is the
  largest valid multiple of `12`, declared gross weight is at most `25kg`, and
  gross weight is declared net plus `1.5kg`.

Current tested local implementations:

- Engineering, pirate, firefighting, police:
  `C:/Users/Administrator/Documents/Codex/2026-07-05/new-chat/work/pirate_engineer_particle_first_v1/`
- Christmas and Halloween:
  `C:/Users/Administrator/Documents/Codex/2026-07-05/new-chat/work/holiday_particle_first_v1/`
- Six-SKU catalog delivery:
  `C:/Users/Administrator/Documents/Codex/2026-07-05/new-chat/work/generate_final_six_theme_catalogs.py`
