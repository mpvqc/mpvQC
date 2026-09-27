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

    title: qsTranslate("InputConfEditDialog", "Edit input.conf")
    contentWidth: Math.min(1080, MpvqcWindowUtility.windowGeometryWidth * 0.75)
    contentHeight: Math.min(1080, MpvqcWindowUtility.windowGeometryHeight * 0.70)
    standardButtons: Dialog.RestoreDefaults | Dialog.Cancel | Dialog.Ok

    contentItem: ColumnLayout {
        spacing: MpvqcConstants.dialogSectionSpacing

        Label {
            id: _label
            objectName: "inputConfLearnMoreLabel"

            property string url: "https://mpv.io/manual/master/#list-of-input-commands"
            property string text1: qsTranslate("InputConfEditDialog", "Changes to the input.conf are available after a restart.")
            property string text2: qsTranslate("InputConfEditDialog", "Learn more")

            text: `${text1} <a href="${url}">${text2}</a>.`
            color: MpvqcAppearance.palette.hint
            linkColor: MpvqcAppearance.palette.accent
            horizontalAlignment: Text.AlignLeft
            wrapMode: Text.Wrap

            Layout.fillWidth: true
            Layout.topMargin: MpvqcConstants.dialogContentTopMargin

            ToolTip.delay: MpvqcConstants.tooltipDelay
            ToolTip.text: url
            ToolTip.visible: hoveredLink

            onLinkActivated: link => root.viewModel.openLink(link)

            HoverHandler {
                cursorShape: _label.hoveredLink ? Qt.PointingHandCursor : undefined
            }
        }

        Rectangle {
            objectName: "inputConfEditorCard"

            radius: 20
            color: MpvqcAppearance.palette.sectionCard

            Layout.fillWidth: true
            Layout.fillHeight: true

            ScrollView {
                id: _scrollView

                readonly property bool needsHorizontalScroll: contentWidth > width
                readonly property bool needsVerticalScroll: contentHeight > height

                anchors.fill: parent
                anchors.margins: 12
                anchors.leftMargin: 20

                ScrollBar.horizontal: MpvqcScrollBar {
                    parent: _scrollView
                    x: _scrollView.leftPadding
                    y: _scrollView.height - height
                    width: _scrollView.availableWidth
                    policy: _scrollView.needsHorizontalScroll ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff
                }
                ScrollBar.vertical: MpvqcScrollBar {
                    parent: _scrollView
                    x: _scrollView.mirrored ? 0 : _scrollView.width - width
                    y: _scrollView.topPadding
                    height: _scrollView.availableHeight
                    policy: _scrollView.needsVerticalScroll ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff
                }

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
        }
    }

    onAccepted: _textArea.textDocument.save()
    onReset: _textArea.text = viewModel.defaultInputConfiguration
}
