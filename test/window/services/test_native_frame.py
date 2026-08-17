# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import ast
from dataclasses import dataclass, field
from pathlib import Path
from typing import NamedTuple

import pytest

from mpvqc.window.services import (
    AppBarEdge,
    ClientRect,
    MonitorGeometry,
    MonitorRect,
    ProposedRect,
    WindowRect,
    WorkArea,
    handle_non_client_calculate_size,
    handle_non_client_hit_test,
    overhangs,
    read_hit_test_point,
    reserve_auto_hide_taskbar_strip,
)

DECISIONS = Path(__file__).resolve().parents[3] / "mpvqc" / "window" / "services" / "native_frame.py"

HTTOP = 12
HTTOPLEFT = 13
HTTOPRIGHT = 14
WVR_REDRAW = 0x0300

MONITOR = MonitorRect((0, 0, 1920, 1080))
WORK_AREA = WorkArea((0, 0, 1920, 1040))
GEOMETRY = MonitorGeometry(monitor_rect=MONITOR, work_area=WORK_AREA)

WINDOW = WindowRect((100, 100, 900, 700))
FULL_MONITOR_PROPOSAL = ProposedRect((0, 0, 1920, 1080))
BAND = 8


def pack_point(x: int, y: int) -> int:
    return ((y & 0xFFFF) << 16) | (x & 0xFFFF)


@dataclass
class RecordingHitTestProbe:
    is_maximized: bool = False
    rect: WindowRect | None = WINDOW
    monitor_rect: MonitorRect | None = MONITOR
    cursor: tuple[int, int] = (0, 0)
    band: int = BAND
    asked: list[tuple[str, object]] = field(default_factory=list)

    @property
    def questions(self) -> list[str]:
        return [question for question, _ in self.asked]

    def maximized(self) -> bool:
        self.asked.append(("maximized", None))
        return self.is_maximized

    def window_rect(self) -> WindowRect | None:
        self.asked.append(("window_rect", None))
        return self.rect

    def monitor_rect_for(self, rect: WindowRect) -> MonitorRect | None:
        self.asked.append(("monitor_rect_for", rect))
        return self.monitor_rect

    def cursor_point(self) -> tuple[int, int]:
        self.asked.append(("cursor_point", None))
        return self.cursor

    def resize_band(self) -> int:
        self.asked.append(("resize_band", None))
        return self.band


@dataclass
class RecordingCalcSizeProbe:
    proposed: ProposedRect = FULL_MONITOR_PROPOSAL
    geometry: MonitorGeometry | None = GEOMETRY
    is_maximized: bool = False
    auto_hide: bool = False
    edge: AppBarEdge | None = None
    asked: list[tuple[str, object]] = field(default_factory=list)

    @property
    def questions(self) -> list[str]:
        return [question for question, _ in self.asked]

    def proposed_rect(self) -> ProposedRect:
        self.asked.append(("proposed_rect", None))
        return self.proposed

    def monitor_geometry_for(self, rect: ProposedRect) -> MonitorGeometry | None:
        self.asked.append(("monitor_geometry_for", rect))
        return self.geometry

    def maximized(self) -> bool:
        self.asked.append(("maximized", None))
        return self.is_maximized

    def auto_hide_enabled(self) -> bool:
        self.asked.append(("auto_hide_enabled", None))
        return self.auto_hide

    def auto_hide_edge(self, monitor_rect: MonitorRect) -> AppBarEdge | None:
        self.asked.append(("auto_hide_edge", monitor_rect))
        return self.edge


class PointCase(NamedTuple):
    name: str
    l_param: int
    expected: tuple[int, int]


@pytest.mark.parametrize(
    "case",
    [
        PointCase(name="origin", l_param=pack_point(0, 0), expected=(0, 0)),
        PointCase(name="primary_monitor", l_param=pack_point(640, 480), expected=(640, 480)),
        PointCase(name="monitor_left_of_primary", l_param=pack_point(-1280, 480), expected=(-1280, 480)),
        PointCase(name="monitor_above_primary", l_param=pack_point(640, -1080), expected=(640, -1080)),
        PointCase(name="monitor_left_of_and_above_primary", l_param=pack_point(-1, -1), expected=(-1, -1)),
        PointCase(name="largest_positive_coordinates", l_param=pack_point(32767, 32767), expected=(32767, 32767)),
        PointCase(name="smallest_negative_coordinates", l_param=pack_point(-32768, -32768), expected=(-32768, -32768)),
    ],
    ids=lambda case: case.name,
)
def test_cursor_point_unpacks_both_coordinates_signed(case: PointCase):
    assert read_hit_test_point(case.l_param) == case.expected


class OverhangCase(NamedTuple):
    name: str
    rect: tuple[int, int, int, int]
    expected: bool


@pytest.mark.parametrize(
    "case",
    [
        OverhangCase(name="exactly_the_monitor_is_not_fullscreen", rect=(0, 0, 1920, 1080), expected=False),
        OverhangCase(name="past_the_left_edge", rect=(-8, 0, 1920, 1080), expected=True),
        OverhangCase(name="past_the_top_edge", rect=(0, -8, 1920, 1080), expected=True),
        OverhangCase(name="past_the_right_edge", rect=(0, 0, 1928, 1080), expected=True),
        OverhangCase(name="past_the_bottom_edge", rect=(0, 0, 1920, 1088), expected=True),
        OverhangCase(name="past_every_edge", rect=(-8, -8, 1928, 1088), expected=True),
        OverhangCase(name="smaller_than_the_monitor", rect=(100, 100, 900, 700), expected=False),
        OverhangCase(name="wider_but_shorter_covers_no_edge_pair", rect=(-8, 100, 1928, 700), expected=False),
        OverhangCase(name="shifted_off_one_edge_only", rect=(-8, -8, 1912, 1072), expected=False),
    ],
    ids=lambda case: case.name,
)
def test_overhang_needs_full_cover_plus_one_edge_beyond(case: OverhangCase):
    assert overhangs(WindowRect(case.rect), MONITOR) is case.expected


class StripCase(NamedTuple):
    name: str
    edge: AppBarEdge | None
    expected: tuple[int, int, int, int]


@pytest.mark.parametrize(
    "case",
    [
        StripCase(name="left_edge", edge="left", expected=(2, 0, 1920, 1080)),
        StripCase(name="top_edge", edge="top", expected=(0, 2, 1920, 1080)),
        StripCase(name="right_edge", edge="right", expected=(0, 0, 1918, 1080)),
        StripCase(name="bottom_edge", edge="bottom", expected=(0, 0, 1920, 1078)),
        StripCase(name="no_edge_leaves_the_rect_alone", edge=None, expected=(0, 0, 1920, 1080)),
    ],
    ids=lambda case: case.name,
)
def test_auto_hide_strip_comes_off_the_taskbar_edge(case: StripCase):
    assert reserve_auto_hide_taskbar_strip(ClientRect((0, 0, 1920, 1080)), case.edge) == case.expected


def test_maximized_hit_test_asks_exactly_one_question():
    probe = RecordingHitTestProbe(is_maximized=True)

    assert handle_non_client_hit_test(probe) == (False, 0)
    assert probe.questions == ["maximized"]


def test_hit_test_without_a_window_rect_stops_before_the_monitor():
    probe = RecordingHitTestProbe(rect=None)

    assert handle_non_client_hit_test(probe) == (False, 0)
    assert probe.questions == ["maximized", "window_rect"]


def test_fullscreen_hit_test_stops_before_the_cursor():
    probe = RecordingHitTestProbe(rect=WindowRect((-8, 0, 1928, 1088)))

    assert handle_non_client_hit_test(probe) == (False, 0)
    assert probe.questions == ["maximized", "window_rect", "monitor_rect_for"]


def test_hit_test_looks_up_the_monitor_of_the_window_rect_it_read():
    probe = RecordingHitTestProbe(cursor=(500, 400))

    handle_non_client_hit_test(probe)

    assert ("monitor_rect_for", WINDOW) in probe.asked


def test_hit_test_without_a_monitor_keeps_going():
    probe = RecordingHitTestProbe(monitor_rect=None, cursor=(500, 102))

    assert handle_non_client_hit_test(probe) == (True, HTTOP)


class HitTestCase(NamedTuple):
    name: str
    cursor: tuple[int, int]
    expected: tuple[bool, int]


@pytest.mark.parametrize(
    "case",
    [
        HitTestCase(name="top_left_corner", cursor=(100, 100), expected=(True, HTTOPLEFT)),
        HitTestCase(name="last_pixel_of_the_left_corner", cursor=(115, 100), expected=(True, HTTOPLEFT)),
        HitTestCase(name="first_pixel_past_the_left_corner", cursor=(116, 100), expected=(True, HTTOP)),
        HitTestCase(name="middle_of_the_top_edge", cursor=(500, 107), expected=(True, HTTOP)),
        HitTestCase(name="last_pixel_before_the_right_corner", cursor=(884, 100), expected=(True, HTTOP)),
        HitTestCase(name="first_pixel_of_the_right_corner", cursor=(885, 100), expected=(True, HTTOPRIGHT)),
        HitTestCase(name="top_right_corner", cursor=(899, 100), expected=(True, HTTOPRIGHT)),
        HitTestCase(name="first_row_below_the_band", cursor=(500, 108), expected=(False, 0)),
        HitTestCase(name="deep_inside_the_client_area", cursor=(500, 400), expected=(False, 0)),
        HitTestCase(name="just_above_the_window", cursor=(500, 92), expected=(True, HTTOP)),
    ],
    ids=lambda case: case.name,
)
def test_hit_test_splits_the_top_band_into_corners_and_edge(case: HitTestCase):
    probe = RecordingHitTestProbe(cursor=case.cursor)

    assert handle_non_client_hit_test(probe) == case.expected


def test_hit_test_on_a_monitor_left_of_the_primary_one():
    probe = RecordingHitTestProbe(
        rect=WindowRect((-1820, -100, -1020, 500)),
        monitor_rect=MonitorRect((-1920, -1080, 0, 0)),
        cursor=(-1815, -100),
    )

    assert handle_non_client_hit_test(probe) == (True, HTTOPLEFT)


def test_calculate_size_without_a_monitor_stops_before_the_window_state():
    probe = RecordingCalcSizeProbe(geometry=None)

    assert handle_non_client_calculate_size(probe) == (False, 0, None)
    assert probe.questions == ["proposed_rect", "monitor_geometry_for"]


def test_an_ordinary_window_keeps_the_proposed_client_rect():
    probe = RecordingCalcSizeProbe(proposed=ProposedRect((100, 100, 900, 700)))

    assert handle_non_client_calculate_size(probe) == (False, 0, None)
    assert probe.questions == ["proposed_rect", "monitor_geometry_for", "maximized"]


def test_calculate_size_looks_up_the_monitor_of_the_proposed_rect():
    proposal = ProposedRect((1900, 100, 2700, 700))
    probe = RecordingCalcSizeProbe(proposed=proposal)

    handle_non_client_calculate_size(probe)

    assert ("monitor_geometry_for", proposal) in probe.asked


def test_a_maximized_window_gets_the_work_area():
    probe = RecordingCalcSizeProbe(is_maximized=True)

    assert handle_non_client_calculate_size(probe) == (True, WVR_REDRAW, WORK_AREA)


def test_a_fullscreen_window_gets_the_monitor_rect():
    probe = RecordingCalcSizeProbe(proposed=ProposedRect((-8, -8, 1928, 1088)))

    assert handle_non_client_calculate_size(probe) == (True, WVR_REDRAW, MONITOR)


def test_a_window_the_size_of_its_monitor_is_not_fullscreen():
    probe = RecordingCalcSizeProbe(proposed=FULL_MONITOR_PROPOSAL)

    assert handle_non_client_calculate_size(probe) == (False, 0, None)


def test_the_auto_hide_gate_short_circuits_the_edge_search():
    probe = RecordingCalcSizeProbe(is_maximized=True, auto_hide=False, edge="bottom")

    assert handle_non_client_calculate_size(probe) == (True, WVR_REDRAW, WORK_AREA)
    assert "auto_hide_edge" not in probe.questions


def test_an_auto_hide_taskbar_takes_a_strip_off_the_maximized_client_rect():
    probe = RecordingCalcSizeProbe(is_maximized=True, auto_hide=True, edge="bottom")

    assert handle_non_client_calculate_size(probe) == (True, WVR_REDRAW, (0, 0, 1920, 1038))
    # The edge is searched over the monitor rect, not the work area the client
    # rect came from: an auto-hide taskbar sits outside the work area.
    assert probe.asked[-2:] == [("auto_hide_enabled", None), ("auto_hide_edge", MONITOR)]


def test_an_auto_hide_taskbar_on_another_monitor_leaves_the_client_rect_alone():
    probe = RecordingCalcSizeProbe(is_maximized=True, auto_hide=True, edge=None)

    assert handle_non_client_calculate_size(probe) == (True, WVR_REDRAW, WORK_AREA)


def test_the_decisions_reach_nothing_platform_specific():
    # A module-level reach would already break this file's own import on Linux.
    # The scan is what catches one hidden inside a function, where it would run
    # on Windows and raise everywhere else.
    tree = ast.parse(DECISIONS.read_text(encoding="utf-8"))
    targets = [
        alias.name if isinstance(node, ast.Import) else node.module or ""
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    ]

    assert targets, "the scan read no imports; it would pass on any module"
    assert not [target for target in targets if "ctypes" in target or "windows" in target.split(".")]
