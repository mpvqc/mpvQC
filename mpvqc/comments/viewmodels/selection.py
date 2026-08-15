# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import Property, QObject
from PySide6.QtQml import QmlElement, QmlUncreatable

if TYPE_CHECKING:
    from mpvqc.comments.services import SelectionCell

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
@QmlUncreatable("constructed by MpvqcCommentTableViewModel")
class MpvqcCommentSelectionViewModel(QObject):
    def __init__(self, cell: SelectionCell, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._cell = cell

    @Property(int)
    def selectedRow(self) -> int:
        return self._cell.row

    @selectedRow.setter
    def selectedRow(self, value: int) -> None:
        self._cell.select(value)

    @Property(bool)
    def selectedRowVisible(self) -> bool:
        return self._cell.row_visible

    @selectedRowVisible.setter
    def selectedRowVisible(self, value: bool) -> None:
        self._cell.set_row_visible(value)
