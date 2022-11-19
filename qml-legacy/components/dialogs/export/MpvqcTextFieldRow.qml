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
import helpers


RowLayout {
    spacing: 16
    property real parentWidth: parent.width
    property alias label: label.text
    property alias input: input.text

    Label {
        id: label
        horizontalAlignment: Text.AlignRight
        wrapMode: Text.Wrap
        Layout.preferredWidth: parentWidth / 2
    }

    TextField {
        id: input
        focus: true
        selectByMouse: true
        bottomPadding: topPadding
        horizontalAlignment: Text.AlignLeft
        font.bold: true
        font.pixelSize: MpvqcConstants.fontSizeSmall
        Layout.fillWidth: true
    }

}
