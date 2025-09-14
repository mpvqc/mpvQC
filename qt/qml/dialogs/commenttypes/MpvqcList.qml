// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material

ListView {
    id: root

    required property var mpvqcApplication
    required property int itemHeight

    readonly property var mpvqcTheme: mpvqcApplication.mpvqcTheme

    readonly property int defaultHighlightMoveDuration: 50

    spacing: 0
    clip: true
    reuseItems: true
    boundsBehavior: Flickable.StopAtBounds

    highlightMoveDuration: defaultHighlightMoveDuration
    highlightMoveVelocity: -1
    highlightResizeDuration: 50
    highlightResizeVelocity: -1

    highlight: Rectangle {
        width: parent?.width ?? 0
        height: parent?.height ?? 0
        color: root.mpvqcTheme.rowHighlight
        radius: Material.ExtraSmallScale
    }

    delegate: ItemDelegate {
        id: _delegate

        required property string modelData
        required property int index

        readonly property bool rowSelected: root.currentIndex === index
        readonly property bool isOdd: index % 2 === 1

        readonly property color foregroundColor: root.mpvqcTheme.getForeground(isOdd)
        readonly property color backgroundColor: root.mpvqcTheme.getBackground(isOdd)

        Material.foreground: rowSelected ? root.mpvqcTheme.rowHighlightText : foregroundColor
        Material.background: backgroundColor

        width: parent ? parent.width - _scrollBar.visibleWidth : 0
        height: root.itemHeight

        background: Rectangle {
            parent: _delegate.parent
            y: _delegate.y
            height: _delegate.height
            color: _delegate.backgroundColor
            radius: Material.ExtraSmallScale
        }

        onPressed: {
            root.currentIndex = index;
        }

        Label {
            width: _delegate.width
            height: _delegate.height
            padding: 15

            text: qsTranslate("CommentTypes", _delegate.modelData)
            elide: LayoutMirroring.enabled ? Text.ElideLeft : Text.ElideRight

            horizontalAlignment: Text.AlignLeft
            verticalAlignment: Text.AlignVCenter
        }
    }

    function disableMovingHighlightRectangle(): void {
        root.highlightMoveDuration = 0;
    }

    function enableMovingHighlightRectangle(): void {
        root.highlightMoveDuration = root.defaultHighlightMoveDuration;
    }

    ScrollBar.vertical: ScrollBar {
        id: _scrollBar

        readonly property bool isShown: root.contentHeight > root.height
        readonly property real visibleWidth: isShown ? width : 0

        policy: isShown ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff
    }
}
