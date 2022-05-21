#  mpvQC
#
#  Copyright (C) 2022 mpvQC developers
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.


from pathlib import Path

from PySide6.QtCore import QUrl, Slot, QObject
from PySide6.QtQml import QmlElement, QmlSingleton

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
@QmlSingleton
class FileIoPyObject(QObject):

    # noinspection PyTypeChecker
    @Slot(QUrl, result=str)
    def abs_path_of(self, url: QUrl) -> str:
        path = Path(url.toLocalFile())
        return str(path.absolute())

    # noinspection PyTypeChecker
    @Slot(QUrl, result=str)
    def stem_of(self, url: QUrl) -> str:
        path = Path(url.toLocalFile())
        return path.stem

    # noinspection PyTypeChecker
    @Slot(QUrl, result=QUrl)
    def parent_of(self, url: QUrl) -> QUrl:
        path = Path(url.toLocalFile()).absolute()
        return QUrl.fromLocalFile(path.parent)

    @Slot(QUrl, str)
    def write(self, url: QUrl, content: str):
        path = Path(url.toLocalFile())
        path.write_text(content, encoding='utf-8')
