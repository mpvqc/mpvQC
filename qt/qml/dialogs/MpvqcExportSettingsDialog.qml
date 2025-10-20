// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Layouts

import pyobjects

import "../components"

MpvqcDialog {
    id: root

    readonly property MpvqcExportSettingsDialogViewModel viewModel: MpvqcExportSettingsDialogViewModel {}

    title: qsTranslate("ExportSettingsDialog", "Export Settings")

    contentItem: ColumnLayout {
        spacing: 10

        MpvqcTextFieldRow {
            Layout.topMargin: 10

            label: qsTranslate("ExportSettingsDialog", "Nickname")
            input: root.viewModel.temporaryNickname
            spacing: 16
            fontWeight: Font.DemiBold
            prefWidth: root.contentWidth
            implicitTextFieldWidth: 150

            onTextChanged: text => {
                root.viewModel.temporaryNickname = text;
            }
        }

        MpvqcHeader {
            Layout.topMargin: 20
            Layout.bottomMargin: 10
            Layout.fillWidth: true

            text: qsTranslate("ExportSettingsDialog", "Document Header")
            horizontalAlignment: Text.AlignHCenter
        }

        MpvqcSwitchRow {
            Layout.fillWidth: true

            label: qsTranslate("ExportSettingsDialog", "Write Date")
            checked: root.viewModel.temporaryWriteHeaderDate

            onToggled: state => {
                root.viewModel.temporaryWriteHeaderDate = state;
            }
        }

        MpvqcSwitchRow {
            Layout.fillWidth: true

            //: %1 will be the application name. Most probably 'mpvQC' :)
            label: qsTranslate("ExportSettingsDialog", "Write '%1'").arg(Qt.application.name)
            checked: root.viewModel.temporaryWriteHeaderGenerator

            onToggled: state => {
                root.viewModel.temporaryWriteHeaderGenerator = state;
            }
        }

        MpvqcSwitchRow {
            Layout.fillWidth: true

            label: qsTranslate("ExportSettingsDialog", "Write Nickname")
            checked: root.viewModel.temporaryWriteHeaderNickname

            onToggled: state => {
                root.viewModel.temporaryWriteHeaderNickname = state;
            }
        }

        MpvqcSwitchRow {
            Layout.fillWidth: true

            label: qsTranslate("ExportSettingsDialog", "Write Video Path")
            checked: root.viewModel.temporaryWriteHeaderVideoPath

            onToggled: state => {
                root.viewModel.temporaryWriteHeaderVideoPath = state;
            }
        }

        MpvqcSwitchRow {
            Layout.fillWidth: true

            label: qsTranslate("ExportSettingsDialog", "Write Subtitle Paths")
            checked: root.viewModel.temporaryWriteHeaderSubtitles

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
