# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import assert_never

import inject
from PySide6.QtCore import Property, QAbstractItemModel, QCoreApplication, QObject, Signal, Slot
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QmlElement

from mpvqc.comments.models import CommentStore
from mpvqc.comments.services import (
    AnimatedSelection,
    CommentsService,
    NoViewAction,
    QuickSelection,
    QuickSelectionAndEdit,
    SelectionState,
    ViewAction,
)
from mpvqc.services import PlayerService, SettingsService, TimeFormatterService
from mpvqc.shared import MILLISECONDS_PER_SECOND

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcCommentTableViewModel(QObject):
    _comments = inject.attr(CommentsService)
    _comment_store = inject.attr(CommentStore)
    _player = inject.attr(PlayerService)
    _settings = inject.attr(SettingsService)
    _time_formatter = inject.attr(TimeFormatterService)

    commentTypesChanged = Signal(list)
    videoDurationChanged = Signal(float)

    commentsAboutToBeImported = Signal()

    copiedToClipboard = Signal(str)

    quickSelectionRequested = Signal(int)
    selectionRequested = Signal(int)

    commentEditRequested = Signal(int)

    deleteCommentRequested = Signal(int, int, str, str)  # index, time, commentType, commentText

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._settings.comment_types_changed.connect(self.commentTypesChanged)
        self._player.duration_changed.connect(self.videoDurationChanged)

        self._clipboard = QGuiApplication.clipboard()

        self._comments.view_action.connect(self._on_view_action)
        self._comments.about_to_import.connect(self.commentsAboutToBeImported)

    @Slot(object)
    def _on_view_action(self, action: ViewAction) -> None:
        match action:
            case AnimatedSelection(row=row):
                self.selectionRequested.emit(row)
            case QuickSelection(row=row):
                self.quickSelectionRequested.emit(row)
            case QuickSelectionAndEdit(row=row):
                self.quickSelectionRequested.emit(row)
                self.commentEditRequested.emit(row)
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
        return self._comment_store

    @Property(SelectionState, constant=True, final=True)
    def selection(self) -> SelectionState:
        return self._comments.selection

    @Slot(int)
    def askToDeleteRow(self, index: int) -> None:
        comment = self._comments.comment_at(index)
        self.deleteCommentRequested.emit(index, comment.time, comment.comment_type, comment.comment)

    @Slot(int)
    def jumpToTime(self, time: int) -> None:
        self._player.jump_to(time / MILLISECONDS_PER_SECOND)

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
        time = round(self._player.exact_time_pos * MILLISECONDS_PER_SECOND)
        self._comments.add_row(time, comment_type)

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
