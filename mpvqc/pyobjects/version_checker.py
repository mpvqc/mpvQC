# mpvQC
#
# Copyright (C) 2022 mpvQC developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from typing import Callable

import inject
from PySide6.QtCore import Signal, Slot, Property, QUrl, QThreadPool, QRunnable, QObject
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
    _checker: VersionCheckerService = inject.attr(VersionCheckerService)

    versionChecked = Signal(str, str)

    def get_home_url(self) -> QUrl:
        return QUrl(self._checker.HOME_URL)

    home_url_changed = Signal(QUrl)
    home_url = Property(QUrl, get_home_url, notify=home_url_changed)

    @Slot()
    def check_for_new_version(self) -> None:
        check_runnable = VersionCheckRunnable(self.versionChecked.emit)
        QThreadPool().globalInstance().start(check_runnable)
