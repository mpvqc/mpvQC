// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick.Controls.Material

import "../shared"

MpvqcMessageBox {
    id: root

    required property int commentIndex

    signal deleteCommentConfirmed(index: int)

    title: qsTranslate("MessageBoxes", "Delete Comment")
    text: qsTranslate("MessageBoxes", "Do you really want to delete this comment?")
    standardButtons: Dialog.Yes | Dialog.Cancel

    onAccepted: {
        root.deleteCommentConfirmed(root.commentIndex);
    }
}
