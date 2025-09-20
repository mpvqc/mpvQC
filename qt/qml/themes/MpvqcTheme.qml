// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma Singleton

import QtQuick

import pyobjects

import "../models"

QtObject {
    id: root

    // Allow override in tests
    property var mpvqcSettings: MpvqcSettings

    readonly property bool isDark: _internal.isDark
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

    property QtObject _internal1: QtObject {
        id: _internal

        readonly property string themeIdentifier: root.mpvqcSettings?.themeIdentifier ?? "material-you-dark"
        readonly property int themeColorOption: root.mpvqcSettings?.themeColorOption ?? 4

        readonly property var themeRecord: root.registry.byId(themeIdentifier)
        readonly property var paletteModel: themeRecord?.model ?? null
        readonly property int paletteCount: paletteModel?.count ?? 0
        readonly property bool isDark: themeRecord?.isDark ?? false

        readonly property int effectiveColorOption: {
            if (paletteCount <= 0) {
                return 0;
            }
            return Math.max(0, Math.min(themeColorOption, paletteCount - 1));
        }

        readonly property var currentPalette: {
            return (paletteModel && paletteCount > 0) ? paletteModel.get(effectiveColorOption) : null;
        }

        readonly property AnimatedColor background: AnimatedColor {
            value: _internal.currentPalette?.background ?? "transparent"
        }

        readonly property AnimatedColor foreground: AnimatedColor {
            value: _internal.currentPalette?.foreground ?? "transparent"
        }

        readonly property AnimatedColor control: AnimatedColor {
            value: _internal.currentPalette?.control ?? "transparent"
        }

        readonly property AnimatedColor rowHighlight: AnimatedColor {
            value: _internal.currentPalette?.rowHighlight ?? "transparent"
        }

        readonly property AnimatedColor rowHighlightText: AnimatedColor {
            value: _internal.currentPalette?.rowHighlightText ?? "transparent"
        }

        readonly property AnimatedColor rowBase: AnimatedColor {
            value: _internal.currentPalette?.rowBase ?? "transparent"
        }

        readonly property AnimatedColor rowBaseText: AnimatedColor {
            value: _internal.currentPalette?.rowBaseText ?? "transparent"
        }

        readonly property AnimatedColor rowBaseAlternate: AnimatedColor {
            value: _internal.currentPalette?.rowBaseAlternate ?? "transparent"
        }

        readonly property AnimatedColor rowBaseAlternateText: AnimatedColor {
            value: _internal.currentPalette?.rowBaseAlternateText ?? "transparent"
        }
    }

    readonly property QtObject registry: QtObject {
        readonly property ListModel materialYouModel: MpvqcThemeMaterialYou {}
        readonly property ListModel materialYouDarkModel: MpvqcThemeMaterialYouDark {}

        readonly property var _themes: [
            {
                identifier: "material-you",
                name: "Material You",
                preview: "#f4f4e9",
                isDark: false,
                model: materialYouModel
            },
            {
                identifier: "material-you-dark",
                name: "Material You Dark",
                preview: "#121212",
                isDark: true,
                model: materialYouDarkModel
            }
        ]

        function byId(identifier: string): var {
            for (let i = 0; i < _themes.length; ++i) {
                if (_themes[i].identifier === identifier) {
                    return _themes[i];
                }
            }
            return _themes[0];
        }

        function availableThemes(): list<var> {
            return _themes.map(t => ({
                        identifier: t.identifier,
                        name: t.name,
                        preview: t.preview,
                        isDark: t.isDark
                    }));
        }
    }
}
