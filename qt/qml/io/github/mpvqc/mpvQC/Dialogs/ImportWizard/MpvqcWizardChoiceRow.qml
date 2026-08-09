// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Utility

ItemDelegate {
    id: root

    default property alias rowContent: _content.data

    property bool selected: false

    property string toolTipText
    property bool toolTipSuppressed: false

    property int minimumHeight: MpvqcConstants.listRowHeight

    property bool _animated: false

    implicitHeight: Math.max(root.implicitContentHeight + root.topPadding + root.bottomPadding, root.minimumHeight)
    verticalPadding: MpvqcConstants.listRowVerticalPadding
    horizontalPadding: MpvqcConstants.listRowHorizontalPadding
    hoverEnabled: true

    background: Rectangle {
        radius: Math.min(height, MpvqcConstants.listRowHeight) / 2
        color: {
            if (root.selected) {
                return Qt.alpha(MpvqcAppearance.palette.accent, 0.16);
            }
            return root.hovered ? Qt.alpha(MpvqcAppearance.palette.foreground, MpvqcAppearance.isDark ? 0.08 : 0.12) : "transparent";
        }

        Behavior on color {
            enabled: root._animated

            ColorAnimation {
                duration: 120
            }
        }
    }

    contentItem: RowLayout {
        id: _content

        spacing: MpvqcConstants.listRowContentSpacing
    }

    ToolTip.text: root.toolTipText
    ToolTip.visible: root.toolTipText !== "" && root.hovered && !root.toolTipSuppressed
    ToolTip.delay: MpvqcConstants.tooltipDelay

    Component.onCompleted: root._animated = true

    HoverHandler {
        cursorShape: Qt.PointingHandCursor
    }
}
