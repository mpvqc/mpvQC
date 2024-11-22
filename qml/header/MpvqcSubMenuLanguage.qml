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

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls

import models
import shared

MpvqcMenu {
    id: root

    required property var mpvqcApplication

    readonly property var mpvqcSettings: mpvqcApplication.mpvqcSettings

    readonly property alias repeater: _repeater

    title: qsTranslate("MainWindow", "Language")
    icon.source: "qrc:/data/icons/language_black_24dp.svg"
    icon.height: 24
    icon.width: 24

    Repeater {
        id: _repeater

        model: MpvqcLanguageModel {}

        MenuItem {
            id: item

            required property string language
            required property string identifier

            property var timer: Timer {
                interval: 125

                onTriggered: {
                    Qt.uiLanguage = item.identifier;
                    root.mpvqcSettings.language = item.identifier;
                }
            }

            text: qsTranslate("Languages", item.language)
            autoExclusive: true
            checkable: true
            checked: item.identifier === Qt.uiLanguage

            function changeLanguage() {
                timer.start();
            }

            onTriggered: {
                changeLanguage();
            }
        }
    }
}
