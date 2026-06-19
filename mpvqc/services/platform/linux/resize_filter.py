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


MARGIN_RESIZE_BAND = 8  # grab band hugging the frame, sitting in the shadow margin


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
    def eventFilter(self, _watched: QObject, event: QEvent) -> bool:  # noqa: C901, PLR0912
        event_type = event.type()

        if event_type != QEvent.Type.MouseButtonPress and event_type != QEvent.Type.MouseMove:  # noqa: PLR1714
            return False

        is_normal_window_state = self._window.windowState() == Qt.WindowState.WindowNoState

        if not is_normal_window_state:
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

        window_width = self._window.width()
        window_height = self._window.height()

        # Content frame is inset by `margin`; the grab band hugs its outside,
        # in the transparent shadow (GTK CSD style).
        band = MARGIN_RESIZE_BAND
        left = margin - band <= x < margin
        right = window_width - margin <= x < window_width - margin + band
        top = margin - band <= y < margin
        bottom = window_height - margin <= y < window_height - margin + band
        is_cursor_in_interior = margin <= x < window_width - margin and margin <= y < window_height - margin

        if is_cursor_in_interior:
            self._clear_cursor_override()
            return False

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

            self._clear_cursor_override()
            if cursor_shape is not None:
                self._app.setOverrideCursor(cursor_shape)
                self._cursor_override_active = True
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
