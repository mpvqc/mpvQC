# Store and resolve appearance preferences independently of the old theme

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

## Store the new model under fresh keys

The old model stored a theme identifier and one global accent under `Theme/`. The appearance model stores a color
scheme preference and one accent per color scheme under `Appearance/`. The two models do not line up: System has no old
theme equivalent and is the new default. No code reads, writes, deletes, or migrates the old keys.

Configs outlive the release that wrote them, and users roll releases back. Reusing keys would let an old build read a
new value under the old meaning and overwrite it on the next change. Fresh keys keep both models independent. Existing
users reset to System once, while a rollback finds its old settings unchanged. This one visible reset costs less than
permanent, lossy migration code.

## Resolve an unknown system color scheme to light

Following the system still needs an answer when the system reports no preference. Unknown resolves to light. GNOME
uses no preference for its light state because `prefer-light` remains reserved, while Windows and KDE answer light or
dark directly. A session without a settings portal therefore starts and stays light.

## Consequences

- The old theme keys remain inert in the config. Existing users see System and the declared accent defaults once;
  rollback remains safe.
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
- **Migrate the old theme**: the mapping is lossy, deletion breaks rollback, and keeping both groups lets them drift.
- **Keep historic dark for an unknown system answer**: this ignores the light answer GNOME actually reports.
