# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.services import ResetService, StateService


@pytest.fixture
def state_service_mock() -> MagicMock:
    return MagicMock(spec_set=StateService)


@pytest.fixture(autouse=True)
def configure_injections(
    common_bindings_with,
    state_service_mock,
):
    def custom_bindings(binder: inject.Binder):
        binder.bind(StateService, state_service_mock)

    common_bindings_with(custom_bindings)


@pytest.fixture(autouse=True)
def service():
    return ResetService()


def test_reset(service, state_service_mock, make_spy):
    spy = make_spy(service.perform_reset)

    service.reset()

    assert spy.count() == 1
    state_service_mock.reset.assert_called_once()
