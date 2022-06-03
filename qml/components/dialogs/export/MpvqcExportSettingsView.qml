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
import settings


ColumnLayout {
    spacing: 2

    MpvqcTextFieldRow {
        id: nickname
        label: qsTranslate("ExportSettings", "Nickname")
        input: MpvqcSettings.nickname
    }

    MpvqcDemiBoldLabel {
        text: qsTranslate("AppearanceDialog", "Document Header")
        Layout.topMargin: 36
        Layout.bottomMargin: 18
        Layout.fillWidth: true
    }

    MpvqcSwitchRow {
        id: dateHeader
        label: qsTranslate("ExportSettings", "Write Date")
        state: MpvqcSettings.writeHeaderDate
    }

    MpvqcSwitchRow {
        id: generatorHeader
        label: qsTranslate("ExportSettings", "Write '%1'").arg(Qt.application.name)
        state: MpvqcSettings.writeHeaderGenerator
    }

    MpvqcSwitchRow {
        id: nicknameHeader
        label: qsTranslate("ExportSettings", "Write Nickname")
        state: MpvqcSettings.writeHeaderNickname
    }

    MpvqcSwitchRow {
        id: pathHeader
        label: qsTranslate("ExportSettings", "Write Video Path")
        state: MpvqcSettings.writeHeaderVideoPath
    }

    function save() {
        MpvqcSettings.nickname = nickname.input
        MpvqcSettings.writeHeaderDate = dateHeader.state
        MpvqcSettings.writeHeaderGenerator = generatorHeader.state
        MpvqcSettings.writeHeaderNickname = nicknameHeader.state
        MpvqcSettings.writeHeaderVideoPath = pathHeader.state
    }

}
