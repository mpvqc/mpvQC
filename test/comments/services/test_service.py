# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.comments.models import CommentStore
from mpvqc.comments.services import CommentsService
from mpvqc.session import SessionService


@pytest.fixture
def session_service_mock() -> MagicMock:
    return MagicMock(spec_set=SessionService)


@pytest.fixture(autouse=True)
def configure_injections(common_bindings_with, session_service_mock):
    def custom_bindings(binder: inject.Binder):
        binder.bind(SessionService, session_service_mock)

    common_bindings_with(custom_bindings)


@pytest.fixture
def service(qt_app) -> CommentsService:
    return CommentsService(CommentStore())


def test_mutations_record_change(service, session_service_mock):
    service.add_row(0, "Type")

    session_service_mock.record_change.assert_called_once()


def test_reset_records_no_change(service, session_service_mock):
    service.reset()

    session_service_mock.record_change.assert_not_called()
