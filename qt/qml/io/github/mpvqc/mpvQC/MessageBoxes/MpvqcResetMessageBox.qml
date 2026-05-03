// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick.Controls.Material

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Python

MpvqcMessageBox {
    objectName: "resetMessageBox"

    readonly property MpvqcResetMessageBoxViewModel viewModel: MpvqcResetMessageBoxViewModel {}

    title: qsTranslate("MessageBoxes", "Unsaved Changes")
    text: qsTranslate("MessageBoxes", "Do you really want to create a new QC document without saving your QC?")
    standardButtons: Dialog.Yes | Dialog.No

    onAccepted: viewModel.reset()
}
