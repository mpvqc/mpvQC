# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from PySide6.QtCore import QMimeDatabase

if TYPE_CHECKING:
    from typing import Final


class MimetypeProviderService:
    # fmt: off
    SUBTITLE_FILE_EXTENSIONS: Final[frozenset[str]] = frozenset({
        "aqt", "ass", "idx", "js", "jss", "mks", "rt", "scc", "smi",
        "srt", "ssa", "sub", "sup", "utf", "utf-8", "utf8", "vtt"
    })
    # fmt: on

    @cached_property
    def video_file_glob_pattern(self) -> str:
        patterns = set()
        patterns.add("*.avi")
        patterns.add("*.mkv")
        patterns.add("*.mp4")

        for mime_type in QMimeDatabase().allMimeTypes():
            if mime_type.name().startswith("video/"):
                patterns.update(mime_type.globPatterns())

        return f" ({' '.join(sorted(patterns))})"

    @cached_property
    def subtitle_file_glob_pattern(self) -> str:
        patterns = (f"*.{ext}" for ext in self.SUBTITLE_FILE_EXTENSIONS)
        return f" ({' '.join(sorted(patterns))})"
