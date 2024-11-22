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

    readonly property var mpvqcSettings: mpvqcApplication.mpvqcSettings

    readonly property bool isVerticalLayout: mpvqcSettings.layoutOrientation === Qt.Vertical

    readonly property alias verticalLayout: _verticalLayout
    readonly property alias horizontalLayout: _horizontalLayout

    title: qsTranslate("MainWindow", "Application Layout")
    icon.source: "qrc:/data/icons/vertical_split_black_24dp.svg"
    icon.height: 24
    icon.width: 24

    MenuItem {
        id: _verticalLayout

        text: qsTranslate("MainWindow", "Video Above Comments")
        autoExclusive: true
        checkable: true
        checked: root.isVerticalLayout

        onTriggered: {
            root.mpvqcSettings.layoutOrientation = Qt.Vertical;
        }
    }

    MenuItem {
        id: _horizontalLayout

        text: qsTranslate("MainWindow", "Video Next to Comments")
        autoExclusive: true
        checkable: true
        checked: !root.isVerticalLayout

        onTriggered: {
            root.mpvqcSettings.layoutOrientation = Qt.Horizontal;
        }
    }
}
