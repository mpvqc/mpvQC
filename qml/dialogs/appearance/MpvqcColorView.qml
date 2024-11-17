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

GridView {
    id: root

    required property var mpvqcApplication

    readonly property var mpvqcSettings: mpvqcApplication.mpvqcSettings
    readonly property var mpvqcThemesPyObject: root.mpvqcApplication.mpvqcThemesPyObject

    readonly property string currentThemeIdentifier: mpvqcSettings.themeIdentifier
    readonly property int currentThemeColorOption: mpvqcSettings.themeColorOption
    readonly property bool isDarkTheme: mpvqcThemesPyObject.getThemeSummary(currentThemeIdentifier).isDark

    readonly property int defaultHighlightMoveDuration: 150
    readonly property int itemSize: 52
    readonly property int itemPadding: 8
    readonly property int borderSize: 5

    property var initialThemeColorOption: null

    function reset(): void {
        root.mpvqcSettings.themeColorOption = initialThemeColorOption;
    }

    Component.onCompleted: {
        root.initialThemeColorOption = root.mpvqcSettings.themeColorOption;
    }

    onModelChanged: {
        highlightMoveDuration = 0;
        currentIndex = mpvqcSettings.themeColorOption;
        highlightMoveDuration = defaultHighlightMoveDuration;
    }

    model: mpvqcThemesPyObject.getThemeColorOptions(currentThemeIdentifier)
    boundsBehavior: Flickable.StopAtBounds

    clip: true
    height: (itemSize + itemPadding) * 4
    cellWidth: itemSize + itemPadding
    cellHeight: itemSize + itemPadding

    highlightMoveDuration: 150

    highlight: Rectangle {
        readonly property var colors: root.mpvqcThemesPyObject
            .getThemeColorOption(root.currentThemeColorOption, root.currentThemeIdentifier)

        width: root.itemSize
        height: root.itemSize
        color: root.isDarkTheme ? colors.foreground : colors.background
        radius: Material.SmallScale

        border {
            width: root.isDarkTheme ? 0 : 2
            color: colors.rowHighlight
        }

        Behavior on color {
            ColorAnimation {
                duration: root.highlightMoveDuration
            }
        }
    }

    delegate: ItemDelegate {
        id: _delegate

        required property color rowHighlight
        required property int index

        width: root.itemSize
        height: root.itemSize

        background: Rectangle {
            x: root.borderSize
            y: root.borderSize
            height: parent.height - 2 * root.borderSize
            width: parent.width - 2 * root.borderSize
            color: parent.rowHighlight
            radius: Material.LargeScale
        }

        onPressed: {
            pressAnimation.restart();
            root.currentIndex = index;
            root.mpvqcSettings.themeColorOption = index;
        }

        SequentialAnimation {
            id: pressAnimation

            PropertyAnimation {
                target: _delegate
                property: "scale"
                to: 1.1
                duration: 125
                easing.type: Easing.InOutQuad
            }

            PropertyAnimation {
                target: _delegate
                property: "scale"
                to: 1.0
                duration: 125
                easing.type: Easing.InOutQuad
            }
        }
    }

    populate: Transition {
        SequentialAnimation {
            PropertyAnimation {
                property: "opacity"
                from: 0
                to: 1
                duration: 150
                easing.type: Easing.InOutQuad
            }

            PropertyAnimation {
                property: "scale"
                from: 0.95
                to: 1.0
                duration: 150
                easing.type: Easing.InOutCubic
            }
        }
    }
}
