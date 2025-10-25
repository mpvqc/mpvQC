# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from loguru import logger
from PySide6.QtCore import QObject, QRunnable, QThreadPool, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import ImporterService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


class ContinueImportJob(QRunnable):
    _importer: ImporterService = inject.attr(ImporterService)

    def __init__(self, import_id: str, user_accepted: bool):
        super().__init__()
        self._import_id = import_id
        self._user_accepted = user_accepted

    def run(self):
        # self._importer.continue_video_determination(self._import_id, self._user_accepted)
        raise NotImplementedError


# noinspection PyPep8Naming
@QmlElement
class MpvqcDialogLoaderViewModel(QObject):
    _importer: ImporterService = inject.attr(ImporterService)

    def __init__(self):
        super().__init__()

        def ask_user_what_to_import(*args):
            logger.debug("Asking user what to import {}", args)

        self._importer.ask_user_what_to_import.connect(ask_user_what_to_import)

    @Slot(str, bool)
    def continueWithImport(self, import_id: str, user_accepted: bool):
        job = ContinueImportJob(import_id, user_accepted)
        QThreadPool.globalInstance().start(job)
