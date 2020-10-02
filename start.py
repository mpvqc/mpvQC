#!/usr/bin/env python3

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


if __name__ == "__main__":
    import locale
    import os
    import platform
    import sys
    # noinspection PyUnresolvedReferences
    import resources_rc

    dir_program = sys._MEIPASS if getattr(sys, "frozen", False) else os.path.dirname(os.path.realpath(__file__))
    app_version = "0.7.0"
    app_name = "mpvQC"

    if platform.system() == "Windows":
        os.add_dll_directory(dir_program)

    locale.setlocale(locale.LC_NUMERIC, "C")

    from mpvqc import run

    run(
        dir_program=dir_program,
        app_version=app_version,
        app_name=app_name
    )
