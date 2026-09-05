---
name: writing-services
description: Service placement, class-or-function shape, and background work. Use when creating, editing, or reviewing a service, when moving logic into the services role, or when running work off the GUI thread.
---

# Writing services

The services role is a slice's one home for logic. Its imports are the `slice-imports` lattice, and it reaches a
model through the seam `writing-models` describes under "Service seam".

## Placement and naming

A service the inject container binds carries the `Service` suffix wherever it lives: `ImportService` inside the
importing slice, `StateService` in `mpvqc/services/`. Everything the container does not bind names itself plainly, as
`WindowButtonDetector` does — the window slice's backend builds it in a factory, so it wears no suffix. A model the
container binds keeps its model name, `CommentStore` being the one.

`mpvqc/services/` holds what no feature package has claimed. A helper that belongs to no slice and to no container
sits at the top level of `mpvqc/`, as `mpvqc/jobs.py` does.

No service is QML-registered, so none wears the `Mpvqc` prefix that ADR 0009 governs.

## Class or function

Logic takes one of two shapes, and picking between them is the whole decision (ADR 0012):

- **A container-bound class** where there is state, Qt lifecycle, or a substitution seam worth re-binding: a
  `QObject` with signals, `inject.attr` collaborators, mutable state it owns.
- **A plain module-level function over frozen dataclasses** where the logic is pure: `make_plan` over a `ScanResult`,
  `render_v1` over an `ExportSnapshot`. It is importable and callable with no container and no service instance.

Nothing is injected for uniformity: a pure function stays a function, and vocabulary several areas mean moves out to
`mpvqc.shared` instead.

## Background work

`SerialJobRunner` from `mpvqc/jobs.py` is the seam for everything that leaves the GUI thread, in a service and in a
view model alike. Its owner builds one in `__init__` from an executor the caller may supply:

```python
def __init__(self, executor: JobExecutor | None = None) -> None:
    super().__init__()
    self._jobs = SerialJobRunner(executor)
```

That parameter is the substitution seam tests drive, which `writing-tests` covers.

`on_result` runs back on the GUI thread and receives a `Result[T]` — `Ok(value)` or `Err(error)` — which it matches:

```python
def detect(self) -> None:
    self._jobs.run(work=self._read_preference, on_result=self._apply_preference)

def _apply_preference(self, result: Result[WindowButtonPreference]) -> None:
    match result:
        case Ok(preference):
            ...
        case Err(error):
            logger.error("Window button detection failed", exc_info=error)
```

A job left without `on_result` logs its own failure and delivers nothing, so a result anyone waits on needs the
callback. One runner's jobs never overlap: queued work runs one at a time in order, each result delivered before the
next job starts.

Read Qt and service state on the GUI thread, into locals or a frozen dataclass, before the closure captures it.
`ImportService` captures the settings and player values its plan needs; `ExportService` captures an `ExportSnapshot`.
The work body then touches only what it was handed, which is what makes it race-free.

Reach for the runner rather than a `QThreadPool`, a lock, or a queued signal of your own: those live inside
`SerialJobRunner`.

## Done when

- Every module sits at its narrowest home: the owning slice's `services/`, `mpvqc/services/` when no slice owns it,
  the top level of `mpvqc/` when no container binds it.
- Every container-bound service carries the `Service` suffix, and nothing the container leaves alone carries it.
- The shape matches the logic: state or Qt lifecycle in a bound class, purity in a module-level function over frozen
  dataclasses.
- Every pure function is callable without configuring the container or constructing a service.
- Off-GUI-thread work runs through a `SerialJobRunner` the owner builds from an optional executor.
- Every `on_result` matches both `Ok` and `Err`, and the failure branch handles or logs the error.
- Everything the work body reads was captured on the GUI thread before it was handed over.
- The touched code's own test module passes under `just test-python`.
