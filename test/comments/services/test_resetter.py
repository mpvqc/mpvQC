# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.comments.services import CommentsService, ResetService
from mpvqc.session import SessionService


@pytest.fixture
def comments_service_mock() -> MagicMock:
    return MagicMock(spec_set=CommentsService)


@pytest.fixture
def session_service_mock() -> MagicMock:
    return MagicMock(spec_set=SessionService)


@pytest.fixture(autouse=True)
def configure_injections(common_bindings_with, comments_service_mock, session_service_mock):
    def custom_bindings(binder: inject.Binder):
        binder.bind(CommentsService, comments_service_mock)
        binder.bind(SessionService, session_service_mock)

    common_bindings_with(custom_bindings)


@pytest.fixture
def service() -> ResetService:
    return ResetService()


def test_reset(service, comments_service_mock, session_service_mock):
    service.reset()

    comments_service_mock.reset.assert_called_once()
    session_service_mock.record_reset.assert_called_once()
