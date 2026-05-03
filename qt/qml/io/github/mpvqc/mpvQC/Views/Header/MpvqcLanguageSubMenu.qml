// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material

import io.github.mpvqc.mpvQC.Python
import io.github.mpvqc.mpvQC.Utility

MpvqcMenuBarMenu {
    id: root
    objectName: "languageMenu"

    signal languageSelected(identifier: string)

    title: qsTranslate("MainWindow", "Language")
    icon.source: MpvqcIcons.language

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
