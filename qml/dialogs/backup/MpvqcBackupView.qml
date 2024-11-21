/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import shared

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

    function accept() {
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
}
