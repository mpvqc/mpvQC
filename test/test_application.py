# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Generator
from pathlib import Path
from unittest.mock import MagicMock, patch

import inject
import pytest
from PySide6.QtCore import QCoreApplication, QFile
from PySide6.QtGui import QFontDatabase
from PySide6.QtQuick import QQuickWindow

from mpvqc import application
from mpvqc.appdata.services import ApplicationPathsService
from mpvqc.i18n.services import I18nSettingsService, InternationalizationService


@pytest.fixture
def application_paths(tmp_path: Path) -> ApplicationPathsService:
    (tmp_path / "portable").touch()
    return ApplicationPathsService(tmp_path)


@pytest.fixture
def prepare_app_data_mock() -> Generator[MagicMock]:
    with patch("mpvqc.application.prepare_app_data") as mock:
        yield mock


@pytest.fixture
def load_application_fonts_mock() -> Generator[MagicMock]:
    with patch("mpvqc.application._load_application_fonts") as mock:
        yield mock


@pytest.fixture(autouse=True)
def configure_injections(common_bindings_with, application_paths):
    def custom_bindings(binder: inject.Binder):
        binder.bind(ApplicationPathsService, application_paths)

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
    prepare_app_data_mock,
    application_paths,
    load_application_fonts_mock,
    retranslate_mock,
):
    qt_app.configure()

    load_application_fonts_mock.assert_called_once()
    prepare_app_data_mock.assert_called_once_with(application_paths)
    retranslate_mock.assert_called_once()


def test_language_change_triggers_retranslation(qt_app, prepare_app_data_mock, retranslate_mock, i18n_settings_service):
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


def test_retranslation_happens_before_engine_language_set(qt_app, prepare_app_data_mock, retranslate_mock):
    call_order = []
    retranslate_mock.side_effect = lambda **kwargs: call_order.append("retranslate")
    qt_app._engine.setUiLanguage = lambda lang: call_order.append("setUiLanguage")

    qt_app.configure()

    assert call_order == ["retranslate", "setUiLanguage"]


def test_fonts_present_in_resources(qt_app):
    variants = [
        "NotoSans-Regular.ttf",
        "NotoSans-Italic.ttf",
        "NotoSans-Bold.ttf",
        "NotoSans-SemiBold.ttf",
        "NotoSansHebrew-Bold.ttf",
        "NotoSansHebrew-Regular.ttf",
        "NotoSansHebrew-SemiBold.ttf",
        "NotoSansMono-Regular.ttf",
    ]
    for variant in variants:
        file = QFile(f":/data/fonts/{variant}")
        assert file.exists(), f"Expected to find {variant} in resources but couldn't"


def test_fonts_loaded(qt_app):
    # It's not possible to clear Qt's entire font database. Additionally, font backends on different OS's behave
    # differently. Therefore, we just test for the common font families.
    verifiable_font_families = [
        "Noto Sans",
        "Noto Sans Hebrew",
        "Noto Sans Mono",
    ]

    application._load_application_fonts()
    loaded_font_families = QFontDatabase.families()

    for font_family in verifiable_font_families:
        assert font_family in loaded_font_families, (
            f"Cannot find font family '{font_family}' in loaded font families {loaded_font_families}"
        )
