# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path
from typing import NamedTuple

import inject
import pytest

from mpvqc.enums import MpvqcWindowTitleFormat
from mpvqc.services import PlayerService, SettingsService, StateService
from mpvqc.viewmodels import MpvqcHeaderViewModel

WindowTitleFormat = MpvqcWindowTitleFormat.WindowTitleFormat


@pytest.fixture
def view_model() -> MpvqcHeaderViewModel:
    # noinspection PyCallingNonCallable
    return MpvqcHeaderViewModel()


@pytest.fixture(autouse=True)
def configure_inject(
    common_bindings_with,
    state_service,
    fake_player_service,
    settings_service,
):
    def custom_bindings(binder: inject.Binder):
        binder.bind(StateService, state_service)
        binder.bind(PlayerService, fake_player_service)
        binder.bind(SettingsService, settings_service)

    common_bindings_with(custom_bindings)


class WindowTitleTestCase(NamedTuple):
    saved: bool
    document: Path | None
    window_title_format: WindowTitleFormat
    video: str | None
    expected: str


@pytest.mark.parametrize(
    "test_case",
    [
        WindowTitleTestCase(
            saved=True,
            document=None,
            window_title_format=WindowTitleFormat.DEFAULT,
            video=None,
            expected="TestApp",
        ),
        WindowTitleTestCase(
            saved=False,
            document=Path("doc.qc"),
            window_title_format=WindowTitleFormat.DEFAULT,
            video=None,
            expected="TestApp (unsaved)",
        ),
        WindowTitleTestCase(
            saved=True,
            document=Path("doc.qc"),
            window_title_format=WindowTitleFormat.FILE_NAME,
            video=str(Path.home() / "test_video.mp4"),
            expected="test_video.mp4",
        ),
        WindowTitleTestCase(
            saved=False,
            document=Path("doc.qc"),
            window_title_format=WindowTitleFormat.FILE_NAME,
            video=str(Path.home() / "test_video.mp4"),
            expected="test_video.mp4 (unsaved)",
        ),
        WindowTitleTestCase(
            saved=True,
            document=Path("doc.qc"),
            window_title_format=WindowTitleFormat.FILE_PATH,
            video=str(Path.home() / "test_video.mp4"),
            expected=str(Path.home() / "test_video.mp4"),
        ),
        WindowTitleTestCase(
            saved=False,
            document=Path("doc.qc"),
            window_title_format=WindowTitleFormat.FILE_PATH,
            video=str(Path.home() / "test_video.mp4"),
            expected=str(Path.home() / "test_video.mp4") + " (unsaved)",
        ),
        WindowTitleTestCase(
            saved=True,
            document=None,
            window_title_format=WindowTitleFormat.FILE_NAME,
            video=None,
            expected="TestApp",
        ),
        WindowTitleTestCase(
            saved=False,
            document=None,
            window_title_format=WindowTitleFormat.FILE_NAME,
            video=str(Path.home() / "test_video.mp4"),
            expected="test_video.mp4",
        ),
    ],
)
def test_window_title(
    qt_app,
    view_model,
    configure_state,
    fake_player_service,
    settings_service,
    test_case: WindowTitleTestCase,
):
    configure_state(saved=test_case.saved, document=test_case.document)
    if test_case.video is not None:
        fake_player_service.load_video(test_case.video)
    settings_service.window_title_format = test_case.window_title_format.value

    assert view_model.windowTitle == test_case.expected


def test_window_title_changed(
    view_model,
    configure_state,
    fake_player_service,
    settings_service,
    make_spy,
):
    file = Path.home() / "test_video.mp4"
    configure_state(saved=False)
    fake_player_service.load_video(f"{file.resolve()}")

    spy = make_spy(view_model.windowTitleChanged)

    settings_service.window_title_format = WindowTitleFormat.FILE_NAME.value
    assert spy.count() == 1
