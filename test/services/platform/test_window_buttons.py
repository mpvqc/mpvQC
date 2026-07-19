# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
from unittest.mock import MagicMock, patch

import pytest

if sys.platform != "linux":
    pytest.skip("Requires Linux", allow_module_level=True)

from mpvqc.services import WindowButtonPreference
from mpvqc.services.platform.linux.window_button_detector import WindowButtonDetector


@pytest.fixture
def settings_portal_mock():
    with patch("mpvqc.services.platform.linux.window_button_detector.SettingsPortal") as mock_class:
        mock_instance = MagicMock()
        mock_class.return_value = mock_instance
        mock_instance.__enter__.return_value = mock_instance
        yield mock_instance


@pytest.mark.parametrize(
    ("layout", "expected"),
    [
        ("appmenu:minimize,maximize,close", WindowButtonPreference(True, True, True)),
        (":close", WindowButtonPreference(False, False, True)),
        ("", WindowButtonPreference(False, False, False)),
        ("minimize,close", WindowButtonPreference(True, False, True)),
        ("MINIMIZE,MAXIMIZE,CLOSE", WindowButtonPreference(True, True, True)),
        (None, WindowButtonPreference(True, True, True)),
    ],
)
def test_gnome_parse_button_layout(settings_portal_mock, layout, expected):
    settings_portal_mock.read_one.return_value = layout

    assert WindowButtonDetector._read_preference() == expected


def test_detect_applies_preference_on_drain(qt_app, settings_portal_mock, manual_executor, make_spy):
    settings_portal_mock.read_one.return_value = ":close"

    detector = WindowButtonDetector(manual_executor)
    spy = make_spy(detector.preference_changed)

    detector.detect()
    assert detector.preference == WindowButtonPreference(True, True, True)

    manual_executor.drain()

    assert detector.preference == WindowButtonPreference(False, False, True)
    assert spy.count() == 1


def test_detect_keeps_default_when_portal_reports_default(qt_app, settings_portal_mock, manual_executor, make_spy):
    settings_portal_mock.read_one.return_value = None

    detector = WindowButtonDetector(manual_executor)
    spy = make_spy(detector.preference_changed)

    detector.detect()
    manual_executor.drain()

    assert detector.preference == WindowButtonPreference(True, True, True)
    assert spy.count() == 0
