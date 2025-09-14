// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick

import "../models"

QtObject {
    id: root

    required property string themeIdentifier
    required property int themeColorOption

    readonly property MpvqcThemeMaterialYouDark materialYouDark: MpvqcThemeMaterialYouDark {}
    readonly property MpvqcThemeMaterialYou materialYou: MpvqcThemeMaterialYou {}

    readonly property var availableThemes: [
        {
            "name": materialYouDark.name,
            "preview": materialYouDark.preview
        },
        {
            "name": materialYou.name,
            "preview": materialYou.preview
        }
    ]

    readonly property int colorChangeAnimationDuration: 150

    /* Return all color configurations for the currently configured theme */
    readonly property alias colors: _impl.colors

    readonly property alias isDark: _impl.isDark

    readonly property alias background: _impl.background
    readonly property alias foreground: _impl.foreground

    readonly property alias control: _impl.control
    readonly property alias rowHighlight: _impl.rowHighlight
    readonly property alias rowHighlightText: _impl.rowHighlightText

    readonly property alias rowBase: _impl.rowBase
    readonly property alias rowBaseText: _impl.rowBaseText

    readonly property alias rowBaseAlternate: _impl.rowBaseAlternate
    readonly property alias rowBaseAlternateText: _impl.rowBaseAlternateText

    function getBackground(isOdd: bool): color {
        return isOdd ? root.rowBase : root.rowBaseAlternate;
    }

    function getForeground(isOdd: bool): color {
        return isOdd ? root.rowBaseText : root.rowBaseAlternateText;
    }

    onThemeIdentifierChanged: {
        _impl.reconfigure();
    }

    onThemeColorOptionChanged: {
        _impl.reconfigure();
    }

    Component.onCompleted: {
        _impl.reconfigure();
    }

    readonly property QtObject _: QtObject {
        id: _impl

        readonly property bool isDark: colors.isDark

        property var colors: root.materialYouDark
        property var colorOption: colors.get(root.themeColorOption)

        property color background: colorOption.background
        property color foreground: colorOption.foreground

        property color rowHighlight: colorOption.rowHighlight
        property color rowHighlightText: colorOption.rowHighlightText
        property color control: colorOption.control

        property color rowBase: colorOption.rowBase
        property color rowBaseText: colorOption.rowBaseText

        property color rowBaseAlternate: colorOption.rowBaseAlternate
        property color rowBaseAlternateText: colorOption.rowBaseAlternateText

        function reconfigure(): void {
            switch (root.themeIdentifier) {
            case root.materialYou.name:
                colors = root.materialYou;
                break;
            case root.materialYouDark.name:
                colors = root.materialYouDark;
                break;
            default:
                console.error("Unknown theme:", root.themeIdentifier);
            }
        }

        Behavior on background {
            ColorAnimation {
                duration: root.colorChangeAnimationDuration
            }
        }

        Behavior on foreground {
            ColorAnimation {
                duration: root.colorChangeAnimationDuration
            }
        }

        Behavior on control {
            ColorAnimation {
                duration: root.colorChangeAnimationDuration
            }
        }

        Behavior on rowHighlight {
            ColorAnimation {
                duration: root.colorChangeAnimationDuration
            }
        }

        Behavior on rowHighlightText {
            ColorAnimation {
                duration: root.colorChangeAnimationDuration
            }
        }

        Behavior on rowBase {
            ColorAnimation {
                duration: root.colorChangeAnimationDuration
            }
        }

        Behavior on rowBaseText {
            ColorAnimation {
                duration: root.colorChangeAnimationDuration
            }
        }

        Behavior on rowBaseAlternate {
            ColorAnimation {
                duration: root.colorChangeAnimationDuration
            }
        }

        Behavior on rowBaseAlternateText {
            ColorAnimation {
                duration: root.colorChangeAnimationDuration
            }
        }
    }
}
