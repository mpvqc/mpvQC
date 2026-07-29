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
    objectName: "newCommentMenu"

    property var viewModel: MpvqcNewCommentMenuViewModel {}

    signal commentTypeChosen(commentType: string)

    function calculatePosition(): point {
        const global = viewModel.cursorPosition();
        return parent.mapFromGlobal(global);
    }

    visible: false
    exit: null

    onAboutToShow: {
        viewModel.pausePlayer();
    }

    onClosed: {
        visible = false;
    }

    Repeater {
        model: root.viewModel.commentTypes

        MenuItem {
            required property string modelData

            text: qsTranslate("CommentTypes", modelData)

            onTriggered: {
                root.deferToOnClose = () => root.commentTypeChosen(modelData);
            }
        }
    }
}
