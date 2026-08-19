# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NamedTuple

import inject
import pytest

from mpvqc.window.services import PlatformService
from mpvqc.window.viewmodels import MpvqcPlatformViewModel


@pytest.fixture(autouse=True)
def configure_injections(common_bindings_with, platform_service_stub, qt_app):
    def custom_bindings(binder: inject.Binder):
        binder.bind(PlatformService, platform_service_stub)

    common_bindings_with(custom_bindings)


class FlagsCase(NamedTuple):
    name: str
    keeps_native_frame: bool
    draws_drop_shadow: bool
    popups_need_separate_windows: bool


@pytest.mark.parametrize(
    "case",
    [
        FlagsCase(
            name="native frame, popups as separate windows",
            keeps_native_frame=True,
            draws_drop_shadow=False,
            popups_need_separate_windows=True,
        ),
        FlagsCase(
            name="drop shadow, popups in-scene",
            keeps_native_frame=False,
            draws_drop_shadow=True,
            popups_need_separate_windows=False,
        ),
    ],
    ids=lambda case: case.name,
)
def test_platform_flags_forward(platform_service_stub, case: FlagsCase):
    platform_service_stub.keeps_native_frame = case.keeps_native_frame
    platform_service_stub.draws_drop_shadow = case.draws_drop_shadow
    platform_service_stub.popups_need_separate_windows = case.popups_need_separate_windows

    view_model = MpvqcPlatformViewModel()

    assert view_model.keepsNativeFrame is case.keeps_native_frame
    assert view_model.drawsDropShadow is case.draws_drop_shadow
    assert view_model.popupsNeedSeparateWindows is case.popups_need_separate_windows
