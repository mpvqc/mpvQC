#!/usr/sbin/env python3

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

import locale
import sys
from os import path

from PyQt5.QtGui import QIcon, QFont, QFontDatabase
from PyQt5.QtWidgets import QApplication

from src import gui

DIRECTORY_PROGRAM = sys._MEIPASS if getattr(sys, "frozen", False) else path.dirname(path.realpath(__file__))
APPLICATION_VERSION = "0.0.1"
APPLICATION_NAME = "mpv-qc"

if __name__ == "__main__":
    # todo validation if mpv dependencies are installed and display a message box if not

    from src.gui.uihandler.main import MainHandler

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))

    gui.TYPEWRITER_FONT = QFontDatabase.systemFont(QFontDatabase.FixedFont)
    gui.TYPEWRITER_FONT.setStyleHint(QFont.TypeWriter)

    locale.setlocale(locale.LC_NUMERIC, "C")

    container = MainHandler(app)
    container.show()

    sys.exit(app.exec_())
