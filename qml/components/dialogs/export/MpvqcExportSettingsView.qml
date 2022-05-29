/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/


import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import components.shared
import helpers
import settings


ColumnLayout{
    id: column
    spacing: 2

    MpvqcNicknameRow {
        id: nickname
        spacing: 16
        parentWidth: column.width
    }

    MpvqcDemiBoldLabel {
        text: qsTranslate("AppearanceDialog", "Document Header")
        Layout.topMargin: 36
        Layout.bottomMargin: 18
        Layout.fillWidth: true
    }

    MpvqcSwitchRow {
        id: dateHeader
        labelText: qsTranslate("ExportSettings", "Write Date")
        parentWidth: column.width
        switchChecked: MpvqcSettings.writeHeaderDate

        onSaveTriggered: (checked) => {
            MpvqcSettings.writeHeaderDate = checked
        }
    }

    MpvqcSwitchRow {
        id: generatorHeader
        labelText: qsTranslate("ExportSettings", "Write '%1'").arg(Qt.application.name)
        parentWidth: column.width
        switchChecked: MpvqcSettings.writeHeaderGenerator

        onSaveTriggered: (checked) => {
            MpvqcSettings.writeHeaderGenerator = checked
        }
    }

    MpvqcSwitchRow {
        id: nicknameHeader
        labelText: qsTranslate("ExportSettings", "Write Nickname")
        parentWidth: column.width
        switchChecked: MpvqcSettings.writeHeaderNickname

        onSaveTriggered: (checked) => {
            MpvqcSettings.writeHeaderNickname = checked
        }
    }

    MpvqcSwitchRow {
        id: pathHeader
        labelText: qsTranslate("ExportSettings", "Write Video Path")
        parentWidth: column.width
        switchChecked: MpvqcSettings.writeHeaderVideoPath

        onSaveTriggered: (checked) => {
            MpvqcSettings.writeHeaderVideoPath = checked
        }
    }

    function save() {
        const settings = [nickname, dateHeader, generatorHeader, nicknameHeader, pathHeader]
        for (const setting of settings) {
            setting.save()
        }
    }

}
