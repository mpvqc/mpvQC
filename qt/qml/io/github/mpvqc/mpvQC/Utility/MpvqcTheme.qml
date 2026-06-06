// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma Singleton

import QtQuick

import io.github.mpvqc.mpvQC.Python

QtObject {
    id: root

    readonly property bool isDark: root._viewModel.isDark

    readonly property var palette: QtObject {
        readonly property color background: root._background.value
        readonly property color foreground: root._foreground.value
        readonly property color hint: root._hint.value
        readonly property color accent: root._accent.value
        readonly property color separator: root._separator.value
        readonly property color error: root._error.value
        readonly property color errorText: root._errorText.value
        readonly property color headerBackground: root._headerBackground.value
        readonly property color popupBackground: root._popupBackground.value
        readonly property color popupText: root._popupText.value
        readonly property color menuBackground: root._menuBackground.value
        readonly property color dialogBackground: root._dialogBackground.value
        readonly property color tooltipBackground: root._tooltipBackground.value
        readonly property color tooltipText: root._tooltipText.value
        readonly property color rowBase: root._rowBase.value
        readonly property color rowBaseText: root._rowBaseText.value
        readonly property color rowStripe: root._rowStripe.value
        readonly property color rowStripeText: root._rowStripeText.value
        readonly property color rowSelected: root._rowSelected.value
        readonly property color rowSelectedText: root._rowSelectedText.value

        function rowBackground(index: int): color {
            return index % 2 === 1 ? rowBase : rowStripe;
        }

        function rowForeground(index: int): color {
            return index % 2 === 1 ? rowBaseText : rowStripeText;
        }
    }

    component AnimatedColor: QtObject {
        required property color value

        Behavior on value {
            ColorAnimation {
                duration: 150
            }
        }
    }

    readonly property MpvqcThemeViewModel _viewModel: MpvqcThemeViewModel {}

    // qmlformat off
    readonly property AnimatedColor _background: AnimatedColor { value: root._viewModel.palette.background }
    readonly property AnimatedColor _foreground: AnimatedColor { value: root._viewModel.palette.foreground }
    readonly property AnimatedColor _hint: AnimatedColor { value: root._viewModel.palette.hint }
    readonly property AnimatedColor _accent: AnimatedColor { value: root._viewModel.palette.accent }
    readonly property AnimatedColor _separator: AnimatedColor { value: root._viewModel.palette.separator }
    readonly property AnimatedColor _error: AnimatedColor { value: root._viewModel.palette.error }
    readonly property AnimatedColor _errorText: AnimatedColor { value: root._viewModel.palette.errorText }
    readonly property AnimatedColor _headerBackground: AnimatedColor { value: root._viewModel.palette.headerBackground }
    readonly property AnimatedColor _popupBackground: AnimatedColor { value: root._viewModel.palette.popupBackground }
    readonly property AnimatedColor _popupText: AnimatedColor { value: root._viewModel.palette.popupText }
    readonly property AnimatedColor _menuBackground: AnimatedColor { value: root._viewModel.palette.menuBackground }
    readonly property AnimatedColor _dialogBackground: AnimatedColor { value: root._viewModel.palette.dialogBackground }
    readonly property AnimatedColor _tooltipBackground: AnimatedColor { value: root._viewModel.palette.tooltipBackground }
    readonly property AnimatedColor _tooltipText: AnimatedColor { value: root._viewModel.palette.tooltipText }
    readonly property AnimatedColor _rowBase: AnimatedColor { value: root._viewModel.palette.rowBase }
    readonly property AnimatedColor _rowBaseText: AnimatedColor { value: root._viewModel.palette.rowBaseText }
    readonly property AnimatedColor _rowStripe: AnimatedColor { value: root._viewModel.palette.rowStripe }
    readonly property AnimatedColor _rowStripeText: AnimatedColor { value: root._viewModel.palette.rowStripeText }
    readonly property AnimatedColor _rowSelected: AnimatedColor { value: root._viewModel.palette.rowSelected }
    readonly property AnimatedColor _rowSelectedText: AnimatedColor { value: root._viewModel.palette.rowSelectedText }
    // qmlformat on
}
