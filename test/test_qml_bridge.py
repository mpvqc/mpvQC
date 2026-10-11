# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Callable
from typing import NamedTuple

import pytest
from PySide6.QtCore import QUrl
from PySide6.QtQml import QQmlComponent, QQmlEngine
from PySide6.QtQuick import QQuickItem

from testqml.bridge import MpvqcTestBridge


@pytest.fixture(autouse=True)
def qt_app_must_be_running(qt_app):
    pass


@pytest.fixture
def bridge() -> MpvqcTestBridge:
    return MpvqcTestBridge()


@pytest.fixture
def root() -> QQuickItem:
    return QQuickItem()


def make_item(parent: QQuickItem, *, y: float, height: float) -> QQuickItem:
    item = QQuickItem(parent)
    item.setParentItem(parent)
    item.setY(y)
    item.setHeight(height)
    return item


@pytest.fixture
def make_view() -> Callable[[float], QQuickItem]:
    engine = QQmlEngine()

    def _make(content_height: float) -> QQuickItem:
        component = QQmlComponent(engine, engine)
        component.setData(
            f"import QtQuick\nFlickable {{ width: 100; height: 100; contentHeight: {content_height} }}".encode(),
            QUrl(),
        )
        view = component.create()
        assert isinstance(view, QQuickItem), component.errorString()
        view.setParent(engine)
        return view

    return _make


def test_pixel_tolerance_is_one_pixel(bridge):
    assert bridge.pixelTolerance == 1


class NearCase(NamedTuple):
    actual: float
    near: bool


@pytest.mark.parametrize(
    "case",
    [
        NearCase(actual=571.59, near=True),
        NearCase(actual=571, near=True),
        NearCase(actual=570.99, near=False),
    ],
)
def test_nearly_equal_allows_one_pixel(bridge, case):
    assert bridge.nearlyEqual(case.actual, 572) == case.near


class InsideCase(NamedTuple):
    y: float
    inside: bool


@pytest.mark.parametrize(
    "case",
    [
        InsideCase(y=-1, inside=True),
        InsideCase(y=-1.01, inside=False),
        InsideCase(y=81, inside=True),
        InsideCase(y=81.01, inside=False),
    ],
)
def test_vertically_inside_allows_one_pixel(bridge, root, case):
    viewport = make_item(root, y=50, height=100)
    item = make_item(root, y=50 + case.y, height=20)

    assert bridge.verticallyInside(item, viewport) == case.inside


class ScrollCase(NamedTuple):
    content_y: float
    at_start: bool
    at_end: bool


@pytest.mark.parametrize(
    "case",
    [
        ScrollCase(content_y=1, at_start=True, at_end=False),
        ScrollCase(content_y=1.01, at_start=False, at_end=False),
        ScrollCase(content_y=571, at_start=False, at_end=True),
        ScrollCase(content_y=570.5, at_start=False, at_end=False),
    ],
)
def test_scroll_bounds_are_read_from_the_view(bridge, make_view, case):
    view = make_view(671.59)
    view.setProperty("contentY", case.content_y)

    assert bridge.atScrollStart(view) == case.at_start
    assert bridge.atScrollEnd(view) == case.at_end


def test_short_content_starts_and_ends_at_the_top(bridge, make_view):
    view = make_view(50)

    assert bridge.atScrollStart(view)
    assert bridge.atScrollEnd(view)


class StackCase(NamedTuple):
    tops: list[float]
    stacked: bool


@pytest.mark.parametrize(
    "case",
    [
        StackCase(tops=[0, 41, 81], stacked=True),
        StackCase(tops=[0, 41.01, 81.01], stacked=False),
        StackCase(tops=[0, 38.99, 78.99], stacked=False),
    ],
)
def test_stacked_without_gaps_allows_one_pixel(bridge, root, case):
    items = [make_item(root, y=top, height=40) for top in case.tops]

    assert bridge.stackedWithoutGaps(items) == case.stacked


def test_vertical_gap_compares_items_in_different_parents(bridge, root):
    upper = make_item(root, y=10, height=40)
    container = make_item(root, y=30, height=200)
    lower = make_item(container, y=35.5, height=40)

    assert bridge.verticalGap(upper, lower) == pytest.approx(15.5)
