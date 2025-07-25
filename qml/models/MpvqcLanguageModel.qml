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

ListModel {
    readonly property string systemLanguage: {
        const uiLanguages = Qt.locale().uiLanguages;
        return _identifiers().find(language => uiLanguages.includes(language)) ?? "en-US";
    }

    function _identifiers(): list<string> {
        const marshalled = [];
        for (let i = 0; i < count; i++) {
            marshalled.push(get(i).identifier);
        }
        return marshalled;
    }

    ListElement {
        language: QT_TRANSLATE_NOOP("Languages", "German")
        identifier: "de-DE"
    }
    ListElement {
        language: QT_TRANSLATE_NOOP("Languages", "English")
        identifier: "en-US"
    }
    ListElement {
        language: QT_TRANSLATE_NOOP("Languages", "Spanish")
        identifier: "es-MX"
        translator: "CiferrC"
    }
    ListElement {
        language: QT_TRANSLATE_NOOP("Languages", "Hebrew")
        identifier: "he-IL"
        translator: "cN3rd"
    }
    ListElement {
        language: QT_TRANSLATE_NOOP("Languages", "Italian")
        identifier: "it-IT"
        translator: "maddo"
    }
    ListElement {
        language: QT_TRANSLATE_NOOP("Languages", "Portuguese")
        identifier: "pt-PT"
        translator: "Diogo_23"
    }
}
