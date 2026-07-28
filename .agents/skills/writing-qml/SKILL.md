---
name: writing-qml
description: Use when writing or reviewing any .qml file in this repo.
---

# Writing QML

## Imports

Import `QtQuick.Controls` for controls.

Import the Material style under a namespace, and reach its attached properties through it:

```qml
import QtQuick.Controls.Material as M
```

An unnamespaced `import QtQuick.Controls.Material` resolves controls to Material directly and bypasses the MpvqcStyle
overrides, whatever the import order and without a warning. The three files in `qt/qml/MpvqcStyle/` are the only ones
that import it unnamespaced, because they are the overrides.

## Signals

Declare parameters name first:

```qml
signal deleteConfirmed(index: int)
```

The `signal deleteConfirmed(int index)` form is the legacy one. Convert it when you touch a file that still uses it.

## The ladder

Every mpvQC `.qml` file descends the same ladder. A declaration has exactly one rung, and the rungs never
reorder. When you add something to a file that already exists, find its rung and insert it there.

Above the root object

1. Licence header
2. `pragma`
3. Qt imports
4. Project imports

Identity

5. `id`
6. `objectName`

Interface

7. Enums
8. Required properties
9. The view model property, even when it is private
10. Aliases (`property alias`, `readonly property alias`)
11. Readonly value properties (public)
12. Mutable properties (public)
13. Private properties (underscore-prefixed)
14. Signal declarations
15. Inline `component` definitions
16. JavaScript functions

Configuration

17. Own property bindings (`width`, `height`, `anchors`, `color`, `enter`, ...)
18. Attached property bindings (`M.Material.*`, `Layout.*`, `ListView.*`)

Reactions

19. Property change handlers (`onXChanged`) and own signal handlers (`onClicked`, `onAboutToShow`)
20. Attached signal handlers (`Component.onCompleted`, `ListView.onPooled`, `Keys.onPressed`)

Children and motion

21. Child objects, visual or not (`Rectangle`, `RowLayout`, `Shortcut`, `Binding`, `HoverHandler`)
22. `Behavior`
23. States
24. Transitions

Every nested child object descends the same ladder inside its own braces, starting at rung 5.

Put anything unlisted on the rung whose group it belongs to: it declares the interface, configures this
object, reacts to a change, or is a child.

## Test files

A `TestCase` root carries its harness bindings — `name`, `width`, `height`, `visible`, `when` — directly
under the `id`. The rest of the ladder follows from rung 7.

## Done when

- The Material style is imported under a namespace, unless the file is one of the style overrides.
- Signal parameters read name first.
- You have read the file top to bottom and the rung numbers never decrease.
