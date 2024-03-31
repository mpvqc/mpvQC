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
import QtTest


MpvqcInputComponent {
    id: objectUnderTest

    width: 400
    height: 400

    validateNewCommentType: input => null
    validateEditingOfCommentType: (input, inputBeingEdited) => null

    TestCase {
        name: "MpvqcInputComponent"
        when: windowShown

        SignalSpy { id: addedSpy; target: objectUnderTest; signalName: 'added' }
        SignalSpy { id: editedSpy; target: objectUnderTest; signalName: 'edited' }

        function test_mode_data() {
            return [
                { tag: 'add', editing: false, objectName: 'MpvqcInputControls::add' },
                { tag: 'edit', editing: true, objectName: 'MpvqcInputControls::edit' },
            ]
        }

        function test_mode(data) {
            objectUnderTest.loader.editing = data.editing
            compare(objectUnderTest.loader.item.objectName, data.objectName)
        }

        function test_signal_data() {
            return [
                { tag: 'added', editing: false, spy: addedSpy },
                { tag: 'edited', editing: true, spy: editedSpy },
            ]
        }

        function test_signal(data) {
            objectUnderTest.loader.editing = data.editing
            objectUnderTest.loader.item.accepted(data.tag)
            compare(data.spy.count, 1)
        }

        function test_editing_started() {
            const textToEdit = 'edit me'

            objectUnderTest.loader.editing = false
            objectUnderTest.startEditing(textToEdit)

            verify(objectUnderTest.loader.editing)
            compare(objectUnderTest.loader.item.text, textToEdit)
        }

        function test_editing_stopped_data() {
            return [
                { tag: 'done', exec: () => objectUnderTest.loader.item.done() },
                { tag: 'reset', exec: () => objectUnderTest.stopEditing() },
            ]
        }

        function test_editing_stopped(data) {
            objectUnderTest.loader.editing = true
            data.exec()
            verify(!objectUnderTest.loader.editing)
        }

    }

}
