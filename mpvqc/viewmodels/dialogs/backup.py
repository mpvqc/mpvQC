# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject, Signal, Slot
from PySide6.QtGui import QDesktopServices
from PySide6.QtQml import QmlElement

from mpvqc.services import ApplicationPathsService, SettingsService, TypeMapperService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming,PyTypeChecker
@QmlElement
class MpvqcBackupDialogViewModel(QObject):
    _paths: ApplicationPathsService = inject.attr(ApplicationPathsService)
    _settings: SettingsService = inject.attr(SettingsService)
    _type_mapper: TypeMapperService = inject.attr(TypeMapperService)

    temporaryBackupEnabledChanged = Signal(bool)
    temporaryBackupIntervalChanged = Signal(int)

    def __init__(self, /, parent=None):
        super().__init__(parent)
        self._temporary_backup_enabled = self._settings.backup_enabled
        self._temporary_backup_interval = self._settings.backup_interval

    @Property(bool, notify=temporaryBackupEnabledChanged)
    def temporaryBackupEnabled(self) -> bool:
        return self._temporary_backup_enabled

    @temporaryBackupEnabled.setter
    def temporaryBackupEnabled(self, value: bool) -> None:
        if self._temporary_backup_enabled != value:
            self._temporary_backup_enabled = value
            self.temporaryBackupEnabledChanged.emit(value)

    @Property(int, notify=temporaryBackupIntervalChanged)
    def temporaryBackupInterval(self) -> int:
        return self._temporary_backup_interval

    @temporaryBackupInterval.setter
    def temporaryBackupInterval(self, value: int) -> None:
        if self._temporary_backup_interval != value:
            self._temporary_backup_interval = value
            self.temporaryBackupIntervalChanged.emit(value)

    @Property(str, constant=True, final=True)
    def backupDirectory(self) -> str:
        path = self._paths.dir_backup
        return self._type_mapper.map_path_to_str(path)

    @Slot()
    def openBackupDirectory(self):
        path = self._paths.dir_backup
        url = self._type_mapper.map_path_to_url(path)
        QDesktopServices.openUrl(url)

    @Slot()
    def accept(self):
        self._settings.backup_enabled = self._temporary_backup_enabled
        self._settings.backup_interval = self._temporary_backup_interval
