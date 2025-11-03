// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.impl
import QtQuick.Controls.Material

import "../utility"

IconLabel {
    id: root

    property string toolTipText: ""

    display: IconLabel.IconOnly

    icon.color: MpvqcTheme.control

    ToolTip.delay: 350
    ToolTip.text: root.toolTipText
    ToolTip.visible: root.toolTipText && _mouseArea.containsMouse

    MouseArea {
        id: _mouseArea

        anchors.fill: parent
        acceptedButtons: Qt.NoButton
        hoverEnabled: true
        cursorShape: root.toolTipText ? Qt.PointingHandCursor : undefined
    }
}
