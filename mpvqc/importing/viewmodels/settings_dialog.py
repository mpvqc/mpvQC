# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.importing.domain import ImportFoundVideo
from mpvqc.importing.services import ImportSettingsService

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcImportSettingsDialogViewModel(QObject):
    _settings = inject.attr(ImportSettingsService)

    importFoundVideoChanged = Signal(int)

    def __init__(self, /) -> None:
        super().__init__()
        self._temp_import_found_video = self._settings.import_found_video

    @Property(int, notify=importFoundVideoChanged)
    def importFoundVideo(self) -> int:
        return self._temp_import_found_video.value

    @importFoundVideo.setter
    def importFoundVideo(self, value: int) -> None:
        setting = ImportFoundVideo(value)
        if self._temp_import_found_video != setting:
            self._temp_import_found_video = setting
            self.importFoundVideoChanged.emit(value)

    @Slot()
    def accept(self) -> None:
        self._settings.import_found_video = self._temp_import_found_video
