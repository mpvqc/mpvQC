// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Utility

ListView {
    id: root
    objectName: "commentTypesListView"

    required property var applyMove

    property alias commentTypes: _reorder.model

    readonly property bool reordering: _reorder.busy

    readonly property bool _scrolls: contentHeight > height
    readonly property real _scrollBarGutter: _scrolls ? 20 : 0
    readonly property real _edgeZone: 48
    readonly property real _maximumEdgeSpeed: 360
    readonly property real _edgeSpeed: {
        const pointerY = _reorder.pointerY;
        const depth = pointerY < _edgeZone ? pointerY - _edgeZone : pointerY > height - _edgeZone ? pointerY - height + _edgeZone : 0;
        // The pointer can leave the list while dragging.
        const proximity = Math.max(-1, Math.min(1, depth / _edgeZone));
        return _maximumEdgeSpeed * proximity * Math.abs(proximity);
    }

    signal deleteRequested(index: int)

    function cancelReorder(): void {
        _reorder.cancel();
    }

    clip: true
    model: _reorder
    interactive: !reordering
    boundsBehavior: Flickable.StopAtBounds
    // The lifted row lives in its delegate, so no delegate may be released mid-drag.
    cacheBuffer: Math.max(0, contentHeight)

    move: Transition {
        enabled: !_reorder.applyingMove

        NumberAnimation {
            property: "y"
            duration: 150
            easing.type: Easing.OutCubic
        }
    }

    moveDisplaced: move

    remove: Transition {
        NumberAnimation {
            property: "opacity"
            to: 0
            duration: 50
        }
    }

    removeDisplaced: Transition {
        NumberAnimation {
            property: "y"
            duration: 50
        }
    }

    ScrollBar.vertical: MpvqcScrollBar {
        policy: root._scrolls ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff
    }

    MpvqcCommentTypesReorderModel {
        id: _reorder

        view: root
        applyMove: root.applyMove
        delegate: MpvqcCommentTypesDraggableDelegate {
            view: root
            reorder: _reorder
            gutter: root._scrollBarGutter
            deleteEnabled: root.count > 1

            onDeleteRequested: index => root.deleteRequested(index)
        }
    }

    FrameAnimation {
        running: _reorder.dragging && root._edgeSpeed !== 0

        onTriggered: {
            const minimum = root.originY;
            const maximum = minimum + Math.max(0, root.contentHeight - root.height);
            // A stalled frame must not throw the list far past the pointer.
            const step = root._edgeSpeed * Math.min(frameTime, 0.04);
            root.contentY = Math.max(minimum, Math.min(maximum, root.contentY + step));
        }
    }

    Rectangle {
        objectName: "commentTypesDropIndicator"

        y: _reorder.activeItem ? _reorder.activeItem.y - root.contentY : 0
        height: MpvqcConstants.listRowHeight
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.rightMargin: root._scrollBarGutter
        z: 2
        radius: 8
        color: Qt.alpha(MpvqcAppearance.palette.accent, 0.08)
        visible: root.reordering
    }
}
