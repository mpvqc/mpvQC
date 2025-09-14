// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material

import "../shared"

MpvqcMenu {
    id: root

    required property list<string> commentTypes

    property var _deferToOnClose: () => {}

    signal commentTypeChosen(commentType: string)

    visible: false
    modal: true
    z: 2
    exit: null

    onClosed: {
        visible = false;

        // Instead of directly adding a comment in the MenuItem triggered signal handler,
        // we defer adding it until the popup closes. If we would directly add it,
        // the menu's closing signals would interfere with the focus of the newly added comment.
        root._deferToOnClose(); // qmllint disable
        root._deferToOnClose = () => {};
    }

    Repeater {
        model: root.commentTypes

        MenuItem {
            required property string modelData

            text: qsTranslate("CommentTypes", modelData)

            onTriggered: {
                root._deferToOnClose = () => root.commentTypeChosen(modelData);
            }
        }
    }
}
