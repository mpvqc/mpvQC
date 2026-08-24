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

- Prefer code the type checker can verify: closures over `functools.partial`, named attributes over `getattr`.
- A class QML can name keeps one name in Python and QML: `Mpvqc`, the area, what it is, its role. An unregistered
  class wears no prefix and names itself for its package. When a module gains its first registered class, read ADR
  0015: no two modules holding a registered class share a file name.

## Writing

- Spell it "view model", two words, in all prose: docs, commit messages, tickets, comments. The closed form belongs to
  identifiers only, where a space is impossible: the `ViewModel` class suffix, the `mpvqc/viewmodels/` package, the
  `viewModel` QML property.
- In ADRs and `CONTEXT.md`, name the thing, not where it lives. Paths and file names go stale, so describe the component
  or the command instead. Setup and workflow docs are the exception: there the path is the point.

## Agent skills

### Issue tracker

Three destinations: the public GitHub tracker for user reports and triage, a private tracker for every internal work
item, and `.scratch/` for disposable artifacts. Nothing with a status stays local, and an agent never opens an issue on
the public tracker. `docs/agents/issue-tracker.md` decides where it goes.

### Triage labels

The label vocabulary of each tracker, and which of those labels exist today. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `CONTEXT.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.
