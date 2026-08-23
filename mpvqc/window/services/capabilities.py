# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class PlatformCapabilities:
    keeps_native_frame: bool
    can_draw_own_frame: bool
    embeds_native_player: bool
    sizes_own_window: bool
    popups_need_separate_windows: bool


def windows_capabilities() -> PlatformCapabilities:
    return PlatformCapabilities(
        keeps_native_frame=True,
        can_draw_own_frame=False,
        embeds_native_player=True,
        sizes_own_window=True,
        popups_need_separate_windows=True,
    )


def linux_desktop_capabilities() -> PlatformCapabilities:
    return PlatformCapabilities(
        keeps_native_frame=False,
        can_draw_own_frame=True,
        embeds_native_player=False,
        sizes_own_window=True,
        popups_need_separate_windows=False,
    )


def linux_tiling_capabilities() -> PlatformCapabilities:
    return PlatformCapabilities(
        keeps_native_frame=False,
        can_draw_own_frame=False,
        embeds_native_player=False,
        sizes_own_window=False,
        popups_need_separate_windows=False,
    )
