# SPDX-FileCopyrightText: zhiyiYo
# SPDX-FileCopyrightText: Virace
# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

# Inspired and based on:
#  - https://github.com/zhiyiYo/PyQt-Frameless-Window
#  - https://gitee.com/Virace/pyside6-qml-frameless-window/tree/main


from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtGui import QCursor

if TYPE_CHECKING:
    from PySide6.QtGui import QGuiApplication, QWindow


class LinuxEventFilter(QObject):
    def __init__(self, window: QWindow, app: QGuiApplication) -> None:
        super().__init__()
        self._window = window
        self._app = app
        self._cursor_override_active = False
        self._border_width = 6

    def eventFilter(self, _watched: QObject, event: QEvent) -> bool:  # noqa: C901, PLR0912, PLR0915
        event_type = event.type()

        if event_type != QEvent.Type.MouseButtonPress and event_type != QEvent.Type.MouseMove:  # noqa: PLR1714
            return False

        is_normal_window_state = self._window.windowState() == Qt.WindowState.WindowNoState

        if not is_normal_window_state:
            if event_type == QEvent.Type.MouseMove and self._cursor_override_active:
                self._app.restoreOverrideCursor()
                self._cursor_override_active = False
            return False

        cursor_pos = QCursor.pos()
        window_pos = self._window.position()
        x = cursor_pos.x() - window_pos.x()
        y = cursor_pos.y() - window_pos.y()

        window_width = self._window.width()
        window_height = self._window.height()
        border_width = self._border_width

        is_cursor_in_interior = (
            border_width <= x < window_width - border_width and border_width <= y < window_height - border_width
        )

        if is_cursor_in_interior:
            if event_type == QEvent.Type.MouseMove and self._cursor_override_active:
                self._app.restoreOverrideCursor()
                self._cursor_override_active = False
            return False

        left = x < border_width
        right = x >= window_width - border_width
        top = y < border_width
        bottom = y >= window_height - border_width

        if event_type == QEvent.Type.MouseMove:
            match (top, bottom, left, right):
                case (True, _, True, _) | (_, True, _, True):
                    cursor_shape = Qt.CursorShape.SizeFDiagCursor
                case (True, _, _, True) | (_, True, True, _):
                    cursor_shape = Qt.CursorShape.SizeBDiagCursor
                case (True, _, _, _) | (_, True, _, _):
                    cursor_shape = Qt.CursorShape.SizeVerCursor
                case (_, _, True, _) | (_, _, _, True):
                    cursor_shape = Qt.CursorShape.SizeHorCursor
                case _:
                    cursor_shape = None

            if cursor_shape:
                if self._cursor_override_active:
                    self._app.restoreOverrideCursor()
                self._app.setOverrideCursor(cursor_shape)
                self._cursor_override_active = True
            elif self._cursor_override_active:
                self._app.restoreOverrideCursor()
                self._cursor_override_active = False
        else:  # MouseButtonPress
            edges = Qt.Edge(0)
            if left:
                edges |= Qt.Edge.LeftEdge
            if right:
                edges |= Qt.Edge.RightEdge
            if top:
                edges |= Qt.Edge.TopEdge
            if bottom:
                edges |= Qt.Edge.BottomEdge

            if edges:
                self._window.startSystemResize(edges)
                return True

        return False
