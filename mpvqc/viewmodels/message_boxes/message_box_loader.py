# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import QObject, Signal
from PySide6.QtQml import QmlElement

from mpvqc.services import ExportService, QuitService

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcMessageBoxLoaderViewModel(QObject):
    _exporter = inject.attr(ExportService)
    _quit = inject.attr(QuitService)

    exportErrorOccurred = Signal(str, int)
    confirmQuit = Signal()

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._exporter.export_error_occurred.connect(self.exportErrorOccurred)
        self._quit.confirmQuit.connect(self.confirmQuit)
