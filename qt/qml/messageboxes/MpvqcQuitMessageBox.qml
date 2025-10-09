// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick.Controls.Material

import "../components"

MpvqcMessageBox {
    title: qsTranslate("MessageBoxes", "Unsaved Changes")
    text: qsTranslate("MessageBoxes", "Do you really want to quit without saving your QC?")
    standardButtons: Dialog.Yes | Dialog.Cancel
}
