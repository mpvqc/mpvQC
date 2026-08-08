// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick

import io.github.mpvqc.mpvQC.Components

Item {
    id: root

    property alias title: _card.title
    default property alias content: _card.content

    property bool expanded: true

    readonly property int _animationDuration: 220

    // A section reaches its size while the dialog builds, and that is not motion
    // anybody asked for: only folding and unfolding animates
    property bool _folding: false

    implicitHeight: root.expanded ? _card.implicitHeight : 0
    clip: true
    opacity: root.expanded ? 1 : 0
    visible: root.expanded || root.implicitHeight > 0

    onExpandedChanged: root._folding = true

    MpvqcSectionCard {
        id: _card

        anchors.fill: parent
    }

    Behavior on implicitHeight {
        enabled: root._folding

        NumberAnimation {
            duration: root._animationDuration
            easing.type: Easing.OutCubic
        }
    }

    Behavior on opacity {
        enabled: root._folding

        NumberAnimation {
            duration: root._animationDuration
        }
    }
}
