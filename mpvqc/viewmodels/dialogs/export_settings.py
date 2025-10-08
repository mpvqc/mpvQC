# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import SettingsService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyTypeChecker,PyPep8Naming
@QmlElement
class MpvqcExportSettingsDialogViewModel(QObject):
    _settings: SettingsService = inject.attr(SettingsService)

    nicknameChanged = Signal(str)
    writeHeaderDateChanged = Signal(bool)
    writeHeaderGeneratorChanged = Signal(bool)
    writeHeaderNicknameChanged = Signal(bool)
    writeHeaderVideoPathChanged = Signal(bool)

    def __init__(self, /):
        super().__init__()
        self._temp_nickname = self._settings.nickname
        self._temp_write_header_date = self._settings.write_header_date
        self._temp_write_header_generator = self._settings.write_header_generator
        self._temp_write_header_nickname = self._settings.write_header_nickname
        self._temp_write_header_video_path = self._settings.write_header_video_path

    @Property(str, notify=nicknameChanged)
    def temporaryNickname(self) -> str:
        return self._temp_nickname

    @temporaryNickname.setter
    def temporaryNickname(self, value: str) -> None:
        if self._temp_nickname != value:
            self._temp_nickname = value
            self.nicknameChanged.emit(value)

    @Property(bool, notify=writeHeaderDateChanged)
    def temporaryWriteHeaderDate(self) -> bool:
        return self._temp_write_header_date

    @temporaryWriteHeaderDate.setter
    def temporaryWriteHeaderDate(self, value: bool) -> None:
        if self._temp_write_header_date != value:
            self._temp_write_header_date = value
            self.writeHeaderDateChanged.emit(value)

    @Property(bool, notify=writeHeaderGeneratorChanged)
    def temporaryWriteHeaderGenerator(self) -> bool:
        return self._temp_write_header_generator

    @temporaryWriteHeaderGenerator.setter
    def temporaryWriteHeaderGenerator(self, value: bool) -> None:
        if self._temp_write_header_generator != value:
            self._temp_write_header_generator = value
            self.writeHeaderGeneratorChanged.emit(value)

    @Property(bool, notify=writeHeaderNicknameChanged)
    def temporaryWriteHeaderNickname(self) -> bool:
        return self._temp_write_header_nickname

    @temporaryWriteHeaderNickname.setter
    def temporaryWriteHeaderNickname(self, value: bool) -> None:
        if self._temp_write_header_nickname != value:
            self._temp_write_header_nickname = value
            self.writeHeaderNicknameChanged.emit(value)

    @Property(bool, notify=writeHeaderVideoPathChanged)
    def temporaryWriteHeaderVideoPath(self) -> bool:
        return self._temp_write_header_video_path

    @temporaryWriteHeaderVideoPath.setter
    def temporaryWriteHeaderVideoPath(self, value: bool) -> None:
        if self._temp_write_header_video_path != value:
            self._temp_write_header_video_path = value
            self.writeHeaderVideoPathChanged.emit(value)

    @Slot()
    def accept(self) -> None:
        self._settings.nickname = self._temp_nickname
        self._settings.write_header_date = self._temp_write_header_date
        self._settings.write_header_generator = self._temp_write_header_generator
        self._settings.write_header_nickname = self._temp_write_header_nickname
        self._settings.write_header_video_path = self._temp_write_header_video_path
