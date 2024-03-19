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


Flickable {
    id: root

    required property var mpvqcApplication

    readonly property var mpvqcSettings: mpvqcApplication.mpvqcSettings

    readonly property bool horizontalOrientation: mpvqcSettings.layoutOrientation === Qt.Horizontal
    readonly property var textAlignment: horizontalOrientation
        ? Qt.AlignLeft
        : Qt.AlignVCenter | Qt.AlignRight

    readonly property int columns: horizontalOrientation ? 1 : 2

    readonly property int spacing: 30
    readonly property int shortcutBottomMargin: horizontalOrientation ? spacing + 10 : 0
    readonly property int columnSpacing: horizontalOrientation ? 0 : spacing

    clip: true

    component MpvqcDescriptiveText: Label {
        Layout.alignment: root.textAlignment
    }

    component MpvqcButtonRendered: Button {
        enabled: false
        contentItem: Label {
            text: parent.text
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
    }

    GridLayout {
        anchors.centerIn: root.contentItem
        columns: root.columns
        columnSpacing: root.columnSpacing
        rowSpacing: 10

        MpvqcDescriptiveText {
            text: qsTranslate("CommentTable", "Open Video")
        }

        RowLayout {
            Layout.bottomMargin: root.shortcutBottomMargin

            MpvqcButtonRendered {
                text: qsTranslate("KeyboardKeys", "Ctrl")
            }

            Label {
                text: '+'
            }

            MpvqcButtonRendered {
                text: qsTranslate("KeyboardKeys", "Alt")
            }

            Label {
                text: '+'
            }

            MpvqcButtonRendered {
                text: 'O'
            }

        }


        MpvqcDescriptiveText {
            text: qsTranslate("CommentTable", "Add Comment")
        }

        MpvqcButtonRendered {
            Layout.bottomMargin: root.shortcutBottomMargin

            text: 'E'
        }

        MpvqcDescriptiveText {
            text: qsTranslate("CommentTable", "Show Keyboard Shortcuts")
        }

        MpvqcButtonRendered {
            text: '?'
        }

    }

}
