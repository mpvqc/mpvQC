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
import QtQuick.Controls.Material

import models
import shared


ListView {
    id: root

    required property var mpvqcApplication
    readonly property var mpvqcSettings: mpvqcApplication.mpvqcSettings
    readonly property var mpvqcThemesPyObject: root.mpvqcApplication.mpvqcThemesPyObject

    readonly property string currentThemeIdentifier: mpvqcSettings.themeIdentifier
    readonly property int currentThemeColorOption: mpvqcSettings.themeColorOption

    readonly property int itemSize: 52
    readonly property int borderSize: 5

    property var initialThemeIdentifier: null

    function reset(): void {
        root.mpvqcSettings.themeIdentifier = initialThemeIdentifier
    }

    function selectInitialIndex(): void {
        for (const [index, item] of model.entries()) {
            if (item.name === root.currentThemeIdentifier) {
                root.currentIndex = index
                break
            }
        }
    }

    model: mpvqcThemesPyObject.getThemeSummaries()
    boundsBehavior: Flickable.StopAtBounds
    orientation: ListView.Horizontal

    clip: true
    spacing: 8
    height: itemSize

    highlightMoveDuration: 150
    highlightMoveVelocity: -1
    highlightResizeDuration: 50
    highlightResizeVelocity: -1

    highlight: Rectangle {
        width: root.itemSize
        height: root.itemSize
        color: {
            const themeIdentifier = root.currentItem.name
            const currentColorOption = root.currentThemeColorOption
            root.mpvqcThemesPyObject.getThemeColorOption(currentColorOption, themeIdentifier).control
        }
        radius: Material.MediumScale

        Behavior on color { ColorAnimation { duration: root.highlightMoveDuration }}
    }

    delegate: ItemDelegate {
        required property string name
        required property color preview
        required property int index

        width: root.itemSize
        height: root.itemSize

        background: Rectangle {
            x: root.borderSize
            y: root.borderSize
            height: parent.height - 2 * root.borderSize
            width: parent.width - 2 * root.borderSize
            color: parent.preview
            radius: Material.LargeScale
        }

        onClicked: {
            root.currentIndex = index
            root.mpvqcSettings.themeIdentifier = name
        }
    }

    Component.onCompleted: {
        root.initialThemeIdentifier = root.currentThemeIdentifier
        root.selectInitialIndex()
    }

}
