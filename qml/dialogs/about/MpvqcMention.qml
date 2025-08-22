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
import QtQuick.Layouts

RowLayout {
    id: root

    property string leftContent
    property Item leftItem: Label
    {
        text: root.leftContent
        horizontalAlignment: Text.AlignRight
        Layout.preferredWidth: root.width / 2
    }

    property string rightContent
    property Item rightItem: Label
    {
        text: root.rightContent
        font.italic: true
        horizontalAlignment: Text.AlignLeft
        Layout.preferredWidth: root.width / 2
    }

    children: [leftItem, rightItem]

    height: Math.max(leftItem.height, rightItem.height)

    visible: leftContent
    spacing: 10
}
