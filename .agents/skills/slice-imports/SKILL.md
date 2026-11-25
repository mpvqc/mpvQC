---
name: slice-imports
description: The import rules of the feature slices. Use when creating or editing Python under a feature package (mpvqc/appdata/, mpvqc/appearance/, mpvqc/comments/, mpvqc/exporting/, mpvqc/i18n/, mpvqc/importing/, mpvqc/player/, mpvqc/shell/, mpvqc/window/) or its test tree, when moving code between roles, and when adding a new feature slice.
---

# Slice imports

`test/test_import_rules.py` checks the imports under every `mpvqc/<slice>/`, and its failure message names the rule
broken and the fix. Before adding an import that crosses roles or slices, read the checker's `LATTICE` table.
Production files owe the whole lattice; a slice's tests under `test/<slice>/` owe the role-root rule alone, so a test
may reach any role as long as it goes through that role's root.

## Beyond the lattice

- **Role root**: each role's `__init__` is its public API. Import names from the role root (`mpvqc.<slice>.<role>`),
  in production and in tests alike. A name worth reaching for is worth exporting from the root.
- **Held roots**: a package inside a role that is imported as `mpvqc.<slice>.<role>.<package>`, and that the role
  root above it re-exports nothing from. A package earns the status when re-exporting it would fail or would swamp the
  role, as re-exporting the Windows platform package would import Win32 bindings everywhere. It joins by being listed
  in the checker's `HELD_ROOTS` table.
- **Top level**: a helper under `mpvqc/` is open to the roles the checker's `HELPERS` table lists for it. A top-level
  module without a row there needs one before a slice uses it, following the placement rule in `writing-services`.
- **Enums**: every QML-registered enum lives in the `enums` role of the slice whose area it means.
- **Composition seams**: `wiring.py` imports first-party and Qt inside its functions only, and in production the
  composition roots (`mpvqc/injections.py`, `mpvqc/startup.py`) alone import a slice root. `test/conftest.py` and
  `testqml/` are composition roots too, so they import slice roots and the checker leaves them alone.
- **Logic**: a slice's logic lives in its services role, and `writing-services` decides the shape it takes there.

## Adding a slice

A slice joins the rules by being listed in the checker's `SLICES` table, and listing it arms the scans against the
whole roster at once. Build the directories first: a `wiring.py`, which the wiring check reads without asking whether
it exists; a role `__init__` that imports something; and a test under `test/<slice>/`. Each scan fails when it reads
no imports under the slice, so an empty or misplaced tree is a red, not a pass.

## Done when

`just test-python test/test_import_rules.py` passes. A red here is a design signal, not an obstacle: the missing
concept belongs in one slice's public service, or in the shared vocabulary `mpvqc.shared`. Follow the
message's fix.
