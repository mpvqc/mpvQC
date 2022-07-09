/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/


import QtQuick

QtObject {
    property var shouldIgnore

    signal controlPlusCKeys(var event)
    signal controlPlusFKeys(var event)

    signal deleteKey(var event)
    signal returnKey(var event)
    signal backspaceKey(var event)
    signal eKey(var event)
    signal fKey(var event)
    signal escapeKey(var event)

    signal allOtherKeys(var event)

    function handle(event) {
        const accept = function(callable) { event.accepted = true; callable(event) }
        const ignore = function(whatever) { event.accepted = false }

        const key = event.key
        const modifier = event.modifiers

        if (shouldIgnore(key, modifier))
            return ignore(key)

        if (modifier === Qt.ControlModifier && key === Qt.Key_C )
            return accept(controlPlusCKeys)
        if (modifier === Qt.ControlModifier && key === Qt.Key_F )
            return accept(controlPlusFKeys)

        if (modifier === Qt.NoModifier && key === Qt.Key_Delete)
            return accept(deleteKey)
        if (modifier === Qt.NoModifier && key === Qt.Key_Return)
            return accept(returnKey)
        if (modifier === Qt.NoModifier && key === Qt.Key_Backspace)
            return accept(backspaceKey)
        if (modifier === Qt.NoModifier && key === Qt.Key_E)
            return accept(eKey)
        if (modifier === Qt.NoModifier && key === Qt.Key_F)
            return accept(fKey)
        if (modifier === Qt.NoModifier && key === Qt.Key_Escape)
            return accept(escapeKey)

        event.accepted = true
        allOtherKeys(event)
    }
}
