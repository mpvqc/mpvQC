// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Components

ColumnLayout {
    id: root

    required property var viewModel

    spacing: 20

    MpvqcWizardStepHeader {
        //: Subtitles step prompt above the subtitles list, in the singular when a single subtitle is offered
        text: qsTranslate("ImportWizardDialog", "Which subtitle(s) should be loaded?", "", _listView.count)

        AbstractButton {
            id: _selectAll
            objectName: "selectAll"

            anchors.verticalCenter: parent.verticalCenter

            visible: _listView.count > 1
            //: Tri-state "Select all" checkbox in the subtitles step header
            text: qsTranslate("ImportWizardDialog", "Select all")
            hoverEnabled: true
            verticalPadding: 6
            horizontalPadding: 10

            background: MpvqcWizardPillBackground {
                hovered: _selectAll.hovered
            }

            contentItem: RowLayout {
                spacing: 8

                MpvqcCheckIndicator {
                    objectName: "selectAllIndicator"

                    checked: root.viewModel.selectAllTriState === Qt.Checked
                    partial: root.viewModel.selectAllTriState === Qt.PartiallyChecked

                    Layout.alignment: Qt.AlignVCenter
                }

                Label {
                    text: _selectAll.text
                    horizontalAlignment: Text.AlignLeft

                    Layout.alignment: Qt.AlignVCenter
                }
            }

            onClicked: root.viewModel.toggleSelectAll()

            HoverHandler {
                cursorShape: Qt.PointingHandCursor
            }
        }
    }

    ListView {
        id: _listView
        objectName: "subtitleList"

        model: root.viewModel.subtitles
        implicitHeight: contentHeight
        interactive: false
        spacing: 8

        delegate: MpvqcWizardSubtitlesStepDelegate {
            id: _delegate

            width: _listView.width

            onClicked: root.viewModel.toggle(_delegate.index)
        }

        Layout.fillWidth: true
    }
}
