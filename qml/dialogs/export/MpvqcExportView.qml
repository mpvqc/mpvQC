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
import QtQuick.Layouts

import shared


ColumnLayout {
    id: root

    required property var mpvqcApplication

    property var mpvqcSettings: mpvqcApplication.mpvqcSettings

    property alias nicknameInput: _nicknameInput
    property alias dateToggle: _dateToggle
    property alias generatorToggle: _generatorToggle
    property alias nicknameToggle: _nicknameToggle
    property alias pathToggle: _pathToggle

    MpvqcTextFieldRow {
        id: _nicknameInput

        label: qsTranslate("ExportSettings", "Nickname")
        input: root.mpvqcSettings.nickname
        spacing: 16
        fontWeight: Font.DemiBold
        prefWidth: root.width
        implicitTextFieldWidth: 150
        Layout.topMargin: 20

        onTextChanged: (text) => {
            root.mpvqcSettings.nickname = text
        }
    }

    MpvqcHeader {
        text: qsTranslate("ExportSettings", "Document Header")
        Layout.topMargin: 30
        Layout.bottomMargin: 10
        Layout.fillWidth: true
    }

    MpvqcSwitchRow {
        id: _dateToggle

        label: qsTranslate("ExportSettings", "Write Date")
        checked: root.mpvqcSettings.writeHeaderDate
        prefWidth: root.width

        onToggled: (state) => {
            root.mpvqcSettings.writeHeaderDate = state
        }
    }

    MpvqcSwitchRow {
        id: _generatorToggle

        label: qsTranslate("ExportSettings", "Write '%1'").arg(Qt.application.name)
        checked: root.mpvqcSettings.writeHeaderGenerator
        prefWidth: root.width

        onToggled: (state) => {
            root.mpvqcSettings.writeHeaderGenerator = state
        }
    }

    MpvqcSwitchRow {
        id: _nicknameToggle

        label: qsTranslate("ExportSettings", "Write Nickname")
        checked: root.mpvqcSettings.writeHeaderNickname
        prefWidth: root.width

        onToggled: (state) => {
            root.mpvqcSettings.writeHeaderNickname = state
        }
    }

    MpvqcSwitchRow {
        id: _pathToggle

        label: qsTranslate("ExportSettings", "Write Video Path")
        checked: root.mpvqcSettings.writeHeaderVideoPath
        prefWidth: root.width

        onToggled: (state) => {
            root.mpvqcSettings.writeHeaderVideoPath = state
        }
    }

}
