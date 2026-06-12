# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.services import CommentsService, StateService


@pytest.fixture
def state_service_mock() -> MagicMock:
    return MagicMock(spec_set=StateService)


@pytest.fixture(autouse=True)
def configure_injections(common_bindings_with, state_service_mock):
    def custom_bindings(binder: inject.Binder):
        binder.bind(StateService, state_service_mock)

    common_bindings_with(custom_bindings)


@pytest.fixture
def service(qt_app) -> CommentsService:
    return CommentsService()


def test_mutations_record_change(service, state_service_mock):
    service.add_row(0, "Type")

    state_service_mock.record_change.assert_called_once()


def test_reset_does_not_record_change(service, state_service_mock):
    service.add_row(0, "Type")
    state_service_mock.reset_mock()

    service.reset()

    state_service_mock.record_change.assert_not_called()
