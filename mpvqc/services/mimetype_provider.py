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
    def video_file_endings(self):
        video_types = set()
        video_types.add("*.mp4")
        video_types.add("*.mkv")
        video_types.add("*.avi")

        for mime_type in QMimeDatabase().allMimeTypes():
            if mime_type.name().startswith("video/"):
                video_types.update(mime_type.globPatterns())

        return f" ({" ".join(sorted(video_types))})"
