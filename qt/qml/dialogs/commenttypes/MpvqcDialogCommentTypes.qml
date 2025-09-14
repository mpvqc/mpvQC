// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick.Controls.Material

import "../../shared"

MpvqcDialog {
    id: root

    title: qsTranslate("CommentTypesDialog", "Comment Types")
    standardButtons: Dialog.Ok | Dialog.Cancel | Dialog.Reset

    contentItem: MpvqcCommentTypesView {
        id: _view

        mpvqcApplication: root.mpvqcApplication
    }

    onAccepted: {
        _view.visible = false;
        _view.acceptTemporaryState();
    }

    onReset: {
        _view.resetTemporaryEdits();
    }
}
