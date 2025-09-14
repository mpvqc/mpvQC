// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material
import QtQuick.Layouts

RowLayout {
    id: root

    required property int prefWidth

    property alias label: _label.text
    property alias input: _textField.text
    property alias fontWeight: _textField.font.weight
    property alias implicitTextFieldWidth: _textField.implicitWidth

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
            root.textChanged(text);
        }
    }
}
