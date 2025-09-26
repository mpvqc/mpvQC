# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QAbstractItemModel, QObject, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.models import ImportOptionsModel
from mpvqc.services import SettingsService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyTypeChecker,PyPep8Naming
@QmlElement
class MpvqcImportSettingsDialogControllerPyObject(QObject):
    _settings: SettingsService = inject.attr(SettingsService)

    importWhenVideoLinkedInDocumentChanged = Signal(int)

    def __init__(self, /):
        super().__init__()
        self._import_options_model = ImportOptionsModel()
        self._temp_import_when_video_linked_in_document = self._settings.import_when_video_linked_in_document

    @Property(QAbstractItemModel, constant=True, final=True)
    def importOptionsModel(self) -> ImportOptionsModel:
        return self._import_options_model

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
