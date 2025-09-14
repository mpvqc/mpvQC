// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material
import QtQuick.Layouts

RowLayout {
    id: root

    required property int prefWidth

    property int spinBoxWidth: 130

    property alias spinBox: _input
    property alias label: _label.text
    property alias suffix: _suffix.text
    property alias value: _input.value
    property alias valueFrom: _input.from
    property alias valueTo: _input.to

    signal valueModified(int value)

    Label {
        id: _label

        horizontalAlignment: Text.AlignRight
        wrapMode: Text.Wrap
        Layout.preferredWidth: root.prefWidth / 2
    }

    ColumnLayout {
        Layout.fillWidth: true
        Layout.leftMargin: 10
        Layout.topMargin: 20

        SpinBox {
            id: _input
            editable: true
            Layout.preferredWidth: root.spinBoxWidth

            onValueChanged: {
                root.valueModified(value);
            }
        }

        Label {
            id: _suffix
            horizontalAlignment: Text.AlignHCenter
            Layout.preferredWidth: root.spinBoxWidth
        }
    }
}
