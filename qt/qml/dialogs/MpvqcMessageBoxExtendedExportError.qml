// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick.Controls.Material

import "../shared"

MpvqcMessageBox {
    required property string errorMessage
    required property int errorLine

    title: qsTranslate("MessageBoxes", "Export Error")
    text: errorLine ?
    //: %1 will be the line nr of the error, %2 will be the error message (probably in English)
    qsTranslate("MessageBoxes", "Error at line %1: %2").arg(errorLine).arg(errorMessage) : errorMessage

    standardButtons: Dialog.Ok
}
