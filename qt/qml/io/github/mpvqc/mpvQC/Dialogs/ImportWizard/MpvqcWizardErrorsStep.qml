// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Utility

ColumnLayout {
    id: root

    required property var viewModel

    readonly property bool isMirrored: Application.layoutDirection === Qt.RightToLeft

    spacing: 20

    MpvqcWizardStepHeader {
        objectName: "errorsHeader"
        //: Header above the list of QC documents whose format the importer rejected
        text: qsTranslate("ImportWizardDialog", "%Ln incompatible QC document(s):", "", _listView.count)
    }

    ListView {
        id: _listView
        objectName: "errorList"

        Layout.fillWidth: true
        Layout.fillHeight: true

        model: root.viewModel.documents
        clip: true
        boundsBehavior: Flickable.StopAtBounds
        interactive: contentHeight > height
        spacing: 0

        delegate: ItemDelegate {
            id: _delegate

            required property string filename
            required property string fullPath

            width: ListView.view.width
            verticalPadding: 16
            leftInset: root.isMirrored ? _scrollBar.visibleWidth : 0
            rightInset: root.isMirrored ? 0 : _scrollBar.visibleWidth
            leftPadding: leftInset + 16
            rightPadding: rightInset + 16
            text: _delegate.filename

            icon {
                source: MpvqcIcons.error
                width: 24
                height: 24
            }

            ToolTip.text: _delegate.fullPath
            ToolTip.visible: hovered
            ToolTip.delay: MpvqcConstants.tooltipDelay
        }

        ScrollBar.vertical: ScrollBar {
            id: _scrollBar

            readonly property bool isShown: _listView.contentHeight > _listView.height
            readonly property real visibleWidth: isShown ? width : 0

            policy: isShown ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff
        }
    }
}
