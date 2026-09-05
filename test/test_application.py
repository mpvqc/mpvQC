# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Generator
from unittest.mock import MagicMock, patch

import inject
import pytest
from PySide6.QtCore import QCoreApplication
from PySide6.QtQuick import QQuickWindow

from mpvqc.i18n.services import I18nSettingsService, InternationalizationService
from mpvqc.services import FileStartupService, FontLoaderService


@pytest.fixture
def file_startup_service_mock():
    return MagicMock(spec_set=FileStartupService)


@pytest.fixture
def font_loader_service_mock():
    return MagicMock(spec_set=FontLoaderService)


@pytest.fixture(autouse=True)
def configure_injections(common_bindings_with, file_startup_service_mock, font_loader_service_mock):
    def custom_bindings(binder: inject.Binder):
        binder.bind(FileStartupService, file_startup_service_mock)
        binder.bind(FontLoaderService, font_loader_service_mock)

    common_bindings_with(custom_bindings)


@pytest.fixture
def internationalization_service(configure_injections) -> InternationalizationService:
    return inject.instance(InternationalizationService)


@pytest.fixture
def i18n_settings_service(configure_injections) -> I18nSettingsService:
    return inject.instance(I18nSettingsService)


@pytest.fixture
def retranslate_mock(internationalization_service) -> Generator[MagicMock]:
    # Only the translator swap is stubbed: the settings service keeps its language and its signal, so a language
    # change reaches the app the way it does in production.
    with patch.object(internationalization_service, "retranslate") as mock:
        yield mock


def test_application_configured(
    qt_app,
    file_startup_service_mock,
    font_loader_service_mock,
    retranslate_mock,
):
    qt_app.configure()

    font_loader_service_mock.load_application_fonts.assert_called_once()
    file_startup_service_mock.create_missing_directories.assert_called_once()
    file_startup_service_mock.create_missing_files.assert_called_once()
    retranslate_mock.assert_called_once()


def test_language_change_triggers_retranslation(qt_app, retranslate_mock, i18n_settings_service):
    qt_app.configure()

    i18n_settings_service.language_changed.emit("he-IL")

    assert retranslate_mock.call_count == 2


def test_first_frame_rendered_emitted_once_despite_multiple_frames(qt_app, make_spy):
    spy = make_spy(qt_app.first_frame_rendered)
    window = QQuickWindow()

    qt_app._announce_first_frame(window)
    window.frameSwapped.emit()
    window.frameSwapped.emit()
    QCoreApplication.processEvents()

    assert spy.count() == 1


def test_retranslation_happens_before_engine_language_set(qt_app, retranslate_mock):
    call_order = []
    retranslate_mock.side_effect = lambda **kwargs: call_order.append("retranslate")
    qt_app._engine.setUiLanguage = lambda lang: call_order.append("setUiLanguage")

    qt_app.configure()

    assert call_order == ["retranslate", "setUiLanguage"]
