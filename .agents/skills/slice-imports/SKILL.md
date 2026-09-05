---
name: slice-imports
description: The import rules of the feature slices. Use when creating or editing Python under a feature package (mpvqc/appearance/, mpvqc/comments/, mpvqc/exporting/, mpvqc/i18n/, mpvqc/importing/, mpvqc/player/, mpvqc/shell/, mpvqc/window/) or its test tree, when moving code between roles, and when adding a new feature slice.
---

# Slice imports

A feature slice imports by the lattice below. `test/test_import_rules.py` checks it over `mpvqc/<slice>/`, and its
failure message names the rule broken and the fix. Production files owe the whole lattice; a slice's tests under
`test/<slice>/` owe the role-root rule alone, so a test may reach any role as long as it goes through that role's
root.

## The lattice

An import is allowed when its row lists the target's role. Every role imports freely within its own directory, and
every role may import `mpvqc.shared`, the shared pure vocabulary.

Same slice:

| From          | May import (same slice)                     |
| ------------- | ------------------------------------------- |
| `enums`       | `shared`                                    |
| `models`      | `enums`, `services`, `shared`               |
| `services`    | `services`, `shared`                        |
| `viewmodels`  | `models`, `services`, `enums`, `shared`     |
| `views`       | `models`, `services`, `enums`, `shared`     |

Another slice, and the shared layer (`mpvqc/services/`):

| From          | May import (another slice)                  |
| ------------- | ------------------------------------------- |
| `enums`       | `shared`                                    |
| `models`      | `enums`, `shared`                           |
| `services`    | `services`, `shared`                        |
| `viewmodels`  | `services`, `enums`, `shared`               |
| `views`       | `services`, `enums`, `shared`               |

A foreign slice's `viewmodels`, `views` and `models` are off-limits to everyone: presentation never crosses a slice.

`views` holds a class a slice writes in Python and QML instantiates as part of the scene, the video output mpv draws
into being the case that asks for the role. `enums` holds the QML-registered enums the slice's area means (ADR 0013);
the shared enum package is gone, so every QML enum has a slice.

## No domain role

The lattice has no `domain` row: no slice carries one, and none adds one. A slice's logic lives in its services role,
and `writing-services` decides the shape it takes there (ADR 0019).

## Beyond the tables

- **Role root**: each role's `__init__` is its public API. Import names from the role root (`mpvqc.services`,
  `mpvqc.<slice>.<role>`), in production and in tests alike. A name worth reaching for is worth exporting from the
  root.
- **Held roots**: a package inside a role that the role holds as a root of its own instead of re-exporting. An import
  names `mpvqc.<slice>.<role>.<package>` and takes it from there, and the role root above it re-exports none of its
  names. A package earns the status when re-exporting it would fail or would swamp the role: the `linux` and `windows`
  platform packages, because the role root holds unconditional re-exports and re-exporting the Windows package would
  import Win32 bindings everywhere else; the window slice's `windows_decisions` package, because its Win32
  message-routing and frame-geometry vocabulary outnumbers the rest of the role and only the Windows package reads it.
  A new held root joins by being listed in the checker's `HELD_ROOTS` table.
- **Top level**: a helper under `mpvqc/` is open to a role set of its own, listed in the checker's `HELPERS` table.
  `mpvqc.jobs` is open to services and view models, the roles that run work. `mpvqc.build` is open to every role,
  because build info is read-only facts and the helper rule was written for the job runner. Any other top-level
  module needs a row there before a slice uses it.
- **Composition seams**: `wiring.py` imports first-party and Qt inside its functions only, and in production the
  composition roots (`mpvqc/injections.py`, `mpvqc/startup.py`) alone import a slice root. `test/conftest.py` and
  `testqml/` are composition roots too, so they import slice roots and the checker leaves them alone.

## Adding a slice

A slice joins the rules by being listed in the checker's `SLICES` table, and listing it arms the scans against the
whole roster at once. Build the directories first: a `wiring.py`, which the wiring check reads without asking whether
it exists; a role `__init__` that imports something; and a test under `test/<slice>/`. Each scan fails when it reads
no imports under the slice, so an empty or misplaced tree is a red, not a pass.

## Done when

`just test-python test/test_import_rules.py` passes. A red here is a design signal, not an obstacle: the missing
concept belongs in one slice's public service (ADR 0012), or in the shared vocabulary (ADR 0019). Follow the
message's fix.
