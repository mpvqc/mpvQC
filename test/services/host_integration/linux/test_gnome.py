# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock, patch

import pytest

from mpvqc.services.host_integration.linux.gnome import GnomeDesktop
from mpvqc.services.host_integration.types import OsBackend, WindowButtonPreference

from .conftest import linux_only


@pytest.fixture
def settings_portal_mock():
    with patch("mpvqc.services.host_integration.linux.gnome.SettingsPortal") as mock_class:
        mock_instance = MagicMock()
        mock_class.return_value = mock_instance
        mock_instance.__enter__.return_value = mock_instance
        yield mock_instance


@pytest.fixture(scope="session")
def gnome():
    return GnomeDesktop()


@linux_only
@pytest.mark.parametrize(
    ("layout", "expected"),
    [
        ("appmenu:minimize,maximize,close", WindowButtonPreference(True, True, True)),
        (":close", WindowButtonPreference(False, False, True)),
        ("", WindowButtonPreference(False, False, False)),
        ("minimize,close", WindowButtonPreference(True, False, True)),
        ("MINIMIZE,MAXIMIZE,CLOSE", WindowButtonPreference(True, True, True)),
    ],
)
def test_gnome_parse_button_layout(gnome: OsBackend, settings_portal_mock, layout, expected):
    settings_portal_mock.read_one.return_value = layout

    result = gnome.get_window_button_preference()
    assert result == expected
