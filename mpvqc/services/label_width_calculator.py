# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Iterable
from functools import cached_property

import inject
from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QFontMetricsF

from .font_loader import FontLoaderService


class LabelWidthCalculatorService:
    _font_loader = inject.attr(FontLoaderService)

    @cached_property
    def _font_metrics(self) -> QFontMetricsF:
        return QFontMetricsF(self._font_loader.application_font())

    def calculate_width_for(self, texts: Iterable[str]) -> int:
        if not texts:
            return 0

        max_width = 0.0
        for text in texts:
            bounding_rect = self._font_metrics.tightBoundingRect(text)
            max_width = max(max_width, bounding_rect.width())

        return int(max_width)

    def calculate_comment_types_width(self, comment_types: list[str]) -> int:
        labels = [QCoreApplication.translate("CommentTypes", ct) for ct in comment_types]
        return self.calculate_width_for(labels)

    def calculate_time_width(self, duration: float) -> int:
        hour_format = duration > 60 * 60
        pattern = "{0}{0}:" * (3 if hour_format else 2)
        labels = [pattern.format(i)[:-1] for i in range(10)]
        return self.calculate_width_for(labels)
