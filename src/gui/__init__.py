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


from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtWidgets import QApplication


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
TIME_FORMAT = "HH:mm:ss"

# Supported subtitle file extensions for drag and drop and for opening via dialog
SUPPORTED_SUB_FILES = (".ass", ".ssa", ".srt", ".sup", ".idx", ".utf", ".utf8", ".utf-8", ".smi",
                       ".rt", ".aqt", ".jss", ".js", ".mks", ".vtt", ".sub", ".scc")


def set_theme(application: QApplication, dark_theme: bool):
    if dark_theme:
        application.setStyle("Fusion")

        palette = QPalette()  # https://gist.github.com/QuantumCD/6245215
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Light, Qt.transparent)  # text shadow color of the disabled options in context menu
        palette.setColor(QPalette.Disabled, QPalette.Text, Qt.gray)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        application.setPalette(palette)
        application.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
    else:
        application.setPalette(QPalette())
        application.setStyleSheet("")
