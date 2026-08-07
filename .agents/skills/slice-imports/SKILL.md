---
name: slice-imports
description: The import rules of the feature slices. Use when creating or editing Python under a feature package (mpvqc/appearance/, mpvqc/importing/) or its test tree, when moving code between roles, and when adding a new feature slice.
---

# Slice imports

A feature slice imports by the lattice below. `test/test_import_rules.py` enforces every rule on this page: its
failure message names the rule broken and the fix, and a new slice joins the rules by being listed in its `SLICES`
table.

## The lattice

An import is allowed when its row lists the target's role. Every role imports freely within its own directory.

Same slice:

| From          | May import (same slice)                     |
| ------------- | ------------------------------------------- |
| `domain`      | `domain` only                               |
| `enums`       | `domain`                                    |
| `models`      | `domain`, `enums`, `services`               |
| `services`    | `services`, `domain`                        |
| `viewmodels`  | everything                                  |

Another slice, and the shared layer (`mpvqc/services/`):

| From          | May import (another slice)                  |
| ------------- | ------------------------------------------- |
| `domain`      | `domain`                                    |
| `enums`       | `domain`                                    |
| `models`      | `domain`, `enums`                           |
| `services`    | `services`, `domain`                        |
| `viewmodels`  | `services`, `domain`, `enums`               |

A foreign slice's `viewmodels` and `models` are off-limits to everyone: presentation never crosses a slice.

## Beyond the tables

- **Role root**: each role's `__init__` is its public API. Import names from the role root (`mpvqc.services`,
  `mpvqc.<slice>.<role>`), in production and in tests alike. A name worth reaching for is worth exporting from the
  root.
- **Domain floor**: a domain imports the standard library and other domains, `mpvqc.datamodels` included, and nothing
  else. `TYPE_CHECKING` blocks count the same as runtime imports.
- **Top level**: `mpvqc.datamodels` is shared domain. `mpvqc.jobs` is a helper for services and view models. Any
  other top-level module needs a row in the checker's tables before a slice uses it.
- **Composition seams**: `wiring.py` imports first-party and Qt inside its functions only, and the composition roots
  (`mpvqc/injections.py`, `mpvqc/startup.py`) alone import a slice root. `testqml/` stands outside all of these
  rules.

## Done when

`just test-python test/test_import_rules.py` passes. A red here is a design signal, not an obstacle: the missing
concept belongs in one slice's public service, or in the shared layer (ADR 0012). Follow the message's fix.
