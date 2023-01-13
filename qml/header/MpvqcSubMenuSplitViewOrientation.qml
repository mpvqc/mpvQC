/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

import QtQuick
import QtQuick.Controls

import shared
import settings


MpvqcMenu {
    id: root

    required property var mpvqcApplication

    property var mpvqcSettings: mpvqcApplication.mpvqcSettings

    property alias verticalLayout: _verticalLayout
    property alias horizontalLayout: _horizontalLayout

    title: qsTranslate("MainWindow", "Application Layout")

    MenuItem {
        id: _verticalLayout

        text: qsTranslate("MainWindow", "Vertical Split")
        autoExclusive: true
        checkable: true
        checked: mpvqcSettings.layoutOrientation == Qt.Vertical

        onTriggered: {
            mpvqcSettings.layoutOrientation = Qt.Vertical
        }
    }

    MenuItem {
        id: _horizontalLayout

        text: qsTranslate("MainWindow", "Horizontal Split")
        autoExclusive: true
        checkable: true
        checked: mpvqcSettings.layoutOrientation == Qt.Horizontal

        onTriggered: {
            mpvqcSettings.layoutOrientation = Qt.Horizontal
        }
    }

}
