// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls

import io.github.mpvqc.mpvQC.Components

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

    MenuSeparator {
        visible: root.isCommentTypeUnknown
        // Menu lays out invisible items; only a zero height collapses the slot.
        height: visible ? implicitHeight : 0
    }

    MenuItem {
        readonly property string commentType: root.currentCommentType

        visible: root.isCommentTypeUnknown
        height: visible ? implicitHeight : 0
        text: qsTranslate("CommentTypes", commentType)
        autoExclusive: true
        checkable: true
        checked: root.isCommentTypeUnknown

        onTriggered: root._handleTriggered(commentType)
    }
}
