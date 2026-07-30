# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later


import inject
from PySide6.QtCore import Property, QCoreApplication, QObject, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import (
    InternationalizationService,
    LabelWidthCalculatorService,
    SettingsService,
    TimeFormatPolicyService,
)

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


def _time_candidates(*, long_format: bool) -> list[str]:
    pattern = "{0}{0}:" * (3 if long_format else 2)
    return [pattern.format(digit)[:-1] for digit in range(10)]


@QmlElement
class MpvqcLabelWidthCalculatorViewModel(QObject):
    _settings = inject.attr(SettingsService)
    _i18n = inject.attr(InternationalizationService)
    _policy = inject.attr(TimeFormatPolicyService)
    _width_service = inject.attr(LabelWidthCalculatorService)

    commentTypesLabelWidthChanged = Signal(int)
    timeLabelWidthChanged = Signal(int)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

        self._comment_types_label_width = self._compute_comment_types_label_width()
        self._time_label_width = self._compute_time_label_width()

        self._i18n.retranslated.connect(self._update_comment_types_label_width)
        self._settings.comment_types_changed.connect(self._update_comment_types_label_width)
        self._policy.table_long_format_changed.connect(self._update_time_label_width)

    @Property(int, notify=commentTypesLabelWidthChanged)
    def commentTypesLabelWidth(self) -> int:
        return self._comment_types_label_width

    @Property(int, notify=timeLabelWidthChanged)
    def timeLabelWidth(self) -> int:
        return self._time_label_width

    @Slot()
    def _update_comment_types_label_width(self) -> None:
        value = self._compute_comment_types_label_width()
        if value != self._comment_types_label_width:
            self._comment_types_label_width = value
            self.commentTypesLabelWidthChanged.emit(value)

    @Slot()
    def _update_time_label_width(self) -> None:
        value = self._compute_time_label_width()
        if value != self._time_label_width:
            self._time_label_width = value
            self.timeLabelWidthChanged.emit(value)

    def _compute_comment_types_label_width(self) -> int:
        labels = [QCoreApplication.translate("CommentTypes", ct) for ct in self._settings.comment_types]
        return self._width_service.calculate_width_for(labels)

    def _compute_time_label_width(self) -> int:
        candidates = _time_candidates(long_format=self._policy.table_long_format)
        return self._width_service.calculate_width_for(candidates)
