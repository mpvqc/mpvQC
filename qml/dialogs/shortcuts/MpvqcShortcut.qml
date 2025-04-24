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
import QtQuick.Layouts

RowLayout {
    id: root

    property alias shortcutLabel: _description.text

    property alias shortcutButton1: _button1.text
    property alias shortcutButton1Icon: _button1.icon.source

    property alias shortcutButton2: _button2.text
    property alias shortcutButton2Icon: _button2.icon.source

    property alias shortcutButton3: _button3.text
    property alias shortcutButton3Icon: _button3.icon.source

    property bool isMultiShortcut: false
    property int rightMargin: 0
    property int scrollBarPadding: 0

    Label {
        id: _description

        wrapMode: Text.WordWrap
        horizontalAlignment: Text.AlignLeft

        Layout.maximumWidth: root.width - _buttons.width - root.scrollBarPadding
    }

    Rectangle {
        color: "transparent"
        Layout.fillWidth: true
    }

    RowLayout {
        id: _buttons

        spacing: 4

        MpvqcShortcutButton {
            id: _button1
        }

        Label {
            text: root.isMultiShortcut ? "/" : "+"
            height: _button2.hasContent ? parent.height : 0
            width: _button2.hasContent ? implicitWidth : 0
            visible: _button2.hasContent
            verticalAlignment: Text.AlignVCenter
        }

        MpvqcShortcutButton {
            id: _button2
        }

        Label {
            text: "+"

            height: _button3.hasContent ? parent.height : 0
            width: _button3.hasContent ? implicitWidth : 0
            visible: _button3.hasContent
            verticalAlignment: Text.AlignVCenter
        }

        MpvqcShortcutButton {
            id: _button3
        }
    }

    Rectangle {
        color: "transparent"
        Layout.preferredWidth: root.rightMargin
    }
}
