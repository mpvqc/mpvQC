/*
mpvQC

Copyright (C) 2024 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

import QtQuick

QtObject {
    id: root

    required property var mpvqcApplication

    readonly property var mpvqcSettings: root.mpvqcApplication.mpvqcSettings
    readonly property var mpvqcThemesPyObject: root.mpvqcApplication.mpvqcThemesPyObject

    readonly property QtObject _: QtObject {
        id: _impl

        readonly property string themeIdentifier: root.mpvqcSettings.themeIdentifier
        readonly property string colorOption: root.mpvqcSettings.themeColorOption

        readonly property var themeSummary: root.mpvqcThemesPyObject.getThemeSummary(themeIdentifier)
        readonly property var themeColors: root.mpvqcThemesPyObject.getThemeColorOption(colorOption, themeIdentifier)

        readonly property bool isDark: themeSummary.isDark

        property color background: themeColors.background
        property color foreground: themeColors.foreground

        property color rowHighlight: themeColors.rowHighlight
        property color rowHighlightText: themeColors.rowHighlightText
        property color control: themeColors.control

        property color rowBase: themeColors.rowBase
        property color rowBaseText: themeColors.rowBaseText

        property color rowBaseAlternate: themeColors.rowBaseAlternate
        property color rowBaseAlternateText: themeColors.rowBaseAlternateText

        readonly property int colorChangeAnimationDuration: 150

        Behavior on background { ColorAnimation { duration: _impl.colorChangeAnimationDuration } }
        Behavior on foreground { ColorAnimation { duration: _impl.colorChangeAnimationDuration } }

        Behavior on control { ColorAnimation { duration: _impl.colorChangeAnimationDuration } }
        Behavior on rowHighlight { ColorAnimation { duration: _impl.colorChangeAnimationDuration } }
        Behavior on rowHighlightText { ColorAnimation { duration: _impl.colorChangeAnimationDuration } }

        Behavior on rowBase { ColorAnimation { duration: _impl.colorChangeAnimationDuration } }
        Behavior on rowBaseText { ColorAnimation { duration: _impl.colorChangeAnimationDuration } }

        Behavior on rowBaseAlternate { ColorAnimation { duration: _impl.colorChangeAnimationDuration } }
        Behavior on rowBaseAlternateText { ColorAnimation { duration: _impl.colorChangeAnimationDuration } }
    }

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
}
