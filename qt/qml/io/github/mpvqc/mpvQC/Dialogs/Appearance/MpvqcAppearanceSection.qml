// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Utility

Item {
    id: root

    property alias title: _title.text
    default property alias content: _content.data

    property bool expanded: true

    readonly property int _animationDuration: 220
    readonly property int _padding: 16

    // A section reaches its size while the dialog builds, and that is not motion
    // anybody asked for: only folding and unfolding animates
    property bool _folding: false

    implicitHeight: root.expanded ? _content.implicitHeight + 2 * root._padding : 0
    clip: true
    opacity: root.expanded ? 1 : 0
    visible: root.expanded || root.implicitHeight > 0

    onExpandedChanged: root._folding = true

    Rectangle {
        objectName: "sectionCard"

        anchors.fill: parent
        radius: 20
        color: MpvqcAppearance.palette.sectionCard
    }

    ColumnLayout {
        id: _content

        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.margins: root._padding

        Label {
            id: _title
            objectName: "sectionTitle"

            font.weight: Font.DemiBold
            bottomPadding: 6

            Layout.alignment: Qt.AlignLeft
        }
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
