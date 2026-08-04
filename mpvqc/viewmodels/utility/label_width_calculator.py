# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass, replace

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


def _translate_comment_types(types: frozenset[str]) -> tuple[str, ...]:
    # sorted, so that equal type sets always give an equal snapshot: frozenset iteration is hash order
    return tuple(QCoreApplication.translate("CommentTypes", comment_type) for comment_type in sorted(types))


@dataclass(frozen=True)
class LabelWidthCalculatorInputs:
    displayable_comment_types: frozenset[str]
    """The derivation never reads this. The retranslation fold does, to translate the types under the new language."""

    comment_type_labels: tuple[str, ...]
    table_long_format: bool

    def with_types(self, types: frozenset[str]) -> "LabelWidthCalculatorInputs":
        return replace(self, displayable_comment_types=types, comment_type_labels=_translate_comment_types(types))


@dataclass(frozen=True)
class LabelWidthCalculatorProps:
    comment_types_label_width: int
    time_label_width: int


def derive_label_width_calculator_props(
    inputs: LabelWidthCalculatorInputs,
    measure_width: Callable[[Iterable[str]], int],
) -> LabelWidthCalculatorProps:
    return LabelWidthCalculatorProps(
        comment_types_label_width=measure_width(inputs.comment_type_labels),
        time_label_width=measure_width(_time_candidates(long_format=inputs.table_long_format)),
    )


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

        types = self._comment_types_policy.displayable_comment_types
        self._inputs = LabelWidthCalculatorInputs(
            displayable_comment_types=types,
            comment_type_labels=_translate_comment_types(types),
            table_long_format=self._time_format_policy.table_long_format,
        )
        self._props = self._derive()

        self._i18n.retranslated.connect(self._fold_retranslated)
        self._comment_types_policy.displayable_comment_types_changed.connect(self._fold_displayable_comment_types)
        self._time_format_policy.table_long_format_changed.connect(self._fold_table_long_format)

    def _derive(self) -> LabelWidthCalculatorProps:
        return derive_label_width_calculator_props(self._inputs, self._width_service.calculate_width_for)

    @Slot()
    def _fold_retranslated(self) -> None:
        self._update(self._inputs.with_types(self._inputs.displayable_comment_types))

    @Slot(frozenset)
    def _fold_displayable_comment_types(self, value: frozenset[str]) -> None:
        self._update(self._inputs.with_types(value))

    @Slot(bool)
    def _fold_table_long_format(self, value: bool) -> None:
        self._update(replace(self._inputs, table_long_format=value))

    def _update(self, inputs: LabelWidthCalculatorInputs) -> None:
        self._inputs = inputs
        new, old = self._derive(), self._props
        if new == old:
            return
        self._props = new
        if new.comment_types_label_width != old.comment_types_label_width:
            self.commentTypesLabelWidthChanged.emit(new.comment_types_label_width)
        if new.time_label_width != old.time_label_width:
            self.timeLabelWidthChanged.emit(new.time_label_width)

    @Property(int, notify=commentTypesLabelWidthChanged)
    def commentTypesLabelWidth(self) -> int:
        return self._props.comment_types_label_width

    @Property(int, notify=timeLabelWidthChanged)
    def timeLabelWidth(self) -> int:
        return self._props.time_label_width
