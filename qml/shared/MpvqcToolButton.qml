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
import QtQuick.Controls
import QtQuick.Controls.Material.impl


ToolButton {
    id: root

    // Customized from src/quickcontrols/material/ToolButton.qml
    // We changed the color to use the primary color instead of a ripple color
    background: Ripple {
        implicitWidth: root.Material.touchTarget
        implicitHeight: root.Material.touchTarget

        readonly property bool square: root.contentItem.width <= root.contentItem.height

        x: (parent.width - width) / 2
        y: (parent.height - height) / 2
        clip: !square
        width: square ? parent.height / 2 : parent.width
        height: square ? parent.height / 2 : parent.height
        pressed: root.pressed
        anchor: root
        active: root.enabled && (root.down || root.visualFocus || root.hovered)
        color: root.Material.accentColor
    }

}
