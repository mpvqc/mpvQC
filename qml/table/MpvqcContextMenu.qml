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
import QtQuick.Controls.Material

import "../shared"

MpvqcMenu {
    id: root

    required property int currentListIndex
    required property point openedAt

    property var _deferToOnClose: () => {}

    signal copyCommentClicked(index: int)
    signal deleteCommentClicked(index: int)
    signal editCommentClicked(index: int)

    modal: true

    x: root.mirrored ? openedAt.x - width : openedAt.x
    y: openedAt.y

    onClosed: {
        // Run the stored callback.
        // Required for Windows as closing animation interferes with signal handling
        root._deferToOnClose(); // qmllint disable
        root._deferToOnClose = () => {};
    }

    MenuItem {
        //: Context menu on right click in comments table
        text: qsTranslate("CommentTable", "Edit Comment")
        icon.source: "qrc:/data/icons/edit_black_24dp.svg"

        onTriggered: {
            root.exit = null;
            root._deferToOnClose = () => root.editCommentClicked(root.currentListIndex);
        }
    }

    MenuItem {
        //: Context menu on right click in comments table
        text: qsTranslate("CommentTable", "Copy Comment")
        icon.source: "qrc:/data/icons/content_copy_black_24dp.svg"

        onTriggered: root.copyCommentClicked(root.currentListIndex)
    }

    MenuItem {
        //: Context menu on right click in comments table
        text: qsTranslate("CommentTable", "Delete Comment")
        icon.source: "qrc:/data/icons/delete_black_24dp.svg"

        onTriggered: root.deleteCommentClicked(root.currentListIndex)
    }
}
