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

    property alias copyItem: _copyItem
    property alias deleteItem: _deleteItem
    property alias editItem: _editItem

    signal copyCommentClicked()
    signal deleteCommentClicked()
    signal editCommentClicked()

    modal: true
    dim: false

    MenuItem {
        id: _editItem

        text: qsTranslate("CommentTable", "Edit Comment")
        icon.source: "qrc:/data/icons/edit_black_24dp.svg"

        onTriggered: {
            root.exit = null
            root.editCommentClicked()
        }
    }

    MenuItem {
        id: _copyItem

        text: qsTranslate("CommentTable", "Copy Comment")
        icon.source: "qrc:/data/icons/content_copy_black_24dp.svg"

        onTriggered: root.copyCommentClicked()
    }

    MenuItem {
        id: _deleteItem

        text: qsTranslate("CommentTable", "Delete Comment")
        icon.source: "qrc:/data/icons/delete_black_24dp.svg"

        onTriggered: root.deleteCommentClicked()
    }

}
