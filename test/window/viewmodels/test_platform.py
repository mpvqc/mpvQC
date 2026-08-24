# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NamedTuple

import inject
import pytest

from mpvqc.window.services import (
    PlatformCapabilities,
    PlatformService,
    linux_desktop_capabilities,
    windows_capabilities,
)
from mpvqc.window.viewmodels import MpvqcPlatformViewModel


@pytest.fixture
def bind_platform(common_bindings_with, make_platform_service):
    def _bind(capabilities: PlatformCapabilities) -> None:
        platform_service = make_platform_service(capabilities=capabilities)

        def custom_bindings(binder: inject.Binder):
            binder.bind(PlatformService, platform_service)

        common_bindings_with(custom_bindings)

    return _bind


class PlatformCase(NamedTuple):
    name: str
    capabilities: PlatformCapabilities
    keeps_native_frame: bool
    can_draw_own_frame: bool
    embeds_native_player: bool
    popups_need_separate_windows: bool


@pytest.mark.parametrize(
    "case",
    [
        PlatformCase(
            name="windows",
            capabilities=windows_capabilities(),
            keeps_native_frame=True,
            can_draw_own_frame=False,
            embeds_native_player=True,
            popups_need_separate_windows=True,
        ),
        PlatformCase(
            name="linux desktop",
            capabilities=linux_desktop_capabilities(),
            keeps_native_frame=False,
            can_draw_own_frame=True,
            embeds_native_player=False,
            popups_need_separate_windows=False,
        ),
    ],
    ids=lambda case: case.name,
)
def test_platform_flags_forward(bind_platform, case: PlatformCase):
    bind_platform(case.capabilities)

    view_model = MpvqcPlatformViewModel()

    assert view_model.keepsNativeFrame is case.keeps_native_frame
    assert view_model.canDrawOwnFrame is case.can_draw_own_frame
    assert view_model.embedsNativePlayer is case.embeds_native_player
    assert view_model.popupsNeedSeparateWindows is case.popups_need_separate_windows
