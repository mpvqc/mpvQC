# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.controllers import MpvqcAppHeaderViewModel
from mpvqc.services import ResetService, StateService


@pytest.fixture
def reset_service_mock() -> MagicMock:
    return MagicMock(spec_set=ResetService)


@pytest.fixture
def view_model() -> MpvqcAppHeaderViewModel:
    # noinspection PyCallingNonCallable
    return MpvqcAppHeaderViewModel()


@pytest.fixture(autouse=True)
def configure_inject(reset_service_mock, state_service):
    def config(binder: inject.Binder):
        binder.bind(StateService, state_service)
        binder.bind(ResetService, reset_service_mock)

    inject.configure(config, clear=True)


def test_request_reset_app_state(view_model, configure_state, reset_service_mock, make_spy):
    spy = make_spy(view_model.confirmResetRequested)

    configure_state(saved=True)
    view_model.requestResetAppState()
    reset_service_mock.reset.assert_called_once()
    assert spy.count() == 0

    reset_service_mock.reset.reset_mock()
    configure_state(saved=False)
    view_model.requestResetAppState()
    assert spy.count() == 1
    reset_service_mock.reset.assert_not_called()
