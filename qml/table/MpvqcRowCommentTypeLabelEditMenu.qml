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
import QtQuick.Controls

import shared

MpvqcMenu {
    id: root

    required property var mpvqcApplication
    required property string currentCommentType

    readonly property alias unknownCommentType: _unknownCommentType
    readonly property alias repeater: _repeater

    readonly property var mpvqcSettings: mpvqcApplication.mpvqcSettings
    readonly property var commentTypes: mpvqcSettings.commentTypes
    readonly property bool isCommentTypeKnown: commentTypes.some(commentType => commentType === currentCommentType)
    readonly property bool isCommentTypeUnknown: !isCommentTypeKnown

    signal itemClicked(string commentType)

    dim: false
    modal: true

    Repeater {
        id: _repeater

        model: root.commentTypes

        MenuItem {
            required property string modelData

            text: qsTranslate("CommentTypes", modelData)
            autoExclusive: true
            checkable: true
            checked: modelData === root.currentCommentType

            onTriggered: {
                root.itemClicked(modelData);
            }
        }
    }

    MenuSeparator {
        visible: root.isCommentTypeUnknown
        height: root.isCommentTypeUnknown ? implicitHeight : 0
    }

    MenuItem {
        id: _unknownCommentType

        visible: root.isCommentTypeUnknown
        height: root.isCommentTypeUnknown ? implicitHeight : 0

        text: qsTranslate("CommentTypes", root.currentCommentType)
        autoExclusive: true
        checkable: true
        checked: visible

        onTriggered: {
            root.itemClicked(root.currentCommentType);
        }
    }
}
