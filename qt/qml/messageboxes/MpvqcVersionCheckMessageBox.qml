// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick

import pyobjects

import "../components"

MpvqcMessageBox {
    property var viewModel: MpvqcVersionCheckMessageBoxViewModel {}

    title: viewModel.title || qsTranslate("MessageBoxes", "Checking for Updates...")
    text: viewModel.text || qsTranslate("MessageBoxes", "Loading...")
}
