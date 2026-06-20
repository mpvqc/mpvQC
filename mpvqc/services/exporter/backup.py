# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING
from zipfile import ZIP_DEFLATED, ZipFile

from PySide6.QtCore import QCoreApplication, QDateTime

from .documents import render_backup

if TYPE_CHECKING:
    from .context import RenderContext


def backup(backup_dir: Path, context: RenderContext) -> None:
    now = QDateTime.currentDateTime()

    zip_name = f"{now.toString('yyyy-MM')}.zip"
    zip_path = backup_dir / zip_name
    file_name = f"{now.toString('yyyy-MM-dd_HH-mm-ss')}_{_video_name(context.video_path)}.json"

    with ZipFile(zip_path, mode="a" if zip_path.exists() else "w", compression=ZIP_DEFLATED) as file:
        file.writestr(file_name, render_backup(context))


def _video_name(video_path: str | None) -> str:
    if video_path:
        return Path(video_path).name
    #: Will be used in the file name proposal when saving a qc document when there's no video being loaded
    return QCoreApplication.translate("FileInteractionDialogs", "untitled")
