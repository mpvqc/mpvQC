# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject, QRunnable, Qt, QThreadPool, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import VersionCheckerService

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcVersionCheckMessageBoxViewModel(QObject):
    _checker = inject.attr(VersionCheckerService)

    titleChanged = Signal()
    textChanged = Signal()
    _result_ready = Signal(str, str)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._title = ""
        self._text = ""
        self._result_ready.connect(self._apply_result, Qt.ConnectionType.QueuedConnection)
        self._check_for_new_version()

    def _check_for_new_version(self) -> None:
        def check_version() -> None:
            title, text = self._checker.check_for_new_version()
            self._result_ready.emit(title, text)

        runnable = QRunnable.create(check_version)
        QThreadPool.globalInstance().start(runnable)

    @Slot(str, str)
    def _apply_result(self, title: str, text: str) -> None:
        self._set_title(title)
        self._set_text(text)

    @Property(str, notify=titleChanged)
    def title(self) -> str:
        return self._title

    def _set_title(self, value: str) -> None:
        if self._title != value:
            self._title = value
            self.titleChanged.emit()

    @Property(str, notify=textChanged)
    def text(self) -> str:
        return self._text

    def _set_text(self, value: str) -> None:
        if self._text != value:
            self._text = value
            self.textChanged.emit()
