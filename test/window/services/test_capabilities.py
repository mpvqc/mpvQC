# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from mpvqc.window.services import (
    PlatformCapabilities,
    linux_desktop_capabilities,
    linux_tiling_capabilities,
    windows_capabilities,
)


def test_windows_capabilities():
    assert windows_capabilities() == PlatformCapabilities(
        keeps_native_frame=True,
        draws_drop_shadow=False,
        embeds_native_player=True,
        sizes_own_window=True,
    )


def test_linux_desktop_capabilities():
    assert linux_desktop_capabilities() == PlatformCapabilities(
        keeps_native_frame=False,
        draws_drop_shadow=True,
        embeds_native_player=False,
        sizes_own_window=True,
    )


def test_linux_tiling_capabilities():
    assert linux_tiling_capabilities() == PlatformCapabilities(
        keeps_native_frame=False,
        draws_drop_shadow=False,
        embeds_native_player=False,
        sizes_own_window=False,
    )
