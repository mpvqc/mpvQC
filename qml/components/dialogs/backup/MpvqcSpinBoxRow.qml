/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/


import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import helpers


RowLayout {
    spacing: 16
    property real parentWidth: parent.width
    property alias label: label.text
    property alias value: input.value

    Label {
        id: label
        horizontalAlignment: Text.AlignRight
        wrapMode: Text.Wrap
        Layout.preferredWidth: parentWidth / 2
    }

    ColumnLayout {
        Layout.fillWidth: true

        SpinBox {
            id: input
            editable: true
            from: 15
            to: 5 * 60
            Layout.fillWidth: true
        }

        Label {
            text: qsTranslate("BackupSettings", "Seconds")
            horizontalAlignment: Text.AlignHCenter
            Layout.fillWidth: true
        }
    }
}
