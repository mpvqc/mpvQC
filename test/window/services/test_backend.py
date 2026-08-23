# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
from types import ModuleType
from typing import NamedTuple

import pytest

from mpvqc.window.services import PlatformCapabilities, select_platform_backend
from mpvqc.window.services.linux import WindowButtonDetector

WINDOWS_PACKAGE = "mpvqc.window.services.windows"


class Win32Stub:
    pass


class StubWindowsPackage(ModuleType):
    """The real package binds Win32 through ctypes, which no other platform can import."""

    def __init__(self) -> None:
        super().__init__(WINDOWS_PACKAGE)
        self.WindowsFrameIntegration = Win32Stub
        self.WindowsWindowStateHandler = Win32Stub
        self.WindowRevealFilter = Win32Stub


@pytest.fixture(autouse=True)
def stub_the_windows_collaborators(monkeypatch):
    monkeypatch.setitem(sys.modules, WINDOWS_PACKAGE, StubWindowsPackage())


@pytest.fixture(autouse=True)
def skip_window_button_detection(monkeypatch):
    monkeypatch.setattr(WindowButtonDetector, "detect", lambda _self: None)


class BackendCase(NamedTuple):
    name: str
    platform: str
    desktop: str
    capabilities: PlatformCapabilities


BACKENDS = [
    BackendCase(
        name="Windows",
        platform="win32",
        desktop="",
        capabilities=PlatformCapabilities(
            keeps_native_frame=True,
            can_draw_own_frame=False,
            embeds_native_player=True,
            sizes_own_window=True,
            popups_need_separate_windows=True,
        ),
    ),
    BackendCase(
        name="Linux tiling desktop",
        platform="linux",
        desktop="niri",
        capabilities=PlatformCapabilities(
            keeps_native_frame=False,
            can_draw_own_frame=False,
            embeds_native_player=False,
            sizes_own_window=False,
            popups_need_separate_windows=False,
        ),
    ),
    BackendCase(
        name="Linux desktop",
        platform="linux",
        desktop="GNOME",
        capabilities=PlatformCapabilities(
            keeps_native_frame=False,
            can_draw_own_frame=True,
            embeds_native_player=False,
            sizes_own_window=True,
            popups_need_separate_windows=False,
        ),
    ),
]


@pytest.mark.parametrize("case", BACKENDS, ids=lambda case: case.name)
def test_selected_backend_carries_its_capabilities(case: BackendCase, monkeypatch):
    monkeypatch.setattr(sys, "platform", case.platform)
    monkeypatch.setenv("XDG_CURRENT_DESKTOP", case.desktop)

    backend = select_platform_backend()

    assert backend.capabilities == case.capabilities
