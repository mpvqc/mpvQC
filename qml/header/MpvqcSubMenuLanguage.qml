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

import models
import shared


MpvqcMenu {
    id: root

    required property var mpvqcApplication

    property var mpvqcSettings: mpvqcApplication.mpvqcSettings

    property alias repeater: _repeater

    title: qsTranslate("MainWindow", "&Language")

    Repeater {
        id: _repeater

        model: MpvqcLanguageModel {}

        MenuItem {
            id: item

            required property var language
            required property var identifier

            property var timer: Timer {
                interval: 125

                onTriggered: {
                    Qt.uiLanguage = item.identifier
                    root.mpvqcSettings.language = item.identifier
                }
            }

            text: qsTranslate("Languages", item.language)
            autoExclusive: true
            checkable: true
            checked: item.identifier === Qt.uiLanguage

            function changeLanguage() {
                timer.start()
            }

            onTriggered: {
                changeLanguage()
            }
        }
    }

}
