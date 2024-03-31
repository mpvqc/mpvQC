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


Column {
    id: root

    readonly property alias textFieldHasFocus: _textField.activeFocus

    property alias textField: _textField
    property alias acceptButton: _acceptButton
    property alias rejectButton: _rejectButton

    property alias focusTextFieldOnCompletion: _textField.focusOnCompletion
    property alias validateInput: _textField.validate
    property alias placeholderText: _textField.placeholderText
    property alias text: _textField.text

    signal accepted(string input)
    signal done()

    height: Math.max(_textField.height, _acceptButton.height)

    RowLayout {
        width: root.width
        spacing: 0

        MpvqcInputTextField {
            id: _textField

            Layout.fillWidth: true
            Layout.rightMargin: _acceptButton.leftPadding * 2

            onAcceptedInput: (input) => {
                root.accepted(input)
            }

            onEditingStopped: {
                root.done()
            }
        }

        ToolButton {
            id: _acceptButton
            enabled: _textField.isValid
            icon.width: 20
            icon.height: 20
            icon.source: "qrc:/data/icons/done_black_24dp.svg"

            onClicked: {
                _textField.accepted()
            }
        }

        ToolButton {
            id: _rejectButton
            enabled: _textField.hasText || _textField.hasError
            icon.width: 20
            icon.height: 20
            icon.source: "qrc:/data/icons/close_black_24dp.svg"

            onClicked: {
                _textField.rejected()
            }
        }
    }

    Label {
        text: !_textField.error ? ' ' : _textField.error
        color: Material.accent
        horizontalAlignment: Text.AlignLeft
        width: root.width
        wrapMode: Label.WordWrap
        topPadding: 5
    }

}
