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


TextField {
    id: root

    required property var validate // param: text -> return: error: string
    required property bool focusOnCompletion

    readonly property bool hasText: text.trim() !== ''
    readonly property bool hasError: error !== ''
    readonly property bool isValid: hasText && !hasError

    property string error: ''

    signal acceptedInput(string input)
    signal editingStopped()

    selectByMouse: true
    bottomPadding: topPadding
    horizontalAlignment: Text.AlignLeft

    function _validate(): void {
        const error = validate(text.trim())
        if (error) {
            _setError(error)
        } else {
            _removeError()
        }
    }

    function _setError(message: string): void {
        error = message
    }

    function _removeError(): void {
        error = ''
    }

    function _removeText(): void {
        text = ''
    }

    function _removeFocus(): void {
        focus = false
    }

    function rejected(): void {
        _stopEditing()
    }

    function _stopEditing(): void {
        _removeText()
        _removeError()
        _removeFocus()
        editingStopped()
    }

    onTextChanged: {
        _validate()
    }

    onAccepted: {
        if (isValid) {
            acceptedInput(text.trim())
            _stopEditing()
        }
    }

    Component.onCompleted: {
        if (focusOnCompletion) {
            forceActiveFocus()
        } else {
            _removeFocus()
        }
    }

    Keys.onEscapePressed: {
        _stopEditing()
    }

}
