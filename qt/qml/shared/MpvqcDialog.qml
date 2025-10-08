// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material

Dialog {
    id: root

    readonly property bool isMirrored: Application.layoutDirection === Qt.RightToLeft

    popupType: Qt.platform.os === "windows" ? Popup.Window : Popup.Item
    anchors.centerIn: parent
    contentWidth: 370
    contentHeight: 450
    modal: true
    dim: false
    z: 2
    closePolicy: Popup.CloseOnEscape
    standardButtons: Dialog.Ok

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
