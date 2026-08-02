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
- Run QML tests via `just test-qml`.
- Rebuild the test resource bundle via `just prepare-tests` after changing production QML, data, or translation files.
  `just test-python` and `just test-qml` don't rebuild it, and tests pass against a stale bundle without a warning.

## Coding

- Prefer the correct term over the term already in the repo. When a name contradicts the spec or the project it refers
  to, rename it and record the term in `CONTEXT.md`. Don't keep a wrong name to match other wrong names.
- Don't use structural comments like `# region` or `# ---`.
- Avoid comments unless absolutely necessary. In any case, keep them short.
- Run background work through `SerialJobRunner` from `mpvqc/jobs.py`. Don't use `QThreadPool`, locks, or private queued
  signals in services directly.
- Prefer code the type checker can verify:
  - Use closures instead of `functools.partial`
  - Don't use getattr
- A feature package under `mpvqc/<feature>/` bundles everything one area needs: `domain.py` at its root, plus role
  directories (`services/`, `models/`, `viewmodels/`) for what the area owns. It contributes its own bindings and the
  composition root calls them.
- Inject-wired classes carry the `Service` suffix wherever they live. `mpvqc/services/` holds what no feature package
  has claimed; helpers that aren't inject-wired live at the top level of `mpvqc/`.
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

- Load the `committing` skill before committing.

## Agent skills

### Issue tracker

User reports and triage live on GitHub Issues; larger chunks of work are planned as local markdown under
`.scratch/<feature>/`, and internally found bugs go to `.scratch/bugs/` — never to the public tracker. See
`docs/agents/issue-tracker.md`.

### Triage labels

Default label vocabulary (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See
`docs/agents/triage-labels.md`.

### Domain docs

Single-context: `CONTEXT.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.
