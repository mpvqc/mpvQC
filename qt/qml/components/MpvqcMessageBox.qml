// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material

Dialog {
    id: root

    property alias text: _content.text

    popupType: Qt.platform.os === "windows" ? Popup.Window : Popup.Item
    contentWidth: 420
    z: 2
    standardButtons: Dialog.Ok
    closePolicy: Popup.CloseOnEscape
    anchors.centerIn: Overlay.overlay
    dim: false

    contentItem: Label {
        id: _content

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

    footer: MpvqcKeyboardFocusableButtonBox {}

    Binding {
        when: Qt.platform.os === "windows"
        target: root
        property: "enter"
        value: null
        restoreMode: Binding.RestoreNone
    }

    Binding {
        when: Qt.platform.os === "windows"
        target: root
        property: "exit"
        value: null
        restoreMode: Binding.RestoreNone
    }
}
