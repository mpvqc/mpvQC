# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Iterable

import inject
from PySide6.QtCore import Property, QObject, QTimer, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.decorators import QmlSingletonInProductionOnly
from mpvqc.services import LabelWidthCalculatorService, PlayerService, SettingsService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming,PyTypeChecker
@QmlElement
@QmlSingletonInProductionOnly
class MpvqcLabelWidthCalculator(QObject):
    _settings: SettingsService = inject.attr(SettingsService)
    _player: PlayerService = inject.attr(PlayerService)
    _width_service: LabelWidthCalculatorService = inject.attr(LabelWidthCalculatorService)

    commentTypesLabelWidthChanged = Signal(int)
    timeLabelWidthChanged = Signal(int)

    def __init__(self, /, parent=None):
        super().__init__(parent)

        self._comment_type_label_width = 0
        self._time_label_width = 0

        self._update_comment_types_label_width()
        self._update_time_label_width()

        self._settings.languageChanged.connect(self._schedule_comment_types_label_width_update)
        self._settings.commentTypesChanged.connect(self._schedule_comment_types_label_width_update)
        self._player.duration_changed.connect(self._schedule_update_time_label_width_update)

    @Property(int, notify=commentTypesLabelWidthChanged)
    def commentTypesLabelWidth(self) -> int:
        return self._comment_type_label_width

    def _schedule_comment_types_label_width_update(self, *_) -> None:
        QTimer.singleShot(0, self._update_comment_types_label_width)

    def _update_comment_types_label_width(self) -> None:
        new_width = self._width_service.calculate_comment_types_width(self._settings.comment_types)
        self._comment_type_label_width = new_width
        self.commentTypesLabelWidthChanged.emit(new_width)

    @Property(int, notify=timeLabelWidthChanged)
    def timeLabelWidth(self) -> int:
        return self._time_label_width

    def _schedule_update_time_label_width_update(self, *_) -> None:
        QTimer.singleShot(0, self._update_time_label_width)

    def _update_time_label_width(self) -> None:
        new_width = self._width_service.calculate_time_width(self._player.duration)
        self._time_label_width = new_width
        self.timeLabelWidthChanged.emit(new_width)

    @Slot(list, result=int)
    def calculateWidthFor(self, labels: Iterable[str]) -> int:
        return self._width_service.calculate_width_for(labels)
