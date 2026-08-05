// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Python
import io.github.mpvqc.mpvQC.Utility

MpvqcDialog {
    id: root
    objectName: "importSettingsDialog"

    readonly property MpvqcImportSettingsDialogViewModel viewModel: MpvqcImportSettingsDialogViewModel {}

    contentHeight: MpvqcConstants.smallDialogContentHeight

    title: qsTranslate("ImportSettingsDialog", "Import Settings")
    standardButtons: Dialog.Ok | Dialog.Cancel

    contentItem: ColumnLayout {
        spacing: 10

        RowLayout {
            spacing: 30

            Layout.topMargin: 20

            Label {
                text: qsTranslate("ImportSettingsDialog", "Open video if found")
                horizontalAlignment: Text.AlignRight
                wrapMode: Text.Wrap

                Layout.preferredWidth: 165
            }

            ComboBox {
                objectName: "importFoundVideoComboBox"

                textRole: "text"
                valueRole: "value"

                model: MpvqcImportSettingsModel {}

                Layout.preferredWidth: 165

                onActivated: value => {
                    root.viewModel.importFoundVideo = value;
                }

                Component.onCompleted: {
                    currentIndex = indexOfValue(root.viewModel.importFoundVideo);
                }
            }
        }

        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true
        }
    }

    onAccepted: root.viewModel.accept()
}
