# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import replace
from pathlib import Path
from typing import NamedTuple

import inject
import pytest

from mpvqc.enums import MpvqcWindowTitleFormat
from mpvqc.player.services import PlayerService
from mpvqc.services import InternationalizationService, SettingsService, StateService
from mpvqc.viewmodels import MpvqcHeaderViewModel
from mpvqc.viewmodels.views.header.header import HeaderInputs, HeaderProps, derive_header_props

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


@pytest.fixture(autouse=True)
def qt_app_must_be_running(qt_app):
    pass


BASE_INPUTS = HeaderInputs(
    video_loaded=True,
    filename="test_video.mp4",
    path="/videos/test_video.mp4",
    window_title_format=WindowTitleFormat.DEFAULT,
    has_unsaved_document=False,
    app_name="TestApp",
    unsaved_template="%1 (unsaved)",
)


class DerivationCase(NamedTuple):
    name: str
    inputs: HeaderInputs
    expected: HeaderProps


@pytest.mark.parametrize(
    "case",
    [
        DerivationCase(
            name="no video shows the app name",
            inputs=replace(BASE_INPUTS, video_loaded=False, filename="", path=""),
            expected=HeaderProps(window_title="TestApp"),
        ),
        DerivationCase(
            name="no video with unsaved document suffixes the app name",
            inputs=replace(BASE_INPUTS, video_loaded=False, filename="", path="", has_unsaved_document=True),
            expected=HeaderProps(window_title="TestApp (unsaved)"),
        ),
        DerivationCase(
            name="no video forces the app name despite file name format",
            inputs=replace(BASE_INPUTS, video_loaded=False, window_title_format=WindowTitleFormat.FILE_NAME),
            expected=HeaderProps(window_title="TestApp"),
        ),
        DerivationCase(
            name="default format shows the app name despite video",
            inputs=BASE_INPUTS,
            expected=HeaderProps(window_title="TestApp"),
        ),
        DerivationCase(
            name="file name format shows the file name",
            inputs=replace(BASE_INPUTS, window_title_format=WindowTitleFormat.FILE_NAME),
            expected=HeaderProps(window_title="test_video.mp4"),
        ),
        DerivationCase(
            name="file name format with unsaved document suffixes the file name",
            inputs=replace(BASE_INPUTS, window_title_format=WindowTitleFormat.FILE_NAME, has_unsaved_document=True),
            expected=HeaderProps(window_title="test_video.mp4 (unsaved)"),
        ),
        DerivationCase(
            name="file path format shows the file path",
            inputs=replace(BASE_INPUTS, window_title_format=WindowTitleFormat.FILE_PATH),
            expected=HeaderProps(window_title="/videos/test_video.mp4"),
        ),
        DerivationCase(
            name="file path format with unsaved document suffixes the file path",
            inputs=replace(BASE_INPUTS, window_title_format=WindowTitleFormat.FILE_PATH, has_unsaved_document=True),
            expected=HeaderProps(window_title="/videos/test_video.mp4 (unsaved)"),
        ),
        DerivationCase(
            name="untranslated template is honored",
            inputs=replace(BASE_INPUTS, has_unsaved_document=True, unsaved_template="%1 (unsaved)"),
            expected=HeaderProps(window_title="TestApp (unsaved)"),
        ),
        DerivationCase(
            name="german-shaped template is honored",
            inputs=replace(BASE_INPUTS, has_unsaved_document=True, unsaved_template="%1 (ungespeichert)"),
            expected=HeaderProps(window_title="TestApp (ungespeichert)"),
        ),
    ],
    ids=lambda case: case.name,
)
def test_derivation(case: DerivationCase):
    assert derive_header_props(case.inputs) == case.expected


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


def test_initial_snapshot_reads_services_at_construction(
    configure_state,
    fake_player_service,
    settings_service,
):
    configure_state(saved=False, document=Path("doc.qc"))
    fake_player_service.load_video("/videos/test_video.mp4")
    settings_service.window_title_format = WindowTitleFormat.FILE_NAME.value

    # noinspection PyCallingNonCallable
    view_model = MpvqcHeaderViewModel()

    assert view_model.windowTitle == "test_video.mp4 (unsaved)"


def test_retranslation_folds_german_unsaved_template(
    qt_app,
    view_model,
    configure_state,
    make_spy,
):
    configure_state(saved=False, document=Path("doc.qc"))
    assert view_model.windowTitle == "TestApp (unsaved)"
    spy = make_spy(view_model.windowTitleChanged)

    inject.instance(InternationalizationService).retranslate(qt_app, "de-DE")

    assert spy.count() == 1
    assert spy.at(0, 0) == "TestApp (ungespeichert)"
    assert view_model.windowTitle == "TestApp (ungespeichert)"
