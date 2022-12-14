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
    property var mpvqcFilePathsPyObject: mpvqcApplication.mpvqcFilePathsPyObject
    property var mpvqcFileSystemHelperPyObject: mpvqcApplication.mpvqcFileSystemHelperPyObject

    property alias backupEnabledSwitch: _backupEnable
    property alias backupIntervalSpinBox: _backupInterval.spinBox
    property alias backupLocationOpenButton: _backupLocationOpenButton

    property var openBackupLocationFunc: Qt.openUrlExternally

    MpvqcSwitchRow {
        id: _backupEnable

        label: qsTranslate("BackupSettings", "Backup Enabled")
        prefWidth: root.width
        checked: mpvqcSettings.backupEnabled
        Layout.topMargin: 20

        onToggled: (state) => {
            mpvqcSettings.backupEnabled = state
        }
    }

    MpvqcSpinBoxRow {
        id: _backupInterval

        label: qsTranslate("BackupSettings", "Backup Interval")
        suffix: qsTranslate("BackupSettings", "Seconds")
        prefWidth: root.width
        value: root.mpvqcSettings.backupInterval
        valueFrom: 15
        valueTo: 5 * 60

        onValueModified: (value) => {
            mpvqcSettings.backupInterval = value
        }
    }

    ToolButton {
        id: _backupLocationOpenButton

        property url backupDirectory: root.mpvqcFilePathsPyObject.dir_backup

        text: qsTranslate("BackupSettings", "Backup Location")
        icon.source: "qrc:/data/icons/launch_black_24dp.svg"
        hoverEnabled: true
        Layout.alignment: Qt.AlignHCenter
        Layout.topMargin: 40
        Layout.fillWidth: true

        onClicked: {
            root.openBackupLocationFunc(backupDirectory)
        }

        ToolTip {
            visible: _backupLocationOpenButton.hovered
            text: root.mpvqcFileSystemHelperPyObject.url_to_absolute_path(_backupLocationOpenButton.backupDirectory)
            y: - (_backupLocationOpenButton.height - 10)
        }

    }

}
