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
import Qt.labs.settings


Item {
    id: current
    required property var settingsFile
    property string nickname: settings.nickname
    property bool writeHeaderDate: settings.writeHeaderDate
    property bool writeHeaderGenerator: settings.writeHeaderGenerator
    property bool writeHeaderNickname: settings.writeHeaderNickname
    property bool writeHeaderVideoPath: settings.writeHeaderVideoPath

    Settings {
        id: settings
        fileName: current.settingsFile
        category: "Export"
        property string nickname: MpvqcDefaultNickname.defaultNickname
        property bool writeHeaderDate: true
        property bool writeHeaderGenerator: true
        property bool writeHeaderNickname: false
        property bool writeHeaderVideoPath: true
    }

    function store() {
        settings.nickname = current.nickname
        settings.writeHeaderDate = current.writeHeaderDate
        settings.writeHeaderGenerator = current.writeHeaderGenerator
        settings.writeHeaderNickname = current.writeHeaderNickname
        settings.writeHeaderVideoPath = current.writeHeaderVideoPath
    }

}
