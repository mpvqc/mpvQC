# Communicate across slices with calls, not events

Feature packages have to talk to each other, and the mainstream shape for that in a modular monolith is domain events
between modules. We decided against it. A slice commands a more central slice by calling its public service API through
injection, and the rest of the app learns what happened from the state the called slice already publishes. There is no
event bus, no relay, no subscription between slices.

The reasoning runs on the difference between a command and a fact. An import is a sequential transaction: reset, load
the video, insert the comments. A subscriber that ignores it breaks it, so it is a command, and modeling commands as
events scatters one transaction across subscribers with implicit ordering. Facts go the other way, and they already
have a channel: the slice that owns a fact publishes it as state with a change signal, and reactors couple to that
owner, not to whoever caused the change. Ten causes of a comment change need zero new subscriptions. Events between
slices would also point the arrow backwards, with core slices subscribing to peripheral ones, and the decoupling they
buy pays off across process and team boundaries that a desktop app in one repo does not have. The substitution seam
tests need exists either way: the inject container re-binds a service as easily as it would re-bind a port.

## The lattice

Which role may import what from another slice:

| From         | May import from another slice                             |
| ------------ | --------------------------------------------------------- |
| `domain/`    | `domain/` only                                            |
| `models/`    | `domain/` only                                            |
| `services/`  | `services/`, `domain/`                                    |
| `viewmodels/`| `services/`, `domain/`. Never `viewmodels/` or `models/`  |

Nobody imports another slice's internals. Cross-slice use cases live in view models, which may command several slices'
services: services never know their coordinators. Presentation never crosses slices in Python; views compose views in
QML. A signal that crosses a slice boundary lives on the slice's public service and carries primitives or shared domain
types, never internal objects. Signal payloads are checked by Qt at runtime only, in every style, since the PySide6
stubs type a slot as `object`; the surface the type checker verifies is the methods, and that is where the domain types
travel.

## Ports stay the exception

Dependency inversion is for arrows that would otherwise point at something volatile or in the wrong direction: an OS
boundary, an external process, a plugin seam, or a central slice that would otherwise depend on a peripheral one. The
platform backends already use it, and correctly. Everywhere else a port would invert an arrow that already points the
right way, at the price of a third vocabulary and a pass-through layer per edge.

A prototype pinned the Qt-viable port shape and the migration cost. A Protocol cannot carry a signal (pyrefly rejects
descriptor members, and signal access needs a QObject instance), so a signal-carrying port is an abstract QObject base
with a forwarding adapter bound at the composition root:

```python
class PlaybackFacts(QObject):              # the port
    duration_changed = Signal(float)

class PlayerFactsAdapter(PlaybackFacts):   # the adapter
    def __init__(self) -> None:
        super().__init__()
        inject.instance(PlayerService).duration_changed.connect(self.duration_changed)
```

Extracting a port later touches three files and the consumer's `.connect()` call sites survive verbatim, so choosing
calls today closes no door.

## Consequences

- The service graph between slices stays acyclic and points at the more stable slice. Two slices' services wanting each
  other is evidence of a missing concept that one of them should own, never a reason for a bus.
- Every foreign edge of a slice is greppable in one role directory, and the lattice is mechanical enough for an import
  linter to enforce. Wiring that up is follow-up work.
- A future edge that earns a port pays for that one edge when it happens. Nothing is prepaid.
