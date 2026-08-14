# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from PySide6.QtCore import Property, QObject, Signal
from PySide6.QtQml import QmlElement, QmlUncreatable

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
@QmlUncreatable("constructed by CommentsService")
class SelectionState(QObject):
    """One-way view state updated from QML to Python."""

    selectedRowChanged = Signal(int)
    selectedRowVisibleChanged = Signal(bool)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._selected_row = -1
        self._selected_row_visible = True

    @Property(int, notify=selectedRowChanged)
    def selectedRow(self) -> int:
        return self._selected_row

    @selectedRow.setter
    def selectedRow(self, value: int) -> None:
        if self._selected_row != value:
            self._selected_row = value
            self.selectedRowChanged.emit(value)

    @Property(bool, notify=selectedRowVisibleChanged)
    def selectedRowVisible(self) -> bool:
        return self._selected_row_visible

    @selectedRowVisible.setter
    def selectedRowVisible(self, value: bool) -> None:
        if self._selected_row_visible != value:
            self._selected_row_visible = value
            self.selectedRowVisibleChanged.emit(value)
