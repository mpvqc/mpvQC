// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma Singleton

import QtQuick

import io.github.mpvqc.mpvQC.Python

QtObject {
    id: root

    // Mutable, not readonly: the QML test harness swaps in a fresh view model per test.
    property MpvqcPaletteViewModel _viewModel: MpvqcPaletteViewModel {}

    readonly property bool isDark: root._viewModel.isDark

    readonly property color listStripe: Qt.alpha(palette.foreground, isDark ? 0.04 : 0.08)
    readonly property color hoverHighlight: Qt.alpha(palette.foreground, isDark ? 0.15 : 0.24)

    readonly property MpvqcAnimatedPalette palette: MpvqcAnimatedPalette {
        viewModel: root._viewModel
    }
}
