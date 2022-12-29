#  mpvQC
#
#  Copyright (C) 2022 mpvQC developers
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from pathlib import Path

import inject
from PySide6.QtCore import QUrl, Slot, QObject
from PySide6.QtQml import QmlElement

from mpvqc.services import ApplicationPathsService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcFileSystemHelperPyObject(QObject):
    _paths = inject.attr(ApplicationPathsService)

    @Slot(QUrl, result=str or None)
    def url_to_absolute_path(self, url: QUrl) -> str:
        path = Path(url.toLocalFile())
        return str(path.absolute())

    @Slot(str, result=QUrl or None)
    def absolute_path_to_url(self, file: str) -> QUrl:
        return QUrl.fromLocalFile(file)

    @Slot(QUrl, result=bool or None)
    def url_is_file(self, url: QUrl) -> bool:
        return Path(url.toLocalFile()).absolute().is_file()

    @Slot(QUrl, result=str or None)
    def url_to_filename_without_suffix(self, url: QUrl) -> str:
        return Path(url.toLocalFile()).stem

    @Slot(QUrl, result=QUrl or None)
    def url_to_parent_file_url(self, url: QUrl) -> QUrl:
        path = Path(url.toLocalFile()).absolute()
        return QUrl.fromLocalFile(path.parent)

    @Slot(QUrl, str)
    def write(self, url: QUrl, content: str) -> None:
        path = Path(url.toLocalFile())
        path.write_text(content, encoding='utf-8')
