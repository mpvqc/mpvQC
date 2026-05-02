// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material
import QtQuick.Layouts

import pyobjects

import "../components"
import "../utility"

MpvqcDialog {
    id: root
    objectName: "backupDialog"

    readonly property MpvqcBackupDialogViewModel viewModel: MpvqcBackupDialogViewModel {}

    readonly property int minBackupInterval: 15
    readonly property int maxBackupInterval: 5 * 60

    contentHeight: 450

    title: qsTranslate("BackupDialog", "Backup Settings")

    contentItem: ColumnLayout {

        MpvqcSwitchRow {
            objectName: "backupEnabledRow"

            Layout.topMargin: 20
            Layout.fillWidth: true

            label: qsTranslate("BackupDialog", "Backup Enabled")
            checked: root.viewModel.temporaryBackupEnabled

            onToggled: state => {
                root.viewModel.temporaryBackupEnabled = state;
            }
        }

        MpvqcSpinBoxRow {
            objectName: "backupIntervalRow"

            label: qsTranslate("BackupDialog", "Backup Interval")
            suffix: qsTranslate("BackupDialog", "Seconds")
            prefWidth: parent.width

            value: root.viewModel.temporaryBackupInterval
            valueFrom: root.minBackupInterval
            valueTo: root.maxBackupInterval

            onValueModified: value => {
                root.viewModel.temporaryBackupInterval = value;
            }
        }

        Button {
            objectName: "backupOpenLocationButton"

            text: qsTranslate("BackupDialog", "Backup Location")
            icon.source: MpvqcIcons.folderOpen
            hoverEnabled: true
            Layout.alignment: Qt.AlignHCenter
            Layout.topMargin: 40

            onPressed: root.viewModel.openBackupDirectory()

            ToolTip.delay: 350
            ToolTip.text: root.viewModel.backupDirectory
            ToolTip.visible: hovered
        }

        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true
        }
    }

    onAccepted: root.viewModel.accept()
}
