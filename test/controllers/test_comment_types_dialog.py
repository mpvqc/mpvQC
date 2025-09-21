# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.controllers import MpvqcCommentTypesDialogControllerPyObject
from mpvqc.services import CommentTypeValidatorService, ReverseTranslatorService, SettingsService


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
def controller() -> MpvqcCommentTypesDialogControllerPyObject:
    # noinspection PyCallingNonCallable
    return MpvqcCommentTypesDialogControllerPyObject()


def test_initial_state(controller, comment_types):
    # Model should be populated
    assert controller.temporaryCommentTypesModel.rowCount() == len(comment_types)
    assert controller.temporaryCommentTypesModel.stringList() == comment_types

    # Initial properties
    assert controller.textFieldContent == ""
    assert controller.validationError == ""
    assert controller.selectedIndex == 0

    # Buttons should be in idle state
    assert not controller.isAcceptButtonEnabled
    assert not controller.isRejectButtonEnabled
    assert not controller.isMoveUpButtonEnabled  # Can't move first item up
    assert controller.isMoveDownButtonEnabled
    assert controller.isEditButtonEnabled
    assert controller.isDeleteButtonEnabled


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
    controller_override = MpvqcCommentTypesDialogControllerPyObject()

    assert controller_override.temporaryCommentTypesModel.rowCount() == 1
    assert not controller_override.isDeleteButtonEnabled  # Can't delete last item
    assert not controller_override.isMoveUpButtonEnabled
    assert not controller_override.isMoveDownButtonEnabled


def test_idle_to_adding_transition(controller, make_spy):
    clear_text_field_requested_spy = make_spy(controller.clearTextFieldRequested)

    controller.onTextFieldFocusChanged(True)

    # Should clear text field
    assert clear_text_field_requested_spy.count() == 1

    # Should enable reject button, disable accept
    assert controller.isRejectButtonEnabled
    assert not controller.isAcceptButtonEnabled

    # List controls should be disabled
    assert not controller.isMoveUpButtonEnabled
    assert not controller.isMoveDownButtonEnabled
    assert not controller.isEditButtonEnabled
    assert not controller.isDeleteButtonEnabled


def test_adding_to_idle_via_reject(controller, make_spy):
    clear_text_field_requested_spy = make_spy(controller.clearTextFieldRequested)
    focus_text_field_requested_spy = make_spy(controller.focusTextFieldRequested)

    # Enter adding mode
    controller.onTextFieldFocusChanged(True)
    controller.onTextChanged("New Type")

    # Reject
    controller.rejectInput()

    # Should clear and unfocus text field
    assert clear_text_field_requested_spy.count() == 2  # Once for entering add mode, once for reject
    assert focus_text_field_requested_spy.count() == 1
    assert not focus_text_field_requested_spy.at(0, 0)

    # Should return to idle state
    assert controller.textFieldContent == ""
    assert not controller.isAcceptButtonEnabled
    assert not controller.isRejectButtonEnabled


def test_idle_to_editing_transition(controller, make_spy):
    set_text_field_requested_spy = make_spy(controller.setTextFieldRequested)
    focus_text_field_requested_spy = make_spy(controller.focusTextFieldRequested)

    controller.selectItem(1)  # Select second item
    controller.startEdit()

    # Should populate text field with current value
    assert set_text_field_requested_spy.count() == 1
    assert set_text_field_requested_spy.at(0, 0) == "CommentType 2"
    assert focus_text_field_requested_spy.count() == 1
    assert focus_text_field_requested_spy.at(0, 0)

    # Buttons should be in editing state
    assert controller.isAcceptButtonEnabled
    assert controller.isRejectButtonEnabled

    # List controls disabled
    assert not controller.isEditButtonEnabled


def test_add_valid_comment_type(controller, mock_validator, comment_types):
    mock_validator.validate_new_comment_type.return_value = None  # No error

    # Enter adding mode and type
    controller.onTextFieldFocusChanged(True)
    controller.onTextChanged("New Type")

    # Should enable accept button when valid
    assert controller.isAcceptButtonEnabled

    # Accept the input
    controller.acceptInput()

    # Should add to model
    assert controller.temporaryCommentTypesModel.rowCount() == len(comment_types) + 1
    assert "New Type" in controller.temporaryCommentTypesModel.stringList()

    # Should select the new item
    assert controller.selectedIndex == len(comment_types)

    # Should return to idle
    assert controller.textFieldContent == ""


def test_add_with_validation_error(controller, mock_validator, make_spy):
    validation_error_changed_spy = make_spy(controller.validationErrorChanged)
    mock_validator.validate_new_comment_type.return_value = "Duplicate name"

    controller.onTextFieldFocusChanged(True)
    controller.onTextChanged("Duplicate")

    # Should show error
    assert controller.validationError == "Duplicate name"
    assert validation_error_changed_spy.count() == 1
    assert validation_error_changed_spy.at(0, 0) == "Duplicate name"

    # Accept button should be disabled
    assert not controller.isAcceptButtonEnabled

    # Attempting to accept should do nothing
    initial_count = controller.temporaryCommentTypesModel.rowCount()
    controller.acceptInput()
    assert controller.temporaryCommentTypesModel.rowCount() == initial_count


def test_add_empty_not_allowed(controller, mock_validator):
    mock_validator.validate_new_comment_type.return_value = None

    controller.onTextFieldFocusChanged(True)
    controller.onTextChanged("")

    assert not controller.isAcceptButtonEnabled


def test_edit_comment_type(controller, mock_validator, mock_translator):
    mock_validator.validate_editing_of_comment_type.return_value = None

    controller.selectItem(1)
    controller.startEdit()

    # Modify the text
    controller.onTextChanged("Modified Type")

    assert controller.isAcceptButtonEnabled

    # Accept edit
    controller.acceptInput()

    # Should update the model
    updated_list = controller.temporaryCommentTypesModel.stringList()
    assert updated_list[1] == "Modified Type"

    # Should call translator
    mock_translator.lookup.assert_called_with("Modified Type")


def test_edit_with_validation_error(controller, mock_validator):
    mock_validator.validate_editing_of_comment_type.return_value = "Invalid edit"

    controller.selectItem(2)
    controller.startEdit()
    controller.onTextChanged("Bad Edit")

    assert controller.validationError == "Invalid edit"
    assert not controller.isAcceptButtonEnabled


def test_cancel_edit(controller, make_spy):
    clear_text_field_requested_spy = make_spy(controller.clearTextFieldRequested)

    controller.selectItem(1)
    original_value = controller.temporaryCommentTypesModel.stringList()[1]

    controller.startEdit()
    controller.onTextChanged("Changed")
    controller.rejectInput()

    # Should not modify the item
    assert controller.temporaryCommentTypesModel.stringList()[1] == original_value

    # Should return to idle
    assert clear_text_field_requested_spy.count() >= 1


def test_move_item_up(controller):
    original_list = controller.temporaryCommentTypesModel.stringList().copy()

    controller.selectItem(2)  # Select third item
    controller.moveUp()

    updated_list = controller.temporaryCommentTypesModel.stringList()

    # Item should have moved up
    assert updated_list[1] == original_list[2]
    assert updated_list[2] == original_list[1]

    # Selection should follow the item
    assert controller.selectedIndex == 1


def test_move_item_down(controller):
    original_list = controller.temporaryCommentTypesModel.stringList().copy()

    controller.selectItem(1)
    controller.moveDown()

    updated_list = controller.temporaryCommentTypesModel.stringList()

    assert updated_list[1] == original_list[2]
    assert updated_list[2] == original_list[1]
    assert controller.selectedIndex == 2


def test_move_boundaries(controller):
    # First item can't move up
    controller.selectItem(0)
    assert not controller.isMoveUpButtonEnabled

    original_list = controller.temporaryCommentTypesModel.stringList().copy()
    controller.moveUp()  # Should do nothing
    assert controller.temporaryCommentTypesModel.stringList() == original_list

    # Last item can't move down
    last_index = controller.temporaryCommentTypesModel.rowCount() - 1
    controller.selectItem(last_index)
    assert not controller.isMoveDownButtonEnabled

    controller.moveDown()  # Should do nothing
    assert controller.temporaryCommentTypesModel.stringList() == original_list


def test_delete_item(controller):
    initial_count = controller.temporaryCommentTypesModel.rowCount()

    controller.selectItem(2)
    deleted_item = controller.temporaryCommentTypesModel.stringList()[2]

    controller.deleteItem()

    # Item should be removed
    assert controller.temporaryCommentTypesModel.rowCount() == initial_count - 1
    assert deleted_item not in controller.temporaryCommentTypesModel.stringList()

    # Selection should remain valid
    assert controller.selectedIndex == 2 or controller.selectedIndex == initial_count - 2


def test_delete_last_item_updates_selection(controller):
    last_index = controller.temporaryCommentTypesModel.rowCount() - 1
    controller.selectItem(last_index)

    controller.deleteItem()

    # Selection should move to new last item
    assert controller.selectedIndex == controller.temporaryCommentTypesModel.rowCount() - 1


def test_cannot_delete_last_remaining_item(controller):
    # Delete all but one
    while controller.temporaryCommentTypesModel.rowCount() > 1:
        controller.selectItem(0)
        controller.deleteItem()

    assert controller.temporaryCommentTypesModel.rowCount() == 1
    assert not controller.isDeleteButtonEnabled

    # Try to delete - should do nothing
    controller.deleteItem()
    assert controller.temporaryCommentTypesModel.rowCount() == 1


def test_reset_to_defaults(controller, comment_types_reset):
    # Make some changes
    controller.onTextFieldFocusChanged(True)
    controller.onTextChanged("New Item")
    controller.acceptInput()

    controller.selectItem(0)
    controller.deleteItem()

    # Reset
    controller.reset()

    # Should restore defaults
    assert controller.temporaryCommentTypesModel.stringList() == comment_types_reset
    assert controller.selectedIndex == 0

    # Should return to idle state
    assert controller.textFieldContent == ""
    assert not controller.isAcceptButtonEnabled


def test_accept_saves_to_settings(controller, comment_types, mock_settings):
    # Make changes
    controller.onTextFieldFocusChanged(True)
    controller.onTextChanged("New Type")
    controller.acceptInput()

    modified_list = controller.temporaryCommentTypesModel.stringList()

    # Accept dialog
    controller.accept()

    # Should save to settings
    assert mock_settings.comment_types == modified_list == [*comment_types.copy(), "New Type"]


def test_signals_on_selection_change(controller, make_spy):
    selected_index_changed_spy = make_spy(controller.selectedIndexChanged)
    is_move_up_button_enabled_changed_spy = make_spy(controller.isMoveUpButtonEnabledChanged)
    is_move_down_button_enabled_changed_spy = make_spy(controller.isMoveDownButtonEnabledChanged)

    controller.selectItem(3)

    assert selected_index_changed_spy.count() == 1
    assert selected_index_changed_spy.at(0, 0) == 3
    assert is_move_up_button_enabled_changed_spy.count() == 1
    assert is_move_down_button_enabled_changed_spy.count() >= 0


def test_validation_error_signal(controller, mock_validator, make_spy):
    validation_error_changed_spy = make_spy(controller.validationErrorChanged)
    mock_validator.validate_new_comment_type.return_value = "Error message"

    controller.onTextFieldFocusChanged(True)
    controller.onTextChanged("Invalid")

    assert validation_error_changed_spy.count() == 1
    assert validation_error_changed_spy.at(0, 0) == "Error message"

    # Clear error
    mock_validator.validate_new_comment_type.return_value = None
    controller.onTextChanged("Valid")

    # Should emit with empty string
    assert validation_error_changed_spy.count() == 2
    assert validation_error_changed_spy.at(1, 0) == ""


def test_no_focus_change_in_idle(controller, make_spy):
    clear_text_field_requested_spy = make_spy(controller.clearTextFieldRequested)

    controller.onTextFieldFocusChanged(False)

    # Should not emit any signals
    assert clear_text_field_requested_spy.count() == 0
    assert not controller.isRejectButtonEnabled


def test_text_change_in_idle_ignored(controller):
    controller.onTextChanged("Some text")

    # Should not update text field content in idle mode
    assert controller.textFieldContent == ""


def test_operations_blocked_during_editing(controller):
    controller.selectItem(1)
    controller.startEdit()

    # Try list operations - should be blocked
    original_list = controller.temporaryCommentTypesModel.stringList().copy()
    original_index = controller.selectedIndex

    controller.moveUp()
    controller.moveDown()
    controller.deleteItem()

    # Nothing should change
    assert controller.temporaryCommentTypesModel.stringList() == original_list
    assert controller.selectedIndex == original_index


def test_validation_only_after_typing(controller, mock_validator):
    mock_validator.validate_new_comment_type.return_value = "Error"

    controller.onTextFieldFocusChanged(True)

    # No validation yet - user hasn't typed
    assert controller.validationError == ""
    mock_validator.validate_new_comment_type.assert_not_called()

    # Now type something
    controller.onTextChanged("x")

    # Now validation should occur
    assert controller.validationError == "Error"
    mock_validator.validate_new_comment_type.assert_called()
