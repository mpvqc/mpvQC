// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material
import QtQuick.Layouts

Item {
    id: root

    property alias text: _question.text
    default property alias rightContent: _rightArea.data

    readonly property int minimumHeight: 40

    Layout.fillWidth: true
    Layout.preferredHeight: Math.max(root.minimumHeight, _question.implicitHeight)

    Label {
        id: _question
        objectName: "question"

        anchors.left: parent.left
        anchors.right: _rightArea.left
        anchors.rightMargin: _rightArea.childrenRect.width > 0 ? 12 : 0
        anchors.top: parent.top
        anchors.bottom: parent.bottom

        horizontalAlignment: Text.AlignLeft
        verticalAlignment: Text.AlignVCenter
        wrapMode: Text.Wrap
        textFormat: Text.StyledText
    }

    Item {
        id: _rightArea

        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        width: childrenRect.width
    }
}
