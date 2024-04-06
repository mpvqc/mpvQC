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


MpvqcMenu {
    id: root

    required property var mpvqcApplication

    property var mpvqcSettings: mpvqcApplication.mpvqcSettings

    property alias verticalLayout: _verticalLayout
    property alias horizontalLayout: _horizontalLayout
    property bool isVerticalLayout: mpvqcSettings.layoutOrientation === Qt.Vertical

    title: qsTranslate("MainWindow", "Application Layout")
    icon.source: "qrc:/data/icons/vertical_split_black_24dp.svg"
    icon.height: 24
    icon.width: 24

    MenuItem {
        id: _verticalLayout

        text: qsTranslate("MainWindow", "Vertical Layout")
        autoExclusive: true
        checkable: true
        checked: root.isVerticalLayout

        onTriggered: {
            root.mpvqcSettings.layoutOrientation = Qt.Vertical
        }
    }

    MenuItem {
        id: _horizontalLayout

        text: qsTranslate("MainWindow", "Horizontal Layout")
        autoExclusive: true
        checkable: true
        checked: !root.isVerticalLayout

        onTriggered: {
            root.mpvqcSettings.layoutOrientation = Qt.Horizontal
        }
    }

}
