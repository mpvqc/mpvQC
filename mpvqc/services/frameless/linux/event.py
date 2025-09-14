# Copyright 2023
# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

# Inspired and based on:
#  - https://github.com/zhiyiYo/PyQt-Frameless-Window
#  - https://gitee.com/Virace/pyside6-qml-frameless-window/tree/main


from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtGui import QCursor, QGuiApplication, QWindow


class LinuxEventFilter(QObject):
    """"""

    def __init__(self, window: QWindow, app: QGuiApplication) -> None:
        super().__init__()
        self._border_width = 6

        self._window = window
        self._app = app

    def eventFilter(self, obj, event):  # noqa: C901
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

        if event.type() == QEvent.Type.MouseMove and self._window.windowState() == Qt.WindowState.WindowNoState:
            if edges in {Qt.Edge.LeftEdge | Qt.Edge.TopEdge, Qt.Edge.RightEdge | Qt.Edge.BottomEdge}:
                self._app.setOverrideCursor(Qt.CursorShape.SizeFDiagCursor)
            elif edges in {Qt.Edge.RightEdge | Qt.Edge.TopEdge, Qt.Edge.LeftEdge | Qt.Edge.BottomEdge}:
                self._app.setOverrideCursor(Qt.CursorShape.SizeBDiagCursor)
            elif edges in {Qt.Edge.TopEdge, Qt.Edge.BottomEdge}:
                self._app.setOverrideCursor(Qt.CursorShape.SizeVerCursor)
            elif edges in {Qt.Edge.LeftEdge, Qt.Edge.RightEdge}:
                self._app.setOverrideCursor(Qt.CursorShape.SizeHorCursor)
            else:
                self._app.restoreOverrideCursor()

        if event.type() == QEvent.Type.MouseButtonPress and edges:
            self._window.startSystemResize(edges)
            return True

        return super().eventFilter(obj, event)
