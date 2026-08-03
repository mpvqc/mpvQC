# Let a feature package own its settings keys

`SettingsService` held every key the app stores. Keys carry domain types, so it had to import them from whichever area
meant them, and the arrow ran backwards through the seam a feature package exists to draw: the shared layer knew what a
feature means. For the first feature to move out that was eleven names, and only an empty package root kept it from
being an import cycle.

A feature package owns the settings its area means. It holds the key names, the defaults, the domain-typed accessors
and the signal that publishes them, and it reads the file through the shared boundary service that locates and opens
it. What no feature package has claimed stays in `SettingsService`, the same way the layer packages hold every class no
feature has claimed. Both services write through one shared file handle, so there is one open file and no ordering
question between them.

Ownership follows meaning, not ini section. Appearance happens to be one whole section, so the two rules agree there,
and they will not agree next time: `Common/commentTypes` belongs to comments while `Common/language` does not. A
section rule would owe every later feature a key rename, and a stored key does not rename cheaply: an older build still
reads the old name, so the rename buys either two meanings under one name across a rollback, or migration code that
ships forever.

## Consequences

- Nothing shared names what a feature means. A feature reads the settings file service; the settings file service
  knows about files.
- One area's storage reads as one file: its keys, its defaults, its accessors, and the one value it publishes.
- A key two areas mean is shared by that test, and stays in `SettingsService`. Ownership is a claim about meaning, so a
  contested key is evidence there is no owner.
- A second feature inherits the open file and nothing else. The shared service's key descriptor (one key, one default,
  one stored type, one change signal) is private to it, so the next feature writes its own accessors and its own
  signal. The first one had to anyway: it composes a key per case, reads an absent key as a domain state rather than a
  missing value, and publishes one aggregate in place of a signal per key.
