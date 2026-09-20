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
    objectName: "exportSettingsDialog"

    readonly property MpvqcExportSettingsDialogViewModel viewModel: MpvqcExportSettingsDialogViewModel {}

    width: Math.min(contentWidth + leftPadding + rightPadding, Math.max(0, (Overlay.overlay?.width ?? 0) - 2 * margins))
    contentWidth: MpvqcConstants.smallDialogContentWidth
    contentHeight: Math.min(_sections.implicitHeight, Math.max(0, (Overlay.overlay?.height ?? 0) - 2 * margins - topPadding - bottomPadding - implicitHeaderHeight - implicitFooterHeight - 2 * spacing))
    margins: MpvqcConstants.dialogEdgeMargin
    title: qsTranslate("ExportSettingsDialog", "Export Settings")
    standardButtons: Dialog.Ok | Dialog.Cancel

    contentItem: ScrollView {
        id: _scroll

        clip: true
        contentWidth: availableWidth
        contentHeight: _sections.implicitHeight

        ScrollBar.horizontal.policy: ScrollBar.AlwaysOff

        ColumnLayout {
            id: _sections

            width: _scroll.availableWidth
            spacing: MpvqcConstants.dialogSectionSpacing

            MpvqcSectionCard {
                title: qsTranslate("ExportSettingsDialog", "Nickname")

                Layout.fillWidth: true
                Layout.topMargin: MpvqcConstants.dialogContentTopMargin

                TextField {
                    id: _nickname
                    objectName: "exportNicknameField"

                    text: root.viewModel.temporaryNickname
                    selectByMouse: true
                    bottomPadding: topPadding
                    // Inherited mirroring can leave the rendered text at its old alignment.
                    horizontalAlignment: _sections.LayoutMirroring.enabled ? Text.AlignRight : Text.AlignLeft

                    ContextMenu.menu: null
                    LayoutMirroring.enabled: false
                    Layout.fillWidth: true

                    onTextEdited: root.viewModel.temporaryNickname = text
                }
            }

            MpvqcSectionCard {
                title: qsTranslate("ExportSettingsDialog", "Document Header")
                spacing: 0

                Layout.fillWidth: true

                MpvqcSwitchRow {
                    objectName: "exportWriteDateRow"

                    label: qsTranslate("ExportSettingsDialog", "Write Date")
                    checked: root.viewModel.temporaryWriteHeaderDate
                    edgeAligned: true

                    Layout.fillWidth: true

                    onToggled: state => root.viewModel.temporaryWriteHeaderDate = state
                }

                MpvqcSwitchRow {
                    objectName: "exportWriteGeneratorRow"

                    //: %1 will be the application name. Most probably 'mpvQC' :)
                    label: qsTranslate("ExportSettingsDialog", "Write '%1'").arg(Qt.application.name)
                    checked: root.viewModel.temporaryWriteHeaderGenerator
                    edgeAligned: true

                    Layout.fillWidth: true

                    onToggled: state => root.viewModel.temporaryWriteHeaderGenerator = state
                }

                MpvqcSwitchRow {
                    objectName: "exportWriteNicknameRow"

                    label: qsTranslate("ExportSettingsDialog", "Write Nickname")
                    checked: root.viewModel.temporaryWriteHeaderNickname
                    edgeAligned: true

                    Layout.fillWidth: true

                    onToggled: state => root.viewModel.temporaryWriteHeaderNickname = state
                }

                MpvqcSwitchRow {
                    objectName: "exportWriteVideoPathRow"

                    label: qsTranslate("ExportSettingsDialog", "Write Video Path")
                    checked: root.viewModel.temporaryWriteHeaderVideoPath
                    edgeAligned: true

                    Layout.fillWidth: true

                    onToggled: state => root.viewModel.temporaryWriteHeaderVideoPath = state
                }

                MpvqcSwitchRow {
                    objectName: "exportWriteSubtitlesRow"

                    label: qsTranslate("ExportSettingsDialog", "Write Subtitle Paths")
                    //: Tooltip for the "Write Subtitle Paths" export setting.
                    labelToolTip: qsTranslate("ExportSettingsDialog", "Include paths of manually imported subtitle files in the document header")
                    checked: root.viewModel.temporaryWriteHeaderSubtitles
                    edgeAligned: true

                    Layout.fillWidth: true

                    onToggled: state => root.viewModel.temporaryWriteHeaderSubtitles = state
                }
            }
        }
    }

    onAboutToShow: _nickname.forceActiveFocus(Qt.PopupFocusReason)
    onAccepted: root.viewModel.accept()
}
