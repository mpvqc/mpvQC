// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material
import QtQuick.Layouts

import "../../shared"

ColumnLayout {
    id: root

    required property var mpvqcApplication

    property var mpvqcSettings: mpvqcApplication.mpvqcSettings
    property var mpvqcApplicationPathsPyObject: mpvqcApplication.mpvqcApplicationPathsPyObject
    property var mpvqcUtilityPyObject: mpvqcApplication.mpvqcUtilityPyObject

    property alias backupEnabledSwitch: _backupEnable
    property alias backupIntervalSpinBox: _backupInterval.spinBox
    property alias backupLocationOpenButton: _backupLocationOpenButton

    property bool currentBackupEnabled: root.mpvqcSettings.backupEnabled
    property int currentBackupInterval: root.mpvqcSettings.backupInterval

    function accept(): void {
        mpvqcSettings.backupEnabled = currentBackupEnabled;
        mpvqcSettings.backupInterval = currentBackupInterval;
    }

    MpvqcSwitchRow {
        id: _backupEnable

        label: qsTranslate("BackupDialog", "Backup Enabled")
        prefWidth: root.width
        checked: root.currentBackupEnabled
        Layout.topMargin: 20

        onToggled: state => {
            root.currentBackupEnabled = state;
        }
    }

    MpvqcSpinBoxRow {
        id: _backupInterval

        label: qsTranslate("BackupDialog", "Backup Interval")
        suffix: qsTranslate("BackupDialog", "Seconds")
        prefWidth: root.width
        value: root.currentBackupInterval
        valueFrom: 15
        valueTo: 5 * 60

        onValueModified: value => {
            root.currentBackupInterval = value;
        }
    }

    ToolButton {
        id: _backupLocationOpenButton

        property url backupDirectory: root.mpvqcApplicationPathsPyObject.dir_backup

        text: qsTranslate("BackupDialog", "Backup Location")
        icon.source: "qrc:/data/icons/launch_black_24dp.svg"
        hoverEnabled: true
        Layout.alignment: Qt.AlignHCenter
        Layout.topMargin: 40
        Layout.fillWidth: true

        onPressed: {
            Qt.openUrlExternally(backupDirectory);
        }

        ToolTip {
            y: -_backupLocationOpenButton.height + 10
            delay: 500
            visible: _backupLocationOpenButton.hovered
            text: root.mpvqcUtilityPyObject.urlToAbsolutePath(_backupLocationOpenButton.backupDirectory)
        }
    }

    Item {
        Layout.fillWidth: true
        Layout.fillHeight: true
    }
}
