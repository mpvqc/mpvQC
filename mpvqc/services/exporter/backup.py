# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import inject
from PySide6.QtCore import QCoreApplication, QDateTime

from mpvqc.services.application_paths import ApplicationPathsService
from mpvqc.services.exporter.documents import DocumentRenderService
from mpvqc.services.player import PlayerService
from mpvqc.services.resource import ResourceService


class DocumentBackupService:
    _paths = inject.attr(ApplicationPathsService)
    _player = inject.attr(PlayerService)
    _renderer = inject.attr(DocumentRenderService)
    _resources = inject.attr(ResourceService)

    @property
    def _video_name(self) -> str:
        if path := self._player.path:
            return Path(path).name
        #: Will be used in the file name proposal when saving a qc document when there's no video being loaded
        return QCoreApplication.translate("FileInteractionDialogs", "untitled")

    @property
    def _content(self) -> str:
        return self._renderer.render(self._resources.backup_template)

    def backup(self) -> None:
        now = QDateTime.currentDateTime()

        zip_name = f"{now.toString('yyyy-MM')}.zip"
        zip_path = self._paths.dir_backup / zip_name
        file_name = f"{now.toString('yyyy-MM-dd_HH-mm-ss')}_{self._video_name}.txt"

        with ZipFile(zip_path, mode="a" if zip_path.exists() else "w", compression=ZIP_DEFLATED) as file:
            file.writestr(file_name, self._content)
