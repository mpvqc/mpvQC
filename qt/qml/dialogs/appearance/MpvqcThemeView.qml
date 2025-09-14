// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

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
