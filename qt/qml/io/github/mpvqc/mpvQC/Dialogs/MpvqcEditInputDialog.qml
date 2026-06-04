// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Python
import io.github.mpvqc.mpvQC.Utility

MpvqcDialog {
    id: root
    objectName: "editInputDialog"

    readonly property MpvqcEditInputDialogViewModel viewModel: MpvqcEditInputDialogViewModel {}
    readonly property var mpvqcTheme: MpvqcTheme

    title: qsTranslate("InputConfEditDialog", "Edit input.conf")
    contentWidth: Math.min(1080, MpvqcWindowUtility.appWidth * 0.75)
    contentHeight: Math.min(1080, MpvqcWindowUtility.appHeight * 0.70)
    standardButtons: Dialog.Ok | Dialog.Cancel | Dialog.Reset

    onAccepted: _textArea.textDocument.save()

    onReset: _textArea.text = viewModel.defaultInputConfiguration

    component Separator: Rectangle {
        property int topMargin: 0

        color: root.mpvqcTheme.palette.separator

        Layout.topMargin: topMargin
        Layout.preferredHeight: 1
        Layout.fillWidth: true
    }

    contentItem: ColumnLayout {

        Label {
            id: _label
            objectName: "inputConfLearnMoreLabel"

            property string url: "https://mpv.io/manual/master/#list-of-input-commands"
            property string text1: qsTranslate("InputConfEditDialog", "Changes to the input.conf are available after a restart.")
            property string text2: qsTranslate("InputConfEditDialog", "Learn more")

            horizontalAlignment: Text.AlignLeft
            text: `${text1} <a href="${url}">${text2}</a>.`

            Layout.topMargin: 20
            Layout.fillWidth: true

            onLinkActivated: link => root.viewModel.openLink(link)

            HoverHandler {
                cursorShape: _label.hoveredLink ? Qt.PointingHandCursor : undefined
            }

            ToolTip.delay: 350
            ToolTip.text: url
            ToolTip.visible: hoveredLink
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
                objectName: "inputConfTextArea"

                background: null
                font: MpvqcFonts.monospaceFont
                leftPadding: _scrollView.mirrored && _scrollView.needsVerticalScroll ? 22 : 0
                textDocument.source: root.viewModel.inputFileUrl

                ContextMenu.menu: null
            }
        }

        Separator {}
    }
}
