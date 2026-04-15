// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick

DragHandler {
    id: root

    required property int edgeMarginVertical
    required property int parentHeight
    required property int popupHeight
    required property int popupY

    readonly property int snapThreshold: 15
    readonly property int minY: edgeMarginVertical
    readonly property int maxY: parentHeight - popupHeight - edgeMarginVertical
    readonly property bool isPressed: _hasPassiveGrab || _hasExclusiveGrab

    property int targetY: maxY
    property bool snapToBottom: true

    property int _dragStartY: -1
    property bool _hasPassiveGrab: false
    property bool _hasExclusiveGrab: false

    signal pointerPressed
    signal pointerReleased
    signal dragStarted

    function _updateTargetPosition(newY: int): void {
        targetY = Math.max(minY, Math.min(maxY, newY));
        snapToBottom = (targetY >= maxY - snapThreshold);

        if (!active && snapToBottom) {
            targetY = maxY;
        }
    }

    dragThreshold: 0
    target: null
    xAxis.enabled: false
    yAxis.enabled: true

    onGrabChanged: transition => {
        const wasPressed = isPressed;

        switch (transition) {
        case PointerDevice.GrabPassive:
            _hasPassiveGrab = true;
            break;
        case PointerDevice.GrabExclusive:
            _hasExclusiveGrab = true;
            break;
        case PointerDevice.UngrabPassive:
        case PointerDevice.CancelGrabPassive:
            _hasPassiveGrab = false;
            break;
        case PointerDevice.UngrabExclusive:
        case PointerDevice.CancelGrabExclusive:
            _hasExclusiveGrab = false;
            break;
        }

        if (isPressed && !wasPressed) {
            root.pointerPressed();
        } else if (!isPressed && wasPressed) {
            root.pointerReleased();
        }
    }

    onActiveChanged: {
        if (active) {
            _dragStartY = root.popupY;
            root.dragStarted();
        } else {
            _dragStartY = -1;
        }
    }

    onMaxYChanged: {
        if (maxY <= 0)
            return;

        if (snapToBottom) {
            targetY = maxY;
        } else {
            _updateTargetPosition(targetY);
        }
    }

    yAxis.onActiveValueChanged: {
        if (_dragStartY === -1)
            return;
        _updateTargetPosition(_dragStartY + yAxis.activeValue);
    }
}
