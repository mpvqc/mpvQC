// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material

import "../../shared"

MpvqcDialog {
    id: root

    property alias editView: _editView

    title: qsTranslate("MpvConfEditDialog", "Edit mpv.conf")

    contentWidth: Math.min(1080, mpvqcApplication.width * 0.75)
    contentHeight: Math.min(1080, mpvqcApplication.height * 0.75)
    standardButtons: Dialog.Ok | Dialog.Cancel | Dialog.Reset

    contentItem: MpvqcEditMpvView {
        id: _editView

        mpvqcApplication: root.mpvqcApplication
    }

    onAccepted: {
        _editView.acceptContent();
    }

    onReset: {
        _editView.restorePreviousContent();
    }
}
