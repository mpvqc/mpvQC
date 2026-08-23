# Run dataflow view models on the snapshot pattern

A dataflow view model consumes service state and exposes derived values to QML. Written slot by slot, every consumed
signal gets a public setter and every derived value its own update method, each hand-maintaining its dedupe and its
list of dependents. The derivation smears across the file, the interface fills with wiring, and tests push state
through that wiring past the seam production uses.

The pattern runs on two frozen structs private to the view model. The **inputs snapshot** holds one field per consumed
upstream signal, so its field list names the exact dependency set. The **props snapshot** holds every QML-facing
property that carries derived state. The cycle between the two is three motions:

- **Fold**: one private handler per signal replaces that one field and runs the cycle. Services are read once, at
  construction; afterwards only payloads arrive, and they are trustworthy because every upstream emits from stored
  state, deduped at its own boundary.
- **Derive**: one pure function takes the inputs snapshot and returns the props snapshot. A stateful dependency crosses
  as an injected callable, so the signature names the derivation's real dependencies.
- **Emit**: the props snapshot is swapped in before the first emission, then each per-field notify emits exactly when
  its value changed. The swap completing first means an observer of any notify sees consistent state, whatever the
  connection order.

The pattern covers more than view models. A service that consumes upstream signals and hands derived values to its
consumers runs on the same cycle, and the main window service is the one instance: it folds the window's surface size,
the platform's surface and state reads, the application's focus window and the display zoom into the values the window
controls, the player and the video resize service read. Being bound to a window changes two things. The
read-once moment is the bind, not construction, because there is no window to read before it: binding reads every
upstream once and runs a single update. And a fold may re-read through a port whose platform implementation acts on
what it reads: the Windows state read retires an abandoned fullscreen session as it answers, and that retire can
re-enter the fold. Such a fold reads before it replaces the inputs, so it folds onto whatever the re-entrant run left
behind.

Granularity follows the props' co-change structure. One field per property with its own notify is the default. Fields
that always co-change belong in one composite field behind one notify, as long as the consumer dedupes at the sink.
Per-field notifies exist so an unrelated update cannot wake an unrelated binding, and where every field moves together
there is no unrelated update: QML's own change detection discards whatever did not move, so the extra signals were
measured to wake no fewer sinks and to cost the same.

## Consequences

- The interface holds only what the view binds. Service wiring is private, so neither callers nor tests can push state
  past the production seam.
- Every derived value is verifiable by calling the derivation directly, one table row per case.
- Wiring tests drive real service signals in and assert exact emission sets out: the fields whose derived value
  changed, nothing else.
- An unrelated service field never wakes the view model at all.

## Dropped alternatives

- **A shared single notify** across props that move independently: QML re-reads every property on any change.
- **A map payload** for a composite field, its fields crossing as one map: the fastest wiring measured, and the only
  one that gives up linter checking on the field names.
- **Per-value selector objects**: more objects and connection order back in play, for the same observable behavior.
- **Descriptor or dependency-graph primitives** that generate the wiring: speculative machinery, when the cycle is a
  dozen plain lines per view model.
- **Read-everything refresh** on any signal: reintroduces the initial-read versus update divergence and hides the
  dependency set the inputs snapshot exists to name.
