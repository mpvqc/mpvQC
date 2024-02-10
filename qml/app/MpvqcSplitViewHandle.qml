// Copyright (C) 2018 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

// Adapted from qtdeclarative/qml/QtQuick/Controls/Material/SplitView.qml
// SplitHandles should be purely visual but we need to detect when the mouse hovers the handle

import QtQuick
import QtQuick.Templates as T
import QtQuick.Controls.impl
import QtQuick.Controls.Material


Rectangle {
    id: root

    required property var control

    implicitWidth: control.orientation === Qt.Horizontal ? 6 : control.width
    implicitHeight: control.orientation === Qt.Horizontal ? control.height : 6
    color: T.SplitHandle.pressed ? control.Material.background
        : Qt.lighter(control.Material.background, T.SplitHandle.hovered ? 1.2 : 1.1)

    Rectangle {
        color: control.Material.secondaryTextColor
        width: control.orientation === Qt.Horizontal ? thickness : length
        height: control.orientation === Qt.Horizontal ? length : thickness
        radius: thickness
        x: (parent.width - width) / 2
        y: (parent.height - height) / 2

        property int length: parent.T.SplitHandle.pressed ? 3 : 8
        readonly property int thickness: parent.T.SplitHandle.pressed ? 3 : 1

        Behavior on length {
            NumberAnimation {
                duration: 100
            }
        }

        // Begin: Listen to hover changes
        property var hoveredd: parent.T.SplitHandle.hovered

        onHovereddChanged: {
            root.hovered = hoveredd
        }
        //   End: Listen to hover changes
    }

    // Begin: Listen to hover changes
    property var hovered: false
    //   End: Listen to hover changes
}
