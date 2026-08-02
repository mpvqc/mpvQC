# Let a feature package own its settings keys

`SettingsService` held every key the app stores, appearance's among them. Those keys carry domain types, so the shared
service imported twelve names from the appearance domain: the color scheme types, the accent color preference, the
parse and format pair, the aggregate it published. The arrow ran backwards through the seam the feature package exists
to draw — the shared layer knew what appearance means — and only an empty package root kept it from being an import
cycle.

A feature package owns the settings its area means. It holds the key names, the defaults, the domain-typed accessors
and the signal that publishes them, and it reads the file through the shared boundary service that locates and opens
it. What no feature package has claimed stays in `SettingsService`, the same way the layer packages hold every class no
feature has claimed. Both services write through one shared file handle, so there is one open file and no ordering
question between them.

Ownership follows meaning, not ini section. Appearance happens to be one whole section, so the two rules agree here,
and they will not agree next time: `Common/commentTypes` belongs to comments while `Common/language` does not. A
section rule would owe every later feature a key rename, and renaming a stored key means another round of the medicine
[ADR 0008](0008-store-color-scheme-preference-under-fresh-keys.md) prescribed — two meanings behind one name across a
rollback, or migration code that ships forever.

## Consequences

- Nothing shared names what a feature means. A feature reads the settings file service; the settings file service
  knows about files.
- One area's storage reads as one file: its keys, its defaults, its accessors, and the one value it publishes.
- A key two areas mean is shared by that test, and stays in `SettingsService`. Ownership is a claim about meaning, so a
  contested key is evidence there is no owner.
- The rule scales the way the package split does: a feature claims its keys when it is carved out, and until then they
  sit in the shared service.

## Dropped alternatives

- **Settings exports plain strings and appearance parses them at its edge** — keeps the domain types out of the shared
  layer but not the keys: settings would still name `Appearance/accentColor/light`, a key composed per color scheme,
  and a plain string cannot say what an absent key says, which is that the user never confirmed a pick. Three string
  settings also cannot produce the single deduped appearance preference
  [ADR 0007](0007-store-accent-colors-per-color-scheme.md) asks consumers to fold.
- **A settings store port in front of the file** — an interface the feature depends on and the shared layer implements.
  ADR 0009 already dropped ports in front of stable in-process services for the indirection they cost, and tests build
  a real `QSettings` over a temporary ini file, so there is no testability left to buy.
