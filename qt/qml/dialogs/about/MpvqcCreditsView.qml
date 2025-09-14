// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick

import "../../models"
import "../../shared"

Column {
    id: root

    MpvqcHeader {
        text: qsTranslate("AboutDialog", "Made by")
        width: root.width
        horizontalAlignment: Text.AlignHCenter
    }

    Repeater {
        model: MpvqcCreditsModel {}
        width: parent.width

        MpvqcMention {
            required property string name
            required property string contribution

            leftContent: name
            rightContent: contribution
            width: parent.width
        }
    }

    Item {
        height: 10
        width: root.width
    }

    Repeater {
        model: MpvqcLanguageModel {}
        width: parent.width

        MpvqcMention {
            required property string translator
            required property string language

            leftContent: translator
            rightContent: language
            width: parent.width
        }
    }
}
