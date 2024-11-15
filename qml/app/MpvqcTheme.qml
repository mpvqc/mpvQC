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

    readonly property bool isDark: true
    readonly property int variant: isDark ? Material.Dark : Material.Light

    readonly property color background: "#2e3440"
    readonly property color foreground: "#d8dee9"

    readonly property color control: "#bf616a"
    readonly property color rowHighlight:  "#934b52"
    readonly property color rowHighlightText: "#d8dee9"

    readonly property color rowBase: "#2e3440"
    readonly property color rowBaseText: "#d8dee9"

    readonly property color rowBaseAlternate: Qt.lighter("#2e3440", 1.3)
    readonly property color rowBaseAlternateText: "#d8dee9"

    function getBackground(isOdd: bool): color {
        return isOdd ? root.rowBase : root.rowBaseAlternate
    }

    function getForeground(isOdd: bool): color {
        return isOdd ? root.rowBaseText : root.rowBaseAlternateText
    }

}
