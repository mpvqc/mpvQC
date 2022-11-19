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
import Qt.labs.settings
import models


Item {
    id: root

    readonly property var languages: MpvqcLanguageModel {}
    property var uiLanguages: Qt.locale().uiLanguages
    property alias language: settings.language

    Settings {
        id: settings
        // fileName: current.settingsFile
        category: 'Common'
        property string language: root.defaultLanguage()
    }

    function defaultLanguage() {
        for (let idx = 0, count = languages.count; idx < count; idx++) {
            const language = languages.get(idx).identifier
            if (uiLanguages.includes(language)) {
                return language
            }
        }
        return 'en-US'
    }

}
