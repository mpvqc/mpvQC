// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Utility

ColumnLayout {
    id: root

    required property var viewModel

    spacing: 20

    MpvqcWizardStepHeader {
        objectName: "errorsHeader"
        //: Header above the list of QC documents the importer rejected
        text: qsTranslate("ImportWizardDialog", "%Ln QC document(s) could not be imported:", "", _listView.count)
    }

    ListView {
        id: _listView
        objectName: "errorList"

        model: root.viewModel.documents
        implicitHeight: contentHeight
        interactive: false
        spacing: 0

        delegate: ItemDelegate {
            id: _delegate

            required property string filename
            required property string fullPath
            required property string reason

            readonly property int iconSize: 24

            width: ListView.view.width
            height: Math.max(implicitHeight, MpvqcConstants.listRowHeight)
            verticalPadding: 12
            leftPadding: 16
            rightPadding: 16

            contentItem: RowLayout {
                spacing: 12

                MpvqcIconLabel {
                    iconColor: MpvqcAppearance.palette.error
                    icon.source: MpvqcIcons.error
                    icon.width: _delegate.iconSize
                    icon.height: _delegate.iconSize

                    Layout.preferredWidth: _delegate.iconSize
                    Layout.preferredHeight: _delegate.iconSize
                }

                ColumnLayout {
                    spacing: 2

                    Layout.fillWidth: true

                    Label {
                        objectName: "filenameLabel"

                        text: _delegate.filename
                        horizontalAlignment: Text.AlignLeft
                        elide: Text.ElideRight

                        Layout.fillWidth: true
                    }

                    Label {
                        objectName: "reasonLabel"

                        text: _delegate.reason
                        color: MpvqcAppearance.palette.hint
                        horizontalAlignment: Text.AlignLeft
                        elide: Text.ElideRight

                        Layout.fillWidth: true
                    }
                }
            }

            ToolTip.text: _delegate.fullPath
            ToolTip.visible: hovered
            ToolTip.delay: MpvqcConstants.tooltipDelay
        }

        Layout.fillWidth: true
    }
}
