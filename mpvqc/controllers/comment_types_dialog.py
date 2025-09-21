# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from enum import Enum, auto

import inject
from PySide6.QtCore import Property, QAbstractItemModel, QModelIndex, QObject, QStringListModel, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import CommentTypeValidatorService, ReverseTranslatorService, SettingsService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


class TextFieldMode(Enum):
    IDLE = auto()
    ADDING = auto()
    EDITING = auto()


# noinspection PyPep8Naming,PyTypeChecker
@QmlElement
class MpvqcCommentTypesDialogControllerPyObject(QObject):
    _validator: CommentTypeValidatorService = inject.attr(CommentTypeValidatorService)
    _translator: ReverseTranslatorService = inject.attr(ReverseTranslatorService)
    _settings: SettingsService = inject.attr(SettingsService)

    validationErrorChanged = Signal(str)
    textFieldContentChanged = Signal(str)
    selectedIndexChanged = Signal(int)

    isAcceptButtonEnabledChanged = Signal(bool)
    isRejectButtonEnabledChanged = Signal(bool)
    isMoveUpButtonEnabledChanged = Signal(bool)
    isMoveDownButtonEnabledChanged = Signal(bool)
    isEditButtonEnabledChanged = Signal(bool)
    isDeleteButtonEnabledChanged = Signal(bool)

    clearTextFieldRequested = Signal()
    setTextFieldRequested = Signal(str)
    focusTextFieldRequested = Signal(bool)

    def __init__(self, /, parent=None):
        super().__init__(parent)
        self._temporary_comment_types_model = QStringListModel(list(self._settings.comment_types), self)

        self._text_field_content = ""
        self._text_field_mode = TextFieldMode.IDLE
        self._validation_error = ""
        self._has_typed_since_mode_change = False

        self._is_accept_button_enabled = False
        self._is_reject_button_enabled = False

        self._selected_index = 0

        self._is_move_up_button_enabled = False
        self._is_move_down_button_enabled = False
        self._is_edit_button_enabled = False
        self._is_delete_button_enabled = False

        self._transition_to_idle()

    @Property(QAbstractItemModel, constant=True, final=True)
    def temporaryCommentTypesModel(self) -> QStringListModel:
        return self._temporary_comment_types_model

    @Property(str, notify=textFieldContentChanged)
    def textFieldContent(self) -> str:
        return self._text_field_content

    @Property(bool, notify=isAcceptButtonEnabledChanged)
    def isAcceptButtonEnabled(self) -> bool:
        return self._is_accept_button_enabled

    def _set_is_accept_button_enabled(self, value: bool) -> None:
        if value != self._is_accept_button_enabled:
            self._is_accept_button_enabled = value
            self.isAcceptButtonEnabledChanged.emit(value)

    @Property(bool, notify=isRejectButtonEnabledChanged)
    def isRejectButtonEnabled(self) -> bool:
        return self._is_reject_button_enabled

    def _set_is_reject_button_enabled(self, value: bool) -> None:
        if value != self._is_reject_button_enabled:
            self._is_reject_button_enabled = value
            self.isRejectButtonEnabledChanged.emit(value)

    @Property(str, notify=validationErrorChanged)
    def validationError(self) -> str:
        return self._validation_error

    def _set_validation_error(self, error: str) -> None:
        if error != self._validation_error:
            self._validation_error = error
            self.validationErrorChanged.emit(error)

    @Property(int, notify=selectedIndexChanged)
    def selectedIndex(self) -> int:
        return self._selected_index

    def _set_selected_index(self, value: int) -> None:
        if value != self._selected_index:
            self._selected_index = value
            self.selectedIndexChanged.emit(value)

    @Property(bool, notify=isMoveUpButtonEnabledChanged)
    def isMoveUpButtonEnabled(self) -> bool:
        return self._is_move_up_button_enabled

    def _set_is_move_up_button_enabled(self, value: bool) -> None:
        if value != self._is_move_up_button_enabled:
            self._is_move_up_button_enabled = value
            self.isMoveUpButtonEnabledChanged.emit(value)

    @Property(bool, notify=isMoveDownButtonEnabledChanged)
    def isMoveDownButtonEnabled(self) -> bool:
        return self._is_move_down_button_enabled

    def _set_is_move_down_button_enabled(self, value: bool) -> None:
        if value != self._is_move_down_button_enabled:
            self._is_move_down_button_enabled = value
            self.isMoveDownButtonEnabledChanged.emit(value)

    @Property(bool, notify=isEditButtonEnabledChanged)
    def isEditButtonEnabled(self) -> bool:
        return self._is_edit_button_enabled

    def _set_is_edit_button_enabled(self, value: bool) -> None:
        if value != self._is_edit_button_enabled:
            self._is_edit_button_enabled = value
            self.isEditButtonEnabledChanged.emit(value)

    @Property(bool, notify=isDeleteButtonEnabledChanged)
    def isDeleteButtonEnabled(self) -> bool:
        return self._is_delete_button_enabled

    def _set_is_delete_button_enabled(self, value: bool) -> None:
        if value != self._is_delete_button_enabled:
            self._is_delete_button_enabled = value
            self.isDeleteButtonEnabledChanged.emit(value)

    @Slot(bool)
    def onTextFieldFocusChanged(self, has_focus: bool) -> None:
        if has_focus and self._text_field_mode == TextFieldMode.IDLE:
            self._transition_to_add()

    @Slot(str)
    def onTextChanged(self, text: str) -> None:
        if self._text_field_mode == TextFieldMode.IDLE:
            return

        old_content = self._text_field_content
        self._text_field_content = text

        if text != old_content:
            self._has_typed_since_mode_change = True

        self._validate_and_update_input_buttons()

    @Slot()
    def acceptInput(self):
        if not self._text_field_content or self._validation_error:
            return

        if self._text_field_mode == TextFieldMode.ADDING:
            self._add_comment_type()
        elif self._text_field_mode == TextFieldMode.EDITING:
            self._edit_current_comment_type()

        self._transition_to_idle()

    @Slot()
    def rejectInput(self):
        self._transition_to_idle()

    @Slot(int)
    def selectItem(self, index: int) -> None:
        if self._text_field_mode == TextFieldMode.IDLE:
            self._set_selected_index(index)
            self._update_list_control_buttons()

    @Slot()
    def moveUp(self):
        idle_mode = self._text_field_mode == TextFieldMode.IDLE
        model_count = self._temporary_comment_types_model.rowCount()
        in_range = 0 < self._selected_index < model_count

        if idle_mode and in_range:
            self._moveItem(self._selected_index, self._selected_index - 1)
            self._set_selected_index(self._selected_index - 1)
            self._update_list_control_buttons()

    @Slot()
    def moveDown(self):
        idle_mode = self._text_field_mode == TextFieldMode.IDLE
        model_count = self._temporary_comment_types_model.rowCount()
        in_range = 0 <= self._selected_index < model_count - 1

        if idle_mode and in_range:
            self._moveItem(self._selected_index, self._selected_index + 1)
            self._set_selected_index(self._selected_index + 1)
            self._update_list_control_buttons()

    @Slot()
    def startEdit(self):
        idle_mode = self._text_field_mode == TextFieldMode.IDLE
        model_count = self._temporary_comment_types_model.rowCount()
        in_range = 0 <= self._selected_index < model_count

        if idle_mode and in_range:
            self._transition_to_editing()

    @Slot()
    def deleteItem(self):
        idle_mode = self._text_field_mode == TextFieldMode.IDLE
        model_count = self._temporary_comment_types_model.rowCount()
        in_range = 0 <= self._selected_index < model_count

        if idle_mode and in_range and model_count > 1:
            self._temporary_comment_types_model.removeRow(self._selected_index)

            if self._temporary_comment_types_model.rowCount() == 0:
                self._set_selected_index(-1)
            elif self._selected_index >= self._temporary_comment_types_model.rowCount():
                self._set_selected_index(self._temporary_comment_types_model.rowCount() - 1)

            self._update_list_control_buttons()

    @Slot()
    def reset(self):
        initial_items = list(self._settings.get_default_comment_types())
        self._temporary_comment_types_model.setStringList(initial_items)

        self._set_selected_index(0)
        self._transition_to_idle()

    @Slot()
    def accept(self):
        self._settings.comment_types = self._temporary_comment_types_model.stringList()

    def _add_comment_type(self):
        position = self._temporary_comment_types_model.rowCount()
        self._temporary_comment_types_model.insertRow(position)
        index = self._temporary_comment_types_model.index(position, 0)
        self._temporary_comment_types_model.setData(index, self._text_field_content)
        self._set_selected_index(position)

    def _edit_current_comment_type(self):
        index = self._temporary_comment_types_model.index(self._selected_index, 0)
        content = self._translator.lookup(self._text_field_content)
        self._temporary_comment_types_model.setData(index, content)

    def _moveItem(self, from_index: int, to_index: int) -> None:
        if from_index == to_index:
            return

        row_count = self._temporary_comment_types_model.rowCount()
        if not (0 <= from_index < row_count and 0 <= to_index < row_count):
            return

        dest_index = to_index + 1 if to_index > from_index else to_index
        self._temporary_comment_types_model.moveRow(QModelIndex(), from_index, QModelIndex(), dest_index)

    def _transition_to_idle(self):
        self._text_field_mode = TextFieldMode.IDLE
        self._text_field_content = ""
        self.clearTextFieldRequested.emit()
        self.focusTextFieldRequested.emit(False)
        self._set_validation_error("")
        self._set_is_accept_button_enabled(False)
        self._set_is_reject_button_enabled(False)
        self._update_list_control_buttons()

    def _transition_to_add(self):
        self._text_field_mode = TextFieldMode.ADDING
        self._text_field_content = ""
        self.clearTextFieldRequested.emit()
        self._set_validation_error("")
        self._has_typed_since_mode_change = False
        self._set_is_accept_button_enabled(False)
        self._set_is_reject_button_enabled(True)
        self._disable_list_controls()

    def _transition_to_editing(self):
        self._text_field_mode = TextFieldMode.EDITING
        self._has_typed_since_mode_change = True
        self._disable_list_controls()
        self._set_is_accept_button_enabled(True)
        self._set_is_reject_button_enabled(True)
        current_text = self._getItem(self._selected_index)
        self.setTextFieldRequested.emit(current_text)
        self.focusTextFieldRequested.emit(True)

    def _validate_and_update_input_buttons(self):
        error = None

        if self._has_typed_since_mode_change:
            content = self._text_field_content
            temporary_comment_types = self._temporary_comment_types_model.stringList()
            count = self._temporary_comment_types_model.rowCount()

            match self._text_field_mode:
                case TextFieldMode.ADDING:
                    error = self._validator.validate_new_comment_type(content, temporary_comment_types)
                case TextFieldMode.EDITING if 0 <= self._selected_index < count:
                    original = self._getItem(self._selected_index)
                    error = self._validator.validate_editing_of_comment_type(content, original, temporary_comment_types)

        self._set_validation_error(error or "")

        match self._text_field_mode:
            case TextFieldMode.ADDING | TextFieldMode.EDITING:
                self._set_is_accept_button_enabled(bool(self._text_field_content) and error is None)
                self._set_is_reject_button_enabled(True)
            case TextFieldMode.IDLE:
                self._set_is_accept_button_enabled(False)
                self._set_is_reject_button_enabled(False)

    def _update_list_control_buttons(self):
        if self._text_field_mode != TextFieldMode.IDLE:
            self._disable_list_controls()
            return

        model_count = self._temporary_comment_types_model.rowCount()
        has_selection = 0 <= self._selected_index < model_count
        can_move_up = self._selected_index > 0 and has_selection
        can_move_down = has_selection and self._selected_index < model_count - 1

        self._set_is_move_up_button_enabled(can_move_up)
        self._set_is_move_down_button_enabled(can_move_down)
        self._set_is_edit_button_enabled(has_selection)
        self._set_is_delete_button_enabled(has_selection and model_count > 1)

    def _disable_list_controls(self):
        self._set_is_move_up_button_enabled(False)
        self._set_is_move_down_button_enabled(False)
        self._set_is_edit_button_enabled(False)
        self._set_is_delete_button_enabled(False)

    def _getItem(self, index: int) -> str:
        model_index = self._temporary_comment_types_model.index(index, 0)
        return self._temporary_comment_types_model.data(model_index)
