// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material
import QtQuick.Layouts

import pyobjects

Item {
    id: root

    readonly property MpvqcPlaceholderViewModel viewModel: MpvqcPlaceholderViewModel {}

    readonly property bool horizontalLayout: viewModel.layoutOrientation === Qt.Horizontal
    readonly property var textAlignment: horizontalLayout ? Qt.AlignLeft : Qt.AlignVCenter | Qt.AlignRight
    readonly property int shortcutBottomMargin: horizontalLayout ? spacing + 10 : 0
    readonly property int spacing: 30

    GridLayout {
        anchors.centerIn: root
        columns: root.horizontalLayout ? 1 : 2
        columnSpacing: root.horizontalLayout ? 0 : root.spacing
        rowSpacing: 10

        Label {
            //: Keyboard shortcut - displayed when there are zero comments
            text: qsTranslate("CommentTable", "Open Video")

            Layout.alignment: root.textAlignment
        }

        RowLayout {
            Layout.bottomMargin: root.shortcutBottomMargin

            Button {
                text: qsTranslate("KeyboardKeys", "Ctrl")
                enabled: false
            }

            Label {
                text: "+"
            }

            Button {
                text: qsTranslate("KeyboardKeys", "Alt")
                enabled: false
            }

            Label {
                text: "+"
            }

            Button {
                text: "O"
                enabled: false
            }
        }

        Label {
            //: Keyboard shortcut - displayed when there are zero comments
            text: qsTranslate("CommentTable", "Add Comment")

            Layout.alignment: root.textAlignment
        }

        Button {
            text: "E"
            enabled: false

            Layout.bottomMargin: root.shortcutBottomMargin
        }

        Label {
            //: Keyboard shortcut - displayed when there are zero comments
            text: qsTranslate("CommentTable", "Show Keyboard Shortcuts")

            Layout.alignment: root.textAlignment
        }

        Button {
            text: "?"
            enabled: false
        }
    }
}
