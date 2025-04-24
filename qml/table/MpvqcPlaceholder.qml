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

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material
import QtQuick.Layouts

Item {
    id: root

    required property bool horizontalLayout

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
