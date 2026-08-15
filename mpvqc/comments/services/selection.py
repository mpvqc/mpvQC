# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from PySide6.QtCore import QObject, Signal


class SelectionCell(QObject):
    """The selected row and whether it is on screen.

    Service state and the view's at once, merged here: the last write wins.
    """

    row_selected = Signal(int)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._row = -1
        self._row_visible = True

    @property
    def row(self) -> int:
        return self._row

    @property
    def row_visible(self) -> bool:
        return self._row_visible

    def select(self, row: int) -> None:
        if self._row == row:
            return
        self._row = row
        self.row_selected.emit(row)

    def set_row(self, row: int) -> None:
        self._row = row

    def clear_row(self) -> None:
        self._row = -1

    def set_row_visible(self, visible: bool) -> None:
        self._row_visible = visible
