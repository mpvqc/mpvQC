# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject, QRunnable, QThreadPool, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import DocumentBackupService, SettingsService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


class BackupJob(QRunnable):
    _backupper: DocumentBackupService = inject.attr(DocumentBackupService)

    @Slot()
    def run(self):
        self._backupper.backup()


# noinspection PyTypeChecker,PyPep8Naming
@QmlElement
class MpvqcBackupTimerViewModel(QObject):
    _settings: SettingsService = inject.attr(SettingsService)

    backupEnabledChanged = Signal(bool)
    backupIntervalChanged = Signal(int)

    def __init__(self, /, parent=None):
        super().__init__(parent)

        self._job = BackupJob()
        self._job.setAutoDelete(False)

        self._settings.backupEnabledChanged.connect(self.backupEnabledChanged.emit)
        self._settings.backupIntervalChanged.connect(self.backupIntervalChanged.emit)

    @Property(bool, notify=backupEnabledChanged)
    def backupEnabled(self) -> bool:
        return self._settings.backup_enabled

    @Property(int, notify=backupIntervalChanged)
    def backupInterval(self) -> int:
        return max(self._settings.backup_interval * 1000, 15000)

    @Slot()
    def backup(self):
        QThreadPool.globalInstance().start(self._job)
