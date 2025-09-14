// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material
import QtQuick.Layouts

Column {
    id: root

    required property var mpvqcApplication

    readonly property var mpvqcTheme: mpvqcApplication.mpvqcTheme

    readonly property alias textFieldHasFocus: _textField.activeFocus

    property alias textField: _textField
    property alias acceptButton: _acceptButton
    property alias rejectButton: _rejectButton

    property alias focusTextFieldOnCompletion: _textField.focusOnCompletion
    property alias validateInput: _textField.validate
    property alias placeholderText: _textField.placeholderText
    property alias text: _textField.text

    signal accepted(input: string)
    signal done

    height: Math.max(_textField.height, _acceptButton.height)

    RowLayout {
        width: root.width
        spacing: 0

        MpvqcInputTextField {
            id: _textField

            Layout.fillWidth: true
            Layout.rightMargin: _acceptButton.leftPadding * 2

            onAcceptedInput: input => {
                root.accepted(input);
            }

            onEditingStopped: {
                root.done();
            }
        }

        ToolButton {
            id: _acceptButton
            enabled: _textField.isValid
            icon.width: 20
            icon.height: 20
            icon.source: "qrc:/data/icons/done_black_24dp.svg"

            onPressed: {
                _textField.accepted();
            }
        }

        ToolButton {
            id: _rejectButton
            enabled: _textField.hasText || _textField.hasError
            icon.width: 20
            icon.height: 20
            icon.source: "qrc:/data/icons/close_black_24dp.svg"

            onPressed: {
                _textField.rejected();
            }
        }
    }

    Label {
        text: !_textField.error ? " " : _textField.error
        color: root.mpvqcTheme.control
        horizontalAlignment: Text.AlignLeft
        width: root.width
        wrapMode: Label.WordWrap
        topPadding: 5
    }
}
