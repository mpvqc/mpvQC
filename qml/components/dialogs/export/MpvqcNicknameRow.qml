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
import settings


RowLayout {
    required property var parentWidth

    MpvqcFormLabel {
        text: qsTranslate("ExportSettings", "Nickname")
        Layout.preferredWidth: parentWidth / 2
    }

    TextField {
        id: input
        text: MpvqcSettings.nickname
        focus: true
        selectByMouse: true
        bottomPadding: topPadding
        horizontalAlignment: Text.AlignLeft
        font.bold: true
        font.pixelSize: MpvqcConstants.fontSizeSmall
        Layout.fillWidth: true
    }

    function save() {
        MpvqcSettings.nickname = input.text
    }

}
