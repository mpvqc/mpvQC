// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick

import "../../themes"

import pyobjects

QtObject {

    // --- Exposed properties to overwrite in testing
    readonly property var mpvqcTheme: MpvqcTheme
    readonly property var mpvqcSettings: MpvqcSettings

    // --- Exposed properties
    readonly property var themeModel: mpvqcTheme.registry.availableThemes()
    readonly property var colorModel: currentTheme?.model ?? []
    readonly property var currentTheme: mpvqcTheme.registry.byId(mpvqcSettings.themeIdentifier)

    readonly property int themeModelIndex: findThemeIndex(mpvqcSettings.themeIdentifier)
    readonly property int colorModelIndex: _colorModelIndex

    readonly property bool suppressColorAnimation: _suppressColorAnimation

    readonly property color controlColor: mpvqcTheme.control
    readonly property color colorOptionHighlightColor: mpvqcTheme.isDark ? mpvqcTheme.foreground : mpvqcTheme.background
    readonly property color colorOptionHighlightBorderColor: mpvqcTheme.rowHighlight
    readonly property int colorOptionHighlightBorderWidth: mpvqcTheme.isDark ? 0 : 2

    // --- State
    property int _colorModelIndex: mpvqcSettings.themeColorOption
    property var _initialState: ({
            themeIdentifier: "",
            themeColorOption: -1
        })
    property bool _suppressColorAnimation: false

    function findThemeIndex(identifier: string): int {
        for (const [index, item] of themeModel.entries()) {
            if (item.identifier === identifier) {
                return index;
            }
        }
        return -1;
    }

    function init(): void {
        _initialState.themeIdentifier = mpvqcSettings.themeIdentifier;
        _initialState.themeColorOption = mpvqcSettings.themeColorOption;
    }

    function reset(): void {
        mpvqcSettings.themeIdentifier = _initialState.themeIdentifier;
        mpvqcSettings.themeColorOption = _initialState.themeColorOption;
    }

    function setTheme(themeIdentifier: string): void {
        mpvqcSettings.themeIdentifier = themeIdentifier;
    }

    function setColorOption(index: int): void {
        mpvqcSettings.themeColorOption = index;
        _colorModelIndex = index;
    }

    function restoreColorOptionIndexAfterModelChange(): void {
        _suppressColorAnimation = true;
        const desiredIndex = colorModelIndex;
        _colorModelIndex = -1;
        _colorModelIndex = desiredIndex;
        _suppressColorAnimation = false;
    }
}
