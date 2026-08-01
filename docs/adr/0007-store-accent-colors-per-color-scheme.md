# Store accent colors per color scheme and publish the appearance

The accent color was one global stored hex that had to exist in every theme — an invariant nothing stated or
enforced, holding only because both shipped themes carry identical seed sets. A future theme with its own accent set
would have broken accent persistence silently. We scope the accent color choice to its theme instead: settings
remember one accent per theme, sparse, and every theme declares its own default accent, checked against its own set
by the color generator before it writes and by a test over the shipped bundle. Today's themes are one per color
scheme, so this is the per-scheme accent storage the planned color scheme preference rework needs anyway.

Because a theme switch changes two things in one observation — the identifier and which stored accent entry is
relevant — settings publish the appearance (theme identifier plus that theme's stored accent) as a single deduped
value, and consumers fold that one payload. This instantiates the snapshot-pattern ADR's revisit clause for
co-changing fields; it is a projection of settings' own stored state, not derivation. An accent write for a theme
that is not current emits nothing.

## Considered options

- **A catalog-wide accent contract** — every theme must realize one shared accent set, checked at load. Formalizes
  the restriction instead of removing it; a Solarized could never ship its own accents.
- **Symbolic accent names** as stored keys: costs a data format change, a settings migration, and names for custom
  seeds, while keeping the shared-set restriction.
- **Reset on theme switch** (no memory): hostile to the user and contradicts the planned per-scheme accents.
- **Interpretive mapping** (nearest color in the new theme): trades a stated restriction for a hidden algorithm, and
  a global interpreted accent collides with per-scheme storage later.
- **Runtime palette generation from a free accent color**: dissolves accent sets entirely, but is a product-level
  change and its own project.

## Consequences

- The legacy global accent value is not migrated: its stored key is abandoned in place and existing users see the
  declared defaults once. Accents chosen from then on no longer bleed across themes.
- A theme may ship any accent set of any size; nothing outside the theme's own data constrains it.
- The appearance dialog's cancel must restore the full state its preview can dirty: the theme identifier plus every
  theme's accent entry, captured as a baseline when the dialog opens.
