# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass
from html import escape
from typing import assert_never

import inject
from PySide6.QtCore import Property, QCoreApplication, QObject, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.shell.services import (
    HOME_URL,
    CheckOutcome,
    NewVersionAvailable,
    ServerError,
    ServerNotReachable,
    UpToDate,
    VersionCheckerService,
)

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@dataclass(frozen=True)
class VersionCheckProps:
    title: str
    text: str


def derive_version_check_props(outcome: CheckOutcome) -> VersionCheckProps:
    # fmt: off
    match outcome:
        case ServerError(code):
            title = QCoreApplication.translate("VersionCheckDialog", "Server Error")
            text = QCoreApplication.translate("VersionCheckDialog", "The server returned error code {}.").format(code)
            return VersionCheckProps(title=title, text=text)
        case ServerNotReachable():
            title = QCoreApplication.translate("VersionCheckDialog", "Server Not Reachable")
            text = QCoreApplication.translate("VersionCheckDialog", "A connection to the server could not be established.")
            return VersionCheckProps(title=title, text=text)
        case NewVersionAvailable(version):
            new_version = f"<i>{escape(version)}</i>"
            home_url = f'<a href="{HOME_URL}">{HOME_URL}</a>'
            title = QCoreApplication.translate("VersionCheckDialog", "New Version Available")
            text = QCoreApplication.translate("VersionCheckDialog", "There is a new version of mpvQC available ({}). Visit {} to download it.") \
                .format(new_version, home_url)
            return VersionCheckProps(title=title, text=text)
        case UpToDate():
            title = "👌"
            text = QCoreApplication.translate("VersionCheckDialog", "You are already using the most recent version of mpvQC!")
            return VersionCheckProps(title=title, text=text)
        case _:
            assert_never(outcome)
    # fmt: on


@QmlElement
class MpvqcVersionCheckMessageBoxViewModel(QObject):
    _checker = inject.attr(VersionCheckerService)

    titleChanged = Signal(str)
    textChanged = Signal(str)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._props = VersionCheckProps(title="", text="")
        self._checker.outcome_ready.connect(self._present)
        self._checker.check()

    @Slot(object)
    def _present(self, outcome: CheckOutcome) -> None:
        new, old = derive_version_check_props(outcome), self._props
        self._props = new
        if new.title != old.title:
            self.titleChanged.emit(new.title)
        if new.text != old.text:
            self.textChanged.emit(new.text)

    @Property(str, notify=titleChanged)
    def title(self) -> str:
        return self._props.title

    @Property(str, notify=textChanged)
    def text(self) -> str:
        return self._props.text
