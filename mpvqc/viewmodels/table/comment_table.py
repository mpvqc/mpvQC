# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QCoreApplication, QObject, QPointF, Signal, Slot
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QmlElement

from mpvqc.models import MpvqcCommentModel
from mpvqc.services import PlayerService, SettingsService, TimeFormatterService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming,PyTypeChecker
@QmlElement
class MpvqcCommentTableViewModel(QObject):
    _player: PlayerService = inject.attr(PlayerService)
    _settings: SettingsService = inject.attr(SettingsService)
    _time_formatter: TimeFormatterService = inject.attr(TimeFormatterService)

    commentTypesChanged = Signal(list)
    videoDurationChanged = Signal(float)

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

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._settings.commentTypesChanged.connect(self.commentTypesChanged)
        self._player.duration_changed.connect(self.videoDurationChanged)

        self._clipboard = QGuiApplication.clipboard()

        # noinspection PyCallingNonCallable
        self._model: MpvqcCommentModel = MpvqcCommentModel(parent=self)

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

    @Property(list, notify=commentTypesChanged)
    def commentTypes(self) -> list[str]:
        return self._settings.comment_types

    @Property(float, notify=videoDurationChanged)
    def videoDuration(self) -> float:
        return self._player.duration

    @Property(MpvqcCommentModel, constant=True)
    def model(self) -> MpvqcCommentModel:
        return self._model

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
        comment = self._model.comment_at(index)
        self.deleteCommentRequested.emit(index, comment.time, comment.comment_type, comment.comment)

    @Slot(int)
    def jumpToTime(self, seconds: int) -> None:
        self._player.jump_to(seconds)

    @Slot()
    def pauseVideo(self) -> None:
        self._player.pause()

    @Slot(int)
    def copyToClipboard(self, row: int) -> None:
        comment = self._model.comment_at(row)
        time = self._time_formatter.format_time_to_string(comment.time, long_format=True)
        comment_type = QCoreApplication.translate("CommentTypes", comment.comment_type)
        content = f"[{time}] [{comment_type}] {comment.comment}"
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
