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
import QtQuick.Layouts

import models
import shared

ScrollView {
    id: _root

    width: parent.width
    contentWidth: parent.width

    Column {
        id: _container
        
        width: parent.width

        MpvqcHeader {
            //: Header for the section about people that contributed source code to the project
            text: qsTranslate("AboutDialog", "Development")
            width: _container.width
        }

        Repeater {
            model: MpvqcDeveloperModel {}
            width: parent.width

            Label {
                required property string name

                text: name
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }

        MpvqcHeader {
            //: Header for the section about people that contributed images, icons or other artwork to the project
            text: qsTranslate("AboutDialog", "Artwork")
            width: _container.width
        }

        Repeater {
            model: MpvqcArtworkModel {}
            width: parent.width

            Label {
                required property string name

                anchors.horizontalCenter: parent.horizontalCenter
                text: name
            }
        }

        MpvqcHeader {
            //: Header for the section about people that contributed images, icons or other artwork to the project
            text: qsTranslate("AboutDialog", "Translation")
            width: _container.width
        }

        Repeater {
            model: MpvqcLanguageModel {}
            width: parent.width

            RowLayout {
                id: _delegate

                visible: translator
                spacing: 10

                required property string translator
                required property string language

                Label {
                    text: _delegate.translator
                    horizontalAlignment: Text.AlignRight
                    Layout.preferredWidth: _root.width / 2
                }

                Label {
                    text: qsTranslate("Languages", _delegate.language)
                    font.italic: true
                    horizontalAlignment: Text.AlignLeft
                    Layout.preferredWidth: _root.width / 2
                }
            }
        }
    }
}
