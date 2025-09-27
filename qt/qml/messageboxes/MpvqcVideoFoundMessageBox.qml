// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick.Controls.Material

import "../shared"

MpvqcMessageBox {
    title: qsTranslate("MessageBoxes", "Video Found")
    text: qsTranslate("MessageBoxes", "A video was found. Do you want to open it?")
    standardButtons: Dialog.Yes | Dialog.No
}
