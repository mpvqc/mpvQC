// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material
import QtQuick.Layouts

import pyobjects

import "../shared"

MpvqcDialog {
    id: root

    readonly property MpvqcBackupDialogControllerPyObject controller: MpvqcBackupDialogControllerPyObject {}

    readonly property int minBackupInterval: 15
    readonly property int maxBackupInterval: 5 * 60

    title: qsTranslate("BackupDialog", "Backup Settings")

    contentItem: ColumnLayout {

        MpvqcSwitchRow {
            Layout.topMargin: 20

            label: qsTranslate("BackupDialog", "Backup Enabled")
            prefWidth: parent.width
            checked: root.controller.temporaryBackupEnabled

            onToggled: state => {
                root.controller.temporaryBackupEnabled = state;
            }
        }

        MpvqcSpinBoxRow {
            label: qsTranslate("BackupDialog", "Backup Interval")
            suffix: qsTranslate("BackupDialog", "Seconds")
            prefWidth: parent.width

            value: root.controller.temporaryBackupInterval
            valueFrom: root.minBackupInterval
            valueTo: root.maxBackupInterval

            onValueModified: value => {
                root.controller.temporaryBackupInterval = value;
            }
        }

        Button {
            text: qsTranslate("BackupDialog", "Backup Location")
            icon.source: "qrc:/data/icons/folder_open_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
            hoverEnabled: true
            Layout.alignment: Qt.AlignHCenter
            Layout.topMargin: 40

            onPressed: root.controller.openBackupDirectory()

            MpvqcTooltip {
                y: -parent.height + 10
                z: 10
                visible: (parent as Button).hovered
                text: root.controller.backupDirectory
            }
        }

        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true
        }
    }

    onAccepted: root.controller.accept()
}
