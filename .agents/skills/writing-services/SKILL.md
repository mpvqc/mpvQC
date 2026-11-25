---
name: writing-services
description: Service placement, class-or-function shape, and background work. Use when creating, editing, or reviewing a service, when moving logic into the services role, or when running work off the GUI thread.
---

# Writing services

The services role is a slice's one home for logic. Its imports are the `slice-imports` lattice, and it reaches a
model through the seam `writing-models` describes under "Service seam".

## Placement and naming

A bound class with an area belongs in that area's slice. A bound class every feature writes and none owns, holding a
fact and no logic, is a top-level helper under `mpvqc/`, and so is an unbound mechanism. A pure rule several areas
mean belongs in `mpvqc.shared`. There is no core, common, infra, or platform package; a module fitting none of these
homes stops the work until the user revisits the rule.

A service the inject container binds carries the `Service` suffix wherever it lives: `ImportService` inside the
importing slice, `SessionService` in `mpvqc.session`. Everything the container does not bind names itself plainly, as
`WindowButtonDetector` does. A model the container binds keeps its model name, `CommentStore` being the one. No
service is QML-registered, so none wears the `Mpvqc` prefix.

## Class or function

Picking the shape is the whole decision:

- **A container-bound class** where there is state, Qt lifecycle, or a substitution seam worth re-binding: a
  `QObject` with signals, `inject.attr` collaborators, mutable state it owns.
- **A plain module-level function over frozen dataclasses** where the logic is pure, such as `make_plan` over a
  `ScanResult`. It is callable with no container and no service instance.

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

- Every module sits in its home under the placement rule, and the `Service` suffix marks exactly the container-bound
  classes.
- The shape matches the logic, and every pure function runs without the container.
- Off-GUI-thread work runs through a `SerialJobRunner` the owner builds from an optional executor.
- Every `on_result` matches both `Ok` and `Err`, and the failure branch handles or logs the error.
- Everything the work body reads was captured on the GUI thread before it was handed over.
