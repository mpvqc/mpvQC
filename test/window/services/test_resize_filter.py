# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NamedTuple

import pytest
from PySide6.QtCore import QEvent, QPointF, Qt
from PySide6.QtGui import QMouseEvent, QWindow

from mpvqc.window.services.linux import (
    WindowResizeFilter,
    cursor_shape_for,
    resize_edges_at,
)

WIDTH = 800
HEIGHT = 600
DROP_SHADOW_MARGIN = 20

NO_EDGES = Qt.Edge(0)


class EdgeCase(NamedTuple):
    name: str
    x: int
    y: int
    expected: Qt.Edge


EDGE_CASES = [
    EdgeCase(name="interior center", x=400, y=300, expected=NO_EDGES),
    EdgeCase(name="interior boundary just inside content", x=DROP_SHADOW_MARGIN, y=300, expected=NO_EDGES),
    EdgeCase(name="deep shadow outside the band", x=5, y=5, expected=NO_EDGES),
    EdgeCase(name="left band outer boundary", x=12, y=300, expected=Qt.Edge.LeftEdge),
    EdgeCase(name="left band inner boundary", x=19, y=300, expected=Qt.Edge.LeftEdge),
    EdgeCase(name="just outside left band", x=11, y=300, expected=NO_EDGES),
    EdgeCase(name="right band outer boundary", x=780, y=300, expected=Qt.Edge.RightEdge),
    EdgeCase(name="right band inner boundary", x=787, y=300, expected=Qt.Edge.RightEdge),
    EdgeCase(name="just outside right band", x=788, y=300, expected=NO_EDGES),
    EdgeCase(name="top band", x=400, y=12, expected=Qt.Edge.TopEdge),
    EdgeCase(name="bottom band", x=400, y=580, expected=Qt.Edge.BottomEdge),
    EdgeCase(name="just outside bottom band", x=400, y=588, expected=NO_EDGES),
    EdgeCase(name="top left corner", x=12, y=12, expected=Qt.Edge.TopEdge | Qt.Edge.LeftEdge),
    EdgeCase(name="top right corner", x=787, y=12, expected=Qt.Edge.TopEdge | Qt.Edge.RightEdge),
    EdgeCase(name="bottom left corner", x=12, y=587, expected=Qt.Edge.BottomEdge | Qt.Edge.LeftEdge),
    EdgeCase(name="bottom right corner", x=787, y=587, expected=Qt.Edge.BottomEdge | Qt.Edge.RightEdge),
]


@pytest.mark.parametrize("case", EDGE_CASES, ids=lambda case: case.name)
def test_resize_edges(case: EdgeCase) -> None:
    assert resize_edges_at(case.x, case.y, WIDTH, HEIGHT, DROP_SHADOW_MARGIN) == case.expected


class CursorCase(NamedTuple):
    name: str
    edges: Qt.Edge
    expected: Qt.CursorShape | None


CURSOR_CASES = [
    CursorCase(
        name="top left",
        edges=Qt.Edge.TopEdge | Qt.Edge.LeftEdge,
        expected=Qt.CursorShape.SizeFDiagCursor,
    ),
    CursorCase(
        name="bottom right",
        edges=Qt.Edge.BottomEdge | Qt.Edge.RightEdge,
        expected=Qt.CursorShape.SizeFDiagCursor,
    ),
    CursorCase(
        name="top right",
        edges=Qt.Edge.TopEdge | Qt.Edge.RightEdge,
        expected=Qt.CursorShape.SizeBDiagCursor,
    ),
    CursorCase(
        name="bottom left",
        edges=Qt.Edge.BottomEdge | Qt.Edge.LeftEdge,
        expected=Qt.CursorShape.SizeBDiagCursor,
    ),
    CursorCase(
        name="top",
        edges=Qt.Edge.TopEdge,
        expected=Qt.CursorShape.SizeVerCursor,
    ),
    CursorCase(
        name="bottom",
        edges=Qt.Edge.BottomEdge,
        expected=Qt.CursorShape.SizeVerCursor,
    ),
    CursorCase(
        name="left",
        edges=Qt.Edge.LeftEdge,
        expected=Qt.CursorShape.SizeHorCursor,
    ),
    CursorCase(
        name="right",
        edges=Qt.Edge.RightEdge,
        expected=Qt.CursorShape.SizeHorCursor,
    ),
    CursorCase(
        name="no edges",
        edges=NO_EDGES,
        expected=None,
    ),
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
    event_filter.set_drop_shadow_margin(DROP_SHADOW_MARGIN)
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
