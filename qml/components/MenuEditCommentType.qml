/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/


import QtQuick
import QtQuick.Controls
import pyobjects


MenuAutoWidth {

    id: menu

    property string currentCommentType
    property bool currentCommentTypeKnown: Qt.binding(function() {
        return
    })

    signal itemClicked(string type)

    modal: true
    dim: false

    Repeater {
        model: menu.createModel()

        MenuItem {
            text: qsTranslate("CommentTypes", model.item)
            autoExclusive: true
            checkable: true
            checked: model.item === currentCommentType
            onTriggered: triggerClicked(model.item)
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

    function createModel() {
        const model = Qt.createQmlObject('import QtQuick; ListModel {}', menu)
        for (let commentType of SettingsPyObject.comment_types) {
            model.append({ item: commentType })
        }
        return model
    }

    function isCurrentCommentTypeKnown() {
        return SettingsPyObject.comment_types.includes(currentCommentType)
    }

    function triggerClicked(item) {
        menu.itemClicked(item)
    }

}
