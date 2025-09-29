// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material

Dialog {
    id: root

    required property var mpvqcApplication

    property alias text: _content.text

    popupType: Qt.platform.os === "windows" ? Popup.Window : Popup.Item
    contentWidth: 420
    z: 2
    parent: mpvqcApplication.contentItem
    standardButtons: Dialog.Ok
    closePolicy: Popup.CloseOnEscape
    anchors.centerIn: parent
    dim: false

    contentItem: Label {
        id: _content

        horizontalAlignment: Text.AlignLeft
        wrapMode: Label.WordWrap
        elide: Text.ElideLeft
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
