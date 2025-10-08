# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path

import inject
from PySide6.QtCore import Property, QCoreApplication, QObject, Signal, Slot
from PySide6.QtQml import QmlElement, QQmlComponent

from mpvqc.services import (
    DocumentExportService,
    StateService,
    TypeMapperService,
)

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyTypeChecker
@QmlElement
class MpvqcManagerBackendPyObject(QObject):
    _app_state: StateService = inject.attr(StateService)
    _exporter: DocumentExportService = inject.attr(DocumentExportService)
    _type_mapper: TypeMapperService = inject.attr(TypeMapperService)

    savedChanged = Signal(bool)

    def __init__(self):
        super().__init__()
        QCoreApplication.instance().application_ready.connect(lambda: self._on_application_ready())

        self._app_state.saved_changed.connect(self.savedChanged)

    @Property(bool, notify=savedChanged)
    def saved(self) -> bool:
        return self._app_state.saved

    @property
    def _document(self) -> Path | None:
        return self._app_state.document

    def _on_application_ready(self):
        def bind_qml_property_with(name: str) -> QQmlComponent:
            qml_prop = self.property(name)
            if not qml_prop:
                msg = f"Could not find qml property with name '{name}'"
                raise ValueError(msg)
            return qml_prop

        # fmt: off
        self.dialog_export_document_factory \
            = bind_qml_property_with(name="mpvqcDialogExportDocumentFactory")
        # fmt: on

    @Slot()
    def save_impl(self):
        if document := self._document:
            self._save(document)
        else:
            self.save_as_impl()

    def _save(self, document: Path):
        self._exporter.save(document)
        self._app_state.save(document)

    @Slot()
    def save_as_impl(self):
        path_proposal = self._exporter.generate_file_path_proposal()

        properties = {"selectedFile": self._type_mapper.map_path_to_url(path_proposal)}

        dialog = self.dialog_export_document_factory.createObject(None, properties)
        dialog.accepted.connect(dialog.deleteLater)
        dialog.rejected.connect(dialog.deleteLater)
        dialog.savePressed.connect(lambda url: self._save(self._type_mapper.map_url_to_path(url)))
        dialog.open()
