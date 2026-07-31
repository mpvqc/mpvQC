# Run dataflow view models on the snapshot pattern

A dataflow view model consumes service state and exposes derived values to QML. Written slot by slot, every consumed
signal gets a public setter, every derived value its own update method, and each hand-maintains its own dedupe and
its own list of dependents. The derivation smears across the file, the interface fills with members that are wiring
rather than interface, and tests push state through that wiring past the seam production uses. The footer view model
was the worst case and is the first migration.

The pattern runs on two frozen structs private to the view model. The **inputs snapshot** holds exactly the scalars
the view model derives from, one field per consumed upstream signal — a projection whose field list names the exact
dependency set, never an embedded service state. The **props snapshot** holds the value of every QML-facing
property. The cycle between them is three motions:

- **Fold**: one private handler per consumed signal replaces that one field in the inputs snapshot and runs the
  cycle. Services are read exactly once, at construction, to build the initial inputs snapshot; afterwards only
  signal payloads arrive. Payloads are trustworthy because every upstream emits from stored state, coerced and
  deduped at its own boundary — so initial-read and update semantics cannot diverge.
- **Derive**: one pure function takes the inputs snapshot and returns the props snapshot. Pure static helpers are
  called directly inside it; a stateful dependency crosses as an injected callable, so the signature names the
  derivation's real dependencies.
- **Emit**: the new props snapshot is swapped in before the first emission, then each per-field notify emits exactly
  when its value changed, carrying the new value. The swap completing first makes settled-state reads structural: an
  observer of any notify sees fully consistent state, independent of connection order.

Sourcing is per-field by default: the view model subscribes to the per-field signals the services already emit.

The unchanged-inputs guard — returning early when the folded inputs equal the previous snapshot — is a conditional
element, not part of the base pattern. While every upstream dedupes at its source, the guard is unreachable and
untestable through the seam. It is added only when an upstream can refire an unchanged payload; the first expected
case is a payload-free trigger like retranslation.

## Consequences

- The interface holds only what the view binds: the properties, their notifies, and real slots. Service wiring is
  private, so neither callers nor tests can push state past the production seam.
- Every derived value is verifiable by calling the derivation directly — one table row per case, no view model
  construction.
- Wiring tests drive real service signals in and assert exact emission sets out: the fields whose derived value
  changed, nothing else.
- An unrelated update never makes QML re-read the other properties, and an unrelated service field never wakes the
  view model at all.
- Roughly thirteen dataflow view models are expected to migrate onto the pattern; the rest of the layer — dialog
  drivers, one-shot commands — coexists unchanged.

## Dropped alternatives

- **A shared single notify** for all properties: one signal on any change makes QML re-read every property and
  loses per-property change granularity.
- **Per-value selector objects**, one per derived value with its own recompute and signal: more objects and
  connection order back in play, for the same observable behavior.
- **Descriptor or dependency-graph primitives** that declare fields once and generate the wiring: speculative
  machinery — the cycle is a dozen plain lines per view model.
- **Read-everything refresh**, re-reading all services on any signal and diffing: reintroduces the initial-read
  versus update divergence and hides the dependency set the inputs snapshot exists to name.
- **A player state-snapshot publication**, the player service emitting its whole reduced state as one payload: no
  two consumed fields co-change in one reduce today, per-field payloads are equally trustworthy, and per-field
  sourcing wakes consumers strictly less often. Revisit when a consumer must read co-changing fields in one
  observation — a path load's video-loaded flag together with its dimensions, or both track counts.
