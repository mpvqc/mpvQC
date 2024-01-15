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


from PySide6.QtCore import QObject, Slot, QUrl
from PySide6.QtQml import QmlElement

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcExtendedDocumentExporterPyObject(QObject):

    @Slot(list, dict, result=str)
    def create_file_content(self, comments: list, options: dict) -> str:
        for comment in comments:
            print("PYTHON comment", comment)
        print("PYTHON # comments", len(comments))
        print("PYTHON options", options)

        video: QUrl = options['video']
        print("PYTHON Video path", video.path())

        return 'return value'
