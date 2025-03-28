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
import QtQuick.Controls.Material

import shared
import settings

MpvqcMenu {
    id: root

    required property var mpvqcApplication

    readonly property var mpvqcSettings: mpvqcApplication.mpvqcSettings

    readonly property alias defaultFormat: _defaultFormat
    readonly property alias fileNameFormat: _fileNameFormat
    readonly property alias filePathFormat: _filePathFormat

    title: qsTranslate("MainWindow", "Application Title")
    icon.source: "qrc:/data/icons/title_black_24dp.svg"
    icon.height: 24
    icon.width: 24

    MenuItem {
        id: _defaultFormat

        property var selection: MpvqcSettings.WindowTitleFormat.DEFAULT // qmllint disable unqualified

        text: qsTranslate("MainWindow", "Default Title")
        autoExclusive: true
        checkable: true
        checked: root.mpvqcSettings.windowTitleFormat === selection

        onTriggered: {
            root.mpvqcSettings.windowTitleFormat = selection;
        }
    }

    MenuItem {
        id: _fileNameFormat

        property var selection: MpvqcSettings.WindowTitleFormat.FILE_NAME  // qmllint disable unqualified

        text: qsTranslate("MainWindow", "Video File")
        autoExclusive: true
        checkable: true
        checked: root.mpvqcSettings.windowTitleFormat === selection

        onTriggered: {
            root.mpvqcSettings.windowTitleFormat = selection;
        }
    }

    MenuItem {
        id: _filePathFormat

        property var selection: MpvqcSettings.WindowTitleFormat.FILE_PATH // qmllint disable unqualified

        text: qsTranslate("MainWindow", "Video Path")
        autoExclusive: true
        checkable: true
        checked: root.mpvqcSettings.windowTitleFormat === selection

        onTriggered: {
            root.mpvqcSettings.windowTitleFormat = selection;
        }
    }
}
