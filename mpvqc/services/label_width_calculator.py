# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Iterable
from functools import cached_property
from math import ceil

import inject
from PySide6.QtGui import QFontMetricsF

from .font_loader import FontLoaderService


class LabelWidthCalculatorService:
    _font_loader = inject.attr(FontLoaderService)

    @cached_property
    def _font_metrics(self) -> QFontMetricsF:
        return QFontMetricsF(self._font_loader.application_font())

    def calculate_width_for(self, texts: Iterable[str]) -> int:
        return ceil(max((self._font_metrics.horizontalAdvance(text) for text in texts), default=0))
