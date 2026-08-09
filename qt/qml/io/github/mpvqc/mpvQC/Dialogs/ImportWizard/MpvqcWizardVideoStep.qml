// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Layouts

ColumnLayout {
    id: root

    required property var viewModel

    spacing: 20

    MpvqcWizardStepHeader {
        //: Video step prompt above the candidate list
        text: qsTranslate("ImportWizardDialog", "Which video should be loaded?")
    }

    ListView {
        id: _listView
        objectName: "videoList"

        model: root.viewModel.candidates
        implicitHeight: contentHeight
        interactive: false
        spacing: 0

        delegate: MpvqcWizardVideoStepDelegate {
            width: _listView.width
            leftPadding: 16
            rightPadding: 16
            selected: root.viewModel.selectedIndex === index

            onClicked: root.viewModel.selectedIndex = index
        }

        Layout.fillWidth: true
    }
}
