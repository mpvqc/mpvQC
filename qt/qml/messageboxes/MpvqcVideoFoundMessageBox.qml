// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick.Controls.Material

import "../components"

MpvqcMessageBox {
    required property string file
    required property string trackingId

    signal importDecisionMade(trackingId: string, openVideo: bool)

    title: qsTranslate("MessageBoxes", "Video Found")
    text: qsTranslate("MessageBoxes", "A video was found. Do you want to open it?") + "\n\n" + file
    standardButtons: Dialog.Yes | Dialog.No

    onAccepted: importDecisionMade(trackingId, true)
    onRejected: importDecisionMade(trackingId, false)
}
