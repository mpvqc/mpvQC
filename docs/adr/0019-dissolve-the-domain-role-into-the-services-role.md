# Dissolve the domain role into the services role

Every slice carried a mandatory domain: the area's pure rules, walled off by the lattice from Qt, from injection, and
from the other roles. The wall was there to buy testability, and in one place it did: the import planner's
combinatorics run as table-driven tests over frozen dataclasses, with no toolkit anywhere. But the wall taxed every
slice whether or not it had such a core. The export renderers took a time formatter as a handed-in callable because
the lattice barred the domain from a function that is itself pure standard library; the renderer's pure test
re-implemented that formatter to stay inside the wall, and a contract test existed only to re-couple what the first
test had decoupled. Thin domains were half vocabulary, and services forwarded to them one hop deep.

What the wall protected turns out not to need one. Frozen inputs, pure functions, no shared mutable state: those
properties belong to the code, not to the directory holding it. They are what make a body handed to the serial job
runner race-free, and they survive any move. So the domain role is dissolved. The services role is a slice's one home
for logic, under one admission rule: a class bound in the inject container where there is state, Qt lifecycle, or a
substitution seam worth re-binding; a plain module-level function over frozen dataclasses where the logic is pure.
Nothing is injected merely for uniformity. Vocabulary that several areas mean lives in the shared vocabulary module at
the top of the package tree, and every role may import it. Subsecond time formatting sits there now, beside the
comment type, so pure code reaches shared pure code by import instead of by parameter.

The new shape has no mechanical purity floor. We considered one and dropped it: a pure module's own Qt-free tests are
the guard, and a lapse breaks that one module, nothing more. The import checker still enforces the lattice below.

## The lattice, amended

This table replaces the one in ADR 0012. The reasoning there stands: calls not events, and presentation never crosses
a slice. Every role also imports freely within its own directory.

| From         | Same slice                     | Another slice, and the shared layer |
| ------------ | ------------------------------ | ----------------------------------- |
| `enums`      | shared                         | shared                              |
| `models`     | `enums`, `services`, shared    | `enums`, shared                     |
| `services`   | `services`, shared             | `services`, shared                  |
| `viewmodels` | `models`, `services`, `enums`, shared | `services`, `enums`, shared  |
| `views`      | `models`, `services`, `enums`, shared | `services`, `enums`, shared  |

A foreign slice's `viewmodels`, `views` and `models` stay off-limits to everyone. The `views` role holds a class a
slice writes in Python and QML instantiates as part of the scene; the video output mpv draws into is the case that
asks for it.

## Transition

The transition is done. Exporting piloted the shape, appearance followed, and importing was the last slice to move
its domain into its services role. The checker's domain rows and the old floor (standard library, other domains, the
shared vocabulary module) went with the last domain module. No slice carries a domain, and a new one never adds it.

## What stands

- ADR 0012: cross-slice communication by calls into public services, facts as published state with a change signal,
  ports the exception.
- ADR 0013's boundary shape: QML enums stay a role of their own, and pin-or-translate stays the rule at the QML
  boundary. Its floor, "a domain imports no Qt", dissolves with the role.
- ADR 0009's role directories and role-root exports, and the wiring attachment of ADR 0014. Only the
  domain-at-the-package-root shape is superseded.

## Consequences

- Adding logic to a slice is one decision, not three: stateful goes to a container class, pure goes to a plain
  function, shared vocabulary goes to the shared module.
- Purity is claimed by a test rather than a directory: a module that wants pure tests keeps itself import-clean, and a
  lapse shows up as that module's tests pulling in Qt.
- The lattice loses a row per table, and the import checker loses its strongest mechanical rule. We knew, and traded
  it for less ceremony in the slices without a pure core.
