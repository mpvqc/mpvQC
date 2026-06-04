// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material as M

import io.github.mpvqc.mpvQC.Utility

ListView {
    id: root
    objectName: "commentTypesListView"

    required property real rowHeight

    readonly property var mpvqcTheme: MpvqcTheme
    readonly property int _animationDuration: 50
    readonly property int _appearDuration: 180
    readonly property int _staggerInterval: 15

    property bool _moving: false
    property bool _deleting: false

    function ensureVisible(peekOffset: int): void {
        const lookIndex = currentIndex + peekOffset;
        const item = itemAtIndex(lookIndex);
        if (!item) {
            return;
        }

        const itemTop = item.y - contentY;
        const itemBottom = itemTop + item.height;
        const viewHeight = height;

        const isFullyVisible = itemTop >= 0 && itemBottom <= viewHeight;
        if (isFullyVisible) {
            return;
        }

        const padding = 25;

        if (itemTop < 0) {
            contentY = Math.max(0, item.y - padding);
        } else if (itemBottom > viewHeight) {
            contentY = Math.min(contentHeight - height, item.y + item.height - height + padding);
        }
    }

    function beginRemoval(): void {
        _deleting = true;
    }

    spacing: 0
    clip: true
    boundsBehavior: Flickable.StopAtBounds

    highlightFollowsCurrentItem: !_deleting
    highlightMoveDuration: _moving ? 0 : _animationDuration
    highlightMoveVelocity: -1
    highlightResizeDuration: 0
    highlightResizeVelocity: -1

    populate: Transition {
        id: _populateTransition

        SequentialAnimation {
            PropertyAction {
                property: "opacity"
                value: 0
            }
            PauseAnimation {
                duration: _populateTransition.ViewTransition.index * root._staggerInterval
            }
            NumberAnimation {
                property: "opacity"
                from: 0
                to: 1
                duration: root._appearDuration
                easing.type: Easing.OutCubic
            }
        }
    }

    move: Transition {
        SequentialAnimation {
            PropertyAction {
                target: root
                property: "_moving"
                value: true
            }
            NumberAnimation {
                properties: "y"
                duration: root._animationDuration
            }
            PropertyAction {
                target: root
                property: "_moving"
                value: false
            }
        }
    }

    remove: Transition {
        SequentialAnimation {
            NumberAnimation {
                properties: "y"
                duration: root._animationDuration
            }
            PropertyAction {
                target: root
                property: "_deleting"
                value: false
            }
        }
    }

    displaced: Transition {
        NumberAnimation {
            properties: "y"
            duration: root._animationDuration
        }
    }

    highlight: Item {
        Rectangle {
            x: LayoutMirroring.enabled ? _scrollBar.visibleWidth : 0
            width: parent.width - _scrollBar.visibleWidth
            height: parent.height
            color: root.mpvqcTheme.palette.rowSelected
            radius: M.Material.ExtraSmallScale
            visible: !root._moving
        }
    }

    delegate: ItemDelegate {
        id: _delegate

        required property var modelData
        required property int index

        readonly property color foregroundColor: root.mpvqcTheme.palette.foreground
        readonly property color stripeColor: Qt.alpha(root.mpvqcTheme.palette.foreground, 0.08)
        readonly property color backgroundColor: ListView.isCurrentItem ? (root._moving ? root.mpvqcTheme.palette.rowSelected : "transparent") : index % 2 === 0 ? stripeColor : "transparent"

        width: ListView.view.width
        height: root.rowHeight
        leftInset: LayoutMirroring.enabled ? _scrollBar.visibleWidth : 0
        rightInset: LayoutMirroring.enabled ? 0 : _scrollBar.visibleWidth

        M.Material.foreground: ListView.isCurrentItem ? root.mpvqcTheme.palette.rowSelectedText : foregroundColor
        M.Material.background: backgroundColor

        onPressed: root.currentIndex = index

        background: Rectangle {
            parent: _delegate.parent
            y: _delegate.y
            height: _delegate.height
            color: _delegate.backgroundColor
            radius: M.Material.ExtraSmallScale
            opacity: _delegate.opacity
        }

        contentItem: Label {
            padding: 15
            anchors.fill: parent

            text: qsTranslate("CommentTypes", _delegate.modelData.display)
            elide: LayoutMirroring.enabled ? Text.ElideLeft : Text.ElideRight
            horizontalAlignment: Text.AlignLeft
            verticalAlignment: Text.AlignVCenter
        }
    }

    ScrollBar.vertical: ScrollBar {
        id: _scrollBar

        readonly property bool isShown: root.contentHeight > root.height
        readonly property real visibleWidth: isShown ? width : 0

        policy: isShown ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff
    }

    Behavior on contentY {
        NumberAnimation {
            duration: root._animationDuration
        }
    }
}
