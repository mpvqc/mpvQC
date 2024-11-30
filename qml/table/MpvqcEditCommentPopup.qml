/*
mpvQC

Copyright (C) 2024 mpvQC developers

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
import QtQuick.Controls.Material

Popup {
    id: root

    required property int currentListIndex
    required property string currentComment

    required property var sanitizeTextFunc

    required property color backgroundColor
    required property color rowHighlightColor
    required property color rowHighlightTextColor

    property bool acceptValue: true

    signal commentEdited(index: int, newComment: string)

    width: root.parent.width

    leftPadding: root.parent.leftPadding / 2 // qmllint disable
    rightPadding: root.parent.rightPadding / 2 // qmllint disable
    topPadding: root.parent.topPadding / 2 // qmllint disable
    bottomPadding: root.parent.bottomPadding / 2 // qmllint disable

    background: null
    dim: false
    modal: false
    enter: null
    exit: null

    contentItem: TextArea {
        id: _textField

        text: root.currentComment
        wrapMode: Text.WordWrap
        horizontalAlignment: Text.AlignLeft

        focus: true
        selectByMouse: true

        bottomPadding: root.bottomPadding
        topPadding: root.topPadding
        leftPadding: root.leftPadding
        rightPadding: root.rightPadding

        selectionColor: root.rowHighlightColor
        selectedTextColor: root.rowHighlightTextColor

        background: Rectangle {
            anchors.fill: parent
            color: root.backgroundColor
        }

        Keys.onReturnPressed: {
            root.close();
        }
    }

    onAboutToHide: {
        if (!acceptValue)
            return;

        const text = _textField.text.trim();
        const sanitizedText = root.sanitizeTextFunc(text); // qmllint disable

        if (root.currentComment !== sanitizedText) {
            root.commentEdited(root.currentListIndex, sanitizedText);
        }
    }

    onActiveFocusChanged: {
        if (!activeFocus) {
            root.close();
        }
    }

    onOpened: {
        _textField.selectAll();
        _textField.forceActiveFocus();
    }

    Shortcut {
        sequence: "Esc"

        onActivated: {
            root.acceptValue = false;
            root.close();
        }
    }

    Binding {
        when: root.visible
        target: root.parent
        property: "text"
        value: "" // don't display text below the editing popup
    }

    Binding {
        when: root.visible
        target: root.parent
        property: "editorHeight"
        value: root.height
    }
}
