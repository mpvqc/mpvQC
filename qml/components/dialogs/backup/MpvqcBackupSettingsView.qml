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
import components
import pyobjects
import settings


ColumnLayout {
    spacing: 2

    ToolButton {
        text: qsTranslate("BackupSettings", "Backup Location")
        icon.source: "qrc:/data/icons/launch_black_24dp.svg"
        hoverEnabled: true
        ToolTip.visible: hovered
        ToolTip.text: FileIoPyObject.abs_path_of(backupDirectory)
        Layout.alignment: Qt.AlignHCenter
        Layout.bottomMargin: 36
        Layout.fillWidth: true

        property url backupDirectory: MpvqcFilePathsPyObject.dir_backup

        onClicked: {
            Qt.openUrlExternally(backupDirectory)
        }
    }

    MpvqcSwitchRow {
        id: backupEnable
        label: qsTranslate("BackupSettings", "Backup Enabled")
        state: MpvqcSettings.backupEnabled
    }

    MpvqcSpinBoxRow {
        id: backupInterval
        label: qsTranslate("BackupSettings", "Backup Interval")
        value: MpvqcSettings.backupInterval
        Layout.topMargin: 16
    }

    function save() {
        MpvqcSettings.backupEnabled = backupEnable.state
        MpvqcSettings.backupInterval = backupInterval.value
    }

}
