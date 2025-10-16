// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material

import "../../utility"

Popup {
    id: root

    required property int currentTime
    required property int currentListIndex
    required property int videoDuration
    required property point openedAt

    readonly property bool isOpenedInBottomRegion: {
        if (root.parent) {
            const regionSize = height + MpvqcConstants.popupWindowEdgeMargin;
            return MpvqcWindowUtility.isInBottomRegion(root.parent, openedAt.x, openedAt.y, regionSize);
        }
        return false;
    }

    readonly property url iconNext: "qrc:/data/icons/keyboard_arrow_right_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
    readonly property url iconBefore: "qrc:/data/icons/keyboard_arrow_left_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"

    readonly property url downIcon: mirrored ? iconNext : iconBefore
    readonly property url upIcon: mirrored ? iconBefore : iconNext

    property bool acceptValue: true

    signal timeEdited(index: int, newTime: int)
    signal timeKept(oldTime: int)
    signal timeTemporaryChanged(newTemporaryValue: int)

    function decrementValue(): void {
        _spinBox.decrease();
        _spinBox.valueModified();
    }

    function incrementValue(): void {
        _spinBox.increase();
        _spinBox.valueModified();
    }

    x: mirrored ? openedAt.x - width : openedAt.x
    y: isOpenedInBottomRegion ? openedAt.y - height : openedAt.y
    transformOrigin: isOpenedInBottomRegion ? (mirrored ? Popup.BottomRight : Popup.BottomLeft) : (mirrored ? Popup.TopRight : Popup.TopLeft)

    visible: true
    dim: false
    modal: true
    width: 155
    padding: 6

    contentItem: SpinBox {
        id: _spinBox

        value: root.currentTime

        from: 0
        to: root.videoDuration > 0 ? root.videoDuration : 24 * 60 * 60 - 1

        textFromValue: value => MpvqcTableUtility.formatTime(value)

        bottomPadding: topPadding
        background: null

        down.indicator: ToolButton {
            x: root.mirrored ? _spinBox.width - width : 0
            height: _spinBox.height
            width: height
            icon.source: root.downIcon

            onPressed: root.decrementValue()
        }

        up.indicator: ToolButton {
            x: root.mirrored ? 0 : _spinBox.width - width
            height: _spinBox.height
            width: height
            icon.source: root.upIcon

            onPressed: root.incrementValue()
        }

        onValueModified: {
            if (root.acceptValue) {
                root.timeTemporaryChanged(_spinBox.value);
            }
        }
    }

    MouseArea {
        anchors.fill: _spinBox.contentItem
        hoverEnabled: true
        acceptedButtons: Qt.NoButton
        cursorShape: Qt.IBeamCursor

        onWheel: event => {
            if (event.angleDelta.y > 0) {
                root.incrementValue();
            } else {
                root.decrementValue();
            }
        }
    }

    onAboutToHide: {
        if (acceptValue && root.currentTime !== _spinBox.value) {
            root.timeEdited(root.currentListIndex, _spinBox.value);
        } else {
            root.timeKept(root.currentTime);
        }
    }

    Shortcut {
        sequence: "Esc"

        onActivated: {
            root.acceptValue = false;
            root.close();
        }
    }

    Shortcut {
        sequences: ["left", "down"]

        onActivated: root.decrementValue()
    }

    Shortcut {
        sequences: ["right", "up"]

        onActivated: root.incrementValue()
    }
}
