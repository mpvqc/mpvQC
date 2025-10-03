# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from functools import cached_property

from PySide6.QtCore import QMimeDatabase


class MimetypeProviderService:
    @cached_property
    def video_file_glob_pattern(self):
        patterns = set()
        patterns.add("*.avi")
        patterns.add("*.mkv")
        patterns.add("*.mp4")

        for mime_type in QMimeDatabase().allMimeTypes():
            if mime_type.name().startswith("video/"):
                patterns.update(mime_type.globPatterns())

        return f" ({' '.join(sorted(patterns))})"

    @cached_property
    def subtitle_file_glob_pattern(self):
        patterns = (f"*.{ext}" for ext in self.subtitle_file_extensions)
        return f" ({' '.join(sorted(patterns))})"

    @cached_property
    def subtitle_file_extensions(self) -> set[str]:
        # fmt: off
        return {
            "aqt", "ass", "idx", "js", "jss", "mks", "rt", "scc", "smi",
            "srt", "ssa", "sub", "sup", "utf", "utf-8", "utf8", "vtt"
        }
        # fmt: on
