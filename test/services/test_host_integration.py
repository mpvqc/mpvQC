# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import platform
from unittest.mock import MagicMock, patch

import pytest

from mpvqc.services import WindowButtonPreference
from mpvqc.services.host_integration import read_linux_window_button_preference

linux_only = pytest.mark.skipif(platform.system() != "Linux", reason="Requires Linux")


@pytest.fixture
def settings_portal_mock():
    with patch("mpvqc.services.host_integration.portals.SettingsPortal") as mock_class:
        mock_instance = MagicMock()
        mock_class.return_value = mock_instance
        mock_instance.__enter__.return_value = mock_instance
        yield mock_instance


@linux_only
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

    assert read_linux_window_button_preference() == expected
