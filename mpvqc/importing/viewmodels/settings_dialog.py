# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QCoreApplication, QObject, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.importing.services import ImportSettingsService, LoadFoundVideo

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcImportSettingsDialogViewModel(QObject):
    _settings = inject.attr(ImportSettingsService)

    loadFoundVideoChanged = Signal(int)

    def __init__(self, /) -> None:
        super().__init__()
        self._temp_load_found_video = self._settings.import_found_video
        self._options = [
            {
                "text": QCoreApplication.translate("ImportSettingsDialog", "Always"),
                "value": LoadFoundVideo.ALWAYS.value,
            },
            {
                "text": QCoreApplication.translate("ImportSettingsDialog", "Ask every time"),
                "value": LoadFoundVideo.ASK_EVERY_TIME.value,
            },
            {
                "text": QCoreApplication.translate("ImportSettingsDialog", "Never"),
                "value": LoadFoundVideo.NEVER.value,
            },
        ]

    @Property(list, constant=True, final=True)
    def options(self) -> list[dict[str, str | int]]:
        return self._options

    @Property(int, notify=loadFoundVideoChanged)
    def loadFoundVideo(self) -> int:
        return self._temp_load_found_video.value

    @loadFoundVideo.setter
    def loadFoundVideo(self, value: int) -> None:
        setting = LoadFoundVideo(value)
        if self._temp_load_found_video != setting:
            self._temp_load_found_video = setting
            self.loadFoundVideoChanged.emit(value)

    @Slot()
    def accept(self) -> None:
        self._settings.import_found_video = self._temp_load_found_video
