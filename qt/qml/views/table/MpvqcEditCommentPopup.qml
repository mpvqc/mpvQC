// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material

Popup {
    id: root

    required property int currentListIndex
    required property string currentComment

    required property color backgroundColor
    required property color rowHighlightColor
    required property color rowHighlightTextColor

    property bool acceptValue: true

    signal commentEdited(index: int, newComment: string)
    signal commentEditPopupHeightChanged

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
        const sanitizedText = MpvqcTableUtility.sanitizeText(text);

        if (root.currentComment !== sanitizedText) {
            root.commentEdited(root.currentListIndex, sanitizedText);
        }
    }

    onOpened: {
        _textField.selectAll();
        _textField.forceActiveFocus();
    }

    onActiveFocusChanged: {
        if (!activeFocus) {
            root.close();
        }
    }

    onHeightChanged: {
        root.commentEditPopupHeightChanged();
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
