// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ColumnLayout {
    id: root

    required property var viewModel

    readonly property bool isMirrored: Application.layoutDirection === Qt.RightToLeft

    spacing: 20

    MpvqcWizardStepHeader {
        //: Video step prompt above the candidate list
        text: qsTranslate("ImportWizardDialog", "Which video should be loaded?")
    }

    ListView {
        id: _listView
        objectName: "videoList"

        Layout.fillWidth: true
        Layout.fillHeight: true

        model: root.viewModel.candidates
        clip: true
        boundsBehavior: Flickable.StopAtBounds
        interactive: contentHeight > height
        spacing: 0

        delegate: MpvqcWizardVideoStepDelegate {
            width: _listView.width
            leftInset: root.isMirrored ? _scrollBar.visibleWidth : 0
            rightInset: root.isMirrored ? 0 : _scrollBar.visibleWidth
            leftPadding: leftInset + 16
            rightPadding: rightInset + 16
            selected: root.viewModel.selectedIndex === index

            onClicked: root.viewModel.selectedIndex = index
        }

        ScrollBar.vertical: ScrollBar {
            id: _scrollBar

            readonly property bool isShown: _listView.contentHeight > _listView.height
            readonly property real visibleWidth: isShown ? width : 0

            policy: isShown ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff
        }
    }
}
