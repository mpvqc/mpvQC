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
    property alias titleActions: _titleActions.data
    default property alias content: _content.data

    readonly property int _padding: 20

    implicitHeight: _content.implicitHeight + 2 * root._padding

    Rectangle {
        objectName: "cardBackground"

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

        RowLayout {
            Layout.fillWidth: true
            Layout.bottomMargin: 6

            Label {
                id: _title
                objectName: "cardTitle"

                font.weight: Font.DemiBold
                horizontalAlignment: Text.AlignLeft

                Layout.fillWidth: true
            }

            RowLayout {
                id: _titleActions

                visible: _titleActions.children.length > 0
            }
        }
    }
}
