# Development

This guide covers local setup and the normal development loop. See [architecture.md](architecture.md) for the codebase
shape.

## Prerequisites

- The Python version required by `pyproject.toml`
- [uv](https://github.com/astral-sh/uv)
- [just](https://github.com/casey/just)
- libmpv
  - **Linux:** install libmpv through your package manager
  - **Windows:** download [libmpv](https://github.com/shinchiro/mpv-winbuild-cmake/releases) and place its DLL in the
    repository root
- **Windows only:** [Git Bash](https://git-scm.com/downloads), because the recipes use a POSIX shell

Linux development and testing target Wayland.

## Setup

From the repository root:

```shell
just init
just build-develop
uv run main.py
```

The default setup enables portable mode, so local application state stays inside the repository. Running `just init`
again refreshes generated development configuration and seed files.

`just build-develop` regenerates the PySide project file list, Python QML type metadata, translations, and the resource
bundle. Run it after changing runtime assets or QML-facing Python types, and after adding or removing files included in
the PySide project. Never edit the generated file table in `pyproject.toml` by hand.

## Development loop

Run `just` to see the current recipes and their descriptions.

- `just test` rebuilds resources and runs the full Python and QML test suites.
- `just test-python` and `just test-qml` run one side without rebuilding resources.
- `just prepare-tests` rebuilds and stages resources before targeted test runs.
- `just fmt` formats the repository and runs Python, type, and license checks.
- `just lint-qml` rebuilds resources and runs semantic QML checks.

Direct test commands can pass against a stale resource bundle. Run `just prepare-tests` first after changing QML,
translations, or bundled data.

Maintenance recipes live beside the part of the repository they maintain. Run `just` there to discover them instead
of copying their names into this guide.

## Conventions

- Prefer code the tooling can verify. Use a closure instead of `functools.partial`.
- Two Python files holding `@QmlElement` classes must not share a file name. Generated QML type metadata is flat, so
  one file would overwrite the other and hide types from the QML linter.

## See also

- [Architecture](architecture.md)
- [Configuration](configuration.md)
- [Internationalization](internationalization.md)
- [Releasing](releasing.md)
