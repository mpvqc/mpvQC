// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma Singleton

import QtQuick

import io.github.mpvqc.mpvQC.Python

QtObject {
    readonly property bool isDark: _internal.viewModel.isDark
    readonly property var palette: _palette

    component AnimatedColor: QtObject {
        required property color value

        Behavior on value {
            ColorAnimation {
                duration: 150
            }
        }
    }

    property QtObject _: QtObject {
        id: _internal

        readonly property var viewModel: MpvqcThemeViewModel {}

        readonly property AnimatedColor background: AnimatedColor {
            value: _internal.viewModel.palette.background
        }

        readonly property AnimatedColor backgroundAlternate: AnimatedColor {
            value: _internal.viewModel.palette.backgroundAlternate
        }

        readonly property AnimatedColor foreground: AnimatedColor {
            value: _internal.viewModel.palette.foreground
        }

        readonly property AnimatedColor foregroundAlternate: AnimatedColor {
            value: _internal.viewModel.palette.foregroundAlternate
        }

        readonly property AnimatedColor control: AnimatedColor {
            value: _internal.viewModel.palette.control
        }

        readonly property AnimatedColor rowHighlight: AnimatedColor {
            value: _internal.viewModel.palette.rowHighlight
        }

        readonly property AnimatedColor rowHighlightText: AnimatedColor {
            value: _internal.viewModel.palette.rowHighlightText
        }

        readonly property AnimatedColor rowBase: AnimatedColor {
            value: _internal.viewModel.palette.rowBase
        }

        readonly property AnimatedColor rowBaseText: AnimatedColor {
            value: _internal.viewModel.palette.rowBaseText
        }

        readonly property AnimatedColor rowBaseAlternate: AnimatedColor {
            value: _internal.viewModel.palette.rowBaseAlternate
        }

        readonly property AnimatedColor rowBaseAlternateText: AnimatedColor {
            value: _internal.viewModel.palette.rowBaseAlternateText
        }
    }

    property QtObject __palette: QtObject {
        id: _palette

        readonly property color background: _internal.background.value
        readonly property color backgroundAlternate: _internal.backgroundAlternate.value
        readonly property color foreground: _internal.foreground.value
        readonly property color foregroundAlternate: _internal.foregroundAlternate.value
        readonly property color control: _internal.control.value
        readonly property color rowHighlight: _internal.rowHighlight.value
        readonly property color rowHighlightText: _internal.rowHighlightText.value
        readonly property color rowBase: _internal.rowBase.value
        readonly property color rowBaseText: _internal.rowBaseText.value
        readonly property color rowBaseAlternate: _internal.rowBaseAlternate.value
        readonly property color rowBaseAlternateText: _internal.rowBaseAlternateText.value

        function rowBackground(index: int): color {
            return index % 2 === 1 ? rowBase : rowBaseAlternate;
        }

        function rowForeground(index: int): color {
            return index % 2 === 1 ? rowBaseText : rowBaseAlternateText;
        }
    }
}
