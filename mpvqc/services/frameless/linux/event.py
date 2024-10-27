# Copyright 2023
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

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

    def eventFilter(self, obj, event):
        if event.type() != QEvent.MouseButtonPress and event.type() != QEvent.MouseMove:
            return False

        pos = QCursor.pos() - self._window.position()
        edges = Qt.Edge(0)
        if pos.x() < self._border_width:
            edges |= Qt.LeftEdge
        if pos.x() >= self._window.width() - self._border_width:
            edges |= Qt.RightEdge
        if pos.y() < self._border_width:
            edges |= Qt.TopEdge
        if pos.y() >= self._window.height() - self._border_width:
            edges |= Qt.BottomEdge

        if event.type() == QEvent.MouseMove and self._window.windowState() == Qt.WindowNoState:
            if edges in (Qt.LeftEdge | Qt.TopEdge, Qt.RightEdge | Qt.BottomEdge):
                self._app.setOverrideCursor(Qt.SizeFDiagCursor)
            elif edges in (Qt.RightEdge | Qt.TopEdge, Qt.LeftEdge | Qt.BottomEdge):
                self._app.setOverrideCursor(Qt.SizeBDiagCursor)
            elif edges in (Qt.TopEdge, Qt.BottomEdge):
                self._app.setOverrideCursor(Qt.SizeVerCursor)
            elif edges in (Qt.LeftEdge, Qt.RightEdge):
                self._app.setOverrideCursor(Qt.SizeHorCursor)
            else:
                self._app.restoreOverrideCursor()

        if event.type() == QEvent.MouseButtonPress and edges:
            self._window.startSystemResize(edges)
            return True

        return super().eventFilter(obj, event)
