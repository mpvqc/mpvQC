// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Utility

Item {
    id: root

    required property string filename
    required property string fullPath
    required property string reason

    readonly property int _iconSize: 20

    // The floor keeps the card's sweep still for anything but real content
    implicitHeight: Math.max(_row.implicitHeight + 2 * MpvqcConstants.listRowVerticalPadding, MpvqcConstants.listRowHeight)

    ToolTip.text: root.fullPath
    ToolTip.visible: _hover.hovered
    ToolTip.delay: MpvqcConstants.tooltipDelay

    RowLayout {
        id: _row

        anchors.left: parent.left
        anchors.leftMargin: MpvqcConstants.listRowHorizontalPadding
        anchors.right: parent.right
        anchors.rightMargin: MpvqcConstants.listRowHorizontalPadding
        anchors.verticalCenter: parent.verticalCenter
        spacing: MpvqcConstants.listRowContentSpacing

        MpvqcIconLabel {
            iconColor: MpvqcAppearance.palette.error
            icon.source: MpvqcIcons.error
            icon.width: root._iconSize
            icon.height: root._iconSize

            Layout.preferredWidth: root._iconSize
            Layout.preferredHeight: root._iconSize
            // Not centered: the icon belongs on the first line of the filename, and a wrapping
            // name would drag a centered icon down
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

    HoverHandler {
        id: _hover
    }
}
