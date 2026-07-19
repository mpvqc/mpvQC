# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NamedTuple

import pytest
from PySide6.QtCore import QEvent, QPointF, Qt
from PySide6.QtGui import QMouseEvent, QWindow

from mpvqc.services.platform.linux.resize_filter import (
    WindowResizeFilter,
    cursor_shape_for,
    resize_edges_at,
)

WIDTH = 800
HEIGHT = 600
MARGIN = 20

NO_EDGES = Qt.Edge(0)


class EdgeCase(NamedTuple):
    name: str
    x: int
    y: int
    expected: Qt.Edge


EDGE_CASES = [
    EdgeCase("interior center", 400, 300, NO_EDGES),
    EdgeCase("interior boundary just inside content", MARGIN, 300, NO_EDGES),
    EdgeCase("deep shadow outside the band", 5, 5, NO_EDGES),
    EdgeCase("left band outer boundary", 12, 300, Qt.Edge.LeftEdge),
    EdgeCase("left band inner boundary", 19, 300, Qt.Edge.LeftEdge),
    EdgeCase("just outside left band", 11, 300, NO_EDGES),
    EdgeCase("right band outer boundary", 780, 300, Qt.Edge.RightEdge),
    EdgeCase("right band inner boundary", 787, 300, Qt.Edge.RightEdge),
    EdgeCase("just outside right band", 788, 300, NO_EDGES),
    EdgeCase("top band", 400, 12, Qt.Edge.TopEdge),
    EdgeCase("bottom band", 400, 580, Qt.Edge.BottomEdge),
    EdgeCase("just outside bottom band", 400, 588, NO_EDGES),
    EdgeCase("top left corner", 12, 12, Qt.Edge.TopEdge | Qt.Edge.LeftEdge),
    EdgeCase("top right corner", 787, 12, Qt.Edge.TopEdge | Qt.Edge.RightEdge),
    EdgeCase("bottom left corner", 12, 587, Qt.Edge.BottomEdge | Qt.Edge.LeftEdge),
    EdgeCase("bottom right corner", 787, 587, Qt.Edge.BottomEdge | Qt.Edge.RightEdge),
]


@pytest.mark.parametrize("case", EDGE_CASES, ids=lambda case: case.name)
def test_resize_edges(case: EdgeCase) -> None:
    assert resize_edges_at(case.x, case.y, WIDTH, HEIGHT, MARGIN) == case.expected


class CursorCase(NamedTuple):
    name: str
    edges: Qt.Edge
    expected: Qt.CursorShape | None


CURSOR_CASES = [
    CursorCase("top left", Qt.Edge.TopEdge | Qt.Edge.LeftEdge, Qt.CursorShape.SizeFDiagCursor),
    CursorCase("bottom right", Qt.Edge.BottomEdge | Qt.Edge.RightEdge, Qt.CursorShape.SizeFDiagCursor),
    CursorCase("top right", Qt.Edge.TopEdge | Qt.Edge.RightEdge, Qt.CursorShape.SizeBDiagCursor),
    CursorCase("bottom left", Qt.Edge.BottomEdge | Qt.Edge.LeftEdge, Qt.CursorShape.SizeBDiagCursor),
    CursorCase("top", Qt.Edge.TopEdge, Qt.CursorShape.SizeVerCursor),
    CursorCase("bottom", Qt.Edge.BottomEdge, Qt.CursorShape.SizeVerCursor),
    CursorCase("left", Qt.Edge.LeftEdge, Qt.CursorShape.SizeHorCursor),
    CursorCase("right", Qt.Edge.RightEdge, Qt.CursorShape.SizeHorCursor),
    CursorCase("no edges", NO_EDGES, None),
]


@pytest.mark.parametrize("case", CURSOR_CASES, ids=lambda case: case.name)
def test_cursor_shape(case: CursorCase) -> None:
    assert cursor_shape_for(case.edges) == case.expected


@pytest.fixture
def restore_cursor(qt_app):
    yield
    while qt_app.overrideCursor() is not None:
        qt_app.restoreOverrideCursor()


@pytest.fixture
def window(qt_app) -> QWindow:
    window = QWindow()
    window.setPosition(0, 0)
    window.resize(WIDTH, HEIGHT)
    return window


@pytest.fixture
def resize_filter(window, qt_app, restore_cursor) -> WindowResizeFilter:
    event_filter = WindowResizeFilter(window, qt_app)
    event_filter.set_resize_margin(MARGIN)
    return event_filter


def make_mouse_event(event_type: QEvent.Type, x: int, y: int) -> QMouseEvent:
    pos = QPointF(x, y)
    button = Qt.MouseButton.LeftButton if event_type == QEvent.Type.MouseButtonPress else Qt.MouseButton.NoButton
    return QMouseEvent(event_type, pos, pos, pos, button, button, Qt.KeyboardModifier.NoModifier)


def test_move_over_band_sets_resize_cursor(qt_app, resize_filter, window):
    handled = resize_filter.eventFilter(window, make_mouse_event(QEvent.Type.MouseMove, 15, 300))

    assert handled is False
    override = qt_app.overrideCursor()
    assert override is not None
    assert override.shape() == Qt.CursorShape.SizeHorCursor


def test_move_back_to_interior_restores_cursor(qt_app, resize_filter, window):
    resize_filter.eventFilter(window, make_mouse_event(QEvent.Type.MouseMove, 15, 300))
    resize_filter.eventFilter(window, make_mouse_event(QEvent.Type.MouseMove, 400, 300))

    assert qt_app.overrideCursor() is None


def test_press_in_band_starts_system_resize(resize_filter, window):
    handled = resize_filter.eventFilter(window, make_mouse_event(QEvent.Type.MouseButtonPress, 15, 300))

    assert handled is True


def test_press_in_interior_is_ignored(resize_filter, window):
    handled = resize_filter.eventFilter(window, make_mouse_event(QEvent.Type.MouseButtonPress, 400, 300))

    assert handled is False


def test_non_normal_window_state_disables_resize(qt_app, resize_filter, window):
    resize_filter.eventFilter(window, make_mouse_event(QEvent.Type.MouseMove, 15, 300))
    window.setWindowState(Qt.WindowState.WindowMaximized)

    handled = resize_filter.eventFilter(window, make_mouse_event(QEvent.Type.MouseMove, 15, 300))

    assert handled is False
    assert qt_app.overrideCursor() is None


def test_without_margin_nothing_happens(qt_app, window, restore_cursor):
    event_filter = WindowResizeFilter(window, qt_app)

    handled = event_filter.eventFilter(window, make_mouse_event(QEvent.Type.MouseMove, 15, 300))

    assert handled is False
    assert qt_app.overrideCursor() is None
