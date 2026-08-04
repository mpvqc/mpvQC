# Store accent colors per color scheme

An accent color is chosen against a palette. The user picks it while looking at light surfaces or dark ones, and it is
that pairing they are approving. One stored accent for the whole app breaks the pairing the moment the color scheme
changes, and under the follow-the-system preference the scheme changes on its own, at dusk or when the desktop says so.
So the accent color preference is stored per color scheme.

An accent the user never picked is not stored at all. The palette family's own declared default renders instead, so a
user who never opens the dialog keeps following whatever ships, release after release.

Settings publish all of it as one value: the color scheme preference and both schemes' accent color preferences
together. Its consumers read across those fields rather than one at a time, since the palette needs the accent
belonging to whichever scheme renders, and the dialog paints every scheme's row with the accent that scheme would show.
A signal per key would make each of them rebuild a set settings already holds whole.

## Consequences

- The old global accent color key is not migrated: it is abandoned in place, and existing users see the declared
  default accent colors once. Accent colors chosen from then on no longer bleed across color schemes.
- A palette family may ship any accent colors, in any number. A stored accent color the family does not offer resolves
  to that family's default, so shrinking or replacing a family's accent set costs nothing.
- Following the system names no single color scheme to key an accent color preference to, so the appearance dialog
  offers no accent colors while that preference is selected.
- The appearance dialog's cancel restores everything its live preview can dirty. The dialog captures the appearance
  preference when it opens and writes that baseline back wholesale on reject, in one restore.

## Dropped alternatives

- **A catalog-wide accent contract**, every palette family offering one shared set of accent colors: formalizes a
  restriction instead of removing it, and a Solarized family could never ship its own accent colors.
- **Symbolic accent names** as stored keys: costs a data format change, a settings migration, and names for custom
  accent colors, while keeping the shared-set restriction.
- **Reset when the color scheme changes**, keeping no accent memory at all: hostile to the user, and it contradicts
  per-scheme accent colors.
- **Interpretive mapping**, resolving a stored accent color to the nearest one in the new palette family: trades a
  stated restriction for a hidden algorithm, and the result is still one global accent color.
- **Runtime palette generation from a free accent color**: dissolves the fixed accent colors entirely, but it is a
  product-level change and its own project.
- **A signal per stored key** instead of one payload: every consumer reads across the keys, so each has to hold the
  other keys' last values and reassemble the set the payload already is.
