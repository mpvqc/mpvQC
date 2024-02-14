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

import "MpvqcStateChanges.js" as MpvqcStateChanges


Item {
    id: root

    property var state: new MpvqcStateChanges.InitialState()

    property url document: ''
    property url video: ''
    property bool saved: true

    function handleChange(): void {
        state = state.handleChange()
    }

    /**
     * @param change {MpvqcStateChanges.ImportChanges}
     */
    function handleImport(change): void {
        state = state.handleImport(change)
    }

    function handleReset(): void {
        state = state.handleReset()
    }

    function handleSave(document: url): void {
        state = state.handleSave(document)
    }

    onStateChanged: {
        root.document = state.document
        root.video = state.video
        root.saved = state.saved
    }

}
