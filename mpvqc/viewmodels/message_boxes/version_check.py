# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
from html import escape
from typing import TYPE_CHECKING, assert_never

import inject
from PySide6.QtCore import Property, QCoreApplication, QObject, Signal
from PySide6.QtQml import QmlElement

from mpvqc.jobs import Err, Ok, SerialJobRunner
from mpvqc.services import VersionCheckerService
from mpvqc.services.version_checker import (
    HOME_URL,
    CheckOutcome,
    NewVersionAvailable,
    ServerError,
    ServerNotReachable,
    UpToDate,
)

if TYPE_CHECKING:
    from mpvqc.jobs import JobExecutor, Result

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1

logger = logging.getLogger(__name__)


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

    def __init__(self, parent: QObject | None = None, executor: JobExecutor | None = None) -> None:
        super().__init__(parent)
        self._title = ""
        self._text = ""
        self._jobs = SerialJobRunner(executor)
        self._check_for_new_version()

    def _check_for_new_version(self) -> None:
        self._jobs.run(work=self._checker.check_for_new_version, on_result=self._present)

    def _present(self, result: Result[CheckOutcome]) -> None:
        match result:
            case Ok(outcome):
                title, text = present_outcome(outcome)
                self._set_title(title)
                self._set_text(text)
            case Err(error):
                logger.error("Version check failed", exc_info=error)

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
