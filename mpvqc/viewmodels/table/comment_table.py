# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TYPE_CHECKING

import inject
from PySide6.QtCore import Property, QAbstractItemModel, QObject, QPointF, Signal, Slot
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QmlElement

from mpvqc.services import PlayerService, SettingsService

if TYPE_CHECKING:
    from mpvqc.models import MpvqcCommentModel


QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming,PyTypeChecker
@QmlElement
class MpvqcCommentTableViewModel(QObject):
    _player: PlayerService = inject.attr(PlayerService)
    _settings: SettingsService = inject.attr(SettingsService)

    commentTypesChanged = Signal(list)
    videoDurationChanged = Signal(float)
    modelChanged = Signal()

    copiedToClipboard = Signal(str)

    quickSelectionRequested = Signal(int)
    selectionRequested = Signal(int)
    rowEditRequested = Signal(int)
    lastRowSelected = Signal()

    timeEditRequested = Signal(int, int, QPointF)
    commentTypeEditRequested = Signal(int, str, QPointF)
    commentEditRequested = Signal(int)

    showSearchBoxRequested = Signal()
    contextMenuRequested = Signal(int, QPointF)
    deleteCommentRequested = Signal(int, int, str, str)  # index, time, commentType, commentText

    def __init__(self, parent=None):
        super().__init__(parent)
        self._settings.commentTypesChanged.connect(self.commentTypesChanged)
        self._player.duration_changed.connect(self.videoDurationChanged)

        self._clipboard = QGuiApplication.clipboard()
        self._model: MpvqcCommentModel | None = None

    @Property(list, notify=commentTypesChanged)
    def commentTypes(self) -> list[str]:
        return self._settings.comment_types

    @Property(float, notify=videoDurationChanged)
    def videoDuration(self) -> float:
        return self._player.duration

    @Property(QAbstractItemModel, notify=modelChanged)
    def model(self) -> QAbstractItemModel:
        return self._model

    @model.setter
    def model(self, value: QAbstractItemModel) -> None:
        if self._model == value:
            return

        self._model: MpvqcCommentModel = value

        self._model.comments_imported_initial.connect(self.quickSelectionRequested)
        self._model.comments_imported_undo.connect(self.quickSelectionRequested)
        self._model.comments_imported_redo.connect(self.quickSelectionRequested)

        self._model.comments_cleared_undo.connect(self.lastRowSelected)

        self._model.comment_added_initial.connect(self.rowEditRequested)
        self._model.comment_added_undo.connect(self.quickSelectionRequested)
        self._model.comment_added_redo.connect(self.quickSelectionRequested)

        self._model.comment_removed_undo.connect(self.quickSelectionRequested)

        self._model.time_updated_initial.connect(self.selectionRequested)
        self._model.time_updated_undo.connect(self.quickSelectionRequested)
        self._model.time_updated_redo.connect(self.quickSelectionRequested)

        self._model.comment_type_updated_initial.connect(self.quickSelectionRequested)
        self._model.comment_type_updated_undo.connect(self.quickSelectionRequested)

        self._model.comment_updated_initial.connect(self.quickSelectionRequested)
        self._model.comment_updated_undo.connect(self.quickSelectionRequested)

        self.modelChanged.emit()

    @Slot(int)
    def select(self, index: int) -> None:
        self.selectionRequested.emit(index)

    @Slot(int)
    def selectQuickly(self, index: int) -> None:
        self.quickSelectionRequested.emit(index)

    @Slot(int, int, QPointF)
    def startEditingTime(self, index: int, time: int, coordinates: QPointF) -> None:
        self.timeEditRequested.emit(index, time, coordinates)

    @Slot(int, str, QPointF)
    def startEditingCommentType(self, index: int, comment_type: str, coordinates: QPointF) -> None:
        self.commentTypeEditRequested.emit(index, comment_type, coordinates)

    @Slot(int)
    def startEditingComment(self, index: int) -> None:
        self.commentEditRequested.emit(index)

    @Slot()
    def showSearchBox(self) -> None:
        self.showSearchBoxRequested.emit()

    @Slot(int, QPointF)
    def openContextMenu(self, index: int, coordinates: QPointF) -> None:
        self.contextMenuRequested.emit(index, coordinates)

    @Slot(int)
    def askToDeleteRow(self, index: int) -> None:
        time, comment_type, comment = self._model.get_comment(index)
        self.deleteCommentRequested.emit(index, time, comment_type, comment)

    @Slot(int)
    def jumpToTime(self, seconds: int) -> None:
        self._player.jump_to(seconds)

    @Slot()
    def pauseVideo(self) -> None:
        self._player.pause()

    @Slot(int)
    def copyToClipboard(self, row: int) -> None:
        content = self._model.get_clipboard_content(row)
        self._clipboard.setText(content)
        self.copiedToClipboard.emit(content)

    @Slot(str)
    def addRow(self, comment_type: str) -> None:
        self._model.add_row(comment_type)

    @Slot(int)
    def removeRow(self, row: int) -> None:
        self._model.remove_row(row)

    @Slot(int, int)
    def updateTime(self, row: int, new_time: int) -> None:
        self._model.update_time(row, new_time)

    @Slot(int, str)
    def updateCommentType(self, row: int, comment_type: str) -> None:
        self._model.update_comment_type(row, comment_type)

    @Slot(int, str)
    def updateComment(self, row: int, comment: str) -> None:
        self._model.update_comment(row, comment)

    @Slot()
    def undo(self) -> None:
        self._model.undo()

    @Slot()
    def redo(self) -> None:
        self._model.redo()
