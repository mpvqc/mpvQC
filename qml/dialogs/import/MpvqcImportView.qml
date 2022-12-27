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

import settings


ColumnLayout {
    id: root

    required property var mpvqcApplication

    property var mpvqcSettings: mpvqcApplication.mpvqcSettings

    property alias selectionAlways: _selectionAlways
    property alias selectionAsk: _selectionAsk
    property alias selectionNever: _selectionNever

    RowLayout {
        Layout.topMargin: 20
        spacing: 30

        Label {
            text: qsTranslate("ImportSettings", "Open video if found")
            horizontalAlignment: Text.AlignRight
            wrapMode: Text.Wrap
            Layout.preferredWidth: 165
        }

        ColumnLayout {
            Layout.preferredWidth: 165

            ButtonGroup { id: radioGroup }

            CheckBox {
                id: _selectionAlways

                property var selection: MpvqcSettings.ImportWhenVideoLinkedInDocument.ALWAYS

                text: qsTranslate("ImportSettings", "Always")
                checked: root.mpvqcSettings.importWhenVideoLinkedInDocument == selection
                ButtonGroup.group: radioGroup

                onPressed: {
                    root.mpvqcSettings.importWhenVideoLinkedInDocument = selection
                }
            }

            CheckBox {
                id: _selectionAsk

                property var selection: MpvqcSettings.ImportWhenVideoLinkedInDocument.ASK_EVERY_TIME

                text: qsTranslate("ImportSettings", "Ask every time")
                checked: root.mpvqcSettings.importWhenVideoLinkedInDocument == selection
                ButtonGroup.group: radioGroup

                onPressed: {
                    root.mpvqcSettings.importWhenVideoLinkedInDocument = selection
                }
            }

            CheckBox {
                id: _selectionNever

                property var selection: MpvqcSettings.ImportWhenVideoLinkedInDocument.NEVER

                text: qsTranslate("ImportSettings", "Never")
                checked: root.mpvqcSettings.importWhenVideoLinkedInDocument == selection
                ButtonGroup.group: radioGroup

                onPressed: {
                    root.mpvqcSettings.importWhenVideoLinkedInDocument = selection
                }
            }
        }
    }

}
