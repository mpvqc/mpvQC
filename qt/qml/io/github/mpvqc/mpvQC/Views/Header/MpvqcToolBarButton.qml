// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material

import MpvqcStyle

ToolButton {
    id: root

    required property real size
    required property url iconSource
    required property string toolTipText

    readonly property int iconSize: 22
    readonly property int cornerRadius: 8

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

    background: Rectangle {
        radius: root.cornerRadius
        color: root.hovered ? root.Material.rippleColor : "transparent"
    }

    ToolTip {
        y: implicitHeight + 16
        popupType: Qt.platform.os === "windows" ? Popup.Window : Popup.Item

        text: root.toolTipText
        visible: root.hovered && !root.pressedDuringHover
        delay: 700
        timeout: 1500
    }
}
