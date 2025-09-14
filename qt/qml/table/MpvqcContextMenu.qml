// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

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
