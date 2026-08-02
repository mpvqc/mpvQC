# Group a feature into a feature package

The layer packages sort code by what a class is, not by what it is about. Everything appearance means — the color
scheme types, the resolution rule, the palette lookup, the settings-backed preference, the dialog's derivation — sat
spread across four of them, and the only thing holding it together was that the names all started with color or
palette. Reading the area meant opening every layer and picking the appearance files out of it; changing the area meant
touching every layer for one idea.

Appearance now lives in a feature package. `domain.py` at its root holds the types and the pure rules, and role
directories under it hold what the area owns: the color scheme service with its style-hints seam, the palette catalog
with its palette family. Tests mirror the same shape. The layer packages keep everything no feature package has
claimed, and no re-export shim stays behind — call sites name the new home.

The skeleton is the template for the next one:

```text
mpvqc/<feature>/
├── __init__.py      # empty
├── domain.py        # types and pure rules
├── injections.py    # bindings(binder)
├── services/
├── models/          # as the feature claims them
└── viewmodels/
```

Role directories are plural, matching the vocabulary the repo already uses. They exist because one concept recurs
across roles: the color scheme is a domain type, a service, and a model, and without the directory each would grow a
role suffix to stay distinct. The directory carries the role, so the concept keeps its name everywhere.

Package `__init__` files stay empty. Imports then name the module they mean, so a reader sees which role they are
pulling from — and, load-bearing, an empty init is what keeps the horizontal seams importable from inside a feature
package. The settings service reads the appearance domain, and the color scheme service reads the settings service; if
importing a feature package pulled its own services in, that would be a cycle.

A feature package brings its own bindings. Its `bindings(binder)` is called by the composition root, first, and how a
service is assembled — the style-hints adapter wrapping Qt's, in particular — is knowledge that stops at the package
boundary. The root keeps deciding which packages participate. Bindings must stay lazy: injection is configured before
`QGuiApplication` exists, so anything reaching for Qt's application-level state has to be constructed on demand.

QML-facing classes register by decorator, when their module is imported, and startup does those imports explicitly.
Because a feature package's inits are empty, importing the package registers nothing — the startup import has to name
the modules that hold the classes.

## What stays horizontal

Settings and resources stay in the layer packages, and the palette data file stays where the resource bundle wants it.
Both are shared boundary services: several areas read through them, and appearance is one caller among many. A feature
package owns what its area means, not the I/O under it — it reads through those seams rather than absorbing them.

## Consequences

- One area is one directory. Reading appearance means reading one tree, and the tree names its own dependencies at the
  places it imports across.
- Feature packages and layer packages coexist. There is no migration to finish: a layer package is where code lives
  until a feature claims it.
- A feature's wiring is reviewable on its own, and adding one touches the root twice: an import and a call.
- Import direction is worth watching. One feature package reaching into another's internals is the failure mode this
  shape makes both easy to write and easy to see.

## Dropped alternatives

- **Full hexagonal architecture** — ports for every service, adapters behind all of them, a use-case layer over the
  domain. The part that pays is the domain-typed seam at the OS boundary, and that part is already here: the style
  hints protocol takes and returns domain types, so Qt's color scheme enum meets the domain's in exactly one adapter,
  and the resolution rule is testable without Qt. Putting ports in front of the stable in-process services buys
  indirection against a change that isn't coming, and a use-case layer over a desktop app whose use cases are view
  model slots is a layer of pass-throughs. The style hints seam is the in-repo template to copy if a genuinely
  volatile boundary shows up.
- **A `common/` or `shared/` package** for what stays horizontal: renames the layer packages without changing what is
  in them, and invites everything to drift in.
- **Keeping a re-export shim** in the layer package so call sites need not move: two spellings for one class, and the
  old one is the one that looks correct in a review.
