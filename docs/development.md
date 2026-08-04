# Development

How to set the project up, run it locally, and contribute changes. For how the codebase fits together, see
[architecture.md](architecture.md).

## Prerequisites

- [Python 3.13](https://www.python.org/downloads/)
- [uv](https://github.com/astral-sh/uv)
- [just](https://github.com/casey/just)
- libmpv
  - **Linux:** install via your package manager
  - **Windows:** download [libmpv (mpv-dev-x86_64)](https://github.com/shinchiro/mpv-winbuild-cmake/releases), extract
    it, and place the `libmpv-*.dll` in the repository root
- **Windows only:** [Git Bash](https://git-scm.com/downloads) (the `just` recipes assume a POSIX shell)

## First-time setup

Clone the repository, then from the repo root:

```shell
just init           # install dependencies and configure dev tooling
just build-develop  # regenerate project.rcc from QML, data, and translations
uv run main.py      # launch the application
```

Whenever you change files in `data/`, `i18n/`, or `qt/qml/`, re-run `just build-develop` to regenerate the resource
bundle. Configure your IDE to run it before launching the app. For tests, `just prepare-tests` stages that bundle,
`just test-python` and `just test-qml` do not, and they pass against a stale bundle without warning.

## Daily commands

| Recipe                              | What it does                                                                                                          |
| ----------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `just test`                         | Run Python tests and QML tests (recompiles resources first)                                                           |
| `just prepare-tests`                | Recompile resources for testing (runs `build-develop` then stages it)                                                 |
| `just test-python [ARGS]`           | Run pytest (does **not** recompile). `ARGS` replaces the default paths `build-aux test`                               |
| `just test-qml [JOBS]`              | Run QML tests only (does **not** recompile), one process per file                                                     |
| `just test-qml-debug TARGET`        | Run a single QML test file matched by name (useful for iteration)                                                     |
| `just fmt`                          | Format and lint Python, QML, JSON, TOML, YAML, Markdown; also type-checks (pyrefly) and lints license headers (reuse) |
| `just lint-qml`                     | Run pyside6-qmllint (recompiles resources first)                                                                      |
| `just build-develop`                | Regenerate `project.rcc` from `qt/qml/`, `data/`, and `i18n/`                                                         |
| `just clean`                        | Remove all generated files                                                                                            |
| `just update-python-dependencies`   | Upgrade Python dependencies and refresh the versions recorded in `data/build-info.toml`                               |
| `just update-git-hook-dependencies` | Upgrade the pinned git hook revisions                                                                                 |
| `just add-translation LOCALE`       | Start a new translation (see [internationalization.md](internationalization.md))                                      |
| `just update-translations`          | Refresh existing `.ts` files from current source strings                                                              |

## Project layout

| Path         | Contents                                                                                                                                                               |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `mpvqc/`     | Python: feature packages like `appearance/`, the layer packages (`services/`, `viewmodels/`, `models/`, `views/`, `dialogs/`, `enums/`), and the application bootstrap |
| `qt/qml/`    | QML modules following a reverse-DNS layout, with unit tests colocated alongside sources                                                                                |
| `test/`      | Python tests (pytest): services and view models in isolation                                                                                                           |
| `testqml/`   | Test harness for QML integration tests: bridge, fixtures, injection overrides                                                                                          |
| `data/`      | Fonts, icons, default `mpv.conf` / `input.conf`, the palette catalog, `build-info.toml`                                                                                |
| `i18n/`      | Translations as `.ts` source files. The `.qm` binaries are generated                                                                                                   |
| `build-aux/` | Generator and build-helper scripts, plus a `Justfile` of their own                                                                                                     |

## Conventions

- Prefer code the tooling can verify. Example: use a closure instead of `functools.partial`
- Two Python files holding `@QmlElement` classes must not share a file name. The build writes one `.qmltypes` per
  source file into one flat directory, named after the file, so same-named files overwrite each other and the QML
  linter silently loses the types of whichever lost the race.

## See also

- [architecture.md](architecture.md): high-level overview of how Python, QML, and the test harness fit together
- [configuration.md](configuration.md): runtime environment variables
- [internationalization.md](internationalization.md): adding and updating translations
- [releasing.md](releasing.md): release checklist
