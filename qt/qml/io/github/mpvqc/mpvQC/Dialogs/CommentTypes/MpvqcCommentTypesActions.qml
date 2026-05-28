// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material

import io.github.mpvqc.mpvQC.Utility

Column {
    id: root

    required property bool moveUpEnabled
    required property bool moveDownEnabled
    required property bool deleteEnabled

    readonly property alias buttonHeight: _upButton.height

    signal moveUpRequested
    signal moveDownRequested
    signal deleteRequested

    spacing: 4

    ToolButton {
        id: _upButton
        objectName: "commentTypeMoveUpButton"

        enabled: root.moveUpEnabled

        icon {
            width: 28
            height: 28
            source: MpvqcIcons.keyboardArrowUp
        }

        onPressed: root.moveUpRequested()
    }

    ToolButton {
        objectName: "commentTypeMoveDownButton"
        enabled: root.moveDownEnabled

        icon {
            width: 28
            height: 28
            source: MpvqcIcons.keyboardArrowDown
        }

        onPressed: root.moveDownRequested()
    }

    ToolButton {
        objectName: "commentTypeDeleteButton"
        enabled: root.deleteEnabled

        icon {
            source: MpvqcIcons.delete_
        }

        onPressed: root.deleteRequested()
    }
}
