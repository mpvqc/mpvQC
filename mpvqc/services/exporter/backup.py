# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING
from zipfile import ZIP_DEFLATED, ZipFile

from PySide6.QtCore import QCoreApplication, QDateTime

from mpvqc.services.exporter.documents import render_classic

if TYPE_CHECKING:
    from mpvqc.services.application_paths import ApplicationPathsService
    from mpvqc.services.exporter.context import RenderContext
    from mpvqc.services.player import PlayerService
    from mpvqc.services.resource import ResourceService


def backup(paths: ApplicationPathsService, resources: ResourceService, context: RenderContext) -> None:
    now = QDateTime.currentDateTime()

    zip_name = f"{now.toString('yyyy-MM')}.zip"
    zip_path = paths.dir_backup / zip_name
    file_name = f"{now.toString('yyyy-MM-dd_HH-mm-ss')}_{_video_name(context.player)}.txt"

    with ZipFile(zip_path, mode="a" if zip_path.exists() else "w", compression=ZIP_DEFLATED) as file:
        file.writestr(file_name, render_classic(resources.backup_template, context))


def _video_name(player: PlayerService) -> str:
    if path := player.path:
        return Path(path).name
    #: Will be used in the file name proposal when saving a qc document when there's no video being loaded
    return QCoreApplication.translate("FileInteractionDialogs", "untitled")
