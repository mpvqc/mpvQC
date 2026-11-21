# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import shutil
from typing import TYPE_CHECKING
from zipfile import ZIP_DEFLATED, BadZipFile, ZipFile

from .file_names import backup_archive_name, backup_entry_name, unreadable_backup_archive_name
from .render_v1 import render_backup
from .writer import replacing

if TYPE_CHECKING:
    from pathlib import Path

    from .snapshot import ExportSnapshot


def backup(backup_dir: Path, snapshot: ExportSnapshot) -> None:
    archive = backup_dir / backup_archive_name(snapshot.captured_at)
    entry_name = backup_entry_name(snapshot.captured_at, snapshot.video_path)

    if archive.exists() and not _is_readable(archive):
        archive.rename(backup_dir / unreadable_backup_archive_name(snapshot.captured_at))

    with replacing(archive) as temporary:
        if archive.exists():
            shutil.copyfile(archive, temporary)
        with ZipFile(temporary, mode="a", compression=ZIP_DEFLATED) as file:
            file.writestr(entry_name, render_backup(snapshot))


def _is_readable(archive: Path) -> bool:
    try:
        with ZipFile(archive):
            return True
    except BadZipFile, NotImplementedError:
        return False
