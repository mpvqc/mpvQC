// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick

import io.github.mpvqc.mpvQC.Utility

Item {
    id: root
    objectName: "commentTypeDelegate"

    required property string display
    required property int index
    required property ListView view
    required property MpvqcCommentTypesReorderModel reorder
    required property real gutter
    required property bool deleteEnabled

    readonly property bool _lifted: reorder.activeItem === root

    property real _settleFrom: 0
    property real _settleProgress: 0

    signal deleteRequested(index: int)

    function _viewY(scenePosition: point): real {
        return view.mapFromItem(null, scenePosition).y;
    }

    function _release(): void {
        _settleFrom = _content.y;
        _settleProgress = 0;
        reorder.drop();
        _settleAnimation.start();
    }

    width: view.width
    height: MpvqcConstants.listRowHeight

    on_LiftedChanged: {
        if (!_lifted) {
            _settleAnimation.stop();
        }
    }

    MpvqcCommentTypesRow {
        id: _content

        width: root.width
        height: root.height
        commentType: root.display
        gutter: root.gutter
        lifted: root._lifted
        hoverFeedback: !root.reorder.busy
        deleteEnabled: root.deleteEnabled

        onDeleteClicked: {
            // A removed row can still receive clicks during its fade-out.
            if (root.index >= 0) {
                root.deleteRequested(root.index);
            }
        }

        states: State {
            when: root._lifted

            ParentChange {
                target: _content
                parent: root.view
            }

            PropertyChanges {
                _content.x: 0
                _content.y: root.reorder.settling ? root._settleFrom + (root.y - root.view.contentY - root._settleFrom) * root._settleProgress : root.reorder.liftedY
                _content.z: 1
            }
        }
    }

    DragHandler {
        id: _handler

        parent: _content.dragHandle
        target: null
        enabled: !root.reorder.settling
        xAxis.enabled: false
        cursorShape: Qt.ClosedHandCursor

        onActiveChanged: {
            if (active) {
                const grabOffset = root._viewY(centroid.scenePressPosition) - root.mapToItem(root.view, 0, 0).y;
                root.reorder.begin(root, root.index, root._viewY(centroid.scenePosition), grabOffset);
            }
        }
        onCentroidChanged: {
            if (active) {
                root.reorder.track(root._viewY(centroid.scenePosition));
            }
        }
        onGrabChanged: (transition, point) => {
            if (!root._lifted || !root.reorder.dragging) {
                return;
            }
            if (transition === PointerDevice.UngrabExclusive || transition === PointerDevice.CancelGrabExclusive) {
                if (point.state === EventPoint.Released) {
                    root._release();
                } else {
                    root.reorder.cancel();
                }
            }
        }
    }

    NumberAnimation {
        id: _settleAnimation

        target: root
        property: "_settleProgress"
        to: 1
        duration: 130
        easing.type: Easing.OutCubic

        onFinished: root.reorder.finish()
    }
}
