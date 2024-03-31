/*
mpvQC

Copyright (C) 2024 mpvQC developers

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
import QtQuick.Controls.Material
import QtQuick.Layouts

import shared


ScrollView {
    id: root

    required property bool singleColumn

    Binding on contentHeight {
        when: !root.singleColumn
        value: root.availableHeight
    }

    Binding on contentWidth {
        when: root.singleColumn
        value: root.availableWidth
    }

    ScrollBar.horizontal {
        policy: contentWidth > width ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff
        position: root.mirrored ? 1.0 - ScrollBar.horizontal.size : 0
    }

    ScrollBar.vertical {
        policy: contentHeight > height ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff
    }

    leftPadding: LayoutMirroring.enabled ? 22 : 0

    GridLayout {
        id: _grid

        readonly property int elementHeight: Math.max(_header.height, _shortcut.height)
        readonly property int elementWidth: Math.max(_header.width, _shortcut.width)

        rows: root.contentHeight / _grid.elementHeight
        columns: 1
        flow: root.singleColumn ? GridLayout.LeftToRight : GridLayout.TopToBottom
        columnSpacing: 20

        MpvqcHeader {
            id: _header

            text: "mpvQC"
            Layout.fillWidth: true
        }

        MpvqcShortcut {
            id: _shortcut

            label: qsTranslate("KeyboardKeys", "New QC Document")
            button1: qsTranslate("KeyboardKeys", "Ctrl")
            button2: "N"
        }

        MpvqcShortcut {
            label: qsTranslate("KeyboardKeys", "Open QC Document(s)")
            button1: qsTranslate("KeyboardKeys", "Ctrl")
            button3: "O"
        }

        MpvqcShortcut {
            label: qsTranslate("KeyboardKeys", "Save QC Document")
            button1: qsTranslate("KeyboardKeys", "Ctrl")
            button2: "S"
        }

        MpvqcShortcut {
            label: qsTranslate("KeyboardKeys", "Save as new QC Document")
            button1: qsTranslate("KeyboardKeys", "Ctrl")
            button2: qsTranslate("KeyboardKeys", "Shift")
            button3: "S"
        }

        MpvqcShortcut {
            label: qsTranslate("KeyboardKeys", "Open Video")
            button1: qsTranslate("KeyboardKeys", "Ctrl")
            button2: qsTranslate("KeyboardKeys", "Alt")
            button3: "O"
        }

        MpvqcShortcut {
            label: qsTranslate("KeyboardKeys", "Resize Video to Original Resolution")
            button1: qsTranslate("KeyboardKeys", "Ctrl")
            button2: "R"
        }

        MpvqcShortcut {
            label: qsTranslate("KeyboardKeys", "Add Comment")
            button1: "E"
        }

        MpvqcShortcut {
            label: qsTranslate("KeyboardKeys", "Keyboard Shortcuts")
            button1: "?"
        }

        MpvqcShortcut {
            label: qsTranslate("KeyboardKeys", "Quit")
            button1: qsTranslate("KeyboardKeys", "Ctrl")
            button2: "Q"
        }

        MpvqcHeader {
            text: qsTranslate("KeyboardKeys", "Comments")
            Layout.fillWidth: true
        }

        MpvqcShortcut {
            label: qsTranslate("KeyboardKeys", "Edit Comment")
            button1Icon: "qrc:/data/icons/keyboard_return_black_24dp.svg"
        }

        MpvqcShortcut {
            label: qsTranslate("KeyboardKeys", "Copy Comment to Clipboard")
            button1: qsTranslate("KeyboardKeys", "Ctrl")
            button2: "C"
        }

        MpvqcShortcut {
            label: qsTranslate("KeyboardKeys", "Delete Comment")
            button1Icon: "qrc:/data/icons/keyboard_backspace_black_24dp.svg"
            isAndConnection: false
            button2: qsTranslate("KeyboardKeys", "Delete")
        }

        MpvqcShortcut {
            label: qsTranslate("KeyboardKeys", "Previous Comment")
            button1Icon: "qrc:/data/icons/keyboard_arrow_up_black_24dp.svg"
        }

        MpvqcShortcut {
            label: qsTranslate("KeyboardKeys", "Next Comment")
            button1Icon: "qrc:/data/icons/keyboard_arrow_down_black_24dp.svg"
        }

        MpvqcHeader {
            text: qsTranslate("KeyboardKeys", "Video")
            Layout.fillWidth: true
        }

        MpvqcShortcut {
            label: qsTranslate("KeyboardKeys", "Toggle Fullscreen")
            button1: "F"
        }

        MpvqcShortcut {
            label: qsTranslate("KeyboardKeys", "Toggle Play/Pause")
            button1Icon: "qrc:/data/icons/space_bar_black_24dp.svg"
        }

        MpvqcShortcut {
            label: qsTranslate("KeyboardKeys", "Seek Backward by 2 Seconds")
            button1Icon: "qrc:/data/icons/keyboard_arrow_left_black_24dp.svg"
        }

        MpvqcShortcut {
            label: qsTranslate("KeyboardKeys", "Seek Forward by 2 Seconds")
            button1Icon: "qrc:/data/icons/keyboard_arrow_right_black_24dp.svg"
        }

        MpvqcShortcut {
            label: qsTranslate("KeyboardKeys", "Seek Backward by 5 Seconds to Keyframe")
            button1: qsTranslate("KeyboardKeys", "Shift")
            button2Icon: "qrc:/data/icons/keyboard_arrow_left_black_24dp.svg"
        }

        MpvqcShortcut {
            label: qsTranslate("KeyboardKeys", "Seek Forward by 5 Seconds to Keyframe")
            button1: qsTranslate("KeyboardKeys", "Shift")
            button2Icon: "qrc:/data/icons/keyboard_arrow_right_black_24dp.svg"
        }

        MpvqcShortcut {
            label: qsTranslate("KeyboardKeys", "Decrease Volume")
            button1: "9"
        }

        MpvqcShortcut {
            label: qsTranslate("KeyboardKeys", "Increase Volume")
            button1: "0"
        }

        MpvqcShortcut {
            label: qsTranslate("KeyboardKeys", "Toggle Mute")
            button1: "M"
        }

        MpvqcShortcut {
            label: qsTranslate("KeyboardKeys", "Frame Step Backward")
            button1: ","
        }

        MpvqcShortcut {
            label: qsTranslate("KeyboardKeys", "Frame Step Forward")
            button1: "."
        }

        MpvqcShortcut {
            label: qsTranslate("KeyboardKeys", "Cycle Through Subtitle Tracks")
            button1: "J"
        }

        MpvqcShortcut {
            label: qsTranslate("ShortcutsDialog", "Cycle Through Audio Tracks")
            button1: "#"
        }

        MpvqcShortcut {
            label: qsTranslate("KeyboardKeys", "Video Screenshot (Unscaled)")
            button1: "S"
        }

        MpvqcShortcut {
            label: qsTranslate("KeyboardKeys", "Video Screenshot (Scaled)")
            button1: qsTranslate("KeyboardKeys", "Shift")
            button2: "S"
        }

        MpvqcShortcut {
            label: qsTranslate("KeyboardKeys", "Cycle Through Subtitle Render Modes")
            button1: "B"
        }

        MpvqcShortcut {
            label: qsTranslate("KeyboardKeys", "Toggle Video Statistics")
            button1: "I"
        }
    }
}
