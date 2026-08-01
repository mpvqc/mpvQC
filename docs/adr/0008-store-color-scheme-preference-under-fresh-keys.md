# Store the color scheme preference under fresh keys

The old model stored a theme identifier and one accent color per theme identifier under `Theme/`. The new model
stores a color scheme preference and one accent color per color scheme under `Appearance/`. The two do not line up:
the preference has a value no theme identifier can express, System, and it is the new default. The new model gets a
fresh group, and nothing on the new path reads, writes, or deletes the old one. There is no migration. The theme
entity keeps using its own keys for as long as it survives the rework; once it is deleted, `Theme/` is untouched by
any code path.

Flatpak configs outlive the app that wrote them, and users roll releases back. Reusing key names would put two
meanings behind one key: a rolled-back build would read `system` where it expects a theme identifier, fall back to
its default, and write a theme identifier back over the preference on the next change. Fresh keys keep both models
whole and independent, so a rollback finds its own settings exactly as it left them. Windows builds carry no
persistent config at all, which removes the other constituency a migration would have served.

The price is one reset: every existing user lands on System once and starts with no stored accent per color scheme.
That is acceptable because System is what most users want from an app that can follow the desktop, and because the
alternative is migration code that must map a dead entity onto a live one, forever, for a one-time gain.

## Considered options

- **Migrate on first run** — read `Theme/`, write `Appearance/`, delete `Theme/`. Guts the config of any user who
  rolls back, and the code has to ship in every release from now on to catch the last stragglers.
- **Migrate but keep the old keys** — rollback-safe on the first pass, but the two groups then drift with no way for
  either version to tell which is current. Also lossy in the direction that matters: it would read
  `material-you-dark` as an explicit Dark preference and lock users out of the System default they are most likely
  to want.
- **Reuse the `Theme/` group with new key names** — same drift, plus a settings group named after an entity this
  rework deletes.
- **Reuse the exact old keys with new values** — the case above: an old build silently misreads `system` and writes
  its own vocabulary back over it.

## Consequences

- Every existing user resets to System once, with both schemes' accents empty; the declared defaults render until
  they choose again.
- A rollback finds the `Theme/` keys byte-identical, so the previous version keeps working.
- `Theme/` stays in user configs once the theme entity is gone: inert data that nothing reads and nothing cleans up.
- No migration code ships, so no migration bug can. The cost of the decision is paid once, by users, visibly, rather
  than repeatedly, by the codebase, invisibly.
