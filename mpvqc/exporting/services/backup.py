# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING
from zipfile import ZIP_DEFLATED, ZipFile

from .file_names import backup_archive_name, backup_entry_name
from .render_v1 import render_backup

if TYPE_CHECKING:
    from pathlib import Path

    from .snapshot import ExportSnapshot


def backup(backup_dir: Path, snapshot: ExportSnapshot) -> None:
    zip_path = backup_dir / backup_archive_name(snapshot.captured_at)
    file_name = backup_entry_name(snapshot.captured_at, snapshot.video_path)

    with ZipFile(zip_path, mode="a" if zip_path.exists() else "w", compression=ZIP_DEFLATED) as file:
        file.writestr(file_name, render_backup(snapshot))
