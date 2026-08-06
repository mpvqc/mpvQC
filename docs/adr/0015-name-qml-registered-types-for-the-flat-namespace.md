# Name QML-registered types for the flat namespace

Two flat spaces sit behind every QML-registered class, and neither shows at the call site. Every registered type in
the app lands in one QML module, so the namespace QML sees is flat no matter how the Python side is packaged. And the
type-info generator writes one file per source module into one flat directory, named after the module's file name, so
that space is flat too. A package that shortens a name for its own tidiness still compiles and runs, because elements
register at import time; only the static picture goes wrong. A file-name collision during the importing carve-out
silently dropped a view model's type info, and the QML linter reported the type as not found, pointing nowhere near
the cause.

So one question decides how free a name is: can QML name the type?

A class QML can name carries `Mpvqc` and its full qualification — the area, what it is, and its role — because the
flat namespace is the only context the name will ever have. The Python name and the QML name are one name. The prefix
means exactly that QML can name the type, so nothing unregistered wears it. Modules holding registered classes never
share a file name. That check belongs in the test suite, because the build driver stays replaceable by upstream and
cannot carry it; nothing runs it yet, and writing it is follow-up work. Everything QML cannot name is free: it names
itself for its package, and package, role directory, and module carry the context a flat namespace cannot.

## Consequences

- A registered view model reads long inside its own package. The wizard's session step view model repeats what its
  package and module already say, and that length is the price of a name that must stand alone in the flat namespace.
- Whether a name may drop its area words is decidable at a glance: registered, never; unregistered, free.
- The prefix is load-bearing. A registered type without it is a defect, not a style choice, and an unregistered class
  wearing it claims a registration it does not have.
- A module gaining its first registered class inherits both constraints at once: its class name enters the flat
  namespace, and its file name enters the flat type-info directory.

## Dropped alternatives

- **Shorten wherever the short name is unique today** — uniqueness by luck fails silently later. The next slice mints
  the same name, one type-info file overwrites the other, and the linter chases a ghost far from the cause. A rule
  that prevents the collision class beats a check that catches one instance.
- **Split the Python name from the QML name** — the toolkit can register a short Python class under a longer QML name,
  but then one thing answers to two names and a search for the QML name never finds the class. The redundancy a split
  saves is smaller than the traceability it costs.
- **Prefix registered module file names deterministically** — an area prefix on every registered module's file name
  would make uniqueness structural, but it buys with a mass rename across every slice what a test can simply assert.
