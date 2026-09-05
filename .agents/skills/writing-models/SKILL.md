---
name: writing-models
description: Qt list model conventions. Use when creating, reviewing, or modifying a Qt list model.
---

# Writing models

## Reach for Qt first

Use Qt's own model before subclassing one. Bare strings with no custom roles belong in a `QStringListModel` wrapped
by a plain helper, as in `CommentTypeList`.

## Construction and placement

A model that builds its own rows and takes no input is a `@QmlElement`; QML constructs it. Python constructs every
other model, and a view model publishes it through:

```python
@Property(QAbstractItemModel, constant=True, final=True)
```

A registered model that Python constructs also carries `@QmlUncreatable`.

Put a model in its feature package's `models/` role; every area is a slice, so there is no shared models package.

## List contract

`rowCount` has this signature and returns zero for a valid parent:

```python
def rowCount(self, parent: QModelIndex | QPersistentModelIndex | None = None) -> int:
    if parent is not None and parent.isValid():
        return 0
    return len(self._items)
```

The `None` default is load-bearing. View models, services, tests, and the comment `Store` protocol call `rowCount()`
without an argument, while Qt passes an invalid index.

In `data()`, bind the sequence about to be indexed to a local, check the index against that local's length, then index
the same local. Never guard through `rowCount()`. The models that still guard that way predate this rule; don't copy
them.

## Roles

Declare model-owned roles as class attributes, `XxxRole = Qt.ItemDataRole.UserRole + N`, and match them as
`case self.XxxRole`. Move roles to an `IntEnum` in the slice's `services/` only when code outside the model must name
them. The comment `Role` enum is the example: undo steps name the role they change.

`roleNames()` names every role the class declares. Keep the mapping complete even when one role, such as shortcuts'
`SearchTextRole`, exists for Python rather than a QML binding.

## Row storage

Store the upstream type directly when it already carries the row data, as `ErrorsModel` stores `RejectedDocument` and
`MpvqcDependencyModel` stores `Dependency`.

Define a private entry type only when the row adds data absent from the upstream type:

- `_SubtitleEntry` adds the checked flag.
- `_VideoEntry` makes the path optional, so the skip sentinel fits in a row.
- `_TemplateEntry` carries the mapped URL.

An entry type is a frozen dataclass. Prefer `slots=True`, but it is not required.

## Backend and proxy

Split a model when QML needs sorted or filtered rows. A `QAbstractListModel` backend owns the rows and roles;
`QSortFilterProxyModel` owns ordering, filtering, and every QML-facing property. The language and shortcuts models are
the examples.

Only the proxy is a `@QmlElement` and carries the `Mpvqc` name. The backend goes without the prefix, because the
prefix marks exactly the classes QML can name as a type.

`CommentStore` is the exception.

## Extra properties

Expose a property only for information a role cannot carry. `MpvqcExportTemplateModel.count` exists because QML
cannot call `rowCount()`.

## Signalling

Every `dataChanged` emission carries an explicit role list.

Emit one row at a time when the old values are already available, as `MpvqcColorSchemePreferenceModel` does. A span is
valid when they are not, as in `SubtitlesModel.set_all_checked`.

Wrap mutations in their Qt pair:

- Insert with `beginInsertRows` and `endInsertRows`.
- Remove with `beginRemoveRows` and `endRemoveRows`.
- Move with `beginMoveRows` and `endMoveRows`.
- Replace the whole sequence with `beginResetModel` and `endResetModel`.

A model that computes rows instead of storing them derives the structural and data signals by hand.
`MpvqcAccentColorModel.set_preference` is the worked example.

## Service seam

A service reaches a model through a structural `Protocol` declared in the slice's `services/` and bound with
`inject`. `Store` and `CommentStore` are the example. The protocol describes the Python-facing shape, including
`rowCount()` without an argument; the service imports and types against that protocol, never against the model class,
which `slice-imports` rejects.

## Declaration ladder

A model file descends these rungs. Every declaration has exactly one rung:

1. Licence header
2. `QML_IMPORT_NAME` and `QML_IMPORT_MAJOR_VERSION`
3. Module-level types and constants: entry dataclasses and sentinels
4. Decorators, then the class
5. `inject.attr` class attributes
6. Role constants
7. Signal declarations
8. `__init__`, then private helpers reached only by `__init__`, directly or through each other
9. Qt `@Property` and Python `@property`
10. Overrides in the parent class's declaration order
11. Everything else

Rung 10 puts `rowCount` before `data` before `roleNames`, which is `QAbstractItemModel`'s own order and already what
every model writes. A private helper also called by a signal handler or public method belongs at rung 11, not rung 8.

## Tests

A model that changes after construction has a test that installs Qt's invariant checker:

```python
QAbstractItemModelTester(model, QAbstractItemModelTester.FailureReportingMode.Fatal, model)
```

`CommentStore`, `MpvqcAccentColorModel` and `MpvqcColorSchemePreferenceModel` have one. A model whose rows are fixed at
construction sits outside the rule.

## Done when

- Bare strings with no roles sit in a `QStringListModel` behind a plain helper, not in a subclass.
- Construction, registration, naming, and placement follow the model's ownership boundary.
- `rowCount`, `data`, roles, row storage, and extra properties follow the list contract.
- A sorted or filtered QML model has a backend and proxy with one responsibility each.
- Every structural change runs through its begin/end pair, and every `dataChanged` carries its role list.
- Every model that changes after construction has a fatal `QAbstractItemModelTester`, and every mutator has a test
  asserting the exact signal set it emits.
- Every declaration occupies exactly one ladder rung.
