# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import ImportExportWiringService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


class ContinueImportJob(QRunnable):
    _import_export: ImportExportWiringService = inject.attr(ImportExportWiringService)

    def __init__(self, import_id: str, user_accepted: bool):
        super().__init__()
        self._import_id = import_id
        self._user_accepted = user_accepted

    def run(self):
        self._import_export.continue_video_determination(self._import_id, self._user_accepted)


# noinspection PyPep8Naming
@QmlElement
class MpvqcMessageBoxLoaderViewModel(QObject):
    _import_export: ImportExportWiringService = inject.attr(ImportExportWiringService)

    erroneousDocumentsImported = Signal(list)
    askUserDocumentVideoImport = Signal(str, str)
    askUserSubtitleVideoImport = Signal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._import_export.erroneous_documents_imported.connect(self.erroneousDocumentsImported)
        self._import_export.ask_user_document_video_import.connect(self.askUserDocumentVideoImport)
        self._import_export.ask_user_subtitle_video_import.connect(self.askUserSubtitleVideoImport)

    @Slot(str, bool)
    def continueWithImport(self, import_id: str, user_accepted: bool):
        job = ContinueImportJob(import_id, user_accepted)
        QThreadPool.globalInstance().start(job)
