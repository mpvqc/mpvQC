# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Iterator

import inject
from PySide6.QtCore import Property, QCoreApplication, QObject, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import (
    CommentTypesPolicyService,
    InternationalizationService,
    LabelWidthCalculatorService,
    TimeFormatPolicyService,
)

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


def _time_candidates(*, long_format: bool) -> Iterator[str]:
    pattern = "{0}{0}:" * (3 if long_format else 2)
    return (pattern.format(digit)[:-1] for digit in range(10))


@QmlElement
class MpvqcLabelWidthCalculatorViewModel(QObject):
    _i18n = inject.attr(InternationalizationService)
    _comment_types_policy = inject.attr(CommentTypesPolicyService)
    _time_format_policy = inject.attr(TimeFormatPolicyService)
    _width_service = inject.attr(LabelWidthCalculatorService)

    commentTypesLabelWidthChanged = Signal(int)
    timeLabelWidthChanged = Signal(int)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

        self._comment_types_label_width = self._compute_comment_types_label_width()
        self._time_label_width = self._compute_time_label_width()

        self._i18n.retranslated.connect(self._update_comment_types_label_width)
        self._comment_types_policy.displayable_comment_types_changed.connect(self._update_comment_types_label_width)
        self._time_format_policy.table_long_format_changed.connect(self._update_time_label_width)

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
        types = self._comment_types_policy.displayable_comment_types
        labels = (QCoreApplication.translate("CommentTypes", ct) for ct in types)
        return self._width_service.calculate_width_for(labels)

    def _compute_time_label_width(self) -> int:
        candidates = _time_candidates(long_format=self._time_format_policy.table_long_format)
        return self._width_service.calculate_width_for(candidates)
