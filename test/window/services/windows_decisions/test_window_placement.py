# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NamedTuple

import pytest

from mpvqc.window.services.windows_decisions import Rect, WindowPlacement

SW_HIDE = 0
SW_SHOWNORMAL = 1
SW_SHOWMINIMIZED = 2
SW_SHOWMAXIMIZED = 3

WPF_SETMINPOSITION = 0x0001
WPF_RESTORETOMAXIMIZED = 0x0002
WPF_ASYNCWINDOWPLACEMENT = 0x0004

NORMAL_RECT: Rect = (100, 100, 900, 700)


def placement(*, flags: int = 0, show_cmd: int = SW_SHOWNORMAL) -> WindowPlacement:
    return WindowPlacement(
        flags=flags,
        show_cmd=show_cmd,
        min_position=(-1, -1),
        max_position=(-1, -1),
        normal_rect=NORMAL_RECT,
    )


class ShowCase(NamedTuple):
    name: str
    show_cmd: int
    expected: bool


@pytest.mark.parametrize(
    "case",
    [
        ShowCase(name="maximized", show_cmd=SW_SHOWMAXIMIZED, expected=True),
        ShowCase(name="normal", show_cmd=SW_SHOWNORMAL, expected=False),
        ShowCase(name="minimized", show_cmd=SW_SHOWMINIMIZED, expected=False),
        ShowCase(name="hidden", show_cmd=SW_HIDE, expected=False),
    ],
    ids=lambda case: case.name,
)
def test_shows_maximized_reads_the_show_command(case: ShowCase):
    assert placement(show_cmd=case.show_cmd).shows_maximized is case.expected


class RestoreCase(NamedTuple):
    name: str
    flags: int
    expected: bool


@pytest.mark.parametrize(
    "case",
    [
        RestoreCase(
            name="no_flags",
            flags=0,
            expected=False,
        ),
        RestoreCase(
            name="the_restore_flag_alone",
            flags=WPF_RESTORETOMAXIMIZED,
            expected=True,
        ),
        RestoreCase(
            name="another_flag_alone",
            flags=WPF_SETMINPOSITION,
            expected=False,
        ),
        RestoreCase(
            name="the_restore_flag_beside_a_lower_one",
            flags=WPF_SETMINPOSITION | WPF_RESTORETOMAXIMIZED,
            expected=True,
        ),
        RestoreCase(
            name="the_restore_flag_beside_a_higher_one",
            flags=WPF_RESTORETOMAXIMIZED | WPF_ASYNCWINDOWPLACEMENT,
            expected=True,
        ),
    ],
    ids=lambda case: case.name,
)
def test_restores_to_maximized_reads_one_bit_out_of_the_flags(case: RestoreCase):
    # A minimized window keeps the show command of its minimized state, so what
    # it would come back to is only ever in the flags.
    assert placement(flags=case.flags).restores_to_maximized is case.expected
