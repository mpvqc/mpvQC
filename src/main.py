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


def run(dir_program: str, app_version: str, app_name: str):
    from src._metadata import set_metadata
    from src._files import set_files

    set_metadata(dir_program, app_version, app_name)
    set_files()

    import sys

    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtGui import QIcon

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))

    from src.uihandler import MainHandler

    container = MainHandler(app)
    container.show()

    sys.exit(app.exec_())
