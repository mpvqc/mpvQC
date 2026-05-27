# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject, QThreadPool, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import DocumentBackupService, SettingsService

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcBackupTimerViewModel(QObject):
    _settings = inject.attr(SettingsService)
    _backupper = inject.attr(DocumentBackupService)

    MIN_INTERVAL_MS = 15000

    backupEnabledChanged = Signal(bool)
    backupIntervalChanged = Signal(int)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._settings.backup_enabled_changed.connect(self.backupEnabledChanged)
        self._settings.backup_interval_changed.connect(self.backupIntervalChanged)

    @Property(bool, notify=backupEnabledChanged)
    def backupEnabled(self) -> bool:
        return self._settings.backup_enabled

    @Property(int, notify=backupIntervalChanged)
    def backupInterval(self) -> int:
        return max(self._settings.backup_interval * 1000, self.MIN_INTERVAL_MS)

    @Slot()
    def backup(self) -> None:
        QThreadPool.globalInstance().start(self._backupper.backup)
