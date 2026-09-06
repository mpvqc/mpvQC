# Organize Python as feature slices

Horizontal layer packages sorted code by what a class was, not what it was about. One feature was spread across every
layer and held together by naming. Python is therefore organized vertically: each area gets one feature slice, with a
directory for every role it claims. Tests mirror the slice.

## Slice roles and ownership

A slice may contain `services`, `models`, `viewmodels`, `views`, and `enums`. Each role exposes a public API. Callers
outside the role import through that API, so they name the role while the layout beneath it remains free to change.
The slice itself exports no vocabulary.

Ownership follows meaning. A slice owns its settings keys, defaults, typed accessors, and change signals even when the
underlying ini section also contains another slice's keys. Stored keys do not rename cheaply because an older release
may still read them. The settings handle is bound once in composition, and every slice writes through it.

Shared vocabulary, top-level helpers, and composition stay horizontal. A bound class with an area belongs in that
area's slice. A bound class every feature writes and none owns, holding a fact and no logic of its own, is a top-level
helper. An unbound mechanism is a top-level helper. A pure rule several areas mean belongs in the shared vocabulary.
The import checker's helper table is the roster. There is no core, common, infra, or platform package; a module fitting
none of these stops the work until the placement rule is revisited.

The desktop service is a shell-owned boundary: the about dialog, config editors, and app data command all hand URLs
to the OS. The backup dialog uses that same service through the shell's public services API.

## Logic lives in services

The services role is a slice's one home for application logic. Stateful logic, Qt lifecycle, and substitution seams
use classes bound in the injection container. Pure logic uses module-level functions over frozen data. Nothing is
injected merely for uniformity.

An earlier domain role tried to enforce purity by directory. It helped the import planner's pure combinatorics, but
taxed every thinner slice with forwarding services, handed-in pure helpers, and tests that had to reconnect what the
boundary split. Purity comes from frozen inputs, pure functions, and no shared mutable state, not from a directory.
Modules that need pure tests keep their own imports clean. No slice has a domain role.

Vocabulary that several slices mean lives in the shared vocabulary component, where every role can import it. This is
vocabulary only, not a second home for application logic.

## Attach a slice through its wiring

Each slice exposes `bindings` and `register_qml_types` through its wiring component. Composition roots decide which
slices participate and call those two entry points; they do not know which roles a slice contains.

The wiring component imports no first-party or Qt component until one of its entry points is called, so importing a
slice loads no toolkit and triggers no QML registration. Wiring is a composition seam, not vocabulary or a role, and
therefore sits outside the import lattice.

## Import lattice

The communication rule in [ADR 0008](0008-communicate-across-slices-with-calls-not-events.md) stands: commands cross
slices through public service calls, facts cross as public service state and signals, and presentation never crosses a
slice. Every role may import freely inside itself and may import the shared vocabulary.

| From | Same slice | Another slice |
| --- | --- | --- |
| `enums` | - | - |
| `models` | `enums`, `services` | `enums` |
| `services` | `services` | `services` |
| `viewmodels` | `models`, `services`, `enums` | `services`, `enums` |
| `views` | `models`, `services`, `enums` | `services`, `enums` |

A foreign slice's models, view models, and views are closed. The `views` role holds native Qt objects that QML
instantiates as part of the scene. The import checker enforces the lattice, role-root imports, and lazy wiring.

## Consequences

- One area is one tree, and each foreign edge is visible in its imports.
- Adding logic means one choice: a container-bound class, a pure function, or shared vocabulary.
- Adding or removing a role changes only the slice. Composition roots keep calling the same two wiring entry points.
- Purity is no longer enforced for a whole role. A lapse affects the module that wanted pure tests rather than every
  slice paying for a mechanical wall.
