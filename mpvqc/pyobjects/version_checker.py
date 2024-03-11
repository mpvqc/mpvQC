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

import inject
from PySide6.QtCore import Signal, Slot, Property, QUrl
from PySide6.QtGui import QValidator
from PySide6.QtQml import QmlElement

from mpvqc.services import VersionCheckerService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcVersionCheckerPyObject(QValidator):
    _checker: VersionCheckerService = inject.attr(VersionCheckerService)

    #

    def get_home_url(self) -> QUrl:
        return QUrl(self._checker.HOME_URL)

    home_url_changed = Signal(QUrl)
    home_url = Property(QUrl, get_home_url, notify=home_url_changed)

    #

    @Slot(result=dict)
    def check_for_new_version(self) -> dict[str, str]:
        title, text = self._checker.check_for_new_version()
        return {
            'title': title,
            'text': text
        }
