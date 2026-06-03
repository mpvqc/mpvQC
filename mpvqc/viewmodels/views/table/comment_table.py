# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Any, assert_never

import inject
from PySide6.QtCore import Property, QAbstractItemModel, QCoreApplication, QObject, QPointF, Signal, Slot
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QmlElement

from mpvqc.datamodels import Comment
from mpvqc.models.comments import (
    AnimatedSelection,
    CommentsFacade,
    NoViewAction,
    QuickSelection,
    QuickSelectionAndEdit,
    SelectionState,
    ViewAction,
)
from mpvqc.services import CommentsService, PlayerService, SettingsService, StateService, TimeFormatterService

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcCommentTableViewModel(QObject):
    _comments_service = inject.attr(CommentsService)
    _player = inject.attr(PlayerService)
    _settings = inject.attr(SettingsService)
    _state = inject.attr(StateService)
    _time_formatter = inject.attr(TimeFormatterService)

    commentTypesChanged = Signal(list)
    videoDurationChanged = Signal(float)

    commentsAboutToBeImported = Signal()

    copiedToClipboard = Signal(str)

    quickSelectionRequested = Signal(int)
    selectionRequested = Signal(int)

    timeEditRequested = Signal(int, int, QPointF)
    commentTypeEditRequested = Signal(int, str, QPointF)
    commentEditRequested = Signal(int, str)  # index, comment

    contextMenuRequested = Signal(int, QPointF)
    deleteCommentRequested = Signal(int, int, str, str)  # index, time, commentType, commentText
    searchRequested = Signal()

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._settings.comment_types_changed.connect(self.commentTypesChanged)
        self._player.duration_changed.connect(self.videoDurationChanged)

        self._clipboard = QGuiApplication.clipboard()

        self._comments = CommentsFacade(parent=self)
        self._comments.view_action.connect(self._on_view_action)
        self._comments.dirty.connect(self._state.record_change)
        self._comments.about_to_import.connect(self.commentsAboutToBeImported)
        self._comments_service.register(self._comments)

    @Slot(object)
    def _on_view_action(self, action: ViewAction) -> None:
        match action:
            case AnimatedSelection(row=row):
                self.selectionRequested.emit(row)
            case QuickSelection(row=row):
                self.quickSelectionRequested.emit(row)
            case QuickSelectionAndEdit(row=row):
                self.quickSelectionRequested.emit(row)
                self.startEditingComment(row)
            case NoViewAction():
                pass
            case _ as unreachable:
                assert_never(unreachable)

    # pyrefly: ignore [bad-argument-type]
    @Property("QStringList", notify=commentTypesChanged)
    def commentTypes(self) -> list[str]:
        return self._settings.comment_types

    @Property(float, notify=videoDurationChanged)
    def videoDuration(self) -> float:
        return self._player.duration

    @Property(QAbstractItemModel, constant=True, final=True)
    def model(self) -> QAbstractItemModel:
        return self._comments.store

    @Property(SelectionState, constant=True, final=True)
    def selection(self) -> SelectionState:
        return self._comments.selection

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
        comment = self._comments.comment_at(index).comment
        self.commentEditRequested.emit(index, comment)

    @Slot(int, QPointF)
    def openContextMenu(self, index: int, coordinates: QPointF) -> None:
        self.contextMenuRequested.emit(index, coordinates)

    @Slot()
    def openSearchBox(self) -> None:
        self.searchRequested.emit()

    @Slot(int)
    def askToDeleteRow(self, index: int) -> None:
        comment = self._comments.comment_at(index)
        self.deleteCommentRequested.emit(index, comment.time, comment.comment_type, comment.comment)

    @Slot(int)
    def jumpToTime(self, time: int) -> None:
        self._player.jump_to(time / TimeFormatterService.MILLISECONDS_PER_SECOND)

    @Slot()
    def pauseVideo(self) -> None:
        self._player.pause()

    @Slot(int)
    def copyToClipboard(self, row: int) -> None:
        comment = self._comments.comment_at(row)
        time = self._time_formatter.format_milliseconds_to_string(comment.time, long_format=True)
        comment_type = QCoreApplication.translate("CommentTypes", comment.comment_type)
        content = f"[{time}] [{comment_type}] {comment.comment}"
        self._clipboard.setText(content)
        self.copiedToClipboard.emit(content)

    @Slot(str)
    def addRow(self, comment_type: str) -> None:
        self._comments.add_row(self._player.time_pos * TimeFormatterService.MILLISECONDS_PER_SECOND, comment_type)

    @Slot(int)
    def removeRow(self, row: int) -> None:
        self._comments.remove_row(row)

    @Slot(int, int)
    def updateTime(self, row: int, new_time: int) -> None:
        self._comments.update_time(row, new_time)

    @Slot(int, str)
    def updateCommentType(self, row: int, comment_type: str) -> None:
        self._comments.update_comment_type(row, comment_type)

    @Slot(int, str)
    def updateComment(self, row: int, comment: str) -> None:
        self._comments.update_comment(row, comment)

    @Slot()
    def undo(self) -> None:
        self._comments.undo()

    @Slot()
    def redo(self) -> None:
        self._comments.redo()

    @Slot(list)
    def importComments(self, comments: list[dict[str, Any]]) -> None:
        self._comments.import_comments(
            [Comment(time=c["time"], comment_type=c["commentType"], comment=c["comment"]) for c in comments]
        )

    @Slot()
    def clearComments(self) -> None:
        self._comments.clear_comments()

    @Slot(result=list)
    def comments(self) -> list[dict[str, Any]]:
        return self._comments.comments()
