# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import re
from pathlib import Path
from typing import TYPE_CHECKING, Literal

from PySide6.QtCore import QCoreApplication

if TYPE_CHECKING:
    from datetime import datetime

_INVALID_FILENAME_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')


def _untitled_video_name() -> str:
    #: Stands in for the video's name wherever one is expected but no video is loaded:
    #: in the file name proposed when saving or exporting, and in a backup's entry name.
    return QCoreApplication.translate("FileInteractionDialogs", "untitled")


def propose_document_path(
    video_path: str | None,
    nickname: str | None,
    suffix: Literal["json", "txt"],
    fallback_directory: Path,
) -> Path:
    if video_path:
        video = Path(video_path)
        directory = video.parent
        video_name = video.stem
    else:
        directory = fallback_directory
        video_name = _untitled_video_name()

    sanitized = _INVALID_FILENAME_CHARS.sub("_", nickname or "")
    file_name = f"[QC]_{video_name}_{sanitized}.{suffix}" if sanitized else f"[QC]_{video_name}.{suffix}"

    return directory.joinpath(file_name).absolute()


def backup_archive_name(captured_at: datetime) -> str:
    return f"{captured_at:%Y-%m}.zip"


def backup_entry_name(captured_at: datetime, video_path: str | None) -> str:
    video_name = Path(video_path).name if video_path else _untitled_video_name()
    return f"{captured_at:%Y-%m-%d_%H-%M-%S}_{video_name}.json"
