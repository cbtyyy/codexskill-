# Character, Story, and Theme Template Rules

Use these rules whenever a magnetic-cube scene contains people, animals,
vehicles, occupations, or a buyer-visible story.

## 1. Design the theme before counting cubes

- Define one hero silhouette that identifies the theme with the title hidden.
- Define a theme-specific circulation path: road, dock, deck, courtyard,
  doorway, bridge, track, river, or work zone.
- Define at least two semantic support elements that explain the hero object.
- Reuse only cube primitives and small generic support helpers. Never reuse a
  complete wall, stair, platform, tower, or building skeleton across themes.
- Reject a template when recoloring it would make it usable as another theme.

Examples:

- Police: station/gate, road or checkpoint, traffic-control prop, patrol role.
- Pirate: hull/deck, mast or sail, shore/dock/treasure path, captain and crew.
- Engineering: crane or machine, active work zone, materials path, operator.

## 2. Compose a readable micro-world

Use three depth zones rather than an even pile of blocks:

- Foreground: entry path, small prop, antagonist/visitor, or story trigger.
- Midground: the interaction zone and most important character action.
- Background: the hero silhouette and one controlled height accent.

Keep one dominant mass, one secondary mass, and a few accents. Avoid equal
heights, mirrored filler, repeated stair-step walls, and broad empty platforms.
The visual rhythm must include solid masses, openings, vertical accents, and
short low elements.

## 3. Character identity gate

Before modeling, write a role card for every character:

- role and story function;
- emotion;
- eye shape and direction;
- eyebrow shape;
- mouth shape;
- hair or headgear;
- costume palette and identifying prop.

No two featured characters in one scene may share the same combination of eyes,
brows, and mouth. Do not use a generic dot-eye/curve-mouth face repeatedly.
Facial features must be large enough to read in the final scene, centered on the
front face, and surrounded by sufficient skin-color clearance.

## 4. Six-face character continuity

- Front: complete buyer-facing identity and expression.
- Left/right: ear, cheek contour, hair or hat continuation, sleeve or side seam.
- Back: back of hair/headgear and rear costume details.
- Top: crown, cap, hair part, bandana, or helmet structure.
- Bottom: neutral underside or shoe/sole logic.

Never duplicate the front face on a side. Do not add a gray side overlay. Side
ink must stay close to the front-face color under the shared renderer.

## 5. Story-led placement

- Place authority roles at the entrance, command point, or hero structure.
- Place operators next to the equipment they use.
- Place antagonists, visitors, treasure hunters, or recipients at the story
  trigger in the foreground or checkpoint.
- Stagger characters across depth and height. Do not line all figures along the
  same front edge.
- Rotate or position the figure so the production camera sees the complete front
  artwork. A visible side may support the pose but cannot replace the front.
- Do not let props, badges, labels, or packaging typography cover a character.

## 6. Texture hierarchy

- Use natural textures for structural material, clean graphics for functional
  objects, and illustrated prints for theme anchors and characters.
- Favor large, clean, readable motifs over dense micro-pattern noise.
- Structural filler must remain subordinate to windows, doors, signs, vehicle
  faces, treasure, tools, foliage, and role-specific character prints.
- Keep each theme's palette coherent. Use saturation contrast and warm/cool
  contrast to separate the hero object from supporting materials.

## 7. PCS integrity

- Build the best scene first, within the approved range, then report the actual
  modeled count.
- Small, medium, and large variants must be genuine geometry variants with
  different counts, not one shared render with several labels.
- Increasing PCS must add story depth, access paths, useful props, or a stronger
  hero silhouette. Never add repeated decoration as filler.

## 8. Acceptance tests

Reject the scene unless all are true:

1. With the title hidden, a buyer can name the theme and identify the roles.
2. In grayscale silhouette, the hero object remains recognizable.
3. Recoloring cannot turn the model into another theme's template.
4. Every face is centered, readable, and visible from the production camera.
5. Side/top/back character art is continuous and not a duplicated front.
6. Characters occupy story-driven positions rather than a fixed lineup.
7. The scene has distinct foreground, midground, and background layers.
8. The displayed PCS equals the actual modeled count.

## 9. Multi-archetype generation and rejection

For every theme family intended for reuse, maintain at least three different
topologies. For example, police may use a checkpoint station, an intersection
precinct, and an open garage courtyard; pirate may use a docked ship, a skull
cave dock, and a lookout-tower cove. These are topology changes, not recolors.

Generate low-detail gray candidates before final particle art and record:

- footprint and top-view occupancy;
- dominant mass and secondary mass;
- major opening or negative space;
- foreground, midground, and background depth layers;
- height levels and longest uninterrupted run;
- circulation/story path and character anchors.

Reject a candidate when any is true:

- top-view occupancy similarity to another candidate is above `0.70`;
- fewer than three structural properties differ from the nearest candidate;
- a long wall, strip, or platform becomes the scene's dominant silhouette;
- no door, arch, bridge gap, garage opening, road turn, dock gap, or comparable
  negative space is readable;
- character anchors repeat the same front-edge lineup;
- removing decals makes the theme unrecognizable.

Only approved geometry receives the locked six-face particle art. PCS may vary
from 80 to 200, but the chosen count must improve the silhouette and story rather
than pad a weak template.
