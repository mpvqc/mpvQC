// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material

Dialog {
    id: root

    readonly property bool isMirrored: Application.layoutDirection === Qt.RightToLeft

    property string text

    popupType: Qt.platform.os === "windows" ? Popup.Window : Popup.Item
    contentWidth: 420
    z: 2
    standardButtons: Dialog.Ok
    closePolicy: Popup.CloseOnEscape
    anchors.centerIn: Overlay.overlay
    dim: false

    contentItem: Label {
        text: root.text
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
}
