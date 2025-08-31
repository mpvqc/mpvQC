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

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material

ListView {
    id: root

    required property var mpvqcTheme
    required property string currentThemeIdentifier

    readonly property int itemSize: 52
    readonly property int borderSize: 5

    signal themeIdentifierPressed(themeIdentifier: string)

    function selectInitialIndex(): void {
        for (const [index, item] of model.entries()) {
            if (item.name === root.currentThemeIdentifier) {
                root.currentIndex = index;
                break;
            }
        }
    }

    model: mpvqcTheme.availableThemes
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
        color: root.mpvqcTheme.control
        radius: Material.SmallScale

        Behavior on color {
            ColorAnimation {
                duration: root.highlightMoveDuration
            }
        }
    }

    delegate: ItemDelegate {
        id: _delegate

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
            color: _delegate.preview
            radius: Material.LargeScale
        }

        Behavior on scale {
            NumberAnimation {
                duration: 125
                easing.type: Easing.InOutQuad
            }
        }

        MouseArea {
            anchors.fill: parent
            onPressed: {
                _delegate.scale = 1.1;
                root.currentIndex = _delegate.index;
                root.themeIdentifierPressed(_delegate.name);
            }
            onReleased: {
                _delegate.scale = 1.0;
            }
            onCanceled: {
                _delegate.scale = 1.0;
            }
        }
    }

    populate: Transition {
        ParallelAnimation {
            PropertyAnimation {
                property: "opacity"
                from: 0
                to: 1
                duration: 250
                easing.type: Easing.OutCubic
            }
            PropertyAnimation {
                property: "scale"
                from: 0.85
                to: 1.0
                duration: 250
                easing.type: Easing.OutBack
            }
        }
    }

    Component.onCompleted: {
        root.selectInitialIndex();
    }
}
