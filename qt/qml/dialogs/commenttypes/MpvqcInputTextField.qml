// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material

TextField {
    id: root

    required property var validate // param: text -> return: error: string
    required property bool focusOnCompletion

    readonly property bool hasText: text.trim() !== ""
    readonly property bool hasError: error !== ""
    readonly property bool isValid: hasText && !hasError

    property string error: ""

    signal acceptedInput(string input)
    signal editingStopped

    selectByMouse: true
    bottomPadding: topPadding
    horizontalAlignment: Text.AlignLeft

    function _validate(): void {
        const error = validate(text.trim());
        if (error) {
            _setError(error);
        } else {
            _removeError();
        }
    }

    function _setError(message: string): void {
        error = message;
    }

    function _removeError(): void {
        error = "";
    }

    function _removeText(): void {
        text = "";
    }

    function _removeFocus(): void {
        focus = false;
    }

    function rejected(): void {
        _stopEditing();
    }

    function _stopEditing(): void {
        _removeText();
        _removeError();
        _removeFocus();
        editingStopped();
    }

    onTextChanged: {
        _validate();
    }

    onAccepted: {
        if (isValid) {
            acceptedInput(text.trim());
            _stopEditing();
        }
    }

    Component.onCompleted: {
        if (focusOnCompletion) {
            forceActiveFocus();
        } else {
            _removeFocus();
        }
    }

    Keys.onEscapePressed: {
        _stopEditing();
    }
}
