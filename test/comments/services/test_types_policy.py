# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
import pytest

from mpvqc.comments.services import CommentsService, CommentsSettingsService, CommentTypesPolicyService


@pytest.fixture
def comments_service() -> CommentsService:
    return inject.instance(CommentsService)


@pytest.fixture(autouse=True)
def configure_inject(common_bindings_with, comments_settings_service):
    def custom_bindings(binder: inject.Binder):
        binder.bind(CommentsSettingsService, comments_settings_service)

    common_bindings_with(custom_bindings)


@pytest.fixture(autouse=True)
def configured_types(comments_settings_service):
    comments_settings_service.comment_types = ["Translation", "Spelling"]


@pytest.fixture
def policy() -> CommentTypesPolicyService:
    return CommentTypesPolicyService()


def test_displayable_types_union_configured_and_document_types(comments_settings_service, comments_service):
    comments_service.add_row(time=0, comment_type="Spelling")
    comments_service.add_row(time=1, comment_type="CustomType")

    policy = CommentTypesPolicyService()

    assert policy.displayable_comment_types == frozenset({"Translation", "Spelling", "CustomType"})


def test_unknown_type_entering_and_leaving_document_emits(policy, comments_service, make_spy):
    spy = make_spy(policy.displayable_comment_types_changed)

    comments_service.add_row(time=0, comment_type="CustomType")

    assert policy.displayable_comment_types == frozenset({"Translation", "Spelling", "CustomType"})
    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == frozenset({"Translation", "Spelling", "CustomType"})

    comments_service.remove_row(0)

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


def test_mutation_keeping_types_does_not_emit(policy, comments_service, make_spy):
    comments_service.add_row(time=0, comment_type="CustomType")
    spy = make_spy(policy.displayable_comment_types_changed)

    comments_service.update_comment(row=0, comment="Edited")

    assert spy.count() == 0


def test_adding_comment_with_configured_type_does_not_emit(policy, comments_service, make_spy):
    spy = make_spy(policy.displayable_comment_types_changed)

    comments_service.add_row(time=0, comment_type="Spelling")

    assert spy.count() == 0


def test_reordering_configured_types_does_not_emit(policy, comments_settings_service, make_spy):
    spy = make_spy(policy.displayable_comment_types_changed)

    comments_settings_service.comment_types = ["Spelling", "Translation"]

    assert spy.count() == 0


def test_removing_configured_type_still_in_document_does_not_emit(
    policy, comments_settings_service, comments_service, make_spy
):
    comments_service.add_row(time=0, comment_type="Spelling")
    spy = make_spy(policy.displayable_comment_types_changed)

    comments_settings_service.comment_types = ["Translation"]

    assert policy.displayable_comment_types == frozenset({"Translation", "Spelling"})
    assert spy.count() == 0
