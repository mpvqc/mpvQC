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
