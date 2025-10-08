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
class MpvqcImportSettingsDialogViewModel(QObject):
    _settings: SettingsService = inject.attr(SettingsService)

    importWhenVideoLinkedInDocumentChanged = Signal(int)

    def __init__(self, /):
        super().__init__()
        self._temp_import_when_video_linked_in_document = self._settings.import_when_video_linked_in_document

    @Property(int, notify=importWhenVideoLinkedInDocumentChanged)
    def importWhenVideoLinkedInDocument(self) -> int:
        return self._temp_import_when_video_linked_in_document

    @importWhenVideoLinkedInDocument.setter
    def importWhenVideoLinkedInDocument(self, value: int) -> None:
        if self._temp_import_when_video_linked_in_document != value:
            self._temp_import_when_video_linked_in_document = value
            self.importWhenVideoLinkedInDocumentChanged.emit(value)

    @Slot()
    def accept(self) -> None:
        self._settings.import_when_video_linked_in_document = self._temp_import_when_video_linked_in_document
