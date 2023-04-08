/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

import QtQuick
import QtQuick.Controls
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
                root.valueModified(value)
            }
        }

        Label {
            id: _suffix
            horizontalAlignment: Text.AlignHCenter
            Layout.preferredWidth: root.spinBoxWidth
        }
    }

}
