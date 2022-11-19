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
    readonly property var languagesForTranslationTool: [
        qsTranslate("Languages", "English"),
        qsTranslate("Languages", "German"),
        qsTranslate("Languages", "Hebrew"),
        qsTranslate("Languages", "Italian"),
        qsTranslate("Languages", "Spanish"),
    ]

    ListElement {
        language: "English"
        identifier: "en-US"
    }
    ListElement {
        language: "German"
        identifier: "de-DE"
        translator: "Frechdachs"
    }
    ListElement {
        language: "Hebrew"
        identifier: "he-IL"
        translator: "cN3rd"
    }
    ListElement {
        language: "Italian"
        identifier: "it-IT"
        translator: "maddo"
    }
    ListElement {
        language: "Spanish"
        identifier: "es-ES"
        translator: "RcUchiha"
    }
}
