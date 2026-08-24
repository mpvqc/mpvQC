# Agents

## Project structure

- See [docs/development.md](docs/development.md) for setup and commands.
- See [docs/architecture.md](docs/architecture.md) for the architecture and how everything fits together.
- Follow the MVVM architecture pattern. See [docs/architecture.md](docs/architecture.md) for the layer split.

## Project commands

- Run `just` to list common commands.
- Run linter and formatter via `just fmt`.
- Run the QML linter via `just lint-qml`.
- Run Python tests via `just test-python ARGS`. `ARGS` is passed to `pytest`.
- Run QML tests via `just test-qml`.
- Rebuild the test resource bundle via `just prepare-tests` after changing production QML, data, or translation files.
  `just test-python` and `just test-qml` don't rebuild it, and tests pass against a stale bundle without a warning.
- Never edit the file table in `pyproject.toml` by hand; `just build-develop` or `just prepare-tests` regenerates it.

## Coding

- Prefer the correct term over the term already in the repo. When a name contradicts the spec or the project it refers
  to, rename it and record the term in `CONTEXT.md`. Don't keep a wrong name to match other wrong names.
- Don't use structural comments like `# region` or `# ---`.
- Run background work through `SerialJobRunner` from `mpvqc/jobs.py`. Don't use `QThreadPool`, locks, or private queued
  signals in services directly.
- Prefer code the type checker can verify:
  - Use closures instead of `functools.partial`
  - Don't use getattr
- A feature package under `mpvqc/<feature>/` bundles everything one area needs: role directories (`services/`,
  `models/`, `viewmodels/`, `views/`, `enums/`) for what the area owns. Its root exports `bindings` and
  `register_qml_types` from its `wiring.py`, and the roots call them.
- A `views/` role holds a class the slice writes in Python and QML instantiates as part of the scene, such as a video
  output. The QML files themselves stay under `qt/qml/`.
- QML-registered enums live in the feature's `enums/`.
- There is no domain role (ADR 0019). A slice's logic lives in its services role: container-bound classes where
  there's state or Qt lifecycle, plain module-level functions over frozen dataclasses where it's pure. Shared pure
  vocabulary lives in `mpvqc/shared`.
- A class QML can name as a type keeps one full name in Python and QML: `Mpvqc`, the area, what it is, and its role.
  The prefix marks exactly those classes; everything unregistered names itself for its package.
- Inject-wired classes carry the `Service` suffix wherever they live. `mpvqc/services/` holds what no feature package
  has claimed; helpers that aren't inject-wired live at the top level of `mpvqc/`.
- Load the `slice-imports` skill before creating or editing Python in a feature package or its test tree.
- Load the `load-bearing-comments` skill before adding a comment or docstring, and when reviewing code.
- Load the `writing-models` skill before creating, reviewing, or modifying a Qt list model.
- Load the `writing-qml` skill before writing or editing a QML file.
- Load the `writing-view-models` skill before writing or editing a view model that reads service state.

## Testing

- Load the `writing-tests` skill before writing or changing a test.

## Writing

- Spell it "view model", two words, in all prose: docs, commit messages, tickets, comments. The closed form belongs to
  identifiers only, where a space is impossible: the `ViewModel` class suffix, the `mpvqc/viewmodels/` package, the
  `viewModel` QML property.
- In ADRs and `CONTEXT.md`, name the thing, not where it lives. Paths and file names go stale, so describe the component
  or the command instead. Setup and workflow docs are the exception: there the path is the point.
- Load the `writing-glossary` skill before adding or changing a term in `CONTEXT.md`.

## Committing

- Load the `committing` skill before committing — a code review gates the commit.

## Agent skills

### Issue tracker

Three destinations: the public GitHub tracker for user reports and triage, a private tracker for every internal work
item, and `.scratch/` for disposable artifacts. Nothing with a status stays local, and an agent never opens an issue on
the public tracker. Load the `filing-tickets` skill before filing anything and when picking up a tracked ticket;
`docs/agents/issue-tracker.md` decides where it goes.

### Triage labels

The label vocabulary of each tracker, and which of those labels exist today. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `CONTEXT.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.
