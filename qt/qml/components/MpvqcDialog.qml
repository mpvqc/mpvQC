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
    anchors.centerIn: Overlay.overlay
    contentWidth: 370
    contentHeight: 450
    modal: true
    dim: false
    z: 2
    closePolicy: Popup.CloseOnEscape
    standardButtons: Dialog.Ok

    Binding {
        when: root.popupType === Popup.Window
        target: root
        property: "enter"
        value: null
        restoreMode: Binding.RestoreNone
    }

    Binding {
        when: root.popupType === Popup.Window
        target: root
        property: "exit"
        value: null
        restoreMode: Binding.RestoreNone
    }

    Binding {
        when: root.popupType === Popup.Window && root.contentItem
        target: root.contentItem
        property: "LayoutMirroring.enabled"
        value: root.isMirrored
        restoreMode: Binding.RestoreNone
    }

    Binding {
        when: root.popupType === Popup.Window && root.contentItem
        target: root.contentItem
        property: "LayoutMirroring.childrenInherit"
        value: true
        restoreMode: Binding.RestoreNone
    }

    Binding {
        when: root.popupType === Popup.Window && root.footer
        target: root.footer
        property: "LayoutMirroring.enabled"
        value: root.isMirrored
        restoreMode: Binding.RestoreNone
    }

    Binding {
        when: root.popupType === Popup.Window && root.footer
        target: root.footer
        property: "LayoutMirroring.childrenInherit"
        value: true
        restoreMode: Binding.RestoreNone
    }

    Binding {
        when: root.popupType === Popup.Window && root.header
        target: root.header
        property: "LayoutMirroring.enabled"
        value: root.isMirrored
        restoreMode: Binding.RestoreNone
    }

    Binding {
        when: root.popupType === Popup.Window && root.header
        target: root.header
        property: "LayoutMirroring.childrenInherit"
        value: true
        restoreMode: Binding.RestoreNone
    }
}
