# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import inject
from PySide6.QtCore import (
    Property,
    QAbstractItemModel,
    QModelIndex,
    QObject,
    QStringListModel,
    Slot,
)
from PySide6.QtQml import QmlElement

from mpvqc.services import CommentTypeValidatorService, SettingsService

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


class CommentTypeList:
    _validator = inject.attr(CommentTypeValidatorService)
    _settings = inject.attr(SettingsService)

    def __init__(self, parent: QObject) -> None:
        self._model = QStringListModel(list(self._settings.comment_types), parent)

    @property
    def qt_model(self) -> QStringListModel:
        return self._model

    def append(self, text: str) -> int:
        position = self._model.rowCount()
        self._model.insertRow(position)
        self._model.setData(self._model.index(position, 0), text)
        return position

    def remove(self, index: int) -> None:
        self._model.removeRow(index)

    def move(self, from_index: int, to_index: int) -> None:
        row_count = self._model.rowCount()
        if from_index == to_index or not (0 <= from_index < row_count and 0 <= to_index < row_count):
            return
        dest = to_index + 1 if to_index > from_index else to_index
        self._model.moveRow(QModelIndex(), from_index, QModelIndex(), dest)

    def validate_new(self, text: str) -> str:
        return self._validator.validate_new_comment_type(text, self._model.stringList()) or ""

    def reset_to_defaults(self) -> None:
        self._model.setStringList(list(self._settings.default_comment_types()))

    def save(self) -> None:
        self._settings.comment_types = self._model.stringList()


@QmlElement
class MpvqcCommentTypesDialogViewModel(QObject):
    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._items = CommentTypeList(self)

    @Property(QAbstractItemModel, constant=True, final=True)
    def commentTypesModel(self) -> QStringListModel:
        return self._items.qt_model

    @Slot(str, result=str)
    def validateNew(self, text: str) -> str:
        return self._items.validate_new(text)

    @Slot(str, result=int)
    def append(self, text: str) -> int:
        return self._items.append(text)

    @Slot(int)
    def remove(self, index: int) -> None:
        self._items.remove(index)

    @Slot(int, int)
    def move(self, from_index: int, to_index: int) -> None:
        self._items.move(from_index, to_index)

    @Slot()
    def save(self) -> None:
        self._items.save()

    @Slot()
    def resetToDefaults(self) -> None:
        self._items.reset_to_defaults()
