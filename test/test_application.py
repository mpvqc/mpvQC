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

import pytest
from PySide6.QtCore import QObject, QUrl

QML = """
    import QtQuick
    import QtQuick.Controls

    ApplicationWindow {
        visible: false; width: 50; height: 50

        Button { objectName: "button-click-me"; text: "Click Me" }
    }
"""


def test_find_object(qt_app):
    qt_app._engine.loadData(QML.encode(), QUrl())
    obj = qt_app.find_object(QObject, "button-click-me")
    assert obj

    with pytest.raises(AssertionError):
        qt_app.find_object(QObject, "other-button-that-does-not-exist")
