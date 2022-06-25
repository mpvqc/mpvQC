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
import helpers


Dialog {
    id: inputDialog
    width: MpvqcConstants.dialogWidth * 0.80
    modal: true
    focus: true
    anchors.centerIn: parent
    closePolicy: Popup.CloseOnEscape
    footer: DialogButtonBox {
        id: buttons
        standardButtons: Dialog.Ok | Dialog.Cancel
    }

    property var validate: {}
    property bool inputValid: false
    property alias headerLabel: headerLabel.text
    property alias text: textInput.text

    signal inputReceived(string text)

    onInputValidChanged: {
        updateOkButtonState()
    }

    function updateOkButtonState() {
        buttons.standardButton(Dialog.Ok).enabled = inputValid
    }

    Component.onCompleted: {
        textInput.triggerValidation()
        updateOkButtonState()
    }

    ColumnLayout {
        width: parent.width
        spacing: 6

        Label {
            id: headerLabel
            font.bold: true
            font.pixelSize: MpvqcConstants.fontSizeSmall
        }

        TextField {
            id: textInput
            focus: true
            selectByMouse: true
            bottomPadding: topPadding
            horizontalAlignment: Text.AlignLeft
            Layout.fillWidth: true

            onTextChanged: {
                triggerValidation()
            }

            function triggerValidation() {
                if (!textInput.text.trim()) {
                    handleEmptyText()
                } else {
                    handleExistingText()
                }
            }

            function handleEmptyText() {
                errorLabel.text = ' '
                inputValid = false
            }

            function handleExistingText() {
                const error = validate(textInput.text.trim())
                if (error) {
                    errorLabel.text = error
                    inputValid = false
                } else {
                    errorLabel.text = ' '
                    inputValid = true
                }
            }

            onAccepted: {
                if (inputValid) {
                    inputDialog.accepted()
                }
            }
        }

        Label {
            id: errorLabel
            text: ' '
            color: Material.accent
        }
    }

    onAccepted: {
        inputReceived(textInput.text.trim())
    }

}
