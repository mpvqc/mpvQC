// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Python

MpvqcPositionedMenu {
    id: root
    objectName: "editCommentTypeMenu"

    required property MpvqcCommentTableViewModel viewModel

    required property string currentCommentType
    required property int currentListIndex

    readonly property bool isCommentTypeUnknown: !root.viewModel.commentTypes.includes(root.currentCommentType)

    function _handleTriggered(newCommentType: string): void {
        if (root.currentCommentType !== newCommentType) {
            root.viewModel.updateCommentType(root.currentListIndex, newCommentType);
        }
    }

    Repeater {
        model: root.viewModel.commentTypes

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
