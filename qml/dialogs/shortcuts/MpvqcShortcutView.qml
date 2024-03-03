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
import QtQuick.Controls
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

    ScrollBar.horizontal.policy: contentWidth > width ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff
    ScrollBar.vertical.policy: contentHeight > height ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff

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

            text: qsTranslate("ShortcutsDialog", "mpvQC")
            Layout.fillWidth: true
        }

        MpvqcShortcut {
            id: _shortcut

            label: qsTranslate("ShortcutsDialog", "New QC Document")
            button1: qsTranslate("KeyboardKeys", "Ctrl")
            button2: "N"
        }

        MpvqcShortcut {
            label: qsTranslate("ShortcutsDialog", "Open QC Document(s)")
            button1: qsTranslate("KeyboardKeys", "Ctrl")
            button3: "O"
        }

        MpvqcShortcut {
            label: qsTranslate("ShortcutsDialog", "Save QC Document")
            button1: qsTranslate("KeyboardKeys", "Ctrl")
            button2: "S"
        }

        MpvqcShortcut {
            label: qsTranslate("ShortcutsDialog", "Save as new QC Document")
            button1: qsTranslate("KeyboardKeys", "Ctrl")
            button2: qsTranslate("KeyboardKeys", "Shift")
            button3: "S"
        }

        MpvqcShortcut {
            label: qsTranslate("ShortcutsDialog", "Open Video")
            button1: qsTranslate("KeyboardKeys", "Ctrl")
            button2: qsTranslate("KeyboardKeys", "Alt")
            button3: "O"
        }

        MpvqcShortcut {
            label: qsTranslate("ShortcutsDialog", "Resize Video to Original Resolution")
            button1: qsTranslate("KeyboardKeys", "Ctrl")
            button2: "R"
        }

        MpvqcShortcut {
            label: qsTranslate("ShortcutsDialog", "Add Comment")
            button1: "E"
        }

        MpvqcShortcut {
            label: qsTranslate("ShortcutsDialog", "Keyboard Shortcuts")
            button1: "?"
        }

        MpvqcShortcut {
            label: qsTranslate("ShortcutsDialog", "Quit")
            button1: qsTranslate("KeyboardKeys", "Ctrl")
            button2: "Q"
        }

        MpvqcHeader {
            text: qsTranslate("ShortcutsDialog", "Video")
            Layout.fillWidth: true
        }

        MpvqcShortcut {
            label: qsTranslate("ShortcutsDialog", "Toggle Fullscreen")
            button1: "F"
        }

        MpvqcShortcut {
            label: qsTranslate("ShortcutsDialog", "Toggle Play/Pause")
            button1: "␣"
        }

        MpvqcShortcut {
            label: qsTranslate("ShortcutsDialog", "Seek Backward by 2 Seconds")
            button1: "←"
        }

        MpvqcShortcut {
            label: qsTranslate("ShortcutsDialog", "Seek Forward by 2 Seconds")
            button1: "→"
        }

        MpvqcShortcut {
            label: qsTranslate("ShortcutsDialog", "Seek Backward by 5 Seconds to Keyframe")
            button1: qsTranslate("KeyboardKeys", "Shift")
            button2: "←"
        }

        MpvqcShortcut {
            label: qsTranslate("ShortcutsDialog", "Seek Forward by 5 Seconds to Keyframe")
            button1: qsTranslate("KeyboardKeys", "Shift")
            button2: "→"
        }

        MpvqcShortcut {
            label: qsTranslate("ShortcutsDialog", "Decrease Volume")
            button1: "9"
        }

        MpvqcShortcut {
            label: qsTranslate("ShortcutsDialog", "Increase Volume")
            button1: "0"
        }

        MpvqcShortcut {
            label: qsTranslate("ShortcutsDialog", "Toggle Mute")
            button1: "M"
        }

        MpvqcShortcut {
            label: qsTranslate("ShortcutsDialog", "Frame Step Backward")
            button1: ","
        }

        MpvqcShortcut {
            label: qsTranslate("ShortcutsDialog", "Frame Step Forward")
            button1: "."
        }

        MpvqcShortcut {
            label: qsTranslate("ShortcutsDialog", "Cycle Through Subtitle Tracks")
            button1: "J"
        }

        MpvqcShortcut {
            label: qsTranslate("ShortcutsDialog", "Cycle Through Audio Tracks")
            button1: "#"
        }

        MpvqcShortcut {
            label: qsTranslate("ShortcutsDialog", "Video Screenshot (Unscaled)")
            button1: "S"
        }

        MpvqcShortcut {
            label: qsTranslate("ShortcutsDialog", "Video Screenshot (Scaled)")
            button1: qsTranslate("KeyboardKeys", "Shift")
            button2: "S"
        }

        MpvqcShortcut {
            label: qsTranslate("ShortcutsDialog", "Cycle Through Subtitle Render Modes")
            button1: "B"
        }

        MpvqcShortcut {
            label: qsTranslate("ShortcutsDialog", "Toggle Video Statistics")
            button1: "I"
        }
    }
}
