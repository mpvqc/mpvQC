// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Utility

Control {
    id: root

    required property string filename
    required property string fullPath
    required property string reason

    readonly property int _iconSize: 20

    implicitHeight: Math.max(root.implicitContentHeight + root.topPadding + root.bottomPadding, MpvqcConstants.listRowHeight)
    verticalPadding: MpvqcConstants.listRowVerticalPadding
    horizontalPadding: MpvqcConstants.listRowHorizontalPadding
    hoverEnabled: true

    contentItem: RowLayout {
        spacing: MpvqcConstants.listRowContentSpacing

        MpvqcIconLabel {
            objectName: "errorIcon"

            iconColor: MpvqcAppearance.palette.error
            icon.source: MpvqcIcons.error
            icon.width: root._iconSize
            icon.height: root._iconSize

            Layout.preferredWidth: root._iconSize
            Layout.preferredHeight: root._iconSize
            Layout.alignment: Qt.AlignTop
            Layout.topMargin: 2
        }

        ColumnLayout {
            spacing: 2

            Layout.fillWidth: true

            Label {
                objectName: "filenameLabel"

                text: root.filename
                horizontalAlignment: Text.AlignLeft
                wrapMode: Text.WrapAtWordBoundaryOrAnywhere

                Layout.fillWidth: true
            }

            Label {
                objectName: "reasonLabel"

                text: root.reason
                color: MpvqcAppearance.palette.hint
                horizontalAlignment: Text.AlignLeft
                wrapMode: Text.Wrap

                Layout.fillWidth: true
            }
        }
    }

    ToolTip.text: root.fullPath
    ToolTip.visible: root.hovered
    ToolTip.delay: MpvqcConstants.tooltipDelay
}
