# mpvQC
#
# Copyright (C) 2025 mpvQC developers
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
from PySide6.QtCore import QObject, QRunnable, QThreadPool, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import DocumentBackupService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


class BackupJob(QRunnable):
    _backupper: DocumentBackupService = inject.attr(DocumentBackupService)

    @Slot()
    def run(self):
        self._backupper.backup()


@QmlElement
class MpvqcBackupperBackendPyObject(QObject):
    def __init__(self, /, parent=None):
        super().__init__(parent)
        self._job = BackupJob()
        self._job.setAutoDelete(False)

    @Slot()
    def backup(self):
        QThreadPool.globalInstance().start(self._job)
