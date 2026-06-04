<!--
SPDX-FileCopyrightText: mpvQC developers

SPDX-License-Identifier: MIT
-->

## Dev environment tips

## Project structure

- Checkout setup and commands in [docs/development.md](docs/development.md).
- Checkout architecture and how everything fits together in [docs/architecture.md](docs/architecture.md).
- Follow the MVVM architecture pattern; see [docs/architecture.md](docs/architecture.md) for the layer split.

## Project commands

- Checkout common commands by running the command `just`.
- Run linter and formatter via `just fmt`.
- Run QML linter via `just test-qml`.
- Run Python tests via `just test-python ARGS`. `ARGS` is passed over to `pytest`.
- Prepare QML tests via `just prepare-tests` when you've changed production QML, data, or translation files.
- Run specific QML tests via `just test-qml-debug <TARGET>` where `TARGET` is the QML test file to test individual files.
- Run all QML tsts via `just test-qml`.

## Coding

- Follow clean code principles.
- Don't use structural comments like `# region` or `# ---`.
- Avoid comments unless absolutely necessary.
- Use the `signal name(value: type)` notation instead of the old `signal name(type value)` notation in QML signals.
- Import `QtQuick.Controls` for controls. Never import `QtQuick.Controls.Material` unnamespaced: it resolves controls to Material directly and silently bypasses the MpvqcStyle overrides, regardless of import order. For Material attached properties, use `import QtQuick.Controls.Material as M` and reference `M.Material.*`. Only files inside `qt/qml/MpvqcStyle/` import the Material style unnamespaced.
- Follow official QML coding conventions.
- Respect the recommended QML file layout:
  01. id
  02. Required properties
  03. Aliases (property alias / readonly property alias)
  04. Readonly value properties (public)
  05. Mutable properties (public)
  06. Private properties (underscore-prefixed)
  07. Signal declarations
  08. Enums (none here)
  09. JavaScript functions (none here)
  10. Own object property bindings (height, width, anchors, color, etc.)
  11. Attached property bindings (Material. *, ListView.* bindings, Layout.\*)
  12. Property change handlers (onXChanged)
  13. Attached signal handlers (ListView.onPooled/onReused, Component.onCompleted/onDestruction, Keys.onPressed)
  14. Child objects (visual children)
  15. Behaviors
  16. States
  17. Transitions

# Testing

- Prefer data-driven Python tests.
- Prefer testing important areas in the code. Don't go for coverage only.
- Prefer data-driven QML tests and construct the object being tested using `makeControl` / `makeSpy` and `createTemporaryObject`.
- Ensure tests pass on Linux and Windows
- Don't use hard timeouts in QML tests.

## Committing

- Run all pre-commit hooks via `just fmt` to confirm everything's fine before commiting.
- Verify the documentation is up to date before commiting.
- Use the [Conventional Commits](https://www.conventionalcommits.org/) format.
