# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject, Signal
from PySide6.QtQml import QmlElement

from mpvqc.comments.services import TimeFormatPolicyService

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcCommentTableTimeFormatViewModel(QObject):
    _policy = inject.attr(TimeFormatPolicyService)

    useLongFormatChanged = Signal(bool)

    def __init__(self, /) -> None:
        super().__init__()
        self._policy.table_long_format_changed.connect(self.useLongFormatChanged)

    @Property(bool, notify=useLongFormatChanged)
    def useLongFormat(self) -> bool:
        return self._policy.table_long_format
