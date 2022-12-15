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
import QtQuick.Layouts
import models
import shared


ScrollView {
    id: _root

    width: parent.width
    contentWidth: parent.width

    Column {
        width: parent.width

        MpvqcHeader {
            text: qsTranslate("AboutDialog", "Development")
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Repeater {
            model: MpvqcDeveloperModel {}
            width: parent.width

            Label {
                text: name
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }

        MpvqcHeader {
            text: qsTranslate("AboutDialog", "Artwork")
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Repeater {
            model: MpvqcArtworkModel {}
            width: parent.width

            Label {
                anchors.horizontalCenter: parent.horizontalCenter
                text: name
            }
        }

        MpvqcHeader {
            text: qsTranslate("AboutDialog", "Translation")
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Repeater {
            model: MpvqcLanguageModel {}
            width: parent.width

            RowLayout {
                visible: translator
                spacing: 10

                Label {
                    text: translator
                    horizontalAlignment: Text.AlignRight
                    Layout.preferredWidth: _root.width / 2
                }

                Label {
                    text: qsTranslate("Languages", language)
                    font.italic: true
                    horizontalAlignment: Text.AlignLeft
                    Layout.preferredWidth: _root.width / 2
                }
            }
        }

    }

}
