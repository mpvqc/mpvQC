// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material

import pyobjects

import "../../components"
import "../../utility"

MpvqcPositionedMenu {
    id: root

    readonly property var viewModel: MpvqcNewCommentMenuViewModel {}

    function calculatePosition(): point {
        const global = viewModel.cursorPosition();
        return parent.mapFromGlobal(global);
    }

    signal commentTypeChosen(commentType: string)

    visible: false
    z: 2
    exit: null

    Material.background: MpvqcTheme.backgroundAlternate
    Material.foreground: MpvqcTheme.foregroundAlternate

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
