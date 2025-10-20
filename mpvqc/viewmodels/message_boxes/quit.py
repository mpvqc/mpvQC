# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import QObject, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import QuitService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyTypeChecker
@QmlElement
class MpvqcQuitMessageBoxViewModel(QObject):
    _quit: QuitService = inject.attr(QuitService)

    @Slot()
    def quit(self):
        self._quit.confirm_quit_despite_unsaved_changes()
        self._quit.shutdown()
