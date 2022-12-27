/*
mpvQC

Copyright (C) 2022 mpvQC developers

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

import models
import shared


ListView {
    id: root

    required property var mpvqcApplication
    property var mpvqcSettings: mpvqcApplication.mpvqcSettings
    property int itemSize: 52
    property int borderSize: 12

    boundsBehavior: Flickable.StopAtBounds
    model: MpvqcThemeModel {}
    clip: true
    spacing: 8
    height: itemSize
    orientation: ListView.Horizontal

    delegate: MpvqcCircle {
        required property int theme
        property bool selected: theme === root.mpvqcSettings.theme

        width: root.itemSize
        color: selected ? Material.foreground : 'transparent'

        function onItemClicked() {
            root.mpvqcSettings.theme = theme
        }

        onClicked: {
            onItemClicked()
        }

        MpvqcCircle {
            width: parent.width - root.borderSize
            color: Material.background
            Material.theme: parent.theme
            anchors.centerIn: parent

            onClicked: {
                parent.onItemClicked()
            }
        }
    }

}
