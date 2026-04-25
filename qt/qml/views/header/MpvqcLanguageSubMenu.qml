// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material

import pyobjects

MpvqcMenuBarMenu {
    id: root
    objectName: "languageMenu"

    signal languageSelected(identifier: string)

    title: qsTranslate("MainWindow", "Language")
    icon.source: "qrc:/data/icons/language_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"

    // Applying the language retranslates and reshuffles the menu's geometry;
    // deferring until onClosed hides that churn from the user.
    property string _pendingLanguage: ""

    onClosed: {
        if (_pendingLanguage) {
            root.languageSelected(_pendingLanguage);
            _pendingLanguage = "";
        }
    }

    Repeater {
        model: MpvqcLanguageModel {}

        MenuItem {
            objectName: `languageMenuItem_${identifier}`

            required property string language
            required property string identifier

            text: qsTranslate("Languages", language)
            autoExclusive: true
            checkable: true
            checked: identifier === Qt.uiLanguage
            onTriggered: root._pendingLanguage = identifier
        }
    }
}
