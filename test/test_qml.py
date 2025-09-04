# mpvQC
#
# Copyright (C) 2025 mpvQC developers
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

import sys

from PySide6.QtCore import QObject, Slot
from PySide6.QtQml import QQmlEngine
from PySide6.QtQuickTest import QUICK_TEST_MAIN_WITH_SETUP


# noinspection PyPep8Naming
class MpvqcTestSetup(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

    @Slot(QQmlEngine)
    def qmlEngineAvailable(self, _: QQmlEngine):
        import rc_project  # noqa: F401


if __name__ == "__main__":
    ex = QUICK_TEST_MAIN_WITH_SETUP("qmltestrunner", MpvqcTestSetup, sys.argv)
    sys.exit(ex)
