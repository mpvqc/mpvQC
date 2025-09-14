# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

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
