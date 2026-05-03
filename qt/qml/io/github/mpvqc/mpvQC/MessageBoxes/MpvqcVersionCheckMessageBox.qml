// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Python

MpvqcMessageBox {
    objectName: "versionCheckMessageBox"

    readonly property MpvqcVersionCheckMessageBoxViewModel viewModel: MpvqcVersionCheckMessageBoxViewModel {}

    title: viewModel.title || qsTranslate("MessageBoxes", "Checking for Updates...")
    text: viewModel.text || qsTranslate("MessageBoxes", "Loading...")
}
