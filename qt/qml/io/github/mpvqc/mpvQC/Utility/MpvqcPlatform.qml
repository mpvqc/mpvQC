// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma Singleton

import QtQuick

import io.github.mpvqc.mpvQC.Python

QtObject {

    // Mutable, not readonly: the QML test harness swaps in a fresh view model per test.
    property var _viewModel: MpvqcPlatformViewModel {}

    readonly property bool keepsNativeFrame: _viewModel.keepsNativeFrame
    readonly property bool drawsDropShadow: _viewModel.drawsDropShadow
}
