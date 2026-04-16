// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material

import "../../components"
import "../../utility"

MpvqcPositionedMenu {
    id: root
    objectName: "editCommentTypeMenu"

    required property string currentCommentType
    required property int currentListIndex
    required property list<string> commentTypes

    readonly property bool isCommentTypeUnknown: !commentTypes.includes(currentCommentType)

    signal commentTypeEdited(index: int, newCommentType: string)

    function _handleTriggered(newCommentType: string): void {
        if (root.currentCommentType !== newCommentType) {
            root.commentTypeEdited(root.currentListIndex, newCommentType);
        }
    }

    Material.background: MpvqcTheme.backgroundAlternate
    Material.foreground: MpvqcTheme.foregroundAlternate

    Repeater {
        model: root.commentTypes

        delegate: MenuItem {
            required property string modelData
            readonly property string commentType: modelData

            text: qsTranslate("CommentTypes", commentType)
            autoExclusive: true
            checkable: true
            checked: commentType === root.currentCommentType

            onTriggered: root._handleTriggered(commentType)
        }
    }

    Instantiator {
        model: root.isCommentTypeUnknown ? 1 : 0

        delegate: MenuSeparator {}

        onObjectAdded: (_index, object) => root.addItem(object)
    }

    Instantiator {
        model: root.isCommentTypeUnknown ? 1 : 0

        delegate: MenuItem {
            readonly property string commentType: root.currentCommentType

            text: qsTranslate("CommentTypes", commentType)
            autoExclusive: true
            checkable: true
            checked: true

            onTriggered: root._handleTriggered(commentType)
        }

        onObjectAdded: (_index, object) => root.addItem(object)
    }
}
