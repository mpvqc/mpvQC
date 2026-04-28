<!--
SPDX-FileCopyrightText: mpvQC developers

SPDX-License-Identifier: MIT
-->

# Development

This guide covers what you need to set up the project, run it locally, and contribute changes. For a high-level tour of how the codebase fits together, see [architecture.md](architecture.md).

## Prerequisites

- [Python 3.13 or later](https://www.python.org/downloads/)
- [uv](https://github.com/astral-sh/uv)
- [just](https://github.com/casey/just)
- libmpv
  - **Linux:** install via your package manager
  - **Windows:** download [libmpv (mpv-dev-x86_64)](https://github.com/shinchiro/mpv-winbuild-cmake/releases), extract it, and place the `libmpv-*.dll` in the repository root
- **Windows only:** [Git Bash](https://git-scm.com/downloads) — `just` recipes assume a POSIX shell

## First-time setup

Clone the repository, then from the repo root:

```shell
just init           # install dependencies and configure dev tooling
just build-develop  # compile QML, data, and translations into rc_project.py
uv run main.py      # launch the application
```

Whenever you change files in `data/`, `i18n/`, or `qt/qml/`, re-run `just build-develop` so the resource bundle is regenerated. Configure your IDE to run it before launching the app.

## Daily commands

| Recipe                        | What it does                                                                     |
| ----------------------------- | -------------------------------------------------------------------------------- |
| `just test`                   | Run Python tests and QML tests (recompiles resources first)                      |
| `just prepare-tests`          | Recompile resources for testing (runs `build-develop` then stages it)            |
| `just test-python`            | Run Python tests only — does **not** recompile                                   |
| `just test-qml`               | Run QML tests only — does **not** recompile                                      |
| `just test-qml-debug TARGET`  | Run a single QML test file matched by name (useful for iteration)                |
| `just fmt`                    | Format Python, QML, JSON, TOML, YAML, Markdown                                   |
| `just lint-python`            | Run pyrefly type checker                                                         |
| `just lint-qml`               | Run pyside6-qmllint                                                              |
| `just build-develop`          | Recompile QML/data/i18n into the resource bundle                                 |
| `just clean`                  | Remove all generated files                                                       |
| `just add-translation LOCALE` | Start a new translation (see [internationalization.md](internationalization.md)) |
| `just update-translations`    | Refresh existing `.ts` files from current source strings                         |

After changing production QML, data, or translation files, run `just prepare-tests` (or `just test`, which invokes it) so the resource bundle test runners load is up to date. When iterating on test code only, `just test-qml` and `just test-python` run directly without recompiling.

## Project layout

| Path         | Contents                                                                                    |
| ------------ | ------------------------------------------------------------------------------------------- |
| `mpvqc/`     | Python: services (business logic), viewmodels (Qt-exposed glue), application bootstrap      |
| `qt/qml/`    | QML views, components, dialogs, message boxes, file dialogs, plus colocated unit tests      |
| `test/`      | Python tests (pytest) — services and viewmodels in isolation                                |
| `testqml/`   | Test harness for QML integration tests: bridge, fixtures, injection overrides               |
| `data/`      | Fonts, icons, default `mpv.conf` / `input.conf`, themes, `build-info.toml`                  |
| `i18n/`      | Translations as `.ts` source files; `.qm` binaries are generated                            |
| `build-aux/` | Generator scripts: `pyproject.toml` files-list updater, qrc generator, lupdate project file |
| `docs/`      | These docs                                                                                  |

## See also

- [architecture.md](architecture.md) — high-level overview of how Python, QML, and the test harness fit together
- [configuration.md](configuration.md) — runtime environment variables
- [internationalization.md](internationalization.md) — adding and updating translations
- [releasing.md](releasing.md) — release checklist
