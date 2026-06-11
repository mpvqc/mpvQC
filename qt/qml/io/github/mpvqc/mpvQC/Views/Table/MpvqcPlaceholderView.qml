// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Python

Item {
    id: root
    objectName: "placeholder"

    readonly property MpvqcPlaceholderViewModel viewModel: MpvqcPlaceholderViewModel {}

    readonly property bool horizontalLayout: viewModel.layoutOrientation === Qt.Horizontal
    readonly property int textAlignment: horizontalLayout ? Qt.AlignLeft : (Qt.AlignVCenter | Qt.AlignRight)
    readonly property int columnSpacing: 30
    readonly property int rowSpacing: horizontalLayout ? 10 : 14
    readonly property int verticalGroupGap: horizontalLayout ? columnSpacing : 0

    component ShortcutLabel: Label {
        Layout.alignment: root.textAlignment
    }

    component Plus: Label {
        text: "+"
    }

    GridLayout {
        anchors.centerIn: root
        columns: root.horizontalLayout ? 1 : 2
        columnSpacing: root.horizontalLayout ? 0 : root.columnSpacing
        rowSpacing: root.rowSpacing

        ShortcutLabel {
            //: Keyboard shortcut - displayed when there are zero comments
            text: qsTranslate("CommentTable", "Open Video")
        }

        RowLayout {
            Layout.bottomMargin: root.verticalGroupGap

            MpvqcKeycap {
                text: qsTranslate("KeyboardKeys", "Ctrl")
            }

            Plus {}

            MpvqcKeycap {
                text: qsTranslate("KeyboardKeys", "Alt")
            }

            Plus {}

            MpvqcKeycap {
                text: "O"
            }
        }

        ShortcutLabel {
            //: Keyboard shortcut - displayed when there are zero comments
            text: qsTranslate("CommentTable", "Add Comment")
        }

        MpvqcKeycap {
            text: "E"
            Layout.bottomMargin: root.verticalGroupGap
        }

        ShortcutLabel {
            //: Keyboard shortcut - displayed when there are zero comments
            text: qsTranslate("CommentTable", "Show Keyboard Shortcuts")
        }

        MpvqcKeycap {
            text: "?"
        }
    }
}
