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

"""
The gui package contains everything that's directly connected to gui components.
"""

from PyQt5.QtGui import QFont

"""
    1 Typewriter font instance for the application. Will use the default fixed font of the system.

    Can not be set here, because this file is imported before QApplication is started.
    It will be set before the first window is shown. Therefore using this variable should be safe.
    
    
"""
TYPEWRITER_FONT: QFont
# todo/discussion I have mixed feelings about this. Constants should be immutable.
# We could call QFontDatabase.systemFont(QFontDatabase.FixedFont) every time we use it,
# but then we might rewrite everything once we're allowing changes for the monospace font.

# Time format
TIME_FORMAT = "hh:mm:ss"

# Supported subtitle file extensions for drag and drop and for opening via dialog
SUPPORTED_SUB_FILES = (".ass", ".ssa", ".srt", ".sup", ".idx", ".utf", ".utf8", ".utf-8", ".smi",
                       ".rt", ".aqt", ".jss", ".js", ".mks", ".vtt", ".sub", ".scc")
