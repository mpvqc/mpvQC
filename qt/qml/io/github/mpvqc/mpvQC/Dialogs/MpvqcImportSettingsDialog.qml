// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

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

    component ChoiceButton: MpvqcPillButton {
        id: choice
        objectName: `loadFoundVideoChoice_${value}`

        required property int value
        checked: root.viewModel.loadFoundVideo === choice.value

        Layout.fillWidth: true
        Layout.fillHeight: true
        Layout.minimumWidth: 0
        Layout.preferredWidth: 1

        onClicked: root.viewModel.loadFoundVideo = choice.value
    }

    width: Math.min(contentWidth + leftPadding + rightPadding, Math.max(0, (Overlay.overlay?.width ?? 0) - 2 * margins))
    contentWidth: MpvqcConstants.smallDialogContentWidth
    contentHeight: MpvqcConstants.smallDialogContentHeight
    margins: MpvqcConstants.dialogEdgeMargin
    title: qsTranslate("ImportSettingsDialog", "Import Settings")
    standardButtons: Dialog.Ok | Dialog.Cancel

    contentItem: Item {
        MpvqcSectionCard {
            y: MpvqcConstants.dialogContentTopMargin
            width: parent.width
            title: qsTranslate("ImportSettingsDialog", "Open video if found")

            RowLayout {
                spacing: 4

                Layout.fillWidth: true

                ChoiceButton {
                    value: root.viewModel.options[0].value
                    text: root.viewModel.options[0].text
                }

                ChoiceButton {
                    value: root.viewModel.options[1].value
                    text: root.viewModel.options[1].text
                }

                ChoiceButton {
                    value: root.viewModel.options[2].value
                    text: root.viewModel.options[2].text
                }
            }
        }
    }

    onAccepted: root.viewModel.accept()
}
