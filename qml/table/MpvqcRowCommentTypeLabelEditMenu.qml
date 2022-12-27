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

import shared


MpvqcMenu {
    id: root

    required property var mpvqcApplication
    required property string currentCommentType

    readonly property var mpvqcSettings: mpvqcApplication.mpvqcSettings
    readonly property var commentTypes: mpvqcSettings.commentTypes.items()
    readonly property var currentCommentTypeKnown: commentTypes.some(commentType => commentType === currentCommentType)

    signal itemClicked(string commentType)

    visible: true
    dim: false
    modal: true

    function _createMenu(): void {
        for (const commentType of commentTypes) {
            const object = menuItem.createObject(null, { type: commentType })
            repeater.model.append(object)
        }
    }

    function _appendUnknown(): void {
        const separator = menuSeparator.createObject(null)
        const unknown = menuItem.createObject(null, { type: root.currentCommentType })
        repeater.model.append(separator)
        repeater.model.append(unknown)
    }

    Component.onCompleted: {
        _createMenu()
        if (!currentCommentTypeKnown) {
            _appendUnknown()
        }
    }

    Repeater {
        id: repeater

        model: ObjectModel {}
    }

    Component {
        id: menuSeparator

        MenuSeparator {}
    }

    Component {
        id: menuItem

        MenuItem {
            required property string type

            text: qsTranslate("CommentTypes", type)
            autoExclusive: true
            checkable: true
            checked: type === root.currentCommentType

            onTriggered: {
                root.itemClicked(type)
            }
        }
    }

}
