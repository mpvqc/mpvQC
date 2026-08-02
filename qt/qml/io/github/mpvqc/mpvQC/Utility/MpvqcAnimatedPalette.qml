// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick

import io.github.mpvqc.mpvQC.Python

QtObject {
    id: root

    required property MpvqcPaletteViewModel viewModel

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
    readonly property color sectionCard: root._sectionCard.value
    readonly property color tooltipBackground: root._tooltipBackground.value
    readonly property color tooltipText: root._tooltipText.value
    readonly property color rowBase: root._rowBase.value
    readonly property color rowBaseText: root._rowBaseText.value
    readonly property color rowStripe: root._rowStripe.value
    readonly property color rowStripeText: root._rowStripeText.value
    readonly property color rowSelected: root._rowSelected.value
    readonly property color rowSelectedText: root._rowSelectedText.value

    // qmlformat off
    readonly property AnimatedColor _background: AnimatedColor { value: root.viewModel.background }
    readonly property AnimatedColor _foreground: AnimatedColor { value: root.viewModel.foreground }
    readonly property AnimatedColor _hint: AnimatedColor { value: root.viewModel.hint }
    readonly property AnimatedColor _accent: AnimatedColor { value: root.viewModel.accent }
    readonly property AnimatedColor _separator: AnimatedColor { value: root.viewModel.separator }
    readonly property AnimatedColor _error: AnimatedColor { value: root.viewModel.error }
    readonly property AnimatedColor _errorText: AnimatedColor { value: root.viewModel.errorText }
    readonly property AnimatedColor _headerBackground: AnimatedColor { value: root.viewModel.headerBackground }
    readonly property AnimatedColor _popupBackground: AnimatedColor { value: root.viewModel.popupBackground }
    readonly property AnimatedColor _popupText: AnimatedColor { value: root.viewModel.popupText }
    readonly property AnimatedColor _menuBackground: AnimatedColor { value: root.viewModel.menuBackground }
    readonly property AnimatedColor _dialogBackground: AnimatedColor { value: root.viewModel.dialogBackground }
    readonly property AnimatedColor _sectionCard: AnimatedColor { value: root.viewModel.sectionCard }
    readonly property AnimatedColor _tooltipBackground: AnimatedColor { value: root.viewModel.tooltipBackground }
    readonly property AnimatedColor _tooltipText: AnimatedColor { value: root.viewModel.tooltipText }
    readonly property AnimatedColor _rowBase: AnimatedColor { value: root.viewModel.rowBase }
    readonly property AnimatedColor _rowBaseText: AnimatedColor { value: root.viewModel.rowBaseText }
    readonly property AnimatedColor _rowStripe: AnimatedColor { value: root.viewModel.rowStripe }
    readonly property AnimatedColor _rowStripeText: AnimatedColor { value: root.viewModel.rowStripeText }
    readonly property AnimatedColor _rowSelected: AnimatedColor { value: root.viewModel.rowSelected }
    readonly property AnimatedColor _rowSelectedText: AnimatedColor { value: root.viewModel.rowSelectedText }
    // qmlformat on

    component AnimatedColor: QtObject {
        required property color value

        Behavior on value {
            ColorAnimation {
                duration: 150
            }
        }
    }

    function rowBackground(index: int): color {
        return index % 2 === 1 ? root.rowBase : root.rowStripe;
    }

    function rowForeground(index: int): color {
        return index % 2 === 1 ? root.rowBaseText : root.rowStripeText;
    }
}
