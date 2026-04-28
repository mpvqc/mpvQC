<!--
SPDX-FileCopyrightText: mpvQC developers

SPDX-License-Identifier: MIT
-->

## Dev environment tips

- See [docs/development.md](docs/development.md) for setup and commands; [docs/architecture.md](docs/architecture.md) for codebase orientation.
- Use `just test-qml` for QML tests and `just test-python` for Python tests; neither recompiles resources.
- Run `just prepare-tests` (or the umbrella `just test`) when you've changed production QML, data, or translation files.

## Project structure

- Follows the MVVM architecture pattern; see [docs/architecture.md](docs/architecture.md) for the layer split.

## Coding conventions

- Follow clean code principles.
- Avoid comments unless absolutely necessary, including structural ones like `# region` or `# ---`.
- When writing QML tests, prefer data-driven tests and construct the object being tested using `makeControl` and `createTemporaryObject`. Don't use hard timeouts.
- Use the `signal name(value: type)` notation instead of the old `signal name(type value)` notation in QML signals.

## Commit conventions

- Use the [Conventional Commits](https://www.conventionalcommits.org/) format.

## Documentation

- Update the documentation when working on tasks.
