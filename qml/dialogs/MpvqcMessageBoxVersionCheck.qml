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
import QtQuick.Controls.Material

import shared

MpvqcMessageBox {
    id: root

    readonly property var mpvqcVersionCheckerPyObject: mpvqcApplication.mpvqcVersionCheckerPyObject

    title: qsTranslate("MessageBoxes", "Checking for Updates...")

    contentItem: Label {
        text: qsTranslate("MessageBoxes", "Loading...")
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

    Component.onCompleted: {
        root.mpvqcVersionCheckerPyObject.check_for_new_version();
    }

    Connections {
        target: root.mpvqcVersionCheckerPyObject

        function onVersionChecked(title: string, text: string) {
            root.title = title;
            root.contentItem.text = text;
        }
    }
}
