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

ColumnLayout {
    id: root

    required property var viewModel

    spacing: 20

    MpvqcWizardStepHeader {
        //: Session step header: states the incoming comment count and asks how to proceed (%Ln is the count)
        text: qsTranslate("ImportWizardDialog", "You're about to import <b>%Ln</b> comment(s) into your current session. What do you want to do?", "", root.viewModel.incomingCommentCount)
    }

    ListView {
        id: _listView
        objectName: "sessionOptions"

        model: [
            {
                mode: MpvqcImportWizardSessionMode.SessionMode.MERGE,
                //: Merge option label — keeps the existing comments and appends the incoming ones
                text: qsTranslate("ImportWizardDialog", "Add to your current comments"),
                objectName: "mergeRow"
            },
            {
                mode: MpvqcImportWizardSessionMode.SessionMode.REPLACE,
                //: Replace option label — discards the existing comments before importing the incoming ones
                text: qsTranslate("ImportWizardDialog", "Start fresh with the new comments"),
                objectName: "replaceRow"
            },
        ]

        implicitHeight: contentHeight
        interactive: false
        spacing: 8

        delegate: ItemDelegate {
            id: _delegate
            objectName: _delegate.modelData.objectName

            required property var modelData

            readonly property bool selected: root.viewModel.mode === _delegate.modelData.mode

            // Picking a row animates the fill; building the step must not
            property bool _animated: false

            width: ListView.view.width
            implicitHeight: Math.max(_delegate.implicitContentHeight + _delegate.topPadding + _delegate.bottomPadding, MpvqcConstants.listRowHeight)
            verticalPadding: MpvqcConstants.listRowVerticalPadding
            horizontalPadding: MpvqcConstants.listRowHorizontalPadding
            hoverEnabled: true

            background: Rectangle {
                // Capped at the shared row height, so a wrapping row keeps its neighbours' corner
                radius: Math.min(height, MpvqcConstants.listRowHeight) / 2
                color: _delegate.selected ? Qt.alpha(MpvqcAppearance.palette.accent, 0.16) : _delegate.hovered ? Qt.alpha(MpvqcAppearance.palette.foreground, MpvqcAppearance.isDark ? 0.08 : 0.12) : "transparent"

                Behavior on color {
                    enabled: _delegate._animated

                    ColorAnimation {
                        duration: 120
                    }
                }
            }

            contentItem: RowLayout {
                spacing: MpvqcConstants.listRowContentSpacing

                MpvqcRadioIndicator {
                    objectName: "radio"

                    selected: _delegate.selected

                    Layout.alignment: Qt.AlignVCenter
                }

                Label {
                    objectName: "label"

                    text: _delegate.modelData.text
                    horizontalAlignment: Text.AlignLeft
                    wrapMode: Text.Wrap
                    maximumLineCount: 2
                    elide: Text.ElideRight

                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignVCenter
                }
            }

            onClicked: root.viewModel.mode = _delegate.modelData.mode

            Component.onCompleted: _delegate._animated = true
        }

        Layout.fillWidth: true
    }
}
