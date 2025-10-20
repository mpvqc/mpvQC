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

    required property string currentCommentType
    required property int currentListIndex
    required property list<string> commentTypes

    readonly property bool isCommentTypeKnown: commentTypes.some(commentType => commentType === currentCommentType)
    readonly property bool isCommentTypeUnknown: !isCommentTypeKnown

    signal commentTypeEdited(index: int, newCommentType: string)

    function _handleTriggered(potentialNewCommentType: string): void {
        if (root.currentCommentType !== potentialNewCommentType) {
            root.commentTypeEdited(root.currentListIndex, potentialNewCommentType);
        }
    }

    function _populateKnownItems(): void {
        for (const commentType of root.commentTypes) {
            const menuItem = _menuItem.createObject(root.contentItem, {
                commentType
            });
            root.addItem(menuItem);
        }
    }

    function _populateUnknownItem(): void {
        const separator = _menuItemSeparator.createObject(root.contentItem);
        root.addItem(separator);

        const menuItem = _menuItem.createObject(root.contentItem, {
            commentType: root.currentCommentType
        });
        root.addItem(menuItem);
    }

    Material.background: MpvqcTheme.backgroundAlternate
    Material.foreground: MpvqcTheme.foregroundAlternate

    Component.onCompleted: {
        root._populateKnownItems();

        if (isCommentTypeUnknown) {
            root._populateUnknownItem();
        }
    }

    Component {
        id: _menuItemSeparator

        MenuSeparator {}
    }

    Component {
        id: _menuItem

        MenuItem {
            required property string commentType

            text: qsTranslate("CommentTypes", commentType)
            autoExclusive: true
            checkable: true
            checked: commentType === root.currentCommentType

            onTriggered: root._handleTriggered(commentType)
        }
    }
}
