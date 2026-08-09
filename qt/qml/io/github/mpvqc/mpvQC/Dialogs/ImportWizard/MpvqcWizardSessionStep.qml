// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Python

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

        delegate: MpvqcWizardChoiceRow {
            id: _delegate
            objectName: _delegate.modelData.objectName

            required property var modelData

            width: ListView.view.width
            selected: root.viewModel.mode === _delegate.modelData.mode

            onClicked: root.viewModel.mode = _delegate.modelData.mode

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

        Layout.fillWidth: true
    }
}
