# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass, field, replace
from enum import Enum, auto

import inject
from PySide6.QtCore import (
    Property,
    QAbstractItemModel,
    QModelIndex,
    QObject,
    QStringListModel,
    Signal,
    SignalInstance,
    Slot,
)
from PySide6.QtQml import QmlElement

from mpvqc.services import CommentTypeValidatorService, ReverseTranslatorService, SettingsService

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


class Mode(Enum):
    IDLE = auto()
    ADDING = auto()
    EDITING = auto()


@dataclass(frozen=True)
class ButtonStates:
    accept: bool = False
    reject: bool = False
    move_up: bool = False
    move_down: bool = False
    edit: bool = False
    delete: bool = False


@dataclass(frozen=True)
class State:
    mode: Mode = field(default=Mode.IDLE)
    selected_index: int = 0
    row_count: int = 0
    text: str = ""
    error: str | None = None
    has_typed: bool = False

    @property
    def has_selection(self) -> bool:
        return 0 <= self.selected_index < self.row_count

    @property
    def validation_error_text(self) -> str:
        return self.error or ""

    @property
    def buttons(self) -> ButtonStates:
        if self.mode is Mode.IDLE:
            return ButtonStates(
                move_up=self.has_selection and self.selected_index > 0,
                move_down=self.has_selection and self.selected_index < self.row_count - 1,
                edit=self.has_selection,
                delete=self.has_selection and self.row_count > 1,
            )
        return ButtonStates(
            accept=bool(self.text) and self.error is None,
            reject=True,
        )


class CommentTypeList:
    _validator: CommentTypeValidatorService = inject.attr(CommentTypeValidatorService)
    _translator: ReverseTranslatorService = inject.attr(ReverseTranslatorService)
    _settings: SettingsService = inject.attr(SettingsService)

    def __init__(self, parent: QObject) -> None:
        self._model = QStringListModel(list(self._settings.comment_types), parent)

    @property
    def qt_model(self) -> QStringListModel:
        return self._model

    def row_count(self) -> int:
        return self._model.rowCount()

    def item_at(self, index: int) -> str:
        return self._model.data(self._model.index(index, 0))

    def append(self, text: str) -> int:
        position = self._model.rowCount()
        self._model.insertRow(position)
        self._model.setData(self._model.index(position, 0), text)
        return position

    def update(self, index: int, text: str) -> None:
        translated = self._translator.lookup(text)
        self._model.setData(self._model.index(index, 0), translated)

    def remove(self, index: int) -> tuple[int, int]:
        self._model.removeRow(index)
        new_count = self._model.rowCount()
        if new_count == 0:
            return new_count, -1
        if index >= new_count:
            return new_count, new_count - 1
        return new_count, index

    def move(self, from_index: int, to_index: int) -> None:
        if from_index == to_index:
            return
        row_count = self._model.rowCount()
        if not (0 <= from_index < row_count and 0 <= to_index < row_count):
            return
        dest_index = to_index + 1 if to_index > from_index else to_index
        self._model.moveRow(QModelIndex(), from_index, QModelIndex(), dest_index)

    def validate_new(self, text: str) -> str | None:
        return self._validator.validate_new_comment_type(text, self._model.stringList())

    def validate_edit(self, text: str, index: int) -> str | None:
        original = self.item_at(index)
        return self._validator.validate_editing_of_comment_type(text, original, self._model.stringList())

    def reset_to_defaults(self) -> None:
        self._model.setStringList(list(self._settings.get_default_comment_types()))

    def save(self) -> None:
        self._settings.comment_types = self._model.stringList()


# noinspection PyPep8Naming,PyTypeChecker
@QmlElement
class MpvqcCommentTypesDialogViewModel(QObject):
    textFieldContentChanged = Signal()
    validationErrorChanged = Signal()
    selectedIndexChanged = Signal()
    isAcceptButtonEnabledChanged = Signal()
    isRejectButtonEnabledChanged = Signal()
    isMoveUpButtonEnabledChanged = Signal()
    isMoveDownButtonEnabledChanged = Signal()
    isEditButtonEnabledChanged = Signal()
    isDeleteButtonEnabledChanged = Signal()

    clearTextFieldRequested = Signal()
    setTextFieldRequested = Signal(str)
    focusTextFieldRequested = Signal(bool)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._items = CommentTypeList(self)
        self._state = State(row_count=self._items.row_count())

    @Property(QAbstractItemModel, constant=True, final=True)
    def temporaryCommentTypesModel(self) -> QStringListModel:
        return self._items.qt_model

    @Property(str, notify=textFieldContentChanged)
    def textFieldContent(self) -> str:
        return self._state.text

    @Property(str, notify=validationErrorChanged)
    def validationError(self) -> str:
        return self._state.validation_error_text

    @Property(int, notify=selectedIndexChanged)
    def selectedIndex(self) -> int:
        return self._state.selected_index

    @Property(bool, notify=isAcceptButtonEnabledChanged)
    def isAcceptButtonEnabled(self) -> bool:
        return self._state.buttons.accept

    @Property(bool, notify=isRejectButtonEnabledChanged)
    def isRejectButtonEnabled(self) -> bool:
        return self._state.buttons.reject

    @Property(bool, notify=isMoveUpButtonEnabledChanged)
    def isMoveUpButtonEnabled(self) -> bool:
        return self._state.buttons.move_up

    @Property(bool, notify=isMoveDownButtonEnabledChanged)
    def isMoveDownButtonEnabled(self) -> bool:
        return self._state.buttons.move_down

    @Property(bool, notify=isEditButtonEnabledChanged)
    def isEditButtonEnabled(self) -> bool:
        return self._state.buttons.edit

    @Property(bool, notify=isDeleteButtonEnabledChanged)
    def isDeleteButtonEnabled(self) -> bool:
        return self._state.buttons.delete

    @Slot(bool)
    def onTextFieldFocusChanged(self, has_focus: bool) -> None:
        if not has_focus or self._state.mode is not Mode.IDLE:
            return
        self._set_state(replace(self._state, mode=Mode.ADDING, text="", error=None, has_typed=False))
        self.clearTextFieldRequested.emit()

    @Slot(str)
    def onTextChanged(self, text: str) -> None:
        s = self._state
        if s.mode is Mode.IDLE:
            return
        typed = s.has_typed or text != s.text
        error = self._validate(s, text) if typed else None
        self._set_state(replace(s, text=text, has_typed=typed, error=error))

    @Slot()
    def acceptInput(self) -> None:
        s = self._state
        if not s.buttons.accept:
            return
        self._set_state(self._commit(s))
        self.clearTextFieldRequested.emit()
        self.focusTextFieldRequested.emit(False)

    @Slot()
    def rejectInput(self) -> None:
        s = self._state
        if s.mode is Mode.IDLE:
            return
        self._set_state(replace(s, mode=Mode.IDLE, text="", error=None, has_typed=False))
        self.clearTextFieldRequested.emit()
        self.focusTextFieldRequested.emit(False)

    @Slot(int)
    def selectItem(self, index: int) -> None:
        s = self._state
        if s.mode is not Mode.IDLE:
            return
        self._set_state(replace(s, selected_index=index))

    @Slot()
    def moveUp(self) -> None:
        s = self._state
        if not s.buttons.move_up:
            return
        idx = s.selected_index
        self._items.move(idx, idx - 1)
        self._set_state(replace(s, selected_index=idx - 1))

    @Slot()
    def moveDown(self) -> None:
        s = self._state
        if not s.buttons.move_down:
            return
        idx = s.selected_index
        self._items.move(idx, idx + 1)
        self._set_state(replace(s, selected_index=idx + 1))

    @Slot()
    def startEdit(self) -> None:
        s = self._state
        if not s.buttons.edit:
            return
        text = self._items.item_at(s.selected_index)
        self._set_state(replace(s, mode=Mode.EDITING, text=text, has_typed=True, error=None))
        self.setTextFieldRequested.emit(text)
        self.focusTextFieldRequested.emit(True)

    @Slot()
    def deleteItem(self) -> None:
        s = self._state
        if not s.buttons.delete:
            return
        new_count, new_index = self._items.remove(s.selected_index)
        self._set_state(replace(s, row_count=new_count, selected_index=new_index))

    @Slot()
    def reset(self) -> None:
        self._items.reset_to_defaults()
        self._set_state(State(row_count=self._items.row_count()))
        self.clearTextFieldRequested.emit()
        self.focusTextFieldRequested.emit(False)

    @Slot()
    def accept(self) -> None:
        self._items.save()

    def _commit(self, s: State) -> State:
        if s.mode is Mode.ADDING:
            new_index = self._items.append(s.text)
            return State(mode=Mode.IDLE, selected_index=new_index, row_count=s.row_count + 1)
        if s.mode is Mode.EDITING:
            self._items.update(s.selected_index, s.text)
            return State(mode=Mode.IDLE, selected_index=s.selected_index, row_count=s.row_count)
        return s

    def _validate(self, s: State, text: str) -> str | None:
        if s.mode is Mode.ADDING:
            return self._items.validate_new(text)
        if s.mode is Mode.EDITING:
            return self._items.validate_edit(text, s.selected_index)
        return None

    def _set_state(self, new_state: State) -> None:
        old = self._state
        if new_state == old:
            return

        self._state = new_state

        self._emit_if_changed(self.textFieldContentChanged, old.text, new_state.text)
        self._emit_if_changed(self.validationErrorChanged, old.validation_error_text, new_state.validation_error_text)
        self._emit_if_changed(self.selectedIndexChanged, old.selected_index, new_state.selected_index)

        old_buttons, new_buttons = old.buttons, new_state.buttons
        self._emit_if_changed(self.isAcceptButtonEnabledChanged, old_buttons.accept, new_buttons.accept)
        self._emit_if_changed(self.isRejectButtonEnabledChanged, old_buttons.reject, new_buttons.reject)
        self._emit_if_changed(self.isMoveUpButtonEnabledChanged, old_buttons.move_up, new_buttons.move_up)
        self._emit_if_changed(self.isMoveDownButtonEnabledChanged, old_buttons.move_down, new_buttons.move_down)
        self._emit_if_changed(self.isEditButtonEnabledChanged, old_buttons.edit, new_buttons.edit)
        self._emit_if_changed(self.isDeleteButtonEnabledChanged, old_buttons.delete, new_buttons.delete)

    @staticmethod
    def _emit_if_changed(signal: SignalInstance, old: object, new: object) -> None:
        if old != new:
            signal.emit()
