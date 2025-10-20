// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material
import QtQuick.Controls.impl
import QtQuick.Layouts

import "../utility"

RowLayout {
    id: root

    property alias text: _label.text
    property string toolTip

    spacing: toolTip ? 8 : 0

    Label {
        id: _label

        Layout.fillWidth: true

        horizontalAlignment: Text.AlignRight
        wrapMode: Text.Wrap
    }

    IconLabel {
        visible: root.toolTip
        width: visible ? implicitWidth : 0
        opacity: 0.6

        icon {
            source: "qrc:/data/icons/tooltip_2_24dp_5F6368_FILL0_wght400_GRAD0_opsz24.svg"
            width: 18
            height: 18
            color: MpvqcTheme.control
        }

        ToolTip.delay: 350
        ToolTip.text: root.toolTip
        ToolTip.visible: _mouseArea.containsMouse

        MouseArea {
            id: _mouseArea
            anchors.fill: parent
            acceptedButtons: Qt.NoButton
            hoverEnabled: true
            cursorShape: Qt.PointingHandCursor
        }
    }
}
