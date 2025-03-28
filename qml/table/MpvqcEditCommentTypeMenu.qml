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

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material

import "../shared"

MpvqcMenu {
    id: root

    required property string currentCommentType
    required property int currentListIndex
    required property point openedAt

    required property list<string> commentTypes

    readonly property bool isCommentTypeKnown: commentTypes.some(commentType => commentType === currentCommentType)
    readonly property bool isCommentTypeUnknown: !isCommentTypeKnown

    signal commentTypeEdited(index: int, newCommentType: string)

    x: root.mirrored ? openedAt.x - width : openedAt.x
    y: openedAt.y

    modal: true

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
