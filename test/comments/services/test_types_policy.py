# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
import pytest
from PySide6.QtCore import QObject, Signal

from mpvqc.comments.services import CommentsService, CommentsSettingsService, CommentTypesPolicyService


class CommentsServiceMock(QObject):
    """Doubles the comments service surface the policy consumes: a real signal, a stubbed accessor."""

    comments_changed = Signal()

    def __init__(self):
        super().__init__()
        assert isinstance(CommentsService.comments_changed, Signal), "mocked surface drifted: not a signal anymore"
        assert isinstance(CommentsService.distinct_comment_types, property), (
            "mocked surface drifted: not a property anymore"
        )
        self._types: frozenset[str] = frozenset()

    @property
    def distinct_comment_types(self) -> frozenset[str]:
        return self._types

    def mutate_comments(self, *types: str) -> None:
        """Simulates any committed document mutation, leaving these types present."""
        self._types = frozenset(types)
        self.comments_changed.emit()


@pytest.fixture
def comments_service_mock() -> CommentsServiceMock:
    return CommentsServiceMock()


@pytest.fixture(autouse=True)
def configure_inject(common_bindings_with, comments_settings_service, comments_service_mock):
    def custom_bindings(binder: inject.Binder):
        binder.bind(CommentsSettingsService, comments_settings_service)
        binder.bind(CommentsService, comments_service_mock)

    common_bindings_with(custom_bindings)


@pytest.fixture(autouse=True)
def configured_types(comments_settings_service):
    comments_settings_service.comment_types = ["Translation", "Spelling"]


@pytest.fixture
def policy() -> CommentTypesPolicyService:
    return CommentTypesPolicyService()


def test_displayable_types_union_configured_and_document_types(comments_settings_service, comments_service_mock):
    comments_service_mock.mutate_comments("Spelling", "CustomType")

    policy = CommentTypesPolicyService()

    assert policy.displayable_comment_types == frozenset({"Translation", "Spelling", "CustomType"})


def test_unknown_type_entering_and_leaving_document_emits(policy, comments_service_mock, make_spy):
    spy = make_spy(policy.displayable_comment_types_changed)

    comments_service_mock.mutate_comments("CustomType")

    assert policy.displayable_comment_types == frozenset({"Translation", "Spelling", "CustomType"})
    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == frozenset({"Translation", "Spelling", "CustomType"})

    comments_service_mock.mutate_comments()

    assert policy.displayable_comment_types == frozenset({"Translation", "Spelling"})
    assert spy.count() == 2
    assert spy.at(invocation=1, argument=0) == frozenset({"Translation", "Spelling"})


def test_configured_type_list_change_emits(policy, comments_settings_service, make_spy):
    spy = make_spy(policy.displayable_comment_types_changed)

    comments_settings_service.comment_types = ["Translation", "Spelling", "Timing"]

    assert policy.displayable_comment_types == frozenset({"Translation", "Spelling", "Timing"})
    assert spy.count() == 1

    comments_settings_service.comment_types = ["Translation"]

    assert policy.displayable_comment_types == frozenset({"Translation"})
    assert spy.count() == 2


def test_mutation_keeping_types_does_not_emit(policy, comments_service_mock, make_spy):
    comments_service_mock.mutate_comments("CustomType")
    spy = make_spy(policy.displayable_comment_types_changed)

    comments_service_mock.mutate_comments("CustomType")

    assert spy.count() == 0


def test_adding_comment_with_configured_type_does_not_emit(policy, comments_service_mock, make_spy):
    spy = make_spy(policy.displayable_comment_types_changed)

    comments_service_mock.mutate_comments("Spelling")

    assert spy.count() == 0


def test_reordering_configured_types_does_not_emit(policy, comments_settings_service, make_spy):
    spy = make_spy(policy.displayable_comment_types_changed)

    comments_settings_service.comment_types = ["Spelling", "Translation"]

    assert spy.count() == 0


def test_removing_configured_type_still_in_document_does_not_emit(
    policy, comments_settings_service, comments_service_mock, make_spy
):
    comments_service_mock.mutate_comments("Spelling")
    spy = make_spy(policy.displayable_comment_types_changed)

    comments_settings_service.comment_types = ["Translation"]

    assert policy.displayable_comment_types == frozenset({"Translation", "Spelling"})
    assert spy.count() == 0
