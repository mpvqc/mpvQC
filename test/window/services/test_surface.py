# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, NamedTuple

import pytest
from PySide6.QtCore import Qt
from PySide6.QtGui import QRegion

from mpvqc.window.services import NoSurfaceHandler, SurfaceSnapshot
from mpvqc.window.services.linux import RESIZE_BAND_WIDTH, SurfaceController

if TYPE_CHECKING:
    from mpvqc.window.services import SurfaceHandler

SURFACE = "mpvqc.window.services.linux.surface"

NO_STATE = Qt.WindowState.WindowNoState
MINIMIZED = Qt.WindowState.WindowMinimized
MAXIMIZED = Qt.WindowState.WindowMaximized
FULLSCREEN = Qt.WindowState.WindowFullScreen

DROP_SHADOW_MARGIN = 88
NO_OWN_FRAME = SurfaceSnapshot(draws_own_frame=False, drop_shadow_margin=0)
OWN_FRAME = SurfaceSnapshot(draws_own_frame=True, drop_shadow_margin=DROP_SHADOW_MARGIN)

NORMAL_SIZE = (1456, 896)
MAXIMIZED_SIZE = (2844, 1554)


@dataclass
class FakeQpa:
    """The platform layer the controller talks to: the platform name, the
    states the compositor has applied (None without a platform window), and
    the content margins handed down."""

    name: str = "wayland"
    applied_states: Qt.WindowState | None = None
    applied_margins: list[int] = field(default_factory=list)


@pytest.fixture
def qpa(monkeypatch) -> FakeQpa:
    fake = FakeQpa()
    monkeypatch.setattr(f"{SURFACE}.QGuiApplication.platformName", staticmethod(lambda: fake.name))
    monkeypatch.setattr(f"{SURFACE}.wayland_window_states", lambda _window: fake.applied_states)
    monkeypatch.setattr(
        f"{SURFACE}.apply_wayland_content_margins",
        lambda _window, margin: fake.applied_margins.append(margin),
    )
    return fake


class ReadSurfaceTestCase(NamedTuple):
    name: str
    drop_shadow_margin: int
    states: Qt.WindowState
    expected: SurfaceSnapshot


@pytest.mark.parametrize(
    "case",
    [
        ReadSurfaceTestCase(
            name="zero_margin_still_draws_the_frame",
            drop_shadow_margin=0,
            states=NO_STATE,
            expected=SurfaceSnapshot(draws_own_frame=True, drop_shadow_margin=0),
        ),
        ReadSurfaceTestCase(
            name="normal_draws_the_frame_with_the_margin",
            drop_shadow_margin=DROP_SHADOW_MARGIN,
            states=NO_STATE,
            expected=OWN_FRAME,
        ),
        ReadSurfaceTestCase(
            name="maximized_drops_the_frame_and_the_margin",
            drop_shadow_margin=DROP_SHADOW_MARGIN,
            states=MAXIMIZED,
            expected=NO_OWN_FRAME,
        ),
        ReadSurfaceTestCase(
            name="fullscreen_drops_the_frame_and_the_margin",
            drop_shadow_margin=DROP_SHADOW_MARGIN,
            states=FULLSCREEN,
            expected=NO_OWN_FRAME,
        ),
        ReadSurfaceTestCase(
            name="minimized_from_maximized_stays_without_frame",
            drop_shadow_margin=DROP_SHADOW_MARGIN,
            states=MAXIMIZED | MINIMIZED,
            expected=NO_OWN_FRAME,
        ),
        ReadSurfaceTestCase(
            name="minimized_from_normal_keeps_the_frame",
            drop_shadow_margin=DROP_SHADOW_MARGIN,
            states=MINIMIZED,
            expected=OWN_FRAME,
        ),
    ],
    ids=lambda case: case.name,
)
def test_read_surface(case: ReadSurfaceTestCase, make_recording_window):
    window = make_recording_window(case.states)
    handler: SurfaceHandler = SurfaceController(drop_shadow_margin=case.drop_shadow_margin)

    assert handler.read_surface(window) == case.expected


class AppliedStatesTestCase(NamedTuple):
    name: str
    platform_name: str
    applied_states: Qt.WindowState | None
    window_states: Qt.WindowState
    expected: SurfaceSnapshot


@pytest.mark.parametrize(
    "case",
    [
        AppliedStatesTestCase(
            name="wayland_prefers_the_states_the_compositor_applied",
            platform_name="wayland",
            applied_states=MAXIMIZED,
            window_states=NO_STATE,
            expected=NO_OWN_FRAME,
        ),
        AppliedStatesTestCase(
            name="wayland_without_a_platform_window_reads_the_qwindow",
            platform_name="wayland",
            applied_states=None,
            window_states=MAXIMIZED,
            expected=NO_OWN_FRAME,
        ),
        AppliedStatesTestCase(
            name="off_wayland_the_platform_answer_is_ignored",
            platform_name="xcb",
            applied_states=MAXIMIZED,
            window_states=NO_STATE,
            expected=OWN_FRAME,
        ),
    ],
    ids=lambda case: case.name,
)
def test_read_surface_keys_on_the_applied_states(case: AppliedStatesTestCase, make_recording_window, qpa):
    qpa.name = case.platform_name
    qpa.applied_states = case.applied_states
    window = make_recording_window(case.window_states)
    handler: SurfaceHandler = SurfaceController(drop_shadow_margin=DROP_SHADOW_MARGIN)

    assert handler.read_surface(window) == case.expected


class PushTestCase(NamedTuple):
    name: str
    initial_states: Qt.WindowState
    transitions: list[Qt.WindowState]
    pushed: list[SurfaceSnapshot]


@pytest.mark.parametrize(
    "case",
    [
        PushTestCase(
            name="configure_normal_pushes_the_frame",
            initial_states=NO_STATE,
            transitions=[],
            pushed=[OWN_FRAME],
        ),
        PushTestCase(
            name="configure_maximized_stays_silent",
            initial_states=MAXIMIZED,
            transitions=[],
            pushed=[],
        ),
        PushTestCase(
            name="maximize_drops_the_frame_and_restore_brings_it_back",
            initial_states=NO_STATE,
            transitions=[MAXIMIZED, NO_STATE],
            pushed=[OWN_FRAME, NO_OWN_FRAME, OWN_FRAME],
        ),
        PushTestCase(
            name="fullscreen_to_maximized_pushes_only_the_drop",
            initial_states=NO_STATE,
            transitions=[FULLSCREEN, MAXIMIZED],
            pushed=[OWN_FRAME, NO_OWN_FRAME],
        ),
        PushTestCase(
            name="minimize_from_normal_stays_silent",
            initial_states=NO_STATE,
            transitions=[MINIMIZED, NO_STATE],
            pushed=[OWN_FRAME],
        ),
        PushTestCase(
            name="minimize_from_maximized_stays_without_frame",
            initial_states=MAXIMIZED,
            transitions=[MAXIMIZED | MINIMIZED, MAXIMIZED],
            pushed=[],
        ),
    ],
    ids=lambda case: case.name,
)
def test_surface_pushes(case: PushTestCase, qt_app, make_recording_window):
    window = make_recording_window(case.initial_states)
    controller = SurfaceController(drop_shadow_margin=DROP_SHADOW_MARGIN)
    pushed: list[SurfaceSnapshot] = []
    controller.on_surface_changed(pushed.append)

    controller.configure_window(qt_app, window)
    for states in case.transitions:
        window.setWindowStates(states)

    assert pushed == case.pushed


class ResizeSyncTestCase(NamedTuple):
    name: str
    initial_states: Qt.WindowState
    applied_states: Qt.WindowState
    pushed: list[SurfaceSnapshot]
    applied_margins: list[int]


@pytest.mark.parametrize(
    "case",
    [
        ResizeSyncTestCase(
            name="maximize_lands_with_the_resize",
            initial_states=NO_STATE,
            applied_states=MAXIMIZED,
            pushed=[OWN_FRAME, NO_OWN_FRAME],
            applied_margins=[DROP_SHADOW_MARGIN, 0],
        ),
        ResizeSyncTestCase(
            name="fullscreen_lands_with_the_resize",
            initial_states=NO_STATE,
            applied_states=FULLSCREEN,
            pushed=[OWN_FRAME, NO_OWN_FRAME],
            applied_margins=[DROP_SHADOW_MARGIN, 0],
        ),
        ResizeSyncTestCase(
            name="restore_lands_with_the_resize",
            initial_states=MAXIMIZED,
            applied_states=NO_STATE,
            pushed=[OWN_FRAME],
            applied_margins=[DROP_SHADOW_MARGIN],
        ),
        ResizeSyncTestCase(
            name="resize_without_a_state_change_stays_silent",
            initial_states=NO_STATE,
            applied_states=NO_STATE,
            pushed=[OWN_FRAME],
            applied_margins=[DROP_SHADOW_MARGIN],
        ),
    ],
    ids=lambda case: case.name,
)
def test_resize_syncs_the_surface_before_the_state_event_arrives(
    case: ResizeSyncTestCase, qt_app, make_recording_window, qpa
):
    qpa.applied_states = case.initial_states
    window = make_recording_window(case.initial_states)
    window.resize(*NORMAL_SIZE)
    controller = SurfaceController(drop_shadow_margin=DROP_SHADOW_MARGIN)
    pushed: list[SurfaceSnapshot] = []
    controller.on_surface_changed(pushed.append)
    controller.configure_window(qt_app, window)

    # The compositor's configure: the platform window holds the new states
    # while the QWindow still reports the old ones, and the resize comes first.
    qpa.applied_states = case.applied_states
    window.resize(*MAXIMIZED_SIZE)

    assert pushed == case.pushed
    assert qpa.applied_margins == case.applied_margins

    # The queued state event lands afterwards and finds nothing left to do.
    window.setWindowStates(case.applied_states)

    assert pushed == case.pushed
    assert qpa.applied_margins == case.applied_margins


def test_resize_reapplies_the_input_mask_at_the_new_size(qt_app, make_recording_window):
    window = make_recording_window(NO_STATE)
    window.resize(*NORMAL_SIZE)
    controller = SurfaceController(drop_shadow_margin=DROP_SHADOW_MARGIN)
    controller.configure_window(qt_app, window)

    window.resize(*MAXIMIZED_SIZE)

    width, height = MAXIMIZED_SIZE
    inset = DROP_SHADOW_MARGIN - RESIZE_BAND_WIDTH
    assert window.masks[-1] == QRegion(inset, inset, width - 2 * inset, height - 2 * inset)


def test_screen_change_reapplies_content_margins(qt_app, make_recording_window, qpa):
    window = make_recording_window(NO_STATE)
    controller = SurfaceController(drop_shadow_margin=DROP_SHADOW_MARGIN)
    controller.configure_window(qt_app, window)
    assert qpa.applied_margins == [DROP_SHADOW_MARGIN]

    window.screenChanged.emit(window.screen())

    assert qpa.applied_margins == [DROP_SHADOW_MARGIN, DROP_SHADOW_MARGIN]


def test_no_surface_handler_reads_no_own_frame_and_never_pushes(make_recording_window):
    handler: SurfaceHandler = NoSurfaceHandler()
    pushed: list[SurfaceSnapshot] = []
    handler.on_surface_changed(pushed.append)

    for states in (NO_STATE, MINIMIZED, MAXIMIZED, FULLSCREEN):
        window = make_recording_window(states)
        assert handler.read_surface(window) == NO_OWN_FRAME
        window.setWindowStates(states)

    assert pushed == []
