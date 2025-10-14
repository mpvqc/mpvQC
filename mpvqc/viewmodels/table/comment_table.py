# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TYPE_CHECKING

import inject
from PySide6.QtCore import Property, QAbstractItemModel, QObject, Signal, Slot
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QmlElement

from mpvqc.services import PlayerService, SettingsService, TimeFormatterService

if TYPE_CHECKING:
    from mpvqc.models import MpvqcCommentModel


QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyTypeChecker,PyPep8Naming
@QmlElement
class MpvqcCommentTableViewModel(QObject):
    _player: PlayerService = inject.attr(PlayerService)
    _settings: SettingsService = inject.attr(SettingsService)
    _time_formatter: TimeFormatterService = inject.attr(TimeFormatterService)

    commentTypesChanged = Signal(list)
    videoDurationChanged = Signal(float)
    modelChanged = Signal()

    copiedToClipboard = Signal(str)

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
        if self._model != value:
            self._model = value
            self.modelChanged.emit()

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
