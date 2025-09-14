# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path
from unittest.mock import MagicMock

import inject
import pytest
from PySide6.QtCore import QSettings

from mpvqc.services import ApplicationPathsService, SettingsService


@pytest.fixture(scope="module")
def make_settings():
    settings_path = Path()
    mock = MagicMock()
    mock.file_settings = settings_path

    def config(binder: inject.Binder):
        binder.bind(ApplicationPathsService, mock)

    inject.configure(config, clear=True)

    def _make_settings(values: dict[str, ...]) -> SettingsService:
        q_settings = QSettings(f"{settings_path}", QSettings.Format.IniFormat)
        q_settings.clear()
        for key, value in values.items():
            q_settings.setValue(key, value)

        app_settings = SettingsService()
        app_settings._settings = q_settings
        return app_settings

    return _make_settings


def test_settings_language(make_settings):
    settings = make_settings({})
    assert settings.language == "en-US"


@pytest.mark.parametrize(
    ("config", "expected"),
    [
        ({}, ""),
        ({"Export/nickname": ""}, ""),
        ({"Export/nickname": True}, "True"),
        ({"Export/nickname": 1}, "1"),
        ({"Export/nickname": "nick"}, "nick"),
    ],
)
def test_settings_string(make_settings, config, expected):
    settings = make_settings(config)
    assert expected == settings.nickname


@pytest.mark.parametrize(
    ("config", "expected"),
    [
        ({}, False),
        ({"Export/writeHeaderDate": ""}, False),
        ({"Export/writeHeaderDate": True}, True),
        ({"Export/writeHeaderDate": 1}, False),
        ({"Export/writeHeaderDate": "true"}, True),
    ],
)
def test_settings_bool(make_settings, config, expected):
    settings = make_settings(config)
    assert expected == settings.writeHeaderDate


ENUM_VALUE = SettingsService.ImportWhenVideoLinkedInDocument


@pytest.mark.parametrize(
    ("config", "expected"),
    [
        ({"Import/importWhenVideoLinkedInDocument": 0}, ENUM_VALUE.ALWAYS),
        ({"Import/importWhenVideoLinkedInDocument": 1}, ENUM_VALUE.ASK_EVERY_TIME),
        ({"Import/importWhenVideoLinkedInDocument": 2}, ENUM_VALUE.NEVER),
        ({"Import/importWhenVideoLinkedInDocument": ENUM_VALUE.NEVER.value}, ENUM_VALUE.NEVER),
    ],
)
def test_settings_enum(make_settings, config, expected):
    settings = make_settings(config)
    assert expected == settings.import_video_when_video_linked_in_document
