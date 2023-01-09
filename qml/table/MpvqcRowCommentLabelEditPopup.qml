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

    required property var mpvqcApplication
    required property string currentComment
    required property int paddingAround

    property bool acceptValue: true
    property var mpvqcSpecialCharacterValidatorPyObject: mpvqcApplication.mpvqcSpecialCharacterValidatorPyObject

    signal edited(string newComment)
    signal upPressed()
    signal downPressed()

    visible: true
    dim: false
    modal: false
    enter: null
    exit: null
    leftPadding: 0
    rightPadding: 0
    topPadding: paddingAround
    bottomPadding: paddingAround
    closePolicy: Popup.CloseOnPressOutside

    background: Rectangle {
        color: root.Material.accent
    }

    contentItem: TextField {
        id: _textField

        text: root.currentComment
        selectByMouse: true
        horizontalAlignment: Text.AlignLeft
        bottomPadding: topPadding
        leftPadding: root.paddingAround
        rightPadding: root.paddingAround
        focus: true
        validator: root.mpvqcSpecialCharacterValidatorPyObject

        background: Rectangle {
            anchors.fill: parent
            color: Material.background
        }

        onAccepted: root.close()

        onActiveFocusChanged: forceActiveFocus()
    }

    onAboutToHide: {
        if (acceptValue) {
            root.edited(_textField.text.trim())
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

    Connections {
        target: root.mpvqcApplication

        function onActiveFocusItemChanged() {
            if (clickedOutsideOfApplication()) {
                root.close()
            }
        }

        function clickedOutsideOfApplication(): bool {
            return !root.mpvqcApplication.activeFocusItem
        }
    }

    Component.onCompleted: {
        _textField.selectAll();
        _textField.forceActiveFocus()
    }

}
