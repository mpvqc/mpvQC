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


GridView {
    id: root

    required property var mpvqcApplication

    property var mpvqcSettings: mpvqcApplication.mpvqcSettings
    property int itemSize: 52
    property int itemPadding: 8
    property int borderSize: 12
    property color initialAccent: null
    property color initialPrimary: null

    function reset(): void {
        root.mpvqcSettings.accent = initialAccent
        root.mpvqcSettings.primary = initialPrimary
    }

    boundsBehavior: Flickable.StopAtBounds
    model: MpvqcAccentColorModel {}
    clip: true
    height: (itemSize + itemPadding) * 4
    cellWidth: itemSize + itemPadding
    cellHeight: itemSize + itemPadding

    delegate: MpvqcCircle {
        required property color primary
        required property color accent
        property bool selected: primary === root.mpvqcSettings.primary

        width: root.itemSize
        color: selected ? Material.foreground : 'transparent' // todo remove

        function onItemClicked() {
            root.mpvqcSettings.accent = accent
            root.mpvqcSettings.primary = primary
        }

        onClicked: {
            onItemClicked()
        }

        MpvqcCircle {
            width: parent.width - root.borderSize
            color: primary
            Material.primary: primary // todo remove
            anchors.centerIn: parent

            onClicked: {
                parent.onItemClicked()
            }
        }
    }

    Component.onCompleted: {
        root.initialAccent = root.mpvqcSettings.accent
        root.initialPrimary = root.mpvqcSettings.primary
    }

}
