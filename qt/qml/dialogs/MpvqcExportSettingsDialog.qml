// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Layouts

import pyobjects

import "../shared"

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
            label: qsTranslate("ExportSettingsDialog", "Write Date")
            checked: root.viewModel.temporaryWriteHeaderDate
            prefWidth: root.contentWidth

            onToggled: state => {
                root.viewModel.temporaryWriteHeaderDate = state;
            }
        }

        MpvqcSwitchRow {
            //: %1 will be the application name. Most probably 'mpvQC' :)
            label: qsTranslate("ExportSettingsDialog", "Write '%1'").arg(Qt.application.name)
            checked: root.viewModel.temporaryWriteHeaderGenerator
            prefWidth: root.contentWidth

            onToggled: state => {
                root.viewModel.temporaryWriteHeaderGenerator = state;
            }
        }

        MpvqcSwitchRow {
            label: qsTranslate("ExportSettingsDialog", "Write Nickname")
            checked: root.viewModel.temporaryWriteHeaderNickname
            prefWidth: root.contentWidth

            onToggled: state => {
                root.viewModel.temporaryWriteHeaderNickname = state;
            }
        }

        MpvqcSwitchRow {
            label: qsTranslate("ExportSettingsDialog", "Write Video Path")
            checked: root.viewModel.temporaryWriteHeaderVideoPath
            prefWidth: root.contentWidth

            onToggled: state => {
                root.viewModel.temporaryWriteHeaderVideoPath = state;
            }
        }

        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true
        }
    }

    onAccepted: root.viewModel.accept()
}
