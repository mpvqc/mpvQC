// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Utility

Rectangle {
    id: root

    required property url icon
    required property string toolTipText
    required property bool selected

    readonly property alias hovered: _hover.hovered

    property bool _animated: false

    // Not readonly: the Behavior below writes the interpolated values into it.
    property color _tint: root.selected ? MpvqcAppearance.palette.accent : MpvqcAppearance.palette.hint

    readonly property int _iconSize: 18

    implicitWidth: 38
    implicitHeight: 24
    radius: root.height / 2
    color: Qt.alpha(root._tint, 0.12)

    ToolTip.text: root.toolTipText
    ToolTip.visible: root.hovered
    ToolTip.delay: MpvqcConstants.tooltipDelay

    Component.onCompleted: root._animated = true

    MpvqcIconLabel {
        anchors.centerIn: parent

        iconColor: root._tint
        icon.source: root.icon
        icon.width: root._iconSize
        icon.height: root._iconSize
    }

    HoverHandler {
        id: _hover
    }

    Behavior on _tint {
        enabled: root._animated

        ColorAnimation {
            duration: 120
        }
    }
}
