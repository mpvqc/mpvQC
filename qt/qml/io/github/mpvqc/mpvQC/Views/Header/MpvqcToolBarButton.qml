// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls

import MpvqcStyle
import io.github.mpvqc.mpvQC.Utility

ToolButton {
    id: root

    required property real size
    required property url iconSource
    required property string toolTipText

    readonly property int iconSize: 22

    property bool pressedDuringHover: false

    width: size
    height: size
    focusPolicy: Qt.NoFocus
    icon.source: root.iconSource
    icon.width: iconSize
    icon.height: iconSize

    onHoveredChanged: {
        if (!hovered) {
            pressedDuringHover = false;
        }
    }

    onPressedChanged: {
        if (pressed) {
            pressedDuringHover = true;
        }
    }

    ToolTip {
        y: implicitHeight + 16
        popupType: MpvqcConstants.usesWindowedPopups ? Popup.Window : Popup.Item

        text: root.toolTipText
        visible: root.hovered && !root.pressedDuringHover
        delay: 700
        timeout: 1500
    }
}
