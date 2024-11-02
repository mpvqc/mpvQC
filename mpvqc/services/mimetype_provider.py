# mpvQC
#
# Copyright (C) 2024 mpvQC developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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

        return f" ({" ".join(sorted(patterns))})"

    @cached_property
    def subtitle_file_glob_pattern(self):
        patterns = (f"*.{ext}" for ext in self.subtitle_file_extensions)
        return f" ({" ".join(sorted(patterns))})"

    @cached_property
    def subtitle_file_extensions(self) -> list[str]:
        # fmt: off
        return [
            'aqt', 'ass', 'idx', 'js', 'jss', 'mks', 'rt', 'scc', 'smi',
            'srt', 'ssa', 'sub', 'sup', 'utf', 'utf-8', 'utf8', 'vtt'
        ]
        # fmt: on
