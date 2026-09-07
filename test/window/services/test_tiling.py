# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NamedTuple

import pytest

from mpvqc.window.services.linux import is_tiling_desktop


class TilingDesktopTestCase(NamedTuple):
    name: str
    xdg_current_desktop: str | None
    expected: bool


@pytest.mark.parametrize(
    "case",
    [
        TilingDesktopTestCase(
            name="wayland compositor",
            xdg_current_desktop="sway",
            expected=True,
        ),
        TilingDesktopTestCase(
            name="x11 window manager",
            xdg_current_desktop="i3",
            expected=True,
        ),
        TilingDesktopTestCase(
            name="colon separated",
            xdg_current_desktop="sway:wlroots:swayfx",
            expected=True,
        ),
        TilingDesktopTestCase(
            name="semicolon separated",
            xdg_current_desktop="sway;wlroots",
            expected=True,
        ),
        TilingDesktopTestCase(
            name="trailing separator",
            xdg_current_desktop="sway;",
            expected=True,
        ),
        TilingDesktopTestCase(
            name="padded name",
            xdg_current_desktop="GNOME: i3 ",
            expected=True,
        ),
        TilingDesktopTestCase(
            name="mixed case",
            xdg_current_desktop="Hyprland",
            expected=True,
        ),
        TilingDesktopTestCase(
            name="compositor beside its display server",
            xdg_current_desktop="miracle-wm;mir",
            expected=True,
        ),
        TilingDesktopTestCase(
            name="display server alone",
            xdg_current_desktop="mir",
            expected=False,
        ),
        TilingDesktopTestCase(
            name="renamed compositor",
            xdg_current_desktop="mangowc",
            expected=False,
        ),
        TilingDesktopTestCase(
            name="non tiling desktop",
            xdg_current_desktop="GNOME",
            expected=False,
        ),
        TilingDesktopTestCase(
            name="empty",
            xdg_current_desktop="",
            expected=False,
        ),
        TilingDesktopTestCase(
            name="unset",
            xdg_current_desktop=None,
            expected=False,
        ),
    ],
    ids=lambda case: case.name,
)
def test_is_tiling_desktop(monkeypatch, case: TilingDesktopTestCase):
    if case.xdg_current_desktop is None:
        monkeypatch.delenv("XDG_CURRENT_DESKTOP", raising=False)
    else:
        monkeypatch.setenv("XDG_CURRENT_DESKTOP", case.xdg_current_desktop)

    assert is_tiling_desktop() is case.expected
