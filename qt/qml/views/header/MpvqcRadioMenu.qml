// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material

MpvqcMenuBarMenu {
    id: root

    required property var model
    required property int currentValue

    signal optionSelected(value: int)

    Repeater {
        model: root.model

        delegate: MenuItem {
            objectName: `${root.objectName}RadioItem_${identifier}`

            required property string identifier
            required property string label
            required property int value

            text: label
            autoExclusive: true
            checkable: true
            checked: value === root.currentValue
            onTriggered: root.optionSelected(value)
        }
    }
}
