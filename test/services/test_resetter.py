# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.comments.services import CommentsService
from mpvqc.services import ResetService, StateService


@pytest.fixture
def comments_service_mock() -> MagicMock:
    return MagicMock(spec_set=CommentsService)


@pytest.fixture
def state_service_mock() -> MagicMock:
    return MagicMock(spec_set=StateService)


@pytest.fixture(autouse=True)
def configure_injections(common_bindings_with, state_service_mock):
    def custom_bindings(binder: inject.Binder):
        binder.bind(StateService, state_service_mock)

    common_bindings_with(custom_bindings)


@pytest.fixture(autouse=True)
def service(comments_service_mock):
    return ResetService(comments_service_mock)


def test_reset(service, comments_service_mock, state_service_mock):
    service.reset()

    comments_service_mock.reset.assert_called_once()
    state_service_mock.record_reset.assert_called_once()
