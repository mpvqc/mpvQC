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
import QtQuick.Layouts


Dialog {
    id: root

    required property var mpvqcApplication

    property alias bar: _bar
    property alias stack: _stack

    default property alias content: _stack.children

    anchors.centerIn: parent
    parent: mpvqcApplication.contentItem
    width: 420
    height: 540
    modal: true
    z: 2

    contentItem: ColumnLayout {
        id: _layout

        TabBar {
            id: _bar
            contentWidth: _layout.width

            Repeater {
                model: root.content.length

                delegate: TabButton {
                    text: root.content[index].title
                }
            }
        }

        StackLayout {
            id: _stack
            currentIndex: _bar.currentIndex
        }
    }

    onClosed: {
        root.bar.currentIndex = 0
    }

}
