# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later
from collections.abc import Callable

import inject
from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import VersionCheckerService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


class VersionCheckRunnable(QRunnable):
    _checker: VersionCheckerService = inject.attr(VersionCheckerService)

    def __init__(self, callback: Callable[[str, str], None]):
        super().__init__()
        self._callback = callback

    @Slot()
    def run(self):
        title, text = self._checker.check_for_new_version()
        self._callback(title, text)


@QmlElement
class MpvqcVersionCheckerPyObject(QObject):
    versionChecked = Signal(str, str)

    @Slot()
    def check_for_new_version(self) -> None:
        check_runnable = VersionCheckRunnable(self.versionChecked.emit)
        QThreadPool().globalInstance().start(check_runnable)
