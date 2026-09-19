// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls

import io.github.mpvqc.mpvQC.Utility

ItemDelegate {
    id: root

    property int minimumHeight: MpvqcConstants.listRowHeight

    property bool _animated: false

    implicitHeight: Math.max(implicitContentHeight + topPadding + bottomPadding, minimumHeight)
    verticalPadding: MpvqcConstants.listRowVerticalPadding
    horizontalPadding: MpvqcConstants.listRowHorizontalPadding
    hoverEnabled: true

    background: Rectangle {
        radius: Math.min(height, MpvqcConstants.listRowHeight) / 2
        color: {
            if (!root.enabled) {
                return "transparent";
            }
            if (root.highlighted) {
                const opacity = root.down ? 0.24 : root.hovered || root.visualFocus ? 0.20 : 0.16;
                return Qt.alpha(MpvqcAppearance.palette.accent, opacity);
            }
            if (root.down) {
                return Qt.alpha(MpvqcAppearance.palette.foreground, 0.16);
            }
            return root.hovered || root.visualFocus ? Qt.alpha(MpvqcAppearance.palette.foreground, MpvqcAppearance.isDark ? 0.08 : 0.12) : "transparent";
        }

        Behavior on color {
            enabled: root._animated

            ColorAnimation {
                duration: 120
            }
        }
    }

    Component.onCompleted: root._animated = true
}
