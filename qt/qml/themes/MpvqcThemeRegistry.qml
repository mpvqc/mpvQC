// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma Singleton

import QtQuick

import "../models"

QtObject {
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
        for (let i = 0; i < _themes.length; ++i)
            if (_themes[i].identifier === identifier)
                return _themes[i];
        return _themes[0];
    }

    function availableThemes() {
        return _themes.map(t => ({
                    identifier: t.identifier,
                    name: t.name,
                    preview: t.preview,
                    isDark: t.isDark
                }));
    }
}
