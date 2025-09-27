// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick

ListModel {
    ListElement {
        category: "mpvQC"
        label: qsTranslate("ShortcutsDialog", "New QC Document")
        button1: qsTranslate("KeyboardKeys", "Ctrl")
        button2: "N"
    }
    ListElement {
        category: "mpvQC"
        label: qsTranslate("ShortcutsDialog", "Open QC Document(s)")
        button1: qsTranslate("KeyboardKeys", "Ctrl")
        button2: "O"
    }
    ListElement {
        category: "mpvQC"
        label: qsTranslate("ShortcutsDialog", "Save QC Document")
        button1: qsTranslate("KeyboardKeys", "Ctrl")
        button2: "S"
    }
    ListElement {
        category: "mpvQC"
        label: qsTranslate("ShortcutsDialog", "Save as new QC Document")
        button1: qsTranslate("KeyboardKeys", "Ctrl")
        button2: qsTranslate("KeyboardKeys", "Shift")
        button3: "S"
    }
    ListElement {
        category: "mpvQC"
        label: qsTranslate("ShortcutsDialog", "Open Video")
        button1: qsTranslate("KeyboardKeys", "Ctrl")
        button2: qsTranslate("KeyboardKeys", "Alt")
        button3: "O"
    }
    ListElement {
        category: "mpvQC"
        label: qsTranslate("ShortcutsDialog", "Resize Video to Original Resolution")
        button1: qsTranslate("KeyboardKeys", "Ctrl")
        button2: "R"
    }
    ListElement {
        category: "mpvQC"
        label: qsTranslate("ShortcutsDialog", "Add Comment")
        button1: "E"
    }
    ListElement {
        category: "mpvQC"
        label: qsTranslate("ShortcutsDialog", "Keyboard Shortcuts")
        button1: "?"
    }
    ListElement {
        category: "mpvQC"
        label: qsTranslate("ShortcutsDialog", "Open Search")
        button1: qsTranslate("KeyboardKeys", "Ctrl")
        button2: "F"
    }
    ListElement {
        category: "mpvQC"
        label: qsTranslate("ShortcutsDialog", "Undo Previous Action")
        button1: qsTranslate("KeyboardKeys", "Ctrl")
        button2: "Z"
    }
    ListElement {
        category: "mpvQC"
        label: qsTranslate("ShortcutsDialog", "Redo Previous Action")
        button1: qsTranslate("KeyboardKeys", "Ctrl")
        button2: qsTranslate("KeyboardKeys", "Shift")
        button3: "Z"
    }
    ListElement {
        category: "mpvQC"
        label: qsTranslate("ShortcutsDialog", "Quit")
        button1: qsTranslate("KeyboardKeys", "Ctrl")
        button2: "Q"
    }
    ListElement {
        category: qsTranslate("ShortcutsDialog", "Comments")
        label: qsTranslate("ShortcutsDialog", "Edit Comment")
        button1Icon: "qrc:/data/icons/keyboard_return_black_24dp.svg"
    }
    ListElement {
        category: qsTranslate("ShortcutsDialog", "Comments")
        label: qsTranslate("ShortcutsDialog", "Copy Comment to Clipboard")
        button1: qsTranslate("KeyboardKeys", "Ctrl")
        button2: "C"
    }
    ListElement {
        category: qsTranslate("ShortcutsDialog", "Comments")
        label: qsTranslate("ShortcutsDialog", "Delete Comment")
        button1Icon: "qrc:/data/icons/keyboard_backspace_black_24dp.svg"
        isSeparateShortcut: true
        button2: qsTranslate("KeyboardKeys", "Delete")
    }
    ListElement {
        category: qsTranslate("ShortcutsDialog", "Comments")
        label: qsTranslate("ShortcutsDialog", "Previous Comment")
        button1Icon: "qrc:/data/icons/keyboard_arrow_up_black_24dp.svg"
    }
    ListElement {
        category: qsTranslate("ShortcutsDialog", "Comments")
        label: qsTranslate("ShortcutsDialog", "Next Comment")
        button1Icon: "qrc:/data/icons/keyboard_arrow_down_black_24dp.svg"
    }
    ListElement {
        category: qsTranslate("ShortcutsDialog", "Video")
        label: qsTranslate("ShortcutsDialog", "Toggle Fullscreen")
        button1: "F"
    }
    ListElement {
        category: qsTranslate("ShortcutsDialog", "Video")
        label: qsTranslate("ShortcutsDialog", "Toggle Play/Pause")
        button1Icon: "qrc:/data/icons/space_bar_black_24dp.svg"
    }
    ListElement {
        category: qsTranslate("ShortcutsDialog", "Video")
        label: qsTranslate("ShortcutsDialog", "Seek Backward by 2 Seconds")
        button1Icon: "qrc:/data/icons/keyboard_arrow_left_black_24dp.svg"
    }
    ListElement {
        category: qsTranslate("ShortcutsDialog", "Video")
        label: qsTranslate("ShortcutsDialog", "Seek Forward by 2 Seconds")
        button1Icon: "qrc:/data/icons/keyboard_arrow_right_black_24dp.svg"
    }
    ListElement {
        category: qsTranslate("ShortcutsDialog", "Video")
        label: qsTranslate("ShortcutsDialog", "Seek Backward by 5 Seconds to Keyframe")
        button1: qsTranslate("KeyboardKeys", "Shift")
        button2Icon: "qrc:/data/icons/keyboard_arrow_left_black_24dp.svg"
    }
    ListElement {
        category: qsTranslate("ShortcutsDialog", "Video")
        label: qsTranslate("ShortcutsDialog", "Seek Forward by 5 Seconds to Keyframe")
        button1: qsTranslate("KeyboardKeys", "Shift")
        button2Icon: "qrc:/data/icons/keyboard_arrow_right_black_24dp.svg"
    }
    ListElement {
        category: qsTranslate("ShortcutsDialog", "Video")
        label: qsTranslate("ShortcutsDialog", "Decrease Volume")
        button1: "9"
    }
    ListElement {
        category: qsTranslate("ShortcutsDialog", "Video")
        label: qsTranslate("ShortcutsDialog", "Increase Volume")
        button1: "0"
    }
    ListElement {
        category: qsTranslate("ShortcutsDialog", "Video")
        label: qsTranslate("ShortcutsDialog", "Toggle Mute")
        button1: "M"
    }
    ListElement {
        category: qsTranslate("ShortcutsDialog", "Video")
        label: qsTranslate("ShortcutsDialog", "Frame Step Backward")
        button1: ","
    }
    ListElement {
        category: qsTranslate("ShortcutsDialog", "Video")
        label: qsTranslate("ShortcutsDialog", "Frame Step Forward")
        button1: "."
    }
    ListElement {
        category: qsTranslate("ShortcutsDialog", "Video")
        label: qsTranslate("ShortcutsDialog", "Cycle Through Subtitle Tracks")
        button1: "J"
    }
    ListElement {
        category: qsTranslate("ShortcutsDialog", "Video")
        label: qsTranslate("ShortcutsDialog", "Cycle Through Audio Tracks")
        button1: "#"
    }
    ListElement {
        category: qsTranslate("ShortcutsDialog", "Video")
        label: qsTranslate("ShortcutsDialog", "Video Screenshot (Unscaled)")
        button1: "S"
    }
    ListElement {
        category: qsTranslate("ShortcutsDialog", "Video")
        label: qsTranslate("ShortcutsDialog", "Video Screenshot (Scaled)")
        button1: qsTranslate("KeyboardKeys", "Shift")
        button2: "S"
    }
    ListElement {
        category: qsTranslate("ShortcutsDialog", "Video")
        label: qsTranslate("ShortcutsDialog", "Cycle Through Subtitle Render Modes")
        button1: "B"
    }
    ListElement {
        category: qsTranslate("ShortcutsDialog", "Video")
        label: qsTranslate("ShortcutsDialog", "Toggle Video Statistics")
        button1: "I"
    }
}
