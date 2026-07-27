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
- Run all QML tests via `just test-qml`, one process per file. `just test-qml 1` uses a single process, as Windows
  and CI always do.

## Coding

- Follow clean code principles.
- Prefer the correct term over the term already in the repo. When a name contradicts the spec or the project it refers
  to, rename it and record the term in `CONTEXT.md`. Don't keep a wrong name to match other wrong names.
- Don't use structural comments like `# region` or `# ---`.
- Avoid comments unless absolutely necessary. In any case, keep them short.
- Run background work through `SerialJobRunner` from `mpvqc/jobs.py`. Don't use `QThreadPool`, locks, or private queued
  signals in services directly.
- Prefer code the type checker can verify:
  - Use closures instead of `functools.partial`
  - Don't use getattr
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
  03. The view model property, even when it is private
  04. Aliases (property alias / readonly property alias)
  05. Readonly value properties (public)
  06. Mutable properties (public)
  07. Private properties (underscore-prefixed)
  08. Signal declarations
  09. Enums
  10. JavaScript functions
  11. Own object property bindings (height, width, anchors, color, etc.)
  12. Attached property bindings (Material. *, ListView.* bindings, Layout.\*)
  13. Property change handlers (onXChanged)
  14. Attached signal handlers (ListView.onPooled/onReused, Component.onCompleted/onDestruction, Keys.onPressed)
  15. Child objects (visual children)
  16. Behaviors
  17. States
  18. Transitions

## Testing

- Prefer data-driven Python tests but clarity always wins.
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
- Spell it "view model", two words, in all prose: docs, commit messages, tickets, comments. The closed form belongs to
  identifiers only, where a space is impossible: the `ViewModel` class suffix, the `mpvqc/viewmodels/` package, the
  `viewModel` QML property.
- In ADRs and `CONTEXT.md`, name the thing, not where it lives. Paths and file names go stale, so describe the component
  or the command instead. Setup and workflow docs are the exception: there the path is the point.

## Committing

- Never commit before the user has reviewed the changes.
- Run all pre-commit hooks via `just fmt` to confirm everything's fine before committing.
- `just fmt` checks tracked files only. `git add` new files before trusting it.
- Verify the documentation is up to date before committing.
- Use the [Conventional Commits](https://www.conventionalcommits.org/) format.
- Don't add yourself as a co-author.

## Agent skills

### Issue tracker

User reports and triage live on GitHub Issues; larger chunks of work are planned as local markdown under
`.scratch/<feature>/`. See `docs/agents/issue-tracker.md`.

### Triage labels

Default label vocabulary (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See
`docs/agents/triage-labels.md`.

### Domain docs

Single-context: `CONTEXT.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.
