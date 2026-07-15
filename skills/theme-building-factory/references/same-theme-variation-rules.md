# Same-Theme Edition Rules

Use these rules whenever a theme has already been generated, even when the user
asks for the same PCS or the same broad subject again.

## Core distinction

- Across separate SKUs: do not reuse the previous particle library.
- Inside one SKU: the main scene, parts-detail icons, and color-box scene must
  use the exact same newly created library and tone chain.

Previous editions are comparison evidence only. Never register their face files
as candidate materials for a new edition.

## New-edition workflow

1. Normalize a stable `theme_key`, then search archived manifests and delivered
   metadata for all prior editions of that theme.
2. Create a unique `particle_library_id`, for example
   `police-garage-20260715-v02`. Never overwrite an earlier library folder.
3. Choose a different structural archetype and change at least three of:
   footprint, primary mass, major void, height rhythm, foreground path.
4. Draw a complete new set of visible particle faces. Redraw structural
   materials, functional props, theme motifs, characters, expressions,
   costumes, and side/top continuations; do not recolor or crop an old face.
5. Save a manifest containing the library ID and a SHA-256 hash for every face
   image as `particle_face_hashes`.
6. Validate the current metadata together with all archived editions of the same
   theme using `scripts/validate_scene_batch_diversity.py`.
7. Reject the edition when any exact face hash is shared with a prior edition,
   a library ID repeats, or the structure fails the three-axis difference gate.

## What may be reused

- identical 20mm cube mesh and integer-grid rules;
- UV orientation and face naming convention;
- renderer, camera family, lighting calibration, and tone-matching process;
- catalog layout, color-box shell, text styles, and packaging formulas;
- generic code helpers that do not determine the visible scene design.

## What must be new

- every visible particle face image and its manifest;
- hero silhouette and topology for the new edition;
- theme-specific props and decorative motifs;
- featured character faces, expressions, costumes, and story positions;
- palette hierarchy and visual rhythm, while retaining production-safe color.

Use prior contact sheets as a negative reference: the new edition should be
recognizably the same theme but visibly a different product at first glance.
