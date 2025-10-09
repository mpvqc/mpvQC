// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma Singleton

import QtQuick

import pyobjects

QtObject {
    readonly property bool isDark: _internal.viewModel.isDark
    readonly property alias background: _internal.background.value
    readonly property alias foreground: _internal.foreground.value
    readonly property alias control: _internal.control.value
    readonly property alias rowHighlight: _internal.rowHighlight.value
    readonly property alias rowHighlightText: _internal.rowHighlightText.value
    readonly property alias rowBase: _internal.rowBase.value
    readonly property alias rowBaseText: _internal.rowBaseText.value
    readonly property alias rowBaseAlternate: _internal.rowBaseAlternate.value
    readonly property alias rowBaseAlternateText: _internal.rowBaseAlternateText.value

    function getBackground(isOdd: bool): color {
        return isOdd ? rowBase : rowBaseAlternate;
    }

    function getForeground(isOdd: bool): color {
        return isOdd ? rowBaseText : rowBaseAlternateText;
    }

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
            value: _internal.viewModel.background
        }

        readonly property AnimatedColor foreground: AnimatedColor {
            value: _internal.viewModel.foreground
        }

        readonly property AnimatedColor control: AnimatedColor {
            value: _internal.viewModel.control
        }

        readonly property AnimatedColor rowHighlight: AnimatedColor {
            value: _internal.viewModel.rowHighlight
        }

        readonly property AnimatedColor rowHighlightText: AnimatedColor {
            value: _internal.viewModel.rowHighlightText
        }

        readonly property AnimatedColor rowBase: AnimatedColor {
            value: _internal.viewModel.rowBase
        }

        readonly property AnimatedColor rowBaseText: AnimatedColor {
            value: _internal.viewModel.rowBaseText
        }

        readonly property AnimatedColor rowBaseAlternate: AnimatedColor {
            value: _internal.viewModel.rowBaseAlternate
        }

        readonly property AnimatedColor rowBaseAlternateText: AnimatedColor {
            value: _internal.viewModel.rowBaseAlternateText
        }
    }
}
