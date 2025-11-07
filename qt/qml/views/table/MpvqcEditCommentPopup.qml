// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material

import "../../utility"

Popup {
    id: root

    required property int currentListIndex
    required property string currentComment

    readonly property bool isOdd: currentListIndex % 2 === 1

    readonly property alias textField: _textField // for tests

    property int previousHeight: 0
    property bool acceptValue: true

    signal commentEdited(index: int, newComment: string)
    signal commentEditPopupHeightChanged(editorHeight: int, heightDelta: int)

    width: root.parent.width

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

        selectionColor: MpvqcTheme.rowHighlight
        selectedTextColor: MpvqcTheme.rowHighlightText

        background: Rectangle {
            anchors.fill: parent
            color: MpvqcTheme.getBackground(root.isOdd)
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
        const heightDelta = root.height - root.previousHeight;
        if (root.previousHeight > 0) {
            // Skip first change (initialization)
            root.commentEditPopupHeightChanged(root.height, heightDelta);
        }
        root.previousHeight = root.height;
    }

    Shortcut {
        sequence: "Esc"

        onActivated: {
            root.acceptValue = false;
            root.close();
        }
    }

    // Hide original text while editing to avoid visual duplication
    Binding {
        when: root.visible
        target: root.parent
        property: "text"
        value: ""
    }

    // Notify delegate of editor height so it can expand to accommodate growing content
    Binding {
        when: root.visible
        target: root.parent
        property: "editorHeight"
        value: root.height
    }
}
