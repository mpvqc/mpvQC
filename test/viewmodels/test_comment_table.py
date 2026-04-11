# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.datamodels import Comment
from mpvqc.models.comments.mutation import (
    AnimatedSelection,
    LastRowSelection,
    NoViewAction,
    QuickSelection,
    RowAddEdit,
)
from mpvqc.services import CommentsService, PlayerService, SettingsService, StateService
from mpvqc.viewmodels import MpvqcCommentTableViewModel


@pytest.fixture
def comments_service_mock():
    return MagicMock(spec_set=CommentsService)


@pytest.fixture
def state_service_mock():
    return MagicMock(spec_set=StateService)


@pytest.fixture(autouse=True)
def configure_inject(
    common_bindings_with,
    player_service_mock,
    settings_service,
    comments_service_mock,
    state_service_mock,
):
    def custom_bindings(binder: inject.Binder):
        binder.bind(CommentsService, comments_service_mock)
        binder.bind(PlayerService, player_service_mock)
        binder.bind(StateService, state_service_mock)
        binder.bind(SettingsService, settings_service)

    common_bindings_with(custom_bindings)


@pytest.fixture(autouse=True)
def qt_app_must_be_running(qt_app):
    pass


@pytest.fixture
def make_view_model():
    def _make(comments: list[Comment]):
        # noinspection PyCallingNonCallable
        vm = MpvqcCommentTableViewModel()
        # pyrefly: ignore [missing-attribute]
        vm.model.import_comments(tuple(comments))
        return vm

    return _make


def test_registers_comments_service_on_construction(make_view_model, comments_service_mock):
    vm = make_view_model(comments=[])
    comments_service_mock.register.assert_called_once_with(vm.model)


def test_state_changes_on_mutation(make_view_model, state_service_mock):
    vm = make_view_model(comments=[Comment(time=0, comment_type="Type", comment="text")])
    vm.removeRow(0)
    assert state_service_mock.change.call_count == 1

    vm.undo()
    assert state_service_mock.change.call_count == 2


def test_copy_to_clipboard(make_view_model, make_spy):
    vm = make_view_model(
        comments=[
            Comment(time=100, comment_type="Phrasing", comment="Comment Content 1"),
            Comment(time=200, comment_type="Translation", comment="Comment Content 2"),
            Comment(time=300, comment_type="Spelling", comment="Comment Content 3"),
        ]
    )

    spy = make_spy(vm.copiedToClipboard)

    vm.copyToClipboard(0)
    assert spy.at(0, 0) == "[00:01:40] [Phrasing] Comment Content 1"

    vm.copyToClipboard(1)
    assert spy.at(1, 0) == "[00:03:20] [Translation] Comment Content 2"

    vm.copyToClipboard(2)
    assert spy.at(2, 0) == "[00:05:00] [Spelling] Comment Content 3"


def test_on_mutated_quick_selection(make_view_model, make_spy):
    vm = make_view_model(comments=[])
    spy = make_spy(vm.quickSelectionRequested)

    vm._on_mutated(QuickSelection(row=3))

    assert spy.count() == 1
    assert spy.at(0, 0) == 3


def test_on_mutated_animated_selection(make_view_model, make_spy):
    vm = make_view_model(comments=[])
    spy = make_spy(vm.selectionRequested)

    vm._on_mutated(AnimatedSelection(row=7))

    assert spy.count() == 1
    assert spy.at(0, 0) == 7


def test_on_mutated_row_add_edit(make_view_model, make_spy):
    vm = make_view_model(
        comments=[
            Comment(time=0, comment_type="Type", comment="text"),
            Comment(time=1, comment_type="Type", comment="text"),
        ]
    )
    quick_spy = make_spy(vm.quickSelectionRequested)
    edit_spy = make_spy(vm.commentEditRequested)

    vm._on_mutated(RowAddEdit(row=1))

    assert quick_spy.count() == 1
    assert quick_spy.at(0, 0) == 1
    assert edit_spy.count() == 1
    assert edit_spy.at(0, 0) == 1


def test_on_mutated_last_row_selection(make_view_model, make_spy):
    vm = make_view_model(comments=[])
    spy = make_spy(vm.quickSelectionRequested)

    vm._on_mutated(LastRowSelection(row=4))

    assert spy.count() == 1
    assert spy.at(0, 0) == 4


def test_on_mutated_no_view_action(make_view_model, make_spy):
    vm = make_view_model(comments=[])
    quick_spy = make_spy(vm.quickSelectionRequested)
    selection_spy = make_spy(vm.selectionRequested)

    vm._on_mutated(NoViewAction(marks_unsaved=True))

    assert quick_spy.count() == 0
    assert selection_spy.count() == 0


def test_on_mutated_marks_unsaved(make_view_model, state_service_mock):
    vm = make_view_model(comments=[])

    vm._on_mutated(QuickSelection(row=0, marks_unsaved=True))

    state_service_mock.change.assert_called_once()


def test_on_mutated_does_not_mark_unsaved(make_view_model, state_service_mock):
    vm = make_view_model(comments=[])

    vm._on_mutated(QuickSelection(row=0, marks_unsaved=False))

    state_service_mock.change.assert_not_called()
