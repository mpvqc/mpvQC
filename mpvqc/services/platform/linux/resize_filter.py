# SPDX-FileCopyrightText: zhiyiYo
# SPDX-FileCopyrightText: Virace
# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

# Inspired and based on:
#  - https://github.com/zhiyiYo/PyQt-Frameless-Window
#  - https://gitee.com/Virace/pyside6-qml-frameless-window/tree/main


from __future__ import annotations

from typing import TYPE_CHECKING, cast, override

from PySide6.QtCore import QEvent, QObject, Qt

if TYPE_CHECKING:
    from PySide6.QtGui import QGuiApplication, QMouseEvent, QWindow


MARGIN_RESIZE_BAND = 8  # width of the resize strip just outside the content, inside the shadow margin

_HANDLED_MOUSE_EVENTS = frozenset({QEvent.Type.MouseButtonPress, QEvent.Type.MouseMove})


def resize_edges_at(x: int, y: int, window_width: int, window_height: int, margin: int) -> Qt.Edge:
    # The content is inset by `margin`. The resize strip sits just outside
    # it, in the transparent shadow, like GTK client-side decorations.
    band = MARGIN_RESIZE_BAND
    edges = Qt.Edge(0)
    if margin - band <= x < margin:
        edges |= Qt.Edge.LeftEdge
    if window_width - margin <= x < window_width - margin + band:
        edges |= Qt.Edge.RightEdge
    if margin - band <= y < margin:
        edges |= Qt.Edge.TopEdge
    if window_height - margin <= y < window_height - margin + band:
        edges |= Qt.Edge.BottomEdge
    return edges


def cursor_shape_for(edges: Qt.Edge) -> Qt.CursorShape | None:
    top = bool(edges & Qt.Edge.TopEdge)
    bottom = bool(edges & Qt.Edge.BottomEdge)
    left = bool(edges & Qt.Edge.LeftEdge)
    right = bool(edges & Qt.Edge.RightEdge)

    match (top, bottom, left, right):
        case (True, _, True, _) | (_, True, _, True):
            return Qt.CursorShape.SizeFDiagCursor
        case (True, _, _, True) | (_, True, True, _):
            return Qt.CursorShape.SizeBDiagCursor
        case (True, _, _, _) | (_, True, _, _):
            return Qt.CursorShape.SizeVerCursor
        case (_, _, True, _) | (_, _, _, True):
            return Qt.CursorShape.SizeHorCursor
        case _:
            return None


class WindowResizeFilter(QObject):
    def __init__(self, window: QWindow, app: QGuiApplication) -> None:
        super().__init__()
        self._window = window
        self._app = app
        self._cursor_override_active = False
        self._resize_margin = 0
        window.windowStateChanged.connect(self._clear_cursor_override)

    def set_resize_margin(self, margin: int) -> None:
        self._resize_margin = margin

    def _clear_cursor_override(self) -> None:
        if self._cursor_override_active:
            self._app.restoreOverrideCursor()
            self._cursor_override_active = False

    @override
    def eventFilter(self, _watched: QObject, event: QEvent) -> bool:
        event_type = event.type()

        if event_type not in _HANDLED_MOUSE_EVENTS:
            return False

        if self._window.windowState() != Qt.WindowState.WindowNoState:
            self._clear_cursor_override()
            return False

        margin = self._resize_margin
        if not margin:
            self._clear_cursor_override()
            return False

        global_pos = cast("QMouseEvent", event).globalPosition()
        window_pos = self._window.position()
        x = int(global_pos.x() - window_pos.x())
        y = int(global_pos.y() - window_pos.y())

        edges = resize_edges_at(x, y, self._window.width(), self._window.height(), margin)

        if event_type == QEvent.Type.MouseMove:
            self._clear_cursor_override()
            if (cursor_shape := cursor_shape_for(edges)) is not None:
                self._app.setOverrideCursor(cursor_shape)
                self._cursor_override_active = True
            return False

        if edges:
            self._window.startSystemResize(edges)
            return True

        self._clear_cursor_override()
        return False
