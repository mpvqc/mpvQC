// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material as M

import io.github.mpvqc.mpvQC.Utility

Column {
    id: root

    required property bool moveUpEnabled
    required property bool moveDownEnabled
    required property bool deleteEnabled

    signal moveUpRequested
    signal moveDownRequested
    signal deleteRequested

    spacing: 3

    ToolButton {
        id: _upButton
        objectName: "commentTypeMoveUpButton"

        width: 36
        height: 36
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

        width: 36
        height: 36
        enabled: root.moveDownEnabled

        icon {
            width: 28
            height: 28
            source: MpvqcIcons.keyboardArrowDown
        }

        onPressed: root.moveDownRequested()
    }

    Item {
        width: 1
        height: 6
    }

    ToolButton {
        objectName: "commentTypeDeleteButton"

        width: 36
        height: 36
        enabled: root.deleteEnabled

        icon {
            source: MpvqcIcons.delete_
        }

        M.Material.foreground: MpvqcTheme.palette.error

        onPressed: root.deleteRequested()
    }
}
