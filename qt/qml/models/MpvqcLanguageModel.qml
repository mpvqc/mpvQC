// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

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
