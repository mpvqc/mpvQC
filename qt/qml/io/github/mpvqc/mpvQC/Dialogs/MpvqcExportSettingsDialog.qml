// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

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

    contentHeight: MpvqcConstants.smallDialogContentHeight

    title: qsTranslate("ExportSettingsDialog", "Export Settings")
    standardButtons: Dialog.Ok | Dialog.Cancel

    contentItem: ColumnLayout {
        spacing: 10

        MpvqcTextFieldRow {
            objectName: "exportNicknameRow"

            label: qsTranslate("ExportSettingsDialog", "Nickname")
            input: root.viewModel.temporaryNickname
            spacing: 16
            fontWeight: Font.DemiBold
            prefWidth: root.contentWidth
            implicitTextFieldWidth: 150

            Layout.topMargin: 10

            onTextChanged: text => {
                root.viewModel.temporaryNickname = text;
            }
        }

        MpvqcHeader {
            text: qsTranslate("ExportSettingsDialog", "Document Header")
            horizontalAlignment: Text.AlignHCenter

            Layout.topMargin: 20
            Layout.bottomMargin: 10
            Layout.fillWidth: true
        }

        MpvqcSwitchRow {
            objectName: "exportWriteDateRow"

            label: qsTranslate("ExportSettingsDialog", "Write Date")
            checked: root.viewModel.temporaryWriteHeaderDate

            Layout.fillWidth: true

            onToggled: state => {
                root.viewModel.temporaryWriteHeaderDate = state;
            }
        }

        MpvqcSwitchRow {
            objectName: "exportWriteGeneratorRow"

            //: %1 will be the application name. Most probably 'mpvQC' :)
            label: qsTranslate("ExportSettingsDialog", "Write '%1'").arg(Qt.application.name)
            checked: root.viewModel.temporaryWriteHeaderGenerator

            Layout.fillWidth: true

            onToggled: state => {
                root.viewModel.temporaryWriteHeaderGenerator = state;
            }
        }

        MpvqcSwitchRow {
            objectName: "exportWriteNicknameRow"

            label: qsTranslate("ExportSettingsDialog", "Write Nickname")
            checked: root.viewModel.temporaryWriteHeaderNickname

            Layout.fillWidth: true

            onToggled: state => {
                root.viewModel.temporaryWriteHeaderNickname = state;
            }
        }

        MpvqcSwitchRow {
            objectName: "exportWriteVideoPathRow"

            label: qsTranslate("ExportSettingsDialog", "Write Video Path")
            checked: root.viewModel.temporaryWriteHeaderVideoPath

            Layout.fillWidth: true

            onToggled: state => {
                root.viewModel.temporaryWriteHeaderVideoPath = state;
            }
        }

        MpvqcSwitchRow {
            objectName: "exportWriteSubtitlesRow"

            label: qsTranslate("ExportSettingsDialog", "Write Subtitle Paths")
            //: Tooltip for the "Write Subtitle Paths" export setting.
            labelToolTip: qsTranslate("ExportSettingsDialog", "Include paths of manually imported subtitle files in the document header")
            checked: root.viewModel.temporaryWriteHeaderSubtitles

            Layout.fillWidth: true

            onToggled: state => {
                root.viewModel.temporaryWriteHeaderSubtitles = state;
            }
        }

        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true
        }
    }

    onAccepted: root.viewModel.accept()
}
