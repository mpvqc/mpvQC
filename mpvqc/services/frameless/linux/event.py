# SPDX-FileCopyrightText: zhiyiYo
# SPDX-FileCopyrightText: Virace
# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

# Inspired and based on:
#  - https://github.com/zhiyiYo/PyQt-Frameless-Window
#  - https://gitee.com/Virace/pyside6-qml-frameless-window/tree/main


from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtGui import QCursor, QGuiApplication, QWindow


class LinuxEventFilter(QObject):
    def __init__(self, window: QWindow, app: QGuiApplication) -> None:
        super().__init__()
        self._window = window
        self._app = app
        self._cursor_override_active = False
        self._border_width = 6

    def eventFilter(self, obj, event):
        if event.type() != QEvent.Type.MouseButtonPress and event.type() != QEvent.Type.MouseMove:
            return False

        pos = QCursor.pos() - self._window.position()
        edges = Qt.Edge(0)
        if pos.x() < self._border_width:
            edges |= Qt.Edge.LeftEdge
        if pos.x() >= self._window.width() - self._border_width:
            edges |= Qt.Edge.RightEdge
        if pos.y() < self._border_width:
            edges |= Qt.Edge.TopEdge
        if pos.y() >= self._window.height() - self._border_width:
            edges |= Qt.Edge.BottomEdge

        no_window_state = self._window.windowState() == Qt.WindowState.WindowNoState

        if event.type() == QEvent.Type.MouseMove and no_window_state:
            self._update_cursor_for_edges(edges)

        if event.type() == QEvent.Type.MouseButtonPress and no_window_state and edges:
            self._window.startSystemResize(edges)
            return True

        return super().eventFilter(obj, event)

    def _update_cursor_for_edges(self, edges: Qt.Edge) -> None:
        cursor_shape = None
        if edges in {Qt.Edge.LeftEdge | Qt.Edge.TopEdge, Qt.Edge.RightEdge | Qt.Edge.BottomEdge}:
            cursor_shape = Qt.CursorShape.SizeFDiagCursor
        elif edges in {Qt.Edge.RightEdge | Qt.Edge.TopEdge, Qt.Edge.LeftEdge | Qt.Edge.BottomEdge}:
            cursor_shape = Qt.CursorShape.SizeBDiagCursor
        elif edges in {Qt.Edge.TopEdge, Qt.Edge.BottomEdge}:
            cursor_shape = Qt.CursorShape.SizeVerCursor
        elif edges in {Qt.Edge.LeftEdge, Qt.Edge.RightEdge}:
            cursor_shape = Qt.CursorShape.SizeHorCursor

        if cursor_shape:
            if self._cursor_override_active:
                self._app.restoreOverrideCursor()
            self._app.setOverrideCursor(cursor_shape)
            self._cursor_override_active = True

        elif self._cursor_override_active:
            self._app.restoreOverrideCursor()
            self._cursor_override_active = False
