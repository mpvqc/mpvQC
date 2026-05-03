// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material
import QtQuick.Layouts

RowLayout {
    id: root

    property alias toggle: _switch
    property alias checked: _switch.checked
    property alias label: _labelWithToolTip.text
    property alias labelToolTip: _labelWithToolTip.toolTip

    signal toggled(checked: bool)

    MpvqcLabelWithToolTip {
        id: _labelWithToolTip

        Layout.fillWidth: true
        Layout.preferredWidth: 0
    }

    Item {
        Layout.fillWidth: true
        Layout.preferredWidth: 0
        Layout.preferredHeight: _switch.height

        Switch {
            id: _switch

            anchors.left: parent.left
            anchors.verticalCenter: parent.verticalCenter

            onCheckedChanged: root.toggled(checked)
        }
    }
}
