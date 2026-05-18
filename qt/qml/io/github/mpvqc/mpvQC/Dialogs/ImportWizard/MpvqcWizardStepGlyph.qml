// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Utility

Item {
    id: root

    required property bool completed
    required property bool current
    property int size: 20
    property int animationDuration: 150

    implicitWidth: root.size
    implicitHeight: root.size

    component StateIcon: MpvqcIconLabel {
        required property bool active

        anchors.fill: parent

        opacity: active ? 1 : 0
        icon.width: root.size
        icon.height: root.size
        icon.color: MpvqcTheme.palette.foreground

        Behavior on opacity {
            NumberAnimation {
                duration: root.animationDuration
            }
        }
    }

    StateIcon {
        objectName: "upcomingStateIcon"
        active: !root.completed && !root.current
        icon.source: MpvqcIcons.circle
    }

    StateIcon {
        objectName: "currentStateIcon"
        active: root.current
        icon.source: MpvqcIcons.circleFilled
    }

    StateIcon {
        objectName: "completedStateIcon"
        active: root.completed
        icon.source: MpvqcIcons.check
    }
}
