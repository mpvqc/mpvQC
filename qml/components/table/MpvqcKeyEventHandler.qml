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
import helpers


MpvqcKeyEventConsumer {
    shouldIgnore: function(key, modifier) {
        if (key === Qt.Key_Up) return true
        if (key === Qt.Key_Down) return true
    }

    onControlPlusCKeys: {
        console.log("CTRL+C pressed")
    }

    onControlPlusFKeys: {
        console.log("CTRL+F pressed")
    }

    onDeleteKey: {
        console.log("Delete pressed")
    }

    onReturnKey: (event) => {
        if (event.isAutoRepeat) { return }
        globalEvents.requestEditSelectedComment()
    }

    onBackspaceKey: (event) => {
        if (event.isAutoRepeat) { return }
        console.log("Backspace pressed")
    }

    onEKey: {
        globalEvents.requestNewCommentMenu()
    }

    onFKey: (event) => {
        if (event.isAutoRepeat) { return }
        utils.toggleFullScreen()
    }

    onEscapeKey: {
        console.log("Escape pressed")
    }

    onAllOtherKeys: (event) => {
        const command = MpvqcCommandGenerator.generateFrom(event)
        if (command) {
            globalEvents.requestCustomPlayerCommand(command)
        }
    }
}
