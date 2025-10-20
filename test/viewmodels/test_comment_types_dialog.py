# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.services import CommentTypeValidatorService, ReverseTranslatorService, SettingsService
from mpvqc.viewmodels import MpvqcCommentTypesDialogViewModel


@pytest.fixture
def comment_types():
    return ["CommentType 1", "CommentType 2", "CommentType 3", "CommentType 4", "CommentType 5"]


@pytest.fixture
def comment_types_reset():
    return ["OtherType 1", "OtherType 2", "OtherType 3", "OtherType 4", "OtherType 5"]


@pytest.fixture
def mock_validator():
    mock = MagicMock(spec_set=CommentTypeValidatorService)
    mock.validate_new_comment_type.return_value = None
    mock.validate_editing_of_comment_type.return_value = None
    return mock


@pytest.fixture
def mock_translator():
    return MagicMock(spec_set=ReverseTranslatorService)


@pytest.fixture
def mock_settings(comment_types, comment_types_reset):
    mock = MagicMock(spec_set=SettingsService)
    mock.comment_types = comment_types.copy()
    mock.get_default_comment_types.return_value = comment_types_reset.copy()
    return mock


@pytest.fixture(autouse=True)
def configure_injections(mock_validator, mock_translator, mock_settings):
    def config(binder: inject.Binder):
        mock_translator.lookup.side_effect = lambda x: x  # Pass through by default
        binder.bind(CommentTypeValidatorService, mock_validator)
        binder.bind(ReverseTranslatorService, mock_translator)
        binder.bind(SettingsService, mock_settings)

    inject.configure(config, clear=True)


@pytest.fixture
def view_model() -> MpvqcCommentTypesDialogViewModel:
    # noinspection PyCallingNonCallable
    return MpvqcCommentTypesDialogViewModel()


def test_initial_state(view_model, comment_types):
    # Model should be populated
    assert view_model.temporaryCommentTypesModel.rowCount() == len(comment_types)
    assert view_model.temporaryCommentTypesModel.stringList() == comment_types

    # Initial properties
    assert view_model.textFieldContent == ""
    assert view_model.validationError == ""
    assert view_model.selectedIndex == 0

    # Buttons should be in idle state
    assert not view_model.isAcceptButtonEnabled
    assert not view_model.isRejectButtonEnabled
    assert not view_model.isMoveUpButtonEnabled  # Can't move first item up
    assert view_model.isMoveDownButtonEnabled
    assert view_model.isEditButtonEnabled
    assert view_model.isDeleteButtonEnabled


def test_initial_state_single_item():
    # Configure with single item
    def config(binder: inject.Binder):
        single_item = ["Only Item"]
        mock_settings = MagicMock(spec_set=SettingsService)
        mock_settings.comment_types = single_item
        mock_settings.get_default_comment_types.return_value = single_item
        binder.bind_to_constructor(SettingsService, lambda: mock_settings)

    inject.configure(config, clear=True)

    # noinspection PyCallingNonCallable
    view_model_override = MpvqcCommentTypesDialogViewModel()

    assert view_model_override.temporaryCommentTypesModel.rowCount() == 1
    assert not view_model_override.isDeleteButtonEnabled  # Can't delete last item
    assert not view_model_override.isMoveUpButtonEnabled
    assert not view_model_override.isMoveDownButtonEnabled


def test_idle_to_adding_transition(view_model, make_spy):
    clear_text_field_requested_spy = make_spy(view_model.clearTextFieldRequested)

    view_model.onTextFieldFocusChanged(True)

    # Should clear text field
    assert clear_text_field_requested_spy.count() == 1

    # Should enable reject button, disable accept
    assert view_model.isRejectButtonEnabled
    assert not view_model.isAcceptButtonEnabled

    # List controls should be disabled
    assert not view_model.isMoveUpButtonEnabled
    assert not view_model.isMoveDownButtonEnabled
    assert not view_model.isEditButtonEnabled
    assert not view_model.isDeleteButtonEnabled


def test_adding_to_idle_via_reject(view_model, make_spy):
    clear_text_field_requested_spy = make_spy(view_model.clearTextFieldRequested)
    focus_text_field_requested_spy = make_spy(view_model.focusTextFieldRequested)

    # Enter adding mode
    view_model.onTextFieldFocusChanged(True)
    view_model.onTextChanged("New Type")

    # Reject
    view_model.rejectInput()

    # Should clear and unfocus text field
    assert clear_text_field_requested_spy.count() == 2  # Once for entering add mode, once for reject
    assert focus_text_field_requested_spy.count() == 1
    assert not focus_text_field_requested_spy.at(0, 0)

    # Should return to idle state
    assert view_model.textFieldContent == ""
    assert not view_model.isAcceptButtonEnabled
    assert not view_model.isRejectButtonEnabled


def test_idle_to_editing_transition(view_model, make_spy):
    set_text_field_requested_spy = make_spy(view_model.setTextFieldRequested)
    focus_text_field_requested_spy = make_spy(view_model.focusTextFieldRequested)

    view_model.selectItem(1)  # Select second item
    view_model.startEdit()

    # Should populate text field with current value
    assert set_text_field_requested_spy.count() == 1
    assert set_text_field_requested_spy.at(0, 0) == "CommentType 2"
    assert focus_text_field_requested_spy.count() == 1
    assert focus_text_field_requested_spy.at(0, 0)

    # Buttons should be in editing state
    assert view_model.isAcceptButtonEnabled
    assert view_model.isRejectButtonEnabled

    # List controls disabled
    assert not view_model.isEditButtonEnabled


def test_add_valid_comment_type(view_model, mock_validator, comment_types):
    mock_validator.validate_new_comment_type.return_value = None  # No error

    # Enter adding mode and type
    view_model.onTextFieldFocusChanged(True)
    view_model.onTextChanged("New Type")

    # Should enable accept button when valid
    assert view_model.isAcceptButtonEnabled

    # Accept the input
    view_model.acceptInput()

    # Should add to model
    assert view_model.temporaryCommentTypesModel.rowCount() == len(comment_types) + 1
    assert "New Type" in view_model.temporaryCommentTypesModel.stringList()

    # Should select the new item
    assert view_model.selectedIndex == len(comment_types)

    # Should return to idle
    assert view_model.textFieldContent == ""


def test_add_with_validation_error(view_model, mock_validator, make_spy):
    validation_error_changed_spy = make_spy(view_model.validationErrorChanged)
    mock_validator.validate_new_comment_type.return_value = "Duplicate name"

    view_model.onTextFieldFocusChanged(True)
    view_model.onTextChanged("Duplicate")

    # Should show error
    assert view_model.validationError == "Duplicate name"
    assert validation_error_changed_spy.count() == 1
    assert validation_error_changed_spy.at(0, 0) == "Duplicate name"

    # Accept button should be disabled
    assert not view_model.isAcceptButtonEnabled

    # Attempting to accept should do nothing
    initial_count = view_model.temporaryCommentTypesModel.rowCount()
    view_model.acceptInput()
    assert view_model.temporaryCommentTypesModel.rowCount() == initial_count


def test_add_empty_not_allowed(view_model, mock_validator):
    mock_validator.validate_new_comment_type.return_value = None

    view_model.onTextFieldFocusChanged(True)
    view_model.onTextChanged("")

    assert not view_model.isAcceptButtonEnabled


def test_edit_comment_type(view_model, mock_validator, mock_translator):
    mock_validator.validate_editing_of_comment_type.return_value = None

    view_model.selectItem(1)
    view_model.startEdit()

    # Modify the text
    view_model.onTextChanged("Modified Type")

    assert view_model.isAcceptButtonEnabled

    # Accept edit
    view_model.acceptInput()

    # Should update the model
    updated_list = view_model.temporaryCommentTypesModel.stringList()
    assert updated_list[1] == "Modified Type"

    # Should call translator
    mock_translator.lookup.assert_called_with("Modified Type")


def test_edit_with_validation_error(view_model, mock_validator):
    mock_validator.validate_editing_of_comment_type.return_value = "Invalid edit"

    view_model.selectItem(2)
    view_model.startEdit()
    view_model.onTextChanged("Bad Edit")

    assert view_model.validationError == "Invalid edit"
    assert not view_model.isAcceptButtonEnabled


def test_cancel_edit(view_model, make_spy):
    clear_text_field_requested_spy = make_spy(view_model.clearTextFieldRequested)

    view_model.selectItem(1)
    original_value = view_model.temporaryCommentTypesModel.stringList()[1]

    view_model.startEdit()
    view_model.onTextChanged("Changed")
    view_model.rejectInput()

    # Should not modify the item
    assert view_model.temporaryCommentTypesModel.stringList()[1] == original_value

    # Should return to idle
    assert clear_text_field_requested_spy.count() >= 1


def test_move_item_up(view_model):
    original_list = view_model.temporaryCommentTypesModel.stringList().copy()

    view_model.selectItem(2)  # Select third item
    view_model.moveUp()

    updated_list = view_model.temporaryCommentTypesModel.stringList()

    # Item should have moved up
    assert updated_list[1] == original_list[2]
    assert updated_list[2] == original_list[1]

    # Selection should follow the item
    assert view_model.selectedIndex == 1


def test_move_item_down(view_model):
    original_list = view_model.temporaryCommentTypesModel.stringList().copy()

    view_model.selectItem(1)
    view_model.moveDown()

    updated_list = view_model.temporaryCommentTypesModel.stringList()

    assert updated_list[1] == original_list[2]
    assert updated_list[2] == original_list[1]
    assert view_model.selectedIndex == 2


def test_move_boundaries(view_model):
    # First item can't move up
    view_model.selectItem(0)
    assert not view_model.isMoveUpButtonEnabled

    original_list = view_model.temporaryCommentTypesModel.stringList().copy()
    view_model.moveUp()  # Should do nothing
    assert view_model.temporaryCommentTypesModel.stringList() == original_list

    # Last item can't move down
    last_index = view_model.temporaryCommentTypesModel.rowCount() - 1
    view_model.selectItem(last_index)
    assert not view_model.isMoveDownButtonEnabled

    view_model.moveDown()  # Should do nothing
    assert view_model.temporaryCommentTypesModel.stringList() == original_list


def test_delete_item(view_model):
    initial_count = view_model.temporaryCommentTypesModel.rowCount()

    view_model.selectItem(2)
    deleted_item = view_model.temporaryCommentTypesModel.stringList()[2]

    view_model.deleteItem()

    # Item should be removed
    assert view_model.temporaryCommentTypesModel.rowCount() == initial_count - 1
    assert deleted_item not in view_model.temporaryCommentTypesModel.stringList()

    # Selection should remain valid
    assert view_model.selectedIndex == 2 or view_model.selectedIndex == initial_count - 2


def test_delete_last_item_updates_selection(view_model):
    last_index = view_model.temporaryCommentTypesModel.rowCount() - 1
    view_model.selectItem(last_index)

    view_model.deleteItem()

    # Selection should move to new last item
    assert view_model.selectedIndex == view_model.temporaryCommentTypesModel.rowCount() - 1


def test_cannot_delete_last_remaining_item(view_model):
    # Delete all but one
    while view_model.temporaryCommentTypesModel.rowCount() > 1:
        view_model.selectItem(0)
        view_model.deleteItem()

    assert view_model.temporaryCommentTypesModel.rowCount() == 1
    assert not view_model.isDeleteButtonEnabled

    # Try to delete - should do nothing
    view_model.deleteItem()
    assert view_model.temporaryCommentTypesModel.rowCount() == 1


def test_reset_to_defaults(view_model, comment_types_reset):
    # Make some changes
    view_model.onTextFieldFocusChanged(True)
    view_model.onTextChanged("New Item")
    view_model.acceptInput()

    view_model.selectItem(0)
    view_model.deleteItem()

    # Reset
    view_model.reset()

    # Should restore defaults
    assert view_model.temporaryCommentTypesModel.stringList() == comment_types_reset
    assert view_model.selectedIndex == 0

    # Should return to idle state
    assert view_model.textFieldContent == ""
    assert not view_model.isAcceptButtonEnabled


def test_accept_saves_to_settings(view_model, comment_types, mock_settings):
    # Make changes
    view_model.onTextFieldFocusChanged(True)
    view_model.onTextChanged("New Type")
    view_model.acceptInput()

    modified_list = view_model.temporaryCommentTypesModel.stringList()

    # Accept dialog
    view_model.accept()

    # Should save to settings
    assert mock_settings.comment_types == modified_list == [*comment_types.copy(), "New Type"]


def test_signals_on_selection_change(view_model, make_spy):
    selected_index_changed_spy = make_spy(view_model.selectedIndexChanged)
    is_move_up_button_enabled_changed_spy = make_spy(view_model.isMoveUpButtonEnabledChanged)
    is_move_down_button_enabled_changed_spy = make_spy(view_model.isMoveDownButtonEnabledChanged)

    view_model.selectItem(3)

    assert selected_index_changed_spy.count() == 1
    assert selected_index_changed_spy.at(0, 0) == 3
    assert is_move_up_button_enabled_changed_spy.count() == 1
    assert is_move_down_button_enabled_changed_spy.count() >= 0


def test_validation_error_signal(view_model, mock_validator, make_spy):
    validation_error_changed_spy = make_spy(view_model.validationErrorChanged)
    mock_validator.validate_new_comment_type.return_value = "Error message"

    view_model.onTextFieldFocusChanged(True)
    view_model.onTextChanged("Invalid")

    assert validation_error_changed_spy.count() == 1
    assert validation_error_changed_spy.at(0, 0) == "Error message"

    # Clear error
    mock_validator.validate_new_comment_type.return_value = None
    view_model.onTextChanged("Valid")

    # Should emit with empty string
    assert validation_error_changed_spy.count() == 2
    assert validation_error_changed_spy.at(1, 0) == ""


def test_no_focus_change_in_idle(view_model, make_spy):
    clear_text_field_requested_spy = make_spy(view_model.clearTextFieldRequested)

    view_model.onTextFieldFocusChanged(False)

    # Should not emit any signals
    assert clear_text_field_requested_spy.count() == 0
    assert not view_model.isRejectButtonEnabled


def test_text_change_in_idle_ignored(view_model):
    view_model.onTextChanged("Some text")

    # Should not update text field content in idle mode
    assert view_model.textFieldContent == ""


def test_operations_blocked_during_editing(view_model):
    view_model.selectItem(1)
    view_model.startEdit()

    # Try list operations - should be blocked
    original_list = view_model.temporaryCommentTypesModel.stringList().copy()
    original_index = view_model.selectedIndex

    view_model.moveUp()
    view_model.moveDown()
    view_model.deleteItem()

    # Nothing should change
    assert view_model.temporaryCommentTypesModel.stringList() == original_list
    assert view_model.selectedIndex == original_index


def test_validation_only_after_typing(view_model, mock_validator):
    mock_validator.validate_new_comment_type.return_value = "Error"

    view_model.onTextFieldFocusChanged(True)

    # No validation yet - user hasn't typed
    assert view_model.validationError == ""
    mock_validator.validate_new_comment_type.assert_not_called()

    # Now type something
    view_model.onTextChanged("x")

    # Now validation should occur
    assert view_model.validationError == "Error"
    mock_validator.validate_new_comment_type.assert_called()
