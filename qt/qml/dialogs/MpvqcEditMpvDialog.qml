// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material
import QtQuick.Layouts

import pyobjects

import "../shared"
import "../themes"

MpvqcDialog {
    id: root

    readonly property MpvqcEditMpvDialogControllerPyObject controller: MpvqcEditMpvDialogControllerPyObject {}
    readonly property var mpvqcTheme: MpvqcTheme

    title: qsTranslate("MpvConfEditDialog", "Edit mpv.conf")
    contentWidth: Math.min(1080, MpvqcWindowProperties.appWidth * 0.75)
    contentHeight: Math.min(1080, MpvqcWindowProperties.appHeight * 0.70)
    standardButtons: Dialog.Ok | Dialog.Cancel | Dialog.Reset

    onAccepted: _textArea.textDocument.save()

    onReset: _textArea.text = controller.defaultMpvConfiguration

    component Separator: Rectangle {
        property int topMargin: 0

        color: root.mpvqcTheme.control

        Layout.topMargin: topMargin
        Layout.preferredHeight: 1
        Layout.fillWidth: true
    }

    contentItem: ColumnLayout {

        Label {
            id: _label

            property string url: "https://mpv.io/manual/master/#configuration-files"
            property string text1: qsTranslate("MpvConfEditDialog", "Changes to the mpv.conf are available after a restart.")
            property string text2: qsTranslate("MpvConfEditDialog", "Learn more")

            horizontalAlignment: Text.AlignLeft
            text: `${text1} <a href="${url}">${text2}</a>.`

            Layout.topMargin: 20
            Layout.fillWidth: true

            onLinkActivated: link => root.controller.openLink(link)

            MouseArea {
                anchors.fill: parent

                acceptedButtons: Qt.NoButton
                cursorShape: _label.hoveredLink ? Qt.PointingHandCursor : Qt.ArrowCursor
                hoverEnabled: true
            }

            MpvqcTooltip {
                y: _label.height + 5

                text: _label.url
                visible: _label.hoveredLink
            }
        }

        Separator {
            topMargin: 20
        }

        ScrollView {
            id: _scrollView

            readonly property bool needsHorizontalScroll: contentWidth > width
            readonly property bool needsVerticalScroll: contentHeight > height

            Layout.fillWidth: true
            Layout.fillHeight: true

            ScrollBar.horizontal.policy: needsHorizontalScroll ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff
            ScrollBar.vertical.policy: needsVerticalScroll ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff

            TextArea {
                id: _textArea

                background: null
                font.family: "Noto Sans Mono"
                font.pointSize: 11
                leftPadding: _scrollView.mirrored && _scrollView.needsVerticalScroll ? 22 : 0
                textDocument.source: root.controller.mpvFileUrl
            }
        }

        Separator {}
    }
}
