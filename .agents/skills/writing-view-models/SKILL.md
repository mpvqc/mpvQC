---
name: writing-view-models
description: The snapshot pattern for dataflow view models. Use when writing, reviewing, or migrating a view model that reads service state and exposes derived properties to QML.
---

# Writing view models

A view model that reads service state and hands derived values to QML runs on the **snapshot pattern**, and so does a
service that consumes upstream signals and hands derived values to consumers. Written any other way the derivation
smears across the file, every consumed signal grows a public setter, and tests push state in past the seam production
uses.

Out of scope: one-shot commands, and view models that only forward to a service. They stay as they are. Forwarding
covers slot calls, and it covers service values published unchanged under their QML names, each notify connected
straight to the service's signal: nothing is derived there, so there is no snapshot to keep. The window controls view
model is one.

ADR 0006 carries the reasoning and the alternatives that were dropped.

## The two snapshots

Two frozen dataclasses, both private to the view model in intent:

- **Inputs snapshot** — `<Name>Inputs`. One field per consumed upstream signal, holding the scalar the derivation
  reads. Never an embedded service object: the field list is a projection that names the exact dependency set.
- **Props snapshot** — `<Name>Props`. One field per QML-facing property, holding its value. Props that always
  co-change are one composite field behind one notify, where the consumer dedupes at the sink: the palette view model
  carries the whole palette that way and hands QML a read-only object over it. ADR 0006 holds the measurements.

## The cycle

Fold, derive, emit. Every path through the view model runs all three.

### Fold

One private `_fold_<field>` slot per consumed signal. It replaces its one field and runs the cycle:

```python
@Slot(bool)
def _fold_video_loaded(self, value: bool) -> None:
    self._update(replace(self._inputs, video_loaded=value))
```

Services are read exactly once, in `__init__`, to build the first inputs snapshot. Afterwards only signal payloads
arrive. Payloads are trustworthy because every upstream emits from stored state, coerced and deduped at its own
boundary, so the initial read and the update path cannot end up disagreeing.

Subscribe to the per-field signals the services already emit.

### Derive

One module-level pure function, `derive_<name>_props(inputs, ...) -> <Name>Props`, importable and callable without
constructing the view model.

Pure static helpers are called inside it directly. A stateful dependency crosses as an injected callable, so the
signature names the derivation's real dependencies:

```python
def derive_footer_props(inputs: FooterInputs, measure_width: Callable[[str], int]) -> FooterProps:
```

When the derivation takes callables bound to `self`, a private `_derive()` binds them in one place and the cycle calls
that. When it takes the inputs alone, the cycle calls the module function.

### Emit

```python
def _update(self, inputs: FooterInputs) -> None:
    self._inputs = inputs
    new, old = self._derive(), self._props
    if new == old:
        return
    self._props = new
    if new.time_text != old.time_text:
        self.timeTextChanged.emit(new.time_text)
```

`self._props` is swapped in before the first emission. That makes settled-state reads structural: an observer of any
notify sees fully consistent state, whatever the connection order.

Each notify then fires exactly when its own field changed, carrying the new value.

## Conditional elements

Three additions that are not part of the base pattern. Each one names the upstream that needs it, in a comment or in
the commit message.

**Unchanged-inputs guard** — returning early when the folded inputs equal the previous snapshot. Every upstream
dedupes at its source, which leaves the guard unreachable and untestable through the seam. Add it when an upstream can
refire an unchanged payload.

**Burst coalescing** — a trailing debounce between fold and cycle, for a consumer that needs one settled emission per
upstream burst. Folds still apply every payload immediately; the timer defers derive-and-emit alone, so the cycle runs
once against settled inputs and emits only the deltas that survive the burst. The fold side is `_apply`, the timer side
`_derive_and_emit`, and the window is a keyword-only constructor argument. Tests set it far beyond their own run time,
then fire the timer's `timeout` themselves through `findChild(QTimer)`, asserting `isActive()` first. A short window
races the test's own event-loop pumps, and an unarmed timer fired by hand would hide a fold that never starts it.

**Trigger fold** — the fold for a payload-free signal, and how ambient state enters the snapshot. The handler re-reads
exactly the values the signal announces, nothing else, into dedicated inputs fields, so the derivation stays pure over
the inputs snapshot alone. Constants read once at construction sit in the inputs snapshot with no fold at all.

## Tests

Three kinds. A migrated view model has all three.

**Derivation** — a table calling `derive_<name>_props` directly, one row per case, no view model constructed.

**Wiring** — drive a real service signal in and assert the exact emission set out: the fields whose derived value
changed, and a zero count on every field that stayed silent. Cases where a signal changes nothing observable assert
that everything stayed silent.

**Settled state** — one test that an observer of a notify reads fully consistent props:

```python
view_model.isDarkChanged.connect(lambda _: observed.append((view_model.isDark, view_model.background)))
```

## Done when

- Every QML-facing property returns a props field, or an object the view model publishes over one, and no derived
  value is stored anywhere else.
- Services are named in `__init__` and in the slots that write back to them, nowhere else.
- The public surface is the properties, their notifies, and the slots the view binds. No member exists so that
  something can push state in.
- `self._props` is swapped before the first emission, and each notify fires exactly when its field changed.
- The derivation is proven by a table that never constructs the view model, and the wiring by tests that name the
  fields which stayed silent.
