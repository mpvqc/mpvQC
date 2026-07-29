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
    objectName: "backupDialog"

    readonly property MpvqcBackupDialogViewModel viewModel: MpvqcBackupDialogViewModel {}

    readonly property int minBackupInterval: 15
    readonly property int maxBackupInterval: 5 * 60

    contentHeight: MpvqcConstants.smallDialogContentHeight

    title: qsTranslate("BackupDialog", "Backup Settings")
    standardButtons: Dialog.Ok | Dialog.Cancel

    contentItem: ColumnLayout {

        MpvqcSwitchRow {
            objectName: "backupEnabledRow"

            label: qsTranslate("BackupDialog", "Backup Enabled")
            checked: root.viewModel.temporaryBackupEnabled

            Layout.topMargin: 20
            Layout.fillWidth: true

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

            ToolTip.delay: 350
            ToolTip.text: root.viewModel.backupDirectory
            ToolTip.visible: hovered

            onPressed: root.viewModel.openBackupDirectory()
        }

        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true
        }
    }

    onAccepted: root.viewModel.accept()
}
