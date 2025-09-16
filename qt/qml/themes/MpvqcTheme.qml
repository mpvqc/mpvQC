// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick

QtObject {
    id: root

    required property string themeIdentifier
    required property int themeColorOption

    readonly property int colorChangeAnimationDuration: 150

    readonly property var themeRecord: MpvqcThemeRegistry.byId(themeIdentifier)
    readonly property var paletteModel: themeRecord ? themeRecord.model : null
    readonly property int paletteCount: paletteModel ? paletteModel.count : 0
    readonly property int effectiveColorOption: Math.max(0, Math.min(themeColorOption, Math.max(0, paletteCount - 1)))
    readonly property var currentPalette: (paletteModel && paletteCount > 0) ? paletteModel.get(effectiveColorOption) : null

    readonly property bool isDark: themeRecord ? !!themeRecord.isDark : false

    readonly property color background: _background
    readonly property color foreground: _foreground
    readonly property color control: _control
    readonly property color rowHighlight: _rowHighlight
    readonly property color rowHighlightText: _rowHighlightText
    readonly property color rowBase: _rowBase
    readonly property color rowBaseText: _rowBaseText
    readonly property color rowBaseAlternate: _rowBaseAlternate
    readonly property color rowBaseAlternateText: _rowBaseAlternateText

    property color _background: currentPalette ? currentPalette.background : "transparent"
    property color _foreground: currentPalette ? currentPalette.foreground : "transparent"
    property color _control: currentPalette ? currentPalette.control : "transparent"
    property color _rowHighlight: currentPalette ? currentPalette.rowHighlight : "transparent"
    property color _rowHighlightText: currentPalette ? currentPalette.rowHighlightText : "transparent"
    property color _rowBase: currentPalette ? currentPalette.rowBase : "transparent"
    property color _rowBaseText: currentPalette ? currentPalette.rowBaseText : "transparent"
    property color _rowBaseAlternate: currentPalette ? currentPalette.rowBaseAlternate : "transparent"
    property color _rowBaseAlternateText: currentPalette ? currentPalette.rowBaseAlternateText : "transparent"

    function getBackground(isOdd: bool): color {
        return isOdd ? rowBase : rowBaseAlternate;
    }

    function getForeground(isOdd: bool): color {
        return isOdd ? rowBaseText : rowBaseAlternateText;
    }

    Behavior on _background {
        ColorAnimation {
            duration: root.colorChangeAnimationDuration
        }
    }

    Behavior on _foreground {
        ColorAnimation {
            duration: root.colorChangeAnimationDuration
        }
    }

    Behavior on _control {
        ColorAnimation {
            duration: root.colorChangeAnimationDuration
        }
    }

    Behavior on _rowHighlight {
        ColorAnimation {
            duration: root.colorChangeAnimationDuration
        }
    }

    Behavior on _rowHighlightText {
        ColorAnimation {
            duration: root.colorChangeAnimationDuration
        }
    }

    Behavior on _rowBase {
        ColorAnimation {
            duration: root.colorChangeAnimationDuration
        }
    }

    Behavior on _rowBaseText {
        ColorAnimation {
            duration: root.colorChangeAnimationDuration
        }
    }

    Behavior on _rowBaseAlternate {
        ColorAnimation {
            duration: root.colorChangeAnimationDuration
        }
    }

    Behavior on _rowBaseAlternateText {
        ColorAnimation {
            duration: root.colorChangeAnimationDuration
        }
    }
}
