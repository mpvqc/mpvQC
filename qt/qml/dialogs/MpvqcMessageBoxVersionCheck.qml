// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material

import "../shared"

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

        function onVersionChecked(title: string, text: string): void {
            root.title = title;
            root.contentItem.text = text;
        }
    }
}
