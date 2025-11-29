# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path
from typing import NamedTuple

import inject
import pytest

from mpvqc.services import PlayerService, SettingsService, StateService
from mpvqc.viewmodels import MpvqcHeaderViewModel, MpvqcMenuBarViewModel


@pytest.fixture
def view_model() -> MpvqcHeaderViewModel:
    # noinspection PyCallingNonCallable
    return MpvqcHeaderViewModel()


@pytest.fixture(autouse=True)
def configure_inject(
    common_bindings_with,
    state_service,
    player_service_mock,
    settings_service,
):
    def custom_bindings(binder: inject.Binder):
        binder.bind(StateService, state_service)
        binder.bind(PlayerService, player_service_mock)
        binder.bind(SettingsService, settings_service)

    common_bindings_with(custom_bindings)


class WindowTitleTestCase(NamedTuple):
    saved: bool
    window_title_format: MpvqcMenuBarViewModel.WindowTitleFormat
    video_loaded: bool
    filename: str | None
    path: str | None
    expected: str


@pytest.mark.parametrize(
    "test_case",
    [
        WindowTitleTestCase(
            saved=True,
            window_title_format=MpvqcMenuBarViewModel.WindowTitleFormat.DEFAULT,
            video_loaded=False,
            filename=None,
            path=None,
            expected="TestApp",
        ),
        WindowTitleTestCase(
            saved=False,
            window_title_format=MpvqcMenuBarViewModel.WindowTitleFormat.DEFAULT,
            video_loaded=False,
            filename=None,
            path=None,
            expected="TestApp (unsaved)",
        ),
        WindowTitleTestCase(
            saved=True,
            window_title_format=MpvqcMenuBarViewModel.WindowTitleFormat.FILE_NAME,
            video_loaded=True,
            filename="test_video.mp4",
            path=None,
            expected="test_video.mp4",
        ),
        WindowTitleTestCase(
            saved=False,
            window_title_format=MpvqcMenuBarViewModel.WindowTitleFormat.FILE_NAME,
            video_loaded=True,
            filename="test_video.mp4",
            path=None,
            expected="test_video.mp4 (unsaved)",
        ),
        WindowTitleTestCase(
            saved=True,
            window_title_format=MpvqcMenuBarViewModel.WindowTitleFormat.FILE_PATH,
            video_loaded=True,
            filename=None,
            path=str(Path.home() / "test_video.mp4"),
            expected=str(Path.home() / "test_video.mp4"),
        ),
        WindowTitleTestCase(
            saved=False,
            window_title_format=MpvqcMenuBarViewModel.WindowTitleFormat.FILE_PATH,
            video_loaded=True,
            filename=None,
            path=str(Path.home() / "test_video.mp4"),
            expected=str(Path.home() / "test_video.mp4") + " (unsaved)",
        ),
        WindowTitleTestCase(
            saved=True,
            window_title_format=MpvqcMenuBarViewModel.WindowTitleFormat.FILE_NAME,
            video_loaded=False,
            filename=None,
            path=None,
            expected="TestApp",
        ),
    ],
)
def test_window_title(
    qt_app,
    view_model,
    configure_state,
    player_service_mock,
    settings_service,
    test_case: WindowTitleTestCase,
):
    configure_state(saved=test_case.saved)
    player_service_mock.update(
        video_loaded=test_case.video_loaded,
        filename=test_case.filename,
        path=test_case.path,
    )
    settings_service.window_title_format = test_case.window_title_format.value

    assert view_model.windowTitle == test_case.expected


def test_window_title_changed(
    view_model,
    configure_state,
    player_service_mock,
    settings_service,
    make_spy,
):
    file = Path.home() / "test_video.mp4"
    configure_state(saved=False)
    player_service_mock.update(
        video_loaded=True,
        filename=file.name,
        path=f"{file.resolve()}",
    )

    spy = make_spy(view_model.windowTitleChanged)

    settings_service.language = "es-MX"
    assert spy.count() == 1
