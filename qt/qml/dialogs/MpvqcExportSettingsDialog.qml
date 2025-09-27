// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Layouts

import pyobjects

import "../shared"

MpvqcDialog {
    id: root

    readonly property MpvqcExportSettingsDialogControllerPyObject controller: MpvqcExportSettingsDialogControllerPyObject {}

    title: qsTranslate("ExportSettingsDialog", "Export Settings")

    contentItem: ColumnLayout {
        spacing: 10

        MpvqcTextFieldRow {
            Layout.topMargin: 10

            label: qsTranslate("ExportSettingsDialog", "Nickname")
            input: root.controller.temporaryNickname
            spacing: 16
            fontWeight: Font.DemiBold
            prefWidth: root.contentWidth
            implicitTextFieldWidth: 150

            onTextChanged: text => {
                root.controller.temporaryNickname = text;
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
            checked: root.controller.temporaryWriteHeaderDate
            prefWidth: root.contentWidth

            onToggled: state => {
                root.controller.temporaryWriteHeaderDate = state;
            }
        }

        MpvqcSwitchRow {
            //: %1 will be the application name. Most probably 'mpvQC' :)
            label: qsTranslate("ExportSettingsDialog", "Write '%1'").arg(Qt.application.name)
            checked: root.controller.temporaryWriteHeaderGenerator
            prefWidth: root.contentWidth

            onToggled: state => {
                root.controller.temporaryWriteHeaderGenerator = state;
            }
        }

        MpvqcSwitchRow {
            label: qsTranslate("ExportSettingsDialog", "Write Nickname")
            checked: root.controller.temporaryWriteHeaderNickname
            prefWidth: root.contentWidth

            onToggled: state => {
                root.controller.temporaryWriteHeaderNickname = state;
            }
        }

        MpvqcSwitchRow {
            label: qsTranslate("ExportSettingsDialog", "Write Video Path")
            checked: root.controller.temporaryWriteHeaderVideoPath
            prefWidth: root.contentWidth

            onToggled: state => {
                root.controller.temporaryWriteHeaderVideoPath = state;
            }
        }

        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true
        }
    }

    onAccepted: root.controller.accept()
}
