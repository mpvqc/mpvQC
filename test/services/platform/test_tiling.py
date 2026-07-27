# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NamedTuple

import pytest

from mpvqc.services.platform.linux.tiling import is_tiling_desktop


class TilingDesktopTestCase(NamedTuple):
    name: str
    xdg_current_desktop: str | None
    expected: bool


@pytest.mark.parametrize(
    "case",
    [
        TilingDesktopTestCase("wayland compositor", "sway", expected=True),
        TilingDesktopTestCase("x11 window manager", "i3", expected=True),
        TilingDesktopTestCase("colon separated", "sway:wlroots:swayfx", expected=True),
        TilingDesktopTestCase("mixed case", "Hyprland", expected=True),
        TilingDesktopTestCase("non tiling desktop", "GNOME", expected=False),
        TilingDesktopTestCase("unset", None, expected=False),
    ],
    ids=lambda case: case.name,
)
def test_is_tiling_desktop(monkeypatch, case: TilingDesktopTestCase):
    if case.xdg_current_desktop is None:
        monkeypatch.delenv("XDG_CURRENT_DESKTOP", raising=False)
    else:
        monkeypatch.setenv("XDG_CURRENT_DESKTOP", case.xdg_current_desktop)

    assert is_tiling_desktop() is case.expected
