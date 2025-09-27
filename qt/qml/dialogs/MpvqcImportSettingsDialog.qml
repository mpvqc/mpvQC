// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material
import QtQuick.Layouts

import pyobjects

import "../shared"

MpvqcDialog {
    id: root

    readonly property MpvqcImportSettingsDialogControllerPyObject controller: MpvqcImportSettingsDialogControllerPyObject {}

    title: qsTranslate("ImportSettingsDialog", "Import Settings")

    contentItem: ColumnLayout {
        spacing: 10

        RowLayout {
            Layout.topMargin: 20
            spacing: 30

            Label {
                Layout.preferredWidth: 165

                text: qsTranslate("ImportSettingsDialog", "Open video if found")
                horizontalAlignment: Text.AlignRight
                wrapMode: Text.Wrap
            }

            ComboBox {
                Layout.preferredWidth: 165

                textRole: "text"
                valueRole: "value"

                model: ImportOptionsModel {}

                onActivated: value => {
                    root.controller.importWhenVideoLinkedInDocument = value;
                }

                Component.onCompleted: {
                    currentIndex = indexOfValue(root.controller.importWhenVideoLinkedInDocument);
                }
            }
        }

        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true
        }
    }

    onAccepted: root.controller.accept()
}
