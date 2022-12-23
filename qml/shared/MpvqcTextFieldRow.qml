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

RowLayout {
    id: root

    required property int prefWidth

    property alias label: _label.text
    property alias input: _textField.text
    property alias bold: _textField.font.bold

    signal textChanged(string text)

    Label {
        id: _label

        horizontalAlignment: Text.AlignRight
        wrapMode: Text.Wrap
        Layout.preferredWidth: root.prefWidth / 2
    }

    TextField {
        id: _textField

        focus: true
        selectByMouse: true
        bottomPadding: topPadding
        horizontalAlignment: Text.AlignLeft

        onTextChanged: {
            root.textChanged(text)
        }
    }

}
