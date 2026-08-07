# Attach a feature package through its wiring

The roots knew too much about the packages they composed. Startup listed every role directory that held a
QML-registered class, three of them for one feature, so adding or splitting a role inside a feature meant editing a
function two packages away that had no other reason to change. The two things a feature owes the application, its
container bindings and its QML registrations, also sat apart: one in a module of its own, the other as three lines in
an import list shared with the layer packages.

A feature package answers two calls, `bindings` and `register_qml_types`, and the package root exports both. A root
names the feature and nothing under it. What a feature does when asked stops at its boundary, the same way assembling a
service already did, and the roots go back to deciding only which packages take part.

## The wiring module names no mpvqc module and no Qt

Both functions live in a wiring module that imports no first-party module and no Qt at module level. Each function
imports what it needs when it runs, and the binder type appears only in an annotation, so it goes under `TYPE_CHECKING`.

The rule does not make configuring injection registration-free, and claiming otherwise would be wrong. Binding a
feature's services reaches `mpvqc.services`, which pulls in the shared enum package and the comment selection service,
and six QML types register there before `QGuiApplication` exists. That chain is its own problem and this decision does
not touch it.

What the rule buys is narrower and still worth having. Naming a feature in a root costs nothing until something calls
in, so a domain test that wants no toolkit gets none. And the wiring module never becomes one more place the chain can
start: QML-facing classes register by decorator when their module is imported, so a top-level import of a view model
here would fire this feature's registrations on every import of the package, including the imports that wanted none of
them. That is the shape of the accident that ran seven registrations inside a domain import (ADR 0013), and it would
arrive the same way, with someone hoisting an import to the top and nothing complaining. Written as "no `mpvqc` and no
`PySide6` at module level", the rule is short enough to check by eye.

## Why the root exports it

ADR 0009 said the package root exports nothing. It now says no vocabulary, which is what the rule always meant.
Re-exporting `ImporterService` from the root would give the class two names and let a call site drop the role it
belongs to, so each role directory does its own re-exporting and the root stays out of it. Vocabulary still travels by
role: a call site importing a service or a view model names the role that owns it.

Wiring is not vocabulary. It is neither a service nor a model nor a view model, so no role directory fits it, and it is
the only thing the root exports. The rule it breaks was never aimed at it.

The cross-slice lattice (ADR 0012) has a row per role and none for wiring, which is correct rather than an omission.
The lattice governs what one slice's roles may import from another slice. Wiring imports its own package and the shared
boundary services every feature already reads, and it runs from a root that by definition knows every package. It is
the composition seam, and it stands outside the table the way a composition root always does.

## Consequences

- Importing a feature package loads its wiring and nothing else. Naming a feature in a root costs no Qt and no
  registration until something calls in.
- Attaching a feature is two lines in each of the two roots, an import and a call. Roles the feature adds or drops
  later touch neither root.
- The bare imports left in startup name the layer packages no feature has claimed. The list shrinks as areas migrate,
  so it reads as the state of the migration.
- One filename no longer finds every wiring site. `fd injections` used to catch both features and the root; the
  features took the new name and the root kept the old one. Grep the functions instead.
- Nothing checks that a wiring module keeps the rule. The check has to run in a fresh interpreter or read the module's
  top-level nodes, because under pytest both `mpvqc` and `PySide6` are in `sys.modules` before the test starts and an
  assertion against that would pass no matter what the module imports. Writing it is follow-up work.
