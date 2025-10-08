# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import QObject, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import ResetService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyTypeChecker
@QmlElement
class MpvqcResetMessageBoxViewModel(QObject):
    _resetter: ResetService = inject.attr(ResetService)

    @Slot()
    def reset(self):
        self._resetter.reset()
