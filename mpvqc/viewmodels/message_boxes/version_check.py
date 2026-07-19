# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from html import escape
from typing import assert_never

import inject
from PySide6.QtCore import Property, QCoreApplication, QObject, QRunnable, Qt, QThreadPool, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import VersionCheckerService
from mpvqc.services.version_checker import (
    HOME_URL,
    CheckOutcome,
    NewVersionAvailable,
    ServerError,
    ServerNotReachable,
    UpToDate,
)

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


def present_outcome(outcome: CheckOutcome) -> tuple[str, str]:
    # fmt: off
    match outcome:
        case ServerError(code):
            title = QCoreApplication.translate("VersionCheckDialog", "Server Error")
            text = QCoreApplication.translate("VersionCheckDialog", "The server returned error code {}.").format(code)
            return title, text
        case ServerNotReachable():
            title = QCoreApplication.translate("VersionCheckDialog", "Server Not Reachable")
            text = QCoreApplication.translate("VersionCheckDialog", "A connection to the server could not be established.")
            return title, text
        case NewVersionAvailable(version):
            new_version = f"<i>{escape(version)}</i>"
            home_url = f'<a href="{HOME_URL}">{HOME_URL}</a>'
            title = QCoreApplication.translate("VersionCheckDialog", "New Version Available")
            text = QCoreApplication.translate("VersionCheckDialog", "There is a new version of mpvQC available ({}). Visit {} to download it.") \
                .format(new_version, home_url)
            return title, text
        case UpToDate():
            title = "👌"
            text = QCoreApplication.translate("VersionCheckDialog", "You are already using the most recent version of mpvQC!")
            return title, text
        case _:
            assert_never(outcome)
    # fmt: on


@QmlElement
class MpvqcVersionCheckMessageBoxViewModel(QObject):
    _checker = inject.attr(VersionCheckerService)

    titleChanged = Signal()
    textChanged = Signal()
    _result_ready = Signal(object)  # CheckOutcome union; Qt signals can't carry type aliases

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._title = ""
        self._text = ""
        self._result_ready.connect(self._apply_result, Qt.ConnectionType.QueuedConnection)
        self._check_for_new_version()

    def _check_for_new_version(self) -> None:
        def check_version() -> None:
            outcome = self._checker.check_for_new_version()
            self._result_ready.emit(outcome)

        runnable = QRunnable.create(check_version)
        QThreadPool.globalInstance().start(runnable)

    @Slot(object)
    def _apply_result(self, outcome: CheckOutcome) -> None:
        title, text = present_outcome(outcome)
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
