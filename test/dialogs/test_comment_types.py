# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.dialogs import MpvqcCommentTypesDialogViewModel
from mpvqc.services import CommentTypeValidatorService, SettingsService


@pytest.fixture
def comment_types():
    return ["CommentType 1", "CommentType 2", "CommentType 3", "CommentType 4", "CommentType 5"]


@pytest.fixture
def comment_types_reset():
    return ["OtherType 1", "OtherType 2", "OtherType 3", "OtherType 4", "OtherType 5"]


@pytest.fixture
def comment_type_validator_service_mock():
    mock = MagicMock(spec_set=CommentTypeValidatorService)
    mock.validate_new_comment_type.return_value = None
    return mock


@pytest.fixture
def settings_service_mock(comment_types, comment_types_reset):
    mock = MagicMock(spec_set=SettingsService)
    mock.comment_types = comment_types.copy()
    mock.default_comment_types.return_value = comment_types_reset.copy()
    return mock


@pytest.fixture(autouse=True)
def configure_inject(
    common_bindings_with,
    comment_type_validator_service_mock,
    settings_service_mock,
):
    def custom_bindings(binder: inject.Binder):
        binder.bind(CommentTypeValidatorService, comment_type_validator_service_mock)
        binder.bind(SettingsService, settings_service_mock)

    common_bindings_with(custom_bindings)


@pytest.fixture
def view_model() -> MpvqcCommentTypesDialogViewModel:
    # noinspection PyCallingNonCallable
    return MpvqcCommentTypesDialogViewModel()


def test_initial_model_state(view_model, comment_types):
    assert view_model.commentTypesModel.rowCount() == len(comment_types)
    assert view_model.commentTypesModel.stringList() == comment_types


def test_validate_new_passes_through_to_service(view_model, comment_type_validator_service_mock, comment_types):
    comment_type_validator_service_mock.validate_new_comment_type.return_value = None
    assert not view_model.validateNew("anything")
    comment_type_validator_service_mock.validate_new_comment_type.assert_called_once_with("anything", comment_types)


def test_validate_new_returns_error_message(view_model, comment_type_validator_service_mock):
    comment_type_validator_service_mock.validate_new_comment_type.return_value = "Duplicate"
    assert view_model.validateNew("anything") == "Duplicate"


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


def test_reset_to_defaults_replaces_list(view_model, comment_types_reset):
    view_model.append("Garbage")
    view_model.resetToDefaults()
    assert view_model.commentTypesModel.stringList() == comment_types_reset
