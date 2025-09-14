// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material

GridView {
    id: root

    required property var mpvqcTheme
    required property int currentThemeColorOption

    readonly property int defaultHighlightMoveDuration: 150
    readonly property int itemSize: 52
    readonly property int itemPadding: 8
    readonly property int borderSize: 5

    signal colorOptionPressed(option: int)

    onModelChanged: {
        highlightMoveDuration = 0;
        currentIndex = root.currentThemeColorOption;
        highlightMoveDuration = defaultHighlightMoveDuration;
    }

    model: mpvqcTheme.colors
    boundsBehavior: Flickable.StopAtBounds

    clip: true
    height: (itemSize + itemPadding) * 4
    cellWidth: itemSize + itemPadding
    cellHeight: itemSize + itemPadding

    highlightMoveDuration: 150

    highlight: Rectangle {
        width: root.itemSize
        height: root.itemSize
        color: root.mpvqcTheme.isDark ? root.mpvqcTheme.foreground : root.mpvqcTheme.background
        radius: Material.SmallScale

        border {
            width: root.mpvqcTheme.isDark ? 0 : 2
            color: root.mpvqcTheme.rowHighlight
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
            color: _delegate.rowHighlight
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
                root.colorOptionPressed(_delegate.index);
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
}
