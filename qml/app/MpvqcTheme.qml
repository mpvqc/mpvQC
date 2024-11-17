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
import QtQuick.Controls.Material

QtObject {
    id: root

    required property var mpvqcApplication

    readonly property QtObject _: QtObject {
        id: _impl

        readonly property var mpvqcSettings: root.mpvqcApplication.mpvqcSettings
        readonly property var mpvqcThemesPyObject: root.mpvqcApplication.mpvqcThemesPyObject

        readonly property string themeIdentifier: mpvqcSettings.themeIdentifier
        readonly property string colorOption: mpvqcSettings.themeColorOption

        readonly property bool isDark: mpvqcThemesPyObject.getThemeSummary(themeIdentifier).isDark
        readonly property int variant: isDark ? Material.Dark : Material.Light

        readonly property var theme: mpvqcThemesPyObject.getThemeColorOption(colorOption, themeIdentifier)

        property color background: theme.background
        property color foreground: theme.foreground

        Behavior on background { ColorAnimation { duration: 150 }}
        Behavior on foreground { ColorAnimation { duration: 150 }}

        property color rowHighlight: theme.rowHighlight
        property color rowHighlightText: theme.rowHighlightText
        property color control: theme.control

        Behavior on control { ColorAnimation { duration: 150 }}
        Behavior on rowHighlight { ColorAnimation { duration: 150 }}
        Behavior on rowHighlightText { ColorAnimation { duration: 150 }}

        property color rowBase: theme.rowBase
        property color rowBaseText: theme.rowBaseText

        Behavior on rowBase { ColorAnimation { duration: 150 }}
        Behavior on rowBaseText { ColorAnimation { duration: 150 }}

        property color rowBaseAlternate: theme.rowBaseAlternate
        property color rowBaseAlternateText: theme.rowBaseAlternateText

        Behavior on rowBaseAlternate { ColorAnimation { duration: 150 }}
        Behavior on rowBaseAlternateText { ColorAnimation { duration: 150 }}
    }

    readonly property alias isDark: _impl.isDark
    readonly property alias variant: _impl.variant

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
        return isOdd ? root.rowBase : root.rowBaseAlternate
    }

    function getForeground(isOdd: bool): color {
        return isOdd ? root.rowBaseText : root.rowBaseAlternateText
    }

}
