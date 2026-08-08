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
                objectName: "mergeRadio"
            },
            {
                mode: MpvqcImportWizardSessionMode.SessionMode.REPLACE,
                //: Replace option label — discards the existing comments before importing the incoming ones
                text: qsTranslate("ImportWizardDialog", "Start fresh with the new comments"),
                objectName: "replaceRadio"
            },
        ]

        implicitHeight: contentHeight
        interactive: false
        spacing: 0

        delegate: ItemDelegate {
            id: _delegate
            objectName: _delegate.modelData.objectName

            required property int index
            required property var modelData

            readonly property bool selected: root.viewModel.mode === _delegate.modelData.mode
            readonly property int iconSize: 24

            width: ListView.view.width
            verticalPadding: 16

            contentItem: RowLayout {
                spacing: 12

                MpvqcAnimatedIcon {
                    active: _delegate.selected
                    activeIcon: MpvqcIcons.radioButtonChecked
                    inactiveIcon: MpvqcIcons.radioButtonUnchecked
                    iconSize: _delegate.iconSize
                    activationDuration: 150
                    deactivationDuration: 75
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
        }

        Layout.fillWidth: true
    }
}
