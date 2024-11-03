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

    readonly property alias importPolicyComboBox: _importPolicyComboBox

    property int currentImportPolicy: root.mpvqcSettings.importWhenVideoLinkedInDocument

    function accept() {
        root.mpvqcSettings.importWhenVideoLinkedInDocument = currentImportPolicy
    }

    RowLayout {
        Layout.topMargin: 20
        spacing: 30

        Label {
            text: qsTranslate("ImportSettingsDialog", "Open video if found")
            horizontalAlignment: Text.AlignRight
            wrapMode: Text.Wrap
            Layout.preferredWidth: 165
        }

        ComboBox {
            id: _importPolicyComboBox

            Layout.preferredWidth: 165

            textRole: 'text'
            valueRole: 'value'

            model: [
                {
                    text: qsTranslate("ImportSettingsDialog", "Always"),
                    value: MpvqcSettings.ImportWhenVideoLinkedInDocument.ALWAYS,
                },
                {
                    text: qsTranslate("ImportSettingsDialog", "Ask every time"),
                    value: MpvqcSettings.ImportWhenVideoLinkedInDocument.ASK_EVERY_TIME,
                },
                {
                    text: qsTranslate("ImportSettingsDialog", "Never"),
                    value: MpvqcSettings.ImportWhenVideoLinkedInDocument.NEVER,
                }
            ]

            onActivated: value => {
                root.currentImportPolicy = value
            }

            Component.onCompleted: {
                currentIndex = indexOfValue(root.currentImportPolicy)
            }
        }

    }

}
