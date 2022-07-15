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
import components.shared
import settings


MpvqcAutoWidthMenu {
    id: control
    modal: true
    dim: false

    property string currentCommentType

    signal itemClicked(string commentType)

    Repeater {
        id: repeater
        model: MpvqcSettings.commentTypes

        MenuItem {
            text: qsTranslate("CommentTypes", model.type)
            autoExclusive: true
            checkable: true
            checked: model.type === currentCommentType
            onTriggered: triggerClicked(model.type)
        }
    }

    MenuSeparator {
        id: separator
        height: isCurrentCommentTypeKnown() ? 0 : implicitHeight
    }

    MenuItem {
        height: isCurrentCommentTypeKnown() ? 0 : implicitHeight
        visible: !isCurrentCommentTypeKnown()
        text: qsTranslate("CommentTypes", currentCommentType)
        autoExclusive: true
        checkable: true
        checked: true
        onTriggered: triggerClicked(currentCommentType)
    }

    function isCurrentCommentTypeKnown() {
        const model = repeater.model
        for (let i = 0, count = model.count; i < count; i++) {
            if (model.get(i).type === currentCommentType) {
                return true
            }
        }
        return false
    }

    function triggerClicked(item) {
        control.itemClicked(item)
    }

}
