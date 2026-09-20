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
    objectName: "backupDialog"

    readonly property MpvqcExportBackupDialogViewModel viewModel: MpvqcExportBackupDialogViewModel {}

    contentHeight: MpvqcConstants.smallDialogContentHeight

    title: qsTranslate("BackupDialog", "Backup Settings")
    standardButtons: Dialog.Ok | Dialog.Cancel

    contentItem: ScrollView {
        id: _scroll

        clip: true
        contentWidth: availableWidth
        contentHeight: _sections.implicitHeight

        ScrollBar.horizontal.policy: ScrollBar.AlwaysOff

        ColumnLayout {
            id: _sections

            width: _scroll.availableWidth
            spacing: 0

            MpvqcSectionCard {
                objectName: "backupEnabledCard"

                title: qsTranslate("BackupDialog", "Backup Enabled")
                titleActions: Item {
                    // Keep the full hit area without letting the control set the title row's height.
                    implicitWidth: _enabledSwitch.implicitWidth

                    Switch {
                        id: _enabledSwitch
                        objectName: "backupEnabledSwitch"

                        anchors.centerIn: parent
                        checked: root.viewModel.temporaryBackupEnabled

                        Accessible.name: qsTranslate("BackupDialog", "Backup Enabled")

                        onToggled: root.viewModel.temporaryBackupEnabled = checked
                    }
                }

                Layout.fillWidth: true
                Layout.topMargin: MpvqcConstants.dialogContentTopMargin
                Layout.bottomMargin: MpvqcConstants.dialogSectionSpacing
            }

            Item {
                id: _intervalFold

                implicitHeight: root.viewModel.temporaryBackupEnabled ? _intervalCard.implicitHeight + MpvqcConstants.dialogSectionSpacing : 0
                clip: true
                enabled: root.viewModel.temporaryBackupEnabled
                opacity: root.viewModel.temporaryBackupEnabled ? 1 : 0

                Layout.fillWidth: true
                Layout.preferredHeight: implicitHeight

                MpvqcSectionCard {
                    id: _intervalCard
                    objectName: "backupIntervalCard"

                    width: parent.width
                    height: implicitHeight
                    visible: _intervalFold.height > 0
                    title: qsTranslate("BackupDialog", "Backup Interval")
                    spacing: 0

                    GridLayout {
                        columns: 3
                        columnSpacing: 4
                        rowSpacing: 0
                        uniformCellWidths: true

                        Layout.fillWidth: true

                        Repeater {
                            model: [30, 60, 90, 120, 180, 300]

                            delegate: MpvqcPillButton {
                                id: _preset
                                objectName: `backupIntervalPreset_${modelData}`

                                required property int modelData

                                text: Number(modelData < 120 ? modelData : modelData / 60).toLocaleString(Qt.locale(), 'f', 0) + " " + (modelData < 120 ? qsTranslate("BackupDialog", "Seconds") : qsTranslate("BackupDialog", "Minutes"))
                                checked: root.viewModel.temporaryBackupInterval === modelData

                                Layout.fillWidth: true
                                Layout.fillHeight: true
                                Layout.minimumWidth: 0
                                Layout.preferredWidth: 1

                                onClicked: root.viewModel.temporaryBackupInterval = modelData
                            }
                        }
                    }
                }

                Behavior on implicitHeight {
                    enabled: root.opened

                    NumberAnimation {
                        duration: 220
                        easing.type: Easing.OutCubic
                    }
                }

                Behavior on opacity {
                    enabled: root.opened

                    NumberAnimation {
                        duration: 220
                    }
                }
            }

            MpvqcSectionCard {
                objectName: "backupLocationCard"

                title: qsTranslate("BackupDialog", "Backup Location")
                spacing: 0

                Layout.fillWidth: true

                RowLayout {
                    spacing: 12

                    Layout.fillWidth: true

                    Label {
                        objectName: "backupDirectoryLabel"

                        textFormat: Text.PlainText
                        color: MpvqcAppearance.palette.hint
                        wrapMode: Text.Wrap

                        Layout.fillWidth: true
                        Layout.minimumWidth: 0
                        Layout.preferredWidth: 1

                        Component.onCompleted: text = root.viewModel.backupDirectory
                    }

                    ToolButton {
                        objectName: "backupOpenLocationButton"

                        text: qsTranslate("BackupDialog", "Backup Location")
                        display: AbstractButton.IconOnly
                        icon.source: MpvqcIcons.folderOpen

                        Layout.alignment: Qt.AlignVCenter

                        ToolTip.delay: MpvqcConstants.tooltipDelay
                        ToolTip.text: root.viewModel.backupDirectory
                        ToolTip.visible: hovered

                        onClicked: root.viewModel.openBackupDirectory()
                    }
                }
            }
        }
    }

    onAccepted: root.viewModel.accept()
}
