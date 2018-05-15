# Copyright (C) 2016-2017 Frechdachs <frechdachs@rekt.cc>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from PyQt5.QtGui import QFont

# 1 Font instance for the application
TYPEWRITER_FONT = QFont("monospace")
TYPEWRITER_FONT.setStyleHint(QFont.TypeWriter)

# Time format
TIME_FORMAT = "hh:mm:ss"

# Supported subtitle file extensions for drag and drop and for opening via dialog
SUPPORTED_SUB_FILES = ("ass", "ssa", "srt", "sup", "idx", "utf", "utf8", "utf-8", "smi", "rt", "aqt", "jss", "js",
                       "mks", "vtt", "sub", "scc")

# Supported video file extensions for drag and drop and for opening via dialog
SUPPORTED_VIDEO_FILES = ("mp4", "mkv", "avi")
