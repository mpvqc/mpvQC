---
name: writing-tests
description: Silent passes in mpvQC tests. Use when writing, changing, or debugging a Python or QML test in this repo.
---

# Writing tests

The failure this repo keeps hitting is the **silent pass**: a test that goes green without exercising what it names.
Qt makes them easy to write. An exception raised inside a slot never reaches pytest. A spy waiting on a thread pool
holds the lock the pool needs. A QML test run against a stale resource bundle tests yesterday's code. Every rule
below closes one.

## What to test

Test the areas that carry risk, not the lines that are cheap to reach.

Reach for a table when the inputs vary and the assertion does not: `@pytest.mark.parametrize` in Python, a
`test_<name>_data()` function returning tagged rows in QML. Write cases out longhand when a table would hide what
each one proves.

Every test passes on Linux and Windows.

## Python

### Background work

Pass `manual_executor` to the service constructor. Background work then queues instead of running, and the test
drives it:

```python
service = SomeService(manual_executor)
service.do_something()
manual_executor.drain()
```

`drain()` runs everything queued, including jobs a callback adds while draining. `run_next()` runs exactly one, which
is how you assert on ordering and on what is still pending.

### Asserting across a callback

PySide swallows exceptions at the emit boundary, so an assert inside a slot or an `on_result` callback cannot fail
the test. The test goes green on an assertion that never ran, a silent pass. Record into a list, then assert after
the drain:

```python
deliveries: list[Result[None]] = []
runner.run(work, deliveries.append)
manual_executor.drain()
assert deliveries == [Ok(None)]
```

The `SerialJobRunner` tests work this way throughout.

### Case bags

A parametrized `NamedTuple` case list reads worst when its entries mix shapes. Pick one shape for the whole bag: if
every entry fits the line limit as a true one-liner, every entry is one; otherwise every entry is one field per
line, with a trailing comma on the last field so `just fmt` keeps it exploded. Never leave some entries one-liners
and others wrapped, and never let the formatter's default partial wrap stand.

Spell out the field names (`InvalidCase(name=..., data=..., match=...)`) rather than passing positional arguments —
positional calls hide which value is which once a bag has more than one or two fields.

### Real thread pools

When a test needs the real executor rather than `manual_executor`, wait with
`QThreadPool.globalInstance().waitForDone()` followed by `processEvents()`. Repeat the pair once per queued job: the
runner hands out one job at a time and delivers each result on the GUI thread before starting the next.

A spy's `wait()` holds the GIL, so the pooled job never starts and the wait times out.

### Spies

Build them with the `make_spy` fixture. It asserts the connection is valid on construction; a raw `QSignalSpy` bound
to a misspelled signal reports zero emissions and fails nothing: a silent pass.

## QML

### Running them

`just prepare-tests` first, if production QML, data, or translations changed. The session fixture catches a resource
bundle that is missing, never one that is out of date, so a stale bundle is a silent pass on yesterday's QML.

Run one file with `just test-qml-debug <TARGET>`, all of them with `just test-qml`. `just test-qml 1` uses a single
process, which is what Windows and CI do.

### Building the object under test

Create it through `createTemporaryObject` so it dies with the test. Wrap that in a local `makeControl()` that also
verifies it, and a local `makeSpy()` for spies:

```qml
function makeControl(properties = {}): Item {
    const control = createTemporaryObject(objectUnderTest, testCase, properties);
    verify(control);
    return control;
}
```

Add `waitForRendering(control)` when the test touches layout or geometry. When several test files share the
scaffolding, it lives in a `TestHelpers.qml` beside them.

### Waiting

Wait on the condition with `tryCompare` or `tryVerify`. A fixed delay is either longer than the test needs or shorter
than a loaded CI machine, and the second one is a flake.

## Done when

- Every assertion sits on the test's own stack, never inside a slot or a callback.
- Every case bag has one shape throughout: all one-liners, or all one field per line.
- Nothing waits on a duration.
- `just prepare-tests` has run, if production QML, data, or translations changed.
- The full suite passes, not only the tests you filtered to while iterating.
