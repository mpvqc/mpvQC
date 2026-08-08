// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Utility

ItemDelegate {
    id: root

    required property int index
    required property string filename
    required property string fullPath
    required property bool isChecked

    // A row grows only when its filename wraps, so the sweep moves for real content alone
    implicitHeight: Math.max(root.implicitContentHeight + root.topPadding + root.bottomPadding, MpvqcConstants.listRowHeight)
    verticalPadding: MpvqcConstants.listRowVerticalPadding
    horizontalPadding: MpvqcConstants.listRowHorizontalPadding

    ToolTip.text: root.fullPath
    ToolTip.visible: root.hovered
    ToolTip.delay: MpvqcConstants.tooltipDelay

    // Checked rows keep the plain background: the indicator alone carries their state
    background: MpvqcWizardPillBackground {
        hovered: root.hovered
    }

    contentItem: RowLayout {
        spacing: MpvqcConstants.listRowContentSpacing

        MpvqcCheckIndicator {
            objectName: "checkIndicator"

            checked: root.isChecked

            Layout.alignment: Qt.AlignVCenter
        }

        Label {
            objectName: "label"

            text: root.filename
            horizontalAlignment: Text.AlignLeft
            wrapMode: Text.WrapAtWordBoundaryOrAnywhere

            Layout.fillWidth: true
            Layout.alignment: Qt.AlignVCenter
        }
    }
}
