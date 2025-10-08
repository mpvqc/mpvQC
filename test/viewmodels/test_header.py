# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path
from typing import NamedTuple
from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.services import PlayerService, ResetService, SettingsService, StateService
from mpvqc.viewmodels import MpvqcAppHeaderViewModel


@pytest.fixture
def reset_service_mock() -> MagicMock:
    return MagicMock(spec_set=ResetService)


@pytest.fixture
def view_model() -> MpvqcAppHeaderViewModel:
    # noinspection PyCallingNonCallable
    return MpvqcAppHeaderViewModel()


@pytest.fixture(autouse=True)
def configure_inject(reset_service_mock, state_service, player_service_mock, settings_service):
    def config(binder: inject.Binder):
        binder.bind(StateService, state_service)
        binder.bind(ResetService, reset_service_mock)
        binder.bind(PlayerService, player_service_mock)
        binder.bind(SettingsService, settings_service)

    inject.configure(config, clear=True)


class WindowTitleTestCase(NamedTuple):
    saved: bool
    window_title_format: MpvqcAppHeaderViewModel.WindowTitleFormat
    video_loaded: bool
    filename: str | None
    path: str | None
    expected: str


@pytest.mark.parametrize(
    "test_case",
    [
        WindowTitleTestCase(
            saved=True,
            window_title_format=MpvqcAppHeaderViewModel.WindowTitleFormat.DEFAULT,
            video_loaded=False,
            filename=None,
            path=None,
            expected="TestApp",
        ),
        WindowTitleTestCase(
            saved=False,
            window_title_format=MpvqcAppHeaderViewModel.WindowTitleFormat.DEFAULT,
            video_loaded=False,
            filename=None,
            path=None,
            expected="TestApp (unsaved)",
        ),
        WindowTitleTestCase(
            saved=True,
            window_title_format=MpvqcAppHeaderViewModel.WindowTitleFormat.FILE_NAME,
            video_loaded=True,
            filename="test_video.mp4",
            path=None,
            expected="test_video.mp4",
        ),
        WindowTitleTestCase(
            saved=False,
            window_title_format=MpvqcAppHeaderViewModel.WindowTitleFormat.FILE_NAME,
            video_loaded=True,
            filename="test_video.mp4",
            path=None,
            expected="test_video.mp4 (unsaved)",
        ),
        WindowTitleTestCase(
            saved=True,
            window_title_format=MpvqcAppHeaderViewModel.WindowTitleFormat.FILE_PATH,
            video_loaded=True,
            filename=None,
            path=str(Path.home() / "test_video.mp4"),
            expected=str(Path.home() / "test_video.mp4"),
        ),
        WindowTitleTestCase(
            saved=False,
            window_title_format=MpvqcAppHeaderViewModel.WindowTitleFormat.FILE_PATH,
            video_loaded=True,
            filename=None,
            path=str(Path.home() / "test_video.mp4"),
            expected=str(Path.home() / "test_video.mp4") + " (unsaved)",
        ),
        WindowTitleTestCase(
            saved=True,
            window_title_format=MpvqcAppHeaderViewModel.WindowTitleFormat.FILE_NAME,
            video_loaded=False,
            filename=None,
            path=None,
            expected="TestApp",
        ),
    ],
)
def test_window_title(
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


def test_request_reset_app_state(view_model, configure_state, reset_service_mock, make_spy):
    spy = make_spy(view_model.confirmResetRequested)

    configure_state(saved=True)
    view_model.requestResetAppState()
    reset_service_mock.reset.assert_called_once()
    assert spy.count() == 0

    reset_service_mock.reset.reset_mock()
    configure_state(saved=False)
    view_model.requestResetAppState()
    assert spy.count() == 1
    reset_service_mock.reset.assert_not_called()
