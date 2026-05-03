# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import QObject, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import ResetService

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyTypeChecker
@QmlElement
class MpvqcResetMessageBoxViewModel(QObject):
    _resetter = inject.attr(ResetService)

    @Slot()
    def reset(self) -> None:
        self._resetter.reset()
