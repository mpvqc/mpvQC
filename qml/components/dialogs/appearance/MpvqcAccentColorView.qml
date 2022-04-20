/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/


import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import components.shared
import helpers
import models


GridView {
    id: gridViewAccent
    model: AccentColorModel {}
    focus: true
    clip: true
    width: 352
    height: (itemSize + itemPadding) * 4
    cellWidth: itemSize + itemPadding
    cellHeight: itemSize + itemPadding

    property int itemSize: 52
    property int itemPadding: 6
    property int itemBorder: 12

    delegate: Component {

        MpvqcCircle {
            width: gridViewAccent.itemSize
            height: width
            color: appThemeColorAccent === accentColor ? Material.foreground : "transparent"

            MpvqcCircle {
                width: parent.width - gridViewAccent.itemBorder
                height: width
                anchors.centerIn: parent
                color: Material.accent
                Material.accent: appWindow.displayableAccentColorFor(colorFill)

                property int colorFill: accentColor

                onClicked: {
                    appWindow.appThemeColorAccent = colorFill
                    MpvqcSettings.accent = colorFill
                }
            }
        }
    }

}
