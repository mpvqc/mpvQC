/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material


Popup {
    id: root

    required property var mpvqcDefaultTextValidator
    required property var backgroundColor
    required property string currentComment

    property bool acceptValue: true

    signal edited(string newComment)
    signal upPressed()
    signal downPressed()

    visible: true
    dim: false
    modal: false
    enter: null
    exit: null
    topPadding: 4
    bottomPadding: 4

    background: Rectangle {
        color: root.Material.primary
    }

    contentItem: TextField {
        id: _textField

        text: root.currentComment
        selectByMouse: true
        horizontalAlignment: mirrored ? Text.AlignRight : Text.AlignLeft
        bottomPadding: topPadding
        leftPadding: root.leftPadding
        rightPadding: root.rightPadding
        focus: true
        validator: root.mpvqcDefaultTextValidator

        background: Rectangle {
            anchors.fill: parent
            color: root.backgroundColor
        }

        onAccepted: root.close()
    }

    onAboutToHide: {
        if (acceptValue) {
            root.edited(_textField.text.trim())
        }
    }

    onActiveFocusChanged: {
        if (!activeFocus) {
            root.close()
        }
    }

    Shortcut {
        sequence: "Esc"

        onActivated: {
            root.acceptValue = false
            root.close()
        }
    }

    Shortcut {
        sequence: 'Up'

        onActivated: {
            root.upPressed()
            root.close()
        }
    }

    Shortcut {
        sequence: 'Down'

        onActivated: {
            root.downPressed()
            root.close()
        }
    }

    Component.onCompleted: {
        _textField.selectAll();
        _textField.forceActiveFocus()
    }

}
