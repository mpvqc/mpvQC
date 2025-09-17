// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material
import QtQuick.Layouts

import pyobjects

ColumnLayout {
    id: root

    required property var mpvqcApplication

    property var mpvqcSettings: mpvqcApplication.mpvqcSettings

    readonly property alias importPolicyComboBox: _importPolicyComboBox

    property int currentImportPolicy: root.mpvqcSettings.importWhenVideoLinkedInDocument

    function accept(): void {
        root.mpvqcSettings.importWhenVideoLinkedInDocument = currentImportPolicy;
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

            textRole: "text"
            valueRole: "value"

            model: [
                {
                    text: qsTranslate("ImportSettingsDialog", "Always"),
                    value: MpvqcSettings.ImportWhenVideoLinkedInDocument.ALWAYS
                },
                {
                    text: qsTranslate("ImportSettingsDialog", "Ask every time"),
                    value: MpvqcSettings.ImportWhenVideoLinkedInDocument.ASK_EVERY_TIME
                },
                {
                    text: qsTranslate("ImportSettingsDialog", "Never"),
                    value: MpvqcSettings.ImportWhenVideoLinkedInDocument.NEVER
                }
            ]

            onActivated: value => {
                root.currentImportPolicy = value;
            }

            Component.onCompleted: {
                currentIndex = indexOfValue(root.currentImportPolicy);
            }
        }
    }

    Item {
        Layout.fillWidth: true
        Layout.fillHeight: true
    }
}
