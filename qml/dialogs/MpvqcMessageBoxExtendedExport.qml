/*
mpvQC

Copyright (C) 2024 mpvQC developers

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
import QtQuick.Controls.Material

import shared

MpvqcMessageBox {
    title: qsTranslate("MessageBoxes", "Extended Exports")

    contentItem: Label {
        //: %1 will be the link to the Jinja templating engine. %2 will be the link to mpvQC's documentation about export templates
        text: qsTranslate("MessageBoxes", "mpvQC allows for customizing report exports using the %1 engine. To begin, visit %2")
            .arg(`<a href="https://jinja.palletsprojects.com/en/3.1.x/">Jinja template</a>`)
            .arg(`<a href="https://mpvqc.github.io/export-templates">https://mpvqc.github.io/export-templates</a>`)
        horizontalAlignment: Text.AlignLeft
        wrapMode: Label.WordWrap
        elide: Text.ElideLeft

        onLinkActivated: link => {
            Qt.openUrlExternally(link);
        }

        MouseArea {
            anchors.fill: parent
            acceptedButtons: Qt.NoButton
            cursorShape: parent.hoveredLink ? Qt.PointingHandCursor : Qt.ArrowCursor
            hoverEnabled: true
        }
    }
}
