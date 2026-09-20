// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

RowLayout {
    id: root

    property alias toggle: _switch
    property alias checked: _switch.checked
    property alias label: _labelWithToolTip.text
    property alias labelToolTip: _labelWithToolTip.toolTip

    property bool edgeAligned: false

    signal toggled(checked: bool)

    Layout.minimumHeight: root.edgeAligned ? 48 : 0

    MpvqcLabelWithToolTip {
        id: _labelWithToolTip

        horizontalAlignment: root.edgeAligned ? Text.AlignLeft : Text.AlignRight

        Layout.fillWidth: !root.edgeAligned
        Layout.preferredWidth: root.edgeAligned ? implicitWidth : 0
        Layout.maximumWidth: root.edgeAligned ? Math.max(0, root.width - _switch.implicitWidth - 2 * root.spacing) : Number.POSITIVE_INFINITY
    }

    Item {
        visible: root.edgeAligned

        Layout.fillWidth: true
    }

    Item {
        Layout.fillWidth: !root.edgeAligned
        Layout.preferredWidth: root.edgeAligned ? _switch.implicitWidth : 0
        Layout.preferredHeight: _switch.height

        Switch {
            id: _switch

            anchors.left: parent.left
            anchors.verticalCenter: parent.verticalCenter

            onCheckedChanged: root.toggled(checked)
        }
    }
}
