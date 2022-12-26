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

import shared


Item {
    id: root

    required property var mpvqcApplication
    required property var mpvqcCommentTable

    property bool haveComments: root.mpvqcCommentTable.count > 0
    property bool currentlyEditing: root.mpvqcCommentTable.editMode
    property bool currentlyFullscreen: root.mpvqcApplication.fullscreen

    property var newCommentMenu: MpvqcNewCommentMenu {
        mpvqcApplication: root.mpvqcApplication
    }

    signal deleteCommentPressed()
    signal copyToClipboardPressed()

    Shortcut {
        sequence: 'e'
        autoRepeat: false

        onActivated: root.newCommentMenu.popupMenu()
    }

    Shortcut {
        sequence: 'f'
        autoRepeat: false

        onActivated: root.mpvqcApplication.toggleFullScreen()
    }

    Shortcut {
        sequence: 'return'
        autoRepeat: false
        enabled: !currentlyFullscreen && haveComments && !currentlyEditing

        onActivated: root.mpvqcCommentTable.startEditing()
    }

    Shortcut {
        sequence: 'Esc'
        autoRepeat: false
        enabled: currentlyFullscreen

        onActivated: root.mpvqcApplication.disableFullScreen()
    }

    Shortcut {
        sequence: 'delete'
        autoRepeat: false
        enabled: !currentlyFullscreen && haveComments

        onActivated: root.deleteCommentPressed()
    }

    Shortcut {
        sequence: 'backspace'
        autoRepeat: false
        enabled: !currentlyFullscreen && haveComments

        onActivated: root.deleteCommentPressed()
    }

    Shortcut {
        sequence: 'ctrl+c'
        autoRepeat: false
        enabled: !currentlyFullscreen && haveComments && !currentlyEditing

        onActivated: root.copyToClipboardPressed()
    }

    Shortcut {
        sequence: 'ctrl+f'
        autoRepeat: false
        enabled: !currentlyFullscreen && !currentlyEditing

        onActivated: console.warn('[WARN]', 'ctrl+f pressed', )
    }

    function ignore(event: KeyEvent): bool {
        const key = event.key
        const modifiers = event.modifiers
        return key === Qt.Key_Up
          ||   key === Qt.Key_Down
          || ( key === Qt.Key_Return && modifiers === Qt.NoModifier )
          || ( key === Qt.Key_Escape && modifiers === Qt.NoModifier )
          || ( key === Qt.Key_Delete && modifiers === Qt.NoModifier )
          || ( key === Qt.Key_Backspace && modifiers === Qt.NoModifier )
          || ( key === Qt.Key_F && modifiers === Qt.ControlModifier )
          || ( key === Qt.Key_C && modifiers === Qt.ControlModifier )
    }

}
