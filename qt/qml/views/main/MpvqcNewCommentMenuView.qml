// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material

import pyobjects

import "../../components"

MpvqcMenu {
    id: root

    readonly property var viewModel: MpvqcNewCommentMenuViewModel {}

    property var _deferToOnClose: () => {}

    signal commentTypeChosen(commentType: string)

    visible: false
    modal: true
    z: 2
    exit: null

    onAboutToShow: {
        viewModel.pausePlayer();

        const global = viewModel.cursorPosition();
        const local = parent.mapFromGlobal(global);
        x = isMirrored ? local.x - width : local.x;
        y = local.y;
    }

    onClosed: {
        visible = false;

        // Instead of directly adding a comment in the MenuItem triggered signal handler,
        // we defer adding it until the popup closes. If we would directly add it,
        // the menu's closing signals would interfere with the focus of the newly added comment.
        _deferToOnClose(); // qmllint disable
        _deferToOnClose = () => {};
    }

    Repeater {
        model: root.viewModel.commentTypes

        MenuItem {
            required property string modelData

            text: qsTranslate("CommentTypes", modelData)

            onTriggered: {
                root._deferToOnClose = () => root.commentTypeChosen(modelData);
            }
        }
    }
}
