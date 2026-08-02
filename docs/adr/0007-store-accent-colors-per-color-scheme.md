# Store accent colors per color scheme and publish the appearance

The accent color was one global stored hex that had to exist in every palette family — an invariant nothing stated or
enforced, holding only because both shipped families are built from identical accent colors. A future family with its
own accent colors would have broken accent persistence silently. We scope the accent color choice to its palette
family instead: settings remember one accent color per color scheme, sparse, and every family declares its own default
accent color, checked against its own palettes by the color generator before it writes and by a test over the shipped
bundle. Palette families are one per color scheme, so this is the per-scheme accent storage the color scheme
preference rework needs anyway.

Because a color scheme switch changes two things in one observation — which scheme renders and which stored accent
color is relevant — settings publish the appearance as a single deduped value, and consumers fold that one payload.
This instantiates the snapshot-pattern ADR's revisit clause for co-changing fields; it is a projection of settings' own
stored state, not derivation. The payload carries the color scheme preference and both schemes' accent color
preferences, so any accent color write publishes, current scheme or not.

## Considered options

- **A catalog-wide accent contract** — every palette family must offer one shared set of accent colors, checked at
  load. Formalizes the restriction instead of removing it; a Solarized could never ship its own accent colors.
- **Symbolic accent names** as stored keys: costs a data format change, a settings migration, and names for custom
  accent colors, while keeping the shared-set restriction.
- **Reset when the color scheme changes** (no memory): hostile to the user and contradicts per-scheme accent colors.
- **Interpretive mapping** (nearest color in the new palette family): trades a stated restriction for a hidden
  algorithm, and a global interpreted accent color collides with per-scheme storage later.
- **Runtime palette generation from a free accent color**: dissolves the fixed accent colors entirely, but is a
  product-level change and its own project.

## Consequences

- The legacy global accent value is not migrated: its stored key is abandoned in place and existing users see the
  declared defaults once. Accent colors chosen from then on no longer bleed across color schemes.
- A palette family may ship any accent colors, in any number; nothing outside the family's own data constrains it.
- The appearance dialog's cancel must restore the full state its preview can dirty: the color scheme preference plus
  every color scheme's accent color preference, captured as a baseline when the dialog opens.
