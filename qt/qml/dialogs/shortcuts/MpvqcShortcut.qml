// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

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
            visible: _button2.hasContent
            verticalAlignment: Text.AlignVCenter

            Layout.preferredHeight: _button2.hasContent ? parent.height : 0
            Layout.preferredWidth: _button2.hasContent ? implicitWidth : 0
        }

        MpvqcShortcutButton {
            id: _button2
        }

        Label {
            text: "+"

            visible: _button3.hasContent
            verticalAlignment: Text.AlignVCenter

            Layout.preferredHeight: _button3.hasContent ? parent.height : 0
            Layout.preferredWidth: _button3.hasContent ? implicitWidth : 0
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
