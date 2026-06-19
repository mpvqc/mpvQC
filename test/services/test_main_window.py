# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NamedTuple
from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.services import MainWindowService, PlatformService


@pytest.fixture
def platform_service_mock():
    mock = MagicMock(spec_set=PlatformService)
    mock.draws_own_shadow = True
    return mock


@pytest.fixture(autouse=True)
def configure_injections(common_bindings_with, platform_service_mock):
    def custom_bindings(binder: inject.Binder):
        binder.bind(PlatformService, platform_service_mock)

    common_bindings_with(custom_bindings)


@pytest.fixture
def service() -> MainWindowService:
    return MainWindowService()


class ShadowMarginTestCase(NamedTuple):
    name: str
    draws_own_shadow: bool
    is_fullscreen: bool
    is_maximized: bool
    expected: int


@pytest.mark.parametrize(
    "case",
    [
        ShadowMarginTestCase(
            "normal_window_draws_shadow", draws_own_shadow=True, is_fullscreen=False, is_maximized=False, expected=88
        ),
        ShadowMarginTestCase(
            "no_shadow_no_margin", draws_own_shadow=False, is_fullscreen=False, is_maximized=False, expected=0
        ),
        ShadowMarginTestCase(
            "fullscreen_has_no_margin", draws_own_shadow=True, is_fullscreen=True, is_maximized=False, expected=0
        ),
        ShadowMarginTestCase(
            "maximized_has_no_margin", draws_own_shadow=True, is_fullscreen=False, is_maximized=True, expected=0
        ),
    ],
    ids=lambda case: case.name,
)
def test_compute_shadow_margin(case: ShadowMarginTestCase, service, platform_service_mock):
    platform_service_mock.draws_own_shadow = case.draws_own_shadow
    service._is_fullscreen = case.is_fullscreen
    service._is_maximized = case.is_maximized
    assert service._compute_shadow_margin() == case.expected


def test_width_and_height_subtract_the_shadow_margin(service):
    service._outer_width = 1280
    service._outer_height = 720
    service._shadow_margin = 64
    assert service.content_width == 1280 - 2 * 64
    assert service.content_height == 720 - 2 * 64


def test_width_and_height_equal_surface_without_margin(service):
    service._outer_width = 1280
    service._outer_height = 720
    service._shadow_margin = 0
    assert service.content_width == 1280
    assert service.content_height == 720


def test_refresh_shadow_margin_applies_and_emits_content_size(service, platform_service_mock):
    service._outer_width = 1280
    service._outer_height = 720
    platform_service_mock.draws_own_shadow = True

    margins: list[int] = []
    widths: list[int] = []
    service.shadow_margin_changed.connect(margins.append)
    service.content_width_changed.connect(widths.append)

    service._refresh_shadow_margin()

    assert service.shadow_margin == 88
    platform_service_mock.apply_content_margins.assert_called_once_with(88)
    assert margins == [88]
    assert widths == [1280 - 2 * 88]


def test_refresh_shadow_margin_is_noop_when_unchanged(service, platform_service_mock):
    platform_service_mock.draws_own_shadow = False

    margins: list[int] = []
    service.shadow_margin_changed.connect(margins.append)

    service._refresh_shadow_margin()

    assert service.shadow_margin == 0
    platform_service_mock.apply_content_margins.assert_not_called()
    assert margins == []


def test_on_width_changed_reports_content_width(service):
    service._shadow_margin = 64

    widths: list[int] = []
    service.content_width_changed.connect(widths.append)

    service._on_width_changed(1280)

    assert service.content_width == 1280 - 2 * 64
    assert widths == [1280 - 2 * 64]
