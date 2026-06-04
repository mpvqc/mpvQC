// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma Singleton

import QtQuick

import io.github.mpvqc.mpvQC.Python

QtObject {
    readonly property MpvqcFontsViewModel viewModel: MpvqcFontsViewModel {}

    readonly property font applicationFont: viewModel.applicationFont
    readonly property font monospaceFont: viewModel.monospaceFont
}
