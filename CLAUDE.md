<!--
SPDX-FileCopyrightText: mpvQC developers

SPDX-License-Identifier: MIT
-->

# Claude Code

## Project structure

- See [docs/development.md](docs/development.md) for setup and commands.
- See [docs/architecture.md](docs/architecture.md) for the architecture and how everything fits together.
- Follow the MVVM architecture pattern. See [docs/architecture.md](docs/architecture.md) for the layer split.

## Project commands

- Run `just` to list common commands.
- Run linter and formatter via `just fmt`.
- Run the QML linter via `just lint-qml`.
- Run Python tests via `just test-python ARGS`. `ARGS` is passed to `pytest`.
- Prepare QML tests via `just prepare-tests` when you've changed production QML, data, or translation files.
- Run a single QML test file via `just test-qml-debug <TARGET>`.
- Run all QML tests via `just test-qml`.

## Coding

- Follow clean code principles.
- Don't use structural comments like `# region` or `# ---`.
- Avoid comments unless absolutely necessary.
- Run background work through `SerialJobRunner` from `mpvqc/jobs.py`. Don't use `QThreadPool`, locks, or private queued
  signals in services directly.
- Prefer code the type checker can verify: use closures instead of `functools.partial`.
- Only inject-wired classes live in `mpvqc/services/` and carry the `Service` suffix. Helpers that aren't in
  `injections.py` live at the top level of `mpvqc/`.
- Use the `signal name(value: type)` notation instead of the old `signal name(type value)` notation in QML signals.
- Import `QtQuick.Controls` for controls.
  - Never import `QtQuick.Controls.Material` unnamespaced: it resolves controls to Material directly and silently
    bypasses the MpvqcStyle overrides, regardless of import order.
  - For Material attached properties, use `import QtQuick.Controls.Material as M` and reference `M.Material.*`.
  - Only files inside `qt/qml/MpvqcStyle/` import the Material style unnamespaced.
- Follow official QML coding conventions.
- Respect the recommended QML file layout:
  01. id
  02. Required properties
  03. Aliases (property alias / readonly property alias)
  04. Readonly value properties (public)
  05. Mutable properties (public)
  06. Private properties (underscore-prefixed)
  07. Signal declarations
  08. Enums
  09. JavaScript functions
  10. Own object property bindings (height, width, anchors, color, etc.)
  11. Attached property bindings (Material. *, ListView.* bindings, Layout.\*)
  12. Property change handlers (onXChanged)
  13. Attached signal handlers (ListView.onPooled/onReused, Component.onCompleted/onDestruction, Keys.onPressed)
  14. Child objects (visual children)
  15. Behaviors
  16. States
  17. Transitions

## Testing

- Prefer data-driven Python tests.
- Prefer testing important areas in the code. Don't go for coverage only.
- Swap background execution in Python tests by passing `manual_executor` to the service constructor. The
  `manual_executor` fixture lives in `test/conftest.py`.
- Spy on signals with the `make_spy` fixture instead of raw `QSignalSpy`.
- Don't assert inside Qt slots or `on_result` callbacks: PySide swallows exceptions at the emit boundary. Record values
  and assert after the drain.
- Don't wait for thread pool work with a spy's `wait()`: it holds the GIL and the pool job never runs. Use
  `QThreadPool.waitForDone()` plus `processEvents()`.
- Prefer data-driven QML tests and construct the object being tested using `makeControl` / `makeSpy` and
  `createTemporaryObject`.
- Ensure tests pass on Linux and Windows.
- Don't use hard timeouts in QML tests.

## Writing

- Load the `plain-english` skill before writing documentation and when communicating with the user.

## Committing

- Never commit before the user has reviewed the changes.
- Run all pre-commit hooks via `just fmt` to confirm everything's fine before committing.
- `just fmt` checks tracked files only. `git add` new files before trusting it.
- Verify the documentation is up to date before committing.
- Use the [Conventional Commits](https://www.conventionalcommits.org/) format.
