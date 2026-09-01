# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NamedTuple

import inject
import pytest
from PySide6.QtCore import QTimer

from mpvqc.player.services import PlayerService
from mpvqc.viewmodels import MpvqcToolBarViewModel
from mpvqc.viewmodels.views.header.toolbar import ToolbarInputs, ToolbarProps, derive_toolbar_props

BOTH_TRACKS = [{"type": "audio"}, {"type": "sub"}]

# the tests fire the settle themselves; the window only has to outlast the test, a short one races the pushes
BURST_WINDOW_MS = 60_000


@pytest.fixture(autouse=True)
def configure_inject(common_bindings_with, player_service):
    def custom_bindings(binder: inject.Binder):
        binder.bind(PlayerService, player_service)

    common_bindings_with(custom_bindings)


@pytest.fixture(autouse=True)
def qt_app_must_be_running(qt_app):
    pass


@pytest.fixture
def make_view_model():
    def _make() -> MpvqcToolBarViewModel:
        # noinspection PyCallingNonCallable
        return MpvqcToolBarViewModel(burst_window_ms=BURST_WINDOW_MS)

    return _make


def settle(view_model: MpvqcToolBarViewModel) -> None:
    timer = view_model.findChild(QTimer)
    assert timer is not None
    assert timer.isActive(), "no fold armed the settle timer, production would never emit"
    timer.timeout.emit()


@pytest.fixture
def spy_notifies(make_spy):
    def _spy(view_model: MpvqcToolBarViewModel) -> dict:
        return {
            "frameStepActive": make_spy(view_model.frameStepActiveChanged),
            "subtitleActive": make_spy(view_model.subtitleActiveChanged),
            "audioActive": make_spy(view_model.audioActiveChanged),
        }

    return _spy


def emissions(spies: dict) -> dict[str, int]:
    return {name: spy.count() for name, spy in spies.items() if spy.count()}


class DerivationCase(NamedTuple):
    name: str
    inputs: ToolbarInputs
    expected: ToolbarProps


@pytest.mark.parametrize(
    "case",
    [
        DerivationCase(
            name="no video deactivates everything despite tracks",
            inputs=ToolbarInputs(video_loaded=False, audio_track_count=2, subtitle_track_count=1),
            expected=ToolbarProps(frame_step_active=False, subtitle_active=False, audio_active=False),
        ),
        DerivationCase(
            name="video without tracks activates frame step only",
            inputs=ToolbarInputs(video_loaded=True, audio_track_count=0, subtitle_track_count=0),
            expected=ToolbarProps(frame_step_active=True, subtitle_active=False, audio_active=False),
        ),
        DerivationCase(
            name="audio alone activates audio",
            inputs=ToolbarInputs(video_loaded=True, audio_track_count=1, subtitle_track_count=0),
            expected=ToolbarProps(frame_step_active=True, subtitle_active=False, audio_active=True),
        ),
        DerivationCase(
            name="subtitles alone activate subtitles",
            inputs=ToolbarInputs(video_loaded=True, audio_track_count=0, subtitle_track_count=1),
            expected=ToolbarProps(frame_step_active=True, subtitle_active=True, audio_active=False),
        ),
        DerivationCase(
            name="both tracks activate everything",
            inputs=ToolbarInputs(video_loaded=True, audio_track_count=1, subtitle_track_count=1),
            expected=ToolbarProps(frame_step_active=True, subtitle_active=True, audio_active=True),
        ),
    ],
    ids=lambda case: case.name,
)
def test_derivation(case: DerivationCase):
    assert derive_toolbar_props(case.inputs) == case.expected


def test_initial_snapshot_reads_player_at_construction(make_view_model, player_handle):
    player_handle.load_video("/videos/movie.mkv")
    player_handle.update(track_list=BOTH_TRACKS)

    view_model = make_view_model()

    assert view_model.frameStepActive
    assert view_model.subtitleActive
    assert view_model.audioActive


def test_folds_inside_one_window_settle_to_one_emission_batch(make_view_model, player_handle, spy_notifies):
    view_model = make_view_model()
    spies = spy_notifies(view_model)

    player_handle.load_video("/videos/movie.mkv")
    player_handle.update(track_list=BOTH_TRACKS)

    assert emissions(spies) == {}
    assert not view_model.frameStepActive

    settle(view_model)

    assert emissions(spies) == {"frameStepActive": 1, "subtitleActive": 1, "audioActive": 1}
    assert spies["frameStepActive"].at(0, 0) is True
    assert spies["subtitleActive"].at(0, 0) is True
    assert spies["audioActive"].at(0, 0) is True


def test_video_switch_emits_only_settled_deltas(make_view_model, player_handle, spy_notifies):
    player_handle.load_video("/videos/a.mkv")
    player_handle.update(track_list=BOTH_TRACKS)
    view_model = make_view_model()
    spies = spy_notifies(view_model)

    player_handle.unload_video()
    player_handle.load_video("/videos/b.mkv")
    player_handle.update(track_list=[{"type": "audio"}])

    assert emissions(spies) == {}

    settle(view_model)

    assert emissions(spies) == {"subtitleActive": 1}
    assert spies["subtitleActive"].at(0, 0) is False


def test_failed_load_retracts_all_three_buttons(make_view_model, player_handle, spy_notifies):
    player_handle.load_video("/videos/movie.mkv")
    player_handle.update(track_list=BOTH_TRACKS)
    view_model = make_view_model()
    spies = spy_notifies(view_model)

    player_handle.unload_video()

    settle(view_model)

    assert emissions(spies) == {"frameStepActive": 1, "subtitleActive": 1, "audioActive": 1}
    assert spies["frameStepActive"].at(0, 0) is False
    assert spies["subtitleActive"].at(0, 0) is False
    assert spies["audioActive"].at(0, 0) is False
