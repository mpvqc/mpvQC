# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.services import MainWindowService
from mpvqc.viewmodels import MpvqcWindowRadiusViewModel


@pytest.fixture
def main_window_service_mock():
    return MagicMock(spec_set=MainWindowService)


@pytest.fixture(autouse=True)
def configure_injections(common_bindings_with, main_window_service_mock):
    def custom_bindings(binder: inject.Binder):
        binder.bind(MainWindowService, main_window_service_mock)

    common_bindings_with(custom_bindings)


@pytest.mark.parametrize(
    ("shadow_margin", "expected_radius"),
    [
        (0, 0),
        (88, 8),
        (1, 8),
    ],
)
def test_radius_follows_shadow_margin(main_window_service_mock, shadow_margin, expected_radius):
    main_window_service_mock.shadow_margin = shadow_margin

    # noinspection PyCallingNonCallable
    view_model = MpvqcWindowRadiusViewModel()

    assert view_model.radius == expected_radius
