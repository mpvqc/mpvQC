# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock

import inject
import pytest
from PySide6.QtCore import QObject, QUrl

from mpvqc.services import (
    FileStartupService,
    FontLoaderService,
    InternationalizationService,
    SettingsService,
)

QML = """
    import QtQuick
    import QtQuick.Controls

    ApplicationWindow {
        visible: false; width: 50; height: 50

        Button { objectName: "button-click-me"; text: "Click Me" }
    }
"""


def test_find_object(qt_app):
    qt_app._engine.loadData(QML.encode(), QUrl())
    obj = qt_app.find_object(QObject, "button-click-me")
    assert obj

    with pytest.raises(ValueError):  # noqa: PT011
        qt_app.find_object(QObject, "other-button-that-does-not-exist")


@pytest.fixture
def file_startup_service_mock():
    return MagicMock(spec_set=FileStartupService)


@pytest.fixture
def font_loader_service_mock():
    return MagicMock(spec_set=FontLoaderService)


@pytest.fixture
def internationalization_service_mock():
    return MagicMock(spec_set=InternationalizationService)


@pytest.fixture(autouse=True)
def configure_injections(
    common_bindings_with,
    file_startup_service_mock,
    font_loader_service_mock,
    internationalization_service_mock,
    settings_service,
):
    def custom_bindings(binder: inject.Binder):
        binder.bind(FileStartupService, file_startup_service_mock)
        binder.bind(FontLoaderService, font_loader_service_mock)
        binder.bind(InternationalizationService, internationalization_service_mock)
        binder.bind(SettingsService, settings_service)

    common_bindings_with(custom_bindings)


def test_application_configured(
    qt_app,
    file_startup_service_mock,
    font_loader_service_mock,
    internationalization_service_mock,
    settings_service,
):
    qt_app.configure()

    font_loader_service_mock.load_application_fonts.assert_called_once()
    file_startup_service_mock.create_missing_directories.assert_called_once()
    file_startup_service_mock.create_missing_files.assert_called_once()
    internationalization_service_mock.retranslate.assert_called_once()


def test_language_change_triggers_retranslation(qt_app, internationalization_service_mock, settings_service):
    qt_app.configure()

    settings_service.languageChanged.emit("he-IL")

    assert internationalization_service_mock.retranslate.call_count == 2


def test_retranslation_happens_before_engine_language_set(qt_app, internationalization_service_mock):
    call_order = []
    internationalization_service_mock.retranslate.side_effect = lambda **kwargs: call_order.append("retranslate")
    qt_app._engine.setUiLanguage = lambda lang: call_order.append("setUiLanguage")

    qt_app.configure()

    assert call_order == ["retranslate", "setUiLanguage"]
