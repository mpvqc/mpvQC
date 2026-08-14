# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.comments.services import CommentsSettingsService, default_comment_types
from mpvqc.comments.viewmodels import MpvqcCommentTypesDialogViewModel


@pytest.fixture
def comment_types():
    return ["CommentType 1", "CommentType 2", "CommentType 3", "CommentType 4", "CommentType 5"]


@pytest.fixture
def settings_service_mock(comment_types):
    mock = MagicMock(spec_set=CommentsSettingsService)
    mock.comment_types = comment_types.copy()
    return mock


@pytest.fixture(autouse=True)
def configure_inject(
    common_bindings_with,
    settings_service_mock,
):
    def custom_bindings(binder: inject.Binder):
        binder.bind(CommentsSettingsService, settings_service_mock)

    common_bindings_with(custom_bindings)


@pytest.fixture
def view_model() -> MpvqcCommentTypesDialogViewModel:
    # noinspection PyCallingNonCallable
    return MpvqcCommentTypesDialogViewModel()


def test_initial_model_state(view_model, comment_types):
    assert view_model.commentTypesModel.rowCount() == len(comment_types)
    assert view_model.commentTypesModel.stringList() == comment_types


def test_validate_new_accepts_an_unused_name(view_model):
    assert not view_model.validateNew("Something new")


def test_validate_new_checks_the_unsaved_list(view_model):
    view_model.append("New Type")
    assert view_model.validateNew("New Type")


def test_append_adds_item_and_returns_new_index(view_model, comment_types):
    new_index = view_model.append("New Type")
    assert new_index == len(comment_types)
    assert view_model.commentTypesModel.stringList()[-1] == "New Type"


def test_move_swaps_neighbors(view_model, comment_types):
    view_model.move(2, 1)
    updated = view_model.commentTypesModel.stringList()
    assert updated[1] == comment_types[2]
    assert updated[2] == comment_types[1]


def test_move_down_swaps_neighbors(view_model, comment_types):
    view_model.move(1, 2)
    updated = view_model.commentTypesModel.stringList()
    assert updated[1] == comment_types[2]
    assert updated[2] == comment_types[1]


@pytest.mark.parametrize(
    ("from_index", "to_index"),
    [
        (0, 0),
        (-1, 0),
        (0, -1),
        (99, 0),
        (0, 99),
    ],
)
def test_move_no_op_on_invalid_input(view_model, comment_types, from_index, to_index):
    view_model.move(from_index, to_index)
    assert view_model.commentTypesModel.stringList() == comment_types


def test_save_writes_to_settings(view_model, settings_service_mock, comment_types):
    view_model.append("New Type")
    view_model.save()
    assert settings_service_mock.comment_types == [*comment_types, "New Type"]


def test_reset_to_defaults_replaces_list(view_model):
    view_model.append("Garbage")
    view_model.resetToDefaults()
    assert view_model.commentTypesModel.stringList() == default_comment_types()
