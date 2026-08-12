# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING
from zipfile import ZIP_DEFLATED, ZipFile

from PySide6.QtCore import QCoreApplication

from .render_v1 import render_backup

if TYPE_CHECKING:
    from .snapshot import ExportSnapshot


def backup(backup_dir: Path, snapshot: ExportSnapshot) -> None:
    zip_path = backup_dir / f"{snapshot.captured_at:%Y-%m}.zip"
    file_name = f"{snapshot.captured_at:%Y-%m-%d_%H-%M-%S}_{_video_name(snapshot.video_path)}.json"

    with ZipFile(zip_path, mode="a" if zip_path.exists() else "w", compression=ZIP_DEFLATED) as file:
        file.writestr(file_name, render_backup(snapshot))


def _video_name(video_path: str | None) -> str:
    if video_path:
        return Path(video_path).name
    #: Will be used in the file name proposal when saving a qc document when there's no video being loaded
    return QCoreApplication.translate("FileInteractionDialogs", "untitled")
