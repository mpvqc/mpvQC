// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material as M
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Utility

Dialog {
    id: root

    readonly property bool isMirrored: Application.layoutDirection === Qt.RightToLeft

    property string text

    readonly property int _panelPadding: 16

    popupType: MpvqcConstants.preferredPopupType
    contentWidth: 420
    z: MpvqcConstants.zModal
    standardButtons: Dialog.Ok
    closePolicy: Popup.CloseOnEscape
    anchors.centerIn: Overlay.overlay
    modal: true
    dim: false

    contentItem: ScrollView {
        id: _scroll

        contentWidth: availableWidth
        contentHeight: _sections.implicitHeight

        ColumnLayout {
            id: _sections

            width: _scroll.availableWidth

            Rectangle {
                // A one-line message under the full card radius reads as a pill,
                // so short messages flatten the corners
                radius: _body.lineCount > 1 ? 16 : 10
                color: MpvqcAppearance.palette.sectionCard
                implicitHeight: _body.implicitHeight + 2 * root._panelPadding

                Layout.fillWidth: true
                Layout.topMargin: 8

                Label {
                    id: _body

                    anchors.fill: parent
                    anchors.margins: root._panelPadding
                    text: root.text
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                    wrapMode: Label.WordWrap

                    onLinkActivated: link => {
                        Qt.openUrlExternally(link);
                    }

                    HoverHandler {
                        cursorShape: parent.hoveredLink ? Qt.PointingHandCursor : undefined
                    }
                }

                Behavior on radius {
                    NumberAnimation {
                        duration: 150
                    }
                }
            }
        }
    }

    footer: MpvqcKeyboardFocusableButtonBox {}

    M.Material.background: MpvqcAppearance.palette.dialogBackground

    MpvqcModalOverlayTracker {
        open: root.modal && root.visible
    }

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
