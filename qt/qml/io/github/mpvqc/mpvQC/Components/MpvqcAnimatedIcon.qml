// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick

import io.github.mpvqc.mpvQC.Utility

Item {
    id: root

    property bool active: false
    property url activeIcon
    property url inactiveIcon
    property int iconSize: 24
    property int activationDuration: 100
    property int deactivationDuration: 50
    property color iconColor: MpvqcTheme.palette.accent

    implicitWidth: iconSize
    implicitHeight: iconSize

    MpvqcIconLabel {
        anchors.fill: parent
        icon.source: root.inactiveIcon
        icon {
            width: root.iconSize
            height: root.iconSize
        }
        iconColor: root.iconColor
        opacity: root.active ? 0 : 1

        Behavior on opacity {
            NumberAnimation {
                duration: root.active ? root.activationDuration : root.deactivationDuration
            }
        }
    }

    MpvqcIconLabel {
        anchors.fill: parent
        icon.source: root.activeIcon
        icon {
            width: root.iconSize
            height: root.iconSize
        }
        iconColor: root.iconColor
        opacity: root.active ? 1 : 0

        Behavior on opacity {
            NumberAnimation {
                duration: root.active ? root.activationDuration : root.deactivationDuration
            }
        }
    }
}
